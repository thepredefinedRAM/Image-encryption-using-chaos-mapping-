import random
import time
from tkinter import *
from tkinter import filedialog
import threading
from tkinter.ttk import Progressbar

import cv2
from PIL import ImageTk, Image as Im
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt


from ArnoldCatTransform import ArnoldCat
from LogisticChaosMapswithkeymixing import LogisticEncryption, LogisticDecryption

initDir = "\\"
scale_w = 1/3
scale_h = 1/3


class CryptoFrame:

    def __init__(self, masterframe, currentframe, algo, mode):
        self.a = None
        self.img1 = None
        self.img2 = None
        self.filename = "File not selected"
        self.frame = Frame(masterframe)
        self.currentframe = currentframe
        self.algo = algo
        self.mode = mode
        self.filetype = (("All Files", "*.*"),)
        self.heading = Label(self.frame,
                             text=(mode + " " + algo),
                             font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"))
        self.heading.pack()
        fileframe = Frame(self.frame)
        self.labelfile = Label(fileframe,
                               text="File not selected",
                               font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"))
        self.labelfile.grid(row=0, column=0)
        self.filebutton = Button(fileframe,
                                 text="Open File",
                                 font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"),
                                 command=lambda: self.selectFiles())
        self.filebutton.grid(row=0, column=1)
        fileframe.pack()
        framekey = Frame(self.frame)
        self.keylabel = Label(framekey,
                              text="Key:",
                              font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"))
        self.keylabel.grid(row=0, column=0)
        self.key = Entry(framekey, width=50)
        self.key.grid(row=0, column=1)
        framekey.pack()
        self.submit = Button(self.frame,
                             text="Submit",
                             font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"),
                             command=self.submit)
        self.submit["state"] = DISABLED
        self.submit.pack()
        imageframe = Frame(self.frame)
        self.image1 = Label(imageframe)
        self.image1.grid(row=0, column=0)
        self.progress = Progressbar(imageframe,
                                    orient=HORIZONTAL,
                                    length=100,
                                    mode='indeterminate')
        self.progress['value'] = 0
        self.frame.update_idletasks()
        self.image2 = Label(imageframe)
        imageframe.pack()
        self.backbutton = Button(self.frame,
                                 text="Back",
                                 font=("COPPERPLATE GOTHIC LIGHT", 16, "bold"),
                                 command=self.destroy)
        self.backbutton.pack()
        currentframe.pack_forget()
        self.frame.pack(fill='both', expand=1)
        self.frame.bind("<Configure>", self.size)

    def size(self, event):
        # print((int(self.frame.winfo_width()*2/3), int(self.frame.winfo_height()*2/3)))
        if self.img1 is not None:
            img = self.img1.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                                   Im.ANTIALIAS)
            image1 = ImageTk.PhotoImage(img)
            self.image1.configure(image=image1)
            self.image1.image = image1
        if self.img2 is not None:
            img = self.img2.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                                   Im.ANTIALIAS)
            image2 = ImageTk.PhotoImage(img)
            self.image2.configure(image=image2)
            self.image2.image = image2

    def destroy(self):
        self.frame.destroy()
        self.currentframe.pack(fill='both', expand=1)

    def selectFiles(self):
        f = filedialog.askopenfilename(initialdir=initDir, title="Select a File", filetypes=self.filetype)
        f = f.split("/")
        self.filename = "\\".join(f)
        self.labelfile.configure(text="File Opened: " + self.filename)
        if self.filename != "" and self.filename != "File not selected":
            self.submit["state"] = ACTIVE

    def threadprogress(self):
        while self.a.progress < 100:
            # print(self.a.progress)
            time.sleep(0.01)
            self.progress['value'] = self.a.progress
            self.frame.update_idletasks()

    def threadcrypto(self):
        self.submit["state"] = DISABLED
        self.filebutton["state"] = DISABLED
        self.backbutton["state"] = DISABLED
        self.img1 = Im.open(self.filename)
        img = self.img1.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                               Im.ANTIALIAS)
        image1 = ImageTk.PhotoImage(img)
        self.image1.configure(image=image1)
        self.image1.image = image1
        if self.algo == "Logistic Chaos Map":
            key = self.key.get()
            if key == "":
                key = "abcdefghijklm"
            if self.mode == "Encrypt":
                LogisticEncryption(self.filename, key)
                self.img2 = Im.open(self.filename.split('.')[0] + "_LogisticEnc.png")
            elif self.mode == "Decrypt":
                LogisticDecryption(self.filename, key)
                self.img2 = Im.open(self.filename.split('_')[0] + "_LogisticDec.png")
        elif self.algo == "Arnold Cat Transform":
            key = self.key.get()
            if key == "":
                key = 20
            else:
                key = int(key)
            self.a = ArnoldCat()
            threading.Thread(target=self.threadprogress).start()
            if self.mode == "Encrypt":
                self.a.ArnoldCatEncryption(self.filename, key)
                self.img2 = Im.open(self.filename.split('.')[0] + "_ArnoldcatEnc.png")
            elif self.mode == "Decrypt":
                self.a.ArnoldCatDecryption(self.filename, key)
                self.img2 = Im.open(self.filename.split('_')[0] + "_ArnoldcatDec.png")
        img = self.img2.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                               Im.ANTIALIAS)
        image2 = ImageTk.PhotoImage(img)
        self.progress.grid_forget()
        self.image2.grid(row=0, column=1)
        self.image2.configure(image=image2)
        self.image2.image = image2
        self.submit["state"] = ACTIVE
        self.filebutton["state"] = ACTIVE
        self.backbutton["state"] = ACTIVE

    def submit(self):
        self.img2 = None
        self.progress.grid(row=0, column=1, padx=10)
        self.image2.grid_forget()
        threading.Thread(target=self.threadcrypto).start()


