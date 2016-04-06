import numpy as np
import matplotlib.pyplot as plt

def ksi_un(*level, size):
    """
    generate uniform distr with size = size
    :param level: level = [a, b]
    :param size:
    :return:
    """
    a = -level[0]
    if len(level) ==1:
        b = -a
    else:
        b = level[1]
    return np.random.uniform(a,b,size)

def distr(distr, scale, size):
    """

    :param distr:
    :param scale:
    :param size:
    :return:
    """
    if distr == True:
        return ksi_un(scale, size = size)
    else:
        return np.random.normal(0, scale, size)


def test(n = 10, m = 5, scale = 3, scale_x_a = 3, scale_x_b = 6, distr_ksi = False):

    ksi = distr(distr_ksi, scale, size = (m,1))
    X = ksi_un(scale_x_a, scale_x_b, size = (n,m))

    print(X, ksi)

def get_y(X, theta):
    return np.dot(X, theta)

test()



