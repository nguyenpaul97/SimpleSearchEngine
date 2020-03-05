from nltk.stem import PorterStemmer
from bisect import bisect_left
import time
import os
import json as js
import time
import re
import math
N = 55000
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
class search:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def readSearchQuery(self):
        query = input("search query : ")
        query = set(self.tokenizer(query)) - set(stop_words)
        queryList = []
        for q in query:
            queryList.append(self.stemmer.stem(q.lower()))

        return queryList

    def tokenizer(self, text: "str") -> list:
        text_non_ascii = self.removeNonAscii(text)
        data = re.split('[^a-z0-9]+', text_non_ascii.lower())
        data = list(filter(None, data))
        return data


    # https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
    def removeNonAscii(self, s):
        return "".join(i for i in s if ord(i) < 128)

    # This function returns all the tokens with the same first character as the query words
   # return a tuple: documents as a list of string, each string contains one line (token + postings) in the final merged file
   # keyList: list of the tokens
    def final_search_file(self, finalMerge, bookkeeping, list_word : 'list') -> list:
        startTime = time.time()
        print("in final search")
        data= []
        lst = [] # book keeping
        documents = []
        keyList = []
        with open(bookkeeping, "r") as final_m:
            data = final_m.read()
            # add this to a list of pookkeeping
            lst = data.split()
        #print(lst)
        final_marg = open(finalMerge,"r")
        list_word.sort()
        for m in list_word:
            # m is the word
            final_marg.seek(0)
            first_char = m[0]
            start = 0
            end = 0
            if first_char in lst:
                #print(first_char)
                ind = lst.index(first_char)
                #print(ind)
                start = int(lst[ind+1])
                end = int(lst[ind+2])
            
            
            final_marg.seek(start)
            count = start
            sizeWord = len(m)
            
            
            while count < end:
                line = final_marg.readline()
                if line == "":
                    break

                # print(line)
                count += len(line)
                documents.append(line.strip())
                # l = eval(line)
            
                # key = list(l.keys())[0]
                
                
                keyList.append(line[2:sizeWord+2])
                
        print("done with final search", time.time() - startTime, "\n")
        return documents, keyList
    
    def match_exact_word(self, documents, keyList, qList):
        #print(keyList)
        documentIDList = []
        query_word_posting = []
        for q in qList:
            
            i = BinSearch(keyList, q)
            #i = keyList.index(q)
            if (i > 1):
                query_word_posting.append(documents[i])
                start = time.time()
                l = eval(documents[i])
                #print(l)
                key = list(l.keys())[0]
                documentIDList.extend(list(l[key].keys()))
                #key = 
                #print(eval)
        tf_idf(query_word_posting)
        if (len(qList) > 1):
            
            
            return duplicates_helper(documentIDList)
        return documentIDList

# this function return a list of token_document_dict for all the query words
# each query word has a vector (tf-idf score for doc1, tfidf score score for doc 2, etc)
# this vector is token_document_dict {doc1: tf-idf score, doc2: tf-idf score, ...}

def tf_idf(query_word_posting):
    for q in query_word_posting:
        token_document_dict = {}
        q = q.split()
            
        i = 1
        # for z in q:
        #     print(z)
        
        doc_id_index = 1
        tf_index = 2
        df = (len(q) - 1)//3
        
        
        while doc_id_index < len(q):
            tf = int(q[tf_index].replace("[", "").replace(",", ""))
            
            token_document_dict[q[doc_id_index]] = (1+math.log(tf))*math.log(N/df)

            doc_id_index+=3
            tf_index += 3
            df += 1

        #print(token_document_dict[0:10])
        print("\n*******  ",q[0], "appears in ", df, "documents\n")
    
def BinSearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1
def findURL(docIDResults, URLFile, limit):
        print("in find URL")
        read_file = open(URLFile, "r")
        dictionary = read_file.read()
        i = 0
        URL = []
        start = time.time()
        dictionaryList = dictionary.split()
        i = 0
        
        
        for d in docIDResults:
            URL.append(dictionaryList[d*2+1])
        
        
        print("End find URL", time.time() - start, "\n")
        return URL

def duplicates_helper(docIDList):
    #print(docIDList)
    print("in duplicate")
    start = time.time()
    duplicates = set()
    for item in docIDList:
        if docIDList.count(item) > 1:
            duplicates.add(item)
    print("done with duplicate", time.time() - start, "\n")
    return duplicates
if __name__ == "__main__":
    
    searcher = search()
    while True:
        qList = searcher.readSearchQuery()
    
        print("\n")
        starttime = time.time()
        a = searcher.final_search_file("./FileOutput/finalmerged.txt", "./FileOutput/bookkeeping.txt", qList)
        
        d = list(searcher.match_exact_word(a[0], a[1], qList))
        URL = findURL(d, "./FileOutput/urls.txt", 5)
        
        
        endtime = time.time()-starttime
        print("------------\nTotal = ", endtime)

        i = 0
        print("\n************  SEARCH RESULTS   ************* \n\n")
        for u in URL:
            if (i < 5):
                print(u, "\n")
            i+=1
        