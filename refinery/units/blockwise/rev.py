#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import BlockTransformation


class rev(BlockTransformation):
    """
    The blocks of the input data are output in reverse order. If the length of
    the input data is not a multiple of the block size, the data is truncated.
    """
    def process(self, data):
        if self.bytestream:
            return data[::-1]
        else:
            rv = list(self.chunk(data, raw=True))[::-1]
            return self.rest(data) + self.unchunk(rv, raw=True)
