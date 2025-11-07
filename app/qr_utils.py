import cv2
import numpy as np
from pyzbar.pyzbar import decode

def decode_qr(file):
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    decoded_objects = decode(img)

    if not decoded_objects:
        return ""
    return decoded_objects[0].data.decode("utf-8")
