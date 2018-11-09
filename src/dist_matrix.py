#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json, os
import numpy as np
import nltk

VERBOSE = True
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+"

def get_tokens(text, language):
	# Obtém as palavras, removendo pontuações e números
	words = re.findall(regex, text)
	# Remove stop words
	words = [word for word in words if word not in nltk.corpus.stopwords.words(language)]
	return words

def get_bigrams(text, language='english'):
	# Obtém os tokens
	tokens = get_tokens(text, language)
	# Transforma os tokens para um conjunto de bigramas
	return set(list(nltk.bigrams(tokens)))

#methods: binary_distance, jaccard_distance, masi_distance, edit_distance(com list)
def compare_bigrams(set_a, set_b, method=nltk.jaccard_distance):
	return method(set_a, set_b)

if __name__ == '__main__':
	# Lê dataset
	if VERBOSE: print("Lendo dataset...")
	with open(os.path.join(DIR, 'tmdb_100_movies.json')) as file:
		data = json.load(file)
	# Obtém a lista de bigramas de cada overview
	if VERBOSE: print("Obtendo tokens...")
	tokens = []
	for movie in data:
		b = get_bigrams(movie['overview'])
		if len(b) > 0:
			tokens.append(b)
		else:
			print('ATENÇÃO: Não foi possível obter bigramas do filme "', movie['name']['english'], '"')
			#print(b, movie['overview'])
	if VERBOSE: print("Bigramas:", len(tokens))
	# Constroi a matriz de distância
	if VERBOSE: print("Construindo matriz de distância...")
	dist_matrix = np.zeros([len(tokens), len(tokens)], dtype=float)
	for i, movie_a in enumerate(tokens):
		for j, movie_b in enumerate(tokens):
			dist_matrix[i][j] =  compare_bigrams( movie_a, movie_b )
	if VERBOSE: print("Matriz:", np.shape(dist_matrix))
	# Exporta a matrix para um arquivo
	np.save(os.path.join(DIR, 'tmdb_5000_movies.npy'), dist_matrix) # Binário
	np.savetxt(os.path.join(DIR, 'tmdb_5000_movies.txt'), dist_matrix) # Texto

