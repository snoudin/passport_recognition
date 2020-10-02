import pytesseract, cv2
from PIL import Image


def get_snum(name):
    img = cv2.imread(name)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 150
    line = ''
    while 1:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers).lstrip('\n\t ').rstrip('\n\t ')[:12]
        if len(line) > 40 or len(line) < 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return line


def get_recieved_in(name):
    img = cv2.imread(name)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 160
    line = ''
    while 1:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        place = Image.open('bw.png')
        line = pytesseract.image_to_string(place, lang='rus')
        if 'ОТДЕЛ' not in line:
            val += 3
        else:
            break
    while not line.startswith('ОТДЕЛ'):
        line.pop(0)
    return line.lstrip('\n\t ').rstrip('\n\t ')


def more_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def get_surname(name):
    img = cv2.imread(name, 1)
    img = more_contrast(img)
    img = cv2.imread(name)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im_bw = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("bw.png", im_bw)
    surname = Image.open('bw.png')
    line = pytesseract.image_to_string(surname, lang='rus')
    return line.lstrip('\n\t ').rstrip('\n\t ')
