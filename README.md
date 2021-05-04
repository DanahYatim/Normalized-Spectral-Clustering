# Normalized-Spectral-Clustering

## By Guy & Danah

In this code we implement the Normalized Spectral Clustering technique. 
A clustering technique which performs the Laplacian Eigenmaps method, a non-linear dimension reduction method, before clustering in fewer dimensions. 

The method which we use for actual clustering is the k-means algorithm with the improved initialization algorithm - k-means++.

We will compare Normalized Spectral Clustering results to those of the k-means++ Algorithm. Our results will be reflected in the Visualization Module.

## Languages

Our code is mostly implemented in python except for the k-means algorithm itself which is implemented in C.

## Modules

The code consists of 4 main modules:

### Main
The Main module will act as the glue for our entire project.
We receive 3 Command-Line Arguments are transferred from invoke command named run:
K - number of clusters we wish to produce.
N - number of observations.
Random - If Random is set to True, k will be computed using the eigengap heuristic and used for them both.
Otherwise, both will set k to be K.



### Spectral Clustering Module 
 The Spectral Clustering module implements the Normalized Spectral Clustering Algorithm.
 More specifically, implements the Laplacian Eigenmaps dimension reduction method,
 and then send the new observations to the kmenas-pp module for running the kmeans algorithm.
 
### kmeans_pp Module
 The kmeans_pp module implements the k_means++ Algorithm for initializing optimal centroids.
 and send our data to the C modules to compute k_means in C, usung CAPI Python extensions.

### kmeans c Module
The kmeans c module implements the k-means Algorithm in C.

### Visualization Module
The Visualization Module will  output a PDF file named clusters.pdf, containing
the visualization and information on the clusters we have calculated.

## How To Run


 
