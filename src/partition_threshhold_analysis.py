import pandas as pd
import direct as d
import math
import SketchRefineWithBT as sr

partition_10000000 = pd.read_csv('data/partition_10000000.csv')
partition_1000000 = pd.read_csv('data/partition_1000000.csv')
partition_100000 = pd.read_csv('data/partition_100000.csv')
partition_10000 = pd.read_csv('data/partition_10000.csv')
partition_1000 = pd.read_csv('data/partition_1000.csv')
rep_min_10000000 = pd.read_csv('data/representatives_min_100_10000000.csv')
rep_min_1000000 = pd.read_csv('data/representatives_min_100_1000000.csv')
rep_min_100000 = pd.read_csv('data/representatives_min_100_100000.csv')
rep_min_10000 = pd.read_csv('data/representatives_min_100_10000.csv')
rep_min_1000 = pd.read_csv('data/representatives_min_100_1000.csv')
rep_max_10000000 = pd.read_csv('data/representatives_max_100_10000000.csv')
rep_max_1000000 = pd.read_csv('data/representatives_max_100_1000000.csv')
rep_max_100000 = pd.read_csv('data/representatives_max_100_100000.csv')
rep_max_10000 = pd.read_csv('data/representatives_max_100_10000.csv')
rep_max_1000 = pd.read_csv('data/representatives_max_100_1000.csv')
rep_q4_10000000 = pd.read_csv('data/representatives_q4_100_10000000.csv')
rep_q4_1000000 = pd.read_csv('data/representatives_q4_100_1000000.csv')
rep_q4_100000 = pd.read_csv('data/representatives_q4_100_100000.csv')
rep_q4_10000 = pd.read_csv('data/representatives_q4_100_10000.csv')
rep_q4_1000 = pd.read_csv('data/representatives_q4_100_1000.csv')

rep_min = [rep_min_10000000, rep_min_1000000, rep_min_100000, rep_min_10000, rep_min_1000]
rep_max = [rep_max_10000000, rep_max_1000000, rep_max_100000, rep_max_10000, rep_max_1000]
rep_q4 = [rep_q4_10000000, rep_q4_1000000, rep_q4_100000, rep_q4_10000, rep_q4_1000]
part_list = [partition_10000000, partition_1000000, partition_100000, partition_10000, partition_1000]


threshhold_runtime = []
threshhold_objective = []

for i, part in enumerate(part_list):
    Q1 = sr.SketchRefine(part, rep_min[i], 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price', None, 15469853.7043),
                  c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
                  c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
                  c6=('avg_disc', None, 0.110243522496))
    Q2 = sr.SketchRefine(part, rep_min[i], 'min', A_0='ps_min_supplycost', count_constraint=(1, None), c1=('p_size', None, 8))
    Q3 = sr.SketchRefine(part, rep_max[i], 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
    Q4 = sr.SketchRefine(part, rep_q4[i], 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
                  c2=('o_shippriority', 3, None))
    qlist = [Q1, Q2, Q3, Q4]
    runtime_list = []
    objective_list = []
    for q in qlist:
        runtime_list.append(q.run_time)
        objective_list.append(q.objective)
    threshhold_runtime.append(runtime_list)
    threshhold_objective.append(objective_list)
print(threshhold_runtime)
print(threshhold_objective)