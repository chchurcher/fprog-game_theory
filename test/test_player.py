import unittest
from src.player import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.players = [
            AllIn(),
            PartOfReturn(0.1, 0.5),
            PartOfOthers(0.1, 0.4),
            RandomPlayer(10),
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
                self.assertGreaterEqual(float(player.ask_desired_pay_money()), 0)
            except ValueError:
                self.fail("Failed to convert player money into number")

    def test_all_in_player(self):
        player = AllIn()
        player.money = 10
        player.set_win_money(7)
        self.assertEqual(player.get_pay_money(), 17)
        self.assertEqual(player.money, 0)

    def test_string_representation(self):
        for player in self.players:
            self.assertTrue(hasattr(player, '__str__'), "The class does not have a __str__ method")


if __name__ == '__main__':
    unittest.main()
