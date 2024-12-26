class GameState():
    pieceScores = {'p': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False

    def evaluate(self):
        """Evaluates the game state based on material and mobility."""
        materialScore = 0
        mobilityScore = 0
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
        mobilityScore = len(moves) if self.whiteToMove else -len(moves)
        return materialScore + 0.1 * mobilityScore

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
                    print(f"Pruning: Beta ({beta}) <= Alpha ({alpha}) at depth {depth}")
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
                    print(f"Pruning: Beta ({beta}) <= Alpha ({alpha}) at depth {depth}")
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
            print(f"Evaluating move: {move.getChessNotation()}")
            self.makeMove(move)
            self.printBoard()
            evaluation = self.minimax(depth - 1, alpha, beta, False)
            self.undoMove()
            print(f"Move: {move.getChessNotation()}, Evaluation = {evaluation}")
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = move

        if bestMove is not None:
            print(f"Best Move: {bestMove.getChessNotation()}, Evaluation = {maxEval}")
        else:
            print("No move selected as best.")
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
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        """Generates all possible moves without checks."""
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece != "--" and ((piece[0] == 'w' and self.whiteToMove) or (piece[0] == 'b' and not self.whiteToMove)):
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
    bestMove = gs.getBestMove(depth=3)
    if bestMove:
        print(f"Best Move: {bestMove.getChessNotation()}")
    else:
        print("No moves available. Game over or invalid state.")
