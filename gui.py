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

        self.frameMenu = tk.Frame(self.root)
        self.frameMenu.grid(row=0, column=0)
        self.framePres = tk.Frame(self.root)
        self.framePres.grid(row=0, column=1)

        self.listbox = tk.Listbox(self.frameMenu)
        self.listbox.pack()

        self.listeWidgets = []
        self.listeProduct = []

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
                    self.listeWidgets[int(activeItem[0]) - 1][0].grid(row=0, column=0)
                    self.listeWidgets[int(activeItem[0]) - 1][1].grid(row=0, column=1)
                    self.listeWidgets[int(activeItem[0]) - 1][2].grid(row=1, column=1)
                    for elt in [i for i in self.listeWidgets if i != self.listeWidgets[int(activeItem[0]) - 1]]:
                        elt[0].grid_forget()
                        elt[1].grid_forget()
                        elt[2].grid_forget()
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
        imageUrl = requests.get(resp.json()["product"]["image_front_small_url"])
        img = ImageTk.PhotoImage(Image.open(BytesIO(imageUrl.content)))
        presIcon = tk.Label(self.framePres, image=img)
        presIcon.grid_forget()
        presBrand = tk.Label(self.framePres, text = req.json()["product"]["brands"])
        presBrand.grid_forget()
        productName = req.json()["product"]["product_name"]
        presProduct = tk.Label(self.framePres, text = productName)
        presProduct.grid_forget()
        self.listeWidgets.append([presIcon, presBrand, presProduct])
        self.listbox.insert(tk.END, str(self.listeProduct.__len__()) + " " + productName)
