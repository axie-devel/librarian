#!/usr/bin/env python
# -*- coding: utf-8

"""
This scripts reads the table of footnote qualifiers from Redmine
and produces contents of fn_qualifiers.py – a list of valid qualifiers.
"""
from __future__ import print_function, unicode_literals

from lxml import etree
from six.moves.urllib.request import urlopen

url = 'http://redmine.nowoczesnapolska.org.pl/projects/wl-publikacje/wiki/Lista_skr%C3%B3t%C3%B3w'

parser = etree.HTMLParser()
tree = etree.parse(urlopen(url), parser)

print("""\
# -*- coding: utf-8
\"""
List of standard footnote qualifiers.
This file is generated by scripts/fn_qualifiers_list_from_wiki.py,
do not edit it.
\"""
from __future__ import unicode_literals


FN_QUALIFIERS = {""")

for td in tree.findall('//td'):
    print(("    '%s': '%s'," % (
        td[0].text.replace('\\', '\\\\').replace("'", "\\'"),
        td[0].tail.strip(' -').replace('\\', '\\\\').replace("'", "\\'")
    )))

print("""    }""")
