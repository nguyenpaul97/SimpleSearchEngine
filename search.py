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
        for q in self.tokenizer.tokenize(query):
            queryList.append(self.stemmer.stem(q.lower()))

        return queryList

    def tokenizer(self, text: "str") -> list:
        data = []
        data = re.split('[^a-z0-9]+', text.lower())
        data = list(filter(None, data))
        return data