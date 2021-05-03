"""
    The Main Module.
    This module will act as the glue for our entire project.
"""

from sklearn.datasets import make_blobs
import random
import argparse
import spectral_clustering
import kmeans_pp
from textual import make_data,make_cluster_txt
from visualization import visualize
from error_check import check_input,checker
from constant import MAX_ITER,MAX_CAP_2D_K,MAX_CAP_2D_N,MAX_CAP_3D_K,MAX_CAP_3D_N

print("Maximum Capacity for 2 Dimensional is N:" + str(MAX_CAP_2D_N) + ", K:" + str(MAX_CAP_2D_K))
print("Maximum Capacity for 3 Dimensional is N:" + str(MAX_CAP_3D_N) + ", K:" + str(MAX_CAP_3D_K))

#The three Command-Line Arguments are transferred from invoke command name run.Now we evaluate and check the arguments.
parser = argparse.ArgumentParser()
parser.add_argument("K", type=checker)
parser.add_argument("N", type=checker)
parser.add_argument("--Random", default=True, action='store_false', help="Random")
args = parser.parse_args()
K = args.K
N = args.N
Random = args.Random
check_input(K,N,Random)

#Choosing the dimension to be either 2-dimensional or 3-dimensional.
d = random.choice([2,3])

if (d == 2):
    max_cap = MAX_CAP_2D_N
    max_K = MAX_CAP_2D_K
else:
    max_cap = MAX_CAP_3D_N
    max_K = MAX_CAP_3D_K

# If Random is set to True, k will be computed using the eigengap heuristic and used for them both.
# Otherwise, both will set k to be K.

if (Random):
    N = random.randint(max_cap//2,max_cap)
    K = random.randint(max_K//2,max_K)
    Rand_K = True
else:
    Rand_K = False

# The program will generate random points that will be used for clustering
observations,labels = make_blobs(n_samples = N, centers = K, n_features = d)


# The program will output a file containing the data points that were used.

make_data(observations,labels,d,N)

# The program will compute the clusters using two algorithms: the Normalized Spectral Clustering and K-means.

clusters_spectral, k = spectral_clustering.normalized_spectral_clustering(observations, Rand_K, K, N)
clusters_kmean = kmeans_pp.kmeans_plus_plus(k,N,d,MAX_ITER,observations)


# The program will output a file with the resulting clusters from both algorithms.

make_cluster_txt(clusters_spectral,clusters_kmean,k,N)

# The program will output a visualization file comparing the resulting clusters of the two algorithms.

visualize(labels,observations,clusters_spectral,clusters_kmean,d,K,k,N)









