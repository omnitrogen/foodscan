from pyzbar import pyzbar
import numpy as np
import cv2
import requests
from pprint import pprint
from PIL import ImageFont, ImageDraw, Image


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    decode = pyzbar.decode(frame)
    if decode != []:

        print("object detected")

        for obj in decode:
            points = obj.polygon
            n = len(points)
            for j in range(n):
                cv2.line(frame, points[j], points[(j+1) % n], (255, 0, 0), 3)

        resp = requests.get("https://fr.openfoodfacts.org/api/v0/produit/"
                            + decode[0].data.decode()
                            + ".json")

        if resp.json()["status"] == 1:
            product = resp.json()["product"]["brands"]

            font = ImageFont.truetype("mononoki.ttf", 30)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((10, 40),  decode[0].type + ", " + decode[0].data.decode() + ", " + product, font = font, fill = (255, 0, 0, 0))
            draw.text((10, 80),  resp.json()["product"]["product_name"], font = font, fill = (255, 0, 0, 0))
            img = np.array(img_pil)

            cap.release()
            cv2.imshow("result", img)
            cv2.waitKey(0)
            pprint(resp.json())
            break

        elif resp.json()["status"] == 0:
            font = ImageFont.truetype("mononoki.ttf", 30)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((10, 40),  "product not in db", font = font, fill = (0, 0, 255, 0))
            img = np.array(img_pil)

            cap.release()
            cv2.imshow("error", img)
            cv2.waitKey(0)
            pprint(resp.json())
            break

    cv2.imshow("cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
