from bs4 import BeautifulSoup
import urllib.request
import requests
from PIL import Image
import io
import tesserocr
import os
import sys
from multiprocessing import Pool as ProcessPool
import multiprocessing.popen_spawn_win32 as forking 
import multiprocessing
#import time

#windows multithreading bullshit
class _Popen(forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            os.putenv('_MEIPASS2', sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')

class Process(multiprocessing.Process):
    _Popen = _Popen

#webpage links and vars
#start_time = time.time()
pages = [
    'https://www.raskakcija.lt/aibe-akciju-leidinys.htm',
    'https://www.raskakcija.lt/iki-akciju-leidinys.htm',
    'https://www.raskakcija.lt/maxima-akciju-leidinys.htm',
    'https://www.raskakcija.lt/norfa-akciju-leidinys.htm'
]
api = tesserocr.PyTessBaseAPI(os.path.dirname(os.path.realpath(__file__)) + "\\tessdata", lang='lit')
#store checking function
def checkStore(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.findAll(class_= 'plati')
    imgs = list()
    for div in divs:
        string = str(div)
        imgs.append(string.split("\"")[7])
    for j in range(0, len(imgs)):
        response = requests.get(imgs[j])
        img = Image.open(io.BytesIO(response.content))
        api.SetImage(img)
        text = api.GetUTF8Text()
        string = str(text)
        string = string.replace('\n', '').replace('-', '')
        val = string.find("MONSTER")
        if val > -1:
            print(imgs[j])
            return True
    return False
#main
num_of_threads = 4
os.system("")
if __name__ ==  '__main__':
    multiprocessing.freeze_support()
    with ProcessPool(num_of_threads) as pool:
        results = pool.map(checkStore, pages)
        if results[0]:
            print("\033[92mAIBĖ - TAIP")
        else:
            print("\033[91mAIBĖ - NE")
        if results[1]:
            print("\033[92mIKI - TAIP")
        else:
            print("\033[91mIKI - NE")
        if results[2]:
            print("\033[92mMAXIMA - TAIP")
        else:
            print("\033[91mMAXIMA - NE")
        if results[3]:
            print("\033[92mNORFA - TAIP")
        else:
            print("\033[91mNORFA - NE")
        print("\033[0m")
        #print("--- %s seconds ---" % (time.time() - start_time))
        os.system('pause')
        
'''
for i in range(0, 4):
    quote_page = pages[i]
    page = urllib.request.urlopen(quote_page)

    soup = BeautifulSoup(page, 'html.parser')

    divs = soup.findAll(class_= 'plati')
    imgs = list()   
    for div in divs:
        string = str(div)
        imgs.append(string.split("\"")[7])
    for j in range(0, len(imgs)):
        response = requests.get(imgs[j])
        img = Image.open(io.BytesIO(response.content))
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(img, lang="lit")
        string = str(text)
        if string.find("MONSTER") > -1:
            found[i] = True
            break
if found[0]:
    print("AIBĖ - TAIP")
else:
    print("AIBĖ - NE")
if found[1]:
    print("IKI - TAIP")
else:
    print("IKI - NE")
if found[2]:
    print("MAXIMA - TAIP")
else:
    print("MAXIMA - NE")
if found[3]:
    print("NORFA - TAIP")
else:
    print("NORFA - NE")'''