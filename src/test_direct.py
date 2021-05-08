'''
Author: Thomas Fang: tfang@umass.edu
        Ananya Gupta: ananyagupta@umass.edu
'''


import time
from docplex.mp.model import Model
import pandas as pd
from collections import namedtuple
import direct as d
import pulp as pl

df = pd.read_csv('data/tpch.csv', sep=',')
print(df.shape)
# df1 = df.head(1000000)
df1 = df
numRows, numCols = df1.shape


# Query 1: to validate general direct method
def query1_cplex():
    start = time.time()
    mdl = Model(name='Query1')
    lp_variables = []
    for i in range(numRows):
        lp_variables.append(mdl.integer_var(name="t_{}".format(i), lb=0, ub=1))
    mdl.add_constraint(mdl.dot(lp_variables, df1['sum_base_price']) <= 15469853.7043)
    mdl.add_constraint(mdl.dot(lp_variables, df1['sum_disc_price']) <= 45279795.0584)
    mdl.add_constraint(mdl.dot(lp_variables, df1['sum_charge']) <= 95250227.7918)
    mdl.add_constraint(mdl.dot(lp_variables, df1['avg_qty']) <= 50.353948653)
    mdl.add_constraint(mdl.dot(lp_variables, df1['avg_price']) <= 68677.5852459)
    mdl.add_constraint(mdl.dot(lp_variables, df1['avg_disc']) <= 0.110243522496)
    mdl.add_constraint(mdl.dot(lp_variables, df1['sum_qty']) <= 77782.028739)
    mdl.add_constraint(mdl.sum(lp_variables) >= 1)
    mdl.set_objective('max', mdl.dot(lp_variables, df1['count_order']))
    mdl.solve()
    print(mdl.solution)
    end = time.time()
    print('runtime = {0!s}'.format(end - start))


# Query 1: pulp, validate general direct method
def query1_pulp():
    start = time.time()
    lp_variables = []
    for i in range(numRows):
        lp_variables.append(pl.LpVariable("t_{}".format(i), 0, 1, cat='Integer'))
    prob = pl.LpProblem("firstQuery", pl.LpMaximize)
    prob += pl.lpDot(lp_variables, df1['count_order'])
    constraint1 = (pl.lpDot(lp_variables, df1['sum_base_price']) <= 15469853.7043)
    constraint2 = (pl.lpDot(lp_variables, df1['sum_disc_price']) <= 45279795.0584)
    constraint3 = (pl.lpDot(lp_variables, df1['sum_charge']) <= 95250227.7918)
    constraint4 = (pl.lpDot(lp_variables, df1['avg_qty']) <= 50.353948653)
    constraint5 = (pl.lpDot(lp_variables, df1['avg_price']) <= 68677.5852459)
    constraint6 = (pl.lpDot(lp_variables, df1['avg_disc']) <= 0.110243522496)
    constraint7 = (pl.lpDot(lp_variables, df1['sum_qty']) <= 77782.028739)
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


# Query 2: to validate general direct method
def query2_pulp():
    start = time.time()
    prob2 = pl.LpProblem("secondQuery", pl.LpMinimize)
    pl.lp_variables = []
    for i in range(numRows):
        pl.lp_variables.append(pl.LpVariable("t_{}".format(i), 0, 1, cat='Integer'))
    
    objective_prob = pl.lpDot(pl.lp_variables, df1['ps_min_supplycost'])
    
    constraint1 = (pl.lpDot(pl.lp_variables, df1['p_size']) <= 8)
    constraint2 = (pl.lpSum(pl.lp_variables) >= 1)
    prob2 += objective_prob
    prob2 += constraint1
    prob2 += constraint2
    status1 = prob2.solve()
    ans = [pl.value(v) for v in pl.lp_variables]
    for i, val in enumerate(ans):
        if val > 0:
            print(i, val)
    end = time.time()
    print('runtime = {0!s}'.format(end - start))


# Query 3: pulp, to validate general direct method
def query3_pulp():
    start = time.time()
    prob3 = pl.LpProblem("thirdQuery", pl.LpMinimize)
    pl.lp_variables = []
    for i in range(numRows):
        pl.lp_variables.append(pl.LpVariable("t_{}".format(i), 0, 1, cat='Integer'))

    objective_prob = pl.lpSum(pl.lp_variables)

    constraint1 = (pl.lpDot(pl.lp_variables, df1['revenue']) >= 413930.849506)
    constraint2 = (pl.lpSum(pl.lp_variables) >= 1)
    prob3 += objective_prob
    prob3 += constraint1
    prob3 += constraint2
    status3 = prob3.solve()
    ans = [pl.value(v) for v in pl.lp_variables]
    for i, val in enumerate(ans):
        if val > 0:
            print(i, val)
    end = time.time()
    print('runtime = {0!s}'.format(end - start))


