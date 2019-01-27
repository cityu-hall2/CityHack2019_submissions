import numpy as np
from bs4 import BeautifulSoup

hocr_file = "/media/leon/22CEF525CEF4F241/LEONLAH/CityUHack/CityU-Hackathon-2019/Training/1/hocr/1-74.hocr"
output_file = "/media/leon/22CEF525CEF4F241/LEONLAH/CityUHack/projects/result1.txt"

hocr = open(hocr_file, 'r').read()
soup = BeautifulSoup(hocr, 'html.parser')
words = soup.find_all('span', class_='ocrx_word')

result = dict()

for word in words:
    w = word.get_text().lower()

    bbox = word['title'].split(';')
    bbox = bbox[0].split(' ')
    bbox = tuple([int(x) for x in bbox[1:]])

    result.update({w: bbox})

print('')
print(hocr_file)
print(result)

