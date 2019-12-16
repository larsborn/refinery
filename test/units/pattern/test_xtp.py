#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .. import TestUnitBase


class TestPatternExtractor(TestUnitBase):

    def test_extraction_environment_variable(self):
        unit = self.load('evar')
        self.assertEqual(b'%TEST%', unit(B'This is a %TEST% with environment variable.'))

    def test_extraction_domain_01(self):
        unit = self.load('domain', whitelist=False)
        self.assertEqual(b'google.com', unit(b'Just use google.com. It is the best.'))

    def test_extraction_domain_02(self):
        unit = self.load('domain', whitelist=False)
        self.assertEqual(b'evil.c2server.com', unit(b'\x00\x00\x00evil.c2server.com\x52\x50\x00\x00\x00'))

    def test_extraction_domain_03(self):
        unit = self.load('domain', whitelist=False)
        self.assertEqual(b'evil.c2server.com', unit(b'\x00\x00\x00evil.c2server.com\x50\x00\x00\x00\x00'))

    def test_extraction_domain_04(self):
        unit = self.load('domain', whitelist=False)
        self.assertEqual(b'', unit(
            b'\x00ios_base::eofbit set\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'b\x00u\x00i\x00l\x00d\x00.\x00b\x00i\x00n\x00\x00\x00\x00\x00\x00\x00')
        )
