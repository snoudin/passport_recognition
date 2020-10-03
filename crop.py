from PIL import Image
import opencv_borders, recognize


opencv_borders.get_bw('scan.jpg')
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
Image.open('scan.jpg').crop((left, u, x - r, y - d)).save('main.png')

passport = Image.open('main.png')
x, y = passport.size
# TODO: take sizes from .cfg file
snum = passport.crop((11 * x // 13, 0, x, y // 2)).transpose(Image.ROTATE_90)
snum.save('series_and_number.png')
surname = passport.crop((4 * x // 10, y // 60 * 32, 17 * x // 20, y // 60 * 37))
surname.save('surname.png')
recieved_in = passport.crop((2 * x // 10, y // 18 * 2, 18 * x // 20, y // 9 * 2))
recieved_in.save('recieved_in.png')
name = passport.crop((4 * x // 10, y // 60 * 37, 17 * x // 20, y // 20 * 13))
name.save('name.png')
patronym = passport.crop((4 * x // 10, y // 20 * 13, 17 * x // 20, y // 60 * 42))
patronym.save('patronym.png')
gender = passport.crop((11 * x // 30, y // 60 * 42, 10 * x // 20, y // 60 * 44))
gender.save('gender.png')

# TODO: same manipulations
print(recognize.get_snum('series_and_number.png'))
print(recognize.get_recieved_in('recieved_in.png'))
print(recognize.get_name('surname.png'))
print(recognize.get_name('name.png'))
print(recognize.get_name('patronym.png'))
print(recognize.get_gender('gender.png'))
