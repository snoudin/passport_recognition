import pytesseract, cv2
from PIL import Image


def get_snum(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 120
    line = ''
    while 1:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw).lstrip('\n\t ').rstrip('\n\t ')[:12]
        if len(line) != 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return tuple([line[:2] + line[3:5], line[6:]])


def get_recieved_in(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 90
    line = ''
    while 1:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw, lang='rus')
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


def get_name(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 100
    line = ''
    while len(line) < 2:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw, lang='rus')
        while line != '' and (line[0] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[0]) > 1200):
            line = line[1:]
        while line != '' and (line[-1] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[-1]) > 1200):
            line = line[:-1]
        val += 3
        if line == '':
            val += 7
    return line.upper()


def get_gender(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 100
    line = ''
    while line not in ['МУЖ.', 'ЖЕН.']:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw, lang='rus').lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return line


def get_date(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 100
    line = ''
    while 1:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw).lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 10 or sum([1 for i in line if i.isdigit()]) != 8:
            val += 3
        else:
            break
    return line


def get_born_in(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 100
    line = ''
    while len(line) < 2:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw, lang='rus')
        line = line.replace('\n', ' ')
        line = line.replace('--', '-')
        line = line.replace(' -', '')
        line = line.replace('_', '')
        line = line.replace('..', '')
        line = line.replace(' .', '')
        line = line.replace('  ', ' ')
        while line != '' and (line[0] in '-.,:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[0]) > 1200
                              or line[0].islower()):
            line = line[1:]
        while line != '' and (line[-1] in '-.,:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[-1]) > 1200
                              or line[-1].islower()):
            line = line[:-1]
        val += 3
        if line == '':
            val += 7
    return line


def get_code(gray):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    val = 100
    line = ''
    while 1:
        if val > 180:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        line = pytesseract.image_to_string(im_bw)
        while line != '' and (line[0] in '-.,:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[0]) > 1200
                              or line[0].islower()):
            line = line[1:]
        while line != '' and (line[-1] in '-.,:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[-1]) > 1200
                              or line[-1].islower()):
            line = line[:-1]
        line = line.replace('\n', ' ')
        line = line.replace('--', '-')
        line = line.replace(' -', '')
        line = line.replace('_', '')
        line = line.replace('..', '')
        line = line.replace(' .', '')
        line = line.replace('  ', ' ')
        if len(line) != 7 or sum([1 for i in line if i.isdigit()]) != 6:
            val += 3
        else:
            break
    return line
