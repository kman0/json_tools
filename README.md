= JSON tools =

Manipulate JSON documents using [[http://tools.ietf.org/html/draft-ietf-appsawg-json-patch-02|"JSON patch" format]].

== Installation ==

{{{pip install json_tools}}}

== Usage ==

There are two ways of using //json_tools//:
# As a CLI utilty.
# As a Python module.

=== CLI interface ===

After you've installed //json_tools// you can access it via {{{json}}} command in the shell. It provides a pretty simple yet powerfull interface to manipule JSON documents:
* **print** - pretty-print your JSON optionally colorizing it

**Options:**

{{{-c, --color}}} Colorizes output.

{{{
#!bash
echo '{"Hello": ["w", "o", "r", "l", "d", "!"]}' | json print
}}}

{{{
#!json
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
}}}

* **diff** - calculate difference between two JSON documents as a JSON patch:

**Options:**

{{{-c, --color}}} Colorizes output.

{{{
#!bash

json diff doc1.json doc2.json
}}}

{{{
#!json

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
}}}

* **patch** - modify the JSON document using JSON patch and print the resulting document to STDOUT.

{{{
#!bash

json diff doc.json patch.json
}}}

=== Pythonic interface ===

TBD


== Planned features ==

# Support more JSON patch options: currently //json_tools// only supports //add//, //remove// and //replace//.
# Add an option to sort documents' fields alphabetically (they're being output in the order of Python dict iteration at the moment).
# Make **diff** output more human readable (not JSONish).
# Improve documentation.