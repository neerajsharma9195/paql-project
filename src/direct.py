'''
Author: Thomas Fang: tfang@umass.edu
        Neeraj Sharma: neerajsharma@umass.edu
'''

import time
from docplex.mp.model import Model
from collections import namedtuple


def direct(df, minmax, sketchRefine=False, **kwargs):
    '''

    :param df: dataframe df
    :param minmax: "min or "max" for objective
    :param sketchRefine:
    :param kwargs:  A_0='attribute name' for objective function
                    c#=('attribute_name', L_k, U_k) which give bounds for each attribute with a constraint (# can be 1,2,...,14 order doesn't matter)
                    count_range=(L_c, U,c) which is bounds for count constraint
    :return: [solvable as boolean, df of selected tuples, objective value, runtime]
    '''
    start = time.time()
    solvable = False
    solution = None
    objective = None
    A_0 = kwargs.pop('A_0', None)
    count_constraint = kwargs.pop('count_constraint', None)
    constraints = [k for k in kwargs.values()]
    mdl = Model()
    # Create binary variable for each tuple, named after its index in df
    variables = []
    for i in range(len(df)):
        if sketchRefine is False:
            variables.append(mdl.binary_var("t_{}".format(i)))
        else:
            ub = int(df.at[i, 'counts'])
            variables.append(mdl.integer_var(name="t_{}".format(i), lb=0, ub=ub))
    # Add constraints
    for ct in constraints:
        name, L_k, U_k = ct
        if L_k is not None:
            mdl.add_constraint(mdl.dot(variables, df[name]) >= L_k)
        if U_k is not None:
            mdl.add_constraint(mdl.dot(variables, df[name]) <= U_k)
    # Add count constraint
    if count_constraint is not None:
        L_c, U_c = count_constraint
        if L_c is not None:
            mdl.add_constraint(mdl.sum(variables) >= L_c)
        if U_c is not None:
            mdl.add_constraint(mdl.sum(variables) <= U_c)
    # Set objective.  If A_0 is none, we maximize or minimize count(*)
    if A_0 is not None:
        mdl.set_objective(minmax, mdl.dot(variables, df[A_0]))
    else:
        mdl.set_objective(minmax, mdl.sum(variables))
    # Solve model
    solve = mdl.solve()
    if solve is not None:
        indices = []
        solvable = True
        integer_vars = []
        for var in variables:
            if sketchRefine is False:
                if var.solution_value == 1:
                    indices.append(int(var.name[2:]))
            else:
                if var.solution_value > 0:
                    indices.append(int(var.name[2:]))
                    integer_vars.append(var.solution_value)
        solution = df.iloc[indices]
        objective = mdl.objective_value

        # adding the count of each representative
        if sketchRefine:
            solution['integer_var_solution'] = integer_vars

    else:
        print('status code: ')
        print(mdl.solve_details.status_code)
    end = time.time()
    run_time = end - start
    final = namedtuple("final", ["solvable", "solution", "objective", "run_time"])
    return final(solvable, solution, objective, run_time)
