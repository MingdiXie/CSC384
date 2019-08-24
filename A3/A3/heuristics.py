#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    unsigned_list = csp.get_all_unasgn_vars()
    cur_var = unsigned_list[0]
    count = 1000
    for var in unsigned_list:
        cur_count = var.cur_domain_size()
        if cur_count == 0:
            return var
        elif cur_count < count:
            cur_var = var
            count = cur_count
    return cur_var



def val_lcv(csp,var):
    val_dict = dict()
    for val in var.cur_domain():
         val_dict[val] = 0
    constraint_list = csp.get_cons_with_var(var)
    for cons in constraint_list:
        for val in var.cur_domain():
            if (var, val) in cons.sup_tuples:
                val_dict[val] += len(cons.sup_tuples[(var, val)])

    newD = sorted(val_dict.items(), key=lambda kv: kv[1],reverse=True)
    newlist = []
    for v in newD:
        newlist.append(v[0])
    return newlist


