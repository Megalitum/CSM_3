# coding: utf8

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

app = QApplication(sys.argv)
app.setApplicationName('CSM_3')
# -----------------------------------------------------#

form = MainWindow()
form.setWindowTitle('Лабораторная работа №3')
form.show()

# -----------------------------------------------------#
sys.exit(app.exec_())
