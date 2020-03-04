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
#     def final_search_file(self,finalMerge, bookkeeping, list_word ) -> list:        
#         data = []# book keeping
#         str1 = ""
#         c = []
#         with open(bookkeeping, "r") as f:
#             str1 = f.read() 
#         data = str1.split(" ")
#         data = list(filter(None, data))   
#         with open(finalMerge,"r") as marg_file:
#                     lines = marg_file.readlines()  
# # m is each word in query
#         try:
#             for m in list_word:           
#                 first_char = m[0]
#                 # lst has the bookKeeping list
#                 index = data.index(first_char)
#                 start =  data[index+1]
#                 end = data[index+2]
#                 start_index = int(start)
#                 end_index = int(end)            
#                 c.extend(lines[start_index:end_index:1])
#         except:
#             pass
#         return c
#         """ 
#         come up with a better serach algorithem
#         """
    # def match_exact_query(self,sameCharacterWordList, qList):
    #     i = 0
    #     docIDList = []
    #     for s in sameCharacterWordList:            
    #         token = list(eval(s).keys())[0]

    def final_search_file(self, finalMerge, bookkeeping, list_word : 'list') -> list:
        data= []
        lst = [] # book keeping
        documents = []
        with open(bookkeeping, "r") as final_m:
            data = final_m.read()
            # add this to a list of pookkeeping
            lst = data.split()
        #print(lst)
        final_marg = open(finalMerge,"r")
        for m in list_word:
            # m is the word
            final_marg.seek(0)
            first_char = m[0]
            if first_char in lst:
                #print(first_char)
                ind = lst.index(first_char)
                #print(ind)
                start = int(lst[ind+1])
                end = int(lst[ind+2])
            print("Start", start)
            print("End", end)
            #chunk = int(end.strip()) - int(start.strip())
            final_marg.seek(start)
            count = start
            
            while count < end:
                line = final_marg.readline()
                if line == "":
                    break
                #print(line)
                count += len(line)
                d = eval(line)
                key = list(d.keys())[0]
                
                if key == m:
                    print(key)
                    docIDDict = d[key]
                    for docID in docIDDict:
                        documents.append(docID)
                    
                    break
        
        return documents
    def match_exact_word(self, documents, qList):
        d = documents
        if (len(qList) > 1):
            d = duplicates_helper(documents)
            print("done with duplicate")
        return d
def findURL(docIDResults, URLFile, limit):
        read_file = open(URLFile, "r")
        dictionary = read_file.read()
        i = 0
        for docID in docIDResults:
            print(eval(dictionary)[docID])
            if (i >= 4):
                break
            i += 1  
        #print(documents)
def duplicates_helper(docIDList):
    print("in duplicate")
    duplicates = []
    for item in docIDList:
        if docIDList.count(item) > 1:
            duplicates.append(item)
    return set(duplicates)
if __name__ == "__main__":
    searcher = search()
    qList = searcher.readSearchQuery()
    print(qList)
    #query = ["cristina", "lope"]

    a = searcher.final_search_file("./FileOutput/finalmerged.txt", "./FileOutput/bookkeeping.txt", qList)
    #f = open("./FileOutput/finalmerged.txt", "r")
    

    d = list(searcher.match_exact_word(a, qList))
    findURL(d, "./FileOutput/urls.txt", 5)
    # while True and i < 5:
    #     line = f.readline()
    #     increment = len(line) + 1
        
    #     print(count)
    #     f.seek(count)
    #     print(f.readline())
    #     print("--------")
    #     count += increment
        
    #     i += 1
   
