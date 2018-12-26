#!/usr/bin/python3

# Import built-in modules
import os, random
import pickle as Pickle

# Import external packages
import numpy as np
# from sklearn.decomposition import PCA

FPATH_EMBEDDINGS = "./embeddings.pickle"

def doPCA(x, n_components=2, varRetained = 0.95, show = False):
	num_observations, num_dimensions = x.shape
	# from sklearn.preprocessing import StandardScaler
	# x = StandardScaler().fit_transform(x)
	x = (x - x.mean(axis = 0)) # Subtract the mean of column i from column i, in order to center the matrix.
	if num_dimensions > 100:
		eigenvalues, eigenvectors = np.linalg.eigh(dot(x, x.T))
		v = (dot(x.T, eigenvectors).T)[::-1] # Unscaled, but the relative order is still correct.
		s = sqrt(eigenvalues)[::-1] # Unscaled, but the relative order is still correct.
	else:
		u, s, v = np.linalg.svd(x, full_matrices = False)
	return v[:,:2], s


	# cor_mat1 = np.corrcoef(X_std.T)
	# eig_vals, eig_vecs = np.linalg.eig(cor_mat1)

def read_data(fpath):
	"""
	args:
		fpath 		: str or pathlike object
	return:
		data 		: 
	"""
	with open(fpath, "rb") as fo:
		dikt = Pickle.load(fo, encoding="bytes")
	return dikt
V = read_data(FPATH_EMBEDDINGS)
# dikt = read_data(FPATH_DIKT)
# dikt_rvrs = read_data(FPATH_DIKTRVRS)

# pca = PCA(n_components=2)

isAlive = True
while isAlive:
	str_req = input("indexes: ")
	# seq_index = [random.randint(20,500) for i in range(10)]
	# print(seq_index)
	seq_index = [int(c) for c in str_req.split(",")]

	len_argv = len(seq_index)
	dim_vec = 100
	seq_rec = np.zeros(shape=(len_argv, dim_vec), dtype=np.float32)
	for i, index in enumerate(seq_index):
		seq_rec[i] = V[index]
		
		# pca.fit(seq_rec)
		# result_pcas = pca.fit_transform(seq_rec)

	result_pca, sigma = doPCA(seq_rec)
	str_print = ""
	for rec in result_pca: str_print += "{0:8f},{1:8f}\n".format(rec[0],rec[1])
	str_print = str_print.strip("\n")
	print(str_print)
	# print(result_pca)

	# isAlive = input("renew")