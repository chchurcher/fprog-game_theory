from abc import ABC, abstractmethod

NUM_ROUNDS = 10


class Game(ABC):
    """This class handles and executes one simulation of one played_game."""

    def __init__(self, players=None, num_rounds=NUM_ROUNDS):
        """
        Constructor method of one played_game
        :param players: list with the different players playing that played_game
        :param num_rounds: integer with numer of rounds that should be played
        """
        if players is None:
            players = []

        self.players = players
        for participant in players:
            participant.set_game_getter(lambda: self)

        self._money_given_array = []  # array consisting of inputted money of players in previous rounds
        self._money_return_list = []  # list with money a player got back in previous rounds
        self.num_rounds = num_rounds
        self.current_round = 0

        # Calculate the stats at the beginning of the played_game
        money_starting_stats = []
        for participant in players:
            money_starting_stats.append(participant.money)
        self._money_stats = [money_starting_stats]

    def play(self):
        """This method begins the simulation of the played_game"""
        for i in range(self.num_rounds):
            self.current_round = i
            self.make_round()

    def make_round(self):
        """Every round starts by calling this method.
        First the money of the player is gotten
        Second the money is increased or decreased
        Finally the money is distributed"""
        current_money_given_list = []
        for player in self.players:
            current_money_given_list.append(player.get_pay_money())
        self._money_given_array.append(current_money_given_list)

        money_return = self.calc_return_money()
        self._money_return_list.append(money_return)

        self._money_stats.append([])
        for player in self.players:
            player.set_win_money(money_return)
            self._money_stats[-1].append(player.money)

    def get_states_by_round(self):
        """Method the get the money values of the players
        :return: array with list for every round containing the money of every player"""
        return self._money_stats

    def get_states_by_player(self):
        """Method the get the money values of the players
        :return: array with list for every player containing the money in each round"""
        return [[r[p] for r in self._money_stats] for p in range(self.get_num_players())]

    def get_final_stats(self):
        """Method the get the money values of the players in the last round
        :return: list of money of every player in last round"""
        return self._money_stats[-1]

    def get_num_players(self):
        """Getter method for getting the number of player in this round
        :return: integer with number of player in this round"""
        return len(self.players)

    def get_money_given_in_total_list(self):
        """Getter method for summing up the total money given each round
        :return: list with float of total money inputted"""
        return [sum(money_given_round) for money_given_round in self._money_given_array]

    def get_money_returned_list(self):
        """Getter method for getting the _money_return_list
        :return: list with float of money returned each round"""
        return self._money_return_list

    @abstractmethod
    def calc_return_money(self) -> float:
        """Abstract method for calculating the return money on different methods
        :return: float of how much each player should get back"""
        pass


class NoMoneyCreation(Game):
    """This type of played_game doesn't add money to the played_game, just splitting it up each time"""
    
    def __str__(self):
        """String representation of this played_game"""
        return "NoMoneyCreation"

    def calc_return_money(self) -> float:
        """Method for calculating the return money by just splitting the total amount given
        :return: float of how much each player gets back"""
        total_money_given = sum(self._money_given_array[-1])
        return total_money_given / self.get_num_players()


class MultiplicationGame(Game):
    """This type of played_game multiplies the total amount of money given by the players by a certain amount"""
    
    def __str__(self):
        """String representation of this played_game"""
        return "SimpleMultiplication ({:.2f})".format(self.money_multiplier)
    
    def __init__(self, players=None, num_rounds=NUM_ROUNDS, money_multiplier=1.):
        """Constructor method for this class. If no multiplier or 1 is given it equals NoMoneyCreation"""
        super().__init__(players=players, num_rounds=num_rounds)
        self.money_multiplier = money_multiplier
    
    def calc_return_money(self) -> float:
        """Method for calculating the return money by splitting the total amount multiplied by the given multiplier
        :return: float of how much each player gets back"""
        total_money_given = sum(self._money_given_array[-1]) * self.money_multiplier
        return total_money_given / self.get_num_players()


class LinearFunctionByPlayer(Game):
    """This played_game uses as multiplier the doubled mean percentage of the individual given money"""

    def __str__(self):
        """String representation of this played_game"""
        return "LinearFunctionByPlayer"

    def calc_return_money(self) -> float:
        """Method for calculating the return money by splitting the total amount multiplied by the multiplier.
        The multiplier is calculated as the doubled mean of the percentage the players gave away
        If all player give all their money the multiplier is 2
        If all player give half of their money it is 1
        If all player give none it is obviously 0
        :return: float of how much each player gets back"""

        percentage_given_list = [1.] * self.get_num_players()
        for i in range(self.get_num_players()):
            money_given = self._money_given_array[-1][i]
            money_left = self.players[i].money

            if money_given + money_left < 1E-6:
                percentage_given_list[i] = 0.5
                continue
            percentage_given_list[i] = money_given / (money_given + money_left)

        multiplier = sum(percentage_given_list) / len(percentage_given_list) * 2.
        total_money_given = sum(self._money_given_array[-1]) * multiplier
        return total_money_given / self.get_num_players()


class LinearFunctionByTotal(Game):
    """This played_game uses as multiplier the doubled percentage of the total money given"""

    def __str__(self):
        """String representation of this played_game"""
        return "LinearFunctionByTotal"

    def calc_return_money(self) -> float:
        """Method for calculating the return money by splitting the total amount multiplied by the multiplier.
        The multiplier is calculated as the doubled percentage of the total given money
        If all player give all their money the multiplier is 2
        If player give together half of the total money it is 1
        If all player give none it is obviously 0
        :return: float of how much each player gets back"""

        total_money_left = sum([player.money for player in self.players])
        total_money_given = sum(self._money_given_array[-1])

        if total_money_given + total_money_left < 1E-6:
            total_money_left = 0.1
        multiplier = total_money_given / (total_money_given + total_money_left) * 2.
        total_money_given = sum(self._money_given_array[-1]) * multiplier
        return total_money_given / self.get_num_players()
