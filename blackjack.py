import random
from deck import Deck
from player import HumanPlayer, ComputerPlayer, Dealer
from tools import *

print_space = 2  # spaces between printing players
players_per_deck = 6  # number of players per deck


class Game:

    def __init__(self, human_players=1, computer_players=1):
        """
        This class contains the elements of the game. This function
        initialises the number of players in the game, their names and their
        positions relative to the dealer.
        Relevance of the attributes:
        humans = number of human players
        bots = number of computer players
        table = list of Player attributes (Playing table)
        winners = a list of winners in the current round
        max_score = the score of the winner of the current round
        deck = Card deck (class Deck) used in the current game
        player_position = position of the player on the table relative to the dealer

        :param human_players:
        :param computer_players:
        """
        self.humans = human_players
        self.bots = computer_players
        clear_screen()
        self.prompt_num_players()
        self.table = []
        self.winners = []
        self.max_score = 0
        self.deck = self.create_deck()
        self.player_position = {}
        self.dealer = Dealer(self.deck)
        clear_screen()

    def create_deck(self):
        """
        This function creates a game deck based on the number of players in the
        game (to avoid card counting). With the present logic a new deck is
        added for every 6 players
        :return: a new deck object (class Deck)
        """
        temp_deck = Deck()
        temp_deck._cards *= (
                    ((self.humans + self.bots - 1) // players_per_deck) + 1)
        return temp_deck

    def show_table(self):
        """
        Prints out the whole table in a sequential format with spacing
        'print_space'
        :return: None
        """
        for person in self.table:
            print(person, end='\n' * print_space)

    def play(self):
        """
        This function starts the game. The dealer deals the cards for the
        first round, and upon user input cards are distributed eventually.
        After all player cards are dealt, dealer deals his own cards and
        subsequently the winner is announced. The user is prompted to play
        another round in the end.
        :return: None
        """
        clear_screen()
        print("Welcome to Sud's Casino")
        print("Let's play Blackjack")
        print("Human players are marked with (h) and bots with (b)", end='\n\n')
        count1 = 0
        count2 = 0
        if len(self.table) == 0:
            for count1 in range(self.humans):
                self.table.append(HumanPlayer("Player" + str(count1 + 1)))
                self.table[-1].id = count1
            for count2 in range(self.bots):
                self.table.append(
                    ComputerPlayer("Player" + str(count1 + count2 + 2)))
                self.table[-1].id = count1 + count2 + 1
            random.shuffle(self.table)
            self.table.append(self.dealer)
            self.table[-1].id = count1 + count2 + 2
        for position, player in enumerate(self.table[::-1]):
            self.player_position[player.id] = position * print_space

        self.show_table()
        if validate_input(['s', 'e'],
                          "Please press s to start or e to exit the game",
                          " is not a valid input. Please press s to start or e "
                          "to exit the game") == 'e':
            self.exit_game()
            return
        move_lines_up(len(self.table) * print_space)
        self.dealer.deal(self.table)
        for player in self.table:
            status = "hit"
            print("{}'s turn:".format(player.name))
            if player.type == "dealer":
                player.flip_card_up()
                overwrite_prev_line(player, self.player_position[player.id], 3)
            if player.score == 21:
                player.status = "Congrats you hit Blackjack 🎉 "
                overwrite_prev_line(player, self.player_position[player.id], 3)
            while player.score < 21 and status == "hit":
                status = self.dealer.poll(player)
                overwrite_prev_line(player, self.player_position[player.id], 3)
            clear_prev_lines(1)
        self.check_winner()
        self.prompt_another_round()

    def check_winner(self):
        """
        This function determines the winner of the current based on the score
        and prints the result on the screen
        :return: None
        """
        for player in self.table:
            if self.max_score <= player.score <= 21:
                if self.max_score < player.score:
                    self.winners.clear()
                self.winners.append(player)
                self.max_score = player.score
        if len(self.winners) == 0:
            print("Unlucky day!! Nobody won this round ")
        else:
            print("Winners:")
            print(*[f"{player.name}, score: "
                    f"{player.score} 🏆" for player in
                    self.winners],
                  sep="\n", end="\n\n")

    def prompt_another_round(self):
        """
        This function prompts the user for another round and if the user
        requests, initialises the game and starts it all over again.
        :return: None
        """
        for player in self.table:
            self.dealer.collect(player)
            player.status = ""
            player.score = 0
        self.max_score = 0
        self.winners.clear()
        print("Do you want to play another round of Blackjack?")
        result = validate_input(['y', 'n'],
                                "Please press y to start another round or n "
                                "to exit the game",
                                " is not a valid input. Please press y to "
                                "start a new round or n to exit the game")
        if result == 'y':
            result = validate_input(['y', 'n'],
                                    "Do you want to continue with the same "
                                    "players?. Press y if you want to, "
                                    "or n if you want to start a new game",
                                    " is not a valid input. Please press y to "
                                    "continue with the same players or n to "
                                    "start a new game")
            if result == 'y':
                self.play()
            else:
                self.__init__()
                self.play()
        else:
            self.exit_game()

    @staticmethod
    def exit_game():
        """
        This is a static function to exit the game and get the terminal to
        its empty initial state.
        :return: None
        """
        clear_screen()
        print("Hope to see you again soon! Thanks for playing 😊")
        time.sleep(1.5)
        clear_screen()

    def prompt_num_players(self):
        """
        This function prompts the user to add additional human and computer
        players to the game. Measures are also taken to handle improper input values
        :return: None
        """
        print(f"There are currently {self.humans} human player(s) and"
              f" {self.bots} computer player(s)")
        result = validate_input(['y', 'n'],
                                f"Do you want to add more human players? "
                                "Please press y to add, and n to skip",
                                " is not a valid input. Please press y to "
                                f"add a new human player or n to skip")
        if result == 'y':
            num_players = input("Please type in the number of players "
                                "you'd want to add and press enter key: \n")
            while True:
                try:
                    isinstance(int(num_players), int)
                    num_players = int(num_players)
                    clear_prev_lines(2)
                    time.sleep(0.5)
                    break
                except ValueError:
                    clear_prev_lines(2)
                    time.sleep(0.5)
                    num_players = input(
                        f"{num_players} is not a valid integer."
                        f" Please enter a valid integer.\n")
            self.humans += num_players
            time.sleep(1)

        result = validate_input(['y', 'n'],
                                f"Do you want to add more computer players? "
                                "Please press y to add, and n to skip",
                                " is not a valid input. Please press y to "
                                f"add a new computer player or n to skip")
        if result == 'y':
            num_players = input("Please type in the number of players "
                                "you'd want to add and press enter key: \n")
            while True:
                try:
                    isinstance(int(num_players), int)
                    num_players = int(num_players)
                    clear_prev_lines(2)
                    time.sleep(0.5)
                    break
                except ValueError:
                    clear_prev_lines(2)
                    time.sleep(0.5)
                    num_players = input(
                        f"{num_players} is not a valid integer."
                        f" Please enter a valid integer.\n")
            self.bots += num_players
            time.sleep(1)
        clear_prev_lines(1)


if __name__ == "__main__":
    g = Game()
    g.play()
