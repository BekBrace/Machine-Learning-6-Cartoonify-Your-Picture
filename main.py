#importing the modules
import cv2
import easygui
import numpy as np
import imageio
import matplotlib.pyplot as plt

import sys
import os

from tkinter import *
import tkinter as tk

from PIL import ImageTk, Image
#////////////////////////////////

window = tk.Tk()
window.geometry("400x400")
window.title('Cartoonify Your Image App - Tkinter')
window.configure(background="white")



# for uploading the image from your computer [ easygui to be used ]
def upload():
    imagePath = easygui.fileopenbox()
    cartoonify(imagePath)



# for the actual processing on the image
def cartoonify(imagePath):

    #1 initial image that we want to cartoonify
    initialImage = cv2.imread(imagePath)
    initialImage = cv2.cvtColor(initialImage, cv2.COLOR_BGR2RGB)
    
    #condition to check the existence of the image file
    if initialImage is None:
        print('Can not find any images. Please choose appropriate file.')
        sys.extit()

    resized1 = cv2.resize(initialImage, (960, 540))

    #2 Gray Image
    grayImage = cv2.cvtColor(initialImage, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(grayImage, (960, 540))
    
    #3 Smooth Gray Image 
    smoothGrayImage = cv2.medianBlur(grayImage, 5)
    resized3 = cv2.resize(smoothGrayImage, (960, 540))

    #4 Sketchy image
    edge = cv2.adaptiveThreshold(smoothGrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    resized4 = cv2.resize(edge, (960, 540))

    #5 Colored inital without noise - sharp edges
    coloredImage = cv2.bilateralFilter(initialImage, 9, 300, 300)
    resized5 = cv2.resize(coloredImage, (960, 540))

    #6 Cartoon Image
    cartoonImage = cv2.bitwise_and(coloredImage, coloredImage, mask=edge)
    resized6 = cv2.resize(cartoonImage, (960, 540))

    images = [resized1, resized2, resized3, resized4, resized5, resized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for index, axe in enumerate(axes.flat):
        axe.imshow(images[index], cmap='gray')
    
    #Create the save button
    saveButton = Button(window, text="Save Image", command=lambda: save(resized6, imagePath),padx=30, pady=5)
    saveButton.configure(background="#364156", foreground="white", font=("Calibri", 10, 'bold')) 
    saveButton.pack(side=TOP, pady=50)

    plt.show()

#Saving function
def save(resized6, imagePath):
    newName = "Cartoonified_image"
    path0 = os.path.dirname(imagePath)
    extension = os.path.splitext(imagePath)[1]
    path1 = os.path.join(path0, newName+extension)
    cv2.imwrite(path1, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
    message = "Image saved by name: " + newName + "at" + path1
    tk.messagebox.showinfo(title=None, message=message )


upload = Button(window, text="Upload Image To Cartoonify", command = upload, padx=10, pady=5)
upload.configure(background='#364156',foreground='white', font=("Calibri", 10, 'bold'))
upload.pack(side=TOP, pady=50)


window.mainloop()