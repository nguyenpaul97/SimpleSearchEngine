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

# we need the posting.txt final.txt  
#read line by line 

    def final_search_file(finalMerge, bookkeeping, list_word : 'list') -> list:
        data= []
        lst = [] # book keeping
        documents = []
        with open(bookkeeping, "r") as final_m:
            data = final_m.read()
            # add this to a list of pookkeeping
            for i in data:
                lst.extend(i)
        final_marg = open(finalMerge,"r")
        for m in list_word:
            # m is the word
            finalMerge.seek(0)
            first_char = m[0]
            if first_char in lst:
                ind = lst.index(first_char)
                start = lst[ind+1]
                end = lst[ind+2]
            chunk = end - start
            finalMerge.seek(start)
            c = finalMerge.read(chunk)
            while True:
                line = c.readline()
                if line == "":
                    break
                d = eval(line)
                key = list(d.keys())[0]
                if key == m:
                    documents.append(d.values())
                    break

        return documents
if __name__ == "__main__":
    searcher = search()
    qList = searcher.readSearchQuery()
    print(qList)

