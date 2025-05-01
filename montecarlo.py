import math
import random
from tictactoe import TicTacToeNode

class MCTSNode:
    def __init__(self, state: TicTacToeNode, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_states = state.get_children().copy()

    def is_fully_expanded(self):
        return not self.untried_states

    def best_ucb_child(self, c_param=math.sqrt(2)):
        weights = [
            (child.wins / child.visits) + c_param * math.sqrt(2 * math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[weights.index(max(weights))]

    def expand(self):
        next_state = self.untried_states.pop()
        child = MCTSNode(next_state, self)
        self.children.append(child)
        return child

    def rollout(self):
        current = self.state
        while not current.is_terminal():
            current = random.choice(current.get_children())
        return current.check_winner()

    def backpropagate(self, result):
        self.visits += 1
        if result == 'X':
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

class MCTSAgent:
    def __init__(self, simulations=1000, exploration_const=math.sqrt(2)):
        self.simulations = simulations
        self.C = exploration_const

    def choose(self, root_state):
        root = MCTSNode(root_state)
        for _ in range(self.simulations):
            node = root
            while node.is_fully_expanded() and node.children:
                node = node.best_ucb_child(self.C)
            if not node.is_fully_expanded():
                node = node.expand()
            result = node.rollout()
            node.backpropagate(result)
        best = max(root.children, key=lambda c: c.visits)
        return best.state
