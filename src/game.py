from main import NUM_PLAYERS, NUM_ROUNDS, INCREMENTAL_MULTIPICATOR, STARTING_MONEY


class Game:
    def __init__(self, players):
        self.players = players
        self.money_given_array = []  # array consiting of inputed money of players in previous rounds
        self.money_return_list = []  # list with money a player got back in previous rounds

    def get_money_return_list(self):
        return self.money_return_list

    def play(self):
        for i in range(NUM_ROUNDS):
            self.make_round()

    def make_round(self):
        current_money_given_list = []
        for player in self.players:
            current_money_given_list.append(player.pay_money())
        self.money_given_array.append(current_money_given_list)

        money_return = self.calc_return_money()
        self.money_return_list = money_return

        for player in self.players:
            player.win_money(money_return)

    def calc_return_money(self):
        num_players = len(self.players)
        money_of_bank = sum(self.money_given_array[-1]) * INCREMENTAL_MULTIPICATOR
        return money_of_bank / num_players

    def get_states(self):
        money_stats = []
        for player in self.players:
            money_stats.append(player.money)
        return money_stats
