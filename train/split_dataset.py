from os import listdir
from shutil import *


local = 'E:/code/recognition/passport_recognition/train/'


def split_raw():
    txts = [i for i in listdir(local + 'digit dataset') if i.endswith('.txt')]
    pics = [i for i in listdir(local + 'digit dataset') if i.endswith('.png')]

    for ind in range(len(txts)):
        move(local + f'digit dataset/{txts[ind]}', local + f'digit dataset/d{ind % 10}/{txts[ind]}')
        move(local + f'digit dataset/{pics[ind]}', local + f'digit dataset/d{ind % 10}/{pics[ind]}')


def split_box():
    strings = ['' for i in range(10)]
    data = open(f'{local}digit dataset/shakal_digits.font.exp0.box').readlines()
    for i in data:
        digits = i.split()
        ind = int(digits[-1])
        strings[ind % 10] += ' '.join(digits[:-1]) + ' ' + str(ind // 10) + '\n'
    for i in range(10):
        f = open(f'{local}digit dataset/shakal_digits_{i}.font.exp0.box', 'w')
        f.write(strings[i])


split_box()
