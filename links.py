import requests
from bs4 import BeautifulSoup
import functions
def getLinksForChapter(url, chapNumber):
    if url == 'https://onepiece-scan.com/manga/one-piece-scan-':
        url_chap = url + str(chapNumber) + '/'
        response = requests.get(url_chap)
        if response.ok:
            page = BeautifulSoup(response.text,features="html.parser") 
            images = [img['src'] for img in page.find_all('img', { 'class' : 'wp-manga-chapter-img' })]
        return images
    elif url == 'https://scanjujutsukaisen.com/manga/jujutsu-kaisen-scan-':
        if chapNumber >= 160:
            url_chap = url + str(chapNumber) + '-vf/'
        else:
            url_chap = url + str(chapNumber) + '/'
        print(url_chap)
        response = requests.get(url_chap)
        if response.ok:
            page = BeautifulSoup(response.text,features="html.parser") 
            images = [img['src'] for img in page.find_all('img', { 'class' : 'wp-manga-chapter-img' })]
            images.pop(len(images)-1)
        print('les liens:')
        for img in images:
            print(img) 
        return images
    else:
        print("URL non prise en charge")

#https://scanjujutsukaisen.com/manga/jujutsu-kaisen-scan-3/
#https://scanjujutsukaisen.com/manga/jujutsu-kaisen-scan-3-vf/

def saveDim(w,h):
    functions.widthPDF = w
    functions.heightPDF = h