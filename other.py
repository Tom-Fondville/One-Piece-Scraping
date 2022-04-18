#import imp
#import functions
#import os
#import sys
from tkinter.filedialog import *
url = 'https://onepiece-scan.com/manga/one-piece-scan-'
#functions.saveChapter(url,2)
#print(os.path.exists('images/chapter21/img0.jpg'))
#functions.saveAndPDF(url,int(sys.argv[1]),int(sys.argv[2]))

#filepath = askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
path = askdirectory()
print(str(path))