#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json, os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
CSV_REGEX = r'(\d+),"?(\[[^\]]+\]|\[\])"?,([^,]+)?,(\d+),"?(\[[^\]]+\]|\[\])"?,(\w+),"?([^\"]+)"?,"?([^\"]+)"?,(\d+\.\d+)?,?"?(\[[^\]]+\]|\[\])"?,"?(\[[^\]]+\]|\[\])"?,(\d{4}-\d{2}-\d{2})?,(\d+),(\d+\.?\d*)?,"?(\[[^\]]+\]|\[\])"?,([^,]+),([^,]+|"[^"]+")?,"?([^\"]+)"?,(\d{1,2}\.\d{1,2}),(\d+)'
DLIST_REGEX = r'{[^}]+}'
QUOTES_REGEX = r'(""([^\"]+)"")'

def get_movie_info(line):
	# Troca aspas duplas duplicadas por aspas simples
	p = re.compile(QUOTES_REGEX)
	line = p.sub(r"'\2'", line)
	# Busca o regex
	m = re.search(CSV_REGEX, line)
	if m == None:
		#print(line)
		return {}
	# Constroi o objeto
	movie = {}
	# Nome
	movie['name'] = {'original':m.group(7), 'english':m.group(18)}
	# Votos
	movie['votes'] = {'average':m.group(19), 'count':m.group(20)}
	# Tagline
	movie['tagline']  = m.group(17)
	# Sumário
	movie['overview'] = m.group(8)
	## Palavras chave
	#movie['keywords'] = []
	#n = re.findall(DLIST_REGEX, m.group(5))
	#for keyword in n:
	#	movie['keywords'].append(keyword.split('"')[10])
	## Gêneros
	#movie['genres'] = []
	#n = re.findall(DLIST_REGEX, m.group(2))
	#for genre in n:
	#	movie['genres'].append(genre.split('"')[10])

	return movie


def read_movies(path, display_quantity=False, limit=-1):
	movies = []
	num_movies = 0
	with open(path) as f:
		f.readline() # ignora o cabeçalho
		for line in f:
			num_movies += 1
			m = get_movie_info(line)
			if m != {}:
				movies.append(m)
			if limit > 0 and num_movies >= limit:
				break
	if display_quantity:
		print("Imported: {:d}, Dropped: {:d}".format(len(movies), num_movies - len(movies)))
	return movies

def save_data(data, path):
	with open(path, 'w') as f:
		json.dump(data, f)

if __name__ == "__main__":
	movies = read_movies(os.path.join(DIR, 'tmdb_5000_movies.csv'), True)
	save_data(movies, os.path.join(DIR, 'tmdb_5000_movies.json') )
