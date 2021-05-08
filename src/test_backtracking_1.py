'''
Author: Thomas Fang: tfang@umass.edu
'''

import SketchRefineWithBT as sr
import pandas as pd
import time

df = pd.read_csv('../data/tpch.csv')
partition = pd.read_csv('../data/partition_1000000.csv', index_col=0)
representatives = pd.read_csv('../data/representatives_min_1000000.csv', index_col=0)


print("sketchrefine method for query 1:")
Q1 = sr.SketchRefine(partition, representatives, 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price',
              None, 15469853.7043), c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
              c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
              c6=('avg_disc', None, 0.110243522496))
print("solvable: {}".format(Q1.solvable))
print("solution:")
print(Q1.solution)
print("objective: {0!s}".format(Q1.objective))
print("runtime: {0!s}".format(Q1.run_time))

# # Test query 2
print("\n")
print("sketchrefine method for query 2:")
Q2 = sr.SketchRefine(partition, representatives, 'min', A_0='ps_min_supplycost', count_constraint=(1, None),
                     c1=('p_size', None, 8))
print("solvable: {}".format(Q2.solvable))
print("solution:")
print(Q2.solution)
print("objective: {0!s}".format(Q2.objective))
print("runtime: {0!s}".format(Q2.run_time))

representatives = pd.read_csv('../data/representatives_max_1000000.csv', index_col=0)

# # Test query 3
print("\n")
print("sketchrefine method for query 3:")
Q3 = sr.SketchRefine(partition, representatives, 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
print("solvable: {}".format(Q3.solvable))
print("solution:")
print(Q3.solution)
print("objective: {0!s}".format(Q3.objective))
print("runtime: {0!s}".format(Q3.run_time))
#
# # Test query 4
print("\n")
print("sketchrefine method for query 4:")
Q4 = sr.SketchRefine(partition, representatives, 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
              c2=('o_shippriority', 3, None))
print("solvable: {}".format(Q4.solvable))
print("solution:")
print(Q4.solution)
print("objective: {0!s}".format(Q4.objective))
print("runtime: {0!s}".format(Q4.run_time))