## Solution to Information Extraction from Annual Report for Accounting Opening Purpose

-----------

#### 1. Overview

Given the dataset by *BNP Paribas*, we used  [*spaCy*](https://spacy.io, "spaCy") , a Industrial-Strength Natural Language Processing Machine Learning Library in Python, to classify different entity types appeared in datasets and make predictions for testing data based on the result of training.

#### 2. Dataset

Dataset are provided by *BNP Paribas* originated from *Singapore Stock Exchange* containing 40 annual reports of corporations worldwide for training and 4 reports for testing on https://github.com/jeffreynghm/CityU-Hackathon-2019](https://github.com/jeffreynghm/CityU-Hackathon-2019). Contents provided for each annual report are also included.

#### 3. Methodology & Walkthrough

Based on the characteristic of <u>Named Entity Recognition</u> Algorithm implemented by *spaCy*, we first transformed .hocr file into .txt file for word-frequency count analysis and for the convenience of extracting the raw for NER training data, where relevant codes are shown below (in Python):

```python
from __future__ import print_function
import os
import re
from lxml import etree, html
path = "../CityU-Hackathon-2019/Training"

for filename in os.listdir(path):
    fw = open("txtResult/result_"+filename+".txt", "w", encoding="utf-8") ##fout
    for f in os.listdir(path+"/"+filename+"/hocr"):
        fw.write(f.split("-",1)[1]+": \n")
        doc = html.parse(path + "/" + filename + "/hocr/" + f)	
        for para in doc.xpath("//*[@class='ocr_par']"):		## regular expression
           for line in para:
              fw.write(re.sub(r'\s+', '\x20', line.text_content()).strip())
           fw.write("\n")
        fw.write("===================================================\n")
    fw.close()
```



SpaCy requires the input of training data to be in an array containing elements with the format of `(sentences,{'tag_type':[start_index,end_index,'tag'],...,[start_index,end_index,'tag']}`. So we extracted correponding sentence and entity type in every page specified by .json file for each document to be fed into the algorithm and figured out the starting and ending index for input, which is realized by the Python codes below:

```Python
from __future__ import print_function
import os
import json
from lxml import etree, html
import re

path = "CityHack/"

for filename in os.listdir(path):
    file = open(path+"/"+filename+"/"+filename+"_tagged.json", "r", encoding='utf-8')
    fw = open("rw/rwdata_"+filename+".txt", "w",encoding='utf-8') ##file output
    decoded = json.load(file)
    for sjson in decoded["pages"]:
        if not sjson["tags"]:
            continue
        else:
            fdata = sjson["tags"]
            fw.write("Page: " + str(sjson["pageId"]))
            fw.write("\n")
            hocr = open(path+"/"+filename+"/hocr/"+filename+"-"+str(sjson["pageId"])+".hocr","r")
            for subjson in fdata:
                transsubjson = subjson
                if "entityType" in transsubjson:
                    fw.write(transsubjson["entityType"]+": ")
                else:
                    fw.write("NO ENTITY TYPE: ")
                p1 = transsubjson["pt0"][1]
                p2 = transsubjson["pt1"][1]
                doc = html.parse(path+"/"+filename+"/hocr/"+filename+"-"+str(sjson["pageId"])+".hocr")
                for line in doc.xpath("//*[@class='ocr_line']"):
                    attribute = line.get("title")
                    yaxis = float(attribute.split(" ",4)[2])
                    if (yaxis>=p1) and (yaxis<=p2):
                        fw.write(re.sub(r'\s+', '\x20', line.text_content()).strip()+" ")
                        fw.write(line.get(""))
                fw.write("\n")
    fw.write("\n\n")
    fw.close()
```



To do the training, we referred codes provided in [spaCy documentation](https://spacy.io/models/) and [NLP Tutorials](https://github.com/Jcharis/Natural-Language-Processing-Tutorials/blob/master/NLP_with_SpaCy/Training%20the%20Named%20Entity%20Recognizer%20in%20SpaCy.ipynb) and  created and trained a blank spaCy model using data extracted for 100 iterations. 

```python
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar

f = open('file.txt','r',encoding="utf-8")
TRAIN_DATA = eval(f.read())

TRAIN_DATA2 = [];
for data in TRAIN_DATA:
  if data[1]['entities'][0][2] != 'Currency' :
    TRAIN_DATA2.append(data)
print(TRAIN_DATA2)
TRAIN_DATA = TRAIN_DATA2
nlp1 = spacy.load('en')


model = None
output_dir=Path("abc")
n_iter=100



if model is not None:
    nlp = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")
    
    
# create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
# otherwise, get it so we can add labels
else:
    ner = nlp.get_pipe('ner')

  # add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

    # get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            nlp.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.5,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)
```



#### 4. Result demonstration

With the trained ml model, we did testing using annual report with title '67'. With a .json file generated, it is found that although some minor errors may occur, in overall the results are quite promissing. 

An example of the result.json:

```json
{
	"bbox": "316 1644 1495 1665",
	"page": 67,
	"content": "(1) Mr Chan Teck Ee Vincent ceased as an Executive Director of the Company with effect from 31 August 2017.",
	"entityType": "Audit Period"
},
```

```json
{
	"bbox": "316 1543 1029 1566",
	"page": 67,
	"content": "Mr Lye Hoong Yip Raymond independent Director",
	"entityType": "Name of auditor"
}
```

