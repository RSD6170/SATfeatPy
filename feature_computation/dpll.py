import random
import parse_cnf

verbose = True

# unit propagation

#define
num_vars_to_try = 10
num_probes = 5

# num_bin_clauses_with_var, int array containing the number of binary clauses with a certain variable (index),
# this should change as the propogation happens?


def unit_prop_probe(haltOnAssignment, doComp, v, num_bin_clauses_with_var):
    if verbose:
        print("unit prop probe")

    if not doComp:
        next_probe_depth = 1
        for j in range(num_probes):
            next_probe_depth = next_probe_depth * 4
            print("vars-reduced-depth-" + next_probe_depth)
            # they also write the actual feature here? or just reserve the memory for it
            print("feature")

        print("time to calculate unit probing...")

#     Note: depth is number of vars: manually set- not including unitprop
    current_depth = 0
    orig_num_active_vars = v
    reached_bottom = False

    for probe_num in range(num_probes):
        # sets depth to 1, 4, 16, 64, 256

        # alternatively next_probe_depth = 4 ** probe_num
        next_probe_depth = 1
        for j in range(probe_num):
            next_probe_depth = next_probe_depth * 4


        # the actual searching
        while current_depth < next_probe_depth and not reached_bottom:
            # define the int arrays, values not yet initialised though... Contents undefined
            # int varsInMostBinClauses[NUM_VARS_TO_TRY];
            # int numBin[NUM_VARS_TO_TRY];

            vars_in_most_bin_clauses = [0] * num_vars_to_try
            num_bin = [0] * num_vars_to_try


            array_size = 0
            for var in range(1, v+1):
                if var_states[var]

                if array_size < num_vars_to_try: array_size += 1

                j=0
                while j < array_size-1 and num_bin_clauses_with_var[var] < num_bin[j]:
                    j+=1





def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

def bcp(formula, unit):
    """
    If the unit is in the clause, it is fine, as it can be satisfied
    If a negative unit is in there, then remove it from the clause, as this will not be satisfied

    :param formula: formula (cnf still left to solve)
    :param unit:
    :return:
    """
    modified = []
    for clause in formula:
        # this clause is satisfied, so we don't need to search anywhere in it anymore
        if unit in clause: continue
        if -unit in clause:
            c = [x for x in clause if x != -unit]
            # clause is unsatisfiable
            if len(c) == 0: return -1
            modified.append(c)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []
    for literal, num in counter.items():
        if -literal not in counter:
            pures.append(literal)
    for pure in pures:
        formula = bcp(formula, pure)
    assignment += pures
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def variable_selection(formula):
    counter = get_counter(formula)
    return random.choice([x for x in counter.keys()])


def backtracking(formula, assignment):
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)

    assignment = assignment + pure_assignment + unit_assignment
    if formula == -1:
        return []
    if not formula:
        return assignment

    # randomly choose a variable to set
    variable = variable_selection(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])
    return solution


if __name__ == "__main__":
    # test out the algo here
    cnf_path = "../cnf_examples/basic.cnf"

    clauses, c, v = parse_cnf.parse_cnf(cnf_path)
    solution = backtracking(clauses, [])
    if solution:
        solution += [x for x in range(1, v + 1) if x not in solution and -x not in solution]
        solution.sort(key=lambda x: abs(x))
        print('SATISFIABLE')
        print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('UNSATISFIABLE')

    solution = backtracking(clauses, [])
