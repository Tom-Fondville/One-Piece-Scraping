import re
import links
from shutil import ExecError
from tkinter.messagebox import RETRY
from turtle import st
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
import os
import cv2
import sys
from tkinter import *
#url = 'https://onepiece-scan.com/manga/one-piece-scan-'
path ="PDF"
logLabelText = ""
regexType = re.compile(r'(?i)\.(jpg|png)')

class InfoIMG:
    def __init__(self, size, height, width):
        self.size = size
        self.height = height
        self.width = width

class MesVariables:
    rightOrLeft = 'right'
    heightPDF = ""
    widthPDF = ""
    ImageMappingList = [] #Si une image prend la page entirèe {valeur 2,height,width}, si elle prend une demie page {valeur 1,height,width}

def getLinks(url, chapNumber):
    print("Récupération des liens")
    logLabelText.set("Récupération des liens")
    return links.getLinksForChapter(url,chapNumber)


def createFolder(chapNumber):
    print("Créartion du folder " + str(chapNumber))
    logLabelText.set("Créartion du folder " + str(chapNumber))
    os.makedirs('images/chapter' + str(chapNumber), exist_ok=True)

def saveImg(url,chapNumber,pageNumber):
    img_data = requests.get(url).content
    typeOfFyle = regexType.findall(url)[0]
    #print(typeOfFyle)
    with open('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.' + typeOfFyle, 'wb') as handler:
        handler.write(img_data)
    h,w = getDimentions(chapNumber,pageNumber)
    if w == MesVariables.widthPDF:
        MesVariables.ImageMappingList.append(InfoIMG(2,h,w))
    else:
        MesVariables.ImageMappingList.append(InfoIMG(1,h,w))

def saveChapter(url,chapNumber):
    #url_chap = url + str(chapNumber) + '/'
    #print("Début :" +str(url_chap))
    print("Début :" +str(url) + " chapter " + str(chapNumber))
    logLabelText.set("Début :" +str(url))
    links = getLinks(url, chapNumber)
    createFolder(chapNumber)
    print("downloading...")
    logLabelText.set("downloading...")
    for i in range(len(links)):
        if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(i) +'.jpg') == False and os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(i) +'.png') == False:
            print(str(i), end='', flush=True)
            logLabelText.set(str(i))
            saveImg(links[i],chapNumber,i)
    print("\nDownloaded!")
    logLabelText.set("Downloaded!")

def getDimentions(chapNumber,pageNumber):
    if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.jpg'):
        imageInfo = cv2.imread('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg')
    else:
        imageInfo = cv2.imread('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.png')
    return imageInfo.shape[:2]

def getPdfDimentions(chapNumber):
    hMax = 0
    wMax = 0
    for i in range(countNumberPage(chapNumber)):
        h,w = getDimentions(chapNumber,i)
        if w > wMax:
            wMax = w
        if h > hMax:
            hMax = h
    return hMax,wMax


def countNumberPage(chapNumber):
    initial_count = 0
    dir = "images/chapter" + str(chapNumber)
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    #print(initial_count)
    return initial_count

def createPDF(width,height):
    print("Création du PDF")
    logLabelText.set("Création du PDF")
    return FPDF(orientation='P',format=(width,height))

def endPDF(pdf,name):
    print("Fin du PDF")
    logLabelText.set("Fin du PDF")
    pdf.output(path + "/" + str(name) + '.pdf', 'F')

def addPage(pdf,chapNumber,pageNumber):
    height, width = getDimentions(chapNumber,pageNumber)
    print("largeur img :" + str(width))
    print("hauteur img :" + str(height))
    if width == int(MesVariables.widthPDF):
        #print("new page number " + str(pageNumber))
        #pdf.add_page()
        addImage(pdf,chapNumber,pageNumber,height,width,0,0,'true')
    else:
        print("work in progress")
        if MesVariables.rightOrLeft == 'right':
            #print("new page number " + str(pageNumber))
            #pdf.add_page()
            addImage(pdf,chapNumber,pageNumber,height,width,MesVariables.widthPDF/2,0,'true')
            MesVariables.rightOrLeft = 'left'
        else:
            addImage(pdf,chapNumber,pageNumber,height,width,0,0,'false')
            MesVariables.rightOrLeft = 'right'
    print()

def addImage(pdf,chapNumber,pageNumber,height,width,x,y,newPageBool):
    if newPageBool == 'true':
        print("new page number " + str(pageNumber))
        pdf.add_page()
    if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.jpg'):
        pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg', x = x, y = y, w = width, h = height, type = 'JPG', link = '')
    else:
        pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.png', x = x, y = y, w = width, h = height, type = 'PNG', link = '')

def makeChapterInPDF(pdf,chapNumber):
    print("Ajout du chapitre " + str(chapNumber) + " au pdf")
    logLabelText.set("Ajout du chapitre " + str(chapNumber) + " au pdf")
    for i in range(countNumberPage(chapNumber)):
        addPage(pdf,chapNumber,i)

def makeNbChapterInPDF(firstChap,lastChap):
    if lastChap<firstChap:
        return ExecError()
    height, width = getPdfDimentions(firstChap)
    MesVariables.heightPDF = height
    MesVariables.widthPDF = width
    print("Largeur du PDF : " + str(MesVariables.widthPDF))
    pdf = createPDF(width,height)
    
    currChap = firstChap
    while currChap <= lastChap:
        makeChapterInPDF(pdf,currChap)
        currChap+= 1
    if int(firstChap) == int(lastChap):
        endPDF(pdf,"One Piece Chapter " + str(firstChap))
    else:    
        endPDF(pdf,"One Piece Chapter " + str(firstChap) + "-" + str(lastChap))

def saveAndPDF(url,firstChap,lastChap):
    if lastChap<firstChap:
        logLabelText.set("Problème! Le dernier chapitre est inférieur au premier!")
        return ExecError()
    currChap = firstChap
    #Le premier chap 
    saveChapter(url,currChap)
    height, width = getPdfDimentions(firstChap)
    MesVariables.heightPDF = height
    MesVariables.widthPDF = width
    print("Largeur du PDF : " + str(MesVariables.widthPDF))
    pdf = createPDF(width,height)
    makeChapterInPDF(pdf,currChap)
    currChap+= 1
    #Les chap suivants
    while currChap <= lastChap:
        saveChapter(url,currChap)
        makeChapterInPDF(pdf,currChap)
        currChap+= 1
    #makeNbChapterInPDF(firstChap,lastChap)
    if int(firstChap) == int(lastChap):
        endPDF(pdf,"One Piece Chapter " + str(firstChap))
    else:    
        endPDF(pdf,"One Piece Chapter " + str(firstChap) + "-" + str(lastChap))


