#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-02 17:38:36
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-02 22:07:35


class NFANode(object):

    """Node of NFA"""

    def __init__(self, nfa=None, id=0, next={}, data=None):
        super(NFANode, self).__init__()
        self.id = id  # 标号
        self.next = next  # 转移表
        self.NFA = nfa
        self.alphabet = nfa.alphabet
        self.data = data

    def add_next(self, char, next):
        if self.next[char] is None:
            self.next[char] = []
        self.next[char].append(next)


class NFA(object):

    """Nondeterministic Finite Automaton"""

    def __init__(self, alphabet):
        super(NFA, self).__init__()
        self.states = []  # 状态集
        self.alphabet = alphabet
        self.S = self.create_node()
        self.finite = set()

    def create_node(self):
        node = NFANode(self, len(self))
        self.states.append(node)
        return node

    def add_trans(self, u, char, v):
        if (not (u in self.states) or not (v in self.states) or
                not (char in self.alphabet)):
            raise Exception('illigal transition')
        u.add_next(char, v)


class DFA(object):

    """Deterministic Finite Automation"""

    def __init__(self, arg):
        super(DFA, self).__init__()
        self.arg = arg
