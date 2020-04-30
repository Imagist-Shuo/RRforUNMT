# -*- coding: utf-8 -*-

import numpy as np
import random
import sys

text_file = sys.argv[1]
vocab_file = sys.argv[2]
output_src_file = sys.argv[3]
output_mem_file = sys.argv[4]
output_trg_file = sys.argv[5]
vocab_thresh_hold = int(sys.argv[6])
		
vocab = list(map(str.strip, open(vocab_file, 'r', encoding='utf-8').readlines()))
print(len(vocab))

fws = open(output_src_file, 'w+', encoding='utf-8')
fwm = open(output_mem_file, 'w+', encoding='utf-8')
fwt = open(output_trg_file, 'w+', encoding='utf-8')

idx = 0
with open(text_file, 'r', encoding='utf-8') as fr:
	while True:
		line = fr.readline().strip()
		idx += 1
		if not line:
			break
		split_line = line.split(' ')
		length = len(split_line)
		if length < 5 or length > 35:
			continue
		removable_list = [i for i in range(length) if split_line[i] in vocab and vocab.index(split_line[i]) > vocab_thresh_hold]
		if len(removable_list) < 5:
			continue
		max_remove_num = len(removable_list)
		remove_num = random.randint(min(max_remove_num, 3), max_remove_num)
		remove_index = sorted(random.sample(removable_list, remove_num), reverse = False)
		mod_line = ' '.join(['<DEL>' if i in remove_index else split_line[i] for i in range(length)])
		mem_line = ' '.join([split_line[i] for i in remove_index])

		fws.write(mod_line + '\n')
		fwm.write(mem_line + '\n')
		fwt.write(line + '\n')
		print('Finish line', idx, '...', end = '\r')
print('\n')

fws.close()
fwm.close()
fwt.close()
