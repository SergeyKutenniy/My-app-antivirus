from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFileDialog, QApplication
)
from PyQt5.QtCore import Qt 
from windows import win_test

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_win()
        self.initUI()
        self.connects()
        self.show()
        
    def set_win(self):
        # Налаштування екрану
        self.setWindowTitle('Моя перша програма')
        self.resize(800, 600)
        self.setStyleSheet('''

            background: rgba(207, 207, 207, 1);

        ''')

    def initUI(self):
        # створення віджетів та напрямних
        layout = QVBoxLayout()

        self.b_malware = QPushButton('Сканувати файл')
        self.b_malware.setStyleSheet('''

            background: #7079f0;
            color: white;
            min-width: 200px;
            font-size: 20px;
            font-weight: 500;
            border-radius: 0.5em;
            border: none;
            height: 2.8em;

        ''')
        self.b_exit = QPushButton('Вихід')
        self.b_exit.setStyleSheet('''

            background: #7079f0;
            color: white;
            min-width: 200px;
            font-size: 20px;
            font-weight: 500;
            border-radius: 0.5em;
            border: none;
            height: 2.8em;

        ''')

        self.setWindowFlags(Qt.FramelessWindowHint)

        layout.addWidget(self.b_malware, alignment=Qt.AlignCenter)
        layout.addWidget(self.b_exit, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def connects(self):
        # Підключення подій
        self.b_malware.clicked.connect(self.click_malware)
        self.b_exit.clicked.connect(QApplication.quit)
    
    def click_malware(self):
        self.cur_file = QFileDialog.getOpenFileName()[0]
        if not self.cur_file == '':
            self.tw = win_test.TestWin(self.cur_file)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.draggable = True
           self.dragging_position = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
           self.move(event.globalPos() - self.dragging_position)
           event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.draggable = False
           event.accept()








