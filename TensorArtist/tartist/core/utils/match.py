# -*- coding:utf8 -*-
# File   : match.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 2/3/17
# 
# This file is part of TensorArtist.


import fnmatch
import re
import collections

__all__ = ['NameMatcher']


class NameMatcher(object):
    def __init__(self, rules=None):
        if rules is None:
            self._rules = []
        elif isinstance(rules, dict):
            self._rules = list(rules.items())
        else:
            assert isinstance(rules, collections.Iterable)
            self._rules = list(rules)

        self._map = {}
        self._compiled_rules = []
        self._compiled = False

        self._matched = []
        self._unused = set()

    @property
    def rules(self):
        return self._rules

    def map(self):
        assert self._compiled
        return self._map

    def append_rule(self, rule):
        self._rules.append(tuple(rule))

    def insert_rule(self, index, rule):
        self._rules.insert(index, rule)

    def pop_rule(self, index=None):
        self._rules.pop(index)

    def begin(self, *, force_compile=False):
        if not self._compiled or force_compile:
            self.compile()
        self._matched = []
        self._unused = set(range(len(self._compiled_rules)))

    def match(self, k):
        for i, (r, p, v) in enumerate(self._compiled_rules):
            if p.match(k):
                if i in self._unused:
                    self._unused.remove(i)
                self._matched.append((k, r, v))
                return v
        return None

    def end(self):
        return self._matched, {self._compiled_rules[i][0] for i in self._unused}

    def compile(self):
        self._map = dict()
        self._compiled_rules = []

        for r, v in self._rules:
            self._map[r] = v
            p = fnmatch.translate(r)
            p = re.compile(p, flags=re.IGNORECASE)
            self._compiled_rules.append((r, p, v))
        self._compiled = True
