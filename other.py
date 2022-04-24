#import imp
from multiprocessing.dummy import Array
from turtle import width

from numpy import Infinity
import functions
#import os
#import sys
import re
import links
from tkinter.filedialog import *
url = 'https://onepiece-scan.com/manga/one-piece-scan-'
#functions.saveChapter(url,2)
#print(os.path.exists('images/chapter21/img0.jpg'))
#functions.saveAndPDF(url,int(sys.argv[1]),int(sys.argv[2]))

#filepath = askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
#path = askdirectory()
#print(str(path))

#p = re.compile(r'(?i)\.(jpg|png)')
#liens = links.getLinksForChapter('https://scanjujutsukaisen.com/manga/jujutsu-kaisen-scan-',2)
#for img in liens:
#    print(p.findall(img))
class InfoIMG:
    def __init__(self, size, name):
        self.size = size
        self.name = name
def truccool():
    images = [InfoIMG(1,'IMG0'),InfoIMG(2,'IMG1'),InfoIMG(2,'IMG2'),InfoIMG(2,'IMG3'),InfoIMG(1,'IMG4'),InfoIMG(1,'IMG5'),InfoIMG(1,'IMG6'),InfoIMG(1,'IMG7'),InfoIMG(1,'IMG8'),InfoIMG(1,'IMG9'),InfoIMG(1,'IMG10'),InfoIMG(1,'IMG11'),InfoIMG(1,'IMG12'),InfoIMG(1,'IMG13'),InfoIMG(1,'IMG14'),InfoIMG(1,'IMG15')]

    nbPages = 0
    valuePage= 0
    pagesIntegration = []
    index = len(images)-1
    while index >= 0:
        if index == 0:
            valuePage += images[index].size

            if valuePage == 1:
                pagesIntegration.append(['solo',images[index]])
            if valuePage == 2:
                pagesIntegration.append(['full',images[index]])
        else:
            valuePage += images[index].size
            valuePage += images[index-1].size

            if valuePage == 2:
                pagesIntegration.append(['split',images[index],images[index-1]])
            elif valuePage == 3:
                if images[index].size == 1:
                    pagesIntegration.append(['solo',images[index]])
                    pagesIntegration.append(['full',images[index-1]])
                else:
                    pagesIntegration.append(['full',images[index]])
                    print("La valeur de la page :" + str(valuePage))
                    index -=1
                    valuePage = 0
                    continue
            elif valuePage == 4:
                pagesIntegration.append(['full',images[index]])
                pagesIntegration.append(['full',images[index-1]])
        index -= 2
        print("La valeur de la page :" + str(valuePage))
        
        if valuePage > 2:
            nbPages = nbPages + 2
        else:
            nbPages = nbPages + 1

        valuePage = 0

    print("Nb pages:" +str(len(pagesIntegration)))
    pagesIntegration.reverse()
    for page in range(len(pagesIntegration)):
        print("La page " + str(page) + " contient: [",end="")
        if pagesIntegration[page][0] == 'solo':
            print(pagesIntegration[page][1].name + ",]")
        elif pagesIntegration[page][0] == 'full':
            print(pagesIntegration[page][1].name + "]")
        elif pagesIntegration[page][0] == 'split':
            print(pagesIntegration[page][1].name + "," + pagesIntegration[page][2].name + "]")

#print(functions.makeChapterMapping(1))
