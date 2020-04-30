Retrieve the similar sentences from two monolingual corpora. Run the following scripts in order.
1. split_by_length.py: split the monolingual data according to the sentence length for the convenience of easily building the index.
2. build_hnsw_index.py: build the index for each length group, and generate xxx.ann files.
3. calc_self_score.py: read .ann file and calculate the scores of term b in margin(a,b) of Eq.(1).
4. calc_margin_score.py: calculate the margin similarity score for each sentence pair.
5. extract_sim_sentences.py: retrieve similar sentences according to the margin scores calculated above.
