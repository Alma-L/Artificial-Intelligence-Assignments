# Parametrat kryesor
num_guests = 100  # Numri i mysafirëve
num_tables = 10  # Numri i tavolinave

# Kufizimet (shembull):
# Mysafirët që nuk mund të jenë në të njëjtë tavolinë
not_together = [(1, 5), (10, 13), (20, 25)]  # Çifte të mysafirëve
# Mysafirët që duhet të jenë së bashku
must_together = [(2, 3), (6, 7)]

# Variablat SAT (mapohet mysafiri dhe tavolina me një numër të veçantë ndryshoreje)
variables = {(guest, table): i * num_tables + table + 1 for i, guest in enumerate(range(1, num_guests + 1)) for table in
             range(num_tables)}


# Funksione ndihmëse

def at_least_one(guest):
    """Siguro që mysafiri është në të paktën një tavolinë."""
    return [variables[(guest, table)] for table in range(num_tables)]


def at_most_one(guest):
    """Siguro që mysafiri nuk është në më shumë se një tavolinë."""
    clauses = []
    for t1 in range(num_tables):
        for t2 in range(t1 + 1, num_tables):
            clauses.append([-variables[(guest, t1)], -variables[(guest, t2)]])
    return clauses


def not_in_same_table(pair):
    """Siguro që dy mysafirë nuk janë në të njëjtë tavolinë."""
    guest1, guest2 = pair
    clauses = []
    for table in range(num_tables):
        clauses.append([-variables[(guest1, table)], -variables[(guest2, table)]])
    return clauses


def must_be_together(pair):
    """Siguro që dy mysafirë janë gjithmonë së bashku."""
    guest1, guest2 = pair
    clauses = []
    for table in range(num_tables):
        clauses.append([variables[(guest1, table)], -variables[(guest2, table)]])
        clauses.append([-variables[(guest1, table)], variables[(guest2, table)]])
    return clauses


# Gjenerimi i klauzolave
clauses = []
for guest in range(1, num_guests + 1):
    clauses.append(at_least_one(guest))  # Çdo mysafir të jetë në të paktën një tavolinë
    clauses.extend(at_most_one(guest))  # Mysafiri të jetë në më shumë se një tavolinë

for pair in not_together:
    clauses.extend(not_in_same_table(pair))  # Mysafirët që nuk mund të jenë së bashku

for pair in must_together:
    clauses.extend(must_be_together(pair))  # Mysafirët që duhet të jenë së bashku

# Gjenerimi i file-it CNF
num_variables = num_guests * num_tables
num_clauses = len(clauses)

with open("sat_problem.cnf", "w") as f:
    # Shkruaj preambulën
    f.write(f"p cnf {num_variables} {len(clauses)}\n")

    # Shkruaj klauzolat
    for clause in clauses:
        # Çdo klauzolë kthehet në tekst me literale të ndarë me hapësirë dhe përfunduar me '0'
        f.write(" ".join(map(str, clause)) + " 0\n")

