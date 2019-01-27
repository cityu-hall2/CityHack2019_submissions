
from xml.dom import minidom
import json
import string
import constants as C
import numpy as np
from time import sleep

class word:
    def __init__(self,word,p):
        self.word = word.lower()
        done = True
        while(done):
            done = False
            for p in C.punct:
                if(self.word[-1]==p):
                    self.word = self.word[:-1]
                if(self.word[0]==p):
                    self.word=self.word[1:]
            


        
        self.pos = p;
def getwordlist():
    file = open("inputwords.txt","r")
    end = file.readlines()

    for i in range(len(end)):
        end[i] = end[i].strip()
        end[i] = end[i].split(',')
        
    return end


def caseinputs(inputs,fileaddress):
    wordsonpage = extractwords(fileaddress)
    x = []
    for i in inputs:
        isthere = False
        for ii in wordsonpage:
            if(i[0]==ii.word):
                isthere = True
                break;
        if(isthere==True):
            x.append(1)
        else:
            x.append(0)

    return x
def markedpages():
    print("load page numbers")
    file = open("outputs.txt","r")
    end = file.readlines()

    for i in range(len(end)):
        end[i] = end[i].strip()
        end[i] = end[i].split(',')
        end[i][0] = int(end[i][0])
        end[i][1] = int(end[i][1])
    return end

def pagenums(file,ent):
    print("look up page numbers")
    end = []
    doc=jsonmaker(file)
    for p in doc["pages"]:
        if(len(p["tags"])>0):
            for i in range(len(p["tags"])):
                #print(p["tags"][i])
                try:
                    if(p["tags"][i]["entityType"] == ent):
                        end.append(p["pageId"])
                except:
                    print("noname");
    return end
def listofallwords(file,datatype):
    print("search for possible word keys")
    tosearch = []
    for i in range(1,60):
        if i not in C.missingfolders:
            r = pagenums(file+"/"+str(i)+"/"+str(i)+"_tagged.json",datatype)
            tosearch.append((i,r))


    dict = {}
    common = mostcommonwords()
    for i in ["-"," ","_"]: #bad strings
        common.append(i)
    for i in tosearch:
        for ii in i[1]:
            #print(file+"/"+str(i[0])+"/hocr/"+str(i[0])+"-"+str(ii)+".hocr")
            words = extractwords(file+"/"+str(i[0])+"/hocr/"+str(i[0])+"-"+str(ii)+".hocr")
        
            for w in words:
                if w.word in dict.keys():
                    dict[w.word]+=1
                else:
                    dict[w.word]=1

    
    toremove = []
    for i in dict.keys():
        if(dict[i]<C.minwordcout):
            toremove.append(i)
        elif(i.isdigit()):
            toremove.append(i)
        elif (i in common):
            toremove.append(i)

    for i in toremove:
        dict.pop(i)

   

    print("removed words:",toremove)
    sleep(1)
    print("key size:",len(dict.keys()))
    sleep(1)

    sorted = []
    for i in dict.keys():
        sorted.append((dict[i],i))
    sorted.sort()



    sfile = open("outputs.txt","w")
    for d in tosearch:
        documentnum = d[0]
        for p in d[1]:
            sfile.write(str(documentnum))
            sfile.write(',')
            sfile.write(str(p))
            sfile.write("\n")

    file = open("inputwords.txt","w")
    for i in sorted:
        try:
            file.write(i[1])
            file.write(',')
            file.write(str(i[0]))
            file.write('\n')
        except:
            print(i,'|')
    

def loaddata(fname):
    end = []
    dend = []
    rend = []

    data = []
    file = open(fname+".txt",'r')
    data = file.readlines()
    for i in range(len(data)-1):
        data[i] = data[i].strip()
        data[i] = data[i].split(',')
        #arr=[]
        for ii in range(1,len(data[i])):
            #dend.append()
            dend.append(int(data[i][ii]))
        #dend.append(tuple(arr))
        rend.append(int(data[i][0]))
    dend=np.array(dend).reshape(int(len(dend)/(len(data[0])-1)),len(data[0])-1)
    end = [dend,rend]
    return end;

def makedata(fname):
    missing=0
    filew = open(fname+".txt",'w')
    words = getwordlist();

    pages = markedpages();
    print("makeing test cases")
    for doc in range(1,60):
        for pp in range(0,500):
            address = 'Training/'+str(doc) + "/hocr/" + str(doc) +"-"+str(pp) + ".hocr"
            try:
                file = open(address)
                file.close()
            except:
                print(doc,pp)
                break;

            x = caseinputs(words,address)
            #if(1 not in x):
                #continue
            realpage = False
            for k in pages:
                if(k[0]==doc & k[1]==pp):
                    realpage = True
                    break
                elif(k[0]>doc):
                    break

            if(realpage==True):
                if(1 not in x):
                    print("constains too hight! removing case")
                    missing+=1
                    sleep(0.1)
                    continue
                else:
                    filew.write("1")
            else:
                filew.write("0")

            for i in x:
                filew.write(',')
                filew.write(str(i))
            filew.write('\n')

    return missing
def mostcommonwords():
    with open ("1-1000.txt", "r") as myfile:
        data=myfile.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()
    return data
def makecsv(arr):
    return ;



def extractwords(location):
    print("extracting words:",location)
    mydoc = minidom.parse(location)
    items = mydoc.getElementsByTagName('span');
    end = []
    for i in items:
        if i.attributes['class'].value == "ocrx_word":
            try:

                w = word(i.firstChild.nodeValue,i.attributes['title'].value)
                end.append(w)
            except:
                #print("missingw")
                continue
    return end;

def jsonmaker(location):
    print(location)
    with open(location) as f:
        data = json.load(f)
    return data
