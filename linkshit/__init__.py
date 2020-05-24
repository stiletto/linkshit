from __future__ import unicode_literals
#
# Copyright 2014 Stiletto <blasux@blasux.ru>
# Copyright 2012 Kagami Hiiragi <kagami@genshiken.org>
#
# Licensed under the MIT License.
#
# coding: utf-8

import re
import sys

if sys.version_info > (3, 6):
    import typing


_URL_RE = re.compile(r"""\b((?:([\w-]+):(/{1,3})|www[.])(?:(?:(?:[^\s&()]|&amp;|&quot;)*(?:[^!"#$%&'()*+,.:;<=>?@\[\]^`{|}~\s]))|(?:\((?:[^\s&()]|&amp;|&quot;)*\)))+)""")  # noqa: E501
_USER_RE = re.compile(r"""(?:(?<=[\s\W])|^)@([0-9A-Za-z-]+)""")
_MSG_RE = re.compile(r"""(?:(?<=[\s\W])|^)#([0-9A-Za-z]+(?:/[0-9A-Za-z]+)?)""")

shittypes = (
    ('url', _URL_RE, lambda m: (m.group(1), clip_long_url(m))),
    ('msg', _MSG_RE, lambda m: (m.group(1),)),
    ('user', _USER_RE, lambda m: (m.group(1),)),
)


def clip_long_url(m):
    # type: (re.Match) -> str
    """Clip long urls."""
    # It may be done much better.
    url = m.group(1)
    if len(url) > 55:
        url = url[:40] + "....." + url[-10:]
    return url


class LinkParser(object):
    def __init__(self, types=shittypes):
        # noqa: E501 type: (LinkParser, typing.Iterable[typing.Tuple[str, re.Pattern, typing.Callable[[re.Match], typing.Tuple]]]) -> None
        self.types = types

    def parse(self, text):
        # type: (LinkParser, str) -> typing.Iterator[typing.Union[str, typing.Tuple]]
        # Who the fuck wrote this piece of shit?
        # TODO: Refactor this shit.
        pos = 0
        texlen = len(text)
        while pos < texlen:
            mins = texlen
            minm = None
            for typ, reg, handler in self.types:
                m = reg.search(text[pos:])
                if m is None:
                    continue
                s = m.start()
                if s < mins:
                    mins = s
                    minm = (typ, m, handler)
            if not minm:
                yield text[pos:]
                return
            else:
                # TODO: Fix first empty value.
                yield text[pos:pos + mins]
                yield ((minm[0], minm[1].group(0)) + minm[2](minm[1]))
                pos = pos + minm[1].end()


_shitparser = LinkParser()


def linkparse(text):
    return _shitparser.parse(text)
