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
        return ksi_un(np.sqrt(3*scale), size = size)
    else:
        return np.random.normal(0, np.sqrt(scale), size)


def manage(n = 10, m = 3, Theta = np.array([]), X=np.array([]),ksi = np.array([])):
    assert(Theta.shape[0] == m and Theta.shape[1] == 1)
    assert(X.shape == (n,m))
    assert(n > m)
    y = get_y(X, Theta)
    y_ksi = y+ksi
    theta = []
    rss = []
    for Theta, Rss in recursive_lsq(X, y_ksi.T[0]):
        theta.append(Theta)
        rss.append(Rss)
    y_real = np.dot(X, theta[-1])
    t, r1, r2, r3 = getPlotData(n, rss)
    ret = dict(y_gen = y, y_ksi = y_ksi, y_restored = y_real,rsa = r1, cp = r2, fse = r3)
    return ret

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

def plot(r1,r2, r3):
    t = np.arange(1,len(r1)+1)
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

#Theta = np.array([1, 2, 3])[:, np.newaxis]
#manage(Theta = Theta)




