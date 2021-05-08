'''
Author: Neeraj Sharma: neerajsharma@umass.edu
'''

from sklearn.cluster import KMeans
import pandas as pd
import time
import os


def get_k_means_clusers(df, num_clusers, partition_path):
    '''

    :param df: input dataframe
    :param num_clusers: num of clusters
    :param partition_path: path to store partitions with group id
    :return:
    '''
    kmeans = KMeans(n_clusters=num_clusers, random_state=0).fit(df)
    df['gid'] = kmeans.labels_
    df.to_csv(partition_path)


num_clusters = [100, 200, 500, 1000]

for num_cluster in num_clusters:
    start_time = time.time()
    df = pd.read_csv(os.path.join(os.curdir, '/data/tpch.csv'), sep=',')
    partition_path = os.path.join(os.curdir, '/data/partition_kmeans{}.csv'.format(num_cluster))
    get_k_means_clusers(df, num_cluster)
    end_time = time.time()
    print("time taken for creating {} partitions with K Means is {}".format(num_cluster, end_time - start_time))
