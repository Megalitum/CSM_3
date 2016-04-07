# coding: utf8

import sys
import matplotlib
matplotlib.use("Qt5Agg", force=True)
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

import matplotlib.pyplot as plt

app = QApplication(sys.argv)
app.setApplicationName('CSM_3')
# -----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('Лабораторная работа №3')
form.show()

# -----------------------------------------------------#
sys.exit(app.exec_())
