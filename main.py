import time
from tictactoe import TicTacToeNode
from minimax import MinimaxAgent, RandomAgent

def play_game(player1_type='human', starting_player='X', max_depth=3):
    game = TicTacToeNode(player=starting_player)
    minimax_agent = MinimaxAgent(max_depth)
    random_agent = RandomAgent()

    current_player = starting_player

    while not game.is_terminal():
        print("\nTablero actual:")
        game.print_board()

        if current_player == 'X':
            if player1_type == 'human':
                print("Tu turno (X)")
                moves = game.get_children()
                for idx, child in enumerate(moves):
                    print(f"Opción {idx}:")
                    child.print_board()
                option = int(input("Elige el número de opción: "))
                move = moves[option]
            elif player1_type == 'random':
                print("Turno aleatorio (X)")
                move = random_agent.select_move(game)
            else:
                raise ValueError("Tipo de jugador no reconocido")
        else:
            print("Turno del Minimax (O)")
            move = minimax_agent.best_move(game)

        if move is None:
            break

        game = move
        current_player = 'O' if current_player == 'X' else 'X'

    winner = game.check_winner()
    print("\nPartida terminada. Resultado final:")
    game.print_board()

    if winner == 'X':
        print("Ganó el Jugador 1 (X)")
    elif winner == 'O':
        print("Ganó el Jugador 2 (O, Minimax)")
    else:
        print("Empate.")

def simulate_random_vs_minimax(N=1000, starting_player='X', max_depth=3):
    wins = 0
    draws = 0
    losses = 0
    total_nodes = 0

    start_time = time.time()

    for _ in range(N):
        game = TicTacToeNode(player=starting_player)
        minimax_agent = MinimaxAgent(max_depth)
        random_agent = RandomAgent()

        current_player = starting_player

        while not game.is_terminal():
            if current_player == 'X':
                move = random_agent.select_move(game)
            else:
                move = minimax_agent.best_move(game)

            if move is None:
                break
            game = move
            current_player = 'O' if current_player == 'X' else 'X'

        winner = game.check_winner()
        total_nodes += minimax_agent.nodes_explored

        if winner == 'X':
            wins += 1
        elif winner == 'O':
            losses += 1
        else:
            draws += 1

    end_time = time.time()

    print(f"Resultados tras {N} juegos:")
    print(f"Victorias aleatorio (X): {wins}")
    print(f"Victorias Minimax (O): {losses}")
    print(f"Empates: {draws}")
    print(f"Tiempo total: {end_time - start_time:.2f} segundos")
    print(f"Nodos promedio explorados por juego: {total_nodes / N:.2f}")

if __name__ == "__main__":
    print("Opciones:")
    print("1. Jugar tú contra Minimax")
    print("2. Aleatorio contra Minimax")
    mode = int(input("Elige el modo (1 o 2): "))

    starting_player = input("¿Quién empieza? (X/O): ").strip().upper()
    depth = int(input("Profundidad de búsqueda k (ej: 3): "))

    if mode == 1:
        play_game(player1_type='human', starting_player=starting_player, max_depth=depth)
    elif mode == 2:
        N = int(input("Número de juegos a simular (ej: 1000): "))
        simulate_random_vs_minimax(N=N, starting_player=starting_player, max_depth=depth)
    else:
        print("Modo inválido.")
