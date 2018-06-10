from pyzbar import pyzbar
import numpy as np
import cv2
import requests


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    decode = pyzbar.decode(frame)
    if decode != []:

        for obj in decode:
            points = obj.polygon
            n = len(points)
            for j in range(n):
                cv2.line(frame, points[j], points[(j+1) % n], (255, 0, 0), 3)
        resp = requests.get("https://fr.openfoodfacts.org/api/v0/produit/"
                            + decode[0].data.decode()
                            + ".json")
        if resp.json()["status"] == 1:
            product = resp.json()["product"]["product_name"]
        elif resp.json()["status"] == 0:
            product = "product not in db"
        else:
            product = "no internet connection"

        cv2.putText(frame,
                    decode[0].type.decode() + ", "
                    + decode[0].data.decode() + ", "
                    + product,
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2)
        cap.release()
        cv2.imshow("result", frame)
        cv2.waitKey(0)
        break

    cv2.imshow("cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()
