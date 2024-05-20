import unittest
from src.player import *
from src.game import NoMoneyCreation, MultiplicationGame


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.players = [
            AllIn(),
            PartOfReturn(0.1, 0.5),
            PartOfOthers(0.1, 0.4),
            RandomPlayer(10),
            LinearExtrapolation(0.2)
        ]
        self.game = NoMoneyCreation(self.players)

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

    def test_repetive_pattern_player(self):
        percentage_list = [0.2, 0.5, 0., 1.]
        money_multiplier = 2.
        num_rounds = 12
        player = RepetitivePattern(percentage_list, starting_money=STARTING_MONEY)
        game = MultiplicationGame([player], num_rounds=num_rounds, money_multiplier=money_multiplier)
        game.play()
        game_stats = game.get_states()
        print("[" + ", ".join([f"{round_stats[0]:.1f}" for round_stats in game_stats]) + "]")

        final_money = STARTING_MONEY
        print("[", end="")
        for i in range(num_rounds):
            print(final_money, end=", ")
            final_money += percentage_list[i % len(percentage_list)] * final_money
        print(str(final_money) + "]")

        self.assertAlmostEqual(game_stats[-1][0], final_money)


if __name__ == '__main__':
    unittest.main()
