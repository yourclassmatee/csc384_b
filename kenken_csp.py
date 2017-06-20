#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools

def kenken_csp_model(kenken_grid):
    '''Returns a CSP object representing a Kenken CSP problem along 
       with an array of variables for the problem. That is return

       kenken_csp, variable_array

       where kenken_csp is a csp representing the kenken model
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the board (indexed from (0,0) to (N-1,N-1))

       
       The input grid is specified as a list of lists. The first list
	   has a single element which is the size N; it represents the
	   dimension of the square board.
	   
	   Every other list represents a constraint a cage imposes by 
	   having the indexes of the cells in the cage (each cell being an 
	   integer out of 11,...,NN), followed by the target number and the
	   operator (the operator is also encoded as an integer with 0 being
	   '+', 1 being '-', 2 being '/' and 3 being '*'). If a list has two
	   elements, the first element represents a cell, and the second 
	   element is the value imposed to that cell. With this representation,
	   the input will look something like this:
	   
	   [[N],[cell_ij,...,cell_i'j',target_num,operator],...]
	   
       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {1-N}.
       
       This model will also contain BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.) and an n-ary constraint for each cage in the grid.
    '''

    ##IMPLEMENT
    
    #generate dom
    size = kenken_grid[0][0]
    dom = []
    i=0
    for i in range(1, size+1):
        dom.append(i)

    # generate vars
    vars = []
    for i in range(1, size+1):
        each_row = []
        for j in range(1, size+1):
            each_row.append(Variable('V{}{}'.format(i,j), dom))
        vars.append(each_row)

    cons = []
    #add kenken constraints
    for i in range(1, len(kenken_grid)):
        each_cage = kenken_grid[i]

        #generate list of lists for looping
        scope = []
        varDoms = []
        for j in range (0, len(each_cage)-2):
            each_dom = []
            for k in range(1, size+1):
                each_dom.append(k)
            varDoms.append(each_dom)
            index1 = int(str(each_cage[j])[0])
            index2 = int(str(each_cage[j])[1])
            scope.append(vars[index1-1][index2-1])

        sat_tuples = []
        #iterate the cartesian product
        for t in itertools.product(*varDoms):
            if len(each_cage) > 2:
                if check_kenken(t, each_cage[len(each_cage)-2], each_cage[len(each_cage)-1]):
                    sat_tuples.append(t)
            else:
                if check_kenken_2(t, each_cage[len(each_cage)-1]):
                    sat_tuples.append(t)

        #make con
        con = Constraint("C:cage{})".format(i), scope)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)


    #make all binary constraints
    for i in range(1, size+1):
        print("bla")





def check_kenken(t, result, operator):
    if operator == 0: #plus
        sum = 0
        for num in t:
            sum += num
        if sum == result:
            return True
        return False
    elif operator == 1: #minus
        if t[0] - t[1] == result or t[1] - t[0] == result:
            return True
        return False
    elif operator == 2: #divide
        if t[0] / t[1] == result or t[1] / t[0] == result:
            return True
        return False

    elif operator == 3: #multiply
        product = 1
        for num in t:
            product = product * num
        if product == result:
            return True
        return False


def check_kenken_2(t, result):
    if t[0] != result:
        return False
    return True
