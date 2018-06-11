from pyzbar import pyzbar
import numpy as np
import cv2
import requests
from pprint import pprint


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
            product = resp.json()["product"]["brands"]
            cv2.putText(frame,
                        decode[0].type + ", "
                        + decode[0].data.decode() + ", "
                        + product,
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2)

            cv2.putText(frame,
                        resp.json()["product"]["product_name"],
                        (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2)

        elif resp.json()["status"] == 0:
            print("product not in db")

        pprint(resp.json())

        cap.release()
        cv2.imshow("result", frame)
        cv2.waitKey(0)
        break

    cv2.imshow("cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
