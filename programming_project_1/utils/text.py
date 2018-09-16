import sys
def TokenSeqFromFile(path:str,count:int,bufferSize=100000):
    actualCount=0
    with open(path,'r') as f:
        while actualCount < count:
            buf=f.read(bufferSize)  # use buffered reading to avoid going out of memory for very large file
            if len(buf)==0:
                break
            while buf[-1]!=" ":
                c=f.read(1)
                if c:
                    buf+=c
                else:
                    break
            bufSeq=TokenSeqFromText(buf)
            for token in bufSeq:
                yield token  # creating an generator that keep providing the next token until enough or EOF
                actualCount+=1
                if actualCount >= count:
                    break


def TokenSeqFromText(text:str)->list:  # reserved for preprocessing texts (if needed in the future)
    return text.split()

def GenWordList(dictPath:str)->list:
    wordList = []
    with open(dictPath, 'r') as f:
        while True:
            line = f.readline()[:-1]
            if not line:
                break
            wordList.append(line)
    return wordList