from PIL import Image, ImageFont, ImageDraw
from random import *
import numpy as np
import cv2
from test import read_digits


def postprocess(string):
    ans = string.replace(' ', '')
    for ind in range(2000):
        if chr(ind).isdigit():
            continue
        ans = ans.replace(chr(ind), '')
    return ans


def create_im():
    font = ImageFont.truetype("arial.ttf", 200)
    delta = 10
    img = Image.open('фон.png')
    draw = ImageDraw.Draw(img)
    x, y = randrange(20, 150), randrange(20, 60)
    value = randint(1000000000, 9999999999)
    draw.text((x, y), str(value), (145, 60, 70), font=font)
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r += randint(-delta, delta)
            g += randint(-delta, delta)
            b += randint(-delta, delta)
            img.putpixel((i, j), (r, g, b))
    img = img.resize((85, 30), Image.ANTIALIAS)
    img.save('test.jpg')
    return value


def eval_digits(times):
    for i in range(times):
        value = create_im()
        cv_im = Image.open('test.jpg')
        total, good = 0, 0
        if value == int(postprocess(read_digits(np.asarray(cv_im)))):
            good += 1
            total += 1
        else:
            total += 1
    return good / total


print(postprocess(read_digits(np.asarray(Image.open('digit dataset/d0/2000701187.png')))))