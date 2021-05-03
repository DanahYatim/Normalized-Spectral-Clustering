"""
    The Visualization Module.
    This module will  output a PDF file named clusters.pdf, containing
    the visualization and information on the clusters we have calculated.
"""
import itertools
import matplotlib.pyplot as plt

def cluster_to_list(cluster,k,N):
    cluster_lines = []
    for i in range(k):
        line = []
        for j in range(N):
            if (cluster[i * N + j] == 0 and j != 0):
                break
            line.append(cluster[i * N + j])
        cluster_lines.append(line)
    return cluster_lines

def color_labels(clusters_list,N):
    color = [0 for i in range(N)]
    for i in range(len(clusters_list)):
        rgb = i
        for j in clusters_list[i]:
            color[j] = rgb
    return color

def label_pairs(labels,K):
    cluster_labels = [[] for i in range(K)]
    for i in range(len(labels)):
        cluster_labels[labels[i]].append(i)
    final_labels = set()
    for i in cluster_labels:
        i.sort()
        final_labels = final_labels.union(set(itertools.combinations(i,2)))
    return final_labels

def calc_jac(labels,spectral_label,kmeans_label,K,k):
    true_pairs = label_pairs(labels,K)
    spectral_pairs = label_pairs(spectral_label,k)
    kmeans_pairs = label_pairs(kmeans_label,k)
    spec_jac = len(true_pairs.intersection(spectral_pairs))/len(true_pairs.union(spectral_pairs))
    kmeans_jac = len(true_pairs.intersection(kmeans_pairs))/len(true_pairs.union(kmeans_pairs))
    return spec_jac,kmeans_jac

def visualize(labels,observations,clusters_spectral,clusters_kmean,d,K,k,N):
    
    spectral_list = cluster_to_list(clusters_spectral,k,N)
    kmeans_list = cluster_to_list(clusters_kmean,k,N)
    fig = plt.figure()
    spectral_label = color_labels(spectral_list, N)
    kmeans_label = color_labels(kmeans_list,N)
    if (d == 2):
        x= list(observations[:,0])
        y = list(observations[:,1])
        ax1 = fig.add_subplot(2, 2,1)
        ax1.scatter(x,y, c=spectral_label)
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.scatter(x,y, c=kmeans_label)
    else:
        x= list(observations[:,0])
        y = list(observations[:,1])
        z = list(observations[:,2])
        ax1 = fig.add_subplot(2, 2,1, projection='3d')
        ax1.scatter(x,y,z, c=spectral_label)
        ax2 = fig.add_subplot(2, 2, 2, projection='3d')
        ax2.scatter(x,y, z, c=kmeans_label)
  
    ax1.set_title('Normalized Spectral Clustering')
    ax2.set_title('K-means')
    spec_jac, kmeans_jac = calc_jac(labels, spectral_label, kmeans_label, K, k)
    
    fig.suptitle(f"""
        Data was generated from the values:\n
        n = {N} , k = {K}\n
        The k that was used for both algorithms was {k}\n
        The Jaccard measure for Spectral Clustering: {spec_jac}\n
        The Jaccard measure for K-means: {kmeans_jac}""",x=0.5, y=0.4)

    plt.savefig('clusters.pdf')

    

