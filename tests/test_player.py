from src.player import *
import unittest


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
            self.assertTrue(str(player.money).isdigit())
            self.assertGreaterEqual(player.money, 0)

    def test_play_desire(self):
        for player in self.players:
            self.assertTrue(str(player.pay_desire()).isdigit())
            self.assertGreaterEqual(player.pay_desire(), 0)


if __name__ == '__main__':
    unittest.main()
