from PIL import Image

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
