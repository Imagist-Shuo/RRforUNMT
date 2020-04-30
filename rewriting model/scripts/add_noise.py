# -*- coding: utf-8 -*-

import numpy as np
import random
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]
idx = 0
fw = open(out_file, 'w+', encoding='utf-8')
with open(in_file, 'r', encoding='utf-8') as fr:
	while True:
		line = fr.readline().strip()
		if not line:
			break
		idx += 1
		rand = random.random()
		if rand <= 0.2:
			fw.write(line + '\n')
		else:
			split_line = line.split(' ')
			length = len(split_line)
			if rand <= 0.4 and rand > 0.2:				
				delete_pos = sorted(random.sample(list(range(length)), min(2, length)), reverse = True)
				del(split_line[delete_pos[0]])
				rand_seed = random.random()
				if rand_seed > 0.5 and len(delete_pos)==2:
					del(split_line[delete_pos[1]])
			else:
				for i in range(length // 2):
					rand_pos = random.randint(1,length-1)
					swap_pos = rand_pos
					while swap_pos == rand_pos:
						rand_seed = random.random()
						if rand_seed > 0.5:
							swap_pos = max(0, rand_pos-1)
						else:
							swap_pos = min(rand_pos+1, length-1)
					split_line[swap_pos], split_line[rand_pos] = split_line[rand_pos], split_line[swap_pos]
				if rand > 0.9:
					delete_pos = sorted(random.sample(list(range(length)), 2), reverse = True)
					del(split_line[delete_pos[0]])
					rand_seed = random.random()
					if rand_seed > 0.5:
						del(split_line[delete_pos[1]])
			fw.write(' '.join(split_line) + '\n')
		print('Finished', idx, 'lines', end = '\r')
print('\n')
fw.close()
