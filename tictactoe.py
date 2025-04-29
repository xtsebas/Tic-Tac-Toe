class TicTacToeNode:
    def __init__(self, board=None, player='X'):
        if board is None:
            self.board = [[' ' for _ in range(3)] for _ in range(3)]
        else:
            self.board = [row.copy() for row in board]
        self.player = player
        self.children = []  # hijos en el árbol

    def is_terminal(self):
        return self.check_winner() is not None or all(cell != ' ' for row in self.board for cell in row)

    def check_winner(self):
        lines = []

        for i in range(3):
            lines.append(self.board[i])  # filas
            lines.append([self.board[0][i], self.board[1][i], self.board[2][i]])  # columnas

        lines.append([self.board[0][0], self.board[1][1], self.board[2][2]])
        lines.append([self.board[0][2], self.board[1][1], self.board[2][0]])

        for line in lines:
            if line == ['X', 'X', 'X']:
                return 'X'
            elif line == ['O', 'O', 'O']:
                return 'O'
        return None

    def generate_children(self):
        if self.is_terminal():
            return  # no genera hijos si el juego terminó

        next_player = 'O' if self.player == 'X' else 'X'
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    new_board = [row.copy() for row in self.board]
                    new_board[i][j] = self.player
                    child = TicTacToeNode(new_board, next_player)
                    self.children.append(child)
                    child.generate_children()  # recursivo

    def get_children(self):
        if self.is_terminal():
            return []
        next_player = 'O' if self.player == 'X' else 'X'
        children = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    new_board = [row.copy() for row in self.board]
                    new_board[i][j] = self.player
                    children.append(TicTacToeNode(new_board, next_player))
        return children

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
        print('-' * 5)

    def print_tree(self, depth=0):
        print('  ' * depth + f"Player: {self.player}")
        self.print_board()
        for child in self.children:
            child.print_tree(depth + 1)

# Ejemplo de uso
if __name__ == "__main__":
    root = TicTacToeNode()
    root.generate_children()
    print("Árbol generado.")
    root.print_tree()  # cuidado: esto imprimirá todo el árbol (es muy grande)