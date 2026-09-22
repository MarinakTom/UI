import pygame
import random

from environment.environment import Environment
from environment.renderer import Renderer
from environment.move import Move
from chessbot.agent import RandomAgent

class Main:
    WIDTH = 1100
    HEIGHT = 800
    BOARD_SIZE = 800
    
    def __init__(self):
        self.perspective = random.choice(["white", "black"])

        self.humanColor = "w" if self.perspective == "white" else "b"
        self.agent1Color = "b" if self.humanColor == "w" else "w"

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Bot")

        self.environment = Environment()
        self.renderer = Renderer(self.screen, self.environment, perspective=self.perspective)
        self.agent1 = RandomAgent(self.agent1Color)
        #self.agent2 = MinimaxAgent(self.agentColor)

        self.clock = pygame.time.Clock()    

        self.running = True
        self.selectedSquare = None

    def getCurrentPlayerCode(self):
        return "w" if self.environment.currentPlayer == "white" else "b"

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.environment.isTerminal():
                    self.restartGame()
                    continue

                self.handleClick(event)

            if event.type == pygame.MOUSEWHEEL:
                self.handleScroll(event)

    def handleScroll(self, event):
        mouseX, mouseY = pygame.mouse.get_pos()
        
        if mouseX >= 800:
            self.renderer.scrollMoveHistory(event.y)

    def handleClick(self, event):
        if event.button != 1:
            return

        if self.environment.isTerminal():
            return

        if self.getCurrentPlayerCode() != self.humanColor:
            return

        mouseX, mouseY = event.pos

        if (mouseX >= self.BOARD_SIZE or mouseY >= self.BOARD_SIZE):
            return

        clickedCol = (mouseX // self.renderer.squareSize)
        clickedRow = (mouseY // self.renderer.squareSize)

        if self.renderer.perspective == "white":
            row = clickedRow
            col = clickedCol

        else:
            row = 7 - clickedRow
            col = 7 - clickedCol

        self.handleBoardClick(row, col)

    def handleBoardClick(self, row, col):
        piece = self.environment.board.board[row][col]
        playerCode = self.getCurrentPlayerCode()

        if self.selectedSquare is None:

            if (piece is not None and piece[0] == playerCode):
                self.selectedSquare = (row, col)
            return

        if (piece is not None and piece[0] == playerCode):
            self.selectedSquare = (row, col)

            return

        startRow, startCol = self.selectedSquare

        requestedMove = Move(startRow, startCol, row, col)

        self.tryMove(requestedMove)
        self.selectedSquare = None

    def tryMove(self, requestedMove):
        legalMoves = (
            self.environment.getLegalMoves()
        )

        for legalMove in legalMoves:
            if (legalMove.startRow == requestedMove.startRow
                and legalMove.startCol== requestedMove.startCol
                and legalMove.endRow == requestedMove.endRow
                and legalMove.endCol == requestedMove.endCol):

                self.environment.makeMove(legalMove)

                return True

        return False

    def handleAgentTurn(self):
        if self.environment.isTerminal():
            return

        if (self.getCurrentPlayerCode() != self.agent1Color):
            return

        agentMove = self.agent1.chooseMove(self.environment)

        if agentMove is not None:
            self.environment.makeMove(agentMove)

    def draw(self):
        self.renderer.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.eventHandler()

            if not self.running:
                break

            self.handleAgentTurn()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def restartGame(self):
        self.environment.reset()
        self.selectedSquare = None

if __name__ == "__main__":
    game = Main()
    game.run()