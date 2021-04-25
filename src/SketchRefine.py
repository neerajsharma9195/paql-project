import direct as d
import time
import numpy as np


def Sketch(partition, minmax, **kwargs):
    # Input: dataframe for partition, all other constraint inputs for DIRECT problem
    # Output: DIRECT output over representative tuples of partition
    return d.direct(partition, minmax, **kwargs)


def Refine(df, group_id, refining_set, minmax, **kwargs):
    # Input: dataset with group_id, dataframe for refining set, all other constraint inputs for
    #       DIRECT problem
    # Output: [solvable, df for refinning_set, objective] We need to keep
    #       track of which tuples have been refined in refining_set for SketchRefine.  Refine replaces the
    #       representative tuple specified by group id with an actual tuple
    solvable = False
    solution = None
    objective = None

    # Fix sketch set besides the specified group_id
    ref_set_x_gid = refining_set[refining_set['gid'] != group_id]
    # Create new constraints given these fixed tuples
    kwargs_copy = kwargs.copy()
    A_0 = kwargs_copy.pop('A_0', None)
    constraints = [k for k in kwargs_copy.values()]
    constraints_mod = [ref_set_x_gid[ct[0]].sum() for ct in constraints]
    new_constraints = []
    for i, val in enumerate(constraints):
        name, L_k, U_k = val
        if L_k is not None:
            L_k = L_k - constraints_mod[i]
        if U_k is not None:
            U_k = U_k - constraints_mod[i]
        new_constraints.append((name, L_k, U_k))
    objective_mod = [ref_set_x_gid['A_0'].sum()]
    new_kwargs = dict()
    new_kwargs['A_0'] = A_0
    # New count constraint is 1 since we're replacing a single tuple for specified gid
    new_kwargs['count_constraint'] = 1
    for i, val in enumerate(new_constraints):
        new_kwargs['c_{}'.format(i)] = val
    # Run direct to replace representative tuple specified by gid
    df_gid = df[df['gid'] == group_id]
    ilp_output = d.direct(df_gid, minmax, **new_kwargs)
    if ilp_output.solvable:
        solvable = True
        solution = refining_set
        solution.iloc[[group_id]] = ilp_output.solution.iloc[[0]]
        objective = ilp_output.objective + objective_mod
    return [solvable, solution, objective]


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
        refined_tuples = np.zeros(total_groups)
        current_refine_gid = 0
        for gid in range(total_groups):
            refine_output = Refine(df, current_refine_gid, refining_set, minmax, **kwargs)
            if not refine_output.solvable:
                print('ILP failed at refine stage for gid {}'.format(current_refine_gid))
                return [False, None, None, None]
            else:
                refining_set = refine_output.solution
                refined_tuples[gid] = 1
                current_refine_gid += 1
    end = time.time()
    solvable = True
    solution = refining_set
    objective = refine_output.objective
    runtime = end - start
    return [solvable, solution, objective, runtime]



