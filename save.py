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
                end = int(lst[ind+3])
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
                    documents.append(d.values())
                    break

        return documents

def makeBookkeeping(finalMerge, bk):
    newCharacter = False
    with open(bk, "w") as bookKeeping:
        read_file = open(finalMerge, "r")
        count = 0
        bookKeeping.write("# ")
        bookKeeping.close()
  
    with open(bk, "a+") as bookKeeping:
        while True:
            line = read_file.readline()
            increment = len(line)
            
            tokenDict = eval(line.strip())
            token = list(tokenDict.keys())[0]
            #print(token.isdigit())
            print(token[0].isdigit())
            
            if (token[0].isdigit() == False):
                
                bookKeeping.write(str(count) + " ")
                bookKeeping.write(token[0] + " " + str(count) + " ")
                count += increment
                break

            count += increment

        newCharacter = False
        character = token[0]
        while True:
            line = read_file.readline()
            
            
            if (line == ""):
                
                break
            increment = len(line)
            tokenDict = eval(line.strip())
            token = list(tokenDict.keys())[0]
            print(character)
            
            if (token[0] != character):
                newCharacter = True
            else:
                newCharacter = False

            
                
            if (newCharacter == True):
                
                character = token[0]
                bookKeeping.write(token[0] + " " + str(count) + " ")
            count += increment
                
            
    read_file.close()
