NUM_ROUNDS = 10
START_ROUND = 0


class Game:
    """This class handles and executes one simulation of one game."""

    def __init__(self, players=None, num_rounds=NUM_ROUNDS):
        """
        Constructor method of one game
        :param players: list with the different players playing that game
        :param num_rounds: integer with numer of rounds that should be played
        """
        if players is None:
            players = []

        self.players = players
        self._money_given_array = []  # array consisting of inputted money of players in previous rounds
        self.money_return_list = []  # list with money a player got back in previous rounds
        self.num_rounds = num_rounds
        self.current_round = 0

    def play(self):
        for i in range(START_ROUND, START_ROUND + self.num_rounds):
            self.current_round = i
            self.make_round()

    def make_round(self):
        current_money_given_list = []
        for player in self.players:
            current_money_given_list.append(player.pay_money())
        self._money_given_array.append(current_money_given_list)

        money_return = self.calc_return_money()
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

    def get_money_given_in_total_list(self):
        return [sum(money_given_round) for money_given_round in self._money_given_array]

    def calc_return_money(self) -> float:
        pass
