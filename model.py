# coding: utf-8

import numpy as np

class FadingOscillation(object):
    def __init__(self, *args, **kwargs):
        self.delta = args[0]
        self.omega0 = args[1]
        self.omega = np.sqrt(self.omega0**2 - self.delta**2)
        self.step = kwargs.get('step', 1e-7)
        self.A0 = kwargs.get('A0', 1)
        self.phi = kwargs.get('phi', 0)


