#!/usr/bin/env python
import csv
import operator
import sys

def get(arg):
	dp = {}
	with open('pos_train.txt', 'rt') as file:
		# reader = csv.reader(in_file, delimeter = ",")
		for line in file:
			if not line: continue
			row = line.split(',')
			# print row[0]
			r = row[5].lower()
			s = r.split()
			for w in s:
				if w in dp:
					dp[w] += 1
				else:
					dp[w] = 1
	sorted_p = sorted(dp.items(), key=operator.itemgetter(1), reverse=True)
	sp = []
	for c in sorted_p:
		sp.append(c[0])
	dn = {}
	with open('neg_train.txt', 'rt') as file:
		# reader = csv.reader(in_file, delimeter = ",")
		for line in file:
			if not line: continue
			row = line.split(',')
			# print row[0]
			r = row[5].lower()
			s = r.split()
			for w in s:
				if w in dn:
					dn[w] += 1
				else:
					dn[w] = 1
	sorted_n = sorted(dn.items(), key=operator.itemgetter(1), reverse=True)
	sn = []
	for c in sorted_n:
		sn.append(c[0])
	for i in range(250):
		w = sp[i]
		# print i,w,sn.index(w)
		if abs(sn.index(w) - i) > arg:
			print w,sorted_p[i][1]

	print "====\n\n\n"

	for i in range(250):
		w = sn[i]
		if abs(sp.index(w) - i) > arg:
			print w,sorted_n[i][1]



if __name__ == '__main__':
	args = sys.argv 
	get(int(args[1]))