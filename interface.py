from tkinter import *
from tkinter.filedialog import *
import functions
from turtle import color, onclick, width 

def myFunction(event):
    print(str(event))


window = Tk()
window.title("Online Scan to PDF")

urlFrame = Frame(window, borderwidth=0, relief=GROOVE)
urlFrame.pack()
urlLabel = Label(urlFrame, text="URL")
urlLabel.pack()
url_default = StringVar() 
url_default.set("https://onepiece-scan.com/manga/one-piece-scan-")
url_textBox = Entry(urlFrame, textvariable=url_default, width=30)
url_textBox.bind("<Button-1>",myFunction)
url_textBox.pack(expand="yes")


chapterSelectorContainer = PanedWindow(window, orient=HORIZONTAL)

firstFrame = Frame(window, borderwidth=2, relief=GROOVE)
firstFrame.pack()
firstChapterLabel = Label(firstFrame, text="Fist Chapter")
firstChapterLabel.pack()
firstChapter = Spinbox(firstFrame, from_=1, to=1000, width=2)
firstChapter.pack()
chapterSelectorContainer.pack()
chapterSelectorContainer.add(firstFrame)

lastFrame = Frame(window, borderwidth=2, relief=GROOVE)
lastFrame.pack()
lastChapterLabel = Label(lastFrame, text="Last Chapter")
lastChapterLabel.pack()
lastChapter = Spinbox(lastFrame, from_=1, to=1000, width=2)
lastChapter.pack()
chapterSelectorContainer.add(lastFrame)

chapterSelectorContainer.pack()

outFolderButton = Button(window, text="Out folder")
outFolderButton.pack()

bouton=Button(window, text="Download")
bouton.pack()

def outFolderButtonFunction(event):
    functions.path = askdirectory(initialdir = functions.path, title = "Select out folder")
outFolderButton.bind("<Button-1>",outFolderButtonFunction)

def buttonFunction(event):
    currentURL = str(url_textBox.get())
    print(currentURL)
    first = int(firstChapter.get())
    print(str(first))
    last = int(lastChapter.get())
    print(str(last))
    logLabelText = StringVar()
    logLabelText.set("log")
    logLabel = Label(window, textvariable=logLabelText, bg="black", fg="white", width=30)
    logLabel.pack()
    functions.saveAndPDF(logLabelText,currentURL,first,last)
    logLabel.destroy()
bouton.bind("<Button-1>",buttonFunction)

window.mainloop()
