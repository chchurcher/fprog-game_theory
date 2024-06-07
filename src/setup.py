import player
import game
import numpy as np
import math


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

    def set_player(self, players):
        """Used to set the :param players for this setup"""
        self.players = players

    def set_game_creator(self, game_creator):
        """Sets a lambda expression to create a new game with players :param game_creator(players) """
        self.new_game = game_creator

    def set_player_per_game(self, player_per_game):
        """Sets the number of player that should play against each other in one game"""
        self.player_per_game = player_per_game

    def get_num_games(self):
        """This method returns the total number of games played in this setup. differs by num of players
        and the simulation_type"""
        if self.simulation_type == 'all':
            return math.comb(len(self.players), self.player_per_game)
        return 0
