import re

from bs4 import BeautifulSoup

from cliweather.core import ForecastType, Request, UnitConverter, Unit, Forecast, Mapper


class WeatherComParser:
    def __init__(self):
        self.__forecast = {
            ForecastType.TODAY: self.__today_forecast,
            ForecastType.FIVEDAYS: self.__five_and_ten_days_forecast,
            ForecastType.TENDAYS: self.__five_and_ten_days_forecast,
            ForecastType.WEEKEND: self.__weekend_forecast}

        self.__request = Request(
            'https://weather.com/en-Au/weather/{forecast}/l/{area}')

        self.__temp_regex = re.compile(r'(\d+)\D{,2}(\d+)')
        self.__only_digits_regex = re.compile(r'\d+')

        self.__unit_converter = UnitConverter(Unit.CELSIUS)

    def __get_data(self, container, search_items):
        scraped_data = {}

        for key, value in search_items.items():
            result = container.find(value, class_=key)
            data = result.get_text() if result else None
            if data:
                scraped_data[key] = data

        return scraped_data

    def __parse(self, container, criteria):
        results = (self.__get_data(item, criteria)
                   for item in container.children)

        return [result for result in results if result]

    def __parse_list_forecast(self, content, args):
        criteria = {'date-time': 'span',
                    'day-detail': 'span',
                    'description': 'td',
                    'temp': 'td',
                    'wind': 'td',
                    'humidity': 'td'}

        bs = BeautifulSoup(content, 'html.parser')
        forecast_data = bs.find('table', class_='twc-table')
        container = forecast_data.tbody

        return self.__parse(container, criteria)

    def __prepare_data(self, results, args):
        forecast_result = []
        self.__unit_converter.dest_unit = args.unit

        for item in results:
            match = self.__temp_regex.search(item['temp'])
            if match:
                high_temp, low_temp = match.groups()

            try:
                date_info = item['weather-cell']
                if date_info.startswith('Today'):
                    date_time, day_detail = date_info[:5], date_info[5:]
                else:
                    date_time, day_detail = date_info[:3], date_info[3:]
                item['date-time'] = date_time
                item['day-detail'] = day_detail
            except KeyError:
                pass

            day_forecast = Forecast(
                self.__unit_converter.convert(item['temp']),
                item['humidity'],
                item['wind'],
                high_temp=self.__unit_converter.convert(high_temp),
                low_temp=self.__unit_converter.convert(low_temp),
                description=item['description'].strip(),
                forecast_date=f'{item["date-time"]} {item["day-detail"]}',
                forecast_type=self.__forecast_type)
            forecast_result.append(day_forecast)

        return forecast_result

    def __clear_str_number(self, str_number):
        result = self.__only_digits_regex.match(str_number)
        return result.group() if result else '--'

    def __get_additional_info(self, content):
        data = tuple(item.td.span.get_text()
                     for item in content.table.tbody.children)

        return data[:2]

    def __today_forecast(self, args):
        criteria = {'today_nowcard-temp': 'div',
                    'today_nowcard-phrase': 'div',
                    'today_nowcard-hilo': 'div'}
        content = self.__request.fetch_data(args.forecast_option.value,
                                            args.area_code)

        bs = BeautifulSoup(content, 'html.parser')
        container = bs.find('section', class_='today_nowcard-container')
        weather_conditions = self.__parse(container, criteria)
        if len(weather_conditions) < 1:
            raise Exception('Could not parse weather forecast for today.')

        weather_info = weather_conditions[0]
        temp_regex = re.compile(r'H\s+(\d+|\-{,2}).+L\s+(\d+|\-{,2})')
        temp_info = temp_regex.search(weather_info['today_nowcard-hilo'])
        high_temp, low_temp = temp_info.groups()
        side = container.find('div', class_='today_nowcard-sidecar')
        wind, humidity = self.__get_additional_info(side)
        curr_temp = self.__clear_str_number(weather_info['today_nowcard-temp'])
        self.__unit_converter.dest_unit = args.unit
        td_forecast = Forecast(self.__unit_converter.convert(curr_temp),
                               humidity,
                               wind,
                               high_temp=self.__unit_converter.convert(
                                   high_temp),
                               low_temp=self.__unit_converter.convert(
                                   low_temp),
                               description=weather_info['today_nowcard-phrase'])
        return [td_forecast]

    def __five_and_ten_days_forecast(self, args):
        content = self.__request.fetch_data(args.forecast_option.value,
                                            args.area_code)
        results = self.__parse_list_forecast(content, args)
        return self.__prepare_data(results, args)

    def __weekend_forecast(self, args):
        criteria = {'weather-cell': 'header',
                    'temp': 'p',
                    'weather-phrase': 'h3',
                    'wind-conditions': 'p',
                    'humidity': 'p'}
        mapper = Mapper()
        mapper.remap_key('wind-conditions', 'wind')
        mapper.remap_key('weather-phrase', 'description')

        content = self.__request.fetch_data(args.forecast_option.value,
                                            args.area_code)

        bs = BeautifulSoup(content, 'html.parser')

        forecast_data = bs.find('section', class_='ls-mod')
        container = forecast_data.div.div

        partial_results = self.__parse(container, criteria)
        results = mapper.remap(partial_results)
        return self.__prepare_data(results, args)

    def run(self, args):
        self.__forecast_type = args.forecast_option
        forecast_function = self.__forecast[args.forecast_option]
        return forecast_function(args)
