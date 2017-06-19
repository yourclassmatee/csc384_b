#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newVar=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newVar (newly instaniated variable) is an optional argument.
      if newVar is not None:
          then newVar is the most
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

      PROPAGATOR called with newVar = None
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


      PROPAGATOR called with newVar = a variable V
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
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []



def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    if newVar == None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)
    pruned = []
    for con in cons:
        if con.get_n_unasgn() == 1:
            #check if dwo for the last var of the con
            vars = con.get_unasgn_vars()
            last_unasgn_var = vars[0]
            if_dwo, pruned_from_one_con = fc_check(con, last_unasgn_var)
            pruned.extend(pruned_from_one_con)
            if if_dwo:
                return False, pruned

    return True, pruned


def fc_check(con, var):
    pruned = []
    for d in var.cur_domain() :
        #get assigned vars in con
        vals = []
        scope = con.get_scope()
        for scope_var in scope:
            if scope_var.is_assigned():
                vals.append(scope_var.get_assigned_value())
            else:
                vals.append(d)
        if not con.check(vals):
            var.prune_value(d)
            pruned.append((var,d))

    if var.cur_domain() == []:
        # true means dwo occured
        return True, pruned
    else:
        return False, pruned




def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    #prune all values of != assigned val of newVar
    # if (newVar != None):
    #     if newVar.is_assigned() == True:
    #         assigned_val = newVar.get_assigned_value()
    #         for val in newVar.domain():
    #             if (val != assigned_val):
    #                 newVar.prune_value(val)

    # add all c to gac queue
    cons = []
    if (newVar != None):
        cons.extend(csp.get_cons_with_var(newVar))
    else:
        cons.extend(csp.get_all_cons())
    gac_queue = []
    gac_queue.extend(cons)

    pruned = []
    while gac_queue != []:
        con =gac_queue.pop()
        for var in con.get_scope():
            for d in var.cur_domain():
                if con.has_support(var, d):
                    continue
                else:
                    # prune
                    var.prune_value(d)
                    pruned.append((var,d))
                    #check if dwo
                    if var.cur_domain_size() == 0:
                        gac_queue.clear()
                        return False, pruned
                    else:
                        cons_related = csp.get_cons_with_var(var)
                        for adding_con in cons_related:
                            if adding_con not in gac_queue:
                                gac_queue.append(adding_con)

    return True, pruned
