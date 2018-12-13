#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
methods = ["ward","single","average","complete"]

def e_msg():
	print("Uso: clusters_data.py método")
	print("Métodos:", ', '.join(methods))
	exit(-1)

def generate_dendrogram(link, method='ward'):
	Z = hierarchy.linkage(link, method)
	dn = hierarchy.dendrogram(Z)
	plt.figure(figsize=(25,10))
	plt.xlabel('movie')
	plt.ylabel('distance')
	hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
	plt.savefig(os.path.join(DIR, 'dendrogram_%s.png')%(method))

def get_clusters(link, method='ward', criterion='distance', max_d=2):
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
		#dist_matrix = np.load(os.path.join(DIR, 'dist_matrix_%s.npy'%(method)))
		#res_order = np.load(os.path.join(DIR, 'res_order_%s.npy'%(method)))
		res_linkage = np.load(os.path.join(DIR, 'res_linkage_%s.npy'%(method)))
	except:
		print("Erro ao ler dados dos cluters, os arquivos existem?")
		exit(-1)
	
	#generate_dendrogram(res_linkage, method)
	clusters = get_clusters(res_linkage, method)
	np.save(os.path.join(DIR, 'clusters_data.npy'), clusters)
