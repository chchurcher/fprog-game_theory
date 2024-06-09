import player
import game
import matplotlib.pyplot as plt
import numpy as np
import setup


def visualize_game(played_game):
    stats_by_player = played_game.get_states_by_player()
    x_vals = np.arange(played_game.num_rounds + 1)

    for i in range(played_game.get_num_players()):
        money_by_round = stats_by_player[i]
        player_str = str(played_game.players[i])
        plt.plot(x_vals, money_by_round, label=player_str)

    plt.title("Game simulation (n={:d}, p={:d})".format(played_game.num_rounds, played_game.get_num_players()))
    plt.xlabel("Round number")
    plt.ylabel("Money")
    plt.legend()
    plt.show()


differentPlayers = [
    player.FixedPart(0.5),
    player.FixedPart(0.4),
    player.FixedPart(1.0),
    player.RepetitivePattern([0.5, 0.9, 0.0]),
    player.RandomPlayer(10),
    player.LinearExtrapolation(0.1)
]

setup1 = setup.Setup(name='ManyRepetitivePlayers')
setup1.set_players(differentPlayers)
setup1.set_game_creator(lambda p: game.NoMoneyCreation(players=p))
setup1.set_player_per_game(4)
setup1.start()
# setup1.chart_line_all_rounds()
setup1.chart_boxplot()
