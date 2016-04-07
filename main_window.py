# coding: utf8

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUiType

from model import FadingOscillation
from part2 import *

form_class, base_class = loadUiType('main_window.ui')


class MainWindow(QDialog):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.ui = form_class()
        self.ui.setupUi(self)
        # part 1 >>
        self.ui.deltaInput.setText(str(1.))
        self.ui.omegaInput.setText(str(2.))
        self.ui.equationTable.setHorizontalHeaderLabels(["x(n-1)", "x(n)", 'x(n+1)'])
        # << part 1
        # part 2 >>
        self.m = 5
        self.n = None
        self.a = None
        self.b = None
        self.theta = None
        self.scale = None
        self.normal_distr = False
        self.X = None
        self.ksi = None
        self.rss = None
        self.cp = None
        self.fpe = None
        self.y_restored = None
        # << part 2

    @pyqtSlot()
    def run_1(self):
        delta = 0
        omega0 = 0
        try:
            delta = np.float64(self.ui.deltaInput.text())
            omega0 = np.float64(self.ui.omegaInput.text())
            start = np.float64(self.ui.startT.text())
            if not np.isfinite([delta, omega0, start]).all():
                raise ValueError("Values are not finite.")
            if delta > omega0:
                raise ValueError("Delta is greater than omega0.")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        h = 10**self.ui.hDegreeBox.value()
        steps_count = self.ui.stepCountBox.value()
        data_h = h * 10**self.ui.stepMultBox.value()
        model = FadingOscillation(delta, omega0, step=h)
        t_arr = np.arange(start, start + steps_count * data_h, data_h)
        X = np.array(list(model(t_arr))).T
        precision = self.ui.precisionBox.value()
        X = np.around(X, decimals=precision)
        self.ui.equationTable.setRowCount(len(t_arr))
        for i, row in enumerate(X):
            for j in range(3):
                self.ui.equationTable.setItem(i, j, QTableWidgetItem(str(row[j])))
        theta_gen = recursive_lsq(X[:, :2], X[:, 2])
        self.ui.thetaList.clear()
        result = None
        for theta, rss in theta_gen:
            self.ui.thetaList.addItem(str(theta.tolist()))
            result = theta
        self.ui.deltaOutput.setText(str((1 + result[0]) / (1 - result[0]) / h))
        self.ui.omegaOutput.setText(str(np.sqrt(2 * (1 - result[0] - result[1]) / (1 - result[0])) / h))


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
        self.ui.tableX.setColumnCount(self.m)
        self.ui.tableX.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.X = ksi_un(self.a, self.b, size = (self.n,self.m)) # generate X here
        print('X = \n',self.X)
        for i in range(self.n):
            for j in range(self.m):
                self.ui.tableX.setItem(i, j, QTableWidgetItem(str(self.X[i, j])))
        if self.theta is None:
            self.ui.thetaTable.setEnabled(True)
            self.theta = np.array([0] * self.m)
            self.ui.thetaTable.setColumnCount(self.m)
            self.ui.thetaTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.m):
            self.ui.thetaTable.setItem(0, i, QTableWidgetItem(str(self.theta[i])))
        self.gen_ksi()

    @pyqtSlot()
    def gen_ksi(self):
        try:
            self.scale = np.float64(self.ui.line_scale.text())
            if self.scale < 0:
                raise ValueError("scale < 0")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        self.ui.ksiList.clear()
        self.ksi =  distr(not self.normal_distr, self.scale, size = (self.n,1)) # generate ksi here
        print('ksi\n',self.ksi)
        for val in self.ksi:
            self.ui.ksiList.addItem(str(val))
        self.ui.calcYbutton.setEnabled(True)

    @pyqtSlot()
    def change_s(self):
        if self.rss is None or self.cp is None or self.fpe is None or self.y_restored is None:
            return
        self.ui.lineRSS.setText(str(self.rss[self.ui.box_s.currentIndex()]))
        self.ui.lineCP.setText(str(self.cp[self.ui.box_s.currentIndex()]))
        self.ui.lineFPE.setText(str(self.fpe[self.ui.box_s.currentIndex()]))
        self.ui.y_restored.clear()
        for y in self.y_restored[self.ui.box_s.currentIndex()]:
            self.ui.y_restored.addItem(str(y))


    @pyqtSlot()
    def plot(self):
        if self.rss is None or self.cp is None or self.fpe is None:
            return
        plot(self.rss, self.cp, self.fpe)

    @pyqtSlot(int)
    def distr_changed(self, index):
        if index != 0:
            self.normal_distr = True
        else:
            self.normal_distr = False

    @pyqtSlot()
    def calcY(self):
        r = manage(self.n, self.m, self.theta[:, np.newaxis], self.X, self.ksi)
        self.rss = r['rss']
        self.cp = r['cp']
        self.fpe = r['fse']
        self.ui.y_clean.clear()
        for y in r['y_gen']:
            self.ui.y_clean.addItem(str(y))
        self.ui.y_noised.clear()
        for y in r['y_ksi']:
            self.ui.y_noised.addItem(str(y))
        self.y_restored = r['y_restored']
        self.change_s()

    @pyqtSlot(QTableWidgetItem)
    def theta_changed(self, item):
        if self.theta is None:
            return
        newvalue = None
        try:
            newvalue = np.float64(item.text())
            if not np.isfinite(newvalue).all():
                raise ValueError("Values are not finite.")
        except ValueError as e:
            item.setText(str(self.theta[item.column()]))
            return
        self.theta[item.column()] = newvalue