# Query 4: pulp, to validate general direct method
def query4_pulp():
    start = time.time()
    prob4 = pl.LpProblem("forthQuery", pl.LpMinimize)
    pl.lp_variables = []
    for i in range(numRows):
        pl.lp_variables.append(pl.LpVariable("t_{}".format(i), 0, 1, cat='Integer'))
    
    objective_prob = pl.lpSum(pl.lp_variables)
    
    constraint1 = (pl.lpDot(pl.lp_variables, df1['o_totalprice']) <= 453998.242103)
    constraint2 = (pl.lpDot(pl.lp_variables, df1['o_shippriority']) >= 3)
    constraint3 = (pl.lpSum(pl.lp_variables) >= 1)
    prob4 += objective_prob
    prob4 += constraint1
    prob4 += constraint2
    prob4 += constraint3
    status4 = prob4.solve()
    ans = [pl.value(v) for v in pl.lp_variables]
    for i, val in enumerate(ans):
        if val > 0:
            print(i, val)
    end = time.time()


def tuple_to_str(tuple):
    s = '('
    for i, val in enumerate(tuple):
        if i < len(tuple) - 1:
            s += str(val) + ', '
        else:
            s += str(val)
    s += ')'
    return s


def array_to_str(arr):
    s = '['
    for i, val in enumerate(arr):
        if type(val) is tuple:
            if i < len(arr) - 1:
                s += tuple_to_str(val) + ', '
            else:
                s += tuple_to_str(val)
        else:
            if i < len(arr) - 1:
                s += str(val) + ', '
            else:
                s += str(val)
    s += ']'
    return s


print("query size: {}".format(tuple_to_str(df.shape)))

# Query 1_pulp Test
# print("\n")
# print("specific implementation for query 1_pulp:")
# query1_pulp()

print("\n")
print("general direct method for query 1:")
Q1 = d.direct(df1, 'max', A_0='count_order', count_constraint=(1, None), c1=('sum_base_price', None, 15469853.7043),
              c2=('sum_disc_price', None, 45279795.0584), c3=('sum_charge', None, 95250227.7918),
              c4=('avg_qty', None, 50.353948653), c5=('avg_price', None, 68677.5852459),
              c6=('avg_disc', None, 0.110243522496))
print("solvable: {}".format(Q1.solvable))
print("solution:")
print(Q1.solution)
print("objective: {0!s}".format(Q1.objective))
print("runtime: {0!s}".format(Q1.run_time))

# Query 2_pulp Test
# print("\n")
# print("specific implementation for query 2_pulp:")
# query2_pulp()

print("\n")
print("general direct method for query 2:")
Q2 = d.direct(df1, 'min', A_0='ps_min_supplycost', count_constraint=(1, None), c1=('p_size', None, 8))
print("solvable: {}".format(Q2.solvable))
print("solution:")
print(Q2.solution)
print("objective: {0!s}".format(Q2.objective))
print("runtime: {0!s}".format(Q2.run_time))

# Query 3_pulp Test
# print("\n")
# print("specific implementation for query 3_pulp:")
# query3_pulp()

print("\n")
print("general direct method for query 3:")
Q3 = d.direct(df1, 'min', count_constraint=(1, None), c1=('revenue', 413930.849506, None))
print("solvable: {}".format(Q3.solvable))
print("solution:")
print(Q3.solution)
print("objective: {0!s}".format(Q3.objective))
print("runtime: {0!s}".format(Q3.run_time))
print("\n")

print("general direct method for query 4:")
Q4 = d.direct(df1, 'min', count_constraint=(1, None), c1=('o_totalprice', None, 453998.242103),
              c2=('o_shippriority', 3, None))
print("solvable: {}".format(Q4.solvable))
print("solution:")
print(Q4.solution)
print("objective: {0!s}".format(Q4.objective))
print("runtime: {0!s}".format(Q4.run_time))


# Query 4_cplex Test
# print("\n")
# print("specific implementation for query 4_pulp:")
# query4_pulp()



