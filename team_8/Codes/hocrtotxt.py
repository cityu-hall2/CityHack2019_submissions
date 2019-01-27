from __future__ import print_function
import os
import re
from lxml import etree, html
path = "../CityU-Hackathon-2019/Training"

################################################################
# main program
################################################################
for filename in os.listdir(path):
    fw = open("txtResult/result_"+filename+".txt", "w", encoding="utf-8")
    for f in os.listdir(path+"/"+filename+"/hocr"):
        fw.write(f.split("-",1)[1]+": \n")
        doc = html.parse(path + "/" + filename + "/hocr/" + f)
        for para in doc.xpath("//*[@class='ocr_par']"):
           for line in para:
              fw.write(re.sub(r'\s+', '\x20', line.text_content()).strip())
           fw.write("\n")
        fw.write("===================================================\n")
    fw.close()