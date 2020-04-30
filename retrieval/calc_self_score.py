# -*- coding:utf-8 -*-
import sys
import os
import numpy as np
from functools import reduce
import hnswlib
import json

sfname = sys.argv[1]
tfname = sys.argv[2]
group_gap = int(sys.argv[3])
max_length = int(sys.argv[4])
dimension = int(sys.argv[5])
num_elements = int(sys.argv[6])
neighbors = int(sys.argv[7])
candidates = int(sys.argv[8])

group_num = max_length//(group_gap//2)-1
print('Group nums:', group_num)

group_names = [str(group_gap//2*x)+'-'+str(group_gap//2*x+group_gap) for x in range(group_num)]
print('Group names:', group_names)

src_text_files = [sfname + '.' + group_names[x] for x in range(group_num)]
src_index_files = list(map(lambda x:x+'.ann', src_text_files))

trg_text_file = [tfname + '.' + group_names[x] for x in range(group_num)]
trg_index_files = list(map(lambda x:x+'.ann', trg_text_file))

self_sim_dic = {}
self_ave_score = {}

trg_part_1 = hnswlib.Index(space='cosine', dim=dimension)
print('Loading trg part_1 index...')
trg_part_1.load_index(trg_index_files[0], max_elements = num_elements)
for i in range(group_num):
	src_part = hnswlib.Index(space='cosine', dim=dimension)
	print('Loading src index...')
	src_part.load_index(src_index_files[i], max_elements = num_elements)
	if i + 1 < group_num:
		print('Loading trg part_2 index...')
		trg_part_2 = hnswlib.Index(space='cosine', dim=dimension)
		trg_part_2.load_index(trg_index_files[i+1], max_elements = num_elements)
	with open(src_text_files[i], 'r', encoding='utf-8') as fr:
		print('---- Processing file', src_text_files[i], '... ----')
		while True:
			line = fr.readline().strip()
			if not line:
				break
			split_line = line.strip().split('\t')
			sent_id = int(split_line[0])
			if sent_id not in self_sim_dic:
				sent_vec = src_part.get_items([sent_id])[0]
				labels_part_1, distances_part_1 = trg_part_1.knn_query(sent_vec, k=neighbors+1, num_threads=10)
				labels = list(map(int, list(labels_part_1[0])))
				distances = list(map(float, list(distances_part_1[0])))

				sent_length = len(split_line[1].split(' '))
				if i + 1 < group_num and sent_length > 5 and sent_length <= 35:
					labels_part_2, distances_part_2 = trg_part_2.knn_query(sent_vec, k=neighbors+1, num_threads=10)
					labels += list(map(int, list(labels_part_2[0])))
					distances += list(map(float, list(distances_part_2[0])))
				d = dict(zip(labels, distances))
				if sent_id in d:
					del d[sent_id]
				d = sorted(d.items(), key = lambda x:x[1], reverse = False)[:neighbors]
				self_sim_dic[sent_id] = d
				self_ave_score[sent_id] = reduce(lambda x,y:x+y, list(map(lambda x:x[1], d))[:candidates])/candidates
			print('Processed', len(self_ave_score), 'sentences.', end = '\r')

	if i + 1 < group_num:
		trg_part_1 = trg_part_2
		del trg_part_2		
		print('---- Trg Part_1 index has changed. ----')
	del src_part

print('Dumping...')
with open(sfname + '.sim_score.js', 'w+', encoding = 'utf-8') as fw:
	fw.write(json.dumps(self_sim_dic))
with open(sfname + '.ave_score.js', 'w+', encoding = 'utf-8') as fw:
	fw.write(json.dumps(self_ave_score))





	
	