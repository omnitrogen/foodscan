import tkinter as tk
from PIL import Image
from PIL import ImageTk
import requests
from io import BytesIO


def add_item():
    pass

app = tk.Tk()

listeItems = []

frameMenu = tk.Frame(app)
frameMenu.grid(row=0, column=0)
framePres = tk.Frame(app)
framePres.grid(row=0, column=1)

# https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.100.jpg
imageUrl = requests.get("https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.400.jpg")
img = ImageTk.PhotoImage(Image.open(BytesIO(imageUrl.content)))
panel = tk.Label(framePres, image=img)
panel.pack()
imageUrl2 = requests.get("https://static.openfoodfacts.org/images/products/326/385/059/6513/ingredients_fr.9.200.jpg")
img2 = ImageTk.PhotoImage(Image.open(BytesIO(imageUrl2.content)))
panel2 = tk.Label(framePres, image=img2)
panel2.pack()

listebox = tk.Listbox(frameMenu)
listebox.pack()

req = requests.get("https://fr.openfoodfacts.org/api/v0/produit/3263850596513.json")
brand = req.json()["product"]["brands"]
product = req.json()["product"]["product_name"]

listebox.insert(tk.END, brand + " ")
listebox.insert(tk.END, product)
app.mainloop()

'''
Product specs:
["product"]["brands"]
["product"]["product_name"]

Product pics:
'image_front_small_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.200.jpg',
'image_front_thumb_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.100.jpg',
'image_front_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.400.jpg',
'image_ingredients_small_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/ingredients_fr.9.200.jpg',
'image_ingredients_thumb_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/ingredients_fr.9.100.jpg',
'image_ingredients_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/ingredients_fr.9.400.jpg',
'image_small_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.200.jpg',
'image_thumb_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.100.jpg',
'image_url': 'https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.400.jpg',

'''
