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

        # Calculate the stats at the beginning of the game
        money_starting_stats = []
        for player in players:
            money_starting_stats.append(player.money)
        self._money_stats = [money_starting_stats]

    def play(self):
        """This method begins the simulation of the game"""
        for i in range(START_ROUND, START_ROUND + self.num_rounds):
            self.current_round = i
            self.make_round()

    def make_round(self):
        """Every round starts by calling this method.
        First the money of the player is gotten
        Second the money is increased or decreased
        Finally the money is distributed"""
        current_money_given_list = []
        for player in self.players:
            current_money_given_list.append(player.pay_money())
        self._money_given_array.append(current_money_given_list)

        money_return = self.calc_return_money()
        self.money_return_list = money_return

        self._money_stats.append([])
        for player in self.players:
            player.win_money(money_return)
            self._money_stats[-1].append(player.money)

    def get_states(self):
        """Method the get the money values of the players
        :return: array with lists containing the money of every player"""
        return self._money_stats

    def get_num_players(self):
        """Getter method for getting the number of player in this round
        :return: integer with number of player in this round"""
        return len(self.players)

    def get_money_given_in_total_list(self):
        """Getter method for summing up the total money given each round
        :return: list with float of total money inputted"""
        return [sum(money_given_round) for money_given_round in self._money_given_array]

    def calc_return_money(self) -> float:
        """Abstract method for calculating the return money on different methods
        :return: float of how much each player should get back"""
        pass
