import direct as d
import time
import math
import numpy as np
import  pandas as pd
from collections import namedtuple
import random
import heapq


def list_to_str(arr):
    s = '['
    for i, val in enumerate(arr):
        if i < len(arr) - 1:
            s += str(val) + ', '
        else:
            s += str(val)
    s += ']'
    return s


def Sketch(partition, minmax, **kwargs):
    # Input: dataframe for partition, all other constraint inputs for DIRECT problem
    # Output: DIRECT output over representative tuples of partition
    return d.direct(partition, minmax, True, **kwargs)






# def Refining(df, group_id, refining_set, minmax, **kwargs):
#     # Input: dataset with group_id, dataframe for refining set, all other constraint inputs for
#     #       DIRECT problem
#     # Output: [solvable, df for refining_set, objective] We need to keep
#     #       track of which tuples have been refined in refining_set for SketchRefine.  Refine replaces the
#     #       representative tuple specified by group id with an actual tuple
#     solvable = False
#     solution = None
#     objective = None
#
#     # Fix sketch set besides the specified group_id
#     ref_set_x_gid = refining_set[refining_set['gid'] != group_id]
#     # Create new constraints given these fixed tuples
#     kwargs_copy = kwargs.copy()
#     A_0 = kwargs_copy.pop('A_0', None)
#     kwargs_copy.pop('count_constraint', None)
#     constraints = [k for k in kwargs_copy.values()]
#
#     # multiply the occurrences with each representative value then subtract from ub and lb
#     constraints_mod = [ref_set_x_gid[ct[0]].sum() for ct in constraints]
#     new_constraints = []
#     for i, val in enumerate(constraints):
#         name, L_k, U_k = val
#         if L_k is not None:
#             L_k = L_k - constraints_mod[i]
#         if U_k is not None:
#             U_k = U_k - constraints_mod[i]
#         new_constraints.append((name, L_k, U_k))
#     objective_mod = ref_set_x_gid[A_0].sum()
#     new_kwargs = dict()
#     new_kwargs['A_0'] = A_0
#     # New count constraint is 1 since we're replacing a single tuple for specified gid
#     new_kwargs['count_constraint'] = (1, 1)
#     for i, val in enumerate(new_constraints):
#         new_kwargs['c_{}'.format(i)] = val
#     # Run direct to replace representative tuple specified by gid
#     df_gid = df[df['gid'] == group_id]
#     ilp_output = d.direct(df_gid, minmax, **new_kwargs)
#     if ilp_output.solvable:
#         solvable = True
#         solution = refining_set
#         new_row = ilp_output.solution.reset_index(drop=True)
#         new_row['id'] = None
#         solution[solution['gid'] == group_id] = new_row.loc[0]
#         objective = ilp_output.objective + objective_mod
#     final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
#     return final(solvable, solution, objective, None)



def direct_on_one_group(df, representatives, Gi, refining_package, minmax, **kwargs):
    solvable = False
    solution = None
    objective = None
    # Fix refining_package besides the specified group_id
    ref_set_x_gid = refining_package[refining_package['gid'] != Gi]
    # Create new constraints given these fixed tuples
    kwargs_copy = kwargs.copy()
    A_0 = kwargs_copy.pop('A_0', None)
    kwargs_copy.pop('count_constraint', None)
    constraints = [k for k in kwargs_copy.values()]

    # multiply the occurrences with each representative value then subtract from ub and lb
    # change counts  to integer
    for ct in constraints:
        ref_set_x_gid[ct[0]] = ref_set_x_gid[ct[0]] * ref_set_x_gid['integer_var_solution']
    constraints_mod = [ref_set_x_gid[ct[0]].sum() if ref_set_x_gid[ct[0]].sum() is not None else 0 for ct in constraints]
    constraints_mod = [0 if math.isnan(x) else x for x in constraints_mod]

    if ref_set_x_gid is not None:
        new_constraints = []
        for i, val in enumerate(constraints):
            name, L_k, U_k = val
            if L_k is not None:
                L_k = L_k - constraints_mod[i]
            if U_k is not None:
                U_k = U_k - constraints_mod[i]
            new_constraints.append((name, L_k, U_k))
        objective_mod = ref_set_x_gid[A_0].sum()
        new_kwargs = dict()
        new_kwargs['A_0'] = A_0
        # New count constraint is 1 since we're replacing a single tuple for specified gid

        # change count constraint
        # df.loc[df['year'] == 2012, 'sale'].iloc[0]
        ub = representatives.loc[representatives['gid'] == Gi, 'integer_var_solution'].iloc[0]
        new_kwargs['count_constraint'] = (ub, ub)
        for i, val in enumerate(new_constraints):
            new_kwargs['c_{}'.format(i)] = val
    else:
        new_kwargs = kwargs
    # Run direct to replace representative tuple specified by gid
    df_gid = df[df['gid'] == Gi]
    ilp_output = d.direct(df_gid, minmax, **new_kwargs)
    if ilp_output.solvable:
        solvable = True
        solution = refining_package
        new_row = ilp_output.solution.reset_index(drop=True)
        new_row['id'] = None
        new_row['integer_var_solution'] = 1
        print(new_row.columns)
        print(solution.columns)
        # solution[solution['gid'] == Gi] = new_row.loc[0]
        objective = ilp_output.objective + objective_mod
    print(solvable, solution, objective)
    final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
    return final(solvable, solution, objective, None)


