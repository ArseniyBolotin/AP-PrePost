import numpy as np


def similarity(xi, xj):
    return -((xi - xj)**2).sum()


def update_r(n, S, A, R, damping):
    R_new = R.copy()
    for i in range(n):
        v = np.zeros(n)
        np.add(S[i, :], A[i, :], v)
        tmp_max = np.max(v)
        for k in range(n):
            if v[k] == tmp_max:
                tmp = v[k]
                v[k] = -np.inf
                R_new[i, k] = (S[i, k] - np.max(v))
                v[k] = tmp
            else:
                R_new[i, k] = (S[i, k] - tmp_max)
    if np.array_equal(R, R_new):
        return True
    else:
        R_new *= 1 - damping
        R *= damping
        R += R_new
        return False


def update_a(n, A, R, damping):
    A_new = A.copy()
    for k in range(n):
        v = np.array(R[:, k])
        v[v < 0] = 0
        tmp_sum = v.sum()
        for i in range(n):
            if i != k:
                A_new[i, k] = min(0, R[k, k] + (tmp_sum - v[i]))
            else:
                A_new[k, k] = tmp_sum
    if np.array_equal(A, A_new):
        return True
    else:
        A_new *= 1 - damping
        A *= damping
        A += A_new
        return False


def AffinityPropagation(x, max_iter, damping):
    n = x.shape[0]
    S = np.zeros((n, n))
    R = np.zeros((n, n))
    A = np.zeros((n, n))
    mediana_list = []
    for i in range(n):
        for j in range(n):
            mediana_list.append(similarity(x[i], x[j]))
            S[i, j] = similarity(x[i], x[j])

    diagonal = np.median(mediana_list)
    for i in range(n):
        S[i, i] = diagonal

    for i in range(max_iter):
        isEqualR = update_r(n, S, A, R, damping)
        isEqualA = update_a(n, A, R, damping)
        if isEqualR or isEqualA:
            break

    C = A + R
    labels = np.argmax(C, axis=1)
    return labels
