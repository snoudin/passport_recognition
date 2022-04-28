from os import listdir
from PIL import Image


def get_pics():
    return [i for i in listdir('digit dataset/d0') if i.endswith('.png')]


def make_boxes(pic):
    img = Image.open(f'digit dataset/d0/{pic}')
    x, y = img.size
    top, bottom, left, right = y + 1, 0, x + 1, 0
    for i in range(x):
        for j in range(y):
            if img.getpixel((i, j))[0] == 255:
                continue
            top = min(top, j)
            bottom = max(bottom, j + 1)
            left = min(left, i)
            right = max(right, i + 1)
    h = bottom - top + 1
    res = [[left, y - h - top, right, y - top] for i in range(10)]
    maxw = dict()
    maxw['0'] = 6
    maxw['1'] = 4
    maxw['2'] = 6
    maxw['3'] = 6
    maxw['4'] = 6
    maxw['5'] = 6
    maxw['6'] = 6
    maxw['7'] = 5
    maxw['8'] = 6
    maxw['9'] = 6

    def color(col):
        res = 0
        for j in range(top, bottom):
            res += 255 - img.getpixel((col, j))[0]
        return res

    for i in range(10):
        while color(left) == 0:
            left += 1
        res[i][0] = left
        right = min(x + 1, left + maxw[pic[i]])
        for j in range(left + 1, right):
            if color(j) == 0:
                right = j
                break
        if right <= x and color(right) > 0:
            mn, pos = 100000, -1
            for sep in range(left + 3, left + 8):
                cur = color(sep)
                if cur < mn:
                    mn = cur
                    pos = sep
            right = pos + 1
            left = pos
        else:
            left = right
        res[i][2] = right
    return [[str(i) for i in box] for box in res]


def write_res():
    file = open('digit dataset/d0/shakal_digits.font.exp0.box', 'w')
    pics = get_pics()
    res = ''
    for ind in range(len(pics)):
        pic = pics[ind]
        boxes = make_boxes(pic)
        for i in range(10):
            res += pic[i] + ' ' + ' '.join(boxes[i]) + ' ' + str(ind) + '\n'
        if (ind + 1) % 1000 == 0:
            print(f'done {ind + 1} images')
    file.write(res)


write_res()
