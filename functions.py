import re

from numpy import Infinity
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
mangaName = "MangaName"
path ="PDF"
logLabelText = ""
regexType = re.compile(r'(?i)\.(jpg|png)')

class InfoIMG:
    def __init__(self, imgNumber, size, height, width):
        self.imgNumber = imgNumber
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
    #logLabelText.set("Récupération des liens")
    return links.getLinksForChapter(url,chapNumber)


def createFolder(chapNumber):
    print("Créartion du folder " + str(chapNumber))
    logLabelText.set("Créartion du folder " + str(chapNumber))
    os.makedirs('images/chapter' + str(chapNumber), exist_ok=True)

def saveImg(url,chapNumber,pageNumber):
    if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.jpg') == False and os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.png') == False:
        print(str(pageNumber), end='', flush=True)
        logLabelText.set(str(pageNumber))
        img_data = requests.get(url).content
        typeOfFyle = regexType.findall(url)[0]
        with open('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.' + typeOfFyle, 'wb') as handler:
            handler.write(img_data)

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
        saveImg(links[i],chapNumber,i)
    print("\nDownloaded!")
    logLabelText.set("Downloaded!")

def getDimentions(chapNumber,pageNumber):
    print("dimentions image" + str(pageNumber))
    if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(pageNumber) +'.jpg'):
        imageInfo = cv2.imread('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg')
        return imageInfo.shape[:2]
    else:
        imageInfo = cv2.imread('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.png')
        return imageInfo.shape[:2]
    

def getPdfDimentions(chapNumber):
    hMax = 0
    wMax = 0
    wMin = Infinity
    print("La chap" +str(chapNumber) +"a "+str(countNumberPage(chapNumber))+" pages")
    for i in range(countNumberPage(chapNumber)):
        h,w = getDimentions(chapNumber,i)
        if w < wMin:
            wMin = w
        if w > wMax:
            wMax = w
        if h > hMax:
            hMax = h
        if wMax - wMin < 200:
            wMax = wMax*2
    return hMax,wMax


def countNumberPage(chapNumber):
    initial_count = 0
    dir = "images/chapter" + str(chapNumber)
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    #print(initial_count)
    return initial_count

def makeChapterMapping(chapNumber):
    for i in range(countNumberPage(chapNumber)):
        h,w = getDimentions(chapNumber,i)
        print("Pour l'image" + str(i) + " " + str(w) + " size", end='')
        if w >= MesVariables.widthPDF - 200 and w <= MesVariables.widthPDF + 200:
            MesVariables.ImageMappingList.append(InfoIMG(i,2,h,w))
            print(2)
        else:
            MesVariables.ImageMappingList.append(InfoIMG(i,1,h,w))
            print(1)
    
    images = MesVariables.ImageMappingList
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
        valuePage = 0

    print("Nb pages:" +str(len(pagesIntegration)))
    links.printMapping(pagesIntegration)
    pagesIntegration.reverse()
    return pagesIntegration
    

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
    print(MesVariables.ImageMappingList[pageNumber].size)
    if MesVariables.ImageMappingList[pageNumber].size == 2:
        print("img Large")
        addImage(pdf,chapNumber,pageNumber,height,width,0,0,'true')
        MesVariables.rightOrLeft = 'right'
    else:
        print("img fine")
        if MesVariables.rightOrLeft == 'right':
            addImage(pdf,chapNumber,pageNumber,height,width,MesVariables.widthPDF/2,0,'true')
            MesVariables.rightOrLeft = 'left'
        else:
            addImage(pdf,chapNumber,pageNumber,height,width,0,0,'false')
            MesVariables.rightOrLeft = 'right'
    print()

def addAllPage(pdf,chapNumber,pagesIntegration):
    for page in range(len(pagesIntegration)):
        print("La page " + str(page) + " contient: [",end="")
        if pagesIntegration[page][0] == 'solo':
            print(str(pagesIntegration[page][1].imgNumber) + ",]")
            h = pagesIntegration[page][1].height
            w = pagesIntegration[page][1].width
            imageNumber = pagesIntegration[page][1].imgNumber
            addImage(pdf,chapNumber,imageNumber,h,w,0,0,'true')

        elif pagesIntegration[page][0] == 'full':
            print(str(pagesIntegration[page][1].imgNumber) + "]")
            h = pagesIntegration[page][1].height
            w = pagesIntegration[page][1].width
            imageNumber = pagesIntegration[page][1].imgNumber
            addImage(pdf,chapNumber,imageNumber,h,w,0,0,'true')

        elif pagesIntegration[page][0] == 'split':
            print(str(pagesIntegration[page][1].imgNumber) + "," + str(pagesIntegration[page][2].imgNumber) + "]")
            h = pagesIntegration[page][1].height
            w = pagesIntegration[page][1].width
            imageNumber = pagesIntegration[page][1].imgNumber
            addImage(pdf,chapNumber,imageNumber,h,w,0,0,'true')
            h = pagesIntegration[page][2].height
            w = pagesIntegration[page][2].width
            imageNumber = pagesIntegration[page][2].imgNumber
            addImage(pdf,chapNumber,imageNumber,h,w,MesVariables.widthPDF/2,0,'false')


def addImage(pdf,chapNumber,imageNumber,height,width,x,y,newPageBool):
    if newPageBool == 'true':
        print("new page number " + str(imageNumber))
        pdf.add_page()
    if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(imageNumber) +'.jpg'):
        pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(imageNumber) +'.jpg', x = x, y = y, w = width, h = height, type = 'JPG', link = '')
    else:
        pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(imageNumber) +'.png', x = x, y = y, w = width, h = height, type = 'PNG', link = '')

def makeChapterInPDF(pdf,chapNumber):
    MesVariables.ImageMappingList.clear()
    print("Ajout du chapitre " + str(chapNumber) + " au pdf")
    logLabelText.set("Ajout du chapitre " + str(chapNumber) + " au pdf")
    pageIntegration = makeChapterMapping(chapNumber)
    print("AAAAAA")
    links.printMapping(pageIntegration)
    addAllPage(pdf,chapNumber,pageIntegration)

    #for i in range(countNumberPage(chapNumber)):
    #    addPage(pdf,chapNumber,i)

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

def saveAndPDF(url,name,firstChap,lastChap):
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
        endPDF(pdf, name + " Chapter " + str(firstChap))
    else:    
        endPDF(pdf, name + " Chapter " + str(firstChap) + "-" + str(lastChap))


