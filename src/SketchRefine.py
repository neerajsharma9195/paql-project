import direct as d
import time
from collections import namedtuple


def Sketch(partition, minmax, **kwargs):
    '''

    :param partition: partition representatives
    :param minmax:  "min or "max" for objective
    :param kwargs: all other constraint inputs for DIRECT problem
    :return: Sketch Package (DIRECT output over representative tuples of partition)
    '''
    return d.direct(partition, minmax, **kwargs)


def Refine(df, group_id, refining_set, minmax, **kwargs):
    '''

    :param df: dataset with group_id
    :param group_id: group id od group which needs to be refined
    :param refining_set: current refined set
    :param minmax: "min or "max" for objective
    :param kwargs: all other constraint inputs for DIRECT problem
    :return: [solvable, df for refining_set, objective]
    (track of which tuples have been refined in refining_set for SketchRefine. Refine replaces the representative tuple specified
     by group id with an actual tuple)
    '''
    solvable = False
    solution = None
    objective = None

    # Fix sketch set besides the specified group_id
    ref_set_x_gid = refining_set[refining_set['gid'] != group_id]
    # Create new constraints given these fixed tuples
    kwargs_copy = kwargs.copy()
    A_0 = kwargs_copy.pop('A_0', None)
    kwargs_copy.pop('count_constraint', None)
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
    objective_mod = ref_set_x_gid[A_0].sum()
    new_kwargs = dict()
    new_kwargs['A_0'] = A_0
    # New count constraint is 1 since we're replacing a single tuple for specified gid
    new_kwargs['count_constraint'] = (1, 1)
    for i, val in enumerate(new_constraints):
        new_kwargs['c_{}'.format(i)] = val
    # Run direct to replace representative tuple specified by gid
    df_gid = df[df['gid'] == group_id]
    ilp_output = d.direct(df_gid, minmax, **new_kwargs)
    if ilp_output.solvable:
        solvable = True
        solution = refining_set
        new_row = ilp_output.solution.reset_index(drop=True)
        new_row['id'] = None
        solution[solution['gid'] == group_id] = new_row.loc[0]
        objective = ilp_output.objective + objective_mod
    final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
    return final(solvable, solution, objective, None)


def SketchRefine(df, partition, minmax, **kwargs):
    '''

    :param df: dataset with group_id
    :param partition: dataframe for partition
    :param minmax:  "min or "max" for objective
    :param kwargs: all other constraint inputs for DIRECT problem
    :return:  [solvable, solution, objective, runtime] complete refined package
    '''
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
        for index, row in refining_set.iterrows():
            current_refine_gid = row['gid']
            refine_output = Refine(df, current_refine_gid, refining_set, minmax, **kwargs)
            if not refine_output.solvable:
                print('ILP failed at refine stage for gid {}'.format(current_refine_gid))
                return [False, None, None, None]
            else:
                refining_set = refine_output.solution
                current_refine_gid += 1
    end = time.time()
    solvable = True
    solution = refining_set
    objective = refine_output.objective
    runtime = end - start
    final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
    return final(solvable, solution, objective, runtime)
