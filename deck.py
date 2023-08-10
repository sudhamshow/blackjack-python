import random
import math

# ANSI escape sequences for representing the card with colours
yellow_background = "\u001b[48;5;230m"
black = "\u001b[30;1m"
red = "\u001b[31;1m"
blue = "\u001b[34;1m"
reset_colors = "\u001b[0m"


class Card:

    def __init__(self, rank, suit):
        """
        This function initialises an object of the Card class, representing
        an actual playing card. Attributes:
        rank: (str) rank of the card
        suit: (str) suit of the cards
        up: (bool) whether the card is face up or down (True for up)
        suits_values: (str (ANSI)) Unicode representations of the cards suits
        rank_values: (int) face values of the card corresponding to the rank
        :param rank: (str) rank value of the card (2 to 'A')
        :param suit: (str) suit value of the card
        """
        self.rank = rank
        self.suit = suit
        self.up = False
        self.suits_values = {"Spades": "\u2660", "Hearts": "\u2665",
                             "Clubs": "\u2663", "Diamonds": "\u2666"}
        self.rank_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                            "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                            "K": 10}

    def __repr__(self):
        """
        This function assigns a representation for the card object based on
        the suit and if the card is face up or down, based on an actual deck
        of playing cards.
        :return: (str) representation of the card object
        """
        color = blue if not self.up else black if self.suit in \
                ["Clubs", "Spades"] else red
        return yellow_background + color + "({}, {})".format(
            *(self.rank, self.suits_values[self.suit]) if self.up else (
                "?", "?")) + reset_colors


class Deck:

    def __init__(self):
        """
        Class Deck - an aggregation of class Card objects, symbolises a deck
        of cards. Attributes:
        ranks= (str) rank of the cars from 2 to 'A'
        suits = (str) suits in a deck of playing cards
        _cards =
        """
        ranks = [str(n) for n in range(2, 11)]
        ranks += ["J", "Q", "K", "A"]
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self._cards = []
        for suit in suits:
            for rank in ranks:
                self._cards.append(Card(rank, suit))

    def __len__(self):
        """
        Returns the number of objects in the current deck
        :return: (int) size of the deck
        """
        return len(self._cards)

    def __getitem__(self, position):
        """
        This function gets the object located at 'position' place in the deck
        :param position: (int) position in the deck whose object is sought
        :return: Card object at place 'position' in the deck
        """
        return self._cards[position]

    def deal_card(self, face_up=True):
        """
        This function deals a card from the dealer's deck to the player
        :param face_up: status of the card dealt (face up or down) to
        facilitate representing face up/down cards
        :return: object Card (default Face up)
        """
        self._cards[-1].up = face_up
        return self._cards.pop()

    def put_card(self, value):
        """
        This function is used to insert a card in a particular location in
        the dealer's deck
        :param value: The position in the dealer's deck the card needs to be
        inserted at
        :return: None
        """
        self._cards.append(value)

    def shuffle(self):
        """
        This function shuffles the cards in the dealers deck randomly
        :return: None
        """
        random.shuffle(self._cards)

    def cut(self):
        """
        This function cuts the deck into half and simulates placeing the
        upper half below the lower half
        :return: None
        """
        middle = math.floor(len(self) / 2)
        self._cards.extend(self._cards[:middle])
        del self._cards[:middle]
