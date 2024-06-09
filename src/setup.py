import itertools
import matplotlib.pyplot as plt


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
        plt.figure(figsize=(8., 5.))

        for player_index in range(len(self.players)):
            x_values = [i for i in range(self.num_games) if self.player_outcomes[player_index][i] is not None]
            y_values = list(filter(lambda x: x is not None, self.player_outcomes[player_index]))
            player_str = '{:d}: {:s}'.format(player_index, str(self.players[player_index]))
            plt.plot(x_values, y_values, 'x-', label=player_str)

        x_values = [i for i in range(self.num_games)]
        x_labels = self.player_combinations
        plt.xticks(x_values, x_labels, rotation=90)
        plt.title("Game simulation of \"{:s}\"".format(self.name))
        plt.xlabel("Round combination")
        plt.ylabel("Outcome Money")
        plt.subplots_adjust(bottom=0.38)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.68), ncol=3)
        plt.show()

    def chart_pie_outcomes(self):
        """Creates a pie chart to visualize the total outcome money and the mean outcome per round"""
        # Total, Mean per round

    def chart_boxplot(self):
        """Creates a boxplot chart to visualize the outcome quartiles of the player"""
        plt.figure(figsize=(6.4, 5.))

        data_values = [[item for item in sublist if item is not None] for sublist in self.player_outcomes]
        plt.boxplot(data_values, vert=True, patch_artist=True)

        x_values = [i for i in range(1, len(self.players) + 1)]
        x_labels = [str(self.players[i]) for i in range(len(self.players))]
        plt.xticks(x_values, x_labels, rotation=30, ha='right')
        plt.subplots_adjust(bottom=0.35)

        plt.title("Game simulation of \"{:s}\"".format(self.name))
        plt.ylabel("Outcome Money")
        plt.show()

    # endregion
