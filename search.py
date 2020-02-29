from nltk.stem import PorterStemmer
import os
import json as js
import re

class search:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def readSearchQuery(self):
        query = input("search query : ")

        queryList = []
        for q in self.tokenizer(query):
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
        documents = []  #
        str1 = ""
        with open(bookkeeping, "r") as f:
            str1 = f.read()
       
        data = str1.split(" ")
        data = list(filter(None, data))
        final_marg = open(finalMerge,"r")

# m is each word in query 
        for m in list_word:
            final_marg.seek(0)
            first_char = m[0]
            # lst has the bookKeeping list
            
            
            index = data.index(first_char)
            start =  data[index+1]
            end = data[index+2]

            chunk = int(end) - int(start)

            
            final_marg.seek(int(start))
            # c has [{},{},...]
            c = final_marg.read(chunk)
            
            documents.extend(c.split('\n'))
            documents = list(filter(None, documents))
            #print(len(documents))
            """ for i in documents:
                print(i) """

        return documents
            
if __name__ == "__main__":
    searcher = search()
    qList = searcher.readSearchQuery()
    #qList = ["a","b"]
    print(qList)
    searcher.final_search_file("./FileOutput/finalmerged.txt", "./FileOutput/bookkeeping.txt",qList)





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