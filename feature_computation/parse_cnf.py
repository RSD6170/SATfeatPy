

def parse_cnf(cnf_path):
    """
    Parse number of variables, number of clauses and the clauses from a standard .cnf file
    :param cnf_path:
    :return: clauses, number of clauses, and number of variables
    """

    with open(cnf_path) as f:

        clauses_list = []
        c = 0
        v = 0

        var_dict = {}
        max_value = 1
        for line in f:
            if line[0] == 'c':
                continue
            if line[0] == 'p':
                sizes = line.split(" ")
                v = int(sizes[2])
                c = int(sizes[3])

            else:
                # all following lines should represent a clause, so literals separated by spaces, with a 0 at the end,
                # denoting the end of the line.
                clause = [int(x) for x in line.split(" ")[:-1]]
                new_clause = []
                for cl in clause:
                    sign = -1 if cl < 0 else 1
                    if abs(cl) not in var_dict:
                        var_dict[abs(cl)] = max_value
                        max_value+=1
                    new_clause.append(var_dict[abs(cl)] * sign)
                clauses_list.append(new_clause)

        c = len(clauses_list)
        if c != 0:
            v = max([abs(l) for clause in clauses_list for l in clause])

    return clauses_list, c, v
