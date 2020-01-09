import os
import importlib
import re
import inspect


def load_parsers(directory):
    # get a list of files in the directory
    filenames = (filename.replace('.py', '')
                 for filename in os.listdir(directory)
                 if not filename.startswith('__'))

    pattern = re.compile(r'.+parser$', re.I)

    # import the files as modules
    modules = (importlib.import_module(f'.{filename}', 'cliweather.parsers')
               for filename in filenames
               if pattern.match(filename))

    # create a dict of class names and their implementations
    classes = {key: value
               for module in modules
               for key, value in inspect.getmembers(module, inspect.isclass)
               if pattern.match(key)}

    return classes
