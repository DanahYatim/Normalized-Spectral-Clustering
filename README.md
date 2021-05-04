# Normalized-Spectral-Clustering

## By Guy & Danah

In this code we implement the Normalized Spectral Clustering technique. 
A clustering technique which performs the Laplacian Eigenmaps method, a non-linear dimension reduction method, before clustering in fewer dimensions. 

The method which we use for actual clustering is the k-means algorithm with the improved initialization algorithm - k-means++.

We will compare Normalized Spectral Clustering results to those of the k-means++ Algorithm. Our results will be reflected in the Visualization Module.

if you wish to run the code, skip to the 'How To Run' sub-title!

## Modules

The code consists of 4 main modules:

### Main
The Main module will act as the glue for our entire project.

#### Input
We receive 3 Command-Line Arguments are transferred from invoke command named run:
K - number of clusters we wish to produce.
N - number of observations.
Random - If Random is set to True k (the number of clusters) will be computed using the eigengap heuristic and used for both the Normalized Spectral Clustering and the kmeans++.
Otherwise, both will set k to be K.
Additionaly, if Random is set to true N and K will be chosen randomly from there max capacity options.
Otherwise, both will be set to the original command line arguments.

#### Max capacity
we will calculate the maximum capacity of N and K so that our program will not exceed more then 5 minutes. 
we will calculate in consideration to dimensiolity of the observations.

#### Generate Data
we will randomly chose the observations dimension to be either 2-dimensional or 3-dimensional.
And then generate N observations for clustering with there following labels for potentiol K-clusters (using skrleans make_blobs function).

#### Computing The Clusters Using The 2 Algorithms
The program will compute the clusters using two algorithms: the Normalized Spectral Clustering and K-means.
It will output a file with the resulting clusters from both algorithms.
and finally, output a visualization file comparing the resulting clusters of the two algorithms (explained more in the Visualization Model).
### Spectral Clustering
 The Spectral Clustering module implements the Normalized Spectral Clustering Algorithm.
 More specifically, implements the Laplacian Eigenmaps dimension reduction method,
 and then send the new observations to the kmenas-pp module for running the kmeans algorithm.
 
### kmeans_pp
 The kmeans_pp module implements the k_means++ Algorithm for initializing optimal centroids.
 and send our data to the C modules to compute k_means in C, usung CAPI Python extensions.

### kmeans c
The kmeans c module implements the k-means Algorithm in C.

### Visualization
The Visualization Module will  output a PDF file named clusters.pdf, containing
the visualization and information on the clusters we have calculated.

## How To Run
Random is set by default to true so if you wish to run with Random:
Run from Terminal:
   python3.8.5 -m invoke run -k [k] -n [n].
   
otherwise, if you do not want Random to be true:
Run from Terminal:
   python3.8.5 -m invoke run -k [k] -n [n] [--[no-]Random]

 
