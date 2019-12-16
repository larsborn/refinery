#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import KeyDerivation
from ... import RefineryException

from typing import List

import struct
import itertools


__all__ = ['ucrypt']


SPT0 = (
    0x00820200, 0x00020000, 0x80800000, 0x80820200, 0x00800000, 0x80020200, 0x80020000, 0x80800000,
    0x80020200, 0x00820200, 0x00820000, 0x80000200, 0x80800200, 0x00800000, 0x00000000, 0x80020000,
    0x00020000, 0x80000000, 0x00800200, 0x00020200, 0x80820200, 0x00820000, 0x80000200, 0x00800200,
    0x80000000, 0x00000200, 0x00020200, 0x80820000, 0x00000200, 0x80800200, 0x80820000, 0x00000000,
    0x00000000, 0x80820200, 0x00800200, 0x80020000, 0x00820200, 0x00020000, 0x80000200, 0x00800200,
    0x80820000, 0x00000200, 0x00020200, 0x80800000, 0x80020200, 0x80000000, 0x80800000, 0x00820000,
    0x80820200, 0x00020200, 0x00820000, 0x80800200, 0x00800000, 0x80000200, 0x80020000, 0x00000000,
    0x00020000, 0x00800000, 0x80800200, 0x00820200, 0x80000000, 0x80820000, 0x00000200, 0x80020200
)

SPT1 = (
    0x10042004, 0x00000000, 0x00042000, 0x10040000, 0x10000004, 0x00002004, 0x10002000, 0x00042000,
    0x00002000, 0x10040004, 0x00000004, 0x10002000, 0x00040004, 0x10042000, 0x10040000, 0x00000004,
    0x00040000, 0x10002004, 0x10040004, 0x00002000, 0x00042004, 0x10000000, 0x00000000, 0x00040004,
    0x10002004, 0x00042004, 0x10042000, 0x10000004, 0x10000000, 0x00040000, 0x00002004, 0x10042004,
    0x00040004, 0x10042000, 0x10002000, 0x00042004, 0x10042004, 0x00040004, 0x10000004, 0x00000000,
    0x10000000, 0x00002004, 0x00040000, 0x10040004, 0x00002000, 0x10000000, 0x00042004, 0x10002004,
    0x10042000, 0x00002000, 0x00000000, 0x10000004, 0x00000004, 0x10042004, 0x00042000, 0x10040000,
    0x10040004, 0x00040000, 0x00002004, 0x10002000, 0x10002004, 0x00000004, 0x10040000, 0x00042000
)

SPT2 = (
    0x41000000, 0x01010040, 0x00000040, 0x41000040, 0x40010000, 0x01000000, 0x41000040, 0x00010040,
    0x01000040, 0x00010000, 0x01010000, 0x40000000, 0x41010040, 0x40000040, 0x40000000, 0x41010000,
    0x00000000, 0x40010000, 0x01010040, 0x00000040, 0x40000040, 0x41010040, 0x00010000, 0x41000000,
    0x41010000, 0x01000040, 0x40010040, 0x01010000, 0x00010040, 0x00000000, 0x01000000, 0x40010040,
    0x01010040, 0x00000040, 0x40000000, 0x00010000, 0x40000040, 0x40010000, 0x01010000, 0x41000040,
    0x00000000, 0x01010040, 0x00010040, 0x41010000, 0x40010000, 0x01000000, 0x41010040, 0x40000000,
    0x40010040, 0x41000000, 0x01000000, 0x41010040, 0x00010000, 0x01000040, 0x41000040, 0x00010040,
    0x01000040, 0x00000000, 0x41010000, 0x40000040, 0x41000000, 0x40010040, 0x00000040, 0x01010000
)

SPT3 = (
    0x00100402, 0x04000400, 0x00000002, 0x04100402, 0x00000000, 0x04100000, 0x04000402, 0x00100002,
    0x04100400, 0x04000002, 0x04000000, 0x00000402, 0x04000002, 0x00100402, 0x00100000, 0x04000000,
    0x04100002, 0x00100400, 0x00000400, 0x00000002, 0x00100400, 0x04000402, 0x04100000, 0x00000400,
    0x00000402, 0x00000000, 0x00100002, 0x04100400, 0x04000400, 0x04100002, 0x04100402, 0x00100000,
    0x04100002, 0x00000402, 0x00100000, 0x04000002, 0x00100400, 0x04000400, 0x00000002, 0x04100000,
    0x04000402, 0x00000000, 0x00000400, 0x00100002, 0x00000000, 0x04100002, 0x04100400, 0x00000400,
    0x04000000, 0x04100402, 0x00100402, 0x00100000, 0x04100402, 0x00000002, 0x04000400, 0x00100402,
    0x00100002, 0x00100400, 0x04100000, 0x04000402, 0x00000402, 0x04000000, 0x04000002, 0x04100400
)

