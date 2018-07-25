import os
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import time
import datetime
import imutils
import cv2
from pyzbar import pyzbar
import requests
from io import BytesIO
import unicodedata


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
        self.listbox.insert(tk.END, "  Put barcodes in front of the webcam to add elements...")
        self.frameCount = tk.Frame(self.frameMenu)
        self.frameCount.pack()
        self.countInt = 0
        self.countStr = tk.StringVar()
        self.labelCountDesc = tk.Label(self.frameCount, text="Elements in the list:")
        self.labelCountDesc.grid(row=0, column=0)
        self.labelCount = tk.Label(self.frameCount, textvariable=self.countStr)
        self.labelCount.grid(row=0, column=1)
        self.countStr.set(str(self.countInt))
        self.buttonExport = tk.Button(self.frameMenu, text="Export to HTML", command=self.export)
        self.buttonExport.pack(pady=10)

        self.monsantoInside = ['Alvalle', 'Aunt Jemima', 'Aurora Foods', 'Banquet', "Ben & Jerry's", 'Benenuts', 'Best Foods', 'Betty Crocker', 'Bisquick', 'Bounty', 'Brossard', 'Burn', 'Cadbury', 'Campbell', 'Campbells', 'Capri Sun', 'Capri-Sun', 'Carambar', 'Carnation', 'Carte Noir', 'Chef Boyardee', 'Cherry Coke', 'Coca Cola', 'Coca-Cola', 'ConAgra', "Côte d'Or", 'Daim', 'Delicious Brand Cookies', 'Doritos', 'Dr Pepper', 'Duncan Hines', 'Famous Amos', 'Fanta', 'Findus', 'Frito Lay', 'Gamble', 'Gatorade', 'General Mills', 'Gloria', 'Green Giant', 'Géant Vert', 'Haagen Dazs', 'Healthy Choice', 'Heinz', 'Hellman', "Hershey's Nestle", 'Hollywood', 'Holsum', 'Hormel', 'Hungry Jack', 'Hunts', 'Interstate Bakeries', 'Jacquet', 'Jiffy', 'KC Masterpiece', 'Keebler/Flowers Industries', "Kellog's", 'Kelloggs', 'Kid Cuisine', 'Knorr', 'Kool-Aid', 'Kraft Philipp Morris', 'Kraft/Phillip Morris', 'Krema', 'La Vosgienne', "Lay's", 'Lean Cuisine', 'Liebig', 'Lipton', 'Lipton Ice Tea', 'Loma Linda', 'Lu', 'Malabar', 'Marie', 'Marie Callenders', 'Maxwell', 'Miko', 'Milka', 'Minute Made', 'Minute Maid', 'Morningstar', 'Ms.Butterworths', 'Nabisco', 'Nature Valley', 'Ocean Spray', 'Old el Paso', 'Ore-Ida', 'Oreo', 'Orville Redenbacher', 'Pampers', 'Pasta-Roni', 'Pepperidge Farms', 'Pepsi', 'Pepsi-Cola', 'Pepsico', 'Philadelphia', 'Pillsbury', 'Pop Secret', 'Post Cereals', 'Poulain', 'Power Bar Brand', 'Prego Pasta Sauce', 'Pringles', 'Procter', 'Procter and Gamble', 'Quaker', 'Quakers', 'Ragu Sauce', 'Rice-A-Roni', 'Royco', 'Ruffles', "Régal'ad", 'Savane', 'Schweppes', 'Seven Up', 'Smart Ones', 'Stouffers', 'Suchard', 'Sweppes', 'Tang', 'Tipiak', 'Toblerone', 'Tombstone Pizza', 'Tostitos', 'Totinos', 'Tropicana', "Uncle Ben's", 'Unilever', 'V8', 'Yoplait']

        self.listeWidgets = []
        self.listeItems = []
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
                if decode != [] and decode[0].data.decode().__len__() == 13:
                    print("[INFO] Product detected:", decode[0].data.decode())
                    if decode[0].data.decode() not in self.listeProduct:
                        self.add_item(decode[0].data.decode())
                    else:
                        print("[INFO] Product already in list.")

                activeItem = self.listbox.get(tk.ACTIVE)
                if activeItem != str():
                    if activeItem != self.activeItem:
                        self.listeWidgets[int(activeItem.split(" ")[0]) - 1][0].pack()
                        self.listeWidgets[int(activeItem.split(" ")[0]) - 1][1].pack()
                        self.listeWidgets[int(activeItem.split(" ")[0]) - 1][2].pack()
                        for elt in [i for i in self.listeWidgets if i != self.listeWidgets[int(activeItem.split(" ")[0]) - 1]]:
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
        try:
            if self.countInt == 0:
                self.listbox.delete(tk.END)
            listeImagesPot = ["image_small_url", "image_front_small_url", "image_url", "image_front_url"]
            self.listbox.insert(tk.END, "  Adding item...")
            resp = requests.get("https://fr.openfoodfacts.org/api/v0/produit/" + data + ".json")
            for elt in list({u for u, v in resp.json()["product"].items() if u[:5] == "image" and "small" in u}):
                listeImagesPot.append(elt)
            listeImagesPot = list(dict.fromkeys(listeImagesPot))
            stop, ind  = False, 0
            while not stop:
                try:
                    url = resp.json()["product"][listeImagesPot[ind]]
                    imageUrl = requests.get(url)
                    img = Image.open(BytesIO(imageUrl.content))
                    img.thumbnail((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)
                    stop = True
                except KeyError:
                    ind += 1

            self.listePhoto.append(img)
            presIcon = tk.Label(self.framePresLeft, image=img)
            presIcon.pack_forget()
            brandName = resp.json()["product"]["brands"]
            presBrand = tk.Label(self.framePresRight, text = brandName)
            presBrand.pack_forget()
            productName = resp.json()["product"]["product_name"]
            presProduct = tk.Label(self.framePresRight, text = productName)
            presProduct.pack_forget()
            self.listeItems.append([url, brandName, productName, ", ".join([i["text"] for i in resp.json()["product"]["ingredients"]])])
            self.listeWidgets.append([presIcon, presBrand, presProduct])
            self.listbox.delete(tk.END)
            self.listbox.insert(tk.END, str(self.listeProduct.__len__() + 1) + " " + productName)
            self.listeProduct.append(data)
            self.listbox.select_clear(0, self.listbox.size() - 1)
            self.listbox.select_set(self.listbox.size() - 1)
            self.listbox.activate(self.listbox.size() - 1)
            self.countInt += 1
            self.countStr.set(str(self.countInt))
            print("[INFO] Product added")

        except KeyError:
            print("[INFO] Error in product detection")
            print("[INFO] Product not added")
            if self.listbox.get(tk.END) == "  Adding item...":
                self.listbox.delete(tk.END)

    def export(self):
        htmlPage = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Food Scan Result</title>
        </head>
        <body>
            <style type="text/css">
                {css}
            </style>
            <h1>Food Scan Results:</h1>
            <table>
                {table}
            </table>
        </body>
        </html>
        '''
        table = ""
        for elt in self.listeItems:
            if self.monsantoInsideFunc(elt[1]):
                table += "<tbody><tr style='background-color: red'><td><img src='" + elt[0] + "'></td><td>" + elt[1] + "</td><td>" + elt[2] + "</td><td>" + elt[3] + "</td><td><img src='../monsantoInside.png'></td></tr></tbody>"
            else:
                table += "<tbody><tr><td><img src='" + elt[0] + "'></td><td>" + elt[1] + "</td><td>" + elt[2] + "</td><td>" + elt[3] + "</td><td></td></tr></tbody>"

        timeNow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        outputFile = "output" + timeNow + ".html"
        os.makedirs("scan-" + timeNow)
        os.chdir("scan-" + timeNow)
        with open(outputFile, "w") as f:
            for elt in htmlPage.format(table=table, css="table {border-collapse: collapse;} table, th, td {border: 1px solid black;} th, td {padding: 15px; text-align: left;} tr:hover {background-color:#dcdde1;}").splitlines():
                f.write(elt)
        print("[INFO] File has been created: " + outputFile)

    def monsantoInsideFunc(self, brand):
        if unicodedata.normalize("NFD", brand).encode('ascii', 'ignore').decode("utf-8").lower() in [i.lower() for i in self.monsantoInside]:
            return True
        return False
