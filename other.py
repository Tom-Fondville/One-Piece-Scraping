#import imp
from multiprocessing.dummy import Array
from turtle import width
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


lst = ['cc','kk']
print(lst[0])
print(lst[1])
try:
    print(lst[2])
except:
    print("out")
