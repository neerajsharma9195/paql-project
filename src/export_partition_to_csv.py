import partitioning as p
import pandas as pd
import time

start = time.time()
df = pd.read_csv('data/tpch.csv', sep=',')
path = '/Users/Thomas/Documents/Umass Amherst/CICS 645/Project/'
partition_filename = 'partition_100000.csv'
representative_filename = 'representative_100000.csv'

tau = 100000
partition_attributes = ['sum_base_price', 'sum_disc_price', 'sum_charge', 'avg_qty', 'avg_price', 'avg_disc', 'sum_qty',
                        'count_order', 'p_size', 'ps_min_supplycost', 'revenue', 'o_totalprice', 'o_shippriority']
partition = p.partition(df, tau, partition_attributes)
representatives = p.get_representative_for_group(partition, partition_attributes)

partition['gid'].to_csv(path + partition_filename)
representatives.to_csv(path + representative_filename)

end = time.time()
print(end - start)



