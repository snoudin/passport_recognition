from PIL import Image
import pytesseract

img = Image.open('trimap.png')
left, u, r, d = 0, 0, 0, 0
pixels = img.load()
x, y = img.size
comp = [0, 128]
while all([pixels[left, j] in comp for j in range(y)]):
    left += 1
while all([pixels[j, u] in comp for j in range(x)]):
    u += 1
while all([pixels[x - r - 1, j] in comp for j in range(y)]):
    r += 1
while all([pixels[j, y - d - 1] in comp for j in range(x)]):
    d += 1
Image.open('image.jpeg').crop((left, u, x - r, y - d)).save('main.png')

passport = Image.open('main.png')
x, y = passport.size
snum = passport.crop((12 * x // 13, 0, x, y // 2)).transpose(Image.ROTATE_90)
snum.save('series_and_number.png')
pytesseract.pytesseract.tesseract_cmd = r'tesseract v5.0.0\tesseract.exe'
print(pytesseract.image_to_string(snum))
