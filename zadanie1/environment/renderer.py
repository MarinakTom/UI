import pygame
from pathlib import Path

class Renderer:
    def __init__(self, screen, environment, boardSize=800, perspective = "white"):
        self.screen = screen
        self.environment = environment

        self.boardSize = boardSize
        self.squareSize = boardSize // 8

        self.perspective = perspective

        self.lightColor = (240, 217, 181)
        self.darkColor = (181, 136, 99)

        self.panelColor = (35, 35, 35)
        self.textColor = (230, 230, 230)

        self.font = pygame.font.Font(None, 28)
        self.titleFont = pygame.font.Font(None, 36)

        self.historyScroll = 0
        self.lastMoveCount = 0

        self.historyTop = 70
        self.historyBottom = boardSize - 20
        self.historyLineHeight = 30

        self.pieceImages = {}

        self.loadPieceImages()

    def loadPieceImages(self):
        basePath = Path(__file__).parent.parent / "assets" / "pieces"

        pieceFiles = {
            "wP": "w_pawn.png",
            "wR": "w_rook.png",
            "wN": "w_knight.png",
            "wB": "w_bishop.png",
            "wQ": "w_queen.png",
            "wK": "w_king.png",

            "bP": "b_pawn.png",
            "bR": "b_rook.png",
            "bN": "b_knight.png",
            "bB": "b_bishop.png",
            "bQ": "b_queen.png",
            "bK": "b_king.png"
        }

        for pieceCode, filename in pieceFiles.items():
            image = pygame.image.load(
                basePath / filename
            ).convert_alpha()

            image = pygame.transform.smoothscale(
                image,
                (self.squareSize, self.squareSize)
            )

            self.pieceImages[pieceCode] = image

    def draw(self):
        self.drawBoard()
        self.drawPieces()
        self.drawMoveHistory()
        self.drawGameOver()

    def drawBoard(self):
        for row in range(8):
            for col in range(8):

                if (row + col) % 2 == 0:
                    color = self.lightColor
                else:
                    color = self.darkColor

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * self.squareSize,
                        row * self.squareSize,
                        self.squareSize,
                        self.squareSize
                    )
                )

    def drawPieces(self):
        board = self.environment.board.board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece is None:
                    continue

                image = self.pieceImages[piece]

                if self.perspective == "white":
                    displayRow = row
                    displayCol = col
                else:
                    displayRow = 7 - row
                    displayCol = 7 - col

                rect = image.get_rect()
                    
                rect.center = (
                    displayCol * self.squareSize + self.squareSize //2,
                    displayRow * self.squareSize + self.squareSize //2
                )

                self.screen.blit(image, rect)

    def drawMoveHistory(self):
        panelX = self.boardSize
        panelWidth = self.screen.get_width() - self.boardSize

        pygame.draw.rect(
            self.screen,
            self.panelColor,
            pygame.Rect(
                panelX,
                0,
                panelWidth,
                self.boardSize
            )
        )

        title = self.titleFont.render(
            "Move History",
            True,
            self.textColor
        )

        self.screen.blit(
            title,
            (panelX + 20, 20)
        )

        moves = self.environment.moveHistory

        visibleHeight = self.historyBottom - self.historyTop

        maxVisibleMoves = (
            visibleHeight // self.historyLineHeight
        )

        if len(moves) != self.lastMoveCount:
            self.historyScroll = max(
                0, len(moves) - maxVisibleMoves
            )

            self.lastMoveCount = len(moves)

        visibleMoves = moves[
            self.historyScroll:
            self.historyScroll + maxVisibleMoves
        ]

        y = self.historyTop

        for index, move in enumerate(visibleMoves):

            actualIndex = self.historyScroll + index

            text = self.font.render(
                f"{actualIndex + 1}. {move}", True, self.textColor
            )

            self.screen.blit(
                text, (panelX + 20, y)
            )

            y += self.historyLineHeight

    def drawGameOver(self):
        if not self.environment.isCheckmate():
            return

        boxWidth = 400
        boxHeight = 160

        boxX = (self.boardSize - boxWidth) // 2
        boxY = (self.boardSize - boxHeight) // 2

        boxRect = pygame.Rect(
            boxX, boxY,
            boxWidth, boxHeight
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            boxRect,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            boxRect,
            width=3,
            border_radius=15
        )

        if self.environment.currentPlayer == "white":
            winner = "Black"
        else:
            winner = "White"

        title = self.titleFont.render(
            "CHECKMATE", True, (0, 0, 0)
        )

        winnerText = self.font.render(
            f"{winner} wins!", True, (0, 0, 0)
        )

        titleRect = title.get_rect(
            center=(self.boardSize // 2, boxY + 55)
        )

        winnerRect = winnerText.get_rect(
            center=(self.boardSize // 2, boxY + 110)
        )

        self.screen.blit(title, titleRect)
        self.screen.blit(winnerText, winnerRect)

    def scrollMoveHistory(self, amount):
        moves = self.environment.moveHistory

        visibleHeight = (
            self.historyBottom - self.historyTop
        )

        maxVisibleMoves = (
            visibleHeight // self.historyLineHeight
        )

        maxScroll = max(
            0, len(moves) - maxVisibleMoves
        )

        self.historyScroll -= amount

        self.historyScroll = max(
            0, min(self.historyScroll, maxScroll)
        )