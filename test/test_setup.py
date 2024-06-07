import unittest
from src.setup import *
import src.player as player
import src.game as game


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
        actual = self.setup1.get_num_games()
        self.setup1.init_combinations()
        expected = len(list(self.setup1.combinations))
        self.assertEqual(actual, expected)
