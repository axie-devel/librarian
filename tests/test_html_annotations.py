# -*- coding: utf-8
from __future__ import unicode_literals

from StringIO import StringIO
import tempfile
from librarian.parser import WLDocument
from librarian.html import extract_annotations
from lxml import etree
from nose.tools import eq_


def _test_annotation(expected, got, name):
    assert got[0].startswith('anchor-'), "%s: Unexpected anchor: '%s', should begin with 'anchor-'" % (name, got[0])
    eq_(expected[0], got[1], "%s: Unexpected type, expected '%s', got '%s'" % (name, expected[0], got[1]))
    eq_(expected[1], got[2], "%s: Unexpected qualifier, expected '%s', got '%s'" % (name, expected[1], got[2]))
    eq_(expected[2], got[3], "%s: Unexpected text representation, expected '%s', got '%s'" % (name, expected[2], got[3]))
    exp_html = '<div class="fn-%s">%s</div>' % (expected[0], expected[3])
    eq_(exp_html, got[4], "%s: Unexpected html representation, expected '%s', got '%s'" % (name, exp_html, got[4]))
    

def test_annotations():
    annotations = (

        ('<pe/>', (
            'pe',
            None, 
            '',
            '<p></p>'
            ),
            'Empty footnote'),

        (
         '<pr>Definiendum --- definiens.</pr>', (
            'pr',
            None, 
            'Definiendum \u2014 definiens.', 
            '<p>Definiendum \u2014 definiens.</p>'
            ),
            'Plain footnote.'),

        ('<pt><slowo_obce>Definiendum</slowo_obce> --- definiens.</pt>', (
            'pt',
            None, 
            'Definiendum \u2014 definiens.', 
            '<p><em class="foreign-word">Definiendum</em> \u2014 definiens.</p>'
            ),
            'Standard footnote.'),

        ('<pr>Definiendum (łac.) --- definiens.</pr>', (
            'pr',
            'łac.', 
            'Definiendum (łac.) \u2014 definiens.', 
            '<p>Definiendum (łac.) \u2014 definiens.</p>'
            ),
            'Plain footnote with qualifier'),

        ('<pe><slowo_obce>Definiendum</slowo_obce> (łac.) --- definiens.</pe>', (
            'pe',
            'łac.', 
            'Definiendum (łac.) \u2014 definiens.', 
            '<p><em class="foreign-word">Definiendum</em> (łac.) \u2014 definiens.</p>'
            ),
            'Standard footnote with qualifier.'),

        ('<pt> <slowo_obce>Definiendum</slowo_obce> (daw.) --- definiens.</pt>', (
            'pt',
            'daw.', 
            'Definiendum (daw.) \u2014 definiens.', 
            '<p> <em class="foreign-word">Definiendum</em> (daw.) \u2014 definiens.</p>'
            ),
            'Standard footnote with leading whitespace and qualifier.'),

        ('<pr>Definiendum (łac.) --- <slowo_obce>definiens</slowo_obce>.</pr>', (
            'pr',
            'łac.', 
            'Definiendum (łac.) \u2014 definiens.', 
            '<p>Definiendum (łac.) \u2014 <em class="foreign-word">definiens</em>.</p>'
            ),
            'Plain footnote with qualifier and some emphasis.'),

        ('<pe><slowo_obce>Definiendum</slowo_obce> (łac.) --- <slowo_obce>definiens</slowo_obce>.</pe>', (
            'pe',
            'łac.', 
            'Definiendum (łac.) \u2014 definiens.', 
            '<p><em class="foreign-word">Definiendum</em> (łac.) \u2014 <em class="foreign-word">definiens</em>.</p>'
            ),
            'Standard footnote with qualifier and some emphasis.'),

    )

    xml_src = '''<utwor><akap> %s </akap></utwor>''' % "".join(
        t[0] for t in annotations)
    html = WLDocument.from_string(xml_src, parse_dublincore=False).as_html().get_file()
    res_annotations = list(extract_annotations(html))

    for i, (src, expected, name) in enumerate(annotations):
        yield _test_annotation, expected, res_annotations[i], name
