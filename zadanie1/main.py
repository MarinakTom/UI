import pygame

from environment.environment import Environment
from environment.renderer import Renderer
from environment.move import Move

pygame.init()

WIDTH = 1100
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chess Bot")

clock = pygame.time.Clock()

environment = Environment()
renderer = Renderer(screen, environment)

running = True

selectedSquare = None

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            mouseX, mouseY = pygame.mouse.get_pos()

            if mouseX >= 800:
                renderer.scrollMoveHistory(event.y)

        if (event.type == pygame.MOUSEBUTTONDOWN and not environment.isCheckmate()):
            if event.button == 1:

                mouseX, mouseY = event.pos

            if mouseX < 800 and mouseY < 800:

                col = mouseX // renderer.squareSize
                row = mouseY // renderer.squareSize

                piece = environment.board.board[row][col]

                if selectedSquare is None:

                    if piece is not None:

                        playerCode = (
                            "w"
                            if environment.currentPlayer == "white"
                            else "b"
                        )

                        if piece[0] == playerCode:
                            selectedSquare = (row, col)

                else:
                    playerCode = (
                        "w"
                        if environment.currentPlayer == "white"
                        else "b"
                    )

                    if piece is not None and piece[0] == playerCode:
                        selectedSquare = (row, col)

                    else:
                        startRow, startCol = selectedSquare

                        requestedMove = Move(
                            startRow, startCol,
                            row, col
                        )

                        legalMoves = environment.getLegalMoves()

                        if requestedMove in legalMoves:
                            environment.makeMove(requestedMove)

                        selectedSquare = None

    renderer.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()