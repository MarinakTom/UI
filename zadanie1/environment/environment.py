from environment.board import Board
from environment.rules import Rules

class Environment:
    def __init__(self):
        self.board = Board()
        self.rules = Rules(self.board)

        self.currentPlayer = "white"
        self.done = False
        self.moveHistory = []

    def reset(self):
        self.board.reset()
        self.currentPlayer = "white"
        self.done = False
        self.moveHistory = []

        return self.getState()

    def getState(self):
        return self.board.board

    def getLegalMoves(self):
        player = self.currentPlayer

        possibleMoves = self.rules.getPossibleMoves(player)

        legalMoves = []

        for move in possibleMoves:
            self.makeMove(
                move, record = False
            )

            if not self.rules.isCheck(player):
                legalMoves.append(move)

            self.undoMove(
                move, record = False
            )

        return legalMoves

    def makeMove(self, move, record=True):
        board = self.board.board

        move.movedPiece = board[move.startRow][move.startCol]
        move.capturedPiece = board[move.endRow][move.endCol]

        board[move.endRow][move.endCol] = move.movedPiece
        board[move.startRow][move.startCol] = None

        if move.promotionPiece is not None:
            color = move.movedPiece[0]

            board[move.endRow][move.endCol] = (
                color + move.promotionPiece
            )

        if record:
            self.moveHistory.append(
                self.moveToString(move)
            )

        self.switchPlayer()

    def moveToString (self, move):
        files = "abcdefgh"

        startSquare = (
            files[move.startCol]
            + str(8 - move.startRow)
        )

        endSquare = (
            files[move.endCol]
            + str(8 - move.endRow)
        )

        return f"{move.movedPiece}: {startSquare} -> {endSquare}"

    def undoMove(self, move, record = True):
        board = self.board.board

        board[move.startRow][move.startCol] = move.movedPiece
        board[move.endRow][move.endCol] = move.capturedPiece

        if record and self.moveHistory:
            self.moveHistory.pop()

        self.switchPlayer()

    def switchPlayer(self):
        if self.currentPlayer == "white":
            self.currentPlayer = "black"
        else:
            self.currentPlayer = "white"

    def isCheck(self, player):
        return self.rules.isCheck(player)

    def isCheckmate(self):
        if not self.isCheck(self.currentPlayer):
            return False

        return len(self.getLegalMoves()) == 0

    def isStalemate(self):
        if not self.isCheck(self.currentPlayer):
            return False
        
        return len(self.getLegalMoves()) == 0

    def isDraw(self):
        return False

    def isTerminal(self):
        return (
            self.isCheckmate()
            or self.isStalemate()
            or self.isDraw()
        )