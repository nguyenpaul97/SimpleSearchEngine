import os
import os.path
from pathlib import Path
import json
from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request
import string  
import sys
import operator
import re
from urllib.parse import urlparse
from simhash import Simhash, SimhashIndex
import binascii
from bitarray import bitarray
import indexer

# need to remove the stop words and add stemmer
#Anyone know a good liberary to use stemmer

def tokenizer(text : "str") -> list:
    data = [] 
    data = re.split('[^a-z]+',text.lower())
    data = list(filter(None, data))
    return data
def computeWordFrequencies(lst : list ) -> dict:
    d = dict()
    for token in lst:
        if token in d:
            d[token] += 1 
        else:
            d[token] = 1
    
    return d


list_paths = []
def add_paths(d : 'obj') -> list:
    for x in d.iterdir():
        if x.is_file():
           list_paths.append(x)
        elif x.is_dir():
           add_paths(x)

def exact_dup(dic_map : dict) -> list:
    dup_list = []
    for k in dic_map:
       lst = dic_map[k]
       if len(lst) > 1:
           #print(k,lst)
           dup_list.append(lst)
    """ for i in dup_list:
        print(i) """
    return dup_list



def check_sum() -> list:
    lst = []
    dic_memory = dict()  # -->  (url, total)
    for x in list_paths:
        if x == None:
            continue
        else:    
            with open(x,"rb") as f:
                d = json.load(f)
                url =d["url"]
            #print(url)
            content = d["content"]
            soup = bs.BeautifulSoup(content,'lxml')
            title =""
            if (soup.title is not None and soup.title.string is not None):     
                title = soup.title.string.strip()
            newContent = ""
            for para in soup.find_all('p'):
                newContent += str(para.text)
            newContent = title + newContent
            lst = tokenizer(newContent)
            url_list = []
            total = 0
            for token in lst:
                for t in token:
                    total += ord(t)
            url_list.append(url) 
            if total in dic_memory:
                dic_memory[total].extend(url_list)
            else:
                
                dic_memory[total] = url_list       
        
            #s = bytes.fromhex(word)
    exact_list = []
    exact_list = exact_dup(dic_memory)  
    return exact_list    
            

#https://pypi.org/project/bitarray/
#https://stackoverflow.com/questions/37016946/remove-b-character-do-in-front-of-a-string-literal-in-python-3
def sim_hash():
    return_dic = dict() # --> (hash_value, url)
    for x in list_paths:
        if x == None:
            continue
        else:    
            with open(x,"rb") as f:
                d = json.load(f)
                url =d["url"]
            content1 = d["content"]
            soup = bs.BeautifulSoup(content1,'lxml')
            title =""
            if (soup.title is not None and soup.title.string is not None):     
                title = soup.title.string.strip()
            newContent = ""
            for para in soup.find_all('p'):
                newContent += str(para.text)
            newContent = title + newContent
            lst = tokenizer(newContent)
        
        
        
            # compute freq
            freq_dic = dict()
            freq_dic = computeWordFrequencies(lst)
            lst = set(lst)
            another_dic = dict() # word, total in binary 
            # word , count
            total = 0
            for token in lst:
                byte_re = 0
                for letter in token:
                    total += ord(letter)
                byte_re = turn_byte(total)
                another_dic[token] = byte_re
            
            for i in range(0,8):
                value = 0
                vect_list = []
                for token in another_dic:
                    if int(another_dic[token][i]) == 1:
                        value += int(another_dic[token][i])*freq_dic[token]
                    else:
                        value -= int(another_dic[token][i])+freq_dic[token]
                    vect_list.append(value)
            
            hash_total = ''
            for i in vect_list:                    
                if int(i) < 0:
                    hash_total += str(0)
                else:
                    hash_total += str(1)
            hash_byte = turn_byte(int(hash_total))
                    #turn the total to binary
                    # than turn them into hashValue
            url_list = []        
            url_list.append(url) 
            if hash_byte in return_dic:
                return_dic[hash_byte].extend(url_list)
            else:
                
                return_dic[hash_byte] = url_list
    return return_dic
                #[word][]
            # create v formed by suming
#type ['1', '1', '0', '0', '0', '0', 
#  = dict()
            
    #return mainDic
def hash_value(dict :dict, freq : dict) -> int:
    
    for i in range(0,8):
        value = 0
        for word in dict:
            #print(dict[word][i],"-->",freq[word])
            value += int(dict[word][i]) * int(freq[word])
       
def turn_byte(word_value)->'byte':
    
    x = word_value 
    x = '{0:08b}'.format(x)
    return x
      
def find_nearly_dup(near : dict) -> list:
    another_dic = dict()
    for b in near:
        if len(near[b]) == 1:
            another_dic[b] = near[b]
    another_dic.keys()

    listofTuples = sorted(another_dic.items() ,  key=lambda x: len (x[0] ) )
    
    lst = []
    counter = 0
    for i in listofTuples:
        if counter == (len(listofTuples)/100) * 10:
            break
        counter += 1
        lst.append(i[1])
    """ for i in lst:
        print(i) """
    return lst


""" 
run each seperatly, first --> the exact_dup, than once done, run the 
nearly dup. than when both are done, add those 2 diffrent list into index_builder parameter and
use this logic in it
if u in exact_duplist:
    url = u
    # add the list to the nearly_duplicate since we dont want any of those links
    # the list is like this [[ , , ],[],[]]
    near_dup.append(exact_dup)
    remove that  list completely from exact_duplist completly
    exactDup.remove()
elif url not in list_dont_want:
    ... go on 
else:
    continue 
"""

if __name__ == "__main__":
    # 1 - add the folder path here
    p = Path('./DEV')

    # get a list of path
    add_paths(p)

    # 2 - run this first to get the exact dup list
    #exact_list = []
    exact_list = check_sum()

    # 3 - run this last to get 10 percent of nearly duplicates
    #sim_dic = dict()
    #near_dup_list = list
    sim_dic = sim_hash()
    near_dup_list = find_nearly_dup(sim_dic)


    # 4 - run the index builder with 2 additional parameter index_b(.., exact_list, near_dup_list)
    indexer.run_indexer(exact_list, near_dup_list)