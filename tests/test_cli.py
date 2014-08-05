"""
    tests.tests_cli
    ~~~~~~~~~~~~~~~

"""

import os
import os.path
import pytest
from subprocess import Popen, PIPE
from jsonspec import cli
import json
from . import TestCase, move_cwd


scenarii = [
    # Pointer scenarii

    # inline json
    ("""json-extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'""", True),
    ("""echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/1'""", True),
    ("""json-extract '#/foo/2' --document-json='{"foo": ["bar", "baz"]}'""", False),
    ("""echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/2'""", False),

    # existant file
    ("""cat fixtures/first.data1.json | json-extract '#/name'""", True),
    ("""json-extract '#/name' < fixtures/first.data1.json""", True),
    ("""json-extract '#/name' --document-file=fixtures/first.data1.json""", True),

    # existant file, but pointer does not match
    ("""cat fixtures/first.data1.json | json-extract '#/foo/bar'""", False),
    ("""json-extract '#/foo/bar' < fixtures/first.data1.json""", False),
    ("""json-extract '#/foo/bar' --document-file=fixtures/first.data1.json""", False),

    # inexistant file
    ("""json-extract '#/foo/1' --document-file=doc.json""", False),
    ("""json-extract '#/foo/1' < doc.json""", False),
    ("""cat doc.json | json-extract '#/foo/1'""", False),

    # Schema scenarii

    #
    ("""json-validate --schema-file=fixtures/three.schema.json < fixtures/three.data1.json""", False),
    ("""json-validate --schema-file=fixtures/three.schema.json < fixtures/three.data2.json""", True),
]


@pytest.mark.parametrize('cmd, success', scenarii)
def test_cli(cmd, success):
    with move_cwd():
        proc = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

    if success and ret > 0:
        assert False, (ret, stdout, stderr)
    if not success and ret == 0:
        assert False, (ret, stdout, stderr)


add_scenes = [
    ('#/foo/bar', {'foo': 'bar'}, {'baz': 'quux'}, False, None),
    ('#/baz', {'foo': 'bar'}, 'quux', True, {'foo': 'bar', 'baz': 'quux'}),
]


@pytest.mark.parametrize('pointer, document, fragment, success, result', add_scenes)
def test_cli_add(pointer, document, fragment, success, result):
    with move_cwd():
        doc, frag = json.dumps(document), json.dumps(fragment)
        proc = Popen(['json-add', pointer, '--document-json', doc, '--fragment-json', frag],
                     stderr=PIPE,
                     stdout=PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

        if success and ret == 0 and json.loads(stdout.decode('utf-8')) == result:
            return
        if not success and ret > 0:
            return

        assert False, (ret, stdout, stderr, success, result)


remove_scenes = [
    ('#/foo/bar', {'foo': 'bar'}, False, None),
    ('#/baz', {'foo': 'bar', 'baz': 'bar'}, True, {'foo': 'bar'}),
]


@pytest.mark.parametrize('pointer, document, success, result', remove_scenes)
def test_cli_remove(pointer, document, success, result):
    with move_cwd():
        doc = json.dumps(document)
        proc = Popen(['json-remove', pointer, '--document-json', doc],
                     stderr=PIPE,
                     stdout=PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

        if success and ret == 0 and json.loads(stdout.decode('utf-8')) == result:
            return
        if not success and ret > 0:
            return

        assert False, (ret, stdout, stderr, success, result)


replace_scenes = [
    ('#/bar', {'foo': 'bar'}, 'quux', False, None),
    ('#/foo', {'foo': 'bar'}, 'quux', True, {'foo': 'quux'}),
]


@pytest.mark.parametrize('pointer, document, fragment, success, result', replace_scenes)
def test_cli_replace(pointer, document, fragment, success, result):
    with move_cwd():
        doc, frag = json.dumps(document), json.dumps(fragment)
        proc = Popen(['json-replace', pointer, '--document-json', doc, '--fragment-json', frag],
                     stderr=PIPE,
                     stdout=PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

        if success and ret == 0 and json.loads(stdout.decode('utf-8')) == result:
            return
        if not success and ret > 0:
            return

        assert False, (ret, stdout, stderr, success, result)


move_scenes = [
    ('#/bar', {'foo': 'bar'}, '#/foo', False, None),
    ('#/foo', {'foo': 'bar'}, '#/baz', True, {'baz': 'bar'}),
]


@pytest.mark.parametrize('pointer, document, target, success, result', move_scenes)
def test_cli_move(pointer, document, target, success, result):
    with move_cwd():
        doc = json.dumps(document)
        proc = Popen(['json-move', pointer, '--document-json', doc, '--target-pointer', target],
                     stderr=PIPE,
                     stdout=PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

        if success and ret == 0 and json.loads(stdout.decode('utf-8')) == result:
            return
        if not success and ret > 0:
            return

        assert False, (ret, stdout, stderr, success, result)


copy_scenes = [
    ('#/bar', {'foo': 'bar'}, '#/foo', False, None),
    ('#/foo', {'foo': 'bar'}, '#/baz', True, {'foo': 'bar', 'baz': 'bar'}),
]


@pytest.mark.parametrize('pointer, document, target, success, result', copy_scenes)
def test_cli_copy(pointer, document, target, success, result):
    with move_cwd():
        doc = json.dumps(document)
        proc = Popen(['json-copy', pointer, '--document-json', doc, '--target-pointer', target],
                     stderr=PIPE,
                     stdout=PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

        if success and ret == 0 and json.loads(stdout.decode('utf-8')) == result:
            return
        if not success and ret > 0:
            return

        assert False, (ret, stdout, stderr, success, result)
