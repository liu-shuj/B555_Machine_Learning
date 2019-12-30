from core.unigram import TrainPD,LogEvidence
from core.metrics import CalcPP
from utils.text import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dict', help="path of the word dictionary")
parser.add_argument('--training_set', help="path of the training data file")
parser.add_argument('--training_size', help="size(count of tokens) of training file to use")
parser.add_argument('--test_set', help="path of the testing data file")
parser.add_argument('--test_size', help="size(count of tokens) of testing file to use")
args=parser.parse_args()

wordList=GenWordList(args.dict)
for alphap in range(1,11):
    tokenSeqTrain = TokenSeqFromFile(args.training_set, int(args.training_size))
    alphaDict = {}
    for word in wordList:
        alphaDict[word] = alphap
    prDict = TrainPD(tokenSeqTrain,alphaDict)

    tokenSeqTest = TokenSeqFromFile(args.test_set,int(args.test_size))
    PP=CalcPP(tokenSeqTest,prDict)
    tokenSeqTest = TokenSeqFromFile(args.test_set,int(args.test_size))  # reset the generator which has reached the end
    le=LogEvidence(tokenSeqTest,alphaDict)
    print("alphaPrime={alphap}, perplexity={PP}, logEvidence={le}".format(alphap=alphap,PP=PP,le=le))
	

