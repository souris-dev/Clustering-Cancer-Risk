"""
Cluster class for Module 3
"""

import math
import alg_cluster

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """

    (dist, idx1, idx2) = (float('inf'), -1, -1)

    for cli1 in range(len(cluster_list)):
        for cli2 in range(len(cluster_list)):
            if (cli1 == cli2):
                continue

            (dist, idx1, idx2) = min((dist, idx1, idx2), (cluster_list[cli1].distance(cluster_list[cli2]), cli1, cli2))
    
    if (idx1 > idx2):
        idx1, idx2 = idx2, idx1

    return (dist, idx1, idx2)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    part_cl_idx = []

    for idx in range(len(cluster_list)):
        if (abs(cluster_list[idx].horiz_center() - horiz_center) < half_width):
            part_cl_idx.append(idx)

    part_cl_idx.sort(key = lambda idx: cluster_list[idx].vert_center())

    n_part_cl = len(part_cl_idx)

    (dist, idx1, idx2) = (float('inf'), -1, -1)

    for cl1 in range(0, n_part_cl - 1):
        for cl2 in range(cl1 + 1, min(cl1 + 3, n_part_cl - 1) + 1):

            (dist, idx1, idx2) = min((dist, idx1, idx2), 
            (cluster_list[part_cl_idx[cl1]].distance(cluster_list[part_cl_idx[cl2]]), 
            part_cl_idx[cl1], part_cl_idx[cl2]))

    if (idx1 > idx2):
        idx1, idx2 = idx2, idx1

    return (dist, idx1, idx2)


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    n_clusters = len(cluster_list)

    if (n_clusters <= 3):
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)

    else:
        m_clusters = int(n_clusters / 2)
        l_cluster_list = cluster_list[:m_clusters]
        r_cluster_list = cluster_list[m_clusters:]

        l_cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        r_cluster_list.sort(key = lambda cluster: cluster.horiz_center())

        (dist_l, idx1_l, idx2_l) = fast_closest_pair(l_cluster_list)
        (dist_r, idx1_r, idx2_r) = fast_closest_pair(r_cluster_list)

        (dist, idx1, idx2) = min((dist_l, idx1_l, idx2_l), (dist_r, idx1_r + m_clusters, idx2_r + m_clusters))

        mid = (cluster_list[m_clusters - 1].horiz_center() + cluster_list[m_clusters].horiz_center()) / 2

        (dist, idx1, idx2) = min((dist, idx1, idx2), closest_pair_strip(cluster_list, mid, dist))

    return (dist, idx1, idx2)



######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """

    # We've been allowed to mutate cluster_list
    n_clusters = len(cluster_list)

    while (n_clusters > num_clusters):
        # need to sort on the basis of x coord to use fast_closest_pair
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())

        (dummy_dist, idx1, idx2) = fast_closest_pair(cluster_list)
        cluster_list[idx1].merge_clusters(cluster_list[idx2])
        cluster_list.remove(cluster_list[idx2])

        n_clusters = len(cluster_list)
    
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    n_clusters = len(cluster_list)
    cl_temp = cluster_list[:]

    # take the n largest counties by population, where n = num_clusters
    # as centers
    cl_temp.sort(key = lambda cluster: cluster.total_population(), reverse=True)
    centers = cl_temp[:num_clusters]

    for dummy_i in range(num_iterations):
        clusters_f = [alg_cluster.Cluster(set(), 0, 0, population=0, risk=0) for dummy_i in range(num_clusters)]

        for j_count in range(0, n_clusters):
            this_cluster = cluster_list[j_count]
            distances = [this_cluster.distance(center) for center in centers]
            nearest_d = min(distances)
            nearest_d_idx = distances.index(nearest_d)

            clusters_f[nearest_d_idx].merge_clusters(this_cluster)

        centers = clusters_f

    return centers