def getImageMatrix_gray(imageName):
    im = Im.open(imageName).convert('LA')
    pix = im.load()
    image_size = im.size
    image_matrix = []
    for width in range(int(image_size[0])):
        row = []
        for height in range(int(image_size[1])):
            row.append((pix[width, height]))
        image_matrix.append(row)
    return image_matrix, image_size[0]   # , image_size[1]


def plotHis(frame, image, imagename):
    fig = plt.Figure(figsize=(3, 2))
    plot = fig.add_subplot(111)
    img = cv2.imread(image, 1)

    # plotting the graph
    histogram_blue = cv2.calcHist([img], [0], None, [256], [0, 256])
    plot.plot(histogram_blue, color='blue')
    histogram_green = cv2.calcHist([img], [1], None, [256], [0, 256])
    plot.plot(histogram_green, color='green')
    histogram_red = cv2.calcHist([img], [2], None, [256], [0, 256])
    plot.plot(histogram_red, color='red')
    plot.title.set_text(imagename)
    plot.set_xlabel('pixel values')
    plot.set_ylabel('pixel count')

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def plotAdg(frame, image, imagename):
    imagematrix, image_size = getImageMatrix_gray(image)
    samples_x = []
    samples_y = []
    for i in range(1024):
        x = random.randint(0, image_size - 2)
        y = random.randint(0, image_size - 1)
        samples_x.append(imagematrix[x][y])
        samples_y.append(imagematrix[x + 1][y])

    fig = plt.figure(figsize=(3, 2))
    plot = fig.add_subplot(111)
    plot.scatter(samples_x, samples_y, s=2)
    plot.title.set_text(imagename)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


