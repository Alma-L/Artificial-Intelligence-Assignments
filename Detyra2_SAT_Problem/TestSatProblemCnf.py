from z3 import *


# Funksioni për të lexuar dhe analizuar CNF file
def read_cnf(file_path):
    clauses = []
    num_vars = 0

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('p'):  # Pjesa që përmban informacionin për variablat dhe klauzat
                _, _, num_vars, num_clauses = line.split()
                num_vars = int(num_vars)
            elif line and not line.startswith('c'):  # Shmangia e komenteve
                clause = [int(x) for x in line.split() if x != '0']
                clauses.append(clause)

    return num_vars, clauses


# Funksioni për të krijuar dhe zgjidhur SAT përmes z3
def solve_cnf(num_vars, clauses):
    solver = Solver()

    # Krijo variablat
    vars = [Bool(f'x{i + 1}') for i in range(num_vars)]

    # Shto kushtet (klauzat) në z3 solver
    for clause in clauses:
        literals = [vars[abs(lit) - 1] if lit > 0 else Not(vars[abs(lit) - 1]) for lit in clause]
        solver.add(Or(*literals))

    # Testo nëse ka një zgjidhje
    if solver.check() == sat:
        model = solver.model()
        return model
    else:
        return None


# Përdorimi i funksioneve
cnf_file = 'sat_problem.cnf'  # Vendosni rrugën e file-it tuaj CNF
num_vars, clauses = read_cnf(cnf_file)
solution = solve_cnf(num_vars, clauses)

if solution:
    print("Zgjidhja e mundshme është:")
    for i in range(num_vars):
        print(f"x{i + 1} = {solution[Bool(f'x{i + 1}')]}")  # Tregon vlerën e secilit variabël
else:
    print("Formula nuk ka zgjidhje.")