SPT4 = (
    0x02000000, 0x00004000, 0x00000100, 0x02004108, 0x02004008, 0x02000100, 0x00004108, 0x02004000,
    0x00004000, 0x00000008, 0x02000008, 0x00004100, 0x02000108, 0x02004008, 0x02004100, 0x00000000,
    0x00004100, 0x02000000, 0x00004008, 0x00000108, 0x02000100, 0x00004108, 0x00000000, 0x02000008,
    0x00000008, 0x02000108, 0x02004108, 0x00004008, 0x02004000, 0x00000100, 0x00000108, 0x02004100,
    0x02004100, 0x02000108, 0x00004008, 0x02004000, 0x00004000, 0x00000008, 0x02000008, 0x02000100,
    0x02000000, 0x00004100, 0x02004108, 0x00000000, 0x00004108, 0x02000000, 0x00000100, 0x00004008,
    0x02000108, 0x00000100, 0x00000000, 0x02004108, 0x02004008, 0x02004100, 0x00000108, 0x00004000,
    0x00004100, 0x02004008, 0x02000100, 0x00000108, 0x00000008, 0x00004108, 0x02004000, 0x02000008
)

SPT5 = (
    0x20000010, 0x00080010, 0x00000000, 0x20080800, 0x00080010, 0x00000800, 0x20000810, 0x00080000,
    0x00000810, 0x20080810, 0x00080800, 0x20000000, 0x20000800, 0x20000010, 0x20080000, 0x00080810,
    0x00080000, 0x20000810, 0x20080010, 0x00000000, 0x00000800, 0x00000010, 0x20080800, 0x20080010,
    0x20080810, 0x20080000, 0x20000000, 0x00000810, 0x00000010, 0x00080800, 0x00080810, 0x20000800,
    0x00000810, 0x20000000, 0x20000800, 0x00080810, 0x20080800, 0x00080010, 0x00000000, 0x20000800,
    0x20000000, 0x00000800, 0x20080010, 0x00080000, 0x00080010, 0x20080810, 0x00080800, 0x00000010,
    0x20080810, 0x00080800, 0x00080000, 0x20000810, 0x20000010, 0x20080000, 0x00080810, 0x00000000,
    0x00000800, 0x20000010, 0x20000810, 0x20080800, 0x20080000, 0x00000810, 0x00000010, 0x20080010
)

SPT6 = (
    0x00001000, 0x00000080, 0x00400080, 0x00400001, 0x00401081, 0x00001001, 0x00001080, 0x00000000,
    0x00400000, 0x00400081, 0x00000081, 0x00401000, 0x00000001, 0x00401080, 0x00401000, 0x00000081,
    0x00400081, 0x00001000, 0x00001001, 0x00401081, 0x00000000, 0x00400080, 0x00400001, 0x00001080,
    0x00401001, 0x00001081, 0x00401080, 0x00000001, 0x00001081, 0x00401001, 0x00000080, 0x00400000,
    0x00001081, 0x00401000, 0x00401001, 0x00000081, 0x00001000, 0x00000080, 0x00400000, 0x00401001,
    0x00400081, 0x00001081, 0x00001080, 0x00000000, 0x00000080, 0x00400001, 0x00000001, 0x00400080,
    0x00000000, 0x00400081, 0x00400080, 0x00001080, 0x00000081, 0x00001000, 0x00401081, 0x00400000,
    0x00401080, 0x00000001, 0x00001001, 0x00401081, 0x00400001, 0x00401080, 0x00401000, 0x00001001
)

