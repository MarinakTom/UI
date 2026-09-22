import random

from environment.environment import Environment

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def chooseMove(self, environment):
        legalMoves = environment.getLegalMoves()

        if len(legalMoves) == 0:
            return None
        
        return random.choice(legalMoves)
    
class MinimaxAgent:
    def __init__(self):
        self.color = self

    def chooseMove(self, environment):
        pass