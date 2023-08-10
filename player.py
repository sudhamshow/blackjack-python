from abc import ABC, abstractmethod
from tools import *
import random
import time

busted_list = ["😭", "🤦", "😱", "💔", "👎", "🙈"]


def prompt_name(player):
    """
    This function prompts for the player's name and renames the player
    character if requested.
    :param player: Player object whose name is prompted to be changed
    :return: None
    """
    time.sleep(0.5)
    player_type = "(h)uman" if player.type == 'h' else "(b)ot"
    print("{} is of type {}. Would you like to rename {}?".format(player.name,
                                                                  player_type,
                                                                  player.name))
    decision = validate_input(['y', 'n'],
                              "Press y to rename player and n if you don't",
                              " is not a valid input. Please press y to rename "
                              "the player and n if you don't")
    if decision == 'y':
        name = input("Please type name and press enter key: \n")
        player.name = name
        clear_prev_lines(2)
        time.sleep(0.5)
    clear_prev_lines(1)


class Player(ABC):
    def __init__(self):
        """
        This class is a Player base class to be inherited by all the
        participants of the game. It contains attributes common to all the
        participants of the game
        id: (int) unique id of the player in the game
        name: (str) Name of the player
        type: (str) Type of the player
        cards: (list(Card)) List of card objects
        score:(int) Score of the participant
        have_Ace: (bool) If the participant has an Ace in hand
        status: (str) Emphatic representation of the player's status in the game
        """
        self.id = 0
        self.name = "default"
        self.type = "default"
        self.cards = []
        self.score = 0
        self.have_Ace = False
        self.status = ""

    def __repr__(self):
        """
        This function creates a printing representation for the objects of the
        class (and inheriting classes)
        :return: (str) representation of the Player object
        """
        return f"{self.name} ({self.type}) : {self.cards}  {self.status}"

    @abstractmethod
    def call(self):
        pass

    def update_score(self, card):
        """
        This function calculates the total score of the hand of the participant
        :param card: (Card) Card object, which on receiving, the player's
        score is updated.
        :return: None
        """
        if card.rank == 'A':
            if self.score < 11:
                self.score += 11
                self.have_Ace = True
            else:
                self.score += 1
        else:
            self.score += card.rank_values[card.rank]
        if self.score > 21 and self.have_Ace:
            self.score -= 10
            self.have_Ace = False
        self.update_status()

    def update_status(self):
        """
        This function updates the status of the player, if they go bust
        :return: None
        """
        if self.score > 21:
            self.status = "You got busted!!! " + (random.sample(busted_list,
                                                                1))[0]


class HumanPlayer(Player):
    def __init__(self, name):
        """
        This class creates a human player object and prompts for a name change
        name = (str) Name of the player
        type = (str) type of the player ('h' for human)
        :param name: (str) default name assigned by the game
        """
        super().__init__()
        self.name = name
        self.type = 'h'
        prompt_name(self)

    def call(self):
        """
        This method enables the player to 'call' their decisions based on their
        current hand. The method prompts the human user to input actions in
        the game.
        :return: (str) Decision of the human player (hit ('h') or stay ('s'))
        """
        return validate_input(['h', 's'],
                              "Please press h to hit or s to stay",
                              " is not a valid input. Please press h to hit, "
                              "or s to stay")


class ComputerPlayer(Player):
    def __init__(self, name):
        """
        This class creates a human player object and prompts for a name change
        name = (str) Name of the player
        type = (str) type of the player ('b' for bot)
        threshold = random integer between 14 and 18 (both inclusive) above
        which the computer player will not ask to hit
        :param name: (str) default name assigned by the game
        """
        super().__init__()
        self.name = name
        self.type = 'b'
        self.threshold = random.randint(14, 18)
        prompt_name(self)

    def call(self):
        """
        This method enables the bot to 'call' their decisions based on their
        current hand. The bot asks to hit if the current hand score is below
        the threshold else stay with the hand
        :return: (str) Decision of the computer player (hit ('h) or stay ('s'))
        """
        print("{} is playing... ".format(self.name), end="")
        time.sleep(random.uniform(1, 2.5))  # to simulate delay in player
        # decision
        if self.score < self.threshold:
            print("{} chose to Hit.".format(self.name))
            time.sleep(2)
            clear_prev_lines(1)
            sys.stdout.flush()
            return 'h'
        else:
            print("{} chose to Stay.".format(self.name))
            time.sleep(2)
            clear_prev_lines(1)
            sys.stdout.flush()
            return 's'


class Dealer(Player):
    def __init__(self, game_deck):
        """
        This method initialises a dealer object for the game and gets the
        deck of cards ready to be dealt to players. Attributes:
        deck = (class Deck) Deck of cards with the dealer for playing blackjack
        :param game_deck: (class Deck) Deck of cards used by the game
        """
        super().__init__()
        self.name = "Dealer"
        self.type = "dealer"
        self.deck = game_deck
        self.deck.shuffle()
        self.deck.cut()
        self.deck.shuffle()

    def __repr__(self):
        """
        Representation of the dealer object. Prints name and hand
        :return: None
        """
        return f"{self.name} : {self.cards}"

    def deal(self, player_list):
        """
        This method deals the cards to all the players on the table (for the
        first round before the actual game begins)
        :param player_list: (list(class Player)) The list of players for whom
        the cards (2 cards) are to be dealt.
        :return: None
        """
        for player in player_list[0:-1]:
            card = self.deck.deal_card()
            player.update_score(card)
            player.cards.append(card)
            update_current_line(player)
            card = self.deck.deal_card()
            player.update_score(card)
            player.cards.append(card)
            print(player, end="\n\n")
            time.sleep(1)
        self.cards.append(self.deck.deal_card())
        self.update_score(self.cards[-1])
        update_current_line(self)
        self.cards.append(self.deck.deal_card(False))
        print(self, end="\n\n")
        time.sleep(1)

    def poll(self, player):
        """
        This method enables the dealer to request the player for his decision
        in the game
        :param player: (class Player) Player from whom decision is elicited.
        :return: (str) Decision taken by the player
        """
        read = player.call()
        if read == 'h':
            card = self.deck.deal_card()
            player.update_score(card)
            player.cards.append(card)
            return "hit"
        elif read == 's':
            return "stay"
        else:
            return "quit"

    def call(self):
        """
        This method forces the dealer to deal cards to himself until the
        score of his hands reaches 17 or above.
        :return: (str) Clue to himself - to hit if hand score is less than 17,
        else stay
        """
        print("{} is Playing..".format(self.name))
        time.sleep(1.5)
        if self.score < 17:
            clear_prev_lines(1)
            return 'h'
        else:
            clear_prev_lines(1)
            return 's'

    def flip_card_up(self):
        """
        This method gets the dealer to flip up his face down card after all
        the players have finished their turns
        :return: None
        """
        self.cards[-1].up = True
        self.update_score(self.cards[-1])

    def collect(self, player):
        """
        This method enables the dealer to collect  the cards from the
        player in the game and put it back in his deck.
        :param player: (class Player) The player whose cards are collected by the dealer
        :return: None
        """
        self.deck._cards.extend(player.cards)
        player.cards.clear()

    def update_status(self):
        """
        This method creates a non-emphatic muted status for the dealer
        regardless of his score
        :return:
        """
        self.status = ""
