#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-01 19:05:49
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-03 16:37:25
import re
import json
from fa import Epsilon, NFA


def read_lexical():
    line_number = 0
    final = []
    productions = []
    reg = re.compile(r'(?P<left>\w+)\s*=\s*((?P<epsilon>\$)|'
                     '((?P<right>\w+))?\s*\"(?P<terminate>.*)\")')
    for line in open('lex.txt'):
        if line[0] == '#':
            continue
        if line_number == 0:
            final = line.split(' ')
        else:
            groups = reg.search(line)
            if groups is None:
                continue
            p = groups.groupdict()
            if p['epsilon'] is not None:
                p['epsilon'] = True
            if p['terminate']:
                p['terminate'] = json.loads('"' + p['terminate'] + '"')
            productions.append(p)
        line_number += 1
    print 'lexical loaded, %d lines at all' % line_number
    return final, productions


def create_nfa(final_states_name, productions):
    alphabet = set()
    for i in range(ord(' '), ord('~') + 1):
        alphabet.add(chr(i))
    nfa = NFA(alphabet)
    name_to_state_dict = {}

    def get_state_by_name(name):
        if name not in name_to_state_dict:
            name_to_state_dict[name] = nfa.create_node()
        return name_to_state_dict[name]

    for final_state_name in final_states_name:
        node = nfa.create_node()
        node.data = {'token': final_state_name}
        nfa.final_state.add(node)
        name_to_state_dict[final_state_name] = node
        print 'index: %3d, name: %s' % (node.index, final_state_name)
    for p in productions:
        left_state = get_state_by_name(p['left'])
        if p['epsilon']:
            nfa.add_trans(nfa.S, Epsilon, left_state)
            continue
        if p['right'] is not None:
            f = get_state_by_name(p['right'])
        else:
            f = nfa.S
        for i in p['terminate'][:-1]:
            node = nfa.create_node()
            nfa.add_trans(f, i, node)
            f = node
        nfa.add_trans(f, p['terminate'][-1:], left_state)
    nfa.name_to_state_dict = name_to_state_dict
    return nfa


def main():
    print 'Tokenizer by comzyh'
    final, productions = read_lexical()
    nfa = create_nfa(final, productions)
    # print json.dumps(nfa.states)
    # nfa.S.show()
    # nfa.states[141].show()
if __name__ == '__main__':
    main()
