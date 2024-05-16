from main import NUM_PLAYERS, NUM_ROUNDS, INCREMENTAL_MULTIPICATOR, STARTING_MONEY


class Game:
    def __init__(self, players):
        self.players = players
        self.rounds_money_list = []

    def get_previous_rounds(self):
        return self.rounds_money_list

    def play(self):
        for i in range(NUM_ROUNDS):
            self.make_round()

    def make_round(self):
        current_money_list = []
        for player in self.players:
            current_money_list.append(player.pay_money())
        self.rounds_money_list.append(current_money_list)

        money_return = self.calc_return_money()

        for player in self.players:
            player.win_money(money_return)

    def calc_return_money(self):
        num_players = len(self.players)
        money_of_bank = sum(self.rounds_money_list[-1]) * INCREMENTAL_MULTIPICATOR
        return money_of_bank / num_players

    def get_states(self):
        money_stats = []
        for player in self.players:
            money_stats.append(player.money)
        return money_stats
