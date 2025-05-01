import time
import random
from tictactoe import TicTacToeNode
from minimax import MinimaxAgent, RandomAgent
from montecarlo import MCTSAgent

AGENT_TYPES_INTERACTIVE = {1: 'human', 2: 'random', 3: 'minimax', 4: 'mcts'}
AGENT_TYPES_SIM = {1: 'random', 2: 'minimax', 3: 'mcts'}


def play_game(player1_type='human', starting_player='X', max_depth=3, mcts_simulations=1000, mcts_exploration=1.4):
    game = TicTacToeNode(player=starting_player)
    minimax_agent = MinimaxAgent(max_depth)
    random_agent = RandomAgent()
    mcts_agent = MCTSAgent(simulations=mcts_simulations, exploration_const=mcts_exploration)

    current = starting_player
    while not game.is_terminal():
        print("\nTablero actual:")
        game.print_board()
        if current == 'X':
            print("Turno X:")
            print("1. Humano  2. Aleatorio  3. Minimax  4. MCTS")
            choice = int(input("Elige tipo de X (1-4): "))
            agent_type = AGENT_TYPES_INTERACTIVE.get(choice)
            if agent_type == 'human':
                moves = game.get_children()
                for idx, m in enumerate(moves):
                    print(f"{idx}: ")
                    m.print_board()
                sel = int(input("Elige jugada: "))
                next_state = moves[sel]
            elif agent_type == 'random':
                next_state = random_agent.select_move(game)
            elif agent_type == 'minimax':
                next_state = minimax_agent.best_move(game)
            elif agent_type == 'mcts':
                next_state = mcts_agent.choose(game)
            else:
                raise ValueError("Opción inválida para X")
        else:
            print("Turno O (Minimax):")
            next_state = minimax_agent.best_move(game)

        game = next_state
        current = 'O' if current == 'X' else 'X'

    winner = game.check_winner()
    print("\nPartida final:")
    game.print_board()
    if winner:
        print(f"Ganador: {winner}")
    else:
        print("Empate.")


def simulate_agents(N=1000, starting_player='X', max_depth=3, mcts_simulations=500, mcts_exploration=1.4):
    print("Agente X:")
    print("1. Aleatorio  2. Minimax  3. MCTS")
    choice_x = int(input("Tipo de X (1-3): "))
    agent_x_type = AGENT_TYPES_SIM.get(choice_x)
    print("Agente O:")
    print("1. Aleatorio  2. Minimax  3. MCTS")
    choice_o = int(input("Tipo de O (1-3): "))
    agent_o_type = AGENT_TYPES_SIM.get(choice_o)

    def make_agent(t):
        if t == 'random': return RandomAgent()
        if t == 'minimax': return MinimaxAgent(max_depth)
        return MCTSAgent(simulations=mcts_simulations, exploration_const=mcts_exploration)

    agent_x = make_agent(agent_x_type)
    agent_o = make_agent(agent_o_type)

    results = {'X': 0, 'O': 0, 'draw': 0}
    total_time = 0.0
    total_nodes = 0

    for _ in range(N):
        game = TicTacToeNode(player=starting_player)
        if isinstance(agent_x, MinimaxAgent): agent_x.nodes_explored = 0
        if isinstance(agent_o, MinimaxAgent): agent_o.nodes_explored = 0

        current = starting_player
        while not game.is_terminal():
            t0 = time.time()
            if current == 'X':
                if agent_x_type == 'random':
                    move = agent_x.select_move(game)
                elif agent_x_type == 'minimax':
                    move = agent_x.best_move(game)
                else:
                    move = agent_x.choose(game)
            else:
                if agent_o_type == 'random':
                    move = agent_o.select_move(game)
                elif agent_o_type == 'minimax':
                    move = agent_o.best_move(game)
                else:
                    move = agent_o.choose(game)

            total_time += time.time() - t0
            game = move
            current = 'O' if current == 'X' else 'X'

        winner = game.check_winner()
        results[winner or 'draw'] += 1
        if isinstance(agent_x, MinimaxAgent): total_nodes += agent_x.nodes_explored
        if isinstance(agent_o, MinimaxAgent): total_nodes += agent_o.nodes_explored

    print(f"X ganó: {results['X']}, O ganó: {results['O']}, Empates: {results['draw']}")
    print(f"Tiempo medio por jugada: {total_time/(N*5):.4f}s")
    if total_nodes:
        print(f"Nodos Minimax medio: {total_nodes/N:.2f}")

if __name__ == "__main__":
    print("1. Juego interactivo")
    print("2. Simulación automática")
    mode = int(input("Elige modo (1 o 2): "))

    if mode == 1:
        start = input("¿Quién empieza? (X/O): ").strip().upper()
        depth = int(input("Profundidad Minimax (k): "))
        sims = int(input("Simulaciones MCTS: "))
        expl = float(input("Constante exploración MCTS: "))
        play_game(player1_type='human', starting_player=start, max_depth=depth,
                  mcts_simulations=sims, mcts_exploration=expl)
    else:
        N = int(input("Número de partidas: "))
        start = input("¿Quién empieza? (X/O): ").strip().upper()
        depth = int(input("Profundidad Minimax (k): "))
        sims = int(input("Simulaciones MCTS: "))
        expl = float(input("Constante exploración MCTS: "))
        simulate_agents(N=N, starting_player=start, max_depth=depth,
                        mcts_simulations=sims, mcts_exploration=expl)
