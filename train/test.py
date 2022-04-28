import pytesseract, cv2
import numpy as np
from PIL import Image


def clear(img, denoise=True):
    if denoise:
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        ret, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    connectivity = 5
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity, cv2.CV_32S)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1
    min_size = 4  # threshhold value for small noisy components
    img2 = np.zeros((output.shape), np.uint8)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255
    res = cv2.bitwise_not(img2)
    #cv2.imwrite('cleared.png', res)
    return res


def fast_upscale(img):
    y, x = img.shape
    res = cv2.GaussianBlur(cv2.resize(img, (x * 2, y * 2), interpolation=cv2.INTER_AREA), (5, 5), 0)
    #cv2.imwrite('fast_upscaled.png', res)
    return res


def more_contrast(img):
    res = np.zeros(img.shape, img.dtype)
    alpha = 1.1  # Simple contrast control
    beta = 40     # Simple brightness control
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                res[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)
    #cv2.imwrite('contrasted.png', res)
    return res


def separate(img):
    res = np.zeros(img.shape, img.dtype)
    tres1, tres2 = 150, 120
    for y in range(res.shape[0]):
        for x in range(res.shape[1]):
            sum = 0
            for c in range(res.shape[2]):
                sum += 255 - img[y, x, c]
            if sum < tres2:
                for c in range(res.shape[2]):
                    res[y, x, c] = 255
            elif sum < tres1:
                for c in range(res.shape[2]):
                    res[y, x, c] = 128
    #cv2.imwrite('separated.png', res)
    return res


def read_digits(img):
    pytesseract.pytesseract.tesseract_cmd = r'E:\code\recognition\passport_recognition\tesseract v5.0.0\tesseract.exe'
    img = separate(more_contrast(img))
    return pytesseract.image_to_string(img, lang='digits_comma', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789-')


def read_line(img):
    pytesseract.pytesseract.tesseract_cmd = r'E:\code\recognition\passport_recognition\tesseract v5.0.0\tesseract.exe'
    img = clear(more_contrast(img))
    return pytesseract.image_to_string(img, config='--psm 7 --oem 3', lang='rus')
