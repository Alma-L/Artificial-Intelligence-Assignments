class GameState():
    pieceScores = {
        'p': 1,  # Pawn
        'N': 3.3,  # Knight (slightly more for early-game activity)
        'B': 3.5,  # Bishop (often considered slightly better than knight due to long-range control)
        'R': 5,  # Rook
        'Q': 9,  # Queen
        'K': 1000  # King (assign an arbitrarily high value to ensure safety)
    }

    def __init__(self):
        self.board = [
            ["bR", "--", "bB", "bQ", "bK", "--", "bN", "bR"],
            ["bp", "bp", "bp", "--", "--", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "bN", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wp", "--", "--", "--", "--"],
            ["--", "--", "wN", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "--", "--", "wp", "wp", "wp"],
            ["wR", "--", "wB", "wQ", "wK", "--", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False

    def evaluate(self):
        """Evaluates the game state based on material and mobility."""
        materialScore = 0
        mobilityScore = 0
        kingSafetyScore = 0
        moves = self.getAllPossibleMoves()
        for row in self.board:
            for square in row:
                if square != "--":
                    pieceType = square[1]
                    pieceScore = self.pieceScores[pieceType]
                    if square[0] == 'w':
                        materialScore += pieceScore
                    else:
                        materialScore -= pieceScore

        # Additional bonus for mobility
        mobilityScore = len(moves) if self.whiteToMove else -len(moves)

        # Penalize if king is in unsafe position
        kingSafetyScore = self.evaluateKingSafety()

        return materialScore + 0.1 * mobilityScore + kingSafetyScore

    def evaluateKingSafety(self):
        """Evaluates king safety based on surrounding squares."""
        safetyScore = 0
        kingPosition = self.findKing('w' if self.whiteToMove else 'b')
        if kingPosition:
            row, col = kingPosition
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for d in directions:
                r, c = row + d[0], col + d[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = self.board[r][c]
                    if piece == "--":
                        safetyScore -= 0.05  # Penalize open squares near the king
                    elif piece[0] == ('w' if self.whiteToMove else 'b'):
                        safetyScore += 0.1  # Bonus for protected squares
        return safetyScore

    def findKing(self, color):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == f"{color}K":
                    return (r, c)
        return None

    def printBoard(self):
        for row in self.board:
            print(' '.join(row))
        print("\n")

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        """MiniMax algorithm with Alpha-Beta pruning."""
        if depth == 0 or self.checkmate or self.stalemate:
            return self.evaluate()

        moves = self.getValidMoves()

        if not moves:
            if self.checkmate:
                return float('-inf') if maximizingPlayer else float('inf')
            return 0  # Stalemate

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in moves:
                self.makeMove(move)
                evaluation = self.minimax(depth - 1, alpha, beta, False)
                self.undoMove()
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in moves:
                self.makeMove(move)
                evaluation = self.minimax(depth - 1, alpha, beta, True)
                self.undoMove()
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval

    def getBestMove(self, depth):
        """Finds the best move using MiniMax with Alpha-Beta pruning."""
        bestMove = None
        maxEval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        validMoves = self.getValidMoves()

        if not validMoves:
            print("No valid moves available!")
            return None

        for move in validMoves:
            self.makeMove(move)
            evaluation = self.minimax(depth - 1, alpha, beta, False)
            self.undoMove()
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = move

        return bestMove

    def makeMove(self, move):
        """Executes a move."""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        """Undoes the last move."""
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        """Generates valid moves."""
        moves = self.getAllPossibleMoves()
        moves.sort(key=lambda move: self.pieceScores.get(move.pieceCaptured[1], 0), reverse=True)
        return moves

    def getAllPossibleMoves(self):
        """Generates all possible moves without checks."""
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece != "--" and (
                        (piece[0] == 'w' and self.whiteToMove) or (piece[0] == 'b' and not self.whiteToMove)):
                    self.addPieceMoves(r, c, moves)
        return moves

    def addPieceMoves(self, r, c, moves):
        """Adds moves for a specific piece."""
        piece = self.board[r][c][1]
        if piece == 'p':
            self.getPawnMoves(r, c, moves)
        elif piece == 'R':
            self.getRookMoves(r, c, moves)
        elif piece == 'N':
            self.getKnightMoves(r, c, moves)
        elif piece == 'B':
            self.getBishopMoves(r, c, moves)
        elif piece == 'Q':
            self.getQueenMoves(r, c, moves)
        elif piece == 'K':
            self.getKingMoves(r, c, moves)

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r - 1 >= 0 and self.board[r - 1][c] == "--":  # Move forward
                moves.append(Move((r, c), (r - 1, c), self.board))
            if r == 6 and self.board[r - 1][c] == "--" and self.board[r - 2][c] == "--":  # Double move
                moves.append(Move((r, c), (r - 2, c), self.board))
        else:
            if r + 1 < 8 and self.board[r + 1][c] == "--":  # Move forward
                moves.append(Move((r, c), (r + 1, c), self.board))
            if r == 1 and self.board[r + 1][c] == "--" and self.board[r + 2][c] == "--":  # Double move
                moves.append(Move((r, c), (r + 2, c), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow, endCol = r + m[0], c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in kingMoves:
            endRow, endCol = r + m[0], c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

# Main driver
if __name__ == "__main__":
    gs = GameState()
    print("Initial Board:")
    gs.printBoard()

    validMoves = gs.getValidMoves()
    if validMoves:
        moveEvaluations = []
        for move in validMoves:
            gs.makeMove(move)
            evaluation = gs.minimax(depth=3, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=False)
            moveEvaluations.append((move, evaluation))
            gs.undoMove()
            print(f"Move {move.getChessNotation()}: Evaluation = {evaluation:.2f}")

        # Sort moves by evaluation to find the top 3 moves
        moveEvaluations.sort(key=lambda x: x[1], reverse=True)
        bestMoves = moveEvaluations[:3]

        print("\nTop 3 Moves and Evaluations:")
        for idx, (move, eval) in enumerate(bestMoves):
            print(f"Move {idx + 1}: {move.getChessNotation()} (Evaluation = {eval:.2f})")
            gs.makeMove(move)
            print("Board after move:")
            gs.printBoard()
            gs.undoMove()
    else:
        print("No valid moves available. Game over or invalid state.")


