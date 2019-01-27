from __future__ import print_function
import os
import json
from lxml import etree, html
import re

path = "C:/Users/Harry Sun/Desktop/HarrySun/City University of Hong Kong/Year 2/CityHack/CityU-Hackathon-2019/Training"

for filename in os.listdir(path):
    file = open(path+"/"+filename+"/"+filename+"_tagged.json", "r", encoding='utf-8')
    fw = open("rw/rwdata_"+filename+".txt", "w",encoding='utf-8')
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