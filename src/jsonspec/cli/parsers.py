__all__ = ['parser_base', 'parse_document', 'parse_schema',
           'parse_fragment', 'parse_target', 'parse_pointer',
           'parser_pointer', 'parser_document', 'parser_fragment',
           'parser_schema', ]

import argparse
import errno
import os
import stat
import sys
from textwrap import dedent
from jsonspec import driver


def parser_pointer(parser):
    parser.add_argument('pointer', help='a valid json pointer')


def parser_document(parser):
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')


def parser_fragment(parser):
    parser.add_argument('--fragment-json')
    parser.add_argument('--fragment-file')


def parser_schema(parser):
    parser.add_argument('--schema-json', help='json structure')
    parser.add_argument('--schema-file', help='filename')


def parser_base(txt):
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
