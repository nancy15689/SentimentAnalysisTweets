#!/usr/bin/env python
import argparse
import csv
import errno
import os
import operator
import numpy
from math import *

class lang_models():
	
	def __init__(self, data, indices):
		self.unigram_model = {}
		self.bigram_model = {}
		self.tokens = data 
		self.indices = indices
		self.ngram_model_gen()

	def ngram_model_gen(self): 
		for index in range(len(self.indices)): 
			if index % 2 == 0: 
				start = self.indices[index]
				end = self.indices[index + 1]
				for i in range(start, end): 
					self.unigram_model[self.tokens[i][0]] = self.unigram_model.get(
						self.tokens[i][0], 0) + 1 
					for j in range(1, len(self.tokens[i])): 
						self.unigram_model[self.tokens[i][j].lower()] = self.unigram_model.get(
							self.tokens[i][j].lower(), 0) + 1 
						word_tuple = self.tokens[i][j - 1].lower(), self.tokens[i][j].lower()
						self.bigram_model[word_tuple] = self.bigram_model.get(
							word_tuple, 0) + 1

	def unknown(self, offset): 
		unknown_count = 0
		self.unigram_model_unknown = {} 
		for k, v in self.unigram_model.items():
			if v == 1:
				unknown_count = unknown_count + 1
			else:
				self.unigram_model_unknown[k] = v
		self.unigram_model_unknown["<unknown>"] = unknown_count

		self.bigram_model_unknown = {} 
		for k, v in self.bigram_model.items():
			prev_w, w = k
			if w not in self.unigram_model_unknown:
				w = "<unknown>"
			if prev_w not in self.unigram_model_unknown:
				prev_w = "<unknown>"
			self.bigram_model_unknown[(prev_w, w)] = self.bigram_model_unknown.get(
				(prev_w, w), 0) + v * offset

	def smoothing(self, k_smooth = 0.01): 
		unigram_base = self.unigram_model_unknown
		if unigram_base != None and len(unigram_base) == 0: 
			unigram_base = self.unigram_model
		unigram_model = {k:(v + k_smooth)*1.0/(sum(unigram_base.values())+
			(len(unigram_base) * k_smooth)) for k, v in unigram_base.items()}

		bigram_model = {}
		bigram_base = self.bigram_model_unknown
		if bigram_base != None and len(bigram_base) == 0: 
			bigram_base = self.bigram_model
		for k, v in bigram_base.items(): 
			prev_w, w = k 
			bigram_model[k] = (v + k_smooth) * 1.0 / (unigram_base[prev_w] + 
				len(unigram_base) * k_smooth)

		return unigram_model, bigram_model
