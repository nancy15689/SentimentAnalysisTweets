# Project Proposal 

To: ORIE 4741

From: Yu (Nancy) Gu yg234, Jiangyue (Sophia) Zhu jz552 

Subject: Proposal for sentiment analysis project

Date: September 22, 2017 

Problem Statement 

As social media become an important part of human life, there is a copious amount of information people can find from tweets, online reviews, blogs, and other channels. Although this information helps us gain knowledge in fields we are unfamiliar with and express our opinions openly, it also creates the problem of information overload, and the majority of us cannot filter out useful information among the gigantic sources of data. We want to explore the problem of sentiment analysis, analyzing people’s attitudes towards a certain subject by identifying and extracting information from text pieces. This is an important problem because by programmatically gathering information from people’s written pieces with high accuracy, it can save a lot of manual work and effectively filter out information we want to see. In this project we are going to use people’s tweets as our dataset since tweets are a form of informal communication containing vast amount of sass and idiom, and are the most similar to how people communicate in daily life. Details about our dataset can be found in the next section. Since the dataset is fairly big and in detail and is closely related to a relaxed form of communication, we believe that it can facilitate our initial analysis on humans’ choice of words upon expressing positive or negative opinions. This project is worthwhile since it has a lot of potential applications. For example, we can train our model to identify a majority of internet users’ attitudes towards a certain subject such as “Donald Trump”. It can also be trained to react to negative reviews on the Internet for users to be alerted for certain products. We have a lot of hope for the success of this project since similar studies have been done on TripAdvisor reviews and other form of online information. By properly processing our dataset and adjusting language models based on dataset attributes, we believe we can evaluate people’s degrees of opinions successfully. 

Description of dataset 

The dataset we’re planning to use for sentiment analysis is from http://help.sentiment140.com/for-students about tweets’ sentiment polarity. The details about how the data is collected and annotated can be found on the website. The dataset contains tweets with annotated polarity, and the date, id, query, user of the tweet. It dataset is a csv file with size 238MB, it has 6 columns and 1600000 rows(1600000 tweets). For this project’s sentiment analysis, we will process the data further more and only use the date, polarity, text of the tweets, and discard all other columns. The polarity of the tweet is represented by numbers 0,2,or 4, where 0 is negative, 2 is neutral and 4 is positive. The date format is [date of week] [space] [month] [space] [day] [space] [hour] [:] [minute] [:] [second] [space] [time] [space] [year]. The tweet text contains uppercase and lowercase letters, number, as well as symbols and punctuations. Preliminary data analysis shows there are 800000 negative tweets and 800000 positive tweets. The average length of tweet text(string length, not word count) is 74.1. The average length of negative tweet is 74.3, the average of positive tweet is 73.9. We’re planning to get our training and test data from the same dataset using k-fold validation method. We are planning to divide the whole dataset into k partitions, and use k-1 partitions for training, the remaining one partition for testing, record the accuracy and then repeat the process for k-1 times so we will get k accuracy number. After that, we will average the accuracy by summing the k accuracies and divide it by k.
