#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json, os

DIR = os.path.dirname(os.path.abspath(__file__))
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

movies = []
num_movies = 0

print()

with open(DIR+'/dataset/tmdb_5000_movies.csv') as f:
	f.readline() # ignora o cabeçalho
	for line in f:
		num_movies += 1
		m = get_movie_info(line)
		if m != {}:
			movies.append(m)

with open(DIR+'/dataset/tmdb_5000_movies.json', 'w') as f:
	json.dump(movies, f)

print("Imported: {:d}, Dropped: {:d}".format(len(movies), num_movies - len(movies)))