__all__ = ['extract_parser', 'validate_parser']

import argparse
from textwrap import dedent


def add_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Add a fragment to a json document.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--fragment-json')
    parser.add_argument('--fragment-file')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def replace_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Replace the value of pointer.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--fragment-json')
    parser.add_argument('--fragment-file')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def remove_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Remove the value of pointer.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
              %(prog)s '#/foo/1' --document-file=doc.json
              %(prog)s '#/foo/1' < doc.json

            """))

    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def move_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Removes the value at a specified location '
                    'and adds it to the target location.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
              %(prog)s '#/foo/1' --document-file=doc.json
              %(prog)s '#/foo/1' < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('-t', '--target-pointer', help='target pointer')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def copy_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Copies the value at a specified location '
                    'to the target location.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
              %(prog)s '#/foo/1' --document-file=doc.json
              %(prog)s '#/foo/1' < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('-t', '--target-pointer', help='target pointer')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def extract_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Extract a fragment from a json document.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
              %(prog)s '#/foo/1' --document-file=doc.json
              %(prog)s '#/foo/1' < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def check_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Tests that a value at the target location '
                    'is equal to a specified value.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1' --fragment-file=fragment.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
              %(prog)s '#/foo/1' --fragment-file=fragment.json < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--fragment-json')
    parser.add_argument('--fragment-file')
    return parser


def validate_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Validate document against a schema.',
        epilog=dedent("""\
            examples:
              %(prog)s --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s --schema-file=schema.json
              %(prog)s --schema-file=schema.json --document-file=doc.json
              %(prog)s --schema-file=schema.json < doc.json

            """))
    parser.add_argument('--document-json')
    parser.add_argument('--document-file')
    parser.add_argument('--schema-json')
    parser.add_argument('--schema-file')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser
