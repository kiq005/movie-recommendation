#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json, os
import numpy as np
import nltk

VERBOSE = True
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+"

def get_tokens(text, language='english'):
	'''
		input:
			- text é o texto o qual se deseja obter os tokens
			- language é o idioma do texto
		output:
			- uma lista de tokens
		Obtém uma lista de tokens sem stop words
	'''
	# Obtém as palavras, removendo pontuações e números
	words = re.findall(regex, text)
	# Remove stop words
	words = [word.lower() for word in words if word.lower() not in nltk.corpus.stopwords.words(language)]
	return words

def get_bigrams(text, language='english'):
	'''
		input:
			- text é o texto o qual se deseja construir os bigramas
			- language é o idioma do texto
		output:
			- uma lista de bigramas
		obtém uma lista de bigramas construidos com base na função get_tokens
	'''
	# Obtém os tokens
	tokens = get_tokens(text, language)
	# Transforma os tokens para um conjunto de bigramas
	return set(list(nltk.bigrams(tokens)))

def linear(val):
	'''
		input:
			- o valor numérico entre 0 e 1
		output:
			- o valor calculado entre 0 e 1
		retorna um valor linear do tipo f(x)=x
	'''
	return val

def quad(val):
	'''
		input:
			- o valor numérico entre 0 e 1
		output:
			- o valor calculado entre 0 e 1
		aplica e retorna o valor de f(x)=-x²+2x
	'''
	return -(val*val)+2*val

#methods: binary_distance, jaccard_distance, masi_distance, edit_distance(com list)
def compare_bigrams(set_a, set_b, method=nltk.jaccard_distance, func=quad):
	'''
		input:
			- set_a é o primeiro conjunto de referência
			- set_b é o segundo conjunto de referência
			- method é a função com o método de distanciamente dos conjuntos
			- func é a função de escalonamento do valor de distância obtido
		output:
			- o valor de distância calculado
		calcula a distância entre os conjuntos set_a e set_b, com base no method escalonado pela func
	'''
	return func(1 - method(set_a, set_b))

def get_data(file_name):
	'''
		input:
			- file_name nome no arquivo na pasta dataset para se obter os dados
		output:
			- um dict com os dados lidos do arquivo
		lê e retorna os dados de um arquivo .json
	'''
	data = None
	with open(os.path.join(DIR, file_name)) as file:
		data = json.load(file)
	return data

if __name__ == '__main__':
	# Lê dataset
	if VERBOSE: print("Lendo dataset...")
	data = get_data('tmdb_5000_movies.json')
	# Obtém a lista de bigramas de cada overview
	if VERBOSE: print("Obtendo tokens...")
	tokens = []
	for movie in data:
		b = get_bigrams(movie['overview'])
		if len(b) > 0:
			tokens.append(b)
		else:
			print('ATENÇÃO: Não foi possível obter bigramas do filme "', movie['name']['english'], '"')
			#print(b, movie)
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