SPT7 = (
    0x08200020, 0x08208000, 0x00008020, 0x00000000, 0x08008000, 0x00200020, 0x08200000, 0x08208020,
    0x00000020, 0x08000000, 0x00208000, 0x00008020, 0x00208020, 0x08008020, 0x08000020, 0x08200000,
    0x00008000, 0x00208020, 0x00200020, 0x08008000, 0x08208020, 0x08000020, 0x00000000, 0x00208000,
    0x08000000, 0x00200000, 0x08008020, 0x08200020, 0x00200000, 0x00008000, 0x08208000, 0x00000020,
    0x00200000, 0x00008000, 0x08000020, 0x08208020, 0x00008020, 0x08000000, 0x00000000, 0x00208000,
    0x08200020, 0x08008020, 0x08008000, 0x00200020, 0x08208000, 0x00000020, 0x00200020, 0x08008000,
    0x08208020, 0x00200000, 0x08200000, 0x08000020, 0x00208000, 0x00008020, 0x08008020, 0x08200000,
    0x00000020, 0x08208000, 0x00208020, 0x00000000, 0x08000000, 0x08200020, 0x00008000, 0x00208020
)

SKBC0 = (
    0x00000000, 0x00000010, 0x20000000, 0x20000010, 0x00010000, 0x00010010, 0x20010000, 0x20010010,
    0x00000800, 0x00000810, 0x20000800, 0x20000810, 0x00010800, 0x00010810, 0x20010800, 0x20010810,
    0x00000020, 0x00000030, 0x20000020, 0x20000030, 0x00010020, 0x00010030, 0x20010020, 0x20010030,
    0x00000820, 0x00000830, 0x20000820, 0x20000830, 0x00010820, 0x00010830, 0x20010820, 0x20010830,
    0x00080000, 0x00080010, 0x20080000, 0x20080010, 0x00090000, 0x00090010, 0x20090000, 0x20090010,
    0x00080800, 0x00080810, 0x20080800, 0x20080810, 0x00090800, 0x00090810, 0x20090800, 0x20090810,
    0x00080020, 0x00080030, 0x20080020, 0x20080030, 0x00090020, 0x00090030, 0x20090020, 0x20090030,
    0x00080820, 0x00080830, 0x20080820, 0x20080830, 0x00090820, 0x00090830, 0x20090820, 0x20090830
)

SKBC1 = (
    0x00000000, 0x02000000, 0x00002000, 0x02002000, 0x00200000, 0x02200000, 0x00202000, 0x02202000,
    0x00000004, 0x02000004, 0x00002004, 0x02002004, 0x00200004, 0x02200004, 0x00202004, 0x02202004,
    0x00000400, 0x02000400, 0x00002400, 0x02002400, 0x00200400, 0x02200400, 0x00202400, 0x02202400,
    0x00000404, 0x02000404, 0x00002404, 0x02002404, 0x00200404, 0x02200404, 0x00202404, 0x02202404,
    0x10000000, 0x12000000, 0x10002000, 0x12002000, 0x10200000, 0x12200000, 0x10202000, 0x12202000,
    0x10000004, 0x12000004, 0x10002004, 0x12002004, 0x10200004, 0x12200004, 0x10202004, 0x12202004,
    0x10000400, 0x12000400, 0x10002400, 0x12002400, 0x10200400, 0x12200400, 0x10202400, 0x12202400,
    0x10000404, 0x12000404, 0x10002404, 0x12002404, 0x10200404, 0x12200404, 0x10202404, 0x12202404
)

SKBC2 = (
    0x00000000, 0x00000001, 0x00040000, 0x00040001, 0x01000000, 0x01000001, 0x01040000, 0x01040001,
    0x00000002, 0x00000003, 0x00040002, 0x00040003, 0x01000002, 0x01000003, 0x01040002, 0x01040003,
    0x00000200, 0x00000201, 0x00040200, 0x00040201, 0x01000200, 0x01000201, 0x01040200, 0x01040201,
    0x00000202, 0x00000203, 0x00040202, 0x00040203, 0x01000202, 0x01000203, 0x01040202, 0x01040203,
    0x08000000, 0x08000001, 0x08040000, 0x08040001, 0x09000000, 0x09000001, 0x09040000, 0x09040001,
    0x08000002, 0x08000003, 0x08040002, 0x08040003, 0x09000002, 0x09000003, 0x09040002, 0x09040003,
    0x08000200, 0x08000201, 0x08040200, 0x08040201, 0x09000200, 0x09000201, 0x09040200, 0x09040201,
    0x08000202, 0x08000203, 0x08040202, 0x08040203, 0x09000202, 0x09000203, 0x09040202, 0x09040203
)

