from datetime import date

from .forecast_type import ForecastType


class Forecast:
    def __init__(self,
                 current_temp,
                 humidity,
                 wind,
                 high_temp=None,
                 low_temp=None,
                 description='',
                 forecast_date=None,
                 forecast_type=ForecastType.TODAY):
        self.current_temp = current_temp
        self.high_temp = high_temp
        self.low_temp = low_temp
        self.humidity = humidity
        self.wind = wind.strip()
        self.description = description
        self.forecast_type = forecast_type
        if forecast_date:
            self.forecast_date = forecast_date
        else:
            self.forecast_date = date.today().strftime('%a %b %d')

    def __str__(self):
        temperature = None
        offset = ' ' * 4

        if self.forecast_type == ForecastType.TODAY:
            temperature = (f'{offset}{self.current_temp}\xb0\n'
                           f'{offset}High {self.high_temp}\xb0 / Low {self.low_temp}\xb0 ')
        else:
            temperature = (
                f'{offset}High {self.high_temp}\xb0 / Low {self.low_temp}\xb0 ')

        return (f'>> {self.forecast_date}\n'
                f'{temperature}'
                f'({self.description})\n'
                f'{offset}Wind: '
                f'{self.wind} / Humidity: {self.humidity}\n')
