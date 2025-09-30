#!/usr/bin/env python3
"""
Casino Games Menu
Choose between Blackjack, Coin Flip, Rock Paper Scissors, and Tic Tac Toe games.
"""

import sys
from blackjack import BlackjackGame
from coinflip import CoinFlipGame
from rockpaperscissors import RockPaperScissorsGame
from tictactoe import TicTacToeGame


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("🎰 WELCOME TO THE CASINO! 🎰")
    print("="*50)
    print("Choose your game:")
    print("1. Blackjack (Starting balance: $10,000)")
    print("2. Coin Flip Simulator (Starting balance: $10,000)")
    print("3. Rock Paper Scissors (Starting balance: $10,000)")
    print("4. Tic Tac Toe (Starting balance: $10,000)")
    print("5. Exit")
    print("="*50)


def main():
    """Main function to display menu and start games."""
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\nStarting Blackjack...")
                game = BlackjackGame()
                game.play_game()
            elif choice == '2':
                print("\nStarting Coin Flip Simulator...")
                game = CoinFlipGame()
                game.play_game()
            elif choice == '3':
                print("\nStarting Rock Paper Scissors...")
                game = RockPaperScissorsGame()
                game.play_game()
            elif choice == '4':
                print("\nStarting Tic Tac Toe...")
                game = TicTacToeGame()
                game.play_game()
            elif choice == '5':
                print("\nThanks for playing! Goodbye! 👋")
                break
            else:
                print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
