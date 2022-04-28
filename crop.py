import os
import opencv_borders, recognize


def scan(path, background):
    '''
    path can be absolute and local
    background is bool, mean there is picture contains background behind passport
    '''
    try:
        from PIL import Image
        import cv2, json
        import numpy as np
    except ImportError:
        os.system('pip install -r requirements.txt')
        from PIL import Image
        import cv2, json
        import numpy as np
    left, u, r, d = 0, 0, 0, 0
    try:
        img = cv2.imread(path)
    except Exception:
        raise IOError('Wrong file path')
    y, x, _ = img.shape
    if background:
        pixels = Image.fromarray(opencv_borders.get_bw(path)).load()
        while np.mean([pixels[left, j] for j in range(y)]) < 5:
            left += 1
        while np.mean([pixels[j, u] for j in range(x)]) < 5:
            u += 1
        while np.mean([pixels[x - r - 1, j] for j in range(y)]) < 5:
            r += 1
        while np.mean([pixels[j, y - d - 1] for j in range(x)]) < 5:
            d += 1
    passport = Image.fromarray(img).crop((left, u, x - r, y - d))
    x, y = passport.size
    templates = json.load(open('templates.json'))
    best = ({}, 0)
    for template in templates:
        pos = template['snum']
        snum = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y))).transpose(Image.ROTATE_90)

        pos = template['surname']
        surname = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['received_in']
        received_in = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['name']
        name = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['patronym']
        patronym = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['gender']
        gender = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['birth']
        birth = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['born_in']
        born_in = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['receive_date']
        receive_date = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['code']
        code = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        pos = template['data']
        data = passport.crop((int(pos[0] * x), int(pos[1] * y), int(pos[2] * x), int(pos[3] * y)))

        result = {
            'snum': recognize.get_snum(np.asarray(snum)),
            'birth': recognize.get_date(np.asarray(birth)),
            'receive_date': recognize.get_date(np.asarray(receive_date)),
            'code': recognize.get_code(np.asarray(code)),
            'gender': recognize.get_gender(np.asarray(gender)),
            'name': recognize.get_name(np.asarray(name)),
            'surname': recognize.get_name(np.asarray(surname)),
            'patronym': recognize.get_name(np.asarray(patronym)),
            'received_in': recognize.get_received_in(np.asarray(received_in)),
            'born_in': recognize.get_born_in(np.asarray(born_in))
        }
        res = recognize.decrypt(np.asarray(data))
        if res:
            for i in res.keys():
                result[i] = res[i]
        cnt = sum([1 for i in result.keys() if result[i]])
        if cnt > best[1]:
            best = (result, cnt)
    with open('result.json', 'w', encoding='windows-1251') as ans:
        json.dump(best[0], ans, ensure_ascii=False)
    return 0

