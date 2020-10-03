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
surname = passport.crop((int(41 * x / 100), int(y * 32 / 60), int(17 * x / 20), int(y * 37 / 60)))
surname.save('surname.png')
recieved_in = passport.crop((int(2 * x / 10), int(y / 9), int(18 * x / 20), int(y * 2 / 9)))
recieved_in.save('recieved_in.png')
name = passport.crop((int(4 * x / 10), int(y * 37 / 60), int(17 * x / 20), int(y * 39 / 60)))
name.save('name.png')
patronym = passport.crop((int(21 * x / 50), int(y * 16 / 25), int(17 * x / 20), int(y * 55 / 80)))
patronym.save('patronym.png')
gender = passport.crop((int(11 * x / 30), int(y * 41 / 60), int(19 * x / 40), int(y * 43 / 60)))
gender.save('gender.png')
birth = passport.crop((int(17 * x / 30), int(y * 41 / 60), int(3 * x / 4), int(y * 43 / 60)))
birth.save('birth.png')
born_in = passport.crop((int(17 * x / 40), int(y * 43 / 60), int(17 * x / 20), int(y * 50 / 60)))
born_in.save('born_in.png')

# TODO: codes and receive date
print(recognize.get_snum('series_and_number.png'))
print('_______________________________')
print(recognize.get_recieved_in('recieved_in.png'))
print('_______________________________')
print(recognize.get_name('surname.png'))
print('_______________________________')
print(recognize.get_name('name.png'))
print('_______________________________')
print(recognize.get_name('patronym.png'))
print('_______________________________')
print(recognize.get_gender('gender.png'))
print('_______________________________')
print(recognize.get_date('birth.png'))
print('_______________________________')
print(recognize.get_born_in('born_in.png'))
