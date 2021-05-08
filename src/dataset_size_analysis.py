import pandas as pd
import direct as d
import math
import SketchRefineWithBT as sr
import time

df = pd.read_csv('data/tpch.csv', sep=',')
df_10 = df.head(math.ceil(len(df) * .1))
df_40 = df.head(math.ceil(len(df) * .4))
df_70 = df.head(math.ceil(len(df) * .7))
df_sizes = [df_10, df_40, df_70, df]
size_list = [.1, .4, .7, 1]
partition = pd.read_csv('data/partition_1000000.csv', index_col=0)
part_10 = partition.head(math.ceil(len(partition) * .1))
part_40 = partition.head(math.ceil(len(partition) * .4))
part_70 = partition.head(math.ceil(len(partition) * .7))
part_sizes = [part_10, part_40, part_70, partition]
representatives_10_min_1000000 = pd.read_csv('data/representatives_min_10_1000000.csv', index_col=0)
representatives_40_min_1000000 = pd.read_csv('data/representatives_min_40_1000000.csv', index_col=0)
representatives_70_min_1000000 = pd.read_csv('data/representatives_min_70_1000000.csv', index_col=0)
representatives_min_1000000 = pd.read_csv('data/representatives_min_100_1000000.csv', index_col=0)
representatives_10_max_1000000 = pd.read_csv('data/representatives_max_10_1000000.csv', index_col=0)
representatives_40_max_1000000 = pd.read_csv('data/representatives_max_40_1000000.csv', index_col=0)
representatives_70_max_1000000 = pd.read_csv('data/representatives_max_70_1000000.csv', index_col=0)
representatives_max_1000000 = pd.read_csv('data/representatives_max_100_1000000.csv', index_col=0)
representatives_q4_10_1000000 = pd.read_csv('data/representatives_q4_10_1000000.csv', index_col=0)
representatives_q4_40_1000000 = pd.read_csv('data/representatives_q4_40_1000000.csv', index_col=0)
representatives_q4_70_1000000 = pd.read_csv('data/representatives_q4_70_1000000.csv', index_col=0)
representatives_q4_100_1000000 = pd.read_csv('data/representatives_q4_100_1000000.csv', index_col=0)
min_rep = [representatives_10_min_1000000, representatives_40_min_1000000, representatives_70_min_1000000,
           representatives_min_1000000]
max_rep = [representatives_10_max_1000000, representatives_40_max_1000000, representatives_70_max_1000000,
           representatives_max_1000000]
q4_rep = [representatives_q4_10_1000000, representatives_q4_40_1000000, representatives_q4_70_1000000,
          representatives_q4_100_1000000]
# import kmeans
kmeans100 = pd.read_csv('data/partition_kmeans100.csv', index_col=0)
kmeans_partition = df
kmeans_partition['gid'] = kmeans100['gid']
kmeans_part_10 = kmeans_partition.head(math.ceil(len(kmeans_partition) * .1))
kmeans_part_40 = kmeans_partition.head(math.ceil(len(kmeans_partition) * .4))
kmeans_part_70 = kmeans_partition.head(math.ceil(len(kmeans_partition) * .7))
kmeans_part_sizes = [kmeans_part_10, kmeans_part_40, kmeans_part_70, kmeans_partition]
kmeans_representatives_10_min = pd.read_csv('data/kmeans_representatives_min_10.csv', index_col=0)
kmeans_representatives_40_min = pd.read_csv('data/kmeans_representatives_min_40.csv', index_col=0)
kmeans_representatives_70_min = pd.read_csv('data/kmeans_representatives_min_70.csv', index_col=0)
kmeans_representatives_min = pd.read_csv('data/kmeans_representatives_min_100.csv', index_col=0)
kmeans_representatives_10_max = pd.read_csv('data/kmeans_representatives_max_10.csv', index_col=0)
kmeans_representatives_40_max = pd.read_csv('data/kmeans_representatives_max_40.csv', index_col=0)
kmeans_representatives_70_max = pd.read_csv('data/kmeans_representatives_max_70.csv', index_col=0)
kmeans_representatives_max = pd.read_csv('data/kmeans_representatives_max_100.csv', index_col=0)
kmeans_representatives_q4_10 = pd.read_csv('data/kmeans_representatives_q4_10.csv', index_col=0)
kmeans_representatives_q4_40 = pd.read_csv('data/kmeans_representatives_q4_40.csv', index_col=0)
kmeans_representatives_q4_70 = pd.read_csv('data/kmeans_representatives_q4_70.csv', index_col=0)
kmeans_representatives_q4_100 = pd.read_csv('data/kmeans_representatives_q4_100.csv', index_col=0)
kmeans_min_rep = [kmeans_representatives_10_min, kmeans_representatives_40_min, kmeans_representatives_70_min,
           kmeans_representatives_min]
