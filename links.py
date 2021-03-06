import re
import requests
from bs4 import BeautifulSoup
import functions
regexType = re.compile(r'(?i)\.(jpg|png)')
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
            #images.pop(len(images)-1)
        print('les liens:')
        intrus = []
        for img in range(len(images)):
            result = regexType.findall(images[img])
            if len(result) == 0:
                intrus.append(img)
        for i in intrus:
            images.pop(i)
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

def printMapping(pagesIntegration):
    for page in range(len(pagesIntegration)):
        print("La page " + str(page) + " contient: [",end="")
        if pagesIntegration[page][0] == 'solo':
            print(str(pagesIntegration[page][1].imgNumber) + ",]")
        elif pagesIntegration[page][0] == 'full':
            print(str(pagesIntegration[page][1].imgNumber) + "]")
        elif pagesIntegration[page][0] == 'split':
            print(str(pagesIntegration[page][1].imgNumber) + "," + str(pagesIntegration[page][2].imgNumber) + "]")