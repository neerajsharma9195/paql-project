import partitioning as p
import pandas as pd
import time

start = time.time()
df = pd.read_csv('data/tpch.csv', sep=',')
df = df.head(1000)
path = '/Users/ananya/Documents/paql-project/data/'
partition_filename = 'partition_100000.csv'
representative_filename = 'representative_100000.csv'

tau = 0.1 * df.shape[0]
partition_attributes = ['sum_base_price', 'sum_disc_price', 'sum_charge', 'avg_qty', 'avg_price', 'avg_disc', 'sum_qty',
                        'count_order', 'p_size', 'ps_min_supplycost', 'revenue', 'o_totalprice', 'o_shippriority']
partition = p.partition(df, tau, partition_attributes)
representatives = p.get_representative_for_group(partition, partition_attributes)

partition['gid'].to_csv(path + partition_filename, header=['gid'])
representatives.to_csv(path + representative_filename)

end = time.time()
print(end - start)



