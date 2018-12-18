#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Gera as informações de clusters dos filmes
'''
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
methods = ["ward","single","average","complete"]

def e_msg():
	'''
		e_msg imprime uma mensagem com instruções de utilização do
		programa, e finaliza a execução
	'''
	print("Uso: clusters_data.py método")
	print("Métodos:", ', '.join(methods))
	exit(-1)

def generate_dendrogram(link, method='ward'):
	'''
        input:
            - link a árvore hierárquica (dendrogram)
			- method = ["ward","single","average","complete"]
		generate_dendrogram gera a imagens de dendrograma de
		uma árvore hierárquica
	'''
	Z = hierarchy.linkage(link, method)
	dn = hierarchy.dendrogram(Z)
	plt.figure(figsize=(25,10))
	plt.xlabel('movie')
	plt.ylabel('distance')
	hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
	plt.savefig(os.path.join(DIR, 'dendrogram_%s.png')%(method))

def get_clusters(link, method='ward', criterion='distance'):
	'''
        input:
            - link a árvore hierárquica (dendrogram)
			- method = ["ward","single","average","complete"]
			- criterion = ["inconsistent", "distance", "maxclust", "monocrit", "maxclust_monocrit"]
		output:
			- clusters é uma lista de clusters
		get_clusters gera uma lista de clusters para vários
		níveis de uma árvore hierárquica
	'''
	Z = hierarchy.linkage(link, method)
	dn = hierarchy.dendrogram(Z)
	clusters = []
	for d in range(2,100,10):
		clusters.append(hierarchy.fcluster(Z, d, criterion))
	return clusters

if __name__ == '__main__':
	# Carrega os dados com base no argumento passado
	if len(sys.argv) == 2:
		if sys.argv[1] in methods:
			method = sys.argv[1]
		else:
			e_msg()
	else:
		e_msg()
	try:
		res_linkage = np.load(os.path.join(DIR, 'res_linkage_%s.npy'%(method)))
	except:
		print("Erro ao ler dados dos cluters, os arquivos existem?")
		exit(-1)

	clusters = get_clusters(res_linkage, method)
	np.save(os.path.join(DIR, 'clusters_data.npy'), clusters)
