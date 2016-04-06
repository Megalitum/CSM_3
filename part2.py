import numpy as np

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
        return ksi_un([scale], size)
    else:
        return np.random.normal(0, scale, size)


def test():
    n = 10
    m = 5
    scale = 3
    distr_ksi = False
    ksi = distr(distr_ksi, scale, m)
    scale_x = [3,6]
    X = ksi_un(scale_x, size = (n,m))
    print(X, ksi)

test()



