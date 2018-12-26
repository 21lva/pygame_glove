#!/usr/bin/python3

# Import built-in modules
import os, random
# import pickle as Pickle

# Import external packages
import numpy as np
from sklearn.decomposition import PCA


def get_seq_coordinate(seq_index, dim_vec, V):
	# seq_index = [int(c) for c in str_req.split(",")]

	len_argv = len(seq_index)
	# dim_vec = 100
	seq_rec = np.zeros(shape=(len_argv, dim_vec), dtype=np.float32)
	for i, index in enumerate(seq_index):
		seq_rec[i] = V[index]


	pca = PCA(n_components=2)	#
	pca.fit(seq_rec)
	result_pca = pca.fit_transform(seq_rec)

	# result_pca, sigma = doPCA(seq_rec)
	return result_pca
