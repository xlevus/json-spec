__all__ = ['extract_parser', 'validate_parser', 'check_parser',
           'parser_base', 'parse_document', 'parse_schema',
           'parse_fragment', 'parse_target', 'parse_pointer']

import argparse
import errno
import os
import stat
import sys
from textwrap import dedent
from jsonspec import driver


def parser_base(txt):
    """docstring for parser_base"""
    description, _, epilog = txt.lstrip().partition('\n\n')

    if description:
        description = description.replace('\n', ' ')

    if epilog:
        epilog = dedent(epilog).replace('    ', '  ').replace('::\n\n', ':\n')
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog)
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


def parse_document(args, parser):
    if args.document_json:
        doc = driver.loads(args.document_json)
        setattr(args, 'document', doc)
        return doc
    elif args.document_file:
        doc = read_file(args.document_file, 'document')
        setattr(args, 'document', doc)
        return doc
    else:
        mode = os.fstat(0).st_mode
        if stat.S_ISFIFO(mode):
            # cat doc.json | cmd
            doc = driver.load(sys.stdin)
            setattr(args, 'document', doc)
            return doc
        elif stat.S_ISREG(mode):
            # cmd < doc.json
            doc = driver.load(sys.stdin)
            setattr(args, 'document', doc)
            return doc

    parser.error('document is required')


def parse_schema(args, parser):
    if args.schema_json:
        try:
            doc = driver.loads(args.schema_json)
            setattr(args, 'schema', doc)
            return doc
        except Exception:
            raise Exception('could not parse schema, is it a file maybe?')
    elif args.schema_file:
        doc = read_file(args.schema_file, 'schema')
        setattr(args, 'schema', doc)
        return doc

    parser.error('schema is required')


def parse_fragment(args, parser):
    if args.fragment_json:
        try:
            doc = driver.loads(args.fragment_json)
            setattr(args, 'fragment', doc)
            return doc
        except Exception:
            raise Exception('could not parse fragment, is it a file maybe?')
    elif args.fragment_file:
        doc = read_file(args.fragment_file, 'fragment')
        setattr(args, 'fragment', doc)
        return doc

    parser.error('fragment is required')


def parse_pointer(args, parser):
    if args.pointer:
        target = args.pointer
        if target.startswith('#'):
            target = target[1:]
        setattr(args, 'pointer', target)
        return target

    parser.error('target is required')


def parse_target(args, parser):
    if args.target_pointer:
        target = args.target_pointer
        if target.startswith('#'):
            target = target[1:]
        setattr(args, 'target', target)
        return target

    parser.error('target is required')


def read_file(filename, placeholder=None):
    placeholder = placeholder or 'file'
    try:
        return driver.load(open(filename, 'r'))
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise Exception('{} {} does not exists'.format(placeholder,
                                                           filename))
    except Exception as error:
        raise error
