import sys, os
import json, time
import crop
try:
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QMainWindow, QFileDialog
    from PIL import Image
except ImportError:
    os.system('pip install -r passport_recognition/requirements.txt')
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QMainWindow, QFileDialog
    from PIL import *


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

    def load(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png *.jpeg)")[0].replace('/', '\\')
        self.statusBar().showMessage('Фото успешно загружено')

    def analyze(self):
        im = Image.open(self.path)
        new_name = 'localname' + '.' + self.path.split('.')[-1]
        im.save(new_name)
        crop.scan(new_name, 1)  # funny bug: opencv can`t read file with russian letters in path
        os.remove(new_name)
        time.sleep(50)
        res = json.load(open('result.json'))
        self.name_ans.setText(res['name'])
        self.surname_ans.setText(res['surname'])
        self.patronym_ans.setText(res['patronym'])
        self.birth_ans.setText(res['birth'])
        self.born_in_ans.setText(res['born_in'])
        self.gender_ans.setText(res['gender'])
        self.code_ans.setText(res['code'])
        self.receive_date_ans.setText(res['receive_date'])
        self.received_in_ans.setText(res['received_in'])
        self.series_ans.setText(res['snum'][0])
        self.number_ans.setText(res['snum'][1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec())
