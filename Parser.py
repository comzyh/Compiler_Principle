#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-03 23:33:24
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-04 11:29:47
import re
from fa import DFA
import crash_on_ipy
crash_on_ipy.init()


def read_syntax():
    line_number = 0
    legal_number = 0
    final = None
    syntaxs = []
    vn = set()
    reg = re.compile(r'^(?P<left>\w+)\s*=\s*(?P<right>.*?)$')
    for line in open('syntax.txt'):
        line_number += 1
        if line[0] == '#':
            continue
        if line_number == 1:
            final = line[:-1]
            syntaxs.append((final + '\'', final))
        else:
            res = reg.search(line[:-1])
            if not res:
                print 'the line %4d print below is illegal,' % line_number
                print line
                continue
            syntax = tuple([res.group('left')] + res.group('right').split(' '))
            if len(syntax) == 2 and syntax[1] == '$':
                syntaxs.append(syntax[:1])
            else:
                syntaxs.append(syntax)
            vn.add(res.group('left'))
            legal_number += 1
    print 'syntax loaded, %d lines at all' % legal_number
    return final, syntaxs, vn


def read_token_table():
    reg = re.compile(r'^(?P<token>[^\s]+)\s')
    token_table = []
    for line in open('token_table.txt'):
        res = reg.search(line)
        if res:
            token_table.append(res.group('token'))
    return token_table


def read_vt():
    vt = set()
    reg_split_token_type = re.compile(r'(?P<token>\S+):(?P<type>\w+)')
    for t in open('lex.txt', 'r').readline()[:-1].split(' '):
        result = reg_split_token_type.search(t)
        vt.add(result.group('token'))
    return vt


def create_lr_dfa(final, syntaxs, vn, vt):
    if vn.intersection(vt):
        raise Exception('VN and VT has intersection')
    else:
        alptabet = vn.union(vt)
    productions = {}
    for syntax in syntaxs:
        if syntax[0] not in productions:
            productions[syntax[0]] = []
        productions[syntax[0]].append(syntax)
    print 'productions:'
    print productions
    items_set_to_node = {}  # tuple to Node
    first = {}
    nullable = {}

    getting_nullable = set()

    def get_nullable(item):  # 判断一个非终结符是否可以为Epsilon
        if not isinstance(item, str):
            raise Exception('item is not str')
        if item not in vn:
            raise Exception('item not in vn')
        if item in nullable:
            return nullable[item]
        if item in getting_nullable:
            nullable[item] = False
            return nullable[item]
        getting_nullable.add(item)
        nullable[item] = False
        for production in productions[item]:
            _nullable = True
            for t in production[1:]:
                if t in vt:
                    _nullable = False
                else:
                    _nullable &= get_nullable(t)
            nullable[item] |= _nullable
        getting_nullable.remove(item)
        return nullable[item]

    def get_first(item):  # 获取first集,返回set
        if not isinstance(item, tuple):
            raise Exception('item is not tuple')
        if item in first:
            return first[item]
        first[item] = set()
        for t in item:
            if t in vt:
                first[item].add(t)
                break
            else:
                for production in productions[t]:
                    if production[0] in vt:
                        first[item].add(production[0])
            if not get_nullable(t):
                break
        return first[item]

    def closure(item, item_set):
        pos, production, ahead = item
        # print 'pos,production,ahead:'
        # print pos,production,ahead
        right_part = production[pos + 1:]
        # print right_part
        if not right_part or right_part[0] not in vn:
            return
        for production in productions[right_part[0]]:
            new_set = set()
            for t in ahead:
                new_set = new_set.union(get_first(right_part[1:] + (t,)))
            new_item = (0, production, tuple(new_set))
            if new_item not in item_set:
                item_set.add(new_item)
                closure(new_item, item_set)

    # create the start Node
    init_item = (0, (final + '\'', final), ('#'))
    init_set = set()
    init_set.add(init_item)
    closure(init_item, init_set)
    dfa = DFA(alptabet)
    dfa.S.data = tuple(init_set)
    items_set_to_node[dfa.S.data] = dfa.S
    print '-----------items_set--------------'
    for item in dfa.S.data:
        print item
    # start to build dfa
    queue = [dfa.S]
    while queue:
        head = queue.pop(0)
        # print 'head %4d' % head.index
        for symbol in alptabet:
            # print symbol
            new_set = set()
            for item in head.data:
                pos, production, ahead = item
                # print 'production, production[pos + 1: pos + 2]:'
                # print production, production[pos + 1]
                if (pos + 1 < len(production) and
                        production[pos + 1] == symbol):
                    new_item = (pos + 1, production, ahead)
                    new_set.add(new_item)
                    closure(new_item, new_set)

            new_set = tuple(new_set)
            if not new_set:
                continue
            if new_set not in items_set_to_node:
                node = dfa.create_node()
                node.data = new_set
                items_set_to_node[new_set] = node
                queue.append(node)
            dfa.add_trans(head, symbol, items_set_to_node[new_set])
            print "%d ----%10s---->%d" % (head.index, symbol,
                                          items_set_to_node[new_set].index)

    return dfa


def main():
    final, syntaxs, vn = read_syntax()
    token_table = read_token_table()
    vt = read_vt()
    for syntax in syntaxs:
        print syntax
    # print token_table
    # print vn
    # print vt
    dfa = create_lr_dfa(final, syntaxs, vn, vt)


if __name__ == '__main__':
    main()
