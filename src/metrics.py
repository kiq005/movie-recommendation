#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Realiza diversas medidas sobre os dados gerados
'''
import dist_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import nltk
import numpy as np

def common_elements(arr, num):
	'''
		input:
			- arr é uma lista de elementos
			- num é a quantidade de elementos para retornar
		output:
			- uma lista de elementos mais comúns
		common_elements verifica e retorna uma determinada
		quantidade de elementos mais comúns em uma lista
	'''
	return Counter(arr).most_common(num)

def longest_overview(data):
	'''
		input:
			- data é uma lista com filmes
		output:
			- longest é o filme com o sumário mais longo
		longest_overview verifica e retorna o filme com a sinópse mais
		longa numa lista de filmes
	'''
	longest = None
	long_len = -1
	for movie in data:
		cur_len = len(movie['overview'])
		if longest == None or cur_len > long_len:
			longest  = movie
			long_len = cur_len
	return longest


def shortest_overview(data):
	'''
		input:
			- data é uma lista com filmes
		output:
			- shortest é o filme com o sumário mais longo
		shortest_overview verifica e retorna o filme com a sinópse mais
		curta numa lista de filmes
	'''
	shortest = None
	short_len = -1
	for movie in data:
		cur_len = len(movie['overview'])
		if shortest == None or cur_len < short_len:
			shortest  = movie
			short_len = cur_len
	return shortest


def get_words(data):
	'''
		input:
			- data é uma lista com filmes
		output:
			- words é a lista de palavras em todos os filmes
		get_words retorna todas as palavras presentes nas sinopses
		de todos os filmes
	'''
	words = []
	for movie in data:
		words += movie['overview'].split()
	return words

def get_tokens(data):
	'''
		input:
			- data é uma lista com filmes
		output:
			- tokens é a lista de tokens em todos os filmes
		get_tokens retorna todos os tokens presentes nas sinopses
		de todos os filmes
	'''
	tokens = []
	for movie in data:
		tokens += dist_matrix.get_tokens(movie['overview'])
	return tokens

def get_bigrams(data):
	'''
		input:
			- data é uma lista com filmes
		output:
			- bigrams é a lista de bigramas em todos os filmes
		get_bigrams retorna uma lista contendo os bigramas de todos
		os filmes
	'''
	bigrams = []
	for movie in data:
		bigrams += dist_matrix.get_bigrams(movie['overview'])
	return bigrams

def tf_idf(corpus, stopwords, top_n_words=9):
	'''
		input:
			- corpus é a base de dados
			- stopwords é uma lista de palavras vazias
			- top_n_words é a quantidades de palavras para retornar
		output:
			- global_top_features é a lista de features
		tf_idf retorna uma lista de palavras mais relevantes em um conjunto
		de textos
	'''
	vectorizer = TfidfVectorizer(stop_words=stopwords, ngram_range=(1,2))
	X = vectorizer.fit_transform(corpus)

	feature_array = np.array(vectorizer.get_feature_names())

	score_list = []
	size = len(corpus)

	for i in range(size):
	    #scores in a single doc
	    tfidf_score_single_doc = X[i].toarray().flatten()
	    #ordering
	    indices = np.argsort(tfidf_score_single_doc)[::-1]
	    #group feature and score
	    local_top_features = [(feature_array[j], tfidf_score_single_doc[j]) for j in indices]
	    #add to global list
	    score_list.extend(local_top_features)

	#alias
	top_n = top_n_words

	global_top_features = sorted(score_list, key=lambda score: score[1], reverse=True)[:top_n]

	return global_top_features

if __name__ == '__main__':
	# Get data
	data = dist_matrix.get_data('tmdb_5000_movies.json')
	# Collect metrics
	lo = longest_overview(data)
	so = shortest_overview(data)

	# Print data
	print("-- Shortest Overview --")
	print(so['name'])
	print(so['overview'])

	print("\n-- Longest Overview --")
	print(lo['name'])
	print(lo['overview'])

	print("\n-- Common Words --")
	print("Word\tCount\n")
	for p in common_elements(get_words(data), 10):
		print("%s\t%s"%(p[0], p[1]))

	print("\n--  Common Words (no stop words) --")
	print("Word\tCount\n")
	for p in common_elements(get_tokens(data), 10):
		print("%s\t%s"%(p[0], p[1]))

	print("\n-- Common Bigrams --")
	print("Bigram\t\tCount\n")
	for p in common_elements(get_bigrams(data), 10):
		print("(%s,%s)\t%s"%(p[0][0], p[0][1], p[1]))
