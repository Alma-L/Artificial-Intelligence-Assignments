from ortools.sat.python import cp_model

def solve_killer_sudoku():
    # Krijo modelin CSP
    model = cp_model.CpModel()

    # Defino fushat e Sudoku (9x9), secila me vlerë ndërmjet 1 dhe 9
    grid = [[model.NewIntVar(1, 9, f'cell_{i}_{j}') for j in range(9)] for i in range(9)]

    # Shto kufizime për rreshtat dhe kolonat (për të shmangur përsëritjen)
    for i in range(9):
        model.AddAllDifferent([grid[i][j] for j in range(9)])  # Kufizimi për rreshtat
        model.AddAllDifferent([grid[j][i] for j in range(9)])  # Kufizimi për kolonat

    # Defino grupet e "cages" dhe shumën e secilit grup (shembuj të thjeshtë)
    cages = [
        # Format: ((rreshti, kolona), shuma e kërkuar, fushat që përfshin)
        ((0, 0), 15, [(0, 0), (0, 1), (1, 0)]),  # Grup i parë
        ((0, 3), 15, [(0, 3), (0, 4), (1, 3)]),  # Grup i dytë
        # Shto të tjera grupe këtu, sipas puzzles
    ]

    # Shto kufizim për shumën e grupit
    for start_pos, target_sum, cells in cages:
        model.Add(sum(grid[r][c] for r, c in cells) == target_sum)

    # Krijo dhe zgjidh modelin
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Shfaq zgjidhjen nëse është gjetur
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(9):
            print([solver.Value(grid[i][j]) for j in range(9)])
    else:
        print("Nuk u gjet një zgjidhje.")

# Thirr funksionin për të zgjidhur puzzle-n
solve_killer_sudoku()
