from typing import Callable

NUM_ROUNDS = 10


class Game:

    def __init__(self, players=None, calc_return_money=None, num_rounds=NUM_ROUNDS):
        if calc_return_money is None:
            calc_return_money: Callable[[Game], int] = lambda this_game: 0
        if players is None:
            players = []

        self.players = players
        self.money_given_array = []  # array consiting of inputed money of players in previous rounds
        self.money_return_list = []  # list with money a player got back in previous rounds
        self.calc_return_money = calc_return_money
        self.num_rounds = num_rounds
        self.current_round = 0

    def play(self):
        for i in range(self.num_rounds):
            self.current_round = i
            self.make_round()

    def make_round(self):
        current_money_given_list = []
        for player in self.players:
            current_money_given_list.append(player.pay_money())
        self.money_given_array.append(current_money_given_list)

        money_return = self.calc_return_money(self)
        self.money_return_list = money_return

        for player in self.players:
            player.win_money(money_return)

    def get_states(self):
        money_stats = []
        for player in self.players:
            money_stats.append(player.money)
        return money_stats

    def get_num_players(self):
        return len(self.players)

