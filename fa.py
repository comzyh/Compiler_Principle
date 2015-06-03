#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-02 17:38:36
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-03 16:37:11

Epsilon = 0


class NFANode(object):

    """Node of NFA"""

    def __init__(self, nfa=None, index=0, trasfer={}, data=None):
        super(NFANode, self).__init__()
        if not isinstance(index, int):
            raise Exception('id must be integer, got %s' % index)
        self.index = index  # 标号
        self.trasfer = trasfer  # 转移表
        self.NFA = nfa
        self.alphabet = nfa.alphabet
        self.data = data
        self.name_to_state_dict = None

    def add_trasfer(self, char, dest):
        if char not in self.trasfer:
            self.trasfer[char] = []
        self.trasfer[char].append(dest)

    def show(self):
        print '--------------'
        print 'index:%s' % self.index
        for key, arr in self.trasfer.items():
            print key, ':',
            print[state.index for state in arr]
        print '\n'


class NFA(object):

    """Nondeterministic Finite Automaton"""

    def __init__(self, alphabet):
        super(NFA, self).__init__()
        self.states = []  # 状态集
        self.alphabet = alphabet
        self.S = self.create_node()
        self.final_state = set()
        self.data = None

    def create_node(self):
        node = NFANode(self, len(self.states))
        self.states.append(node)
        return node

    def add_trans(self, u, char, v):
        if (not (u in self.states) or not (v in self.states) or
                not (char in self.alphabet or char == Epsilon)):
            print 'u in self.states: %s\n' % (u in self.states)
            print 'v in self.states: %s\n' % (v in self.states)
            print 'chr in self.alphabet %s\n' % (char in self.alphabet)
            print 'char = ', char
            raise Exception('illigal transition')
        u.add_trasfer(char, v)


class DFA(object):

    """Deterministic Finite Automation"""

    def __init__(self, arg):
        super(DFA, self).__init__()
        self.arg = arg
