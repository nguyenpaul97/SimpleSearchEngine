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
import string
from eventlet.timeout import Timeout

INDEX_SIZE = 10

class Indexer:

    def __init__(self):
        # Posting structure: {token: {doc index #: [tf, importance of token]
        self.posting_dict = dict()
        self.doc_num = 0  # document numbering or N
        self.fileId = 1

        # https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = PorterStemmer()

        # for M1 report
        self.doc_count = 0
        self.unique_count = 0

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
                            self.parse_html(self.doc_num, data['content'])
                    self.doc_num += 1
                    if self.doc_num % INDEX_SIZE == 0:
                        self.writeIndexToFile()
                        self.fileId += 1
            self.writeIndexToFile()
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
        json = js.dumps(self.posting_dict, ensure_ascii=False, indent=4)
        if not os.path.exists("./FileOutput"):
            os.mkdir("./FileOutput")
        f = open("./FileOutput/dict" + str(self.fileId) + ".json", "w+")
        f.write(json)
        f.close()
        self.posting_dict = dict()


    def mergeIndexFiles(self):
        pass


    def parse_html(self, doc_index, content):
        soup = BeautifulSoup(content, "lxml")
        #print(doc_index)
        for line in soup.find_all(["h1", "h2", "h3", "strong", "b"]):
            text = line.get_text()
            token_list = self.tokenizer.tokenize(text)
            #token_list = self.tokenize(text)
            for token in token_list:
                self.index_token(token, doc_index, 2)

        all_text = self.find_all_text(soup)
        for words in all_text:
            tokens = self.tokenizer.tokenize(words)
            #tokens = self.tokenize(words)
            for token in tokens:
                self.index_token(token, doc_index, 0)

        #print(self.posting_dict)

        self.doc_count += 1


    # CHANGE THIS FORMAT, TOO CLOSE TO ANDREWS
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

    def tokenize(self, text_list):
        tokenList = []
        for line in text_list:
            line = re.sub(r'[^\x00-\x7f]', r' ', line).lower()
            line = line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            tokenList.extend(line.split())
        return tokenList



if __name__ == "__main__":
    #indexer = Indexer()
    #indexer.indexer_main()

    with open("./FileOutput/mergedict.json", "w+") as mergeFile:
        mergeFile.write('{ ')
        not_end = True
        list_of_keys = []
        f1 = open("./FileOutput/dict1.json", "r")
        f2 = open("./FileOutput/dict2.json", "r")
        while not_end:
            word_f1 = ''
            word_f2 = ''
            line_f1 = f1.readline()
            line_f2 = f2.readline()
            while True:
            #for line in f1:
                part = line_f1.strip()
                if word_f1 == '' and part == '{':
                    line_f1 = f1.readline()
                    continue
                if part == '}}':
                    not_end = False
                word_f1 = word_f1 + part
                if part == '},':
                    print("END")
                    word_f1 = '{'+word_f1[:-1]+'}'
                    #line_f1 = f1.readline()
                    break
                line_f1 = f1.readline()
            word_f1 = eval(word_f1)

            while True:
            #for line in f2:
                part1 = line_f2.strip()
                if word_f2 == '' and part1 == '{':
                    line_f2 = f2.readline()
                    continue
                if part1 == '}}':
                    not_end = False
                word_f2 = word_f2 + part1
                if part1 == '},':
                    print("END")
                    word_f2 = '{'+word_f2[:-1]+'}'
                    #line_f2 = f2.readline()
                    break
                line_f2 = f2.readline()
            word_f2 = eval(word_f2)
            print(word_f1)
            print(word_f2)
            if list(word_f1.keys())[0] == list(word_f2.keys())[0]:
                print("wye")
                word_f1[next(iter(word_f1))].update(word_f2[next(iter(word_f2))])
                print(word_f1)
                mergeFile.write(str(word_f1)[1:-1]+", ")
            if input('dfsd') == 'a':
                mergeFile.close()
            else:
                continue
        mergeFile.write('}')
