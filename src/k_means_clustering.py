'''
Author: Neeraj Sharma: neerajsharma@umass.edu
'''

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

df = pd.read_csv('../data/tpch.csv', sep=',')

kmeans = KMeans(n_clusters=1047, random_state=0).fit(df)

df['gid'] = kmeans.labels_

df.to_csv('../data/partitions_k_means_1047.csv')

print("done")


