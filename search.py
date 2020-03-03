from nltk.stem import PorterStemmer

import os
import json as js
import re
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
class search:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def readSearchQuery(self):
        

        query = input("search query : ")
        
        query = set(self.tokenizer(query)) - set(stop_words)
        print(query)
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

    
    #it returns a chunk of list from first and second word and ...
    def final_search_file(self,finalMerge, bookkeeping, list_word ) -> list:        
        data = []# book keeping
        str1 = ""
        c = []
        with open(bookkeeping, "r") as f:
            str1 = f.read()
       
        data = str1.split(" ")
        data = list(filter(None, data))     
# m is each word in query
        try:
            for m in list_word:           
                first_char = m[0]
                # lst has the bookKeeping list
                index = data.index(first_char)
                start =  data[index+1]
                end = data[index+2]
                start_index = int(start)
                end_index = int(end)            

                with open(finalMerge,"r") as marg_file:
                    lines = marg_file.readlines()
                c.extend(lines[start_index:end_index:1])



                """ j = 0
                for i in c:
                    if j == 10:
                        break;
                    else:
                        print(i)
                    j += 1
                print(len(c)) """
        except:
            pass
        return c
    def match_exact_query(self,sameCharacterWordList, qList):
        i = 0
        docIDList = []
        for s in sameCharacterWordList:
            
            token = list(eval(s).keys())[0]
            
            
            for qToken in qList:
                
                if (token == qToken):
                    posting = list(eval(s).values())
                    #print("match=", token)
                    
                    
                    for p in posting:
                        #print(type(p))
                        docIDList.extend(list(p.keys()))
        #print(docIDList)
        if (len(qList) > 1):
            #print("in the if condition query > 1")
            docIDList = list(duplicate_helper(docIDList))
            #print("length of docIDList", len(docIDList))
            # for i in range(len(docIDList)):
            
            #     print(docIDList[i])
        

            
            
        return docIDList
        
def findURL(docIDResults, URLFile, limit):
        read_file = open(URLFile, "r")
        dictionary = read_file.read()
        i = 0
        for docID in docIDResults:
            print(eval(dictionary)[docID])
            if (i >= 4):
                break
            i += 1
                
def duplicate_helper(docIDList):
    docIDResults = []
    for item in docIDList:
        if docIDList.count(item) > 1:
            docIDResults.append(item)
    return set(docIDResults)

if __name__ == "__main__":

    searcher = search()
    qList = searcher.readSearchQuery()

    
    print(qList)
    sameCharacterWordList = searcher.final_search_file("./FileOutput/finalmerged.txt", "./FileOutput/bookkeeping.txt",qList)
    docIDResults = searcher.match_exact_query(sameCharacterWordList, qList)
    findURL(docIDResults, "./FileOutput/urls.txt", 5)



""" while True:
                line = c.readline()
                if line == "":
                    break
                d = eval(line)
                key = list(d.keys())[0]
                if key == m:
                    documents.append(d.values())
                    break

        return documents """
