#!/usr/bin/env python
import ngram 
import csv 
import argparse
import time 
from math import * 

START_TOKEN = '<s>'
END_TOKEN = '</s>'
pos_trainset = [] 
neg_trainset = [] 
pos_id = [] 
neg_id = [] 
pos_date = [] 
neg_date = [] 
pos_query = [] 
neg_query = [] 
pos_author = [] 
neg_author = []
pos_perplexity = [] 
neg_perplexity = [] 
test_set = [] 
test_perplexity = [] 
test_y = [] 

def separate_nots(string):
	if (string[-3:] == "n't"):
		if string.lower() == "can't":
			return ["can", "'t"]
		else:
			return [string[:-3], "n't"]
	else:
		return [string]

def one_line(string):
	pre = 0
	current = 0
	arr = []
	punctuation = {"?":0,"!":1, ",":2, ".":3, ";":4}
	while current < len(string):
		if string[current] in punctuation:
			if pre < current:
				arr.extend(separate_nots(string[pre:current]))
			if punctuation[string[current]] == 3 and current < len(string) - 2 and string[current:current+3] == "...":
				arr.append(string[current:current+3])
				current += 3
				pre = current
			else:
				arr.extend(separate_nots(string[current]))
				current += 1
				pre = current
		elif string[current] == " ":
			if pre < current:
				arr.append(string[pre:current])
			current += 1
			pre = current
		else:
			current += 1
	return arr 

# read training data, insert start and end token, and save each line to trainset
def read_training_data(train_path, emoticon): 
	with open(train_path, 'rt') as file:
		count = 0 
		for line in file:
			if not line: continue
			parts = line.split(",")
			if emoticon == 0: 
				pos_id.append(parts[1])
				pos_date.append(parts[2])
				pos_query.append(parts[3])
				pos_author.append(parts[4])
			else: 
				neg_id.append(parts[1])
				neg_date.append(parts[2])
				neg_query.append(parts[3])
				neg_author.append(parts[4])				
			line_token = one_line(parts[5])
			line_token.insert(0, START_TOKEN)
			line_token.append(END_TOKEN)
			if emoticon == 0: 
				pos_trainset.append(line_token)
			else: 
				neg_trainset.append(line_token)

def read_testing_data(test_path): 
	global test_y, test_set
	with open(test_path, 'rt') as file: 
		for line in file: 
			if not line: continue 
			parts = line.split(",")
			test_y.append(parts[0])
			line_token = one_line(parts[5])
			line_token.insert(0, START_TOKEN)
			line_token.append(END_TOKEN)
			test_set.append(line_token)

# return unigram and bigram to train on part of dataset and with k smoothing
def train(list_indices, emoticon): 
	if emoticon == 0: 
		return ngram.lang_models(pos_trainset, list_indices)
	else: 
		return ngram.lang_models(neg_trainset, list_indices)

def evaluate(emoticon, pos_unigram, pos_bigram, neg_unigram, neg_bigram, start, end, degree, k): 
	correct = 0 
	for i in range(start, end): 
		if emoticon == 0: 
			tokens = pos_trainset[i] 
		else: 
			tokens = neg_trainset[i]
		prob_pos = 0 
		prob_neg = 0 
		if degree == 1: 
			for j in range(len(tokens)): 
				if tokens[j] not in pos_unigram: 
					prob_pos += log(pos_unigram["<unknown>"])
				else: 
					prob_pos += log(pos_unigram[tokens[i]])
				if tokens[j] not in neg_unigram: 
					prob_neg += log(neg_unigram["<unknown>"])
				else: 
					prob_neg += log(neg_unigram[tokens[i]])
		elif degree == 2: 
			for j in range(1, len(tokens)): 
				prev_w = tokens[j - 1]
				w = tokens[j]
				if prev_w not in pos_unigram: 
					prev_w = "<unknown>"
				if w not in pos_unigram: 
					w = "<unknown>"
				if (prev_w, w) in pos_bigram: 
					prob_pos += log(pos_bigram[(prev_w, w)])
				else: 
					prob_pos += log(k * 1.0 /(pos_unigram[prev_w] + len(pos_unigram) * k))
				prev_w = tokens[j - 1]
				w = tokens[j]
				if prev_w not in neg_unigram: 
					prev_w = "<unknown>"
				if w not in neg_unigram: 
					w = "<unknown>"
				if (prev_w, w) in neg_bigram: 
					prob_neg += log(neg_bigram[(prev_w, w)])
				else: 
					prob_neg += log(k * 1.0 /(neg_unigram[prev_w] + len(neg_unigram) * k))
		if emoticon == 0 and prob_pos >= prob_neg:
			correct += 1 
		elif emoticon == 1 and prob_pos <= prob_neg: 
			correct += 1
	return correct

