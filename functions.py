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
url = 'https://onepiece-scan.com/manga/one-piece-scan-'

def getLinks(url):
    print("Récupération des liens")
    response = requests.get(url)
    if response.ok:
        page = BeautifulSoup(response.text,features="html.parser") 
        #images = page.findAll('img', { 'class' : 'wp-manga-chapter-img' })
        images = [img['src'] for img in page.find_all('img', { 'class' : 'wp-manga-chapter-img' })]
    return images


def createFolder(chapNumber):
    print("Créartion du folder " + str(chapNumber))
    os.makedirs('images/chapter' + str(chapNumber), exist_ok=True)

def saveImg(url,name,chapNumber):
    img_data = requests.get(url).content
    with open('images/chapter' + str(chapNumber) + '/' + str(name) +'.jpg', 'wb') as handler:
        handler.write(img_data)

def saveChapter(url,chapNumber):
    url_chap = url + str(chapNumber) + '/'
    print("Début :" +str(url_chap))
    links = getLinks(url_chap)
    createFolder(chapNumber)
    print("downloading...")
    for i in range(len(links)):
        print(str(i), end='', flush=True)
        saveImg(links[i],'img' + str(i),chapNumber)
    print("\nDownloaded!")

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

def createPDF(width,height):
    print("Création du PDF")
    return FPDF(format=(width,height))

def endPDF(pdf,name):
    print("Fin du PDF")
    pdf.output("PDF/" + str(name) + '.pdf', 'F')

def addPage(pdf,chapNumber,pageNumber,width,height):
    #height, width = getDimentions(chapNumber,pageNumber)
    pdf.add_page()
    pdf.image('images/chapter'+ str(chapNumber) +'/img'+ str(pageNumber) +'.jpg', x = 0, y = 0, w = width, h = height, type = 'JPG', link = '')

def makeChapterInPDF(pdf,chapNumber):
    print("Ajout du chapitre " + str(chapNumber) + " au pdf")
    height, width = getDimentions(chapNumber,2)
    for i in range(countNumberPage(chapNumber)):
        addPage(pdf,chapNumber,i,width,height)

def makeNbChapterInPDF(firstChap,lastChap):
    if lastChap<firstChap:
        return ExecError()
    height, width = getDimentions(firstChap,2)
    pdf = createPDF(width,height)
    currChap = firstChap
    while currChap <= lastChap:
        makeChapterInPDF(pdf,currChap)
        currChap+= 1
    endPDF(pdf,"One Piece Chapter" + str(firstChap) + "-" + str(lastChap))

def saveAndPDF(url,firstChap,lastChap):
    if lastChap<firstChap:
        return ExecError()
    currChap = firstChap
    while currChap <= lastChap:
        saveChapter(url,currChap)
        currChap+= 1
    makeNbChapterInPDF(firstChap,lastChap)


