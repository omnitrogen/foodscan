# Foodscan :boom: :banana:

This program scan a barcode, and send back infos about the product (focusing on food product here).

You can then export a report of all the products scanned in html format. You will see if the product's brand is using any Monsanto product.

>The program uses:
>  - OpenCV (for the camera)
>  - Zbar (to decode barcodes)
>  - [Open Food Facts API](https://fr.openfoodfacts.org/data) (to get infos about food products)


## Installing dependencies:

1) Install Zbar with yout favorite package manager:
  - ```brew install zbar``` (macOS)
  - ```sudo apt-get install libzbar-dev libzbar0``` (ubuntu)
 
2) Install python modules:
  - ```pip install -r requirements.txt``` (might be pip3 depending on your pip install)
  
## Launch:

  - ```python3 main.py```
 
Have fun! :rainbow:
