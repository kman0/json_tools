#!/usr/bin/env python
#-*- coding:utf-8 -*-


""" Functions to patch JSON documents.
"""

from __future__ import print_function

from path import split


def add(data, path, value, replace=False):
    """ Add a new value to the given JSON document @a data at JSON-path @a path.

        If the the path is already used, then no changes are made.
    """

    nodes = split(path)
    d = data
    for pos, (t, name) in enumerate(nodes[:-1]):
        if t == 'object-field' and not isinstance(d, dict):
            raise ValueError('Expected a JSON object for {}'.format(name))
        elif t == 'array-index' and not isinstance(d, list):
            raise ValueError('Expected a JSON array for {}'.format(name))

        try:
            d = d[name]
        except IndexError:
            while len(d) < name:
                d.append(None)
            if nodes[pos + 1][0] == 'array-index':
                d.append([])
            else:
                d.append({})
            d = d[name]
        except:
            next_t, next_v = nodes[pos + 1]
            if next_t == 'object-field':
                d[name] = {}
            elif next_t == 'array-index':
                d[name] = []
            d = d[name]

    t, name = nodes[-1]
    if t == 'array-index':
        while len(d) < name + 1:
            d.append(None)
    d[name] = value

    return data


def replace(data, path, value):
    """ Replace the value of the document's subelement at @a path with value
        @a value.
    """
    return add(data, path, value, True)


def remove(data, path):
    nodes = split(path)
    d = data
    for t, name in nodes[:-1]:
        if t == 'object-field':
            if not isinstance(d, dict) or name not in d:
                return
        elif t == 'array-index':
            if not isinstance(d, list) or name >= len(d):
                return
        d = d[name]
    try:
        del d[nodes[-1][1]]
    except:
        pass
    return data


def patch(data, patch):
    """ Apply a JSON @a patch to the given JSON object @a data.
    """
    for change in patch:
        if 'add' in change:
            add(data, change['add'], change['value'])
        elif 'replace' in change:
            replace(data, change['replace'], change['value'])
        elif 'remove' in change:
            remove(data, change['remove'])
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Apply a JSON patch")
    parser.add_argument('-c', '--colorize', action='store_true',
                        help='Colorize the output')
    parser.add_argument('-i', '--inplace', action='store_true',
                        help='Edit the input file inplace')
    parser.add_argument('input', help='Path to the file to be patched')
    parser.add_argument('patch', nargs='*', help='Path to a single patch')
    args = parser.parse_args()

    import json
    from sys import stderr
    from printer import print_json

    try:
        with open(args.input) as f:
            data = json.load(f)
    except IOError:
        print('Local not found', file=stderr)
        exit(-1)

    for patch_file in args.patch:
        try:
            with open(patch_file) as f:
                _patch = json.load(f)
        except IOError:
            print('Patch not found', file=stderr)
            exit(-1)

        data = patch(data, _patch)

    if not args.inplace:
        print_json(data, args.colors)
    else:
        with open(args.input, 'w') as f:
            json.dump(data, f, indent=4)
