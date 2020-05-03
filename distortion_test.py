"""
Application, Module 3, Question 7
Testing distortions of clusters
"""

from alg_project3_viz import *
import alg_project3_solution as cluster_algs

def compute_distortion(cluster_list, data_table, out_size):
    clust_list = cluster_list[:]

    # note that hierarchical_clustering mutates cluster_list
    clusters_k = cluster_algs.kmeans_clustering(clust_list, out_size, 5)
    clusters_h = cluster_algs.hierarchical_clustering(cluster_list, out_size)

    distortion_h = 0
    distortion_k = 0

    for cluster_h in clusters_h:
        distortion_h += cluster_h.cluster_error(data_table)

    for cluster_k in clusters_k:
        distortion_k += cluster_k.cluster_error(data_table)

    return (distortion_h, distortion_k)
    

def get_distortions(data_url, out_size, prev_rec=False):
    data_table = load_data_table(data_url)

    cluster_list = []
    for line in data_table:
        cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    (distortion_h, distortion_k, _, _1) = compute_distortion(cluster_list, data_table, out_size)

    return distortion_h, distortion_k


def compute_distortion_2(cluster_list, cluster_list_h, data_table, out_size):
    clust_list = cluster_list[:]

    # note that hierarchical_clustering mutates cluster_list
    clusters_k = cluster_algs.kmeans_clustering(clust_list, out_size, 5)
    clusters_h = cluster_algs.hierarchical_clustering(cluster_list_h, out_size)

    distortion_h = 0
    distortion_k = 0

    for cluster_h in clusters_h:
        distortion_h += cluster_h.cluster_error(data_table)

    for cluster_k in clusters_k:
        distortion_k += cluster_k.cluster_error(data_table)

    return (distortion_h, distortion_k, clusters_h, clusters_k)



def prep_distortions_data_csv():
    h_cl_dists = []
    k_cl_dists = []

    tbl_type = ['111', '290', '896']
    tbl_type_i = 0

    for url in (DATA_111_URL, DATA_290_URL, DATA_896_URL):
        data_table = load_data_table(url)

        cluster_list = []
        cluster_list_h = []

        for line in data_table:
            cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
            cluster_list_h.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

        for i in reversed(range(6, 21)):
            (distortion_h, distortion_k, clusters_h, clusters_k) = compute_distortion_2(cluster_list, cluster_list_h, data_table, i)

            h_cl_dists.append(distortion_h)
            k_cl_dists.append(distortion_k)

            cluster_list_h = clusters_h

        # they store data in reverse order right now
        h_cl_dists.reverse()
        k_cl_dists.reverse()

        with open('distortions_' + tbl_type[tbl_type_i] + '.csv', 'w') as data_out:
            data_out.write('n_out_clusters,h_clustering,k_m_clustering\n')

            for i in range(6, 21):
                data_out.write(str(i) + ',' + str(h_cl_dists[i - 6]) + ',' + str(k_cl_dists[i - 6]) + '\n')

        tbl_type_i += 1