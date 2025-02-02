#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Converte os dados de um dataset em formato csv para formato json
'''
import re, csv, json, os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')

def get_movie_info_tmdb(line):
	'''
		input:
			- line é uma linha da tabela de dados no formato de lista
		output:
			- objeto contendo informações de nome, tagline, overview, keywords, e genres do filme

		get_movie_info_tmdb cria um objeto filme com os dados da linha da tabela
	'''
	try:
		# Constroi o objeto
		movie = {}
		if len(line) > 16:
			# Nome em inglês
			movie['name'] = line[17]
			if len(movie['name']) < 1:
				raise
			# Tagline
			if len(line[16]) > 0:
				movie['tagline'] = line[16]
		else:
			# Nome no idioma original
			movie['name'] = line[6]
		# Sumário
		movie['overview'] = line[7]
		if len(line[7]) < 20:
			raise
		## Palavras chave
		movie['keywords'] = []
		for k in json.loads(line[4]):
			movie['keywords'].append(k['name'])
		## Gêneros
		movie['genres'] = []
		for g in json.loads(line[1]):
			movie['genres'].append(g['name'])
		return movie
	except:
		return {}

def get_movie_info_wiki(line):
	'''
		input:
			- line é uma linha da tabela de dados no formato de lista
		output:
			- objeto contendo informações de nome, tagline, overview, keywords, e genres do filme

		get_movie_info_wiki cria um objeto filme com os dados da linha da tabela
	'''
	try:
		# Constroi o objeto
		movie = {}
		# Nome
		movie['name'] = line[1]
		# Plot
		movie['overview'] = line[-1]
		if len(movie['overview']) < 20:
			raise
		## Palavras chave
		movie['keywords'] = []
		## Gêneros
		movie['genres'] = []
		if line[5] != 'unknown':
			movie['genres'] = line[5].split()
		return movie
	except:
		return {}

def read_movies(path, display_quantity=False, limit=-1):
	'''
		input:
			- path é o caminho do arquivo de dados no formato .csv
			- display_quantity é um flag de depuração, que indica se o a chamada deve exibir o número de filmes lidos e a quantidade de filmes que não foram adicionados na lista
			- limit quando positivo, indica a quantidade máxima de filmes a serem listados, utilize para depuração
		output:
			- uma lista de objetos filme, construídos pela função get_movie_info

		read_movies retorna uma uma lista de filmes com as informações relevantes para a análise
	'''
	movies = []
	num_movies = 0
	with open(path) as f:
		f.readline() # ignora o cabeçalho
		csvdata = csv.reader(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		for line in csvdata:
			num_movies += 1
			m = get_movie_info_tmdb(line)
			# Adiciona apenas se tiver informação
			if m!= {}:
				movies.append(m)
			# Verifica o limite
			if limit > 0 and num_movies >= limit:
				break
	# Exibe informações para fins de depuração
	if display_quantity:
		print("Imported: {:d}, Dropped: {:d}".format(len(movies), num_movies - len(movies)))
	return movies

def save_data(data, path):
	'''
		input:
			- data são os dados a serem salvos
			- path é o caminho do arquivo

		save_data salva os dados para um arquivo no formato .json
	'''
	with open(path, 'w') as f:
		json.dump(data, f)

if __name__ == "__main__":
	movies = read_movies(os.path.join(DIR, 'tmdb_5000_movies.csv'), True)
	save_data(movies, os.path.join(DIR, 'tmdb_5000_movies.json') )
