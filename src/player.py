from abc import ABC, abstractmethod
import random
import numpy as np
from typing import Callable
from game import Game

STARTING_MONEY = 10.
random.seed(100)


class Player(ABC):
    """Parent class to represent a player with only the information he has in his point of view.
    Should be inherited"""

    def __init__(self, starting_money=STARTING_MONEY):
        self.starting_money = starting_money
        self.money = starting_money
        self.money_paid_list = []
        self.get_game = None

    @abstractmethod
    def __str__(self):
        pass

    def clear(self):
        """Clears all variables changing during a game"""
        self.money = self.starting_money
        self.money_paid_list = []
        self.get_game = None

    def set_game_getter(self, get_game: Callable[[None], Game]):
        """
        This method is used to give a function to the Player class to get information about the played_game
        :param get_game: function to return the played_game this instance is playing
        """
        self.get_game = get_game

    def set_win_money(self, win: float):
        """
        Increases the money of the player by the amount won.
        :param win: float of the winning amount in this round
        """
        self.money += win

    def get_pay_money(self) -> float:
        """
        Method to be used to get the money of the next round.
        :return: the amount of the money given to the bank
        """
        desired_pay_money = self.ask_desired_pay_money()

        # Protect the players to give more away than what they have
        pay_money = desired_pay_money
        if desired_pay_money > self.money:
            pay_money = self.money
        pay_money = max(pay_money, 0)

        self.money_paid_list.append(pay_money)
        self.money -= pay_money
        return pay_money

    @abstractmethod
    def ask_desired_pay_money(self) -> float:
        """
        Abstract method to be implemented by child classes to calculate the desired money for the next rounds
        with their strategies.
        :return: float of money that wished to be given away
        """
        pass


# region: different player types
class AllIn(Player):
    """This player always gives all his money in the envelope"""

    def __str__(self):
        """String representation of this player"""
        return "AllIn"

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        return self.money


