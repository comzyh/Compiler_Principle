#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-02 17:38:36
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-04 11:19:17

Epsilon = 0


class NFANode(object):

    """Node of NFA"""

    def __init__(self, nfa=None, index=0, transfer=None, data=None):
        super(NFANode, self).__init__()
        if not isinstance(index, int):
            raise Exception('id must be integer, got %s' % index)
        if transfer is None:
            transfer = {}  # 坑, 使用默认参数的话全局都指向一个dictionary了..
        self.index = index  # 标号
        self.transfer = transfer  # 转移表
        self.NFA = nfa
        self.alphabet = nfa.alphabet
        self.data = data

    def add_transfer(self, char, dest):
        if char not in self.transfer:
            self.transfer[char] = []
        self.transfer[char].append(dest)

    def __str__(self):
        s = ''
        s += '--------------\n'
        s += 'index:%s\n' % self.index
        for key, arr in self.transfer.items():
            s += '%s :' % key
            s += str([state.index for state in arr])
            s += '\n'
        return s

    def show_transfer(self, char):
        print '--------------'
        print 'index:%s' % self.index
        if char in self.transfer:
            print char, ':',
            print[state.index for state in self.transfer[char]]


class NFA(object):

    """Nondeterministic Finite Automaton"""

    def __init__(self, alphabet):
        super(NFA, self).__init__()
        self.states = []  # 状态集
        self.alphabet = alphabet
        self.S = self.create_node()
        self.final_state = set()
        self.name_to_state_dict = None

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
        u.add_transfer(char, v)
        # print '%s ----%s----> %s' % (u.index, char, v.index)

    def __str__(self):
        s = ''
        for state in self.states:
            s += state.__str__()
        return s


class DFANode(object):

    """Node of DFA"""

    def __init__(self, dfa=None, index=0, transfer=None):
        super(DFANode, self).__init__()
        self.dfa = dfa
        self.index = index
        if transfer is None:
            transfer = {}
        self.transfer = transfer
        self.data = {}

    def add_transfer(self, char, dest):
        if char not in self.transfer:
            self.transfer[char] = []
        self.transfer[char].append(dest)


class DFA(object):

    """Deterministic Finite Automation"""

    def __init__(self, alphabet):
        super(DFA, self).__init__()
        self.states = []  # 状态集
        self.alphabet = alphabet
        self.S = self.create_node()
        self.final_state = set()
        self.name_to_state_dict = None

    def create_node(self):
        node = DFANode(self, len(self.states))
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
        u.add_transfer(char, v)
