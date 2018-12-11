#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')

if __name__ == '__main__':
	with open(os.path.join(DIR, 'tmdb_5000_movies.json')) as file:
		ds_data = [movie['name'] for movie in json.load(file)]
	with open(os.path.join(DIR, 'user_movies.json')) as file:
		user_data = [movie['title'] for movie in json.load(file)]
	print("Filmes no Dataset:", len(ds_data))
	print("Avaliados pelo usuário:", len(user_data))
	print("Filmes avaliados presentes no Dataset:", len(set(ds_data) & set(user_data)))
