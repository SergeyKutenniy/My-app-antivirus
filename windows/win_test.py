from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel
)
from PyQt5.QtCore import Qt 
from helpers import virustotal


class TestWin(QWidget):
    def __init__(self, cur_file):
        super().__init__()
        self.cur_file = cur_file
        self.set_win()
        self.initUI()
        self.show()
        
        
    def set_win(self):
        # Налаштування екрану
        self.setWindowTitle('Тестовий екран')
        self.resize(600, 400)
        self.setStyleSheet('''

            background: rgba(247, 247, 247, 100);

        ''')

    def initUI(self):
        # створення віджетів та напрямних
       layout = QVBoxLayout()

       s_a = QScrollArea(self)

       data = virustotal.get_info_file(self.cur_file)
       print(data)

       if len(data) == 0:
          label = QLabel('Спробуйте будь-ласка пізніше')
          layout.addWidget(label, alignment=Qt.AlignCenter)
       else:
          for name in data:
              result = f'Антивірус: {name}\nРезультат: {data[name]["result"]}\n'
              label = QLabel(result)
              layout.addWidget(label, alignment=Qt.AlignCenter)

    #    for i in range(100):
    #        label = QLabel(f'Рядок {i}')
    #        layout.addWidget(label, alignment=Qt.AlignCenter)

       content_widget = QWidget()
       content_widget.setLayout(layout)

       s_a.setWidget(content_widget)

       main_layout = QVBoxLayout(self)
       main_layout.addWidget(s_a)




