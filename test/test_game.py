import unittest
from src.game import *
import src.player as player


class TestGame(unittest.TestCase):
    def setUp(self):
        players = [
            player.AllIn(),
            player.PartOfReturn(0.1, 0.5),
            player.PartOfOthers(0.1, 0.4),
            player.RandomPlayer()
        ]
        self.game = Game(players)
        self.game.rounds_money_list = [[7, 1, 3, 5], [3, 1, 4, 2]]

    def test_get_previous_rounds(self):
        self.assertEqual(self.game.get_previous_rounds(), [7, 3, 6, 2])

    def test_zero_round(self):
        for participant in self.game.players:
            participant.money = 0
        self.game.make_round()
        self.assertEqual(self.game.get_previous_rounds()[-1], 0)
        for participant in self.game.players:
            self.assertEqual(participant.money, 0)

    def test_calc_return_money(self):
        self.fail()

    def test_get_states(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
