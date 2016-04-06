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

def getPlotData(n,rss:list):
    cp = []
    fpe = []
    t = np.arange(1,len(rss)+1)
    for i in range(rss):
        s = i+1
        cp.append(rss[i] + 2*s)
        fpe.append((n+s)/(n-s)*rss[i])
    return t,rss, cp, fpe

def plot(t, r1,r2, r3):
    plt.plot(t,r1, label = 'RSS')
    plt.plot(t,r2, label = 'CP')
    plt.plot(t,r3, label = 'FPE')

    plt.xlabel(r'$s$')
    plt.grid(True)
    plt.title(r'$Criteria$')
test()



