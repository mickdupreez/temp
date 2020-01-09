from .unit import Unit


class UnitConverter:
    def __init__(self, parser_default_unit, dest_unit=None):
        self.__parser_default_unit = parser_default_unit
        self.dest_unit = dest_unit

        self.__convert_functions = {Unit.CELSIUS: self.__to_celsius,
                                    Unit.FAHRENHEIT: self.__to_fahrenheit}

    def convert(self, temp):
        try:
            temperature = float(temp)
        except ValueError:
            return 0

        if (self.dest_unit == self.__parser_default_unit or not self.dest_unit):
            return self.__format_results(temperature)

        func = self.__convert_functions[self.dest_unit]

        result = func(temperature)

        return self.__format_results(result)

    def __format_results(self, value):
        return int(value) if value.is_integer() else f'{value:.1f}'

    def __to_celsius(self, fahrenheit_temp):
        return (fahrenheit_temp - 32) * 5/9

    def __to_fahrenheit(self, celsius_temp):
        return (celsius_temp * 9/5) + 32
