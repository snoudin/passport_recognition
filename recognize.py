import pytesseract, cv2
import numpy as np


def get_snum(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('snum.png', img)
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789').lstrip('\n\t\f ').rstrip('\n\t\f ')[:12]
    line.replace(' ', '')
    if not line:
        return None
    return tuple([line[:4], line[4:]])


def get_recieved_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('recieved_in.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('  ', ' ')
    if not line:
        return None
    return line.lstrip(',.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/').rstrip(',.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/').upper()


def get_name(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('name.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    while line != '' and (line[0] in '-,.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200):
        line = line[1:]
    while line != '' and (line[-1] in '-,.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200):
        line = line[:-1]
    if not line:
        return None
    return line.upper()


def get_gender(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(img)
    cv2.imwrite('gender.png', img)
    line = pytesseract.image_to_string(img, lang='rus').upper()
    if not line:
        return None
    if 'M' in line or 'У' in line.lstrip(',.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/').rstrip(',.:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/').upper():
        return 'МУЖ.'
    else:
        return 'ЖЕН.'


def get_date(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('date.png', img)
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.')
    if not line.lstrip(' \n\t\f\x0c.').rstrip(' \n\t\f\x0c.'):
        return None
    return line.lstrip(' \n\t\f\x0c.').rstrip(' \n\t\f\x0c.')


def get_born_in(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('born_in.png', img)
    line = pytesseract.image_to_string(img, lang='rus')
    line = line.replace('\n', ' ')
    line = line.replace('--', '-')
    line = line.replace(' -', '')
    line = line.replace('_', '')
    line = line.replace('..', '')
    line = line.replace(' .', '')
    line = line.replace('  ', ' ')
    while line != '' and (line[0] in '-.,:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[0]) > 1200
                          or line[0].islower()):
        line = line[1:]
    while line != '' and (line[-1] in '-.,:;@#!?[]{}_+= \n\t\f\x0c^*()|\\/' or ord(line[-1]) > 1200
                          or line[-1].islower()):
        line = line[:-1]
    if not line:
        return None
    return line.upper()


def get_code(img):
    pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    cv2.imwrite('code.png', img)
    line = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789-')
    if not line.lstrip(' \n\t\f\x0c-').rstrip(' \n\t\f\x0c-'):
        return None
    return line.lstrip(' \n\t\f\x0c-').rstrip(' \n\t\f\x0c-')


def more_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


# Not used
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


# Not used
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
