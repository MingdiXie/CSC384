# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            if not check_Dead(c):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    # IMPLEMENT
    prune_list = []
    if newVar:
        for c in csp.get_cons_with_var(newVar):

            if c.get_n_unasgn() == 0:
                if not check_Dead(c):

                    return False, []

            elif c.get_n_unasgn() == 1:  # if there is only one unassign value
                vts = val_to_stay(c)
                for unassigned_var in c.get_unasgn_vars():  # get the unassigned variable
                    prune_list += prune_value(unassigned_var, vts)

                    if unassigned_var.cur_domain_size() == 0:

                        return False, prune_list
        return True, prune_list

    if not newVar:
        for c in csp.get_all_cons():
            unss_list = c.get_scope()
            for var in unss_list:
                available_list = var.cur_domain()
                for i in available_list:
                    if not c.has_support(var, i):
                        prune_list.append((var,i))
                        var.prune_value(i)
        return True, prune_list



def prune_value(var, vts):
    prune_list = []
    index = 0
    size = var.domain_size()
    domain = var.domain()
    TFlist = var.curdom

    while index < size:
        if TFlist[index] and domain[index] not in vts:
            prune_list.append((var, domain[index]))
            var.prune_value(domain[index])
        index += 1
    return prune_list


def val_to_stay(cons):
    list_var = cons.get_scope()
    list_val = []
    index = -1
    for var in list_var:
        index += 1
        if var.is_assigned():
            list_val.append(var.get_assigned_value())
        else:
            unassign_index = index
    ok_val = []
    for tuple, flag in cons.sat_tuples.items():
        temp_list = []
        if flag:
            for int in tuple:
                temp_list.append(int)
            temp_val = temp_list.pop(unassign_index)  # unassign var value
            if temp_list == list_val:
                ok_val.append(temp_val)
    return ok_val



def check_Dead(cons):
    vals = []
    vars = cons.get_scope()
    for var in vars:
        vals.append(var.get_assigned_value())
    return cons.check(vals)


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
# IMPLEMENT
    prune_list = []
    if newVar is None:
        cons_list = csp.get_all_cons()
        while cons_list != []:
            c = cons_list.pop(0)
            list_var = c.get_scope()
            for var in list_var:
                list_val = var.cur_domain()
                for val in list_val:
                    if not c.has_support(var, val):
                        prune_list.append((var,val))
                        var.prune_value(val)
                        if var.cur_domain_size() == 0:
                            return False, prune_list
                        for other_con in csp.get_cons_with_var(var):
                            if other_con not in cons_list and other_con != c:
                                cons_list.append(other_con)
        return True, prune_list
    else:
        cons_list = csp.get_cons_with_var(newVar)
        while cons_list != []:
            haha = []
            for i in cons_list:
                haha.append(i.name)
            c = cons_list.pop(0)
            list_var = c.get_scope()
            for var in list_var:
                list_val = var.cur_domain()
                for val in list_val:
                    if not c.has_support(var, val):
                        prune_list.append((var, val))
                        var.prune_value(val)
                        if var.cur_domain_size() == 0:
                            return False, prune_list
                        for other_con in csp.get_cons_with_var(var):
                            if other_con not in cons_list and other_con != c:
                                cons_list.append(other_con)
        return True, prune_list



