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
    player.AllIn(),
    player.FixedPart(0.9),  # SaveUpMyMoney
    player.PartOfOthers(0.2, 0.8),  # Pessimistic
    player.PartOfOthers(0.5, 1.0),  # TitForTat
    player.PartOfOthers(0.8, 1.2),  # Optimistic
    player.RepetitivePattern([0.8, 1., 1.2, 0.0]),  # Deceit
    player.LinearExtrapolation(0.5),  # Mathematician
    player.RandomPlayer(123),
    player.GrimTrigger(7.5)
]

setup1 = setup.Setup(name='FourEachGame')
setup1.set_players(differentPlayers)
setup1.set_game_creator(lambda p: game.LinearFunctionByPlayer(players=p))
setup1.set_player_per_game(4)
setup1.start()
setup1.chart_line_all_rounds()
setup1.chart_boxplot(is_log=False)
setup1.chart_boxplot(is_log=True)
setup1.chart_pie_outcomes()
setup1.chart_gaussian(is_log=False)
setup1.chart_gaussian(is_log=True)
