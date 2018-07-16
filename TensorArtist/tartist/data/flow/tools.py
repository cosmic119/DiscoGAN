# -*- coding:utf8 -*-
# File   : tools.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 2/23/17
# 
# This file is part of TensorArtist.

from .base import SimpleDataFlowBase
from itertools import repeat, cycle as cached_cycle
from itertools import takewhile, dropwhile, filterfalse
from itertools import chain
from itertools import starmap
from itertools import islice
from itertools import tee


__all__ = [
    'cycle', 'cycle_n', 'cached_cycle', 'repeat', 'repeat_n',
    'takewhile', 'dropwhile', 'filtertrue', 'filterfalse',
    'chain',
    'map', 'starmap', 'ssmap'
    'islice', 'truncate',
    'tee',
    'MapDataFlow'
]

repeat_n = repeat
filtertrue = dropwhile
truncate = islice


# implement cycle self, without any cache
def cycle(iterable, times=None):
    if times is None:
        while True:
            for v in iterable:
                yield v 
    else:
        for i in range(times):
            for v in iterable:
                yield v

cycle_n = cycle


def ssmap(function, iterable):
    for args in iterable:
        yield function(**args)


class MapDataFlow(SimpleDataFlowBase):
    def __init__(self, proxy, map_func=None):
        self.__proxy = other
        self.__map_func = map_func

    @property
    def proxy(self):
        return self.__proxy

    def _map(self, data):
        return self.__map_func(data)

    def _gen(self):
        for data in self.proxy:
            yield self._map(data)
