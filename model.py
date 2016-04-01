# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt


class FadingOscillation(object):
    def __init__(self, *args, **kwargs):
        self.delta = args[0]
        self.omega0 = args[1]
        self.omega = np.sqrt(self.omega0**2 - self.delta**2)
        self.step = kwargs.get('step', 1e-6)
        self.A0 = kwargs.get('A0', 1)
        self.phi = kwargs.get('phi', 0)

    def calc_value(self, t):
        return np.exp(-self.delta * t) * self.A0 * np.cos(self.omega * t + self.phi)

    def calc_derivative(self, t):
        return (self.calc_value(t + self.step) - self.calc_value(t - self.step)) / (2 * self.step)

    def calc_detivative_2(self, t):
        return (self.calc_value(t + self.step) + self.calc_value(t - self.step) - 2 * self.calc_value(t)) /\
               (self.step**2)

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.calc_value(t), self.calc_derivative(t), self.calc_detivative_2(t)

    def test(self):
        X = np.arange(0, 10, 0.01)
        z = self(X)
        plt.plot(X, z[0], label='$X$')
        plt.plot(X, z[1], label='$\dot X$')
        plt.plot(X, z[2], label= '$\ddot X$')
        plt.legend(loc='upper right')
        plt.show()

    def test_ls(self):
        X = np.arange(0, 10, 0.01)
        z = self(X)
        print(np.linalg.lstsq(np.hstack((z[0][:, np.newaxis], z[1][:, np.newaxis])), -z[2]))

