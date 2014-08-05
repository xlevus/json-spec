from __future__ import print_function

from functools import wraps
import logging
import sys

try:
    from termcolor import colored
except ImportError:

    def colored(string, *args, **kwargs):
        return string


def disable_logging(func):
    """
    Temporary disable logging.
    """
    handler = logging.NullHandler()

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger()
        logger.addHandler(handler)
        resp = func(*args, **kwargs)
        logger.removeHandler(handler)
        return resp
    return wrapper


def format_output(func):
    """
    Format output.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as error:
            print(colored(error, 'red'), file=sys.stderr)
            sys.exit(1)
        else:
            print(response)
            sys.exit(0)
    return wrapper


class Command(object):
    def get_parser(self):
        raise NotImplementedError()

    def parse(self, args=None):
        args = self.get_parser.parse(args)
        return args

    @disable_logging
    @format_output
    def __call__(self, args=None):
        return self.run(args)
