import numpy as np
import math

def GramSchmidt(A):
    """
    input: matrix nXn
    output: Q and R matrix as described in Gram Schmidt algorithm
    """
    U = np.copy(A)
    n = np.size(A, 0)  # n is the number or rows
    # init R and Q to zero
    R = np.zeros(np.shape(A), np.float64)
    Q = np.zeros(np.shape(A), np.float64)
    for i in range(n):
        R[i, i] = np.linalg.norm(U[:, i])  # compute l2 norma with numpy

        if R[i, i] != 0:
            Q[:, i] = U[:, i] / R[i, i]

        R[i][i + 1:n] = np.transpose(Q[:, i]) @ U[:, i + 1:n]
        temp = (R[i][:, np.newaxis] * Q[:, i])
        U[:, i + 1:n] = U[:, i + 1:n] - temp.transpose()[:, i + 1:n]

    return Q, R
def QRIterationAlgorithm(A):
    """
        input: matrix nXn
        output: A and Q matrix as described in QRIterationAlgorithm
        """
    Ac = np.copy(A)
    n = np.size(A, 0)  # n is the number or rows
    Qc = np.eye(n)  # init to I matrix
    for i in range(n):
        (Q, R) = GramSchmidt(Ac)
        Ac = R @ Q
        newQ = Qc @ Q
        dist = np.abs(Qc) - np.abs(newQ)  # dist is a matrix nXn with the distances of each cell
        if np.all(np.abs(dist) <= 0.0001):  # check if all cells are between [-epsilon,epsilon]
            return Ac, Qc
        Qc = newQ

    return Ac, Qc

def ComputeUnK(Lnorm, n, inputK, Random):
    """
        input: matrix Lnorm nXn, int n
        output: matrix U nXk represent the first k eigenvector  of Q (from QRIterationAlgorithm)
                int k - the Eigengap Heuristic
        """
    (Ac, Qc) = QRIterationAlgorithm(Lnorm)
    eigenvalues = Ac.diagonal()  # array of the eigenvalues
    Qc = np.concatenate((Qc, np.array([eigenvalues])), axis=0)  # adding eigenvalues to last row
    Qc = Qc[:, Qc[n].argsort()]  # sorting columns ny last row
    eigenvalues = Qc[n]  # last row of eigenvalues is now sorted
    delta = np.abs(np.diff(eigenvalues))  # calculating The Eigengap Heuristic
    if Random:
        k = np.argmax(delta[:math.floor((n) / 2)]) + 1
    else:
        k = inputK
    Qc = Qc[:n, :]
    U = Qc[:, :k]  # take the first k eigenvectors which they are already sorted by their eigenvalues
    print(U)
    return U, k