from environment.move import Move

class Rules:
    def __init__(self, board):
        self.board = board

    def isInsideBoard(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def isOwnPiece(self, row, col, player):
        piece = self.board.board[row][col]

        if piece is None:
            return False

        playerCode = "w" if player == "white" else "b"

        return piece[0] == playerCode

    def getPossibleMoves(self, player):
        moves = []

        board = self.board.board
        playerCode = "w" if player == "white" else "b"

        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece is None:
                    continue

                if piece[0] != playerCode:
                    continue

                pieceType = piece[1]

                if pieceType == "P":
                    moves.extend(self.getPawnMoves(row, col, player))

                elif pieceType == "R":
                    moves.extend(self.getRookMoves(row, col, player))

                elif pieceType == "N":
                    moves.extend(self.getKnightMoves(row, col, player))

                elif pieceType == "B":
                    moves.extend(self.getBishopMoves(row, col, player))

                elif pieceType == "Q":
                    moves.extend(self.getQueenMoves(row, col, player))
                
                elif pieceType == "K":
                    moves.extend(self.getKingMoves(row, col, player))

        return moves

    def getSlideMoves(self, row, col, player, directions):
            moves = []
    
            for rowDirection, colDirection in directions:
    
                newRow = row + rowDirection
                newCol = col + colDirection
    
                while self.isInsideBoard(newRow, newCol):
    
                    target = self.board.board[newRow][newCol]
    
                    if target is None:
                        moves.append(
                            Move(row, col, newRow, newCol)
                        )
    
                    else:
                        if not self.isOwnPiece(newRow, newCol, player):
                            moves.append(
                                Move(row, col, newRow, newCol)
                            )
    
                        break
    
                    newRow += rowDirection
                    newCol += colDirection
    
            return moves

    def findKing(self, player):
        king = "wK" if player == "white" else "bK"

        for row in range(8):
            for col in range(8):
                if self.board.board[row][col] == king:
                    return row, col

        return None

    def isSquareAttacked(self, row, col, attacker):
        board = self.board.board
        attackerCode = "w" if attacker == "white" else "b"

        if attacker == "white":
            pawnRow = row + 1
        else:
            pawnRow = row - 1

        for pawn_col in (col - 1, col + 1):
            if self.isInsideBoard(pawnRow, pawn_col):
                if board[pawnRow][pawn_col] == attackerCode + "P":
                    return True

        knightOffsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for rowOffset, colOffset in knightOffsets:
            r = row + rowOffset
            c = col + colOffset

            if self.isInsideBoard(r, c):
                if board[r][c] == attackerCode + "N":
                    return True

        straightDirections = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for rowDirection, colDirection in straightDirections:
            r = row + rowDirection
            c = col + colDirection

            while self.isInsideBoard(r, c):
                piece = board[r][c]

                if piece is not None:
                    if piece[0] == attackerCode:
                        if piece[1] in ("R", "Q"):
                            return True

                    break

                r += rowDirection
                c += colDirection

        diagonalDirections = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        for rowDirection, colDirection in diagonalDirections:
            r = row + rowDirection
            c = col + colDirection

            while self.isInsideBoard(r, c):
                piece = board[r][c]

                if piece is not None:
                    if piece[0] == attackerCode:
                        if piece[1] in ("B", "Q"):
                            return True

                    break

                r += rowDirection
                c += colDirection

        kingDirections = [
            (-1, -1), (-1, 0),
            (-1, 1), (0, -1),
            (0, 1), (1, -1),
            (1, 0), (1, 1)
        ]

        for rowOffset, colOffset in kingDirections:
            r = row + rowOffset
            c = col + colOffset

            if self.isInsideBoard(r, c):
                if board[r][c] == attackerCode + "K":
                    return True

        return False

    def isCheck(self, player):
        kingPosition = self.findKing(player)

        if kingPosition is None:
            return False

        kingRow, kingCol = kingPosition

        enemy = "black" if player == "white" else "white"

        return self.isSquareAttacked(
            kingRow,
            kingCol,
            enemy
        )

    def getPawnMoves(self, row, col, player):
        moves = []
        board = self.board.board

        if player == "white":
            direction = -1
            startRow = 6
            promotionRow = 0
            enemy = "b"
        else:
            direction = 1
            startRow = 1
            promotionRow = 7
            enemy = "w"

        nextRow = row + direction

        if self.isInsideBoard(nextRow, col):
            if board[nextRow][col] is None:

                if nextRow == promotionRow:
                    moves.append(
                        Move(
                            row, col,
                            nextRow, col,
                            promotionPiece="Q"
                        )
                    )
                else:
                    moves.append(
                        Move(
                            row, col,
                            nextRow, col
                        )
                    )

                    twoRows = row + 2 * direction

                    if (
                        row == startRow
                        and board[twoRows][col] is None
                    ):
                        moves.append(
                            Move(
                                row, col,
                                twoRows, col
                            )
                        )

        for colOffset in (-1, 1):
            captureRow = row + direction
            captureCol = col + colOffset

            if not self.isInsideBoard(captureRow, captureCol):
                continue

            target = board[captureRow][captureCol]

            if target is not None and target[0] == enemy:

                if captureRow == promotionRow:
                    moves.append(
                        Move(
                            row, col,
                            captureRow, captureCol,
                            promotionPiece="Q"
                        )
                    )

                else:
                    moves.append(
                        Move(
                            row, col,
                            captureRow, captureCol
                        )
                    )

        return moves

    def getRookMoves(self, row, col, player):
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

        return self.getSlideMoves(
            row, col,
            player, directions
        )

    def getKnightMoves(self, row, col, player):
        moves = []

        offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for rowOffset, colOffset in offsets:
            newRow = row + rowOffset
            newCol = col + colOffset

            if not self.isInsideBoard(newRow, newCol):
                continue

            if not self.isOwnPiece(newRow, newCol, player):
                moves.append(
                    Move(row, col, newRow, newCol)
                )

        return moves

    def getBishopMoves(self, row, col, player):
        directions = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        return self.getSlideMoves(
            row, col,
            player, directions
        )

    def getQueenMoves(self, row, col, player):
        directions = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1),

            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

        return self.getSlideMoves(
            row, col,
            player, directions
        )

    def getKingMoves(self, row, col, player):
        moves = []

        directions = [
            (-1, -1), (-1, 0),
            (-1, 1), (0, -1),
            (0, 1), (1, -1),
            (1, 0),  (1, 1)
        ]

        for rowOffset, colOffset in directions:
            newRow = row + rowOffset
            newCol = col + colOffset

            if not self.isInsideBoard(newRow, newCol):
                continue

            if not self.isOwnPiece(newRow, newCol, player):
                moves.append(
                    Move(row, col, newRow, newCol)
                )

        return moves