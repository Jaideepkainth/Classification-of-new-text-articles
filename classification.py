import os
import re
from nltk.corpus import stopwords
import math

thisPath = os.path.dirname(os.path.abspath(__file__))
thisPath=thisPath+'/'+"20_newsgroups"
newsgroups = os.listdir(thisPath)
stopwords = set(stopwords.words('english'))
unique={}
category_words={}
num_files=0
total_files=0
#Training Part
for category in newsgroups:
	num_words=0
	files=os.listdir(thisPath+'/'+category)
	num_files=int(len(files)/2) #Take half files for training and rest half for testing
	total_files=total_files+num_files
	for i in range (0,num_files):
		file1=open(thisPath+'/'+category+'/'+files[i])
		file1_read=file1.read().lower()
		file1_read_special=re.sub('\W+', ' ',file1_read) #Delete special characters from string
		file1_read_digit=re.sub('\d+', '', file1_read_special).strip() #Delete digits from string
		words=file1_read_digit.split(' ')
		for word in words:
			if not word:
				continue #To eliminate null Strings
			else:
				num_words+=1 #This will calculate number of words in each category
				if word not in stopwords:
					if word not in unique:
						unique[word]={}
					count_word = unique[word].get(category, 0)
					unique[word][category] = count_word + 1 #Number of times that word appeared in each category
	category_words[category]=num_words
# print(category_words)
unique_total=len(unique) #Total number of unique words

#Testing Part
right=0
for category in newsgroups:
	files=os.listdir(thisPath+'/'+category)
	num_files=int(len(files)/2)
	for i in range (num_files,len(files)):
		file1=open(thisPath+'/'+category+'/'+files[i])
		file1_read=file1.read().lower()
		file1_read_special=re.sub('\W+', ' ',file1_read) #Delete special characters from string
		file1_read_digit=re.sub('\d+', '', file1_read_special).strip() #Delete digits from string
		words=file1_read_digit.split(' ')
		probability_categories={}
		for each_category in newsgroups:
			total_prob=0
			for word in words:
				if not word:
					continue #To eliminate null Strings
				else:
					if word not in stopwords:
						if word in unique:
							num_counts=unique[word].get(each_category, 0)
							prob=(num_counts+1)/(category_words[each_category]+unique_total)
							total_prob=total_prob+math.log(prob)
			total_prob_prior=total_prob+math.log(len(files)/total_files) #Adding prior probability
			probability_categories[each_category]=total_prob_prior
		answer=max(probability_categories, key=probability_categories.get)
		if(category==answer):
			right+=1
print("Accuracy is: ", (right/total_files)*100,"%")