# coding: utf8

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUiType

from model import FadingOscillation
from rlsm import recursive_lsq
import numpy as np

form_class, base_class = loadUiType('main_window.ui')


class MainWindow(QDialog):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.ui = form_class()
        self.ui.setupUi(self)
        # part 1 >>
        self.ui.deltaInput.setText(str(1.))
        self.ui.omegaInput.setText(str(2.))
        self.ui.equationTable.setHorizontalHeaderLabels(["x", "x'", '-x"'])
        # << part 1
        # part 2 >>
        self.n = None
        self.a = None
        self.b = None
        self.scale = None
        self.normal_distr = None
        self.X = None
        self.ksi = None
        self.rsa = None
        self.cp = None
        self.fse = None
        # << part 2

    @pyqtSlot()
    def run_1(self):
        delta = 0
        omega0 = 0
        left = 0
        right = 0
        try:
            delta = np.float64(self.ui.deltaInput.text())
            omega0 = np.float64(self.ui.omegaInput.text())
            left = np.float64(self.ui.leftT.text())
            right = np.float64(self.ui.rightT.text())
            if not np.isfinite([delta, omega0, left, right]).all():
                raise ValueError("Values are not finite.")
            if delta > omega0:
                raise ValueError("Delta is greater than omega0.")
            if left > right:
                raise ValueError("Left is greater than right.")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        model = FadingOscillation(delta, omega0)
        t_arr = np.arange(left, right, self.ui.stepBox.value())
        X = np.array(list(model(t_arr))).T
        precision = self.ui.precisionBox.currentText()
        if precision != 'max':
            deg = int(precision)
            X = np.round(10**deg * X) / 10**deg;
        self.ui.equationTable.setRowCount(len(t_arr))
        for i, row in enumerate(X):
            self.ui.equationTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.ui.equationTable.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.ui.equationTable.setItem(i, 2, QTableWidgetItem(str(-row[2])))
        theta_gen = recursive_lsq(X[:, :2], -X[:, 2])
        theta_list = list(theta_gen)
        self.ui.thetaList.clear()
        for theta in theta_list:
            self.ui.thetaList.addItem(str(theta.tolist()))
        self.ui.deltaOutput.setText(str(theta_list[-1][1] / 2))
        self.ui.omegaOutput.setText(str(np.sqrt(theta_list[-1][0])))


    @pyqtSlot()
    def gen_X(self):
        try:
            self.n = self.ui.line_n.value()
            if self.n <= 0:
                raise ValueError("n <= 0")
            self.a = np.float64(self.ui.line_a.text())
            self.b = np.float64(self.ui.line_b.text())
            if not np.isfinite([self.a, self.b]).all():
                raise ValueError("Values are not finite.")
            if self.a > self.b:
                raise ValueError("a is greater than b.")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        self.ui.genKsiButton.setEnabled(True)
        self.ui.tableX.clear()
        self.ui.tableX.setRowCount(self.n)
        self.ui.tableX.setColumnCount(self.n)

    @pyqtSlot()
    def gen_ksi(self):
        try:
            self.scale = np.float64(self.ui.line_scale.text())
            if self.scale <= 0:
                raise ValueError("scale <= 0")
            if self.ui.distrBox.currentText() == "Uniform":
                self.normal_distr = True
            else:
                self.normal_distr = False
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        self.ui.ksiList.clear()
        self.ui.ksiList.addItem('123')
        self.ui.ksiList.addItem('12')

    @pyqtSlot()
    def change_s(self):
        pass

    @pyqtSlot()
    def plot(self):
        pass