def Refine(df, representatives, P, S, refining_package, minmax, priority=0, **kwargs):
    # Input: df - dataset with group_id, dataframe for refining set or solution of sketch with the integer variable solutions for each representative of thr group,
    #        P [(Gi, ti)] - partitioning groups  and S = P initially partitioning groups yet to be refined
    #       all other constraint inputs for DIRECT problem

    F = []


    if len(S) < 1:
        return refining_package, F


    U_priorityQ = []
    random.shuffle(S)
    count = priority
    group_priorities = {}
    for g in S:
        heapq.heappush(U_priorityQ, (-count, g))
        group_priorities[g] = -count
        count += 1

    while len(U_priorityQ) > 0:

        # getting the group of most priority and pop it
        queue_top = heapq.heappop(U_priorityQ)

        Gi = queue_top[1]
        print('queue top = ',Gi)

        # Skip groups that have no representative in refining package
        Gi_solution = representatives.loc[representatives['gid'] == Gi, 'integer_var_solution'].iloc[0]
        if Gi_solution < 1:
            continue

        # run direct method on Gi, ti
        ilp_output = direct_on_one_group(df, representatives, Gi, refining_package, minmax, **kwargs)

        if ilp_output.solvable:
            solvable = True

            # Replace representative with tuples
            refining_package_without_gi = refining_package[refining_package['gid'] != Gi]
            refining_package = pd.concat([refining_package_without_gi, ilp_output.solution])

            S.remove(Gi)

            # recurse
            p, F_new = Refine(df, representatives, P, S, refining_package, minmax, kwargs)

            if len(F_new) < 1:
                return p, F
            else:
                F.extend(F_new)
                # greedily prioritize non refinable groups
                for f in F:
                    U_priorityQ.remove((group_priorities[f], f))
                    heapq.heappush(U_priorityQ, (-count, f))
                    group_priorities[f] = -count
                    count += 1

        else:
            if len(P) != len(S):
                F.append(Gi)
                return None, F
    return None, F








def SketchRefine(df, partition, minmax, **kwargs):
    # Input: dataset with group_id, dataframe for partition, all other constraint inputs for DIRECT problem
    # Output: [solvable, solution, objective, runtime]
    start = time.time()
    solvable = False
    solution = None
    objective = None
    # Sketch solution with representative tuples
    sktch = Sketch(partition, minmax, **kwargs)
    if not sktch.solvable:
        print('ILP failed at sketch phase')
        return [False, None, None, None]
    else:
        refining_set = sktch.solution
        # Refine phase
        total_groups = len(refining_set)
        # for index, row in refining_set.iterrows():
        # current_refine_gid = row['gid']
        gids = refining_set['gid']
        counts = refining_set['counts']
        P = list(gids)
        # refining_set = refining_set.set_index('gid')
        S = list(P)
        ps = refining_set
        representatives = refining_set
        refine_output, F = Refine(df, representatives , P, S, ps, minmax, **kwargs)
        print("Refine outputs")
        print(list_to_str(F))
        print(refine_output.head())
        # end = time.time()
        # print(end-start)
        # exit(0)
        # if len(F) < 1:
        #     return refine_output
        if len(F) > 0:
            print('ILP failed at refine stage for gids {}'.format(list_to_str(F)))
            return [False, None, None, None]
            # if not refine_output.solvable:
            #     print('ILP failed at refine stage for gid {}'.format(current_refine_gid))
            #     return [False, None, None, None]
            # else:
            #     refining_set = refine_output.solution
            #     current_refine_gid += 1
    end = time.time()
    solvable = True
    solution = refine_output
    A_0 = kwargs.pop('A_0', None)
    # calculate objective from the returned tuples-
    if A_0 is not None:
        objective = refine_output[A_0].sum()
    else:
        objective = refine_output.shape[0]


    runtime = end - start
    final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
    return final(solvable, solution, objective, runtime)



