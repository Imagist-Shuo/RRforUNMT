# -*- coding:utf-8 -*-
import sys
import os
import numpy as np
import json

src_file = sys.argv[1]
trg_file = sys.argv[2]
st_sim_score_file = sys.argv[3]
ts_sim_score_file = sys.argv[4]
src_lang = sys.argv[5]
trg_lang = sys.argv[6]
threshold = float(sys.argv[7])
save_folder = sys.argv[8]

lang_pair = src_lang + '-' + trg_lang
ext_src_file = save_folder + '/extract.' + lang_pair + '.tc.' + src_lang
ext_trg_file = save_folder + '/extract.' + lang_pair + '.tc.' + trg_lang

print('Loading text files...')
with open(src_file, 'r', encoding='utf-8') as fr:
	src_texts = list(map(str.strip, fr.readlines()))
with open(trg_file, 'r', encoding='utf-8') as fr:
	trg_texts = list(map(str.strip, fr.readlines()))

print('Loading the similarity file.')
with open(st_sim_score_file, 'r', encoding='utf-8') as fr:
	st_sim_score_dic = json.load(fr)
with open(ts_sim_score_file, 'r', encoding='utf-8') as fr:
	ts_sim_score_dic_tmp = json.load(fr)
ts_sim_score_dic = {}
for src_id, trg_score_dic in ts_sim_score_dic_tmp.items():
	ts_sim_score_dic[src_id] = {}
	for trg_id, sim_score in trg_score_dic.items():
		ts_sim_score_dic[src_id][trg_id] = float(sim_score)

fws = open(ext_src_file, 'w+', encoding='utf-8')
fwt = open(ext_trg_file, 'w+', encoding='utf-8')

idx = 0
keep = 0
keep_mod = True
for src_id, trg_score_dic in st_sim_score_dic.items():
	idx += 1
	keep_mod = True
	for trg_id, st_sim_score in trg_score_dic.items():
		if src_id not in ts_sim_score_dic[trg_id]:
			continue
		ts_sim_score = ts_sim_score_dic[trg_id][src_id]
		if float(st_sim_score) > threshold and float(ts_sim_score) > threshold:
			if keep_mod:
				keep += 1
				keep_mod = False
			fws.write(src_texts[int(src_id)] + '\n')
			fwt.write(trg_texts[int(trg_id)] + '\n')
	print('Processing',idx,'src sentences, the keep ratio is',keep/idx,'.', end = '\r')
print('\n')
fws.close()
fwt.close()
