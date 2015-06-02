#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-06-01 19:05:49
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-02 16:14:54
import re
import json
def main():
	print 'Tokenizer by comzyh'
	line_number = 0
	final = []
	productions = []
	for line in open('lex.txt'):
		if line[0] == '#':
			continue
		if line_number == 0:
			final = line.split(' ')
		else:
			groups = re.search(r'(?P<left>\w+)\s*=\s*((?P<epsilon>\$)|\"(?P<terminate>.*)\"(\s*(?P<right>\w+))?)',line)
			if groups is None:
				continue
			productions.append(groups.groupdict())
		line_number += 1
	print 'lexical loaded, %d lines at all' % line_number
if __name__ == '__main__':
	main()
