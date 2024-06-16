import itertools
import math

import matplotlib.pyplot as plt
from statistics import median
import scipy.stats as stats
from matplotlib.patches import Patch
import seaborn as sns
import numpy as np


class Setup:
    """This class is used to simulate a huge number of games with a certain number of player"""

    def __init__(self, name='None', simulation_type='all'):
        """Constructs a new setup and gives a name to the setup
        :param name: used in plots and data
        :param simulation_type: not implemented
                determines how many games are played
                'all'   every possible game is played"""

        self.name = name
        self.simulation_type = simulation_type
        self.players = []
        self.new_game = None
        self.num_player_per_game = 0
        self.player_outcomes = []
        self.player_combinations = []
        self.num_games = 0
        self.game_index = 0
        self.games = []

    # region: creator methods
    def set_players(self, players):
        """Used to set the players for this setup
        :param players: list with all players in this setup"""
        self.players = players

    def set_game_creator(self, game_creator):
        """Sets a lambda expression to create a new game with players
        :param game_creator: lambda expression with argument players_list"""
        self.new_game = game_creator

    def set_player_per_game(self, player_per_game=4):
        """Sets the number of player that should play against each other in one game"""
        self.num_player_per_game = player_per_game
    # endregion

    # region: simulation methods
    def init_combinations(self):
        """This method should be called before the first game is simulated. A combination of all
        index lists that should be simulated is created depending on simulation_type"""
        if self.simulation_type == 'all':
            player_indices = [i for i in range(len(self.players))]
            combinations = itertools.combinations(player_indices, self.num_player_per_game)
            self.player_combinations = list(combinations)
            self.num_games = len(self.player_combinations)

    def get_player_subgroup(self, game_index):
        """Returns a subgroup of the players for one specific game simulation
        :param game_index: index of the combination list that should be returned
        :return: a list of players"""
        player_subgroup = []
        player_index_list = self.player_combinations[game_index]
        for i in player_index_list:
            pl = self.players[i]
            pl.clear()
            player_subgroup.append(pl)
        return player_subgroup

    def start(self):
        """Function to start all simulations of all specified game player_combinations"""
        self.init_combinations()
        self.player_outcomes = [[None for _ in range(self.num_games)] for _ in range(len(self.players))]
        self.games = [None for _ in range(self.num_games)]
        for i in range(self.num_games):
            self.game_index = i
            self.make_game()

    def make_game(self):
        """Simulates on distinct game in this setup"""
        print('Make game {:d}/{:d}'.format(self.game_index, self.num_games))

        player_subgroup = self.get_player_subgroup(self.game_index)
        current_game = self.new_game(player_subgroup)
        current_game.play()
        self.games[self.game_index] = current_game
        final_result = current_game.get_final_stats()
        for i in range(self.num_player_per_game):
            player_index = self.player_combinations[self.game_index][i]
            self.player_outcomes[player_index][self.game_index] = final_result[i]

    def player_outcome_without_none(self):
        return
    # endregion

    # region: visualization
    def chart_line_all_rounds(self):
        """Creates a line chart to visualize all rounds"""
        plt.figure(figsize=(8., 6.))

        for player_index in range(len(self.players)):
            x_values = [i for i in range(self.num_games) if self.player_outcomes[player_index][i] is not None]
            y_values = list(filter(lambda x: x is not None, self.player_outcomes[player_index]))
            player_str = '{:d}: {:s}'.format(player_index, str(self.players[player_index]))
            plt.plot(x_values, y_values, 'x-', label=player_str)

        x_values = [i for i in range(self.num_games)]
        x_labels = self.player_combinations
        plt.xticks(x_values, x_labels, rotation=90)
        plt.title("Game outcomes of \"{:s}\"".format(self.name))
        plt.xlabel("Round combinations")
        plt.ylabel("Outcome Money")
        plt.subplots_adjust(bottom=0.34)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), ncol=3)
        plt.show()

    def chart_pie_outcomes(self):
        """Creates a pie chart to visualize the max outcome money and the mean outcome per round"""
        # Total, Mean per round
        fig, axs = plt.subplots(2, 2, figsize=(8, 6))

        data_values = [[item for item in sublist if item is not None] for sublist in self.player_outcomes]
        labels = [str(self.players[i]) for i in range(len(self.players))]

        mean_outcomes = [sum(outcomes) / len(outcomes) for outcomes in data_values]
        wedges1, _ = axs[0, 0].pie(mean_outcomes)
        axs[0, 0].set_title('Mean outcome')
        legend_colors = [w.get_facecolor() for w in wedges1]

        med_outcomes = [median(outcomes) for outcomes in data_values]
        axs[0, 1].pie(med_outcomes, colors=legend_colors)
        axs[0, 1].set_title('Median outcome')

        max_outcomes = [max(outcomes) for outcomes in data_values]
        axs[1, 0].pie(max_outcomes, colors=legend_colors)
        axs[1, 0].set_title('Maximum outcome')

        min_outcomes = [max(min(outcomes), 0.1) for outcomes in data_values]
        axs[1, 1].pie(min_outcomes, colors=legend_colors)
        axs[1, 1].set_title('Minimum outcome')

        handles = [Patch(color=legend_colors[i], label=labels[i]) for i in range(len(labels))]
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.015), ncols=2)
        plt.suptitle("Pie charts of \"{:s}\"".format(self.name))
        plt.subplots_adjust(bottom=0.2)
        plt.show()

    def chart_boxplot(self, is_log=False):
        """Creates a boxplot chart to visualize the outcome quartiles of the player"""
        plt.figure(figsize=(8, 6))

        if is_log:
            data_values = [[math.log1p(item) for item in sublist if item is not None] for sublist in
                           self.player_outcomes]
        else:
            data_values = [[item for item in sublist if item is not None] for sublist in
                           self.player_outcomes]

        plt.boxplot(data_values, vert=True, patch_artist=True)

        x_values = [i for i in range(1, len(self.players) + 1)]
        x_labels = [str(self.players[i]) for i in range(len(self.players))]
        plt.xticks(x_values, x_labels, rotation=30, ha='right')
        plt.subplots_adjust(bottom=0.28)

        plt.title("Boxplots of \"{:s}\"".format(self.name))
        if is_log:
            plt.ylabel("Log outcome Money")
        else:
            plt.ylabel("Outcome Money")
        plt.show()

    def chart_heatmap(self, value_type='abs'):
        """Creates a heatmap chart to visualize how the players compete against each other players
        :param value_type: Determines what in shown in the heatmap
            'abs'     Absolute value of the outcome in each duel
            'rel'     Relative value (difference) between the outcomes
            'abs_log' Log of absolute values of the outcome
            'rel_log' Log of differences"""

        # Restricted to two players per game
        if self.num_player_per_game != 2:
            return

        plt.figure(figsize=(10, 6))

        # Create a 2D array (matrix) for heatmap
        heatmap_data = np.empty((len(self.players), len(self.players)))
        heatmap_data[:] = np.nan
        for i in range(len(self.player_combinations)):
            combination = self.player_combinations[i]
            if value_type == 'abs' or value_type == 'abs_log':
                heatmap_data[combination[0], combination[1]] = self.player_outcomes[combination[0]][i]
                heatmap_data[combination[1], combination[0]] = self.player_outcomes[combination[1]][i]
            elif value_type == 'rel_log':
                difference = self.player_outcomes[combination[0]][i] / self.player_outcomes[combination[1]][i]
                heatmap_data[combination[0], combination[1]] = difference
                heatmap_data[combination[1], combination[0]] = 1. / difference
            else:
                difference = self.player_outcomes[combination[0]][i] - self.player_outcomes[combination[1]][i]
                heatmap_data[combination[0], combination[1]] = difference
                heatmap_data[combination[1], combination[0]] = -difference

        if value_type == 'abs_log' or value_type == 'rel_log':
            heatmap_data = np.log1p(heatmap_data)

        labels = [f'{str(i)}: {str(self.players[i])}' for i in range(len(self.players))]

        # Plot the heatmap
        sns.heatmap(heatmap_data, annot=True, cmap='viridis', cbar=False, xticklabels=list(range(len(self.players))),
                    yticklabels=labels)
        plt.subplots_adjust(top=0.9, left=0.4)
        plt.xlabel("Opponent")
        plt.ylabel("Player performances")
        type_string = ""
        if value_type == 'abs':
            type_string = 'Absolute outcomes'
        elif value_type == 'rel':
            type_string = 'Relative outcomes'
        elif value_type == 'abs_log':
            type_string = 'Log absolute outcomes'
        elif value_type == 'rel_log':
            type_string = 'Log relative outcomes'
        plt.title(self.name + f' ({type_string})')
        plt.show()

    def chart_heatmap_outcome(self, is_log=False):
        """Creates a heatmap chart to visualize the results each game"""
        plt.figure(figsize=(10, 6))

        # Create a 2D array (matrix) for heatmap
        heatmap_data = np.array(self.player_outcomes, dtype='float64')
        if is_log:
            heatmap_data = np.log(heatmap_data)
        labels = [f'{str(i)}: {str(self.players[i])}' for i in range(len(self.players))]

        # Plot the heatmap
        sns.heatmap(heatmap_data, annot=True, cmap='viridis', cbar=False, xticklabels=self.player_combinations,
                    yticklabels=labels)
        plt.subplots_adjust(top=0.9, left=0.4)
        plt.xlabel("Player combination")
        plt.ylabel("Player outcomes")
        type_string = "Absolute outcomes"
        if is_log:
            type_string = 'Log outcomes'
        plt.title(self.name + f' ({type_string})')
        plt.show()

    def chart_gaussian(self, is_log=False):
        """Creates a line chart to visualize how the players compete against the other players with plotted gaussian of
        their outcomes"""
        plt.figure(figsize=(8., 6.))

        outcome_values = np.array(self.player_outcomes, dtype='float64')

        if is_log:
            outcome_values = np.log1p(outcome_values)

        mean = np.nanmean(outcome_values, axis=1)
        var = np.nanstd(outcome_values, axis=1)
        max_value = np.max(mean + 3*var)
        if is_log:
            x_values = np.logspace(-1, np.log10(max_value), 100)
        else:
            x_values = np.linspace(0, max_value, 100)

        for player_index in range(len(self.players)):
            normal_distribution = stats.norm.pdf(x_values, mean[player_index], var[player_index])
            player_str = '{:d}: {:s}'.format(player_index, str(self.players[player_index]))
            plt.plot(x_values, normal_distribution, '-', label=player_str)

        plt.title("Game outcomes of \"{:s}\"".format(self.name))
        if is_log:
            plt.xlabel("Log output money")
        else:
            plt.xlabel("Output money")
        plt.ylabel("Probability")
        plt.subplots_adjust(bottom=0.34)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), ncol=2)
        plt.show()
    # endregion

    # region: save data
    def save_player_outcomes(self):
        labels = [f'{str(i)}: {str(self.players[i])}' for i in range(len(self.players))]
        with open(self.name + '.txt', 'w') as f:
            f.write(str(labels))
            f.write('\n')
            f.write(str(self.player_outcomes))
            f.close()
    # endregion
