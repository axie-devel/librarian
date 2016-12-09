# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import urllib
from urllib2 import urlopen, URLError

from librarian import DCNS, BuildError
from .. import Cover


class EvensCover(Cover):
    format_name = u"Evens cover image"
    width = 1024
    height = 1365
    author_top = 900
    title_top = 30
    logo_bottom = 100

    def __init__(self, doc, format=None, width=None, height=None):
        super(EvensCover, self).__init__(doc, format=format, width=width, height=height)
        self.doc = doc

    def set_images(self, ctx):
        cover_url = self.doc.meta.get(DCNS('relation.coverimage.url'))[0]
        if cover_url.startswith('file://'):
            cover_url = ctx.files_path + urllib.quote(cover_url[7:])
        try:
            self.background_img = urlopen(cover_url)
        except URLError:
            raise BuildError('Cannot open the cover image: %s' % cover_url)

        if getattr(ctx, 'cover_logo', None):
            self.logo_width = 150
            self.logo_file = urlopen(ctx.cover_logo)
