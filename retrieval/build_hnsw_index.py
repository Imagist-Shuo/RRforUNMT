# -*- coding:UTF8 -*-
# 
import sys
sys.path.append('../../sentence_emb/SIF/src')
import data_io, params, SIF_embedding, embeddings
import numpy as np
from itertools import islice
import hnswlib

wordfile = sys.argv[1]
weightfile = sys.argv[2]
sentence_folder = sys.argv[3]
batch_size = int(sys.argv[4])
dimension = int(sys.argv[5])
tree_num = int(sys.argv[6])
allout_file = sys.argv[7]
num_elements = int(sys.argv[8])

# input
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 1 # number of principal components to remove in SIF weighting scheme

params = params.params()
params.rmpc = rmpc

(words, We) = data_io.getWordmap(wordfile)
word2weight = data_io.getWordWeight(weightfile, weightpara)
weight4ind = data_io.getWeight(words, word2weight)
print('Fnished loading vecs and weights.')

from os import listdir
from os.path import isfile, join
sentence_files = [join(sentence_folder, f) for f in listdir(sentence_folder) if isfile(join(sentence_folder, f))]
print('All files:',sentence_files)


for sentence_file in sentence_files:
	#if '20-30' in sentence_file or '25-35' in sentence_file or '30-40' \
	#in sentence_file or '5-15' in sentence_file:
	batch_num = 0
	with open(sentence_file, 'r', encoding='utf-8') as fr:
		print('Processing file', sentence_file, '...')
		p = hnswlib.Index(space='cosine', dim=dimension)
		p.init_index(max_elements = num_elements, ef_construction = 2000, M = 80)
		p.set_ef(1000)
		# Set number of threads used during batch search/construction
		# By default using all available cores
		p.set_num_threads(30)
		for n_lines in iter(lambda: tuple(islice(fr, batch_size)), ()):
			sents = list(map(str.strip, n_lines))
			sent_id = list(map(lambda x:int(x.split('\t')[0]), sents))
			sentences = list(map(lambda x:x.split('\t')[-1], sents))
			x, m = data_io.sentences2idx(sentences, words)
			w = data_io.seq2weight(x, m, weight4ind)

			# get SIF embedding
			embedding = SIF_embedding.SIF_embedding(We, x, w, params) # embedding[i,:] is the embedding for sentence i
			embeddings.normalize(embedding, ["unit", "center"])

			p.add_items(embedding,sent_id)
			print('Finished batch', batch_num, '.', end = '\r')
			batch_num += 1
	print('\nFinished loading', sentence_file, '.')
	out_file = sentence_file+'.ann'
	p.save_index(out_file)
	print('Finished saving', out_file, '.')
	del p

