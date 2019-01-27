 #  wrapper over argparse
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar



model = None
output_dir=Path("abc")
n_iter=100


# test the saved model
print("Loading from", output_dir)
# test_data=  [
#     ('Total shareholders’ equity')
# ]

f = open('test_67.txt','r',encoding='utf-8')
test_data = eval(f.read())

nlp2 = spacy.load(output_dir)
for text in test_data:
    doc = nlp2(text['content'])
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])