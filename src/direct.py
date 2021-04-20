from pulp import *


def direct_method(prob_name, is_max_query, dataframe, objective_var, dot_product_constraints, obj_constraint):
    n, m = dataframe.shape
    if is_max_query:
        prob = LpProblem(prob_name, LpMaximize)
    else:
        prob = LpProblem(prob_name, LpMinimize)
    lp_variables = [LpVariable("t_{}".format(i + 1), 0, 1, cat='Integer') for i in range(n)]
    prob += lpDot(lp_variables, dataframe[objective_var])
    for var, constraint, val in dot_product_constraints:
        if constraint == 'less_than':
            prob += (lpDot(lp_variables, dataframe[var]) < val)
        elif constraint == 'less_than_equal_to':
            prob += (lpDot(lp_variables, dataframe[var]) <= val)
        elif constraint == 'equal':
            prob += (lpDot(lp_variables, dataframe[var]) == val)
        elif constraint == 'greater_than':
            prob += (lpDot(lp_variables, dataframe[var]) > val)
        elif constraint == 'greater_than_equal_to':
            prob += (lpDot(lp_variables, dataframe[var]) >= val)
        else:
            print("****************not correct constraint***************")
            exit(1)
    for constraint, val in obj_constraint:
        if constraint == 'less_than':
            prob += (lpSum(lp_variables) < val)
        elif constraint == 'less_than_equal_to':
            prob += (lpSum(lp_variables) <= val)
        elif constraint == 'equal':
            prob += (lpSum(lp_variables) == val)
        elif constraint == 'greater_than':
            prob += (lpSum(lp_variables) > val)
        elif constraint == 'greater_than_equal_to':
            prob += (lpSum(lp_variables) >= val)
        else:
            print("****************not correct constraint***************")
            exit(1)

    status = prob.solve()
    print("status of solved problem {}".format(status))
    if status == 1:
        return [value(v) for i, v in enumerate(lp_variables) if v == 1]
    return []


def first_query(data):
    prob_name = "first_query"
    dot_product_constraints = [('sum_base_price', 'less_than_equal_to', 15469853.7043),
                               ('sum_disc_price', 'less_than_equal_to', 45279795.0584),
                               ('sum_charge', 'less_than_equal_to', 95250227.7918),
                               ('avg_qty', 'less_than_equal_to', 50.353948653),
                               ('avg_price', 'less_than_equal_to', 68677.5852459),
                               ('avg_disc', 'less_than_equal_to', 0.110243522496),
                               ('sum_qty', 'less_than_equal_to', 77782.028739)]
    obj_constraint = [('greater_than_equal_to', 1)]
    obj = 'count_order'
    solution = direct_method(prob_name=prob_name,
                             is_max_query=True,
                             dataframe=data,
                             objective_var=obj,
                             dot_product_constraints=dot_product_constraints,
                             obj_constraint=obj_constraint)
    return solution


def second_query(data):
    prob_name = "second_query"
    dot_product_constraints = [('p_size', 'less_than_equal_to', 8)]
    obj = 'ps_min_supplycost'
    obj_constraint = [('greater_than_equal_to', 1)]
    solution = direct_method(prob_name=prob_name,
                             is_max_query=True,
                             dataframe=data,
                             objective_var=obj,
                             dot_product_constraints=dot_product_constraints,
                             obj_constraint=obj_constraint)
    return solution