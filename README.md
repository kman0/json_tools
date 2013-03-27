JSON tools
==========

Manipulate JSON documents using ["JSON patch" format][1].

Installation
------------

    $ pip install json_tools

Usage
-----

There are two ways of using *json_tools*:

 1. As a CLI utilty.
 2. As a Python module.

### CLI interface

After you've installed *json_tools* you can access it via `json` command in the
shell. It provides a pretty simple yet powerful interface to manipulate JSON 
documents:

 *  **print** - pretty-print your JSON optionally colorizing it

    **Options:**

    `-c, --color` Colorizes output.

        $ echo '{"Hello": ["w", "o", "r", "l", "d", "!"]}' | json print
        {
            "Hello": [
                "w",
                "o",
                "r",
                "l",
                "d",
                "!"
            ]
        }

 *  **diff** - calculate difference between two JSON documents as a JSON patch:

    **Options:**

    `-c, --color` Colorizes output.

        $ json diff doc1.json doc2.json
        [
            {
                "add": "/lol",
                "value": "wut"
            },
            {
                "remove": "/some/field",
                "prev": {
                    "compound": "value"
                }
            }
        ]

 *  **patch** - modify the JSON document using JSON patch and print the 
    resulting document to STDOUT.

        $ json diff doc.json patch.json

### Pythonic interface

TBD


Planned features
----------------

 1. Support more JSON patch options: currently *json_tools* only supports 
    *add*, *remove* and *replace*.
 1. Add an option to sort documents' fields alphabetically (they're being 
    output in the order of Python dict iteration at the moment).
 1. Make **diff** output more human readable (not JSONish).
 1. Improve documentation.


  [1]: http://tools.ietf.org/html/draft-ietf-appsawg-json-patch-02
