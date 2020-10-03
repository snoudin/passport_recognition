import pytesseract, cv2
import numpy as np


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
    return line.lstrip(',.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').rstrip(',.:;@#!?[]{}_+= \n\t\x0c^*()|\\/').upper()


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
    cv2.imwrite('bw.png', cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)[1])
    return line.upper()


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
    return line.upper()


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


def more_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def remove_lines(img):
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(img, [c], -1, (255, 255, 255), 2)
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
    result = 255 - cv2.morphologyEx(255 - img, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
    cv2.imwrite('result.png', result)
    cv2.waitKey()


def remove_noise(im):
    # smooth the image with alternative closing and opening
    # with an enlarging kernel
    morph = im.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # take morphological gradient
    gradient_image = cv2.morphologyEx(morph, cv2.MORPH_GRADIENT, kernel)
    # split the gradient image into channels
    image_channels = np.split(np.asarray(gradient_image), 3, axis=2)
    channel_height, channel_width, _ = image_channels[0].shape
    # apply Otsu threshold to each channel
    for i in range(0, 3):
        _, image_channels[i] = cv2.threshold(~image_channels[i], 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
        image_channels[i] = np.reshape(image_channels[i], newshape=(channel_height, channel_width, 1))
    # merge the channels
    image_channels = np.concatenate((image_channels[0], image_channels[1], image_channels[2]), axis=2)
    # save the denoised image
    cv2.imwrite('output.jpg', image_channels)