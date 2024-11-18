from PyQt5.QtCore import QThread, pyqtSignal
from helpers import virustotal


class ScanThread(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        total_files = len(self.files)
        for index, file_path in enumerate(self.files, 1):
            result = virustotal.upload_file(file_path)
            self.result_signal.emit(f"Файл: {file_path}\nРезультат: {result}\n")
            
            # Обновляем прогресс
            progress = int((index / total_files) * 100)
            self.progress_signal.emit(progress)
