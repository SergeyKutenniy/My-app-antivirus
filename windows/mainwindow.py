from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFileDialog, QApplication, QProgressBar, QTextEdit, QHBoxLayout, QVBoxLayout
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
        # Главный горизонтальный макет
        main_layout = QHBoxLayout()

        # Вертикальный макет для кнопок (слева)
        buttons_layout = QVBoxLayout()
        self.b_scan_file = QPushButton('Сканировать файл')
        self.b_scan_folder = QPushButton('Сканировать папку')
        self.b_exit = QPushButton('Выход')

        # Стили кнопок
        for button in [self.b_scan_file, self.b_scan_folder, self.b_exit]:
            button.setStyleSheet('''
                background: #7079f0;
                color: white;
                min-width: 150px;
                font-size: 16px;
                font-weight: 500;
                border-radius: 0.5em;
                border: none;
                height: 2.5em;
            ''')
            buttons_layout.addWidget(button, alignment=Qt.AlignTop)

        buttons_layout.addStretch()  # Отступ внизу для кнопок

        # Вертикальный макет для прогресс-бара и текста (справа)
        right_layout = QVBoxLayout()

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

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet('''
            background: white;
            border: 1px solid #ccc;
            font-size: 14px;
        ''')

        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.result_box)

        # Добавление макетов в главный макет
        main_layout.addLayout(buttons_layout, stretch=1)  # Кнопки занимают меньше пространства
        main_layout.addLayout(right_layout, stretch=2)  # Прогресс-бар и текст занимают больше пространства

        self.setLayout(main_layout)

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
