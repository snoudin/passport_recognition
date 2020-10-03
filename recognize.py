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
    return tuple([line[:2] + line[3:5], line[6:]])


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
        line = line[1:]
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('  ', ' ')
    return line.lstrip(',.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip(',.:;@#!?[]{}_+= \n\t\x0c^*()|\\/')


def more_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def get_name(name):
    img = cv2.imread(name, 1)
    img = more_contrast(img)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 90
    line = ''
    while len(line) < 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        surname = Image.open('bw.png')
        line = pytesseract.image_to_string(surname, lang='rus')
        while line != '' and (line[0] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[0]) > 1200 or line[0].islower()):
            line = line[1:]
        while line != '' and (line[-1] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[-1]) > 1200 or line[-1].islower()):
            line = line[:-1]
        val += 3
        if line == '':
            val += 7
    return line


def get_gender(name):
    img = cv2.imread(name, 1)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 90
    line = ''
    while line not in ['МУЖ.', 'ЖЕН.']:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        gender = Image.open('bw.png')
        line = pytesseract.image_to_string(gender, lang='rus').lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return line


def get_date(name):
    img = cv2.imread(name)
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 150
    line = ''
    while 1:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers).lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 10 or sum([1 for i in line if i.isdigit()]) != 8:
            val += 3
        else:
            break
    return line
