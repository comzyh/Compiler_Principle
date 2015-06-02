#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-01 19:05:49
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-02 22:18:46
import re
import json


def read_lexical():
    line_number = 0
    final = []
    productions = []
    reg = re.compile(r'(?P<left>\w+)\s*=\s*((?P<epsilon>\$)|'
                     '\"(?P<terminate>.*)\"(\s*(?P<right>\w+))?)')
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
            print p
        line_number += 1
    print 'lexical loaded, %d lines at all' % line_number
    return final, productions


def main():
    print 'Tokenizer by comzyh'
    final, fproductions = read_lexical()

if __name__ == '__main__':
    main()