SKBC3 = (
    0x00000000, 0x00100000, 0x00000100, 0x00100100, 0x00000008, 0x00100008, 0x00000108, 0x00100108,
    0x00001000, 0x00101000, 0x00001100, 0x00101100, 0x00001008, 0x00101008, 0x00001108, 0x00101108,
    0x04000000, 0x04100000, 0x04000100, 0x04100100, 0x04000008, 0x04100008, 0x04000108, 0x04100108,
    0x04001000, 0x04101000, 0x04001100, 0x04101100, 0x04001008, 0x04101008, 0x04001108, 0x04101108,
    0x00020000, 0x00120000, 0x00020100, 0x00120100, 0x00020008, 0x00120008, 0x00020108, 0x00120108,
    0x00021000, 0x00121000, 0x00021100, 0x00121100, 0x00021008, 0x00121008, 0x00021108, 0x00121108,
    0x04020000, 0x04120000, 0x04020100, 0x04120100, 0x04020008, 0x04120008, 0x04020108, 0x04120108,
    0x04021000, 0x04121000, 0x04021100, 0x04121100, 0x04021008, 0x04121008, 0x04021108, 0x04121108
)

SKBD0 = (
    0x00000000, 0x10000000, 0x00010000, 0x10010000, 0x00000004, 0x10000004, 0x00010004, 0x10010004,
    0x20000000, 0x30000000, 0x20010000, 0x30010000, 0x20000004, 0x30000004, 0x20010004, 0x30010004,
    0x00100000, 0x10100000, 0x00110000, 0x10110000, 0x00100004, 0x10100004, 0x00110004, 0x10110004,
    0x20100000, 0x30100000, 0x20110000, 0x30110000, 0x20100004, 0x30100004, 0x20110004, 0x30110004,
    0x00001000, 0x10001000, 0x00011000, 0x10011000, 0x00001004, 0x10001004, 0x00011004, 0x10011004,
    0x20001000, 0x30001000, 0x20011000, 0x30011000, 0x20001004, 0x30001004, 0x20011004, 0x30011004,
    0x00101000, 0x10101000, 0x00111000, 0x10111000, 0x00101004, 0x10101004, 0x00111004, 0x10111004,
    0x20101000, 0x30101000, 0x20111000, 0x30111000, 0x20101004, 0x30101004, 0x20111004, 0x30111004
)

SKBD1 = (
    0x00000000, 0x08000000, 0x00000008, 0x08000008, 0x00000400, 0x08000400, 0x00000408, 0x08000408,
    0x00020000, 0x08020000, 0x00020008, 0x08020008, 0x00020400, 0x08020400, 0x00020408, 0x08020408,
    0x00000001, 0x08000001, 0x00000009, 0x08000009, 0x00000401, 0x08000401, 0x00000409, 0x08000409,
    0x00020001, 0x08020001, 0x00020009, 0x08020009, 0x00020401, 0x08020401, 0x00020409, 0x08020409,
    0x02000000, 0x0A000000, 0x02000008, 0x0A000008, 0x02000400, 0x0A000400, 0x02000408, 0x0A000408,
    0x02020000, 0x0A020000, 0x02020008, 0x0A020008, 0x02020400, 0x0A020400, 0x02020408, 0x0A020408,
    0x02000001, 0x0A000001, 0x02000009, 0x0A000009, 0x02000401, 0x0A000401, 0x02000409, 0x0A000409,
    0x02020001, 0x0A020001, 0x02020009, 0x0A020009, 0x02020401, 0x0A020401, 0x02020409, 0x0A020409
)

SKBD2 = (
    0x00000000, 0x00000100, 0x00080000, 0x00080100, 0x01000000, 0x01000100, 0x01080000, 0x01080100,
    0x00000010, 0x00000110, 0x00080010, 0x00080110, 0x01000010, 0x01000110, 0x01080010, 0x01080110,
    0x00200000, 0x00200100, 0x00280000, 0x00280100, 0x01200000, 0x01200100, 0x01280000, 0x01280100,
    0x00200010, 0x00200110, 0x00280010, 0x00280110, 0x01200010, 0x01200110, 0x01280010, 0x01280110,
    0x00000200, 0x00000300, 0x00080200, 0x00080300, 0x01000200, 0x01000300, 0x01080200, 0x01080300,
    0x00000210, 0x00000310, 0x00080210, 0x00080310, 0x01000210, 0x01000310, 0x01080210, 0x01080310,
    0x00200200, 0x00200300, 0x00280200, 0x00280300, 0x01200200, 0x01200300, 0x01280200, 0x01280300,
    0x00200210, 0x00200310, 0x00280210, 0x00280310, 0x01200210, 0x01200310, 0x01280210, 0x01280310
)

