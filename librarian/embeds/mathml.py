# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lxml import etree
import six
from librarian import get_resource
from . import TreeEmbed, create_embed, downgrades_to


class MathML(TreeEmbed):
    @downgrades_to('application/x-latex')
    def to_latex(self):
        xslt = etree.parse(get_resource('res/embeds/mathml/mathml2latex.xslt'))
        output = self.tree.xslt(xslt)
        return create_embed('application/x-latex', data=six.text_type(output))
