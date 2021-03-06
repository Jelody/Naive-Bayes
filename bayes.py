from numpy import *
import codecs

def loadData():
	pList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
				['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
				['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
				['stop', 'posting', 'stupid', 'worthless', 'garbage'],
				['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
				['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0,1,0,1,0,1]
	return pList, classVec

def Create1(dataSet):
	vocabSet = set([])
	for document in  dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

def Words2Vec(vocabList, inputSet):
	Vec_return = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			Vec_return[vocabList.index(word)] = 1
		else: 
			print("the word: %s is not in my Vocablary!" % word)
	return Vec_return

def Words_bag(vocabList, inputSet):
	Vec_return = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			Vec_return[vocabList.index(word)] += 1
	return Vec_return

def train(trainMatrix, trainCategory):
	TrainDocs_num = len(trainMatrix)
	Words_num = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(TrainDocs_num)
	p0Num = ones(Words_num); p1Num = ones(Words_num)
	p0Denom = 2.0; p1Denom = 2.0

	for i in range(TrainDocs_num):
		if trainCategory[i] ==1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = p1Num/p1Denom
	p0Vect = p0Num/p0Denom
	p1Vect = log(p1Num/p1Denom)
	p0Vect = log(p0Num/p0Denom)
	return p0Vect, p1Vect, pAbusive

def Classify(vec2Classify, p0Vec, p1Vec, pClass1):
	p1 = sum(vec2Classify * p1Vec) + log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def Test_NB():
	list_Post,list_Classes = loadData()
	myVocabList = Create1(list_Post)
	trainMat = []
	for postinDoc in list_Post:
		trainMat.append(Words2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = train(trainMat,list_Classes)

	testEntry = ['love', 'my', 'dalmation']
	thisDoc = array(Words2Vec(myVocabList, testEntry))
	print(testEntry,'classified as: ', Classify(thisDoc, p0V, p1V, pAb))

	testEntry = ['stupid', 'garbage']
	thisDoc = array(Words2Vec(myVocabList, testEntry))
	print(testEntry,'classified as: ', Classify(thisDoc, p0V, p1V, pAb))

def Text(bigString):
	import re
	listOfTokens = re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]
 
def Test_spam():
	docList = []; classList = []; fullText = []
	for i in range(1, 26):
		wordList = Text(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = Text(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = Create1(docList)
	trainingSet = list(range(50)); testSet = []
	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []; trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(Words_bag(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V, p1V, pSpam = train(array(trainMat), array(trainClasses))
	errorCount = 0
	for docIndex in testSet:
		wordVector = Words_bag(vocabList, docList[docIndex])
		if Classify(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
			print("classification error",docList[docIndex])
	print('the error rate is: ', float(errorCount)/len(testSet))

