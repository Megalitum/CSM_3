import numpy as np


def framing_lstsq(X, y):
    """
    Compute Framing Least Squares

    Returns
    -------
    theta
    rss
    """

    n, m = X.shape
    a = np.zeros((1, 1))
    H = np.zeros((1, 1))
    H[0][0] = 1. / np.dot(X[:, :1].T, X[:, :1])[0][0]
    beta = np.dot(X[:, :1].T, X[:, :1])
    eta =  np.dot(X[:, :1].T, X[:, :1])
    theta = np.array([[np.dot(X[:, :1].T, y) / np.dot(X[:, :1].T, X[:, :1])]])

    rss = np.zeros((1, m))
    rss[0][0] = np.dot(y.T, y - np.reshape((theta * X[:, :1]), (n, )))
    #rss[1][0] = rss[0][0] + 2
    #rss[2][0] = rss[0][0] / (n + 1) * (n - 1)

    for s in range(1, m):
        h = np.dot(X[:, :s].T, X[:, s:s + 1])
        a = np.dot(H, h)
        eta = np.dot(X[:, s:s + 1].T, X[:, s:s + 1])
        beta = eta - np.dot(h.T, a)
        gamma = np.dot(X[:, s:s + 1].T, y)
        t = (gamma - np.dot(h.T, theta)) / beta
        theta_star = theta - t * a
        H = (np.vstack((np.hstack((H + 1. / beta * np.dot(a, a.T), -1. / beta * a)),
                        np.hstack((-1. / beta * a.T, 1. / beta))))).reshape((s + 1, s + 1))
        theta = (np.vstack((theta_star, t))).reshape((s + 1, 1))

        rss[0][s] = rss[0][s - 1] - t * t * beta
        #rss[1][s] = rss[0][s] + 2 * (s + 1)
        #rss[2][s] = rss[0][s] * (n + s + 1) / (n - s - 1)

    return np.reshape(theta, (m,)), rss

#X = np.transpose(np.array([np.array([1] * 5), np.arange(5)]))
#y = X[:, 0] + X[:, 1]
X = np.identity(4)
for i in range(4):
    X[i,0] = 1
y = np.arange(4)

print(X)
theta, rss = framing_lstsq(X, y)
print('theta',theta)
print('X,theta', np.dot(X, theta))
print('rss',rss)
