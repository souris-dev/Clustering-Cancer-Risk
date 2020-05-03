"""
Application, Module 3, Question 1
"""

import random
from runtime_test_main import *
import time

def gen_random_clusters(num_clusters):
    clusters = []
    
    for dummy_i in range(num_clusters):
        x = (random.randint(-1000, 1000)) / 1000
        y = (random.randint(-1000, 1000)) / 1000

        clusters.append(ClusterTest(x, y))

    return clusters

def gen_test_report_csv():
    listof_cluster_list = [gen_random_clusters(n_cls) for n_cls in range(2, 201)]

    # This will store a list of strings
    # For writing in a csv file
    # Of format: n_clusters,runtime_slow_closest_pair,runtime_fast_closest_pair
    runtimes = []

    for cluster_list in listof_cluster_list:
        t0_sl = time.time();
        slow_closest_pair(cluster_list)
        time_sl = time.time() - t0_sl

        t0_ft = time.time()
        cluster_list.sort(key = lambda cluster: cluster.x)
        fast_closest_pair(cluster_list)
        time_fast = time.time() - t0_ft


        csv_str = str(len(cluster_list)) + ',' + str(time_sl) + ',' + str(time_fast)
        runtimes.append(csv_str)
        print(csv_str)

    with open('runtimes.csv', 'w') as csv_out:
        csv_out.write('n_clusters,slow_closest_pair,fast_closest_pair\n')
        for line in runtimes:
            csv_out.write(line + "\n")