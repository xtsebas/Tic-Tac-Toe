import random

class MinimaxAlphaBetaAgent:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.nodes_explored = 0

    def evaluate(self, node):
        winner = node.check_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        return 0

    def minimax(self, node, depth, alpha, beta, maximizing_player):
        self.nodes_explored += 1
        if depth == 0 or node.is_terminal():
            return self.evaluate(node)

        if maximizing_player:
            max_eval = float('-inf')
            for child in node.get_children():
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.get_children():
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self, node):
        best_value = float('-inf')
        best_moves = []
        for child in node.get_children():
            eval = self.minimax(child, self.max_depth - 1, float('-inf'), float('inf'), False)
            if eval > best_value:
                best_value = eval
                best_moves = [child]
            elif eval == best_value:
                best_moves.append(child)
        return random.choice(best_moves) if best_moves else None
