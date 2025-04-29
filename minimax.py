import random

class MinimaxAgent:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.nodes_explored = 0

    def evaluate(self, node):
        # Heurística simple:
        winner = node.check_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0  # empate o no terminado

    def minimax(self, node, depth, maximizing_player):
        self.nodes_explored += 1

        if depth == 0 or node.is_terminal():
            return self.evaluate(node)

        if maximizing_player:
            max_eval = float('-inf')
            for child in node.get_children():
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.get_children():
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, node):
        best_value = float('-inf')
        best_moves = []
        for child in node.get_children():
            eval = self.minimax(child, self.max_depth - 1, False)
            if eval > best_value:
                best_value = eval
                best_moves = [child]
            elif eval == best_value:
                best_moves.append(child)
        return random.choice(best_moves) if best_moves else None

class RandomAgent:
    def select_move(self, node):
        children = node.get_children()
        return random.choice(children) if children else None