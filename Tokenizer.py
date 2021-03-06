#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-01 19:05:49
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-05 09:26:11
import re
import json
from fa import Epsilon, NFA, DFA
import crash_on_ipy

crash_on_ipy.init()


def read_lexical():
    line_number = 0
    legal_number = 0
    final = {}
    final_ordered = []
    productions = []
    reg = re.compile(r'(?P<left>\S+)\s*=\s*((?P<epsilon>\$)|'
                     '((?P<right>[^\s\"]+))?\s*\"(?P<terminate>.*)\")')
    reg_split_token_type = re.compile(r'(?P<token>\S+):(?P<type>\w+)')
    for line in open('lex.txt'):
        line_number += 1
        if line[0] == '#':
            continue
        if line_number == 1:
            final_tokens = line[:-1].split(' ')
            for t in final_tokens:
                result = reg_split_token_type.search(t)
                if not result:
                    print 'm', t, 'z'
                final[result.group('token')] = result.group('type')
                final_ordered.append(result.group('token'))
        else:
            result = reg.search(line)
            if result is None:
                print 'the line %4d print below is illegal,' % line_number
                print line
                continue
            p = result.groupdict()
            if p['epsilon'] is not None:
                p['epsilon'] = True
            if p['terminate']:
                p['terminate'] = json.loads('"' + p['terminate'] + '"')
            productions.append(p)
            legal_number += 1
    print 'lexical loaded, %d lines at all' % legal_number
    return final, productions, final_ordered


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
        node = get_state_by_name(final_state_name)
        node.data = {'token': final_state_name}
        nfa.final_state.add(node)
        # print 'index: %3d, name: %s' % (node.index, final_state_name)
    for p in productions:
        # print p
        left_state = get_state_by_name(p['left'])
        if p['epsilon']:
            nfa.add_transfer(nfa.S, Epsilon, left_state)
            continue
        if p['right'] is not None:
            f = get_state_by_name(p['right'])
        else:
            f = nfa.S
        for i in p['terminate'][:-1]:
            node = nfa.create_node()
            nfa.add_transfer(f, i, node)
            f = node
        nfa.add_transfer(f, p['terminate'][-1:], left_state)
    nfa.name_to_state_dict = name_to_state_dict
    return nfa


def tokenizer_over_nfa(string, position, nfa):
    state_set = set()
    state_set.add(nfa.S)
    endpos = position
    for i in range(position, len(string)):
        char = string[i]
        # print 'char: %s' % char
        new_state_set = set()
        for state in state_set:
            # state.show_transfer(char)
            if char in state.transfer:
                new_state_set = new_state_set.union(set(state.transfer[char]))
        if not new_state_set:
            break
        endpos = i
        state_set = new_state_set

    final_states = set()
    for state in state_set:
        if state in nfa.final_state:
            final_states.add(state.data['token'])
    return endpos + 1, final_states, string[position:endpos + 1]


def nfa_to_dfa(nfa):

    dfa = DFA(set(nfa.alphabet))

    def e_colsure(state_set):
        # 能够从NFA状态T开始只通过ε转换到达的NFA状态集合
        if not isinstance(state_set, set):
            raise Exception('state_set must be set')
        queue = list(state_set)
        result = set(state_set)
        while queue:
            h = queue.pop(0)
            for state in h.get_transfer(Epsilon):
                if state not in result:
                    result.add(state)
                    queue.append(state)
        return result

    def move(state_set, symbol):
        result = set()
        for s in state_set:
            result = result.union(set(s.get_transfer(symbol)))
        return result
    state_set_to_node = {}
    start = tuple(e_colsure(set([nfa.S])))
    state_set_to_node[start] = dfa.S
    queue = [start]
    while queue:
        h = queue.pop(0)
        for symbol in nfa.alphabet:
            new_set = tuple(e_colsure(move(set(h), symbol)))
            if not new_set:
                continue
            if new_set not in state_set_to_node:
                node = dfa.create_node()
                node.data['token'] = set()
                state_set_to_node[new_set] = node
                for state in new_set:
                    # if state in nfa.final_state:
                    if state.data:
                        node.data['token'].add(state.data['token'])
                queue.append(new_set)
            dfa.add_transfer(state_set_to_node[h], symbol,
                             state_set_to_node[new_set])

    return dfa


def tokenizer_over_dfa(string, position, dfa):
    state = dfa.S
    endpos = position
    for i in range(position, len(string)):
        char = string[i]
        new_state = state.get_transfer(char)

        if not new_state:
            break
        # print 'char: %s, %s' % (char, new_state.data)
        endpos = i
        state = new_state

    final_states = set(state.data['token'])
    return endpos + 1, final_states, string[position:endpos + 1]


def main():
    print 'Tokenizer by comzyh............'
    final, productions, final_ordered = read_lexical()
    nfa = create_nfa(final.keys(), productions)
    dfa = nfa_to_dfa(nfa)
    print 'NFA has %d states' % len(nfa.states)
    print 'DFA has %d states' % len(dfa.states)
    # for key, value in nfa.name_to_state_dict.items():
    #     print 'index: %d, %s' % (value.index, key)
    # print nfa
    token_table = []
    line_number = 0
    lexical_error = False
    for line in open('input.txt'):
        line_number += 1
        token_table_line = []
        pos = 0
        while pos < len(line) and not lexical_error:
            while pos < len(line) and line[pos] in [' ', '\t', '\n']:
                pos += 1
            if pos < len(line):
                # pos, state_set, token = tokenizer_over_nfa(line, pos, nfa)
                pos, state_set, token = tokenizer_over_dfa(line, pos, dfa)
                if not state_set:
                    print 'lexical error at line %d, column %d' % \
                        (line_number, pos)
                    lexical_error = True
                    break
                token_type = None
                for _type in final_ordered:
                    if _type in state_set:
                        token_type = _type
                        break
                token_table_line.append((token_type, token))
        for token_type, token in token_table_line:
            print token,
        print '\n'
        token_table += token_table_line
        # break
    token_table.append(('#', '#'))
    # print token_table
    output_file = open('token_table.txt', 'w+')
    for token_type, token in token_table:
        output_file.write('%s\t%s\t%s\n' % (token_type,
                                            final[token_type], token))
if __name__ == '__main__':
    main()
