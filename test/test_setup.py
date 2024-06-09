import unittest
from src.setup import *
import src.player as player
import src.game as game
import math


class TestSetup(unittest.TestCase):
    def setUp(self):
        players = [
            player.AllIn(),
            player.PartOfReturn(0.1, 0.5),
            player.PartOfOthers(0.1, 0.4),
            player.RandomPlayer(10),
            player.LinearExtrapolation(0.1)
        ]

        def game_creator(p): return game.NoMoneyCreation(players=p)
        setup1 = Setup(name='TestSetup', simulation_type='all')
        setup1.set_players(players)
        setup1.set_player_per_game(3)
        setup1.set_game_creator(game_creator)
        self.setup1 = setup1

    def test_num_combinations(self):
        expected = math.comb(len(self.setup1.players), self.setup1.num_player_per_game)
        self.setup1.init_combinations()
        actual = len(self.setup1.player_combinations)
        self.assertEqual(actual, expected)

    def test_init_combinations(self):
        self.setup1.set_player_per_game(4)
        self.setup1.init_combinations()
        actual = self.setup1.player_combinations
        expected = [
            (1, 2, 3, 4),
            (0, 2, 3, 4),
            (0, 1, 3, 4),
            (0, 1, 2, 4),
            (0, 1, 2, 3)
        ]
        self.assertEqual(sorted(actual), sorted(expected))


if __name__ == '__main__':
    unittest.main()