kmeans_max_rep = [kmeans_representatives_10_max, kmeans_representatives_40_max, kmeans_representatives_70_max,
           kmeans_representatives_max]
kmeans_q4_rep = [kmeans_representatives_q4_10, kmeans_representatives_q4_40, kmeans_representatives_q4_70,
          kmeans_representatives_q4_100]


dataset_size = [math.ceil(len(df) * .1), math.ceil(len(df) * .4), math.ceil(len(df) * .7), math.ceil(len(df) * 1)]
loadtime = []

# Test load time for different dataset sizes
def load_time(rows):
    start = time.time()
    df = pd.read_csv('data/tpch.csv', nrows=rows)
    end = time.time()
    return end - start


for elt in dataset_size:
    loadtime.append(load_time(elt))
print(loadtime)

sr_size_runtime = []
sr_size_objective = []


for i, part in enumerate(part_sizes):
    Q1 = sr.SketchRefine(part, min_rep[i], 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price', None, 15469853.7043),
                  c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
                  c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
                  c6=('avg_disc', None, 0.110243522496))
    Q2 = sr.SketchRefine(part, min_rep[i], 'min', A_0='ps_min_supplycost', count_constraint=(1, None), c1=('p_size', None, 8))
    Q3 = sr.SketchRefine(part, max_rep[i], 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
    Q4 = sr.SketchRefine(part, q4_rep[i], 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
                  c2=('o_shippriority', 3, None))
    qlist = [Q1, Q2, Q3, Q4]
    runtime_list = []
    objective_list = []
    for q in qlist:
        runtime_list.append(q.run_time)
        objective_list.append(q.objective)
    sr_size_runtime.append(runtime_list)
    sr_size_objective.append(objective_list)
print(sr_size_runtime)
print(sr_size_objective)


direct_size_runtime = []
direct_size_objective = []

for i, df1 in enumerate(df_sizes):
    Q1 = d.direct(df1, 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price', None, 15469853.7043),
                  c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
                  c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
                  c6=('avg_disc', None, 0.110243522496))
    Q2 = d.direct(df1, 'min', A_0='ps_min_supplycost', count_constraint=(1, None), c1=('p_size', None, 8))
    Q3 = d.direct(df1, 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
    Q4 = d.direct(df1, 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
                  c2=('o_shippriority', 3, None))
    qlist = [Q1, Q2, Q3, Q4]
    runtime_list = []
    objective_list = []
    for q in qlist:
        runtime_list.append(q.run_time)
        objective_list.append(q.objective)
    direct_size_runtime.append(runtime_list)
    direct_size_objective.append(objective_list)
print(direct_size_runtime)
print(direct_size_objective)


# kmeans
kmeans_sr_size_runtime = []
kmeans_sr_size_objective = []

for i, kmeans_part in enumerate(kmeans_part_sizes):
    kmeans_Q1 = sr.SketchRefine(kmeans_part, kmeans_min_rep[i], 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price', None, 15469853.7043),
                  c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
                  c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
                  c6=('avg_disc', None, 0.110243522496))
    kmeans_Q2 = sr.SketchRefine(kmeans_part, kmeans_min_rep[i], 'min', A_0='ps_min_supplycost', count_constraint=(1, None), c1=('p_size', None, 8))
    kmeans_Q3 = sr.SketchRefine(kmeans_part, kmeans_max_rep[i], 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
    kmeans_Q4 = sr.SketchRefine(kmeans_part, kmeans_q4_rep[i], 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
                  c2=('o_shippriority', 3, None))
    kmeans_qlist = [kmeans_Q1, kmeans_Q2, kmeans_Q3, kmeans_Q4]
    kmeans_runtime_list = []
    kmeans_objective_list = []
    for q in kmeans_qlist:
        kmeans_runtime_list.append(q.run_time)
        kmeans_objective_list.append(q.objective)
    kmeans_sr_size_runtime.append(kmeans_runtime_list)
    kmeans_sr_size_objective.append(kmeans_objective_list)
print(kmeans_sr_size_runtime)
print(kmeans_sr_size_objective)


