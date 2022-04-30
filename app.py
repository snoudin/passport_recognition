import sys, os
import json
import crop
try:
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QMainWindow, QFileDialog
    from PIL import Image
    import numpy as np
except ImportError:
    os.system('pip install -r passport_recognition/requirements.txt')
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QMainWindow, QFileDialog
    from PIL import Image
    import numpy as np


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hide()
        size = self.size()
        screenGeometry = QDesktopWidget().screenGeometry(-1).size()
        self.setGeometry((screenGeometry.width() - size.width()) // 2, (screenGeometry.height() - size.height()) // 2, size.width(), size.height())
        self.path = ''
        uic.loadUi('Menu.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.load)
        self.pushButton_2.clicked.connect(self.analyze)
        self.pushButton_3.clicked.connect(self.edit)

    def load(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png *.jpeg)")[0].replace('/', '\\')
        self.statusBar().showMessage('Фото успешно загружено')

    def edit(self):
        res = {
            'name': self.name_ans.toPlainText(),
            'surname': self.surname_ans.toPlainText(),
            'patronym': self.patronym_ans.toPlainText(),
            'birth': self.birth_ans.toPlainText(),
            'born_in': self.born_in_ans.toPlainText(),
            'gender': self.gender_ans.toPlainText(),
            'code': self.code_ans.toPlainText(),
            'receive_date': self.receive_date_ans.toPlainText(),
            'received_in': self.received_in_ans.toPlainText(),
            'snum': [self.series_ans.toPlainText(), self.number_ans.toPlainText()]
        }
        with open('result.json', 'w', encoding='utf-8') as ans:
            json.dump(res, ans, ensure_ascii=False)
        self.statusBar().showMessage('Изменения сохранены')

    def analyze(self):
        try:
            im = Image.open(self.path)
        except Exception:
            raise IOError('Wrong file path')
        crop.scan(np.asarray(im))  # funny bug: opencv can`t read file with russian letters in path
        res = json.load(open('result.json', 'r', encoding='utf-8'))
        if res['name']:
            self.name_ans.setText(res['name'])
        if res['surname']:
            self.surname_ans.setText(res['surname'])
        if res['patronym']:
            self.patronym_ans.setText(res['patronym'])
        if res['birth']:
            self.birth_ans.setText(res['birth'])
        if res['born_in']:
            self.born_in_ans.setText(res['born_in'])
        if res['gender']:
            self.gender_ans.setText(res['gender'])
        if res['code']:
            self.code_ans.setText(res['code'])
        if res['receive_date']:
            self.receive_date_ans.setText(res['receive_date'])
        if res['received_in']:
            self.received_in_ans.setText(res['received_in'])
        if res['snum']:
            self.series_ans.setText(res['snum'][0])
            self.number_ans.setText(res['snum'][1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec())
