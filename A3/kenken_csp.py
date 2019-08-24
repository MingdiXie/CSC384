#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(kenken_grid):
    var_list = []
    nonnest_varlst = []
    n = kenken_grid[0][0]
    for i in range(n):
        var_list.append([])
        for j in range(n):
            name = str(i+1) + str(j+1)
            v = Variable(name, [k+1 for k in range(n)])
            var_list[-1].append(v)
            nonnest_varlst.append(v)
    csp = CSP(name, nonnest_varlst)

    #build sat_tuples
    sat_tuples = []
    helperlist = [[i+1 for i in range(n)],[i+1 for i in range(n)]]
    for t in itertools.product(*helperlist):
        if t[0] != t[1]:
            sat_tuples.append(t)


    counter = 0
    overlap_list = []
    helper_valst = [nonnest_varlst,nonnest_varlst]
    for t in itertools.product(*helper_valst):
        var1 = t[0]
        var2 = t[1]

        if (var1.name != var2.name) and (var1.name[0] == var2.name[0] or var1.name[1] == var2.name[1]):
            if [var1, var2] not in overlap_list:
                overlap_list.append([var1,var2])
                overlap_list.append([var2, var1])
                c = Constraint(counter, [var1,var2])
                c.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(c)
                counter += 1

    return csp, var_list


def nary_ad_grid(kenken_grid):
    var_list = []
    nonnest_varlst = []
    n = kenken_grid[0][0]
    for i in range(n):
        var_list.append([])
        for j in range(n):
            name = str(i + 1) + str(j + 1)
            v = Variable(name, [k + 1 for k in range(n)])
            var_list[-1].append(v)
            nonnest_varlst.append(v)
    csp = CSP(name, nonnest_varlst)

    # build sat_tuples
    inner = [i + 1 for i in range(n)]
    sat_tuples = list(itertools.permutations(inner,n))

    #add row constraint
    counter = 0
    for inner_list in var_list:
        c = Constraint(counter,inner_list)
        c.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(c)
        counter += 1

    # add coloumn constraint
    for i in range(n):
        vlist = []
        for j in range(n):
            vlist.append(var_list[j][i])
        c = Constraint(counter, vlist)
        c.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(c)
        counter += 1
    return csp, var_list

def kenken_csp_model(kenken_grid):
    counter = 100
    csp, var_list = binary_ne_grid(kenken_grid)
    n = kenken_grid[0][0]
    n_to_1list = [i+1 for i in range(n)]

    index = 1
    length = len(kenken_grid)

    while index < length:
        cage_list = kenken_grid[index]
        cage_len = len(cage_list)
        box_list = []
        for i in range(cage_len-2):
            row_index = (cage_list[i] // 10) - 1
            col_index = (cage_list[i] % 10) - 1
            box_list.append(var_list[row_index][col_index])


        if cage_len == 2:
            row_index = (cage_list[0] // 10) - 1
            col_index = (cage_list[0] % 10) - 1
            require_num = cage_list[1]
            c = Constraint(counter,[var_list[row_index][col_index]])
            c.add_satisfying_tuples((require_num))
            counter += 1
        else:
            operation = cage_list[-1]
            require_num = cage_list[-2]

            varDoms = []
            for i in range(cage_len-2):
                varDoms.append(n_to_1list)

            sat_tuples = []

            for t in itertools.product(*varDoms):
                if satisfied(t, operation, require_num):
                    sat_tuples.append(t)
                    counter += 1
            if len(sat_tuples) > 0:
                c = Constraint(counter, box_list)
                c.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(c)

        index += 1
    return csp, var_list




def satisfied(tuple, operation, req_num):
    '''
    satisfied((8, 4, 2), 0, 0)
    satisfied([8, 4, 2], 1, 0)
    satisfied([8, 4, 2], 2, 0)
    satisfied([8,4,2], 3, 0)
    '''
    if operation == 0:
        cal = sum(tuple)
        if cal == req_num:
            return True
    elif operation == 1:
        combination = list(itertools.permutations(tuple, len(tuple)))
        for a in combination:
            cal = sum(a)
            cal -= a[0]
            cal = -cal
            cal += a[0]
            if cal == req_num:
                return True
    elif operation == 2:
        combination = list(itertools.permutations(tuple, len(tuple)))
        for a in combination:
            cal = a[0]
            for i in range(1,len(a)):
                cal = cal / a[i]
            if cal == req_num:
                return True
    elif operation == 3:
        cal = tuple[0]
        for i in range(1, len(tuple)):
            cal = cal * tuple[i]
        if cal == req_num:
            return True
    return False
