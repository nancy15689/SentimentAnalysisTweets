#!/usr/bin/env python
import datetime 
import sys 

def main(pos_train, neg_train, pos_per, neg_per, test, test_per): 
	month = [] 
	day = [] 
	hour = [] 
	minute = [] 
	second = [] 
	pos_posts = [] 
	neg_posts = [] 
	perplexity_pos = [] 
	perplexity_neg = [] 
	y = [] 
	total_pos = 0 
	total_neg = 0 
	authors_list = [] 
	pos_authors = {} 
	neg_authors = {} 
	test_month = [] 
	test_day = [] 
	test_hour = [] 
	test_minute = [] 
	test_second = [] 
	test_pos_posts = [] 
	test_neg_posts = [] 
	test_perplexity_pos = [] 
	test_perplexity_neg = [] 
	test_y = [] 
	with open(pos_train, 'rt') as file:
		for line in file:
			if not line: continue
			parts = line.split(",")
			date = datetime.datetime.strptime(parts[2][1:20], '%a %b %d %H:%M:%S')
			month.append(date.month)
			day.append(date.day)
			hour.append(date.hour)
			minute.append(date.minute)
			second.append(date.second)
			authors_list.append(parts[4])
			pos_authors[parts[4]] = pos_authors.get(parts[4], 0) + 1 
			total_pos += 1
			y.append(1)
	with open(pos_per, 'rt') as file: 
		for line in file: 
			if not line: continue
			parts = line.split(" ")
			perplexity_pos.append(parts[0])
			perplexity_neg.append(parts[1][:-1])
	with open(neg_train, 'rt') as file: 
		for line in file:
			if not line: continue
			parts = line.split(",")
			date = datetime.datetime.strptime(parts[2][1:20], '%a %b %d %H:%M:%S')
			month.append(date.month)
			day.append(date.day)
			hour.append(date.hour)
			minute.append(date.minute)
			second.append(date.second)
			authors_list.append(parts[4])
			neg_authors[parts[4]] = neg_authors.get(parts[4], 0) + 1 
			total_neg += 1
			y.append(-1)
	with open(neg_per, 'rt') as file: 
		for line in file: 
			if not line: continue
			parts = line.split(" ")
			perplexity_pos.append(parts[0])
			perplexity_neg.append(parts[1][:-1])
	for i in range(len(authors_list)): 
		pos_posts.append(pos_authors.get(authors_list[i], total_pos * 1.0 / (len(pos_authors) + len(neg_authors))))
		neg_posts.append(neg_authors.get(authors_list[i], total_neg * 1.0 / (len(pos_authors) + len(neg_authors))))
	print (len(month), len(day), len(hour), len(minute), len(second), 
		len(pos_posts), len(neg_posts), len(perplexity_pos), len(perplexity_neg))
	with open('train_input.csv', 'wt') as file: 
		for i in range(len(month)): 
			file.write(str(month[i]) + "," + 
				str(day[i]) + "," + 
				str(hour[i]) + "," + 
				str(minute[i]) + "," + 
				str(second[i]) + "," + 
				str(pos_posts[i]) + ", " + 
				str(neg_posts[i]) + ", " + 
				str(perplexity_pos[i]) + "," + 
				str(perplexity_neg[i]) + "," + str(y[i]) + "\n")

	with open(test, 'rt') as file:
		for line in file:
			if not line: continue
			parts = line.split(",")
			date = datetime.datetime.strptime(parts[2][1:20], '%a %b %d %H:%M:%S')
			test_month.append(date.month)
			test_day.append(date.day)
			test_hour.append(date.hour)
			test_minute.append(date.minute)
			test_second.append(date.second)
			test_pos_posts.append(pos_authors.get(parts[4], total_pos * 1.0 / (len(pos_authors) + len(neg_authors))))
			test_neg_posts.append(neg_authors.get(parts[4], total_pos * 1.0 / (len(pos_authors) + len(neg_authors))))
			if parts[0] == '"0"': 
				test_y.append(-1)
			elif parts[0] == '"4"': 
				test_y.append(1)
			elif parts[0] == '"2"': 
				pass 
			else: 
				print "what the fuck this is not 0, 2, 4"
	with open(test_per, 'rt') as file: 
		for line in file: 
			if not line: continue
			parts = line.split(" ")
			test_perplexity_pos.append(parts[0])
			test_perplexity_neg.append(parts[1][:-1])

	with open('test_input.csv', 'wt') as file: 
		for i in range(len(test_month)): 
			file.write(str(test_month[i]) + "," + 
				str(test_day[i]) + "," + 
				str(test_hour[i]) + "," + 
				str(test_minute[i]) + "," + 
				str(test_second[i]) + "," + 
				str(test_pos_posts[i]) + ", " + 
				str(test_neg_posts[i]) + ", " + 
				str(test_perplexity_pos[i]) + "," + 
				str(test_perplexity_neg[i]) + "," + str(test_y[i]) + "\n")

if __name__ == '__main__':
	args = sys.argv 
	main(args[1], args[2], args[3], args[4], args[5], args[6])