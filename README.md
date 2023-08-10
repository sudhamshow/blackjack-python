# Terminal-Based Blackjack

Welcome to Terminal-Based Blackjack, a unique and engaging text-based Blackjack game you can play right in your terminal. Unlike other text-based Blackjack games, this project includes human-like computer players, customizable decks, and an immersive interface to make you feel like you're right at the casino.

## Features

- **Human and Computer Players**: Play against computer players that make decisions based on real Blackjack strategies.
- **Customizable Decks**: Configure the number of decks based on the number of players.
- **Immersive Interface**: Engaging terminal output with clear instructions and updates.
- **Intuitive Code Structure**: Easy to understand code separated into relevant modules.

## Files

- [blackjack.py](blackjack.py): This is the main file that houses the Game class and controls the overall flow of the game.
- [deck.py](deck.py): Contains the Deck class, which represents a deck of cards with standard playing card functionalities.
- [player.py](player.py): Includes classes for different player types: human, computer, and dealer. Manages player actions, scores, and statuses.
- [tools.py](tools.py): Houses utility functions for user input validation, screen clearing, and other general-purpose tools.

## How to start the game
- **Clone the Repository**: `git clone https://github.com/sudhamshow/blackjack-python.git`
- **Navigate to Directory**: cd blackjack-python
- **Install Requirements (if any)**: No special requirements needed. Ensure you have python3 installed on your system.
- **Run the Game**: `python3 blackjack.py` 
- **Follow the Prompts**: The game will guide you through setting up players and starting the game.

## Demos

Dealing cards to all the players -

![Dealing 2 cards to all players including dealer](/demos/deal_cards.gif)

Game ends after all players have finished their turn -

![Declaring winner after all players have finished their turns](/demos/play.gif)


This project stands out from other text-based, terminal-based Blackjack games by providing a more realistic gaming experience through the inclusion of computer players that act like humans and an interface that keeps you engaged. The modular code design also makes it a great starting point for those looking to experiment with or learn more about programming card games.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.