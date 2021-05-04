# Normalized-Spectral-Clustering

## By Guy & Danah

In this code we implement the Normalized Spectral Clustering technique. 
A clustering technique which performs the Laplacian Eigenmaps method, a non-linear dimension reduction method, before clustering in fewer dimensions. 

The method which we use for actual clustering is the k-means algorithm with the improved initialization algorithm - k-means++.

## Languages

Our code is mostly implemented in python except for the k-means algorithm itself which is implemented in C.

## Modules

The code consists of 4 main modules:

### Main
The Main module will act as the glue for our entire project.

### Spectral Clustering Module 
 The Spectral Clustering module implements the Normalized Spectral Clustering Algorithm.
 More specifically, implements the Laplacian Eigenmaps dimension reduction method,
 and then send the new observations to the kmenas-pp module for running the kmeans algorithm.
 
### kmeans_pp Module
 The kmeans_pp module implements the k_means++ Algorithm for initializing optimal centroids.
 and send our data to the C modules to compute k_means in C, usung CAPI Python extensions.

### kmeans c Module
The kmeans c module implements the k-means Algorithm in C.

## How To Run


 
