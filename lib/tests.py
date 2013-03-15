#!/usr/bin/env python
#-*- coding:utf-8 -*-
import logging
import pprint
from json_tools import diff, patch


def test_simple_diff():
    local = {'foo': 1, 'bar': 2}
    other = {'foo': 2, 'baz': 3}
    delta = diff(local, other)
    logging.debug('delta == \\ \n%s', pprint.pformat(delta))
    assert delta == [
        {'prev': 1, 'value': 2, 'replace': '/foo'},
        {'prev': 2, 'remove': '/bar'},
        {'add': '/baz', 'value': 3}
    ]

def test_nested_diff():
    local = {'foo': {'bar': 1, 'baz': 2}}
    other = {'foo': {'bar': 2, 'qux': 3}}
    delta = diff(local, other)
    logging.debug('delta == \\ \n%s', pprint.pformat(delta))
    assert delta == [
        {'prev': 2, 'remove': '/foo/baz'},
        {'prev': 1, 'replace': '/foo/bar', 'value': 2},
        {'add': '/foo/qux', 'value': 3}
    ]

def test_nested_array_diff():
    local = {'foo': [{'bar': 1, 'baz': 2}, {'qux': 3, 'quux': 4}]}
    other = {'foo': [{'bar': 2, 'qux': 3}, {'quux': 4, 'corge': 5}]}
    delta = diff(local, other)
    logging.debug('delta == \\ \n%s', pprint.pformat(delta))
    assert delta == [
        {'prev': 2, 'remove': '/foo/1/baz'},
        {'prev': 1, 'replace': '/foo/1/bar', 'value': 2},
        {'add': '/foo/1/qux', 'value': 3},
        {'prev': 3, 'remove': '/foo/2/qux'},
        {'add': '/foo/2/corge', 'value': 5}
    ]
    # Currently fails because delta == [
    #     {'prev': 2, 'remove': '/baz'},
    #     {'prev': 1, 'replace': '/bar', 'value': 2},
    #     {'add': '/qux', 'value': 3},
    #     {'prev': 3, 'remove': '/qux'},
    #     {'add': '/corge', 'value': 5}
    # ]

def test_simple_patch():
    local = {'foo': 1, 'bar': 2}
    other = {'foo': 2, 'baz': 3}
    delta = diff(local, other)
    patched = patch(local, delta)
    logging.debug('patched == \\ \n%s', pprint.pformat(patched))
    assert patched == other

def test_nested_patch():
    local = {'foo': {'bar': 1, 'baz': 2}}
    other = {'foo': {'bar': 2, 'qux': 3}}
    delta = diff(local, other)
    patched = patch(local, delta)
    logging.debug('patched == \\ \n%s', pprint.pformat(patched))
    assert patched == other

def test_nested_array_patch():
    local = {'foo': [{'bar': 1, 'baz': 2}, {'qux': 3, 'quux': 4}]}
    other = {'foo': [{'bar': 2, 'qux': 3}, {'quux': 4, 'corge': 5}]}
    delta = diff(local, other)
    patched = patch(local, delta)
    logging.debug('patched == \\ \n%s', pprint.pformat(patched))
    assert patched == other
    # Currently fails because patched == {
    #     'bar': 2,
    #     'corge': 5,
    #     'foo': [{'bar': 1, 'baz': 2}, {'quux': 4, 'qux': 3}]
    # }


if __name__ == '__main__':
    import nose
    nose.runmodule()
