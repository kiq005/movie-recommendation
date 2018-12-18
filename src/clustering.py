#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Realiza o processo de clusterização
Baseado em: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html
'''
import os, sys
import numpy as np
from fastcluster import linkage
import matplotlib.pyplot as plt

# Aumenta o limite de recursão
sys.setrecursionlimit(10000)
# Diretório com dados
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
# Métodos disponíveis
methods = ["ward","single","average","complete"]

def seriation(Z,N,cur_index):
    '''
        input:
            - Z é a árvore hierárquica (dendrogram)
            - N é o número de pontos dados ao processo de clusterização
            - cur_index é a posição na árvore para a travessia recursiva
        output:
            - ordem implicada pela árvore hierárquica Z

        seriation computa a ordem implicada por uma árvore hierárquica (dendrogram)
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
            - dist_mat é a matriz de distância
            - method = ["ward","single","average","complete"]
        output:
            - seriated_dist é a entrada dist_mat,
              mas com a reordenação das linhas e
              colunas de acordo com a serialização,
              i.e. a ordem implicada pela árvore
              hierárquica
            - res_order é a ordem implicada pela
            árvore hierárquica
            - res_linkage é a árvore hierarquica
            (dendrogram)

        compute_serial_matrix transforma uma matriz de distância
        em uma matriz de distância ordenada de acordo com a ordem
        implicada pela árvore hierárquica (dendrogram)
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
    # Argumento de método e nome do arquivo
    method = "ward"
    if len(sys.argv) == 3:
        if sys.argv[1] in methods:
            method = sys.argv[1]
        else:
            print("Uso: clustering.py método arquivo")
            print("Métodos:", ', '.join(methods))
            exit(-1)
        file_name = sys.argv[2]
    else:
        print("Uso: clustering.py método arquivo")
        print("Métodos:", ', '.join(methods))
        exit(-1)
    # Importa a matriz de distanciamento
    try:
        dist_matrix = np.load(os.path.join(DIR, file_name))
    except:
        print("Erro na leitura do arquivo '%s'"%(file_name))
        exit(-1)
    # Ordena a matriz
    dist_matrix, res_order, res_linkage = compute_serial_matrix(dist_matrix,method)
    # Exibe a matriz
    N = len(dist_matrix)
    plt.pcolormesh(dist_matrix)
    plt.colorbar()
    plt.xlim([0,N])
    plt.ylim([0,N])
    plt.savefig(os.path.join(DIR, 'clusters_%s.png')%(method))
    # Salva resultados
    np.save(os.path.join(DIR, 'dist_matrix_%s.npy'%(method)), dist_matrix) # Binário
    np.save(os.path.join(DIR, 'res_order_%s.npy'%(method)), res_order) # Binário
    np.save(os.path.join(DIR, 'res_linkage_%s.npy'%(method)), res_linkage) # Binário
