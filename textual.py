import numpy as np

def make_data(observations,labels,d,N):
    data_lines = np.array([np.append(observations[i], [labels[i]]) for i in range(N)])

    if (d == 2):
        fmt = '%1.8f', '%1.8f', '%d'
    else:
        fmt = '%1.8f', '%1.8f', '%1.8f', '%d'

    np.savetxt('data.txt', data_lines, fmt=fmt, delimiter=',')

def cluster_to_txt(cluster, out, k, N):
    for i in range(k):
        for j in range(N - 1):
            if (cluster[i * N + (j + 1)] == 0):
                out += str(cluster[i * N + j])
                break
            else:
                out += str(cluster[i * N + j]) + ","
        out += "\n"
    return out

def make_cluster_txt(clusters_spectral, clusters_kmean, k, N):
    clusters_file = open('clusters.txt','w')
    out = str(k) + "\n"
    out = cluster_to_txt(clusters_spectral, out, k, N)
    clusters_file.write(cluster_to_txt(clusters_kmean, out, k, N))
    clusters_file.close()

