from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFileDialog, QApplication, QTextEdit
)
from PyQt5.QtCore import Qt
from windows import win_test
from helpers import virustotal

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_win()
        self.initUI()
        self.connects()
        self.show()
    
    def set_win(self):
        self.setWindowTitle('MyAPP')
        self.resize(800, 600)
        self.setStyleSheet('background: rgba(207, 207, 207, 1);')
    
    def initUI(self):
        layout = QVBoxLayout()

        self.result_box = QTextEdit()  # Для виведення результатів сканування
        self.result_box.setReadOnly(True)
        self.b_scan_file = QPushButton('Сканувати файл')
        self.b_scan_file.setStyleSheet(self.button_style())
        self.b_scan_folder = QPushButton('Сканувати папку')
        self.b_scan_folder.setStyleSheet(self.button_style())
        self.b_exit = QPushButton('Вихід')
        self.b_exit.setStyleSheet(self.button_style())

        self.setWindowFlags(Qt.FramelessWindowHint)

        layout.addWidget(self.b_scan_file, alignment=Qt.AlignCenter)
        layout.addWidget(self.b_scan_folder, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_box)
        layout.addWidget(self.b_exit, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def button_style(self):
        return '''
            background: #7079f0;
            color: white;
            min-width: 200px;
            font-size: 20px;
            font-weight: 500;
            border-radius: 0.5em;
            border: none;
            height: 2.8em;
        '''

    def connects(self):
        self.b_scan_file.clicked.connect(self.click_scan_file)
        self.b_scan_folder.clicked.connect(self.click_scan_folder)
        self.b_exit.clicked.connect(QApplication.quit)

    def click_scan_file(self):
        self.cur_file = QFileDialog.getOpenFileName(self, "Обрати файл")[0]
        if self.cur_file:
            self.scan_file(self.cur_file)

    def click_scan_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Обрати папку")
        if directory:
            self.scan_folder(directory)

    def scan_file(self, file_path):
        result = virustotal.upload_file(file_path)
        self.result_box.append(f"Файл: {file_path}\nРезультат: {result}\n")

    def scan_folder(self, folder_path):
        import os
        self.result_box.append(f"Сканування папки: {folder_path}")
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                result = virustotal.upload_file(file_path)
                self.result_box.append(f"Файл: {file_path}\nРезультат: {result}\n")
