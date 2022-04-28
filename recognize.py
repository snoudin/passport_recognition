import pytesseract, cv2
import numpy as np


def postprocess(line):
    line = line.replace(' ', '')
    for ind in range(2000):
        if chr(ind).isdigit():
            continue
        line = line.replace(chr(ind), '')
    return line


def string_postprocess(line):
    for ind in range(2000):
        if chr(ind).isalpha() or chr(ind).isdigit() or chr(ind) in ' .,/\\-—':
            continue
        line = line.replace(chr(ind), '')
    while '  ' in line:
        line = line.replace('  ', ' ')
    return line


def word_postprocess(line):
    line = string_postprocess(line).replace(' ', '')
    for char in '.,/\\':
        line = line.replace(char, '')
    return line


def more_contrast(img):
    res = np.zeros(img.shape, img.dtype)
    alpha = 1.1  # Simple contrast control
    beta = 40     # Simple brightness control
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                res[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)
    cv2.imwrite('contrasted.png', res)
    return res


def clear_noise(img):
    h, w = tuple(img.shape[:2])

    def cnt_near(x, y):
        res = 0
        val = dict()
        val[0] = 2
        val[128] = 1
        val[255] = 0
        res += val[img[y, x - 1, 0]]
        res += val[img[y - 1, x, 0]]
        res += val[img[y, x + 1, 0]]
        res += val[img[y + 1, x, 0]]
        return res

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if img[y, x][0] == 128 and cnt_near(x, y) <= 1:
                img[y, x] = [255, 255, 255]
    cv2.imwrite('cleared.png', img)
    return img


def separate(img, bw=False):
    res = np.zeros(img.shape, img.dtype)
    tres_white = 125
    if bw:
        tres_white -= 25
    tres_gray = 250
    for y in range(res.shape[0]):
        for x in range(res.shape[1]):
            sum, mn, mx = 0, 255, 0
            for c in range(res.shape[2]):
                sum += 255 - img[y, x, c]
                mn = min(mn, img[y, x, c])
                mx = max(mx, img[y, x, c])
            if bw and mx - mn > 20:
                res[y, x] = [255, 255, 255]
                continue
            if sum < tres_white:
                res[y, x] = [255, 255, 255]
            elif sum < tres_gray:
                res[y, x] = [128, 128, 128]
    cv2.imwrite('separated.png', res)
    return clear_noise(res)


def get_snum(img):
    pytesseract.pytesseract.tesseract_cmd = r'E:\code\recognition\passport_recognition\tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('snum.png', img)
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 7 --oem 3')
    line = postprocess(line)
    if len(line) != 10:
        return None
    return tuple([line[:4], line[4:]])


def get_date(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img), True)
    cv2.imwrite('date_after.png', img)
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 7 --oem 3')
    line = postprocess(line)
    if len(line) != 8:
        return None
    if line[0] == '6' or line[0] == '9':
        line[0] = '0'
    if line[2] == '6' or line[2] == '9':
        line[2] = '0'
    if line[0] == '8':
        line[0] = '3'
    d, m, y = int(line[:2]), int(line[2:4]), int(line[4:])
    if d > 31 or m > 12 or y > 2100:
        return None
    return line[:2] + '.' + line[2:4] + '.' + line[4:]


def get_code(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img), True)
    cv2.imwrite('code.png', img)
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 7 --oem 3')
    line = postprocess(line)
    if len(line) != 6:
        return None
    return line[:3] + '-' + line[3:]


def get_received_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img), True)
    line = pytesseract.image_to_string(img, lang='rus')
    line = string_postprocess(line)
    if not line:
        return None
    return line


def get_name(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('name.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    line = word_postprocess(line)
    if not line:
        return None
    return line


def get_gender(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('gender.png', img)
    line = pytesseract.image_to_string(img, lang='rus').upper()
    line = word_postprocess(line)
    if not line:
        return None
    if 'M' in line or 'У' in line.upper():
        return 'МУЖ.'
    else:
        return 'ЖЕН.'


def get_born_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    # cv2.imwrite('born_in.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('  ', ' ')
    line = string_postprocess(line)
    if not line:
        return None
    if 'ГОР.' not in line:
        line = line.replace('ГОР', 'ГОР.')
    if 'Г.' not in line and 'Г ' in line:
        line = line.replace('Г', 'Г.')
    while 'Г.' in line and not line.startswith('Г.'):
        line = line[1:]
    while 'ГОР.' in line and not line.startswith('ГОР.'):
        line = line[1:]
    if not line.startswith('ГОР') and 'Г.' not in line and line.startswith('Г'):
        line = line.replace('Г', 'Г.', 1)
    return line


def decrypt(img):

    return None

    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
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
