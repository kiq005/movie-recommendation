#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Realiza todo o processo de clusterização, desde a obtenção dos dados do dataset no formato json, até a construção dos clusters e geração de imagens
'''
import dist_matrix
import clustering
import clusters_data
import numpy as np
from fastcluster import linkage
import matplotlib.pyplot as plt
import nltk
import sys, os
from scipy.cluster import hierarchy

from multiprocessing import Process

VERBOSE = True
sys.setrecursionlimit(10000)
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')

def generate_sub(method_cl,method_bg,dm):
	'''
		input:
			- method_cl é o nome do método de clusterização
			- method_bg é a função com o método de determinação da
			  distância entre conjuntos
			- dm é a matriz de distância
		generate_sub
	'''
	if VERBOSE: print("Clustering:", method_bg.__name__, method_cl)
	dist_matrix, res_order, res_linkage = clustering.compute_serial_matrix(dm,method_cl)
	# Exibe a matriz
	plt.figure(0)
	plt.pcolormesh(dist_matrix)
	plt.colorbar()
	plt.xlim([0,len(dm)])
	plt.ylim([0,len(dm)])
	if VERBOSE: print("Saving:", 'clusters_%s_%s.png'%(method_bg.__name__, method_cl))
	plt.savefig(os.path.join(DIR, 'clusters_%s_%s.png'%(method_bg.__name__, method_cl)))
	# Dendrogram
	if VERBOSE: print("Dendrogram:", method_bg.__name__, method_cl)
	Z = hierarchy.linkage(res_linkage, method_cl)
	plt.figure(1, figsize=(25,10))
	plt.xlabel('movie')
	plt.ylabel('distance')
	dn = hierarchy.dendrogram(Z)
	hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
	if VERBOSE: print("Saving...", 'dendrogram_%s_%s.png'%(method_bg.__name__, method_cl))
	plt.savefig(os.path.join(DIR, 'dendrogram_%s_%s.png'%(method_bg.__name__, method_cl)))
	# Clusters
	if VERBOSE: print("Clusters:", method_bg.__name__, method_cl)
	clusters = clusters_data.get_clusters(res_linkage, method_cl)
	if VERBOSE: print("Saving...",'clusters_data_%s_%s.npy'%(method_bg.__name__, method_cl))
	np.save(os.path.join(DIR, 'clusters_data_%s_%s.npy'%(method_bg.__name__, method_cl)), clusters)
	if VERBOSE: print("Finished:", method_bg.__name__, method_cl)
	return

def generate(method_bg, bg):
	'''
		input:
			- method_bg é a função com o método de determinação da
			  distância entre conjuntos
			- bg é uma lista contendo as listas de bigramas dos sumários
		generate gera uma matriz de distância com base em um método de distância
		entre conjuntos, e inicia um processo para clusterização com base em uma
		lista de métodos
	'''
	if VERBOSE: print("Método:", method_bg.__name__)
	dm = np.zeros([len(bg), len(bg)], dtype=float)
	for i, movie_a in enumerate(bg):
		for j, movie_b in enumerate(bg):
			dm[i][j] =  dist_matrix.compare_bigrams( movie_a, movie_b, method_bg)
	if VERBOSE: print("Matriz:", np.shape(dm))
	# Clusters
	sub_processes = []
	for method_cl in ["ward","single","average","complete"]:
		p = Process(target=generate_sub, args=(method_cl,method_bg,dm,))
		p.start()
		sub_processes.append(p)
	for p in sub_processes:
		p.join()
	if VERBOSE: print("Complete:", method_bg.__name__)
	return

if __name__ == '__main__':
	# Obtém dados
	if VERBOSE: print("Lendo dataset...")
	data = dist_matrix.get_data('tmdb_5000_movies.json')
	# Obtém lista de bigramas
	if VERBOSE: print("Obtendo bigramas...")
	bg = []
	for movie in data:
		b = dist_matrix.get_bigrams(movie['overview'])
		if len(b) > 0:
			bg.append(b)
	del data
	# Constroi matriz de distância
	processes = []
	for method_bg in [nltk.jaccard_distance, nltk.masi_distance]:
		p = Process(target=generate, args=(method_bg,bg,))
		p.start()
		processes.append(p)
	for p in processes:
		p.join()
	if VERBOSE: print("100% Complete!")
