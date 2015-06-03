#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-03 23:33:24
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-03 23:48:07
import re


def read_syntax():
    line_number = 0
    legal_number = 0
    final = None
    syntaxs = []
    reg = re.compile(r'^(?P<left>\w+)\s*=\s*(?P<right>.*?)$')
    for line in open('syntax.txt'):
        line_number += 1
        if line[0] == '#':
            continue
        if line_number == 1:
            final = line[:-1]
        else:
            res = reg.search(line[:-1])
            if not res:
                print 'the line %4d print below is illegal,' % line_number
                print line
                continue
            syntaxs.append([res.group('left')] + res.group('right').split(' '))
            legal_number += 1
    print 'syntax loaded, %d lines at all' % legal_number
    return final, syntaxs


def read_token_table():
    reg = re.compile(r'^(?P<token>[^\s]+)\s')
    token_table = []
    for line in open('token_table.txt'):
        res = reg.search(line)
        if res:
            token_table.append(res.group('token'))
    return token_table


def main():
    final, syntaxs = read_syntax()
    token_table = read_token_table()
    for syntax in syntaxs:
        print syntax
    print token_table


if __name__ == '__main__':
    main()
