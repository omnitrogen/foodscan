import os
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
from pyzbar import pyzbar
import requests
from io import BytesIO


class GuiApp:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = tk.Tk()
        self.frameGlobal = tk.Frame(self.root)
        self.frameGlobal.pack()
        self.frameMenu = tk.Frame(self.frameGlobal)
        self.frameMenu.grid(row=0, column=0)
        self.framePres = tk.Frame(self.frameGlobal)
        self.framePres.grid(row=0, column=1)
        self.framePresLeft = tk.Frame(self.framePres)
        self.framePresLeft.grid(row=0, column=0)
        self.framePresRight = tk.Frame(self.framePres)
        self.framePresRight.grid(row=0, column=1)
        self.listbox = tk.Listbox(self.frameMenu, width=50)
        self.listbox.pack()

        self.listeWidgets = []
        self.listeProduct = []
        self.listePhoto = []
        self.activeItem = str()

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("Food Scan")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()

                decode = pyzbar.decode(self.frame)
                if decode != []:
                    print("[INFO] Product detected")
                    if decode[0].data.decode() not in self.listeProduct:
                        self.add_item(decode[0].data.decode())
                        print("[INFO] Product added")
                    else:
                        print("[INFO] Product already in list.")

                activeItem = self.listbox.get(tk.ACTIVE)
                if activeItem != str():
                    if activeItem != self.activeItem:
                        self.listeWidgets[int(activeItem[0]) - 1][0].pack()
                        self.listeWidgets[int(activeItem[0]) - 1][1].pack()
                        self.listeWidgets[int(activeItem[0]) - 1][2].pack()
                        for elt in [i for i in self.listeWidgets if i != self.listeWidgets[int(activeItem[0]) - 1]]:
                            elt[0].pack_forget()
                            elt[1].pack_forget()
                            elt[2].pack_forget()
                        self.activeItem = activeItem

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

    def add_item(self, data):
        self.listeProduct.append(data)
        resp = requests.get("https://fr.openfoodfacts.org/api/v0/produit/" + data + ".json")
        imageUrl = requests.get(resp.json()["product"]["image_thumb_url"])
        img = ImageTk.PhotoImage(Image.open(BytesIO(imageUrl.content)))
        self.listePhoto.append(img)
        presIcon = tk.Label(self.framePresLeft, image=img)
        presIcon.pack_forget()
        presBrand = tk.Label(self.framePresRight, text = resp.json()["product"]["brands"])
        presBrand.pack_forget()
        productName = resp.json()["product"]["product_name"]
        presProduct = tk.Label(self.framePresRight, text = productName)
        presProduct.pack_forget()
        self.listeWidgets.append([presIcon, presBrand, presProduct])
        self.listbox.insert(tk.END, str(self.listeProduct.__len__()) + " " + productName)
