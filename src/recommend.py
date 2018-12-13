#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json
import numpy as np

VERBOSE = False
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')

if __name__ == '__main__':
	if VERBOSE: print("Carregando dados...")
	# Load clusters
	clusters_data = np.load(os.path.join(DIR, 'clusters_data.npy'))
	# Load user data
	with open(os.path.join(DIR, 'user_movies.json')) as file:
		user_movies = json.load(file)
	# Load Movies Data
	with open(os.path.join(DIR, 'tmdb_5000_movies.json')) as file:
		movies_data = json.load(file)
	# Build movie clusters data base
	if VERBOSE: print("Construindo data base...")
	db = {}
	for idx, movie in enumerate(movies_data):
		m = {}
		m['clusters'] = []
		m['points'] = 0
		m['watched'] = False
		m['genres'] = movie['genres']
		m['keywords'] = movie['keywords']
		for cluster in clusters_data:
			m['clusters'].append(cluster[idx-1])
		db[movie['name']] = m
	# Pontuate the movies
	if VERBOSE: print("Pontuando filmes...")
	gb = 0
	gt = 0
	kb = 0
	kt = 0
	for movie in user_movies:
		# Ignore missing movies
		if not movie['title'] in db:
			continue
		# Set the movie as watched
		db[movie['title']]['watched'] = True
		# Increase points of movies in the same clusters
		for m in db:
			for cluster in db[m]['clusters']:
				if cluster in db[movie['title']]['clusters']:
					db[m]['points'] += movie['rating'] - 5
					if len( set(db[movie['title']]['genres']) & set(db[m]['genres'])) > 0:
						gb += 1
					gt += 1
					if len( set(db[movie['title']]['keywords']) & set(db[m]['keywords'])) > 0:
						kb += 1
					kt += 1
	if VERBOSE: print("Genres:", "%.2f%%"%(100*gb/gt))
	if VERBOSE: print("Keywords:", "%.2f%%"%(100*kb/kt))
	# Remove filmes assistidos
	if VERBOSE: print("Removendo filmes assistidos...")
	to_remove = []
	for m in db:
		if db[m]['watched'] == True:
			to_remove.append(m)
	for m in to_remove:
		del db[m]
	del to_remove
	# Ordena
	if VERBOSE: print("Ordenando...")
	movies_list = []
	for movie in db:
		movies_list.append( (movie, db[movie]['points']) )
	movies_list.sort(key = lambda t: t[1])
	# Recomenda
	print("Recomendações: ")
	for movie in movies_list[-10:]:
		if VERBOSE:
			print(movie)
		else:
			print(movie[0])
