import pytesseract, cv2
import numpy as np


def get_snum(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = upscale(clear(more_contrast(img)))
    # cv2.imwrite('snum.png', img)
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789').lstrip('\n\t\f ').rstrip('\n\t\f ')[:12]
    line.replace(' ', '')
    if not line:
        return None
    return tuple([line[:4], line[4:]])


def get_recieved_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    line = pytesseract.image_to_string(img, lang='rus')
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('|', '')
    line = line.replace('\\', '')
    line = line.replace('/', '')
    line = line.replace('[', '')
    line = line.replace(']', '')
    line = line.replace('%', '')
    line = line.replace('#', '')
    while '  ' in line:
        line = line.replace('  ', ' ')
    while line != '' and (line[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200 or line[0].islower() or not line[0].isalpha()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200 or line[-1].islower() or not line[-1].isalpha()):
        line = line[:-1]
    if not line:
        return None
    if 'ГОР.' not in line:
        line = line.replace('ГОР', 'ГОР.')
    while not (line.startswith('Г') or line.startswith('ОТДЕЛ')):
        line = line[1:]
    return line


def get_name(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    line = pytesseract.image_to_string(img, lang='rus')
    while line != '' and (line[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200 or not line[0].isalpha()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200 or not line[-1].isalpha()):
        line = line[:-1]
    if not line:
        return None
    words = line.split('\n')
    for i in words:
        pos = words.index(i)
        while i != '' and (i[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(i[0]) > 1200 or not line[0].isalpha()):
            i = i[1:]
        while i != '' and (i[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(i[-1]) > 1200 or not line[-1].isalpha()):
            i = i[:-1]
        words[pos] = i.lstrip('—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/').rstrip('—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/')
        if not i or not i.isupper():
            words.pop(words.index(i))
    if len(words) > 1:
        return words[0]
    return ''.join(words)


def get_gender(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(img)
    line = pytesseract.image_to_string(img, lang='rus').upper()
    while line != '' and (line[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200 or not line[0].isalpha()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200 or not line[-1].isalpha()):
        line = line[:-1]
    if not line:
        return None
    if 'M' in line or 'У' in line.upper():
        return 'МУЖ.'
    else:
        return 'ЖЕН.'


def get_date(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = upscale(clear(more_contrast(img)))
    # cv2.imwrite('date.png', img)
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789').lstrip(' \n\t\f\x0c.').rstrip(' \n\t\f\x0c.')
    line = line.replace('.', '')
    while line != '' and (line[0] in ' \n\t\f\x0c^*()|\\/' or ord(line[0]) > 200):
        line = line[1:]
    while line != '' and (line[-1] in ' \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 200):
        line = line[:-1]
    if not line:
        return None
    for i in line:
        if not i.isdigit():
            line.pop(line.index(i))
    try:
        d, m, y = int(line[:2]), int(line[2:4]), int(line[4:])
        if d > 31 or m > 12 or y > 2100:
            return None
    except Exception:
        return None
    return line[:2] + '.' + line[2:4] + '.' + line[4:]


def get_born_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    # cv2.imwrite('born_in.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('  ', ' ')
    while line != '' and (line[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200
                          or line[0].islower() or not line[0].isalpha()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200
                          or line[-1].islower() or not line[-1].isalpha()):
        line = line[:-1]
    if not line:
        return None
    while 'Г.' in line and not line.startswith('Г.'):
        line = line[1:]
    while 'ГОР.' in line and not line.startswith('ГОР.'):
        line = line[1:]
    if 'ГОР.' not in line:
        line = line.replace('ГОР', 'ГОР.')
    if not line.startswith('ГОР') and 'Г.' not in line and line.startswith('Г'):
        line = line.replace('Г', 'Г.', 1)
    return line


def get_code(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789-').lstrip(' \n\t\f\x0c-').rstrip(' \n\t\f\x0c-')
    while line != '' and (line[0] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 200
                          or line[0].islower()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 200
                          or line[-1].islower()):
        line = line[:-1]
    if not line:
        return None
    return line


def decrypt(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = upscale(clear(more_contrast(img)))
    line = pytesseract.image_to_string(img).lstrip(' \n\t\f\x0c-').rstrip(' \n\t\f\x0c-')
    while line != '' and (line[0] in '—-,.:;@#!>%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 200
                          or line[0].islower()):
        line = line[1:]
    while line != '' and (line[-1] in '—-,.:;>@#!%$?&[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 200
                          or line[-1].islower()):
        line = line[:-1]
    print(line)
    if not line:
        return None
    data = line.split()
    for i in data:
        if not i:
            data.pop(data.index(i))
    if len(data) != 2:
        return False
    data[0] = data[0][5:].rstrip('<>')
    answer = {}
    code = {'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', '2': 'Е', 'J': 'Ж', 'Z': 'З', 'I': 'И',
            'Q': 'И', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т',
            'U': 'У', 'F': 'Ф', 'H': 'Х', 'C': 'Ц', '3': 'Ч', '4': 'Ш', 'W': 'Щ', 'X': 'Ъ', 'Y': 'Ы', '9': 'Ь',
            '6': 'Э', '7': 'Ю', '8': 'Я'}
    words = data[0].strip('<')
    for i in words:
        if not i:
            words.pop(words.index(i))
    for i in range(len(words)):
        words[i] = ''.join([code[j] for j in words[i]]).upper()
    answer = {"surname": words[0], "name": words[1], "patronym": words[2]}
    data = data[1][14:]
    birth = data[:6]
    answer.update({"birth": birth[4:] + '.' + birth[2:4] + '.' + birth[:2]})
    data = data[6:]
    answer["gender"] = 'МУЖ.' if data[1] == 'M' else 'ЖЕН.'
    data = data[2:].lstrip('<')[1:]
    date = data[:6]
    answer.update({"receive_date": date[4:] + '.' + date[2:4] + '.' + date[:2]})
    data = data[6:]
    answer.update({"code": data[:3] + '-' + data[3:6]})
    print(answer)
    return answer


def more_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def clear(img, denoise=True):
    if denoise:
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        ret, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    connectivity = 4
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity, cv2.CV_32S)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1
    min_size = 50  # threshhold value for small noisy components
    img2 = np.zeros((output.shape), np.uint8)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255
    return cv2.bitwise_not(img2)


def upscale(img):
    y, x = img.shape
    return cv2.GaussianBlur(cv2.resize(img, (x * 2, y * 2), interpolation=cv2.INTER_AREA), (5, 5), 0)
