import unittest
from src.player import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.players = [
            AllIn(),
            PartOfReturn(0.1, 0.5),
            PartOfOthers(0.1, 0.4),
            RandomPlayer(),
            LinearExtrapolation(0.2)
        ]

    def test_money(self):
        for player in self.players:
            try:
                self.assertGreaterEqual(float(player.money), 0)
            except ValueError:
                self.fail("Failed to convert player money into number")

    def test_play_desire(self):
        for player in self.players:
            try:
                self.assertGreaterEqual(float(player.pay_desire()), 0)
            except ValueError:
                self.fail("Failed to convert player money into number")

    def test_previous_total_given(self):
        # Eight rounds
        previous_rounds = [list(range(0, 8))]
        for player in self.players:
            player.set_previous_rounds(lambda: previous_rounds)
        total = self.players[0].rounds_total_given()
        self.assertEqual(total, previous_rounds)

    def test_all_in_player(self):
        player = AllIn()
        player.money = 10
        player.win_money(7)
        self.assertEqual(player.pay_money(), 17)
        self.assertEqual(player.money, 0)


if __name__ == '__main__':
    unittest.main()
