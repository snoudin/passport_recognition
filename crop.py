from PIL import Image
import pytesseract
import opencv_borders, recognize
import cv2, numpy as np


pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
img = cv2.cvtColor(opencv_borders.get_bw('scan.jpg'), cv2.COLOR_BGR2RGB)
img = Image.fromarray(img)
left, u, r, d = 0, 0, 0, 0
pixels = img.load()
x, y = img.size
while all([pixels[left, j] == 0 for j in range(y)]):
    left += 1
while all([pixels[j, u] == 0 for j in range(x)]):
    u += 1
while all([pixels[x - r - 1, j] == 0 for j in range(y)]):
    r += 1
while all([pixels[j, y - d - 1] == 0for j in range(x)]):
    d += 1
passport = Image.open('scan.png').crop((left, u, x - r, y - d))
x, y = passport.size
# TODO: take sizes from .cfg file


snum = passport.crop((11 * x // 13, 0, x, y // 2)).transpose(Image.ROTATE_90)
surname = passport.crop((int(41 * x / 100), int(y * 32 / 60), int(17 * x / 20), int(y * 37 / 60)))
received_in = passport.crop((int(2 * x / 10), int(y / 9), int(18 * x / 20), int(y * 2 / 9)))
name = passport.crop((int(4 * x / 10), int(y * 37 / 60), int(17 * x / 20), int(y * 39 / 60)))
patronym = passport.crop((int(21 * x / 50), int(y * 16 / 25), int(17 * x / 20), int(y * 55 / 80)))
gender = passport.crop((int(11 * x / 30), int(y * 41 / 60), int(19 * x / 40), int(y * 43 / 60)))
birth = passport.crop((int(17 * x / 30), int(y * 41 / 60), int(3 * x / 4), int(y * 43 / 60)))
born_in = passport.crop((int(17 * x / 40), int(y * 43 / 60), int(17 * x / 20), int(y * 50 / 60)))
receive_date = passport.crop((int(2 * x / 10), int(y * 15 / 72), int(16 * x / 40), int(y * 9 / 36)))
code = passport.crop((int(11 * x / 20), int(y * 15 / 72), int(9 * x / 10), int(y * 9 / 36)))


# TODO: take sizes from .cfg file
print(recognize.get_snum(np.asarray(snum.convert('L'))))
print('_______________________________')
print(recognize.get_recieved_in(np.asarray(received_in.convert('L'))))
print('_______________________________')
print(recognize.get_name(np.asarray(surname.convert('L'))))
print('_______________________________')
print(recognize.get_name(np.asarray(name.convert('L'))))
print('_______________________________')
print(recognize.get_name(np.asarray(patronym.convert('L'))))
print('_______________________________')
print(recognize.get_gender(np.asarray(gender.convert('L'))))
print('_______________________________')
print(recognize.get_date(np.asarray(birth.convert('L'))))
print('_______________________________')
print(recognize.get_born_in(np.asarray(born_in.convert('L'))))
print('_______________________________')
print(recognize.get_date(np.asarray(receive_date.convert('L'))))
print('_______________________________')
print(recognize.get_code(np.asarray(code.convert('L'))))
