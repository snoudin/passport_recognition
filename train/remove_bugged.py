from os import listdir, remove


local = 'E:/code/recognition/passport_recognition/train/digit dataset/d0'
pics = [i for i in listdir(local) if i.endswith('.png')]
file = open(local + '/screen.log', 'r')
data = file.read().split('Page')
for i in range(1, len(data)):
    if 'FAIL' in data[i]:
        remove(local + '/' + pics[i - 1])