SKBD3 = (
    0x00000000, 0x04000000, 0x00040000, 0x04040000, 0x00000002, 0x04000002, 0x00040002, 0x04040002,
    0x00002000, 0x04002000, 0x00042000, 0x04042000, 0x00002002, 0x04002002, 0x00042002, 0x04042002,
    0x00000020, 0x04000020, 0x00040020, 0x04040020, 0x00000022, 0x04000022, 0x00040022, 0x04040022,
    0x00002020, 0x04002020, 0x00042020, 0x04042020, 0x00002022, 0x04002022, 0x00042022, 0x04042022,
    0x00000800, 0x04000800, 0x00040800, 0x04040800, 0x00000802, 0x04000802, 0x00040802, 0x04040802,
    0x00002800, 0x04002800, 0x00042800, 0x04042800, 0x00002802, 0x04002802, 0x00042802, 0x04042802,
    0x00000820, 0x04000820, 0x00040820, 0x04040820, 0x00000822, 0x04000822, 0x00040822, 0x04040822,
    0x00002820, 0x04002820, 0x00042820, 0x04042820, 0x00002822, 0x04002822, 0x00042822, 0x04042822
)

SHIFTSWITCH = (False, False, True, True, True, True, True, True, False, True, True, True, True, True, True, False)

CON_SALT = (
    0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF, 0xE0, 0xE1,
    0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF, 0xF0, 0xF1,
    0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF, 0x00, 0x01,
    0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A,
    0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A,
    0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x20, 0x21, 0x22, 0x23, 0x24,
    0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34,
    0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x44
)

COV_ALPHABET = B'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


