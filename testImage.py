import tkinter as tk
from PIL import Image
from PIL import ImageTk
import requests
from io import BytesIO

app = tk.Tk()

# https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.100.jpg
imageUrl = requests.get("https://static.openfoodfacts.org/images/products/326/385/059/6513/front_fr.4.400.jpg")
img = ImageTk.PhotoImage(Image.open(BytesIO(imageUrl.content)))
panel = tk.Label(app, image=img)
panel.pack()


listebox = tk.Entry(app, width=100)
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
