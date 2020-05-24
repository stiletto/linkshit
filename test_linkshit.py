from __future__ import unicode_literals
#
# Copyright 2012 Stiletto <blasux@blasux.ru>
#
# Licensed under the MIT License.
#
# coding: utf-8
from linkshit import linkparse

import unittest


class LinkShitTest(unittest.TestCase):
    def check_parsed(self, expected_elements, parsed_elements):
        for i, (expected, actual) in enumerate(zip(expected_elements, parsed_elements)):
            assert expected == actual, (i, expected, actual)

    def test_linkshit(self):
        parsed = linkparse(
            'Ololo lololo #67AB3D fyuck http://bnw.im/u/lol http://ompldr.org/vZGZ1aw damn #ABCDEF/XYZ shit-@govnoeb'
        )
        self.check_parsed([
            'Ololo lololo ',
            ('msg', '#67AB3D', '67AB3D'),
            ' fyuck ',
            ('url', 'http://bnw.im/u/lol', 'http://bnw.im/u/lol', 'http://bnw.im/u/lol'),
            ' ',
            ('url', 'http://ompldr.org/vZGZ1aw', 'http://ompldr.org/vZGZ1aw', 'http://ompldr.org/vZGZ1aw'),
            ' damn ',
            ('msg', '#ABCDEF/XYZ', 'ABCDEF/XYZ'),
            ' shit-',
            ('user', '@govnoeb', 'govnoeb'),
        ], parsed)

    def test_clip(self):
        parsed = linkparse('Hello, http://example.com/fuuuuuuuuuuuuuuuuuuuuuck-yooooooooou.html !')
        self.check_parsed([
            'Hello, ',
            (
                'url',
                'http://example.com/fuuuuuuuuuuuuuuuuuuuuuck-yooooooooou.html',
                'http://example.com/fuuuuuuuuuuuuuuuuuuuuuck-yooooooooou.html',
                'http://example.com/fuuuuuuuuuuuuuuuuuuuu.....oooou.html'
            ),
            ' !'
        ], parsed)


if __name__ == "__main__":
    unittest.main()
