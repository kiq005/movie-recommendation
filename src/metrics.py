#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dist_matrix
from collections import Counter

def common_elements(arr, num):
	return Counter(arr).most_common(num)

def longest_overview(data):
	longest = None
	long_len = -1
	for movie in data:
		cur_len = len(movie['overview'])
		if longest == None or cur_len > long_len:
			longest  = movie
			long_len = cur_len
	return longest


def shortest_overview(data):
	shortest = None
	short_len = -1
	for movie in data:
		cur_len = len(movie['overview'])
		if shortest == None or cur_len < short_len:
			shortest  = movie
			short_len = cur_len
	return shortest


def get_words(data):
	words = []
	for movie in data:
		words += movie['overview'].split()
	return words

def get_tokens(data):
	tokens = []
	for movie in data:
		tokens += dist_matrix.get_tokens(movie['overview'])
	return tokens

def get_bigrams(data):
	bigrams = []
	for movie in data:
		bigrams += dist_matrix.get_bigrams(movie['overview'])
	return bigrams

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