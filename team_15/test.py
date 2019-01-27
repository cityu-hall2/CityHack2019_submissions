from bs4 import BeautifulSoup
import difflib
import numpy as np

hocr_file = "/media/leon/22CEF525CEF4F241/LEONLAH/CityUHack/CityU-Hackathon-2019/Training/1/hocr/1-74.hocr"
shape = (164,1)
hocr_report1 = np.chararray(shape)
# for i in (0,164):
#     hocr_report+


search_terms = ('financial', 'year')

def parse_hocr(search_terms=None, hocr_file=None, regex=None):
    """Parse the hocr file and find a reasonable bounding box for each of the strings
    in search_terms.  Return a dictionary with values as the bounding box to be used for
    extracting the appropriate text.

    inputs:
        search_terms = Tuple, A tuple of search terms to look for in the HOCR file.

    outputs:
        box_dict = Dictionary, A dictionary whose keys are the elements of search_terms and values
        are the bounding boxes where those terms are located in the document.
    """
    # Make sure the search terms provided are a tuple.
    if not isinstance(search_terms,tuple):
        raise ValueError('The search_terms parameter must be a tuple')

    # Make sure we got a HOCR file handle when called.
    if not hocr_file:
        raise ValueError('The parser must be provided with an HOCR file handle.')

    # Open the hocr file, read it into BeautifulSoup and extract all the ocr words.
    hocr = open(hocr_file,'r').read()
    soup = BeautifulSoup(hocr,'html.parser')
    words = soup.find_all('span',class_='ocrx_word')

    result = dict()


    # Loop through all the words and look for our search terms.
    for word in words:

        w = word.get_text().lower()

        for s in search_terms:

            # If the word is in our search terms, find the bounding box
            if len(w) > 1 and difflib.SequenceMatcher(None, s, w).ratio() > .5:
                bbox = word['title'].split(';')
                bbox = bbox[0].split(' ')
                bbox = tuple([int(x) for x in bbox[1:]])
                count = bbox.count(s)

                # Update the result dictionary or raise an error if the search term is in there twice.
                if s not in result.keys():
                    result.update({s:bbox})
                else:

                    result.update({s+"("+str(count)+")":bbox})

            else:
                pass

    return result

print('\n')
print(hocr_file)
print(parse_hocr(search_terms, hocr_file, ))
