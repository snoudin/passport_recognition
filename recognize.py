import pytesseract, cv2
from PIL import Image


def get_snum(gray):
    val = 100
    line = ''
    while 1:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers).lstrip('\n\t ').rstrip('\n\t ')[:12]
        if len(line) != 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return tuple([line[:2] + line[3:5], line[6:]])


def get_recieved_in(gray):
    val = 90
    line = ''
    while 1:
        if val > 200:
            return None
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


def get_name(gray):
    val = 100
    line = ''
    while len(line) < 2:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        surname = Image.open('bw.png')
        line = pytesseract.image_to_string(surname, lang='rus')
        while line != '' and (line[0] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[0]) > 1200):
            line = line[1:]
        while line != '' and (line[-1] in '-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/' or ord(line[-1]) > 1200):
            line = line[:-1]
        val += 3
        if line == '':
            val += 7
    return line.upper()


def get_gender(gray):
    val = 100
    line = ''
    while line not in ['МУЖ.', 'ЖЕН.']:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        gender = Image.open('bw.png')
        line = pytesseract.image_to_string(gender, lang='rus').lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 12 or sum([1 for i in line if i.isdigit()]) != 10:
            val += 3
        else:
            break
    return line


def get_date(gray):
    val = 100
    line = ''
    while 1:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers).lstrip('-,.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip('-,:;@#!?[]{}_+= \n\t\x0c^*()|\\/')
        if len(line) > 40 or len(line) < 10 or sum([1 for i in line if i.isdigit()]) != 8:
            val += 3
        else:
            break
    return line


def get_born_in(gray):
    val = 100
    line = ''
    while len(line) < 2:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        place = Image.open('bw.png')
        line = pytesseract.image_to_string(place, lang='rus')
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
    val = 100
    line = ''
    while 1:
        if val > 200:
            return None
        im_bw = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("bw.png", im_bw)
        numbers = Image.open('bw.png')
        line = pytesseract.image_to_string(numbers)
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
