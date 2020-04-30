# -*- coding:utf-8 -*-
import sys
import os
import numpy as np
from functools import reduce
import hnswlib
import json

src_ave_score_file = sys.argv[1]
trg_ave_score_file = sys.argv[2]

st_sim_score_file = sys.argv[3]
margin_mode = int(sys.argv[4]) #1.distance 2.ratio

with open(src_ave_score_file, 'r', encoding='utf-8') as fr:
	src_self_score = json.load(fr)
with open(trg_ave_score_file, 'r', encoding='utf-8') as fr:
	trg_self_score = json.load(fr)
with open(st_sim_score_file, 'r', encoding='utf-8') as fr:
	st_sim_score = json.load(fr)
print('Finished loading score files.')

st_sim_dic = {}

def margin_dist(src_id, trg_id, distance):
	if margin_mode == 1:
		return distance - ((src_self_score[str(src_id)] + trg_self_score[str(trg_id)])/2)
	elif margin_mode == 2:
		return distance / ((src_self_score[str(src_id)] + trg_self_score[str(trg_id)])/2)

for src_id, dist_dict in st_sim_score.items():
	new_dist_dict = {}
	for trg_id, distance in dist_dict:
		new_dist_dict[trg_id] = margin_dist(src_id, trg_id, distance)
	st_sim_dic[src_id] = new_dist_dict

print('Dumping...')
with open('st.sim_score.js', 'w+', encoding = 'utf-8') as fw:
	fw.write(json.dumps(st_sim_dic))
