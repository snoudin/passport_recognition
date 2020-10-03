import sys, os
try:
    from PyQt5.QtCore import Qt, QByteArray
    from PyQt5 import uic, QtSvg
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QDesktopWidget, QMainWindow, QVBoxLayout
    from PyQt5.QtGui import QMovie
except ImportError:
    os.system('pip install -r requirements.txt')


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
        uic.loadUi('Form.ui', self)
        self.initUI()

    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Load()
    ex.show()
    sys.exit(app.exec())


# TODO: compile to standalone .exe
