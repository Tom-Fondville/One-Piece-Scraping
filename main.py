from turtle import pd
from bs4 import BeautifulSoup
from fpdf import FPDF
import sys
import functions

url = 'https://onepiece-scan.com/manga/one-piece-scan-'
try:
    sys.argv[3]
    functions.saveAndPDF(str(sys.argv[3]),int(sys.argv[1]),int(sys.argv[2]))
except:
    try:
        functions.saveAndPDF(url,int(sys.argv[1]),int(sys.argv[2]))
    except:
        import interface
