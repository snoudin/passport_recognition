import sys, os
import json, time
from threading import Thread
import crop
try:
    from PyQt5.QtCore import Qt, QByteArray
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QDesktopWidget, QMainWindow, QVBoxLayout, QFileDialog
    from PyQt5.QtGui import QMovie
except ImportError:
    os.system('pip install -r passport_recognition/requirements.txt')


class Load(QWidget):
    def __init__(self):
        super().__init__()
        self.movie = QMovie("load.gif", QByteArray(), self)
        size = self.size()
        screenGeometry = QDesktopWidget().screenGeometry(-1).size()
        self.setGeometry((screenGeometry.width() - size.width()) // 2, (screenGeometry.height() - size.height()) // 2, size.width(), size.height())
        self.setWindowTitle('')
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.frame_count = self.movie.frameCount()
        self.movie.frameChanged.connect(self.frameChanged)
        self.frame = 0
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.movie.start()
        self.app = MainApp()
        self.movie.loopCount()

    def frameChanged(self):
        self.frame += 1
        if self.frame >= self.frame_count:
            self.movie.stop()
            self.movie.setParent(None)
            self.movie.deleteLater()
            self.setAttribute(Qt.WA_NoSystemBackground, False)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.destroy()
            self.app.show()


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

    def analyze(self):
        crop.scan(self.path, 1)
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
        self.recieved_in_ans.setText(res['recieved_in'])
        self.animate.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Load()
    ex.show()
    sys.exit(app.exec())