from .bases import Target

# The jsonspec.operations doesn't use the same keywords as
# the RFC. This table of lambdas provides a keyword mapping.

DEFAULT_OPS = {
    'check': lambda doc, path, value: doc.check(path, value, True),
    'remove': lambda doc, path: doc.remove(path),
    'add': lambda doc, path, value: doc.add(path, value),
    'replace': lambda doc, path, value: doc.replace(path, value),

    # 'from' is a reserved word in python.
    'move': lambda doc, **kwargs: doc.move(kwargs['from'], kwargs['path']),
    'copy': lambda doc, **kwargs: doc.copy(kwargs['from'], kwargs['path']),
}


class UnknownOperation(ValueError):
    pass


def patch(document, *operations, **ops):
    """
    Apply a JSON-Patch object(s) to a document.

    :param document: the document to apply operations to
    :type document: dict
    :param *operations: JSON-Patch operations to apply to document
    :type *operations: dict
    :param **ops: Additional non-standard operations to enable.
    :type **ops: function
    :return: patched document
    :rtype: dict

    >>> doc = {
        'a': {
            'b': {
                'c': 'foo',
            }
        }
    }

    >>> patch(doc,
              {'op': 'test', 'path': '/a/b/c', 'value': 'foo'},
              {'op': 'remove': 'path': '/a/b/c'},
              { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] },
              { "op": "replace", "path": "/a/b/c", "value": 42 },
              { "op": "move", "from": "/a/b/c", "path": "/a/b/d" },
              { "op": "copy", "from": "/a/b/d", "path": "/a/b/e" })
    {'a': {'b': {'d': 42, 'e': 42} } }

    Operations can be disabled and additional non-standard operations can be
    implemented with keyword arguments.

    >>> def make_fish(document, path, fish='trout'):
    >>>    return document.replace(path, fish)
    >>>
    >>> patch(doc,
              {'op': 'make_fish', 'path': '/a/b/c'},
              make_fish=make_fish, test=False)
    {'a': {'b': {'c': 'trout'} } }
    """
    op_table = DEFAULT_OPS.copy()
    op_table.update(ops)

    document = Target(document)

    for op in operations:
        op_name = op.pop('op', None)
        func = op_table.get(op_name)
        if not func:
            raise UnknownOperation("Operation '%s' is not known." % op_name)
        document = func(document, **op)
    return document.document

