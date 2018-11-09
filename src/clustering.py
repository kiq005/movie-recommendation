#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ref: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html
import os, sys
import numpy as np
import matplotlib.pyplot as plt

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
methods = ["ward","single","average","complete"]

if __name__ == '__main__':
	# Importa a matriz de distanciamento
	dist_matrix = np.load(os.path.join(DIR, 'tmdb_5000_movies.npy'))
	# Ordena a matriz
	if len(sys.argv) == 2:
		if sys.argv[1] in methods:
			dist_matrix, res_order, res_linkage = compute_serial_matrix(dist_matrix,sys.argv[1])
		else:
			print("Methods: ", ','.join(methods))
			exit(-1)
	# Exibe a matriz
	N = len(dist_matrix)
	plt.colormesh(dist_matrix)
	plt.colorbar()
	plt.xlim([0,N])
	plt.ylim([0,N])
	plt.show()
