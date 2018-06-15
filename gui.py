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



class GuiApp:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = tk.Tk()
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

        self.listeProduits = []

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
                    if decode[0].data.decode() not in self.listeProduits:
                        resp = requests.get("https://fr.openfoodfacts.org/api/v0/produit/"
                                            + decode[0].data.decode()
                                            + ".json")
                        texte = resp.json()["product"]["brands"]
                        + resp.json()["product"]["product_name"]
                        self.listbox.insert(tk.END, texte)
                    else:
                        print("[INFO] Product already in list.")

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
