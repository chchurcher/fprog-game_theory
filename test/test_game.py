import unittest
from src.game import *
import src.player as player


class TestGame(unittest.TestCase):
    def setUp(self):
        self.num_players = 5
        self.allInPlayers = [player.AllIn() for _ in range(self.num_players)]
        self.randomPlayers = [player.RandomPlayer(seed=i)
                              for i in range(self.num_players)]
        self.randomPlayers = [player.RandomPlayer(seed=i)
                              for i in range(self.num_players)]
        self.differentPlayers = [
            player.AllIn(),
            player.PartOfReturn(0.1, 0.5),
            player.PartOfOthers(0.1, 0.4),
            player.RandomPlayer(10),
            player.LinearExtrapolation(0.1)
        ]

        game = NoMoneyCreation(self.allInPlayers, num_rounds=7)
        game.current_round = 2
        game._money_given_array = [[player.STARTING_MONEY] * self.num_players] * game.current_round
        game.money_return_list = [player.STARTING_MONEY] * game.current_round
        game._money_stats = [[player.STARTING_MONEY] * self.num_players] * (game.current_round + 1)
        self.allInGameSecondRound = game

    def test_get_previous_rounds(self):
        game = NoMoneyCreation()
        game._money_given_array = [[7, 1, 3, 5], [3, 1, 4, 2]]
        self.assertEqual(game.get_money_given_in_total_list(), [16, 10])

    def test_zero_round(self):
        game = NoMoneyCreation(self.differentPlayers, num_rounds=4)
        for participant in game.players:
            participant.money = 0
        game.make_round()
        self.assertEqual(game.get_money_given_in_total_list()[-1], 0)
        for participant in game.players:
            self.assertEqual(participant.money, 0)

    def test_no_money_creation(self):
        players = self.allInPlayers
        noMoneyCreationGame = NoMoneyCreation(players, num_rounds=7)
        noMoneyCreationGame.play()

        money_total = 0.
        for participant in players:
            money_total += participant.money
        self.assertAlmostEqual(money_total, player.STARTING_MONEY * self.num_players)

    def test_multiplication_by_one(self):
        num_player = 5
        starting_money = 10.
        num_rounds = 7

        players1 = [player.RandomPlayer(seed=i, starting_money=starting_money) for i in range(num_player)]
        game1 = NoMoneyCreation(players1, num_rounds=num_rounds)
        game1.play()

        players2 = [player.RandomPlayer(seed=i, starting_money=starting_money) for i in range(num_player)]
        game2 = MultiplicationGame(players2, num_rounds=num_rounds, money_multiplier=1.)
        game2.play()

        self.assertEqual(game1.get_states(), game2.get_states())

    def test_doubling_game(self):
        num_rounds = 7

        game1 = MultiplicationGame(self.allInPlayers, num_rounds=num_rounds, money_multiplier=2.)
        game1.play()
        print(game1.get_states())

        sum_real = sum(game1.get_states()[-1])
        sum_expected = self.num_players * player.STARTING_MONEY * 2**num_rounds
        self.assertAlmostEqual(sum_real, sum_expected)

    def test_tent_to_equal(self):
        num_rounds = 100
        players = [player.FixedPart(part_to_give=0.5, starting_money=10**i)
                   for i in range(self.num_players)]
        game1 = NoMoneyCreation(players, num_rounds=num_rounds)
        game1.play()
        print(game1.get_states())

        total_starting_money = sum([10**i for i in range(self.num_players)])
        mean_starting_money = total_starting_money / self.num_players
        self.assertAlmostEqual(mean_starting_money, players[0].money)
        self.assertAlmostEqual(mean_starting_money, players[-1].money)


if __name__ == '__main__':
    unittest.main()
