import math
import itertools


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
        self.player_per_game = 0
        self.player_outcomes = []
        self.combinations = []
        self.current_game_index = 0

    # region: creator methods
    def set_players(self, players):
        """Used to set the players for this setup
        :param players: list with all players in this setup"""
        self.players = players

    def set_game_creator(self, game_creator):
        """Sets a lambda expression to create a new game with players
        :param game_creator: lambda expression with argument players_list"""
        self.new_game = game_creator

    def set_player_per_game(self, player_per_game):
        """Sets the number of player that should play against each other in one game"""
        self.player_per_game = player_per_game
    # endregion

    def get_num_games(self):
        """This method returns the total number of games played in this setup. differs by num of players
        and the simulation_type"""
        if self.simulation_type == 'all':
            return math.comb(len(self.players), self.player_per_game)
        return 0

    def init_combinations(self):
        """This method should be called before the first game is simulated. A combination of all
        index lists that should be simulated is created depending on simulation_type"""
        if self.simulation_type == 'all':
            player_indices = [i for i in range(len(self.players))]
            self.combinations = itertools.combinations(player_indices, self.player_per_game)
        return 0

    def get_player_subgroup(self, combination_index):
        """Returns a subgroup of the players for one specific game simulation
        :param combination_index: index of the combination list that should be returned
        :return: a list of players"""
        player_subgroup = []
        player_index_list = self.combinations[combination_index]
        for i in player_index_list:
            pl = self.players[i]
            pl.clear()
            player_subgroup.append(pl)
        return player_subgroup

    def start(self):
        """Function to start all simulations of all specified game combinations"""
        self.init_combinations()
        for i in range(self.get_num_games()):
            self.current_game_index = i
            self.make_game()

    def make_game(self):
        """Simulates on distinct game in this setup"""
        player_subgroup = self.get_player_subgroup(self.current_game_index)
        current_game = self.new_game(player_subgroup)
        current_game.play()
