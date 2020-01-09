class Mapper:
    def __init__(self):
        self.__mapping = {}

    def __add(self, source, dest):
        self.__mapping[source] = dest

    def remap_key(self, source, dest):
        self.__add(source, dest)

    def remap(self, items):
        return [self.__exec(item) for item in items]

    def __exec(self, src_dict):
        dest = {}

        if not src_dict:
            raise AttributeError(
                'The source dictionary cannot be empty or None')

        for key, value in src_dict.items():
            try:
                new_key = self.__mapping[key]
                dest[new_key] = value
            except KeyError:
                dest[key] = value
        return dest
