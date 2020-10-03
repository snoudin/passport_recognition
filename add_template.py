import json


def add(template):
    '''
    template is dict, that has following form:
        'snum': (11 / 13, 0, 1, 1 / 2) <- this means,
         that for each coord in snum in multiples by list[i]
    '''
    templates = json.load(open('templates.json'))
    if template not in templates:
        templates.append(template)
    with open('templates.json', 'w') as ans:
        json.dump(templates, ans)
