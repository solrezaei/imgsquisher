from sys import exit
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os

dirpath = ""

def jippify(img=Image, new_name=str):
  # halves both dimensions and the quality
  # converts to jpg

  img = img.convert('RGB')
  w, h = img.size
  new_size = (w//2, h//2)
  new_img = img.resize(new_size)
  new_img.save(new_name + '.jpg', optimize=True, quality=50)

def jipperate(root, ext=['.jpg', '.jpeg', '.png'], purge=False, dive=False):
  # jippifies all files with extensions in ext in folder and children
  # root is full path to the directory to jippify
  # ignores files starting with i_
  # purge deletes original files after compression
  
  if root in ["", ()]: 
    statusDisplayVar.set("status: no directory chosen!")
    return
  
  statusDisplayVar.set("status: starting up compression in %s..." % root)
  
  if purge: 
    i = input('purge is turned on. this will OBLITERATE EVERYTHING. continue? y/n: ')
    if i != 'y': 
      print('jipperation cancelled')
      return
  
  if not dive: 
    for f in os.listdir(root): 
        name, extension = os.path.splitext(f)
        if extension not in ext or name[:2] in ['c_','i_']: 
        	continue
        
        statusDisplayVar.set("status: compressing %s" % f)
        
        img = Image.open(os.path.join(root, f))
        jippify(img, os.path.join(root, 'c_' + name))
        
        if purge: 
          os.remove(os.path.join(root, f))
  else:
    for subdir, dirs, files in os.walk(root):
      for f in files: 
        name, extension = os.path.splitext(f)
        if extension not in ext or name[:2] in ['c_','i_']: 
        	continue
        
        statusDisplayVar.set("status: compressing %s" % os.path.join(subdir, f)[len(root):])
        
        img = Image.open(os.path.join(subdir, f))
        jippify(img, os.path.join(subdir, 'c_' + name))
        
        if purge: 
          os.remove(os.path.join(subdir, f))
  
  statusDisplayVar.set("status: finished processing!")

# GUI FUNCTIONS

def info():
  infowin = tk.Tk()
  infowin.title("Squisher Info")
  infowin.resizable(0,0)
  
  infoDisp = tk.Label(infowin, text = "this compressor by default goes into the given folder and walks through every subdirectory, subsubdirectory etc. to compress the images. if you only want to compress the chosen directory and no subdirs, you can uncheck the \"dive\" checkbox. \n\nduring compression, the compressed images are by default saved as \"c_\" prepended to the original filename. if the compressor finds an image with a filename starting with this tag, it ignores it so as to prevent recursion. if you happen to have images in your folder that you don't want to compress at all, prepend the characters \"i_\" to the filenames so the compressor skips them. \n\nnormally the compressor keeps the original image, but if for whatever reason you want to delete the original and only keep the compressed image, tick the \"purge\" checkbox. be sure you know what you're doing when using this option! \n\nnote: atm this program can only convert .jpg, .jpeg and .png. if you need support for more formats, email/message me", wraplength = 250, justify = tk.LEFT)
  infoDisp.grid(row = 0, column = 0, padx = 12, pady = 12)
  
  creditDisp = tk.Label(infowin, text = "\nmade by Luna Rezaei Ghavamabadi\n2023", wraplength = 250)
  creditDisp.grid(row = 1, column = 0, padx = 12, pady = 12)
  
  infowin.mainloop()
  

def dirpathUpdate(): 
  global dirpath
  temp = dirpath
  dirpath = askdirectory()
  if dirpath in ["", ()]: 
    dirpath = temp
  
  dirpathDisplayVar.set("current directory: " + dirpath)
  statusDisplayVar.set("status: ready to compress")

# GUI
window = tk.Tk()
window.title("Luna's Image Squisher")
window.resizable(0,0)

mainframe = tk.Frame(window)#, style="windowframes.TFrame")
mainframe.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S, padx = 12, pady = 12)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

purgeChoiceVar = tk.BooleanVar()
purgeChoiceVar.set(False)
diveChoiceVar = tk.BooleanVar()
diveChoiceVar.set(True)

# TITLE BAR
displayTitle = tk.Label(mainframe, text = "WELCOME TO MY IMAGE SQUISHER")
displayTitle.grid(row=0,column=0, columnspan=3, rowspan=2, padx = 12)

exitButton = tk.Button(mainframe, text = "exit", command = exit)#window.destroy)
exitButton.grid(row = 0, column = 3, sticky = tk.E)

infoButton = tk.Button(mainframe, text = "info", command = info)
infoButton.grid(row = 1, column = 3, sticky = tk.E)

# EXPLANATION
explText = "hi!!! this is a lil application that compresses all images in a folder. the way it works is that it takes the image, makes it 4 times smaller, and converts it to jpg with 50% quality. the compressed image is often at least an order of magnitude smaller than the original. NOTE: please take a moment to read the info before starting up the squisher, so you know what it does exactly :)"

explDisplay = tk.Label(mainframe, text = explText, wraplength=300, justify = tk.LEFT)
explDisplay.grid(row=2, column=0, columnspan = 3, sticky=tk.W, pady=12)

# DIRECTORY INPUT
dirButton = tk.Button(mainframe, text = "change directory", command = dirpathUpdate)
dirButton.grid(row = 3, column = 0, sticky = tk.W)

dirpathDisplayVar = tk.StringVar()
dirpathDisplayVar.set("no directory chosen")
displayDir = tk.Label(mainframe, textvariable=dirpathDisplayVar, wraplength = 300, justify = tk.LEFT)
displayDir.grid(row = 4, column = 0, sticky = tk.W, columnspan = 3)

# COMPRESS
compButton = tk.Button(mainframe, text = "SQUISH!", command = lambda: jipperate(dirpath, purge=purgeChoiceVar.get(), dive=diveChoiceVar.get()), bg="#262626", activebackground="#c4c2c4", fg="white")
compButton.grid(row = 3, column = 2, sticky = tk.E)

# STATUS
statusDisplayVar = tk.StringVar()
statusDisplayVar.set("status: not processing")
statusDisplay = tk.Label(mainframe, textvariable = statusDisplayVar, wraplength = 300, bg="#f5f5f5")
statusDisplay.grid(row = 5, column = 0, columnspan = 3)

# OPTIONS 

purgeButton = tk.Checkbutton(mainframe, text="purge", variable=purgeChoiceVar, fg="red", activeforeground="red")
purgeButton.grid(row = 4, column = 3, sticky = tk.W)

diveButton = tk.Checkbutton(mainframe, text="dive", variable=diveChoiceVar)
diveButton.grid(row = 3, column = 3, sticky = tk.W)


window.mainloop()