class FixedPart(Player):
    """This player always gives a fixed percentage of his money"""

    def __init__(self, part_to_give, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param part_to_give: float between 0..1 to calculate what percentage of money should be given
        """
        super().__init__(starting_money=starting_money)
        self.part_to_give = part_to_give

    def __str__(self):
        """String representation of this player"""
        return "FixedPart ({:.2f})".format(self.part_to_give)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        return self.money * self.part_to_give


class PartOfReturn(Player):
    """This player starts with a percentage of the starting money calculated
     with the given part_of_starting.
     All next rounds then he gives a percentage of his returned money of the
     last round (part_of_return)"""

    def __init__(self, part_of_starting, part_of_return, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param part_of_starting: float between 0..1 to calculate what percentage of start money should be given
        :param part_of_return: float between 0..1 to calculate what percentage should be given
        from the return of the last round
        """
        super().__init__(starting_money=starting_money)
        self.part_of_starting = part_of_starting
        self.part_of_return = part_of_return

    def __str__(self):
        """String representation of this player"""
        return "PartOfReturn ({:.2f}|{:.2f})".format(self.part_of_starting, self.part_of_return)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        game = self.get_game()
        if game.current_round == 0:
            return self.money * self.part_of_starting
        else:
            return game.get_money_returned_list()[-1] * self.part_of_return


class PartOfOthers(Player):
    """This player starts with a percentage of the starting money calculated
     with the given part_of_starting.
     All next rounds he gives a percentage of the values the other players
     (without him) gave the last round"""

    def __init__(self, part_of_starting, part_of_others, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param part_of_starting: float between 0..1 to calculate what percentage of start money should be given
        :param part_of_others: float between 0..1 to calculate what percentage should be given
         of the others input the last round
        """
        super().__init__(starting_money=starting_money)
        self.part_of_starting = part_of_starting
        self.part_of_others = part_of_others

    def __str__(self):
        """String representation of this player"""
        return "PartOfOthers ({:.2f}|{:.2f})".format(self.part_of_starting, self.part_of_others)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        game = self.get_game()
        if game.current_round == 0:
            return self.money * self.part_of_starting
        else:
            previous_others_given = game.get_money_given_in_total_list()[-1] - self.money_paid_list[-1]
            return previous_others_given * self.part_of_others / (game.get_num_players() - 1)


class RandomPlayer(Player):
    """This player always just gives a random amount from his money in"""

    def __init__(self, seed, starting_money=STARTING_MONEY):
        """
        Constructor method of the random player
        :param seed: seed for calculating random values
        """
        super().__init__(starting_money=starting_money)
        self.seed = seed
        self.random_gen = random.Random(seed)

    def __str__(self):
        """String representation of this player"""
        return "RandomPlayer ({:d})".format(self.seed)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        return self.random_gen.random() * self.money


class LinearExtrapolation(Player):
    """The LinearExtrapolation player always calculates a linear regression
    of the mean amount given by the other players and extrapolates this to
    the next round.
    All rounds are weighted with an exponential function into the past."""

    def __init__(self, part_of_starting, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param part_of_starting: float between 0..1 to calculate what percentage of start money should be given
        """
        super().__init__(starting_money=starting_money)
        self.part_of_starting = part_of_starting

    def __str__(self):
        """String representation of this player"""
        return "LinearExtrapolation ({:.2f})".format(self.part_of_starting)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        game = self.get_game()
        if game.current_round == 0:
            return self.money * self.part_of_starting
        elif game.current_round == 1:
            others_given = game.get_money_given_in_total_list()[0] - self.money_paid_list[0]
            return others_given / (game.get_num_players() - 1)
        else:
            total_given = np.asarray(game.get_money_given_in_total_list(), dtype='float64')
            self_given = np.asarray(self.money_paid_list, dtype='float64')
            others_given = np.subtract(total_given, self_given)
            num_played_rounds = np.shape(others_given)[-1]
            mean_others_given = others_given / (game.get_num_players() - 1)

            x_data = np.arange(num_played_rounds)
            weight = np.exp(x_data)
            slope, intercept = np.polyfit(x_data, mean_others_given, deg=1, w=weight)
            return slope * num_played_rounds + intercept


class RepetitivePattern(Player):
    """The RepetitivePattern player uses a pattern repetitively of which he calculates the amount to give"""

    def __init__(self, percentage_list, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param percentage_list: list of floats between 0..1 to calculate what percentage should be given.
        Each round the next entry is used
        """
        super().__init__(starting_money=starting_money)
        self.percentage_list = percentage_list

    def __str__(self):
        """String representation of this player"""
        formatted_list = [f"{percentage:.2f}" for percentage in self.percentage_list]
        formatted_str = ", ".join(formatted_list)
        return "RepetitivePattern ({:s})".format(formatted_str)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        game = self.get_game()
        return self.money * self.percentage_list[game.current_round % len(self.percentage_list)]


class GrimTrigger(Player):
    """The GrimTrigger player only cooperates when a certain input trigger is exceeded by others"""

    def __init__(self, trigger_value, starting_money=STARTING_MONEY):
        """
        Constructor method of this player type
        :param trigger_value: value of money that triggers the cooperation
        """
        super().__init__(starting_money=starting_money)
        self.trigger_value = trigger_value

    def __str__(self):
        """String representation of this player"""
        return "PartOfOthers ({:.2f})".format(self.trigger_value)

    def ask_desired_pay_money(self):
        """
        Implementation of the ask_desired_pay_money method. It is called to calculate the money which is
        then given into the envelope
        :return: float of money that wished to be given away
        """
        game = self.get_game()
        if game.current_round == 0:
            return 0
        else:
            previous_others_given = game.get_money_given_in_total_list()[-1] - self.money_paid_list[-1]
            if previous_others_given > self.trigger_value:
                return self.money
            else:
                return 0
# endregion


# region: static functions
def clear_all_players(players):
    for player in players:
        player.clear()
# endregion
