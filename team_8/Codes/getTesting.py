from __future__ import print_function
import os
import json
from lxml import etree, html
import re

path = "C:/Users/Harry Sun/Desktop/HarrySun/City University of Hong Kong/Year 2/CityHack/CityU-Hackathon-2019/Testing"
a = []
for filename in os.listdir(path):
    fw = open("TestingData/test_"+filename+".txt", "w", encoding="utf-8")
    for f in os.listdir(path+"/"+filename+"/hocr"):
        doc = html.parse(path + "/" + filename + "/hocr/" + f)
        for para in doc.xpath("//*[@class='ocr_par']"):
           for line in para:
               a.append({"bbox":line.get("title").split(";", 1)[0].split(" ",1)[1],"page":int(filename.split("-",1)[0]),"content":re.sub(r'\s+', '\x20', line.text_content()).strip()})
    fw.write(str(a))
    fw.write("\n")
    fw.close()