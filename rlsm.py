import numpy as np


def recursive_lsq(w: np.array, y: np.array):
    assert(w.shape[0] == y.shape[0])
    m = w.shape[1]
    def theta_generator():
        a = 0
        beta = eta = np.dot(w[:, 0], w[:, 0])
        gamma = np.dot(w[:, 0], y)
        nu = gamma / beta
        theta = np.array([nu])
        vec = y - w[:,0] * theta
        rss = np.dot(vec, vec)
        yield theta, rss
        H_inv = np.array([[1/beta]])
        for i in range(1, m):
            h = np.dot(w[:, i], w[:, :i])
            a = np.dot(H_inv, h)
            eta = np.dot(w[:, i], w[:, i])
            gamma = np.dot(w[:, i], y)
            beta = eta - np.dot(h, a)
            nu = (gamma - np.dot(theta, h)) / beta
            theta -= nu * a
            theta = np.hstack((theta, nu))
            rss -= nu**2*beta
            yield theta, rss
            h11 = H_inv + np.dot(a[:, np.newaxis], a[np.newaxis, :]) / beta
            h12 = -a[:, np.newaxis] / beta
            h21 = -a / beta
            h22 = 1 / beta
            H_inv = np.vstack((np.hstack((h11, h12)), np.hstack((h21, h22))))
    return theta_generator()



def test():
    for theta in recursive_lsq(np.array([[1, 1, 2], [3, 4, 5], [5, 6, 7]]), np.array([1, 2, 3])):
        print(theta)
    print(np.linalg.lstsq(np.array([[1, 1, 2], [3, 4, 5], [5, 6, 7]]), np.array([1, 2, 3])))

def test2():
    X = np.identity(4)
    y = np.arange(4)
    for i in range(4):
        X[i, 0] = 1
    theta_list = [theta for theta in recursive_lsq(X, y)]
    print(np.dot(X, theta_list[-1]))