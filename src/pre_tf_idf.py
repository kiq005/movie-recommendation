#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Atua sobre clusters para obter palavras mais relevantes
'''
import pandas as pd
import json

def get_tuples(db):
	'''
		input:
			- db é uma lista de filmes
		output:
			- name_clust é uma lista com um par contendo o nome e
            clusters dos filmes
		get_tuples retorna uma lista de pares com nome e clusters
        de um filme dado uma base de dados
	'''
    df = pd.DataFrame(db)

    #get names
    names = df.columns
    #get clusters
    aux = df[:1].values
    clusters = aux[0]

    name_clust = []
    for i in range(len(names)):
        name_clust.append((names[i], clusters[i]))

    return name_clust

def cluster_list(name_clust, cluster_number):
	'''
		input:
			- name_clust é uma lista de pares com nome e clusters
            de filmes
			- cluster_number é o cluster em que se está interessado
            em analisar
		output:
			- mv_clus é uma lista com os filmes no mesmo cluster
		cluster_list retorna uma lista de filmes no mesmo cluster
	'''
    size = len(name_clust)

    mv_clus = []

    for i in range(size):
        for j in name_clust[i][1]:
            if j == cluster_number:
                mv_clus.append(name_clust[i][0])

    return mv_clus

def get_sinopses(mv_clus):
	'''
		input:
			- mv_clus é uma lista de filmes em um cluster
		output:
			- sinopse uma lista com as sinopses dos filmes
		get_sinopses retorna uma lista com as sinopses de
        uma lista de filmes
	'''
    movie_sinopse_list = []
    clustered_movies = mv_clus

    with open(os.path.join('', 'tmdb_5000_movies.json')) as file:
        movies_data = json.load(file)

        for movies in movies_data:
            for selected in clustered_movies:
                if movies['name'] == selected:
                    movie_sinopse_list.append((movies['name'], movies['overview']))

    sinopse = [x[1] for x in movie_sinopse_list]
    return sinopse
