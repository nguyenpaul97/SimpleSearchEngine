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
