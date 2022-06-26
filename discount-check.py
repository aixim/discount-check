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

#start_time = time.time()
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
        string = string.replace('\n', '').replace('-', '').lower()
        val = string.find("cido") #find occurences with specified item
        if val > -1:
            return imgs[j]
    return False
#main
num_of_threads = 4
os.system("")
if __name__ ==  '__main__':
    pages = [
    'https://www.raskakcija.lt/aibe-akciju-leidinys.htm',
    'https://www.raskakcija.lt/iki-akciju-leidinys.htm',
    'https://www.raskakcija.lt/maxima-akciju-leidinys.htm',
    'https://www.raskakcija.lt/norfa-akciju-leidinys.htm'
    ]
    multiprocessing.freeze_support()
    with ProcessPool(num_of_threads) as pool:
        results = pool.map(checkStore, pages)
        if results[0]:
            print("\033[92mAIBĖ - TAIP - " + results[0])
        else:
            print("\033[91mAIBĖ - NE")
        if results[1]:
            print("\033[92mIKI - TAIP - " + results[1])
        else:
            print("\033[91mIKI - NE")
        if results[2]:
            print("\033[92mMAXIMA - TAIP - " + results[2])
        else:
            print("\033[91mMAXIMA - NE")
        if results[3]:
            print("\033[92mNORFA - TAIP - " + results[3])
        else:
            print("\033[91mNORFA - NE")
        print("\033[0m")
        #print("--- %s seconds ---" % (time.time() - start_time))
        os.system('pause')