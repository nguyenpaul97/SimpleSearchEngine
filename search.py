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



def load_to_memory():
    pass
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
    qList = search.readSearchQuery()
    print(qList)

