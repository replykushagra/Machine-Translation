import re
from itertools import izip
import itertools as iter
import numpy as np
import sys	
def corpusSentences():
	d={}
	innerd={}
	iter=0
	l=[]
#Opening English nd German corpus files 		
	with open(sys.argv[1]) as english, open(sys.argv[2]) as german:
		for line1,line2 in izip(english,german):
#Appending Null to every english sentence
			match1=['NULL'];
#Regular expression for retrieving english sentences
			match1=match1+re.findall(r'[A-Za-z0-9\-\']+',line1,re.I)
#Regular expression for retrieving german sentences
			match2=re.findall(r'[A-Za-z0-9\-\'\&\;]+',line2,re.I)
#Finding initial t(f/e)
			for word in match1:
				iter=0		
				for words in match2:
#Dictionary within a dictionary. Initializing the parent key with a inner dictionary
					innerd={}
					if word not in d:
						d[word]=innerd
#Assinging defualt 0 to every english,german pair
					if words not in d[word]:
						d[word][words]=0
#Assigning actual t(f/e) counts to every english,german pair 
		for english in d:
			iter=0
			for german in d[english]:
				iter=iter+1
			for german in d[english]:
				d[english][german]=float(1.0/iter)
	print d
	print "Please wait until final dictionary is being computed....."
#By this time we have the initial t(f/e) for all german,english pairs in dictionary 'd'
	iteration=0
	sum=0.0
	tempDict={}
	while(iteration<10):
		with open(sys.argv[1]) as english, open(sys.argv[2]) as german:
		
			iteration=iteration+1
			for line1,line2 in izip(english,german):
				match1=['NULL'];
#match1 has the english list , match2 has the german list of words
				match1=match1+re.findall(r'[A-Za-z0-9\-\']+',line1,re.I)
				match2=re.findall(r'[A-Za-z0-9\-\'\&\;]+',line2,re.I)
				sum=0
				m=1
#In every aligned german sentnece finding one german word and aligning with every english word
				for germanWord in match2:
					total=0
					for englishWord in match1:
						if germanWord in d[englishWord]:						
							total=total+d[englishWord][germanWord]
#Dividing the t(f/e) by the total (sum of all t(f/e) f being the same and varying english word in that sentence)
					for englishWord in match1:
						if germanWord in d[englishWord]:
							if germanWord not in tempDict:
								tempDict[germanWord]={}
							if englishWord not in tempDict[germanWord]:
								tempDict[germanWord][englishWord]=0				
							tempDict[germanWord][englishWord]=tempDict[germanWord][englishWord]+(d[englishWord][germanWord]/total)
#Temporary dictionary to original dictionary
			for keys in tempDict:
				for newKeys in tempDict[keys]:
					if keys in d[newKeys]:				
						d[newKeys][keys]=tempDict[keys][newKeys]
#For each english words findinf sum of all t(f/e), e being the same assigning the result to sum
			for keys in d:
				sum=0
				for newKeys in d[keys]:
					sum=sum+d[keys][newKeys]
				for newKeys in d[keys]:
					d[keys][newKeys]=float(d[keys][newKeys]/sum)				
	print d
#Finding words, probabilities for man, mediator
	manList=[]
	manName=[]
	mediatorList=[]
	mediatorName=[]
	for englishKeys in d:
		if englishKeys=='man':
			for germanKeys in d[englishKeys]:
				manList.append(d[englishKeys][germanKeys])
				manName.append(germanKeys)	
		if englishKeys=='mediator':
			for germanKeys in d[englishKeys]:
				mediatorList.append(d[englishKeys][germanKeys])
				mediatorName.append(germanKeys)
	print "man"
	manList,manName=zip(*sorted(zip(manList,manName)))	
	print manList[-5:],
	print manName[-5:]
	print "mediator"
	mediatorList,mediatorName=zip(*sorted(zip(mediatorList,mediatorName)))
	print mediatorList[-5:],
	print mediatorName[-5:]
#Reading the argument 3 which is devword and finding all the corresponding german words with the probabilities
	with open(sys.argv[3]) as devwords:
		for line in devwords:
			match=re.findall(r'[A-Za-z0-9\-\'\&\;]+',line,re.I)
			for words in match:
				print "German words for", words
				for germanWords in d[words]:
					print germanWords,d[words][germanWords]
			print ""
def main():
	corpusSentences()

if __name__ == '__main__':
	main()