class UnixCrypt:

    @staticmethod
    def _hperm(a):
        t = ((a << 18) ^ a) & 0xCCCC0000
        return a ^ t ^ ((t >> 18) & 0x3FFF)

    @staticmethod
    def _perm(a, b, n, m):
        t = ((a >> n) ^ b) & m
        a ^= t << n
        b ^= t
        return a, b

    @property
    def key(self) -> bytes:
        return self.__key

    @property
    def schedule(self) -> List[int]:
        return self.__schedule

    @key.setter
    def key(self, key: bytes):
        key = key.ljust(8, b'\0')
        self.__key = key

        c, d = struct.unpack('<ii', key)
        c = (c & 0x7F7F7F7F) << 1
        d = (d & 0x7F7F7F7F) << 1
        d, c = self._perm(d, c, 4, 0x0F0F0F0F)
        d, c = self._hperm(d), self._hperm(c)
        d, c = self._perm(d, c, 1, 0x55555555)
        c, d = self._perm(c, d, 8, 0x00FF00FF)
        d, c = self._perm(d, c, 1, 0x55555555)
        d = (
            ((0x0000FF00 & d))         | # noqa 
            ((0x000000FF & d) << 0x10) | # noqa
            ((0x00FF0000 & d) >> 0x10) | # noqa
            ((0x0F000000 & (c >> 4)))
        )
        c &= 0x0FFFFFFF

        schedule = []
        switch = itertools.cycle(SHIFTSWITCH)
        for _ in range(self.iterations):
            if next(switch):
                c = (c >> 2) | (c << 26)
                d = (d >> 2) | (d << 26)
            else:
                c = (c >> 1) | (c << 27)
                d = (d >> 1) | (d << 27)
            c = c & 0x0FFFFFFF
            d = d & 0x0FFFFFFF
            s = (
                SKBC0[c & 0x3F]                                    | # noqa                                      
                SKBC1[((c >> 0x06) & 0x03) | ((c >> 0x07) & 0x3C)] | # noqa
                SKBC2[((c >> 0x0D) & 0x0F) | ((c >> 0x0E) & 0x30)] | # noqa
                SKBC3[((c >> 0x14) & 0x01) | ((c >> 0x15) & 0x06) | ((c >> 0x16) & 0x38)]
            )
            t = (
                SKBD0[((d >> 0x00) & 0x3F)]                        | # noqa
                SKBD2[((d >> 0x0F) & 0x3F)]                        | # noqa
                SKBD1[((d >> 0x07) & 0x03) | ((d >> 0x08) & 0x3C)] | # noqa
                SKBD3[((d >> 0x15) & 0x0F) | ((d >> 0x16) & 0x30)]   # noqa
            )
            schedule.append(((t << 16) | (s & 0x0000FFFF)) & 0xFFFFFFFF)
            s = (s >> 0x10) | (t & 0xFFFF0000)
            s = (s << 0x04) | ((s >> 0x1C) & 0x0F)
            schedule.append(s & 0xFFFFFFFF)

        self.__schedule = schedule

    def encrypt(self, L, R, S, E0, E1):
        V = R ^ (R >> 0x10)
        U = V & E0
        V = V & E1
        U = U ^ (U << 0x10) ^ R ^ self.schedule[S]
        T = V ^ (V << 0x10) ^ R ^ self.schedule[S + 1]
        T = (0x0FFFFFFF & (T >> 4)) | (T << 28)
        return L ^ (
            SPT1[(T >> 0x00) & 0x3F] | # noqa
            SPT3[(T >> 0x08) & 0x3F] | # noqa
            SPT5[(T >> 0x10) & 0x3F] | # noqa
            SPT7[(T >> 0x18) & 0x3F] | # noqa
            SPT0[(U >> 0x00) & 0x3F] | # noqa
            SPT2[(U >> 0x08) & 0x3F] | # noqa
            SPT4[(U >> 0x10) & 0x3F] | # noqa
            SPT6[(U >> 0x18) & 0x3F]
        )

    def body(self, E0, E1):
        L = R = 0
        for _ in range(25):
            L, R = R, L
            for i in range(0, self.iterations * 2, 2):
                L, R = R, self.encrypt(L, R, i, E0, E1)
        L = (L >> 1) | ((L & 1) << 31)
        R = (R >> 1) | ((R & 1) << 31)
        R, L = self._perm(R, L, 0x01, 0x55555555)
        L, R = self._perm(L, R, 0x08, 0x00FF00FF)
        R, L = self._perm(R, L, 0x02, 0x33333333)
        L, R = self._perm(L, R, 0x10, 0x0000FFFF)
        R, L = self._perm(R, L, 0x04, 0x0F0F0F0F)
        return L, R

    def __init__(self, key: bytes, salt: bytes = b'', iterations=0x10):
        self.salt = salt.ljust(2, b'A')
        self.iterations = iterations
        self.key = key.ljust(8, B'\0')[:8]

    def __bytes__(self):
        ES0 = CON_SALT[self.salt[0] & 0x7F]
        ES1 = CON_SALT[self.salt[1] & 0x7F] << 4

        l, r = self.body(ES0, ES1)

        a = ((l << 0x10) & 0xFF0000) | ((l >> 0x10) & 0x000000FF) | (l & 0x0000FF00)
        b = ((l >> 0x08) & 0xFF0000) | ((r << 0x08) & 0x0000FF00) | ((r >> 0x08) & 0x000000FF)
        c = (r & 0xFF0000) | (r >> 16 & 0xFF00)

        sixbit = [
            (a >> 18) & 0x3F, (a >> 12) & 0x3F, (a >> 6) & 0x3F, a & 0x3F,
            (b >> 18) & 0x3F, (b >> 12) & 0x3F, (b >> 6) & 0x3F, b & 0x3F,
            (c >> 18) & 0x3F, (c >> 12) & 0x3F, (c >> 6) & 0x3F
        ]
        return self.salt[:2] + bytes((COV_ALPHABET[x] for x in sixbit))


class ucrypt(KeyDerivation):
    """
    Implements the classic Unix crypt algorithm.
    """

    _DEFAULT_SALT = B'AA'
    _DEFAULT_SIZE = 13

    def process(self, data):
        crypted = bytes(UnixCrypt(data, salt=self.salt))
        if len(crypted) < self.args.size:
            raise RefineryException(
                F'unix crypt only provided {len(crypted)} bytes, but {self.args.size} '
                F'were requested.', partial=crypted
            )
        return crypted[:self.args.size]
