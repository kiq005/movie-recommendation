#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Verifica a relação entre o data set e os filmes assistidos pelo usuário
'''
import os, sys, json

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')

if __name__ == '__main__':
	# Carrega os filmes do dataset
	with open(os.path.join(DIR, 'tmdb_5000_movies.json')) as file:
		ds_data = [movie['name'] for movie in json.load(file)]
	# Carrega os filmes ranqueados pelo usuário
	with open(os.path.join(DIR, 'user_movies.json')) as file:
		user_data = [movie['title'] for movie in json.load(file)]
	# Exibe as informações
	print("Filmes no Dataset:", len(ds_data))
	print("Avaliados pelo usuário:", len(user_data))
	print("Filmes avaliados presentes no Dataset:", len(set(ds_data) & set(user_data)))
