from main import NUM_PLAYERS, NUM_ROUNDS, INCREMENTAL_MULTIPICATOR, STARTING_MONEY


class Game:
    def __init__(self, players):
        self.players = players
        self.previous_rounds = []

    def get_previous_rounds(self):
        return self.previous_rounds

    def play(self):
        num_players = len(self.players)
        for i in range(NUM_ROUNDS):
            money_of_bank = 0

            for player in self.players:
                money_of_bank += player.pay_money()

            money_of_bank = money_of_bank * INCREMENTAL_MULTIPICATOR
            money_return = money_of_bank / num_players
            self.previous_rounds.append(money_return)

            for player in self.players:
                player.win_money(money_return)

    def get_states(self):
        money_stats = []
        for player in self.players:
            money_stats.append(player.money)
        return money_stats
