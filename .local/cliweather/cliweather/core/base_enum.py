from enum import Enum


class BaseEnum(Enum):
    # pylint: disable=E0213
    def _generate_next_value_(name, start, count, last_value):
        return name
