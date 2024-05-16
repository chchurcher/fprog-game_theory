from main import NUM_PLAYERS, NUM_ROUNDS, INCREMENTAL_MULTIPICATOR, STARTING_MONEY
from random import random
from sklearn.linear_model import LinearRegression
import numpy as np


class Player:
    """Parent class to represent a player with only the information he has in his point of view.
    Should be inherited"""

    def __init__(self, strategy):
        self.strategy = strategy
        self.money = STARTING_MONEY
        self.giveaways = []
        self.previous_rounds = lambda: []

    def set_previous_rounds(self, previous_rounds):
        """
        This method is used to give a function to the Player class to get the information
         what everybody got in the last round back.

        :param previous_rounds: function to return a list of all the money the players
         got in the last rounds.
        """
        self.previous_rounds = previous_rounds

    def win_money(self, win):
        """
        Increases the money of the player by the amount won.

        :param win: float of the winning amount in this round
        """
        self.money += win

    def pay_money(self):
        """
        Method to be used to get the money of the next round.
        :return: the amount of the money given to the bank
        """
        desire = self.pay_desire()

        # Protect the players to give more away than what they have
        if desire > self.money:
            desire = self.money

        self.giveaways.append(desire)
        self.money -= desire
        return desire

    def pay_desire(self):
        """
        Abstract method to be implemented by child classes to calculate the next rounds with their strategies.
        """
        pass

    def rounds_total_given(self) -> []:
        """
        Calculates the total given amounts of all the previous rounds

        :return: float list with the number of total given
        """
        return self.previous_rounds()


class AllIn(Player):
    """This player always gives all his money in the envelope"""

    def __init__(self):
        """
        Constructor method of this player type
        """
        super().__init__(AllIn.__name__)

    def pay_desire(self):
        """
        Implementation of the pay_desire method. It is called to calculate the money which is
        then given into the envelope

        :return: float of money that should be given away
        """
        return self.money


class PartOfReturn(Player):
    """This player starts with a percentage of the starting money calculated
     with the given part_of_starting.
     All next rounds then he gives a percentage of his returned money of the
     last round (part_of_return)"""

    def __init__(self, part_of_starting, part_of_return):
        """
        Constructor method of this player type

        :param part_of_starting: float between 0..1 to calculate the amount given at the start
        :param part_of_return: positive float to calculate what percentage should be given
         from the return of the last round
        """
        super().__init__(PartOfReturn.__name__)
        self.part_of_starting = part_of_starting
        self.part_of_return = part_of_return

    def pay_desire(self):
        """
        Implementation of the pay_desire method. It is called to calculate the money which is
        then given into the envelope

        :return: float of money that should be given away
        """
        if len(self.giveaways) == 0:
            return self.money * self.part_of_starting
        else:
            return self.previous_rounds()[:-1] * self.part_of_return


class PartOfOthers(Player):
    """This player starts with a percentage of the starting money calculated
     with the given part_of_starting.
     All next rounds he gives a percentage of the values the other players
     (without him) gave the last round"""

    def __init__(self, part_of_starting, part_of_others):
        """
        Constructor method of this player type

        :param part_of_starting: float between 0..1 to calculate the amount given at the start
        :param part_of_others: positive float to calculate what percentage should be given
         of the others input the last round
        """
        super().__init__(PartOfOthers.__name__)
        self.part_of_starting = part_of_starting
        self.part_of_others = part_of_others

    def pay_desire(self):
        """
        Implementation of the pay_desire method. It is called to calculate the money which is
        then given into the envelope

        :return: float of money that should be given away
        """
        if len(self.giveaways) == 0:
            return self.money * self.part_of_starting
        else:
            previous_others_given = self.rounds_total_given()[-1] - self.giveaways[-1]
            return previous_others_given * self.part_of_others / (NUM_PLAYERS - 1)


class RandomPlayer(Player):
    """This player always just gives a random amount from his money in"""

    def __init__(self):
        """
        Constructor method of the random player
        """
        super().__init__(RandomPlayer.__name__)

    def pay_desire(self):
        """
        Implementation of the pay_desire method. It is called to calculate the money which is
        then given into the envelope

        :return: float of money that should be given away
        """
        return random() * self.money


class LinearExtrapolation(Player):
    """The LinearExtrapolation player always calculates a linear regression
    of the mean amount given by the other players and extrapolates this to
    the next round.
    All rounds are weighted with an exponential function into the past."""

    def __init__(self, part_of_starting):
        """
        Constructor method of this player type

        :param part_of_starting: float between 0..1 to calculate the amount given at the start
         of the others input the last round
        """
        super().__init__(LinearExtrapolation.__name__)
        self.part_of_starting = part_of_starting

    def pay_desire(self):
        """
        Implementation of the pay_desire method. It is called to calculate the money which is
        then given into the envelope

        :return: float of money that should be given away
        """
        if len(self.giveaways) == 0:
            return self.money * self.part_of_starting
        else:
            previous_others_given = self.rounds_total_given() - self.giveaways
            mean_others_given = previous_others_given / (NUM_PLAYERS - 1)

            num_rounds = len(previous_others_given)
            model = LinearRegression()
            x_data = [i for i in range(num_rounds)]
            weight = np.exp(x_data)
            model.fit(x_data, mean_others_given, weight)
            return model.predict(num_rounds)
