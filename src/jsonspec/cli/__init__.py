from __future__ import print_function

from jsonspec import driver
from .bases import Command, disable_logging, format_output
from .parsers import *  # noqa


class AddCommand(Command):
    """Add a fragment to a json document.

    examples::

        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser_document(parser)
        parser_fragment(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_pointer(args, parser)
        parse_document(args, parser)
        parse_fragment(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import add, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            response = add(args.document, args.pointer, args.fragment)
            return driver.dumps(response, indent=args.indent)
        except Error as error:
            raise Exception(error)
        except ParseError as error:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class RemoveCommand(Command):
    """Replace the value of pointer.

    examples:
      %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
      echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
      %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
      %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json

    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser_document(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_document(args, parser)
        parse_pointer(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import remove, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            response = remove(args.document, args.pointer)
            return driver.dumps(response, indent=args.indent)
        except Error:
            raise Exception('{} does not match'.format(args.pointer))
        except ParseError:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class ReplaceCommand(Command):
    """Replace a fragment to a json document.

    examples::

        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser_document(parser)
        parser_fragment(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_document(args, parser)
        parse_fragment(args, parser)
        parse_pointer(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import replace, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            response = replace(args.document, args.pointer, args.fragment)
            return driver.dumps(response, indent=args.indent)
        except Error as error:
            raise Exception(error)
        except ParseError as error:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class MoveCommand(Command):
    """Removes the value at a specified location and adds it to the target location.

    examples::

        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser.add_argument('-t', '--target-pointer', help='target pointer')
        parser_document(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_document(args, parser)
        parse_target(args, parser)
        parse_pointer(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import move, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            response = move(args.document, args.target, args.pointer)
            return driver.dumps(response, indent=args.indent)
        except Error as error:
            raise Exception(error)
        except ParseError as error:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class CopyCommand(Command):
    """Copies the value at a specified location to the target location.

    examples::

        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser.add_argument('-t', '--target-pointer', help='target pointer')
        parser_document(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_document(args, parser)
        parse_target(args, parser)
        parse_pointer(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import copy, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            response = copy(args.document, args.target, args.pointer)
            return driver.dumps(response, indent=args.indent)
        except Error as error:
            raise Exception(error)
        except ParseError as error:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class CheckCommand(Command):
    """Tests that a value at the target location is equal to a specified value.

    examples::

        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
        %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser_document(parser)
        parser_fragment(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_pointer(args, parser)
        parse_document(args, parser)
        parse_fragment(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.operations import check, Error
        from jsonspec.pointer import ParseError
        args = self.parse(args)

        try:
            if check(args.document, args.pointer, args.fragment):
                return 'It validates'
            else:
                raise Exception('It does not validate')
        except Error as error:
            raise Exception('It does not validate')
        except ParseError as error:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class ExtractCommand(Command):
    """Extract a fragment from a json document.

    examples::

        %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
        %(prog)s '#/foo/1' --document-file=doc.json
        %(prog)s '#/foo/1' < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_pointer(parser)
        parser_document(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_pointer(args, parser)
        parse_document(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.pointer import extract
        from jsonspec.pointer import ExtractError, ParseError
        args = self.parse(args)
        try:
            response = extract(args.document, args.pointer)
            return driver.dumps(response, indent=args.indent)
        except ExtractError:
            raise Exception('{} does not match'.format(args.pointer))
        except ParseError:
            raise Exception('{} is not a valid pointer'.format(args.pointer))


class ValidateCommand(Command):
    """Validate document against a schema.

    examples::

        %(prog)s --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
        echo '{"foo": ["bar", "baz"]}' | %(prog)s --schema-file=schema.json
        %(prog)s --schema-file=schema.json --document-file=doc.json
        %(prog)s --schema-file=schema.json < doc.json
    """

    def get_parser(self):
        parser = parser_base(self.__doc__)
        parser_document(parser)
        parser_schema(parser)
        parser.add_argument('--indent', type=int, help='indentation')
        return parser

    def parse(self, args=None):
        parser = self.get_parser()
        args = parser.parse_args(args)
        parse_document(args, parser)
        parse_schema(args, parser)
        return args

    def run(self, args=None):
        from jsonspec.validators import load
        from jsonspec.validators import ValidationError
        args = self.parse(args)
        try:
            validated = load(args.schema).validate(args.document)
            return driver.dumps(validated, indent=args.indent)
        except ValidationError as error:
            msg = 'document does not validate with schema.\n\n'
            for pointer, reasons in error.flatten.items():
                msg += '  {}\n'.format(pointer)
                for reason in reasons:
                    msg += '    - reason {}\n'.format(reason)
                msg += '\n'
            raise Exception(msg)


add_cmd = AddCommand()
check_cmd = CheckCommand()
copy_cmd = CopyCommand()
extract_cmd = ExtractCommand()
move_cmd = MoveCommand()
remove_cmd = RemoveCommand()
replace_cmd = ReplaceCommand()
validate_cmd = ValidateCommand()
