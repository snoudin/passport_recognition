from PIL import Image
import opencv_borders, recognize


opencv_borders.get_bw('image.jpg')
img = Image.open('trimap.png')
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
Image.open('image.jpg').crop((left, u, x - r, y - d)).save('main.png')

passport = Image.open('main.png')
x, y = passport.size
snum = passport.crop((11 * x // 13, 0, x, y // 2)).transpose(Image.ROTATE_90)
snum.save('series_and_number.png')


# TODO: same manipulations


print(recognize.get_text('series_and_number.png'))
