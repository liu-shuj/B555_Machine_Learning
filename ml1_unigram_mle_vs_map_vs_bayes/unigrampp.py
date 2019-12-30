from core.unigram import TrainMLE,TrainMAP,TrainPD
from core.metrics import CalcPP
from utils.text import *
import argparse
import pickle
import sys

# handle console arguments
parser = argparse.ArgumentParser()

# common arguments
parser.add_argument('datafile', help="file path of training/testing data")
parser.add_argument('--datasize',help="size(in count of tokens) of the data set to be used; default is the entire file.")

# testing mode argument
parser.add_argument('--model',help="specify file path of an existing model to be used for testing")

# training mode arguments
parser.add_argument('--training', action="store_true", help="run in training mode")
parser.add_argument('--method' ,help="training method, could be 'MLE','MAP or 'PD'")
parser.add_argument('--dict', help="path of the word dictionary")
parser.add_argument('--savepath',help="specify the file path to save the model after training")
parser.add_argument('--alphap',help="specify value of alpha prime; default is 2")
parser.add_argument('--pp', action="store_true", help="calculate and display perplexity of the model on training set after training")

args=parser.parse_args()

def train():
    wordList = GenWordList(args.dict)
    print("Dictionary size is {size}.".format(size=len(wordList)))
	
    # init alpha
    if not args.alphap:
        alphap=2
    else:
        alphap=float(args.alphap)
    alphaDict = {}
    for word in wordList:
        alphaDict[word] = alphap
		
    # default size is the whole file
    if not args.datasize:
        size=sys.maxsize
    else:
        size=int(args.datasize)

    tokenSeq = TokenSeqFromFile(args.datafile, size)
	
    #do training
    if args.method == 'MLE':
        model = TrainMLE(tokenSeq, wordList)
    elif args.method == 'MAP':
        model = TrainMAP(tokenSeq, alphaDict)
    elif args.method == 'PD':
        model = TrainPD(tokenSeq, alphaDict)
    else:
        print("Please specify a method!")
        model = ""
        exit(-1)
		
	#save model
    if not args.savepath:
        if size==sys.maxsize:
            sizestr="ALL"
        else:
            sizestr="{size}".format(size=size)
        savepath=args.method+'_'+sizestr
        if args.alphap:
            savepath+='_'+args.alphap
        savepath+='.model'
    else:
        savepath=args.savepath
    with open(savepath,'wb') as f:
        pickle.dump(model, f)
		
    print("Training complete. Model saved at " + savepath + ".")
	
    if(args.pp):
        tokenSeq = TokenSeqFromFile(args.datafile, size)
        PP=CalcPP(tokenSeq,model)
        print("Perplexity of the model on the training set is {PP}.".format(PP=PP))

def test():
    if not args.model:
        print("Please specify a model. See -h for help.")
        exit(-1)

    # default size is the whole file
    if not args.datasize:
        size=sys.maxsize
    else:
        size=int(args.datasize)

    tokenSeq = TokenSeqFromFile(args.datafile, size)
	
	# load model
    with open(args.model, 'rb') as f:
        prDict = pickle.load(f)
		
	# calculate perplexity
    PP = CalcPP(tokenSeq, prDict)
	
	# display result
    if size==sys.maxsize:
        sizestr="all"
    else:
        sizestr="size {size}".format(size=args.datasize)
    print("Perplexity of the model {model} on {size} of the data set {data} is: {PP}"
          .format(model=args.model, size=sizestr, data=args.datafile, PP=PP))

def handle_args():
    if(args.training):
        train()
    else:
        test()

if __name__=="__main__":
    handle_args()