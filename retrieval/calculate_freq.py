# -*- coding:utf-8 -*-
import sys
from collections import Counter

fname = sys.argv[1]
word_freq = Counter()

with open(fname, 'r', encoding='utf-8') as fr:
    while True:
        line = fr.readline().strip()
        if not line:
            break
        split_line = line.split(' ')
        for w in split_line:
            word_freq[w] += 1
sorted_word_freq = sorted(word_freq.items(), key = lambda x:x[1], reverse = True)

with open(fname + '.freq', 'w+', encoding='utf-8') as fw:
    for pair in sorted_word_freq:
        fw.write(pair[0] + ' ' + str(pair[1]) + '\n')
