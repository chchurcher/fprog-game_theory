import unittest
from src.game import *
import src.player as player


class TestGame(unittest.TestCase):
    def setUp(self):
        players = [
            player.AllIn(),
            player.PartOfReturn(0.1, 0.5),
            player.PartOfOthers(0.1, 0.4),
            player.RandomPlayer(10)
        ]
        self.game = NoMoneyCreation(players)
        self.game._money_given_array = [[7, 1, 3, 5], [3, 1, 4, 2]]
        self.game.current_round = 2
        self.game.money_return_list = [5, 4]

    def test_get_previous_rounds(self):
        self.assertEqual(self.game.get_money_given_in_total_list(), [16, 10])

    def test_zero_round(self):
        for participant in self.game.players:
            participant.money = 0
        self.game.make_round()
        self.assertEqual(self.game.get_money_given_in_total_list()[-1], 0)
        for participant in self.game.players:
            self.assertEqual(participant.money, 0)

    def test_no_money_creation(self):
        noMoneyCreationGame = NoMoneyCreation(self.game.players)
        players = [player.AllIn(), player.AllIn(), player.AllIn(), player.AllIn(), player.AllIn()]
        for participant in players:
            participant.money = 10.
        noMoneyCreationGame.num_rounds = 7
        noMoneyCreationGame.play()
        money_total = 0.
        for participant in players:
            money_total += participant.money
        self.assertAlmostEqual(money_total, 10. * 5)


if __name__ == '__main__':
    unittest.main()
