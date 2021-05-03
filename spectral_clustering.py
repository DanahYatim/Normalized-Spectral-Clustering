"""
    The Normalized Spectral Clustering Module.
    In this module we will implement the Normalized Spectral Clustering Algorithm.
    More specifically, we will implement the Laplacian Eigenmaps dimension reduction method,
    and then send the new observations to the kmenas-pp module for running the kmeans algorithm.
"""

import numpy as np
import pandas as pd
import kmeans_pp
from constant import EPSILON

# Forming the weighted adjacency matrix W from V.

def form_W(V):
    n = len(V)
    W = np.zeros((n, n),dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if(i != j):
                W[i][j] = np.exp(-np.linalg.norm(V[i] - V[j]) * 0.5)
    return W

# Computing the normalized graph Laplacian - Lnorm

def compute_Lnorm(W):
    D = np.zeros_like(W, dtype=np.float64)
    diag = W.sum(axis=1)
    diag = pow(diag, -0.5)
    np.fill_diagonal(D, diag)
    I = np.identity(len(W),dtype=np.float64)
    Lnorm = I - D @ W @D
    return Lnorm

# Finding Eigenvalues and Eigenvectors using the QR-Iteration and Gram-Schmidt algorithms.

def gram_schmidt(A,N):
    U = np.copy(A)
    R = np.zeros_like(U,dtype=np.float64)
    Q = np.zeros_like(U,dtype=np.float64)
    for i in range(N):
        R[i][i] = np.linalg.norm(U[:,i])
        if R[i][i] != 0:
            Q[:,i]=U[:,i]/R[i][i]
        R[i][i + 1:N] = np.transpose(Q[:, i]) @ U[:, i + 1:N]
        t= (R[i][:, np.newaxis] * Q[:, i])
        U[:,i + 1:N] = U[:,i + 1:N] - t.transpose()[:, i + 1:N]
    return Q,R


def QR_Iteration(A,N):
    new_A = np.copy(A)
    hat_Q = np.identity(N,dtype=np.float64)
    
    for i in range(N):
        Q, R = gram_schmidt(new_A,N)
        new_A = R@Q
        new_Q  = hat_Q @ Q
        dist = np.abs(hat_Q)-np.abs(new_Q)
        if np.all(np.abs(dist) <= EPSILON):
            return new_A,hat_Q
        hat_Q = new_Q

    return new_A,hat_Q

# In this function we will:
# 1.Determining k and the first k eigenvectors of Lnorm.
# 2.Form the U matrix containg the first K eigenvectors of Lnorn as columns.
# 3.Form the T matrix by renormalizing each of U's rows to have a unit lenght.

def form_T(A, Q,N, Random, K):
    Eigenvalues = pd.Series(np.diag(A))
    df = pd.DataFrame({'col_1':Eigenvalues})
    df = df.sort_values('col_1')
    sorted_eigenvalues = df['col_1'].tolist()
    k = K
    if(Random):
        k = compute_K(sorted_eigenvalues,N)
        
    index = df.index
    U = Q[:,index[:k]]
    normalize = np.linalg.norm(U,axis=1)
    T = U/np.array([normalize]).T
    return T,k

def compute_K(sorted_eigenvalues,N):
    diff = np.diff(sorted_eigenvalues)
    k = np.argmax(diff[:(N // 2)]) + 1
    return k



# This function will act as the glue for our Normalized Spectrul Clustering Algorithm.

def normalized_spectral_clustering(observations, Random, K, N):
    W = form_W(observations)
    Lnorm = compute_Lnorm(W)
    new_A, new_Q = QR_Iteration(Lnorm,N)
    T, k = form_T(new_A, new_Q,N, Random, K)
    d = k
    clusters = kmeans_pp.kmeans_plus_plus(k,N,d,300,T)
    return clusters,k





