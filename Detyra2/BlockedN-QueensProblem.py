import heapq
import random

def is_safe(board, row, col, N):
    """ Kontrollon nese vendosja e mbretereshes ne (row, col) eshte e sigurte """
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def a_star_n_queens(N, blocked_cells, heuristic):
    """ Zgjidh problemin Blocked N-Queens duke perdorur algoritmin A* """
    def h(state):
        return heuristic(state, N, blocked_cells)

    open_list = []  # Priority queue me heapq
    heapq.heappush(open_list, (0, [], 0))  # (priority, gjendja, g(n))

    while open_list:
        priority, state, g = heapq.heappop(open_list)

        # Nese kemi vendosur te gjitha mbretereshat, kthe rezultatin
        if len(state) == N:
            return state

        # Provo te vendosesh mbreteresha ne rreshtin aktual
        row = len(state)
        for col in range(N):
            if (row, col) not in blocked_cells and is_safe(state, row, col, N):
                new_state = state + [col]
                heapq.heappush(open_list, (g + 1 + h(new_state), new_state, g + 1))

    return None

def heuristic_1(state, N, blocked_cells):
    """ Heuristika 1: Numri i mbretereshave te mbetura """
    return N - len(state)

def heuristic_2(state, N, blocked_cells):
    """ Heuristika 2: Numri i qelizave te lira ne rreshtat e mbetura """
    free_cells = 0
    row = len(state)
    for r in range(row, N):
        free_cells += sum((r, c) not in blocked_cells for c in range(N))
    return max(0, N - len(state) - free_cells)

def heuristic_3(state, N, blocked_cells):
    """ Heuristika 3: Distanca minimale per mbretereshat e mbetura """
    return N - len(state)  # Heuristika naive per shembull

def heuristic_4(state, N, blocked_cells):
    """ Heuristikë me një komponent të rastësishëm për diversifikim """
    remaining_queens = N - len(state)
    random_factor = random.uniform(0, 1)  # Komponenti i zhurmës
    return remaining_queens + random_factor

def combined_heuristic(state, N, blocked_cells):
    """
    Heuristikë e kombinuar: përdor kombinimin e heuristikave ekzistuese.
    """
    queens_left = N - len(state)  # Numri i mbretëreshave të mbetura (nga Heuristika 1)
    free_cells = 0
    current_row = len(state)
    blocked_positions = 0

    for r in range(current_row, N):
        for c in range(N):
            # Qeliza të lira që nuk janë bllokuar
            if (r, c) not in blocked_cells and not any(
                state[i] == c or  # Kolona
                state[i] - i == c - r or  # Diagonalja majtas
                state[i] + i == c + r  # Diagonalja djathtas
                for i in range(len(state))
            ):
                free_cells += 1
            else:
                blocked_positions += 1

    # Penalizim i bazuar në raportin e qelizave të bllokuara
    penalty = blocked_positions / (N * N)

    # Kthimi i kombinimit
    return queens_left + (N - free_cells) + penalty



def visualize_board(N, blocked_cells, solution):
    """ Vizualizon tabelen si matrice """
    board = [["." for _ in range(N)] for _ in range(N)]

    # Vendos qelizat e bllokuara
    for row, col in blocked_cells:
        board[row][col] = "X"

    # Vendos mbretëreshat
    for row, col in enumerate(solution):
        board[row][col] = "Q"

    # Shtyp tabelën
    for row in board:
        print(" ".join(row))
    print()

def visualize_blocked_cells(N, blocked_cells):
    """Vizualizon vetëm qelizat e bllokuara në tabelë."""
    board = [["." for _ in range(N)] for _ in range(N)]
    for row, col in blocked_cells:
        board[row][col] = "X"
    for row in board:
        print(" ".join(row))
    print()


# Shembull: Zgjidh problemin per N = 8 me qeliza te bllokuara
N = 8
blocked_cells = {(0, 2), (3, 4), (5, 5)}

# Shembull: Tabela fillestare me qelizat e bllokuara
print("Tabela fillestare me qelizat e bllokuara:")
visualize_blocked_cells(N, blocked_cells)

# Zgjidh problemin me heuristiken e pare
solution = a_star_n_queens(N, blocked_cells, heuristic_1)
print("Zgjidhja me heuristiken 1:", solution)
visualize_board(N, blocked_cells, solution)

# Zgjidh problemin me heuristiken e dyte
solution = a_star_n_queens(N, blocked_cells, heuristic_2)
print("Zgjidhja me heuristiken 2:", solution)
visualize_board(N, blocked_cells, solution)

# Zgjidh problemin me heuristiken e trete
solution = a_star_n_queens(N, blocked_cells, heuristic_3)
print("Zgjidhja me heuristiken 3:", solution)
visualize_board(N, blocked_cells, solution)

# Zgjidh problemin me heuristikë që ka zhurmë
solution = a_star_n_queens(N, blocked_cells, heuristic_4)
print("Zgjidhja me heuristikë me zhurmë:", solution)
visualize_board(N, blocked_cells, solution)

# Zgjidh problemin me heuristikën e kombinuar
solution = a_star_n_queens(N, blocked_cells, combined_heuristic)
print("Zgjidhja me heuristikën e kombinuar:", solution)
visualize_board(N, blocked_cells, solution)



