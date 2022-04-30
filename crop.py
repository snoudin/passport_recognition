import os
import recognize


def scan(img):
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
    y, x, _ = img.shape
    pixels = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #  cv2.imwrite('passport.png', img)
    #  cv2.imwrite('grayscaled.png', pixels)
    while np.mean([pixels[j, left] for j in range(y)]) > 250:
        left += 1
    while np.mean([pixels[u, j] for j in range(x)]) > 250:
        u += 1
    while np.mean([pixels[j, x - r - 1] for j in range(y)]) > 250:
        r += 1
    while np.mean([pixels[y - d - 1, j] for j in range(x)]) > 250:
        d += 1
    passport = Image.fromarray(img).crop((left, u, x - r, y - d)).convert('RGB')
    #  passport.save('cropped.png')
    x, y = passport.size
    templates = json.load(open('templates.json'))
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
        # res = recognize.decrypt(np.asarray(data))
    with open('result.json', 'w', encoding='utf-8') as ans:
        json.dump(result, ans, ensure_ascii=False)
    return 0

