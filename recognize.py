import pytesseract, cv2
import numpy as np
from math import floor


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
    for char in '-—-':
        line = line.strip(char)
    return line


def data_postprocess(line):
    line = line.upper()
    for ind in range(2000):
        if chr(ind).isdigit():
            continue
        if 'A' <= chr(ind) <= 'Z':
            continue
        if chr(ind) in '<':
            continue
        line = line.replace(chr(ind), '')
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
    used = [[0 for j in range(w)] for i in range(h)]
    process = []

    def near(x, y):
        res = []
        if x > 0:
            res.append((y, x - 1))
        if y > 0:
            res.append((y - 1, x))
        if x + 1 < w:
            res.append((y, x + 1))
        if y + 1 < h:
            res.append((y + 1, x))
        return res

    def val(x):
        return (255 - x) / 127.5

    def cnt_near(x, y):
        res = 0
        for (a, b) in near(x, y):
            res += val(img[a, b, 0])
        return res

    for y in range(h):
        for x in range(w):
            if 0 < img[y, x][0] < 255 and cnt_near(x, y) <= 2:
                process.append((y, x))
                used[y][x] = 1

    while len(process):
        (y, x) = process[-1]
        process.pop()
        img[y, x] = [255, 255, 255]
        for (a, b) in near(x, y):
            if img[a, b][0] in [0, 255] or cnt_near(b, a) > 2:
                continue
            if used[a][b]:
                continue
            used[a][b] = 1
            process.append((a, b))

    cv2.imwrite('cleared.png', img)
    return img


def remove_lines(img):
    h, w = tuple(img.shape[:2])
    cnt = [0 for i in range(h)]
    for x in range(w):
        for y in range(h):
            if img[y, x, 0] != 255:
                cnt[y] += 1
    non_empty_tres = 5
    b = 0
    for i in range(h):
        if cnt[i] < non_empty_tres:
            if (i - b + 1) <= 5:
                for y in range(b, i):
                    for x in range(w):
                        img[y, x] = [255, 255, 255]
            b = i + 1
    return img


def separate(img, bw=False):
    res = np.zeros(img.shape, img.dtype)
    tres_white, tres_grey = 125, 250
    if bw:
        tres_white = 100
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
            elif sum < tres_grey:
                val = 128 - floor(127 * (tres_grey - sum) / (tres_grey - tres_white))
                res[y, x] = [val, val, val]
    cv2.imwrite('separated.png', res)
    return clear_noise(remove_lines(res))


def get_snum(img):
    pytesseract.pytesseract.tesseract_cmd = r'E:\code\recognition\passport_recognition\tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('snum.png', img)
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 8 --oem 3')
    line = postprocess(line)
    if len(line) != 10:
        return None
    return tuple([line[:4], line[4:]])


def get_date(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img), True)
    cv2.imwrite('date_after.png', img)
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 8 --oem 3')
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
    line = pytesseract.image_to_string(img, lang='digits_comma', config='--psm 8 --oem 3')
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
    line = pytesseract.image_to_string(img, lang='rus', config='--psm 7 --oem 3').upper()
    line = word_postprocess(line)
    if not line:
        return None
    return line


def get_gender(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('gender.png', img)
    line = pytesseract.image_to_string(img, lang='rus', config='--psm 7 --oem 3').upper()
    line = word_postprocess(line)
    if not line:
        return None
    if 'M' in line or 'У' in line.upper():
        return 'МУЖ.'
    if 'Е' in line or 'Н' in line.upper():
        return 'ЖЕН.'
    if len(line) < 2:
        return None
    if line[-1] == 'Ж':
        return 'МУЖ.'
    if line[0] == 'Ж':
        return 'ЖЕН.'
    return None


def get_born_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('born_in.png', img)
    line = pytesseract.image_to_string(img, lang='rus').upper()
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
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    cv2.imwrite('data.png', img)
    line = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3')
    line = data_postprocess(line)
    print(line)
    if not line:
        return None
    data = line.split('\n')
    for i in data:
        if not i:
            data.pop(data.index(i))
    if len(data) != 2:
        return False
    data[0] = data[0][5:].rstrip('<>')
    answer = {}
    code = {'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', '2': 'Ё', 'J': 'Ж', 'Z': 'З', 'I': 'И',
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
