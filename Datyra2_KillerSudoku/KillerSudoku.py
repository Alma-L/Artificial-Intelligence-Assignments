from ortools.sat.python import cp_model

def solve_killer_sudoku():
    # Krijo modelin CSP
    model = cp_model.CpModel()

    # Defino fushat e Sudoku (9x9), secila me vlerë ndërmjet 1 dhe 9
    grid = [[model.NewIntVar(1, 9, f'cell_{i}_{j}') for j in range(9)] for i in range(9)]

    # Shto kufizime për rreshtat dhe kolonat
    for i in range(9):
        model.AddAllDifferent([grid[i][j] for j in range(9)])
        model.AddAllDifferent([grid[j][i] for j in range(9)])

    # Shto kufizimet për secilën nënrrjetë (3x3)
    for box_row in range(3):
        for box_col in range(3):
            model.AddAllDifferent([
                grid[3 * box_row + i][3 * box_col + j]
                for i in range(3)
                for j in range(3)
            ])

    # Defino grupet e "cages" dhe shumën e secilit grup
    cages = [
        (15, [(0, 0), (0, 1), (1, 0)]),
        (15, [(0, 3), (0, 4), (1, 3)]),
        (10, [(1, 1), (1, 2)]),
        (14, [(2, 0), (2, 1), (3, 0)]),
        # Shto më shumë cages sipas puzzles
    ]

    # Shto kufizime për shumën e secilit grup
    for target_sum, cells in cages:
        model.Add(sum(grid[r][c] for r, c in cells) == target_sum)

    # Zgjidh modelin
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Shfaq zgjidhjen nëse është gjetur
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Zgjidhja e Sudoku-t:")
        for i in range(9):
            row = ""
            for j in range(9):
                # Shto numrin dhe kufijtë vertikalë
                row += f" {solver.Value(grid[i][j])} "
                if (j + 1) % 3 == 0 and j < 8:
                    row += "|"
            print(row)
            # Shto kufijtë horizontalë pas çdo 3 rreshtash
            if (i + 1) % 3 == 0 and i < 8:
                print("-" * 28)
    else:
        print("Nuk u gjet një zgjidhje.")

# Thirr funksionin për të zgjidhur puzzle-n
solve_killer_sudoku()
