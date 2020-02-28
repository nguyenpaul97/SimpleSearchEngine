import os
import json as js
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import math
import numpy as np
from collections import OrderedDict
import re
from eventlet.timeout import Timeout


INDEX_SIZE = 100

class Indexer:

    def __init__(self):
        # Posting structure: {token: {doc index #: [tf, importance of token]
        self.posting_dict = dict()
        self.url_dict = dict()
        self.doc_num = 0  # document numbering or N
        self.fileId = 1

        # https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = PorterStemmer()

        # for M1 report
        self.doc_count = 0
        self.unique_count = set()
    def readSearchQuery(self):
        query = input("search query : ")
    
        queryList = []
        for q in self.tokenizer.tokenize(query):
            queryList.append(self.stemmer.stem(q.lower()))

        return queryList
    def indexer_main(self):
        if os.path.exists('DEV'):
            for path in os.listdir('DEV'):
                for json_file in os.listdir('DEV/'+path):
                    # load json
                    json_path = 'DEV/'+path+'/'+json_file
                    print(json_path)
                    with open(json_path, 'r') as jfile:
                        with Timeout(5, False):
                            data = js.load(jfile)
                            url = data['url']
                            self.url_dict[self.doc_num] = url
                            self.parse_html(self.doc_num, data['content'])
                    self.doc_num += 1
                    if self.doc_num % INDEX_SIZE == 0:
                        self.writeIndexToFile()
                        self.fileId += 1
            self.writeIndexToFile()
            print(self.doc_count)
            print(self.doc_num)
            print(len(self.unique_count))
            with open("./FileOutput/urls.txt", "w") as url_txt:
                url_txt.write(str(self.url_dict))
            with open("./FileOutput/report.txt", "w+") as f:
                f.write("number of documents: "+str(self.doc_num)+"\n")
                f.write("number of unique tokens: " + str(len(self.unique_count)))

        else:
            print("Please put DEV folder in the folder with this file.")



    def writeIndexToFile(self):
        print("writing index to file", self.fileId)
        # for token in self.posting_dict:
        #     #print(token)
        #     # print(self.posting_dict[token][1])
        #     # print(self.posting_dict[token][2])
        #     df = len(self.posting_dict[token])
        #     for doc in self.posting_dict[token]:
        #         tf = self.posting_dict[token][doc][0]
        #         # Calculate tf-idf for that term inside of the document
        #         self.posting_dict[token][doc][2] = tf * math.log10(self.doc_count / df)


        self.posting_dict = OrderedDict(sorted(self.posting_dict.items()))
        #json = js.dumps(self.posting_dict)
        if not os.path.exists("./FileOutput"):
            os.mkdir("./FileOutput")
        f = open("./FileOutput/dict" + str(self.fileId) + ".txt", "w+")
        for key, value in self.posting_dict.items():
            f.write('{"%s":%s}\n' % (key,value))
        #f.write(json)
        f.close()
        self.posting_dict = dict()


    def parse_html(self, doc_index, content):
        soup = BeautifulSoup(content, "lxml")
        #print(doc_index)
        for line in soup.find_all(["h1", "h2", "h3", "strong", "b", "title"]):
            text = line.get_text()
            text = self.removeNonAscii(text)
            token_list = tokenizer(text)
            #token_list = self.tokenizer.tokenize(text)
            for token in token_list:
                self.index_token(token, doc_index, 2)

        all_text = self.find_all_text(soup)
        for words in all_text:
            words = self.removeNonAscii(words)
            tokens = tokenizer(words)
            #tokens = self.tokenizer.tokenize(words)
            for token in tokens:
                self.index_token(token, doc_index, 0)

        #print(self.posting_dict)

        self.doc_count += 1


    def index_token(self, token, doc_index, importance):
        stemmed = self.stemmer.stem(token.lower())
        if not self.check_word(stemmed):
            return
        if stemmed in self.posting_dict:
            if doc_index in self.posting_dict[stemmed]:
                self.posting_dict[stemmed][doc_index][0] += 1
                self.posting_dict[stemmed][doc_index][1] += importance
            else:
                self.posting_dict[stemmed][doc_index] = [1, importance, 0]
        else: # list contains: frequency, weight, tf-idf score
            self.posting_dict[stemmed] = {doc_index: [1, importance, 0]}
        if stemmed not in self.unique_count:
            self.unique_count.add(stemmed)


    '''
    find_all_text has a time complexity of O(N) because we are going through all the text.
    '''
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?noredirect=1&lq=1
    def find_all_text(self, soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(self.filter_tags, texts)
        return [t.strip() for t in visible_texts if t.strip() != '']

    '''
    Time complexity of filter_tags is O(1) because in evaluation in set only takes O(1) time.
    '''
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?noredirect=1&lq=1
    def filter_tags(self, element):
        if element.parent.name in {'style', 'script', '[document]', 'head', 'title', 'meta', 'noscript', 'h1', 'h2', 'h3', 'strong', 'b'}:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def check_word(self, word):
        if not word.isdigit():
            if len(word) == 1:
                return False
        return True

    # https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
    def removeNonAscii(self, s):
        return "".join(i for i in s if ord(i) < 128)

def merge(file1, file2, writefile):
    with open(writefile, "w") as mergeFile:
        f1 = open(file1, "r")
        f2 = open(file2, "r")
        try:
            merged_list = []
            break_file = 0
            l1 = []
            l2 = []
            while True:
                if len(l1) == 0:
                    line_f1 = f1.readline()
                    if line_f1 == "":
                        print("break line_f1")
                        break_file = 0
                        if len(l2) != 0:
                            mergeFile.write(str(l2[0]) + "\n")
                            #merged_list.append(l2[0])
                        break
                    l1.append(eval(line_f1.strip()))
                if len(l2) == 0:
                    line_f2 = f2.readline()
                    if line_f2 == "":
                        print("break line_f2")
                        break_file = 1
                        if len(l1) != 0:
                            mergeFile.write(str(l1[0]) + "\n")
                            #merged_list.append(l1[0])
                        break
                    l2.append(eval(line_f2.strip()))

                #print(len(l1))
                #print(len(l2))

                if list(l1[0].keys())[0] == list(l2[0].keys())[0]:
                    l1[0][next(iter(l1[0]))].update(l2[0][next(iter(l2[0]))])
                    #merged_list.append(l1[0])
                    mergeFile.write(str(l1[0]) + "\n")
                    #print(l1[0].update(l2[0]))
                    l1.pop(0)
                    l2.pop(0)
                elif list(l1[0].keys())[0] < list(l2[0].keys())[0]:
                    #merged_list.append(l1[0])
                    mergeFile.write(str(l1[0]) + "\n")
                    l1.pop(0)
                elif list(l1[0].keys())[0] > list(l2[0].keys())[0]:
                    #merged_list.append(l2[0])
                    mergeFile.write(str(l2[0]) + "\n")
                    l2.pop(0)
            if break_file == 0:
                while True:
                    line_f2 = f2.readline()
                    if line_f2 == "":
                        break
                    #merged_list.append((eval(line_f2.strip())))
                    #print("write f2")
                    mergeFile.write(str(eval(line_f2.strip())) + "\n")
            elif break_file == 1:
                while True:
                    line_f1 = f1.readline()
                    if line_f1 == "":
                        break
                    #merged_list.append((eval(line_f1.strip())))
                    #print("write f1")
                    mergeFile.write(str(eval(line_f1.strip())) + "\n")
            f1.close()
            f2.close()
            #print(len(merged_list))
            #for i in merged_list:
            #    print(i)
            #    mergeFile.write(str(i) + "\n")
        except EOFError:
            print("end of file")
            f1.close()
            f2.close()
            #pass

            
def tokenizer(text : "str") -> list:
    data = [] 
    data = re.split('[^a-z0-9]+',text.lower())
    data = list(filter(None, data))
    return data

if __name__ == "__main__":
    indexer = Indexer()
    indexer.indexer_main()

    #dict1 = open('./FileOutput/dict1.txt')
    #while True:
    #    line_dict1 = dict1.readline()
    #    print(eval(line_dict1))

    #merge("./FileOutput/dict1.txt", "./FileOutput/dict2.txt", "./FileOutput/mergedict.txt")
    #merge("./FileOutput/mergedict.txt", "./FileOutput/dict3.txt", "./FileOutput/mergedict1.txt")
    #merge("./FileOutput/mergedict1.txt", "./FileOutput/dict4.txt", "./FileOutput/mergedict2.txt")
    #merge("./FileOutput/mergedict2.txt", "./FileOutput/dict5.txt", "./FileOutput/mergedict3.txt")
    #merge("./FileOutput/mergedict3.txt", "./FileOutput/dict6.txt", "./FileOutput/finalmerged.txt")


    # with open("./FileOutput/mergedict.txt", "w+") as mergeFile:
    #     f1 = open("./FileOutput/dict1.txt", "r")
    #     f2 = open("./FileOutput/dict2.txt", "r")
    #     try:
    #         merged_list = []
    #         break_file = 0
    #         while True:
    #             l1 = []
    #             l2 = []
    #             if len(l1) == 0:
    #                 line_f1 = f1.readline()
    #                 if line_f1 == "":
    #                     print("break line_f1")
    #                     break_file = 0
    #                     break
    #                 l1.append(eval(line_f1.strip()))
    #             if len(l2) == 0:
    #                 line_f2 = f2.readline()
    #                 if line_f2 == "":
    #                     print("break line_f2")
    #                     break_file = 1
    #                     break
    #                 l2.append(eval(line_f2.strip()))
    #
    #             # print(l1)
    #             # print(l2)
    #
    #             if list(l1[0].keys())[0] == list(l2[0].keys())[0]:
    #                 l1[0][next(iter(l1[0]))].update(l2[0][next(iter(l2[0]))])
    #                 merged_list.append(l1[0])
    #                 #merged_list.append(l1[0].update(l2[0]))
    #                 #print(l1[0].update(l2[0]))
    #                 l1.pop(0)
    #                 l2.pop(0)
    #             elif list(l1[0].keys())[0] < list(l2[0].keys())[0]:
    #                 merged_list.append(l1[0])
    #                 l1.pop(0)
    #             elif list(l1[0].keys())[0] > list(l2[0].keys())[0]:
    #                 merged_list.append(l2[0])
    #                 l2.pop(0)
    #         if break_file == 0:
    #             while True:
    #                 line_f2 = f2.readline()
    #                 if line_f2 == "":
    #                     break
    #                 merged_list.append((eval(line_f2.strip())))
    #         elif break_file == 1:
    #             while True:
    #                 line_f1 = f1.readline()
    #                 if line_f1 == "":
    #                     break
    #                 merged_list.append((eval(line_f1.strip())))
    #         for i in merged_list:
    #             print(i)
    #             mergeFile.write(str(i) + "\n")
    #     except EOFError:
    #         print("end of file")
    #         pass
