import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication


def file_dialog():
    """Диалог выбора файла
    :return: путь к выбранному файлу
    """
    app = QApplication(sys.argv)
    window = QMainWindow()
    fname = QFileDialog.getOpenFileName(window, 'Open file')
    return fname[0]
