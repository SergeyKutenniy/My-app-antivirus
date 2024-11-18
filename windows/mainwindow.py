from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFileDialog, QApplication, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from helpers import virustotal
import os
from helpers.scan_thread import ScanThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_win()
        self.initUI()
        self.connects()
        self.show()

    def set_win(self):
        self.setWindowTitle('Антивирус с прогресс-баром')
        self.resize(800, 600)
        self.setStyleSheet('background: rgba(207, 207, 207, 1);')

    def initUI(self):
        # Основной layout
        self.layout = QVBoxLayout()

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #7079f0;
                text-align: center;
                color: black;
                background: #fff;
            }
            QProgressBar::chunk {
                background: #7079f0;
            }
        ''')

        # Кнопки
        self.b_scan_file = QPushButton('Сканировать файл')
        self.b_scan_file.setStyleSheet(self.button_style())
        self.b_scan_folder = QPushButton('Сканировать папку')
        self.b_scan_folder.setStyleSheet(self.button_style())
        self.b_exit = QPushButton('Выход')
        self.b_exit.setStyleSheet(self.button_style())

        # Текстовое поле для вывода результатов
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        # Добавление элементов в layout
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.b_scan_file, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.b_scan_folder, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.b_exit, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.result_box)

        self.setLayout(self.layout)

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
        self.cur_file = QFileDialog.getOpenFileName(self, "Выберите файл")[0]
        if self.cur_file:
            self.scan_files([self.cur_file])

    def click_scan_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            files = [
                os.path.join(root, file)
                for root, _, files in os.walk(directory) for file in files
            ]
            self.scan_files(files)

    def scan_files(self, files):
        self.result_box.clear()
        self.progress_bar.setValue(0)

        # Создаем поток для сканирования
        self.scan_thread = ScanThread(files)
        self.scan_thread.progress_signal.connect(self.update_progress)
        self.scan_thread.result_signal.connect(self.append_result)
        self.scan_thread.finished.connect(self.scan_finished)

        self.scan_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def append_result(self, result):
        self.result_box.append(result)

    def scan_finished(self):
        self.result_box.append("Сканирование завершено!")
