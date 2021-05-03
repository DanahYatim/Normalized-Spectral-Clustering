"""
    The kmeans_pp Module.
    In this module we will implement the k_means++ Algorithm for initializing optimal centroids.
    and send our data to the C modules to compute k_means in C, usung CAPI Python extensions.
"""

import mykmeanssp as kmeans
import pandas as pd
import numpy as np


def distance(x,c):
    x = x-c
    x=np.apply_along_axis(lambda t: t**2,1,x)
    x= np.sum(x,axis=1)
    return x


def k_means_pp(K,N,d,observations):
    np.random.seed(0)
    i_1 = np.random.choice(N,1).tolist()[0]
    centroids = np.array([observations[i_1]])
    min_distance = distance(observations, centroids[0])
    centroids_index = np.array([i_1])
    for i in range(0,K-1):
            cendtroid_distance_2 = distance(observations,centroids[i])
            min_distance = np.minimum(min_distance,cendtroid_distance_2)
            sum_min_distance = np.sum(min_distance)
            j = np.random.choice(N,1,p = min_distance/sum_min_distance).tolist()[0]
            centroids = np.append(centroids,np.array([observations[j]]),  axis=0)
            centroids_index = np.append(centroids_index,np.array([j]))
    centroids2 = list()
    for i in centroids:
        for j in i:
            centroids2.append(j)
    return centroids2



def kmeans_plus_plus(k,N,d,MAX_ITER,observations):
    observations_in_a_row = list()
    for i in observations:
        for j in i:
            observations_in_a_row.append(j)
    centroids = k_means_pp(k,N,d,observations)
    try:
        x = kmeans.k_means(k,N,d,MAX_ITER,centroids,observations_in_a_row)
    except(AssertionError):
        exit(1)
    except(TypeError):
        exit(1)
    return(x)

