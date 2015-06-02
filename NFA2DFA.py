#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Comzyh
# @Date:   2015-04-01 01:38:46
# @Last Modified by:   Comzyh
# @Last Modified time: 2015-06-02 17:48:02


def main():
    epsilon = 'e'
    states = list(raw_input('Please enter states: (for Example:"XABCDY")\n'))
    alphabet = list(raw_input('Please enter Input Alphabet\n'))
    transition = {}
    for s in states:
        transition[s] = {}
        for a in alphabet:
            transition[s][a] = []
            transition[s][epsilon] = []
    while True:
        try:
            trans = raw_input()
            trans = trans.split(' ')[:3]
            transition[trans[0]][trans[1]].append(trans[2])

        except EOFError, e:
            break

    def e_colsure(T):
        # 能够从NFA状态T开始只通过ε转换到达的NFA状态集合
        queue = list(T)
        result = set(queue)
        while queue:
            h = queue.pop(0)
            for s in transition[h][epsilon]:
                if not s in result:
                    result.add(s)
                    queue.append(s)
        result = list(result)
        result.sort()
        return ''.join(result)

    def move(T, a):
        result = set()
        for s in T:
            result = result | set(transition[s][a])
        result = list(result)
        result.sort()
        return ''.join(result)
    # NFA-DFA
    flag = set()
    Dstats = []
    queue = []
    Dstats.append(e_colsure(states[0]))
    queue.append(Dstats[0])
    Dtran = {}

    print '%8s %-9s' % ('index', 'State'),
    for a in alphabet:
        print '%-9s' % a,
    print

    while queue:
        T = queue.pop(0)
        # print "T=%s" % T
        flag.add(T)
        if not Dtran.has_key(T):
            Dtran[T] = {}
            for a in alphabet:
                Dtran[T][a] = ''
        move_ = {}
        prints_ = []
        for a in alphabet:
            move_[a] = move(T, a)
            U = e_colsure(move_[a])
            if U == '':
                continue
            if not U in Dstats:
                Dstats.append(U)
                queue.append(U)
                # print "U=%s" % U
                prints_.append('%-8s %-9s' % (move_[a], U))
            Dtran[T][a] = U
        # Output
        print "%8d %-9s" % (len(Dtran) - 1, T),
        for a in alphabet:
            print '%-9s' % move_[a],
        print
        for print_ in prints_:
            print print_

    # Output
    print '----------------------------------------'
    print '%8s %-9s' % ('index', 'State'),
    for a in alphabet:
        print '%-9s' % a,
    print
    remap = {}
    for index in range(len(Dstats)):
        remap[Dstats[index]] = index
    for index in range(len(Dstats)):
        ns = Dstats[index]
        print "%8d %-9s" % (index, ns),
        for a in alphabet:
            print '%-9s' % (remap[Dtran[ns][a]] if Dtran[ns][a] != '' else ''),
        if states[-1] in ns:
            print '%-9s' % 'final',
        print
    print '----------------------------------------'
    for index in range(len(Dstats)):
        ns = Dstats[index]
        print "{id: %s, reflexive: %s}," % (index, 'Y' in ns)
    for index in range(len(Dstats)):
        ns = Dstats[index]
        for a in alphabet:
            if Dtran[ns][a] != '':
                print "{source: nodes[%d], target: nodes[%d], left: false, right: true }," % (index, int(remap[Dtran[ns][a]]))
if __name__ == '__main__':
    main()