# cross validation with num_fold and hyperparameter search 
def cross_validate(pos_train_path, neg_train_path, num_fold):
	read_training_data(pos_train_path, 0)
	read_training_data(neg_train_path, 1)
	pos_num_train_examples = len(pos_trainset)
	neg_num_train_examples = len(neg_trainset)
	pos_num_fold_examples = pos_num_train_examples / num_fold 
	neg_num_fold_examples = neg_num_train_examples / num_fold 
	max_j = -1
	max_accuracy = 0 
	max_k = -1 
	pos_models = [] 
	neg_models = [] 
	for i in range(num_fold): 
		pos_models.append(train([0, i * pos_num_fold_examples, 
			(i + 1) * pos_num_fold_examples, pos_num_train_examples], 0))
		neg_models.append(train([0, i * neg_num_fold_examples, 
			(i + 1) * neg_num_fold_examples, neg_num_train_examples], 1))
	for j in range(6, 7): 
		j_fraction = j * 0.1
		for i in range(num_fold): 
			pos_models[i].unknown(j_fraction)
			neg_models[i].unknown(j_fraction)			 
		for k in range(85, 86): 
			k_fraction = k * 0.01
			print j_fraction, k_fraction
			pos_evaluation_accuracy = 0 
			neg_evaluation_accuracy = 0 
			for l in range(num_fold): 
				pos_unigram, pos_bigram = pos_models[l].smoothing(k_fraction)
				neg_unigram, neg_bigram = neg_models[l].smoothing(k_fraction)
				pos_evaluation_accuracy += evaluate(0, pos_unigram, pos_bigram, 
					neg_unigram, neg_bigram, l * pos_num_fold_examples, 
					min((l + 1) * pos_num_fold_examples, pos_num_train_examples), 2, k_fraction)
				neg_evaluation_accuracy += evaluate(1, pos_unigram, pos_bigram, 
					neg_unigram, neg_bigram, l * neg_num_fold_examples, 
					min((l + 1) * neg_num_fold_examples, neg_num_train_examples), 2, k_fraction)
			pos_evaluation_accuracy /= (num_fold * 1.0)
			neg_evaluation_accuracy /= (num_fold * 1.0)
			evaluation_accuracy = pos_evaluation_accuracy + neg_evaluation_accuracy 
			print evaluation_accuracy
			if max_accuracy < evaluation_accuracy:
				max_j = j_fraction 
				max_accuracy = evaluation_accuracy
				max_k = k_fraction 
	print max_accuracy * 1.0 / (pos_num_fold_examples + neg_num_fold_examples)
	final_pos_model = train([0, pos_num_train_examples], 0)
	final_neg_model = train([1, neg_num_train_examples], 1)
	final_pos_model.unknown(max_j)
	final_neg_model.unknown(max_j)
	print max_j, max_k
	return final_pos_model.smoothing(max_k), final_neg_model.smoothing(max_k), max_k

def training_perpexity_to_file(emoticon, pos_model, neg_model, k): 
	correct = 0 
	pos_unigram, pos_bigram = pos_model
	neg_unigram, neg_bigram = neg_model
	if emoticon == 0: 
		dataset = pos_trainset
		file_name = "pos_train_perplexity.txt"
	elif emoticon == 1: 
		dataset = neg_trainset
		file_name = "neg_train_perplexity.txt"
	else: 
		read_testing_data(args.test_path)
		dataset = test_set
		file_name = "test_perplexity.txt"
	with open(file_name, 'wt') as file:
		for i in range(len(dataset)): 
			tokens = dataset[i]
			prob_pos = 0 
			prob_neg = 0 
			for j in range(1, len(tokens)): 
				prev_w = tokens[j - 1]
				w = tokens[j]
				if prev_w not in pos_unigram: 
					prev_w = "<unknown>"
				if w not in pos_unigram: 
					w = "<unknown>"
				if (prev_w, w) in pos_bigram: 
					prob_pos += log(pos_bigram[(prev_w, w)])
				else: 
					prob_pos += log(k * 1.0 /(pos_unigram[prev_w] + len(pos_unigram) * k))
				prev_w = tokens[j - 1]
				w = tokens[j]
				if prev_w not in neg_unigram: 
					prev_w = "<unknown>"
				if w not in neg_unigram: 
					w = "<unknown>"
				if (prev_w, w) in neg_bigram: 
					prob_neg += log(neg_bigram[(prev_w, w)])
				else: 
					prob_neg += log(k * 1.0 /(neg_unigram[prev_w] + len(neg_unigram) * k))
			file.write(str(prob_pos) + " " + str(prob_neg) + "\n")
			if emoticon == 0: 
				pos_perplexity.append((prob_pos, prob_neg))
			elif emoticon == 1: 
				neg_perplexity.append((prob_pos, prob_neg))
			else: 
				test_perplexity.append((prob_pos, prob_neg))
			if emoticon == 0 and prob_pos >= prob_neg:
				correct += 1 
			elif emoticon == 1 and prob_pos <= prob_neg: 
				correct += 1
			elif emoticon == 2: 
				if test_y[i] == '"4"' and prob_pos >= prob_neg: 
					correct += 1 
				elif test_y[i] == '"0"' and prob_neg >= prob_pos: 
					correct += 1
	return correct

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='ngram model parameters')
	parser.add_argument("pos_train_path", type=str, 
					    help="File path of the pos training file")
	parser.add_argument("neg_train_path", type=str, 
					    help="File path of the neg training file")
	parser.add_argument("test_path", type=str, 
					    help="File path of the testing file")
	parser.add_argument("num_fold", type=int, 
							help="Number of fold for cross validation")
	args = parser.parse_args()
	optimal_parameters = cross_validate(args.pos_train_path, 
		args.neg_train_path, args.num_fold)
	pos_model, neg_model, max_k = optimal_parameters
	pos_correct = training_perpexity_to_file(0, pos_model, neg_model, max_k)
	neg_correct = training_perpexity_to_file(1, pos_model, neg_model, max_k)
	print pos_correct, neg_correct
	print "start testing"
	test_correct = training_perpexity_to_file(2, pos_model, neg_model, max_k)
	print test_correct
	# test_accuracy = test(args.test_path, optimal_parameters)