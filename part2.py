import numpy as np
import matplotlib.pyplot as plt
from rlsm import *


def ksi_un(*level, size):
    """
    generate uniform distr with size = size
    :param level: level = [a, b]
    :param size:
    :return:
    """
    if len(level) ==1:
        a = -level[0]
        b = -a
    else:
        a = level[0]
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


def manage(n = 10, m = 3, scale = 1, scale_x_a = 0, scale_x_b = 1, distr_ksi = False, Theta = np.array([])):
    assert(Theta.shape[0] == m and Theta.shape[1] == 1)
    assert(n > m)
    ksi = distr(distr_ksi, scale, size = (n,1))
    X = ksi_un(scale_x_a, scale_x_b, size = (n,m))
    y = get_y(X, Theta)
    y_ksi = y+ksi
    rss = []
    for theta, rsss in recursive_lsq(X, y_ksi.T[0]):
        rss.append(rsss)
    t, r1, r2, r3 = getPlotData(n, rss)
    plot(t,r1, r2, r3)
    input()

def get_y(X, theta):
    return np.dot(X, theta)

def getPlotData(n,rss:list):
    cp = []
    fpe = []
    t = np.arange(1,len(rss)+1)
    for i in range(len(rss)):
        s = i+1
        cp.append(rss[i] + 2*s)
        fpe.append((n+s)/(n-s)*rss[i])
    return t, rss, cp, fpe

def plot(t, r1,r2, r3):
    assert(len(t) == len(r1) == len(r2) == len(r3))
    plt.plot(t,r1, label = 'RSS')
    plt.plot(t,r2, label = 'CP')
    plt.plot(t,r3, label = 'FPE')

    plt.xlabel(r'$s$')
    plt.grid(True)
    plt.title(r'$Criterion$')
    plt.show()
    pass


#X = np.array([[1, 1, 2], [3, 4, 5], [5, 6, 7]])

Theta = np.array([1, 2, 3])[:, np.newaxis]
manage(Theta = Theta)




