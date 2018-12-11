#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ref: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html
import os, sys
import numpy as np
from fastcluster import linkage
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
methods = ["ward","single","average","complete"]

def seriation(Z,N,cur_index):
    '''
        input:
            - Z is a hierarchical tree (dendrogram)
            - N is the number of points given to the clustering process
            - cur_index is the position in the tree for the recursive traversal
        output:
            - order implied by the hierarchical tree Z
            
        seriation computes the order implied by a hierarchical tree (dendrogram)
    '''
    if cur_index < N:
        return [cur_index]
    else:
        left = int(Z[cur_index-N,0])
        right = int(Z[cur_index-N,1])
        return (seriation(Z,N,left) + seriation(Z,N,right))
    
def compute_serial_matrix(dist_mat,method="ward"):
    '''
        input:
            - dist_mat is a distance matrix
            - method = ["ward","single","average","complete"]
        output:
            - seriated_dist is the input dist_mat,
              but with re-ordered rows and columns
              according to the seriation, i.e. the
              order implied by the hierarchical tree
            - res_order is the order implied by
              the hierarhical tree
            - res_linkage is the hierarhical tree (dendrogram)
        
        compute_serial_matrix transforms a distance matrix into 
        a sorted distance matrix according to the order implied 
        by the hierarchical tree (dendrogram)
    '''
    N = len(dist_mat)
    res_linkage = linkage(dist_mat, method=method,preserve_input=True)
    res_order = seriation(res_linkage, N, N + N-2)
    seriated_dist = np.zeros((N,N))
    a,b = np.triu_indices(N,k=1)
    seriated_dist[a,b] = dist_mat[ [res_order[i] for i in a], [res_order[j] for j in b]]
    seriated_dist[b,a] = seriated_dist[a,b]
    
    return seriated_dist, res_order, res_linkage



if __name__ == '__main__':
    # Importa a matriz de distanciamento
    dist_matrix = np.load(os.path.join(DIR, 'tmdb_5000_movies.npy'))
    # Argumento de método
    method = "ward"
    if len(sys.argv) == 2:
        if sys.argv[1] in methods:
            method = sys.argv[1]
        else:
            print("Methods:", ', '.join(methods))
            exit(-1)
    # Ordena a matriz
    dist_matrix, res_order, res_linkage = compute_serial_matrix(dist_matrix,method)
    #print(dist_matrix)
    #print(res_order)
    print(res_linkage)
    # Exibe a matriz
    #N = len(dist_matrix)
    #plt.pcolormesh(dist_matrix)
    #plt.colorbar()
    #plt.xlim([0,N])
    #plt.ylim([0,N])
    ##plt.show()
    #plt.savefig(os.path.join(DIR, 'clusters_%s.png')%(method))