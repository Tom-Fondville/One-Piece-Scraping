import re
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

def getLinks(logLabelText,url):
    print("Récupération des liens")
    logLabelText.set("Récupération des liens")
    response = requests.get(url)
    if response.ok:
        page = BeautifulSoup(response.text,features="html.parser") 
        images = [img['src'] for img in page.find_all('img', { 'class' : 'wp-manga-chapter-img' })]
    return images


def createFolder(logLabelText,chapNumber):
    print("Créartion du folder " + str(chapNumber))
    logLabelText.set("Créartion du folder " + str(chapNumber))
    os.makedirs('images/chapter' + str(chapNumber), exist_ok=True)

def saveImg(url,name,chapNumber):
    img_data = requests.get(url).content
    with open('images/chapter' + str(chapNumber) + '/' + str(name) +'.jpg', 'wb') as handler:
        handler.write(img_data)

def saveChapter(logLabelText,url,chapNumber):
    url_chap = url + str(chapNumber) + '/'
    print("Début :" +str(url_chap))
    logLabelText.set("Début :" +str(url_chap))
    links = getLinks(logLabelText,url_chap)
    createFolder(logLabelText,chapNumber)
    print("downloading...")
    logLabelText.set("downloading...")
    for i in range(len(links)):
        if os.path.exists('images/chapter' + str(chapNumber) + '/img' + str(i) +'.jpg') == False:
            print(str(i), end='', flush=True)
            logLabelText.set(str(i))
            saveImg(links[i],'img' + str(i),chapNumber)
    print("\nDownloaded!")
    logLabelText.set("Downloaded!")

def getDimentions(chapNumber,pageNumber):
    imageInfo = cv2.imread('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg')
    return imageInfo.shape[:2]

def countNumberPage(chapNumber):
    initial_count = 0
    dir = "images/chapter" + str(chapNumber)
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    print(initial_count)
    return initial_count

def createPDF(logLabelText,width,height):
    print("Création du PDF")
    logLabelText.set("Création du PDF")
    return FPDF(format=(width,height))

def endPDF(logLabelText,pdf,name):
    print("Fin du PDF")
    logLabelText.set("Fin du PDF")
    pdf.output(path + "/" + str(name) + '.pdf', 'F')

def addPage(pdf,chapNumber,pageNumber,width,height):
    #height, width = getDimentions(chapNumber,pageNumber)
    pdf.add_page()
    pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg', x = 0, y = 0, w = width, h = height, type = 'JPG', link = '')

def makeChapterInPDF(logLabelText,pdf,chapNumber):
    print("Ajout du chapitre " + str(chapNumber) + " au pdf")
    logLabelText.set("Ajout du chapitre " + str(chapNumber) + " au pdf")
    height, width = getDimentions(chapNumber,2)
    for i in range(countNumberPage(chapNumber)):
        addPage(pdf,chapNumber,i,width,height)

def makeNbChapterInPDF(logLabelText,firstChap,lastChap):
    if lastChap<firstChap:
        return ExecError()
    height, width = getDimentions(firstChap,2)
    pdf = createPDF(logLabelText,width,height)
    currChap = firstChap
    while currChap <= lastChap:
        makeChapterInPDF(logLabelText,pdf,currChap)
        currChap+= 1
    if int(firstChap) == int(lastChap):
        endPDF(logLabelText,pdf,"One Piece Chapter " + str(firstChap))
    else:    
        endPDF(logLabelText,pdf,"One Piece Chapter " + str(firstChap) + "-" + str(lastChap))

def saveAndPDF(logLabelText,url,firstChap,lastChap):
    if lastChap<firstChap:
        logLabelText.set("Problème! Le dernier chapitre est inférieur au premier!")
        return ExecError()
    currChap = firstChap
    while currChap <= lastChap:
        saveChapter(logLabelText,url,currChap)
        currChap+= 1
    makeNbChapterInPDF(logLabelText,firstChap,lastChap)


