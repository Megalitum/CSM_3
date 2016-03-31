# coding: utf8

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType

form_class, base_class = loadUiType('main_window.ui')


class MainWindow(QDialog):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.ui = form_class()
        self.ui.setupUi(self)

