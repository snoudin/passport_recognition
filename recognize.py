import pytesseract, cv2
import numpy as np
from PIL import Image


def get_text(name):
    img = cv2.imread(name)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 120
    line = ''
    while 1:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers).lstrip('\n\t ').rstrip('\n\t ')[:12]
        if len(line) < 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return line
