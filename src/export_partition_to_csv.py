import partitioning as p
import pandas as pd
import time

start = time.time()
df = pd.read_csv('data/tpch.csv', sep=',')
path = '../data/'
partition_filename = 'partition_max_1000000.csv'
representative_filename = 'representatives_max_1000000.csv'

tau = 100000
partition_attributes = ['sum_base_price', 'sum_disc_price', 'sum_charge', 'avg_qty', 'avg_price', 'avg_disc', 'sum_qty',
                        'count_order', 'p_size', 'ps_min_supplycost', 'revenue', 'o_totalprice', 'o_shippriority']

# partition = pd.read_csv('../data/partition_1000000.csv')
partition = p.partition(df, tau, partition_attributes)

representatives = p.get_representative_for_group(partition, partition_attributes)

partition['gid'].to_csv(path + partition_filename)
representatives.to_csv(path + representative_filename)

end = time.time()
print(end - start)



