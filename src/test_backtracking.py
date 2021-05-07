import SketchRefineWithBT as srt
import pandas as pd
import pulp as pl
import time

og = pd.read_csv('data/tpch.csv').head(1000)
gid = pd.read_csv('data/partition_100000.csv', index_col=0)
representatives = pd.read_csv('data/representative_100000.csv', index_col=0)
df = pd.concat([gid, og], axis=1)
df['counts'] = 1
representatives = representatives.reset_index()
representatives['id'] = None
print("dataframe")
# print(gid.columns)
print(df.columns)
print("representatives")
print(representatives.columns)


numRows, numCols = representatives.shape


# df['gid'].to_csv('/Users/Thomas/Documents/Umass Amherst/CICS 645/Project/data/partition_100000.csv')
# print(og.shape)
# print(df.shape)
# print(representatives.shape)
# print(df.head)
# print(og.head)
# print(df.head)
# print(representatives.head)

# headQ1_sketch = sr.Sketch(representatives, 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price',
#               None, 15469853.7043), c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
#               c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
#               c6=('avg_disc', None, 0.110243522496))
# print(Q1_sketch.solvable)

# Test partition with pulp
def query1_pulp():
    start = time.time()
    lp_variables = []
    for i in range(numRows):
        lp_variables.append(pl.LpVariable("t_{}".format(i), 0, 1, cat='Integer'))
    prob = pl.LpProblem("firstQuery", pl.LpMaximize)
    prob += pl.lpDot(lp_variables, representatives['count_order'])
    constraint1 = (pl.lpDot(lp_variables, representatives['sum_base_price']) <= 15469853.7043)
    constraint2 = (pl.lpDot(lp_variables, representatives['sum_disc_price']) <= 45279795.0584)
    constraint3 = (pl.lpDot(lp_variables, representatives['sum_charge']) <= 95250227.7918)
    constraint4 = (pl.lpDot(lp_variables, representatives['avg_qty']) <= 50.353948653)
    constraint5 = (pl.lpDot(lp_variables, representatives['avg_price']) <= 68677.5852459)
    constraint6 = (pl.lpDot(lp_variables, representatives['avg_disc']) <= 0.110243522496)
    constraint7 = (pl.lpDot(lp_variables, representatives['sum_qty']) <= 77782.028739)
    constraint8 = (pl.lpSum(lp_variables) >= 1)
    prob += constraint1
    prob += constraint2
    prob += constraint3
    prob += constraint4
    prob += constraint5
    prob += constraint6
    prob += constraint7
    prob += constraint8
    status = prob.solve()
    ans = [pl.value(v) for v in lp_variables]
    for i, val in enumerate(ans):
        if val > 0:
            print(i, val)
    end = time.time()
    print('runtime = {0!s}'.format(end - start))


# query1_pulp()


# # Test query 1
# print("sketchrefine method for query 1:")
# Q1 = srt.SketchRefine(df, representatives, 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price',
#                                                                                                      None, 15469853.7043), c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
#                       c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
#                       c6=('avg_disc', None, 0.110243522496))
# print("solvable: {}".format(Q1.solvable))
# print("solution:")
# print(Q1.solution)
# print("objective: {0!s}".format(Q1.objective))
# print("runtime: {0!s}".format(Q1.run_time))


# # # Test query 2
# print("\n")
# print("sketchrefine method for query 2:")
# Q2 = srt.SketchRefine(df, representatives, 'min', A_0='ps_min_supplycost', count_constraint=(1, None),
#                       c1=('p_size', None, 8))
# print("solvable: {}".format(Q2.solvable))
# print("solution:")
# print(Q2.solution)
# print("objective: {0!s}".format(Q2.objective))
# print("runtime: {0!s}".format(Q2.run_time))
#
# Test query 3
# print("\n")
# print("sketchrefine method for query 3:")
# Q3 = srt.SketchRefine(df, representatives, 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
# print("solvable: {}".format(Q3.solvable))
# print("solution:")
# print(Q3.solution)
# print("objective: {0!s}".format(Q3.objective))
# print("runtime: {0!s}".format(Q3.run_time))

# Test query 4
print("\n")
print("sketchrefine method for query 4:")
Q4 = srt.SketchRefine(df, representatives, 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
                      c2=('o_shippriority', 3, None))
print("solvable: {}".format(Q4.solvable))
print("solution:")
print(Q4.solution)
print("objective: {0!s}".format(Q4.objective))
print("runtime: {0!s}".format(Q4.run_time))