import partitioning as p
import pandas as pd
import time
import math


def export_partition(input_df, tau):
    start = time.time()
    df = pd.read_csv('data/tpch.csv', sep=',')
    partition_attributes = df.columns.tolist()
    file_name = 'partition_' + str(tau) + '.csv'
    partition = p.partition(input_df, tau, partition_attributes)
    partition.to_csv('data/' + file_name)
    end = time.time()
    print('time to export: {}'.format(str(end - start)))


def export_representative(tau, size, minmax, kmeans=False):
    start = time.time()
    df = pd.read_csv('data/tpch.csv', sep=',')
    partition_attributes = df.columns.tolist()
    if kmeans is False:
        partition_filename = 'partition_' + str(tau) + '.csv'
        partition = pd.read_csv('data/' + partition_filename, index_col=0)
        file_name = 'representatives_' + minmax + '_' + str(int(size * 100)) + '_' + str(tau) + '.csv'
    else:
        kmeans = pd.read_csv('data/partition_kmeans100.csv', index_col=0)
        partition = df
        partition['gid'] = kmeans['gid']
        file_name = 'kmeans_representatives_' + minmax + '_' + str(int(size * 100)) + '.csv'
    partition = partition.head(math.ceil(len(partition) * size))
    if minmax == 'min':
        representatives = p.get_min_representative_for_group(partition, partition_attributes)
    if minmax == 'max':
        representatives = p.get_max_representative_for_group(partition, partition_attributes)
    representatives.to_csv('data/' + file_name)
    end = time.time()
    print('time to export: {}'.format(str(end - start)))


def export_q4_rep(tau, size, kmeans=False):
    start = time.time()
    partition_filename = 'partition_' + str(tau) + '.csv'
    df = pd.read_csv('data/tpch.csv')
    if kmeans is False:
        partition_filename = 'partition_' + str(tau) + '.csv'
        partition = pd.read_csv('data/' + partition_filename, index_col=0)
        file_name = 'representatives_q4_' + str(int(size * 100)) + '_' + str(tau) + '.csv'
    else:
        kmeans = pd.read_csv('data/partition_kmeans100.csv', index_col=0)
        partition = df
        partition['gid'] = kmeans['gid']
        file_name = 'kmeans_representatives_q4_' + str(int(size * 100)) + '.csv'
    representatives = partition.groupby('gid').agg(o_totalprice=pd.NamedAgg(column='o_totalprice', aggfunc='min'),
                                                   o_shippriority=pd.NamedAgg(column='o_shippriority', aggfunc='max'))
    representatives = representatives.reset_index()
    representatives.to_csv('data/' + file_name)
    counts = partition.groupby('gid').size().reset_index(name='counts')['counts']
    representatives['counts'] = counts
    representatives.to_csv('data/' + file_name)
    end = time.time()
    print('time to export: {}'.format(str(end - start)))


# Create offline partitions
df = pd.read_csv('data/tpch.csv')
export_partition(df, 10000000)
partition_1M = pd.read_csv('/Users/Thomas/Documents/Umass Amherst/CICS 645/Project/data/partition_1000000.csv',
index_col=0)
export_partition(partition_1M, 100000)
partition_100000 = pd.read_csv('data/partition_100000.csv', index_col=0)
export_partition(partition_100000, 10000)
partition_10000 = pd.read_csv('data/partition_10000.csv', index_col=0)
export_partition(partition_10000, 1000)

# Export representatives
export_representative(.1, 1000000, 'min')
export_representative(.4, 1000000, 'min')
export_representative(.7, 1000000, 'min')
export_representative(1, 1000000, 'min')
export_representative(.1, 1000000, 'max')
export_representative(.4, 1000000, 'max')
export_representative(.7, 1000000, 'max')
export_representative(1, 1000000, 'max')
export_q4_rep(1000000, .1)
export_q4_rep(1000000, .4)
export_q4_rep(1000000, .7)
export_q4_rep(1000000, 1)

# Load kmeans representatives
export_representative(None, .1, 'min', kmeans=True)
export_representative(None, .4, 'min', kmeans=True)
export_representative(None, .7, 'min', kmeans=True)
export_representative(None, 1, 'min', kmeans=True)
export_representative(None, .1, 'max', kmeans=True)
export_representative(None, .4, 'max', kmeans=True)
export_representative(None, .7, 'max', kmeans=True)
export_representative(None, 1, 'max', kmeans=True)
export_q4_rep(None, .1, kmeans=True)
export_q4_rep(None, .4, kmeans=True)
export_q4_rep(None, .7, kmeans=True)
export_q4_rep(None, 1, kmeans=True)