class AnalysisFrame:

    def __init__(self, masterframe, currentframe):
        self.img1 = None
        self.img2 = None
        self.file_orig = "File not selected"
        self.file_enc = "File not selected"
        self.filetype = (("All Files", "*.*"),)
        self.frame = Frame(masterframe)
        self.currentframe = currentframe
        self.heading = Label(self.frame,
                             text="Histogram Analysis and Adjacent Pixel Auto-Correlation",
                             font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"))
        self.heading.pack()

        # scrollbar = Scrollbar(self.frame)
        # scrollbar.pack(side=RIGHT, fill=Y)

        fileframe_orig = Frame(self.frame)
        self.labelfile_orig = Label(fileframe_orig,
                                    text="File not selected",
                                    font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"))
        self.labelfile_orig.grid(row=0, column=0)
        Button(fileframe_orig,
               text="Open File",
               font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"),
               command=lambda: self.selectOrig()).grid(row=0, column=1)
        fileframe_orig.pack()

        fileframe_enc = Frame(self.frame)
        self.labelfile_enc = Label(fileframe_enc,
                                   text="File not selected",
                                   font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"))
        self.labelfile_enc.grid(row=0, column=0)
        Button(fileframe_enc,
               text="Open File",
               font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"),
               command=lambda: self.selectEnc()).grid(row=0, column=1)
        fileframe_enc.pack()

        self.submit = Button(self.frame,
                             text="Submit",
                             font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"),
                             command=self.submit)
        self.submit["state"] = DISABLED
        self.submit.pack()

        imageframe = Frame(self.frame)
        self.image1 = Label(imageframe)
        self.image1.grid(row=0, column=0)
        self.image2 = Label(imageframe)
        self.image2.grid(row=0, column=1)
        imageframe.pack()

        analysisframe = Frame(self.frame)

        self.imageframe1 = Frame(analysisframe)
        Label(self.imageframe1,
              text="Histogram Analysis",
              font=("COPPERPLATE GOTHIC LIGHT", 12, "bold")).grid(row=0)
        self.plot1 = Frame(self.imageframe1)
        self.plot1.grid(row=1, column=0)
        self.plot2 = Frame(self.imageframe1)
        self.plot2.grid(row=1, column=1)
        self.imageframe1.pack()

        self.imageframe2 = Frame(analysisframe)
        Label(self.imageframe2,
              text="Adjacent Pixel Auto-Correlation",
              font=("COPPERPLATE GOTHIC LIGHT", 12, "bold")).grid(row=0)
        self.plot3 = Frame(self.imageframe2)
        self.plot3.grid(row=1, column=0)
        self.plot4 = Frame(self.imageframe2)
        self.plot4.grid(row=1, column=1)

        analysisframe.pack()

        swapbuttonframe = Frame(self.frame)
        self.hisbutton = Button(swapbuttonframe,
                                text="Histogram Analysis",
                                font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"),
                                command=self.hisframe)
        self.hisbutton.grid(row=0, column=0)
        self.hisbutton["state"] = DISABLED
        self.adjbutton = Button(swapbuttonframe,
                                text="Adjacent Pixel Auto-Correlation",
                                font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"),
                                command=self.adjframe)
        self.adjbutton.grid(row=0, column=1)
        swapbuttonframe.pack()

        Button(self.frame, text="Back", font=("COPPERPLATE GOTHIC LIGHT", 12, "bold"), command=self.destroy).pack()
        currentframe.pack_forget()
        self.frame.pack(fill='both', expand=1)
        self.frame.bind("<Configure>", self.size)

    def size(self, event):
        # print((int(self.frame.winfo_width()*2/3), int(self.frame.winfo_height()*2/3)))
        if self.img1 is not None:
            img = self.img1.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                                   Im.ANTIALIAS)
            image1 = ImageTk.PhotoImage(img)
            self.image1.configure(image=image1)
            self.image1.image = image1
        if self.img2 is not None:
            img = self.img2.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                                   Im.ANTIALIAS)
            image2 = ImageTk.PhotoImage(img)
            self.image2.configure(image=image2)
            self.image2.image = image2

    def hisframe(self):
        self.imageframe1.pack(fill='both', expand=1)
        self.imageframe2.pack_forget()
        self.hisbutton["state"] = DISABLED
        self.adjbutton["state"] = ACTIVE

    def adjframe(self):
        self.imageframe1.pack_forget()
        self.imageframe2.pack(fill='both', expand=1)
        self.hisbutton["state"] = ACTIVE
        self.adjbutton["state"] = DISABLED

    def destroy(self):
        self.frame.destroy()
        self.currentframe.pack(fill='both', expand=1)

    def selectOrig(self):
        f = filedialog.askopenfilename(initialdir=initDir, title="Select Original Image", filetypes=self.filetype)
        f = f.split("/")
        self.file_orig = "\\".join(f)
        self.labelfile_orig.configure(text="File Opened: " + self.file_orig)
        self.submit["state"] = ACTIVE
        if self.file_orig == "" or self.file_orig == "File not selected":
            self.submit["state"] = DISABLED
        if self.file_enc == "" or self.file_enc == "File not selected":
            self.submit["state"] = DISABLED

    def selectEnc(self):
        f = filedialog.askopenfilename(initialdir=initDir, title="Select Encrypted Image", filetypes=self.filetype)
        f = f.split("/")
        self.file_enc = "\\".join(f)
        self.labelfile_enc.configure(text="File Opened: " + self.file_enc)
        self.submit["state"] = ACTIVE
        if self.file_enc == "" or self.file_enc == "File not selected":
            self.submit["state"] = DISABLED
        if self.file_orig == "" or self.file_orig == "File not selected":
            self.submit["state"] = DISABLED

    def submit(self):
        # self.file_orig = "D:\\EncryptIt\\orig.png"
        # self.file_enc = "D:\\EncryptIt\\orig_ArnoldcatEnc.png"
        self.img1 = Im.open(self.file_orig)
        img = self.img1.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                               Im.ANTIALIAS)
        image1 = ImageTk.PhotoImage(img)
        self.image1.configure(image=image1)
        self.image1.image = image1

        self.img2 = Im.open(self.file_enc)
        img = self.img2.resize((int(self.frame.winfo_width() * scale_w), int(self.frame.winfo_height() * scale_h)),
                               Im.ANTIALIAS)
        image2 = ImageTk.PhotoImage(img)
        self.image2.configure(image=image2)
        self.image2.image = image2

        plotHis(self.plot1, self.file_orig, "Original Image")
        plotHis(self.plot2, self.file_enc, "Encrypted Image")

        plotAdg(self.plot3, self.file_orig, "Original Image")
        plotAdg(self.plot4, self.file_enc, "Encrypted Image")

