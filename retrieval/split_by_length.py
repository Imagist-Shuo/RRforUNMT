# -*- coding:utf-8 -*-
import sys

fname = sys.argv[1]
group_gap = int(sys.argv[2])
max_length = int(sys.argv[3])

group_num = max_length//(group_gap//2)-1
print('Group nums:', group_num)

group_names = [str(group_gap//2*x)+'-'+str(group_gap//2*x+group_gap) for x in range(group_num)]
print('Group names:', group_names)

fws = [open(fname + '.' + group_names[x], 'w+', encoding='utf-8') for x in range(group_num)]

def get_groups(sent):
	words_num = len(sent.split(' '))
	group1 = words_num // (group_gap//2) - 1
	group2 = group1 + 1
	return_list = []
	if group1 >= 0 and group1 < group_num:
		return_list.append(group1)
	if group2 >= 0 and group2 < group_num:
		return_list.append(group2)
	return return_list

idx = 0
with open(fname, 'r', encoding='utf-8') as fr:
	while True:
		line = fr.readline().strip()
		print(idx, end='\r')
		if not line:
			break
		for group_id in get_groups(line):
			fws[group_id].write(str(idx) + '\t' + line+'\n')
		idx += 1
print('\nFinished.')
