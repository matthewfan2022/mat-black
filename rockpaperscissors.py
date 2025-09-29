#!/usr/bin/env python3
"""
Rock Paper Scissors Game
A command-line rock paper scissors betting game.
Starting balance: $10,000
"""

import random
import sys
from typing import Dict, Tuple


class RockPaperScissorsGame:
    """Rock Paper Scissors betting game."""
    
    def __init__(self, starting_balance: int = 10000):
        self.balance = starting_balance
        self.stats = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'ties': 0,
            'current_streak': 0,
            'longest_win_streak': 0,
            'longest_loss_streak': 0,
            'rock_chosen': 0,
            'paper_chosen': 0,
            'scissors_chosen': 0,
            'opponent_rock': 0,
            'opponent_paper': 0,
            'opponent_scissors': 0
        }
        self.choices = ['Rock', 'Paper', 'Scissors']
    
    def get_computer_choice(self) -> str:
        """Get computer's choice (random)."""
        choice = random.choice(self.choices)
        
        # Update opponent choice stats
        if choice == 'Rock':
            self.stats['opponent_rock'] += 1
        elif choice == 'Paper':
            self.stats['opponent_paper'] += 1
        else:
            self.stats['opponent_scissors'] += 1
        
        return choice
    
    def get_bet_amount(self) -> int:
        """Get bet amount from player."""
        while True:
            try:
                print(f"\nYour balance: ${self.balance:,}")
                bet = int(input("Enter your bet amount: $"))
                
                if bet <= 0:
                    print("Bet must be positive!")
                    continue
                
                if bet > self.balance:
                    print("Insufficient funds!")
                    continue
                
                return bet
            except ValueError:
                print("Please enter a valid number!")
    
    def get_player_choice(self) -> str:
        """Get player's choice."""
        while True:
            print("\nChoose your move:")
            print("1. Rock (r)")
            print("2. Paper (p)")
            print("3. Scissors (s)")
            
            choice = input("Enter your choice (1-3 or r/p/s): ").lower().strip()
            
            if choice in ['1', 'r', 'rock']:
                self.stats['rock_chosen'] += 1
                return 'Rock'
            elif choice in ['2', 'p', 'paper']:
                self.stats['paper_chosen'] += 1
                return 'Paper'
            elif choice in ['3', 's', 'scissors']:
                self.stats['scissors_chosen'] += 1
                return 'Scissors'
            else:
                print("Invalid choice! Please enter 1-3, r/p/s, or rock/paper/scissors.")
    
    def determine_winner(self, player_choice: str, computer_choice: str) -> str:
        """Determine the winner. Returns 'player', 'computer', or 'tie'."""
        if player_choice == computer_choice:
            return 'tie'
        
        # Rock beats Scissors, Paper beats Rock, Scissors beats Paper
        winning_combinations = {
            ('Rock', 'Scissors'): 'player',
            ('Paper', 'Rock'): 'player',
            ('Scissors', 'Paper'): 'player',
            ('Scissors', 'Rock'): 'computer',
            ('Rock', 'Paper'): 'computer',
            ('Paper', 'Scissors'): 'computer'
        }
        
        return winning_combinations.get((player_choice, computer_choice), 'tie')
    
    def update_stats(self, result: str):
        """Update game statistics."""
        self.stats['total_games'] += 1
        
        if result == 'player':
            self.stats['wins'] += 1
            if self.stats['current_streak'] >= 0:
                self.stats['current_streak'] += 1
            else:
                self.stats['current_streak'] = 1
            self.stats['longest_win_streak'] = max(
                self.stats['longest_win_streak'], 
                self.stats['current_streak']
            )
        elif result == 'computer':
            self.stats['losses'] += 1
            if self.stats['current_streak'] <= 0:
                self.stats['current_streak'] -= 1
            else:
                self.stats['current_streak'] = -1
            self.stats['longest_loss_streak'] = max(
                self.stats['longest_loss_streak'], 
                abs(self.stats['current_streak'])
            )
        else:  # tie
            self.stats['ties'] += 1
            self.stats['current_streak'] = 0
    
    def display_stats(self):
        """Display current game statistics."""
        print("\n" + "="*50)
        print("GAME STATISTICS")
        print("="*50)
        print(f"Total games: {self.stats['total_games']}")
        print(f"Wins: {self.stats['wins']}")
        print(f"Losses: {self.stats['losses']}")
        print(f"Ties: {self.stats['ties']}")
        
        if self.stats['total_games'] > 0:
            win_rate = (self.stats['wins'] / self.stats['total_games']) * 100
            tie_rate = (self.stats['ties'] / self.stats['total_games']) * 100
            print(f"Win rate: {win_rate:.1f}%")
            print(f"Tie rate: {tie_rate:.1f}%")
        
        if self.stats['current_streak'] > 0:
            print(f"Current streak: {self.stats['current_streak']} wins")
        elif self.stats['current_streak'] < 0:
            print(f"Current streak: {abs(self.stats['current_streak'])} losses")
        else:
            print("Current streak: None")
        
        print(f"Longest win streak: {self.stats['longest_win_streak']}")
        print(f"Longest loss streak: {self.stats['longest_loss_streak']}")
        
        print("\nYour choice frequency:")
        total_choices = self.stats['rock_chosen'] + self.stats['paper_chosen'] + self.stats['scissors_chosen']
        if total_choices > 0:
            print(f"  Rock: {self.stats['rock_chosen']} ({self.stats['rock_chosen']/total_choices*100:.1f}%)")
            print(f"  Paper: {self.stats['paper_chosen']} ({self.stats['paper_chosen']/total_choices*100:.1f}%)")
            print(f"  Scissors: {self.stats['scissors_chosen']} ({self.stats['scissors_chosen']/total_choices*100:.1f}%)")
        
        print("\nOpponent choice frequency:")
        total_opponent = self.stats['opponent_rock'] + self.stats['opponent_paper'] + self.stats['opponent_scissors']
        if total_opponent > 0:
            print(f"  Rock: {self.stats['opponent_rock']} ({self.stats['opponent_rock']/total_opponent*100:.1f}%)")
            print(f"  Paper: {self.stats['opponent_paper']} ({self.stats['opponent_paper']/total_opponent*100:.1f}%)")
            print(f"  Scissors: {self.stats['opponent_scissors']} ({self.stats['opponent_scissors']/total_opponent*100:.1f}%)")
        
        print("="*50)
    
    def play_round(self):
        """Play one round of rock paper scissors."""
        print("\n" + "="*40)
        print("ROCK PAPER SCISSORS ROUND")
        print("="*40)
        
        # Get bet and player choice
        bet = self.get_bet_amount()
        player_choice = self.get_player_choice()
        
        print(f"\nYou bet ${bet:,}")
        print("Rock... Paper... Scissors... Shoot!")
        
        # Get computer choice
        computer_choice = self.get_computer_choice()
        
        print(f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}")
        
        # Determine winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Display result and update balance
        if result == 'player':
            print("🎉 You win!")
            self.balance += bet
            print(f"You won ${bet:,}")
        elif result == 'computer':
            print("😞 You lose!")
            self.balance -= bet
            print(f"You lost ${bet:,}")
        else:  # tie
            print("🤝 It's a tie!")
            print("Your bet is returned.")
        
        # Update statistics
        self.update_stats(result)
        
        print(f"Your new balance: ${self.balance:,}")
    
    def play_game(self):
        """Main game loop."""
        print("🪨📄✂️  Welcome to Rock Paper Scissors!  ✂️📄🪨")
        print(f"Starting balance: ${self.balance:,}")
        print("Beat the computer to win your bet!")
        
        while self.balance > 0:
            print("\nOptions:")
            print("1. Play round")
            print("2. View statistics")
            print("3. Quit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.play_round()
            elif choice == '2':
                self.display_stats()
            elif choice == '3':
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        
        if self.balance == 0:
            print("\n💸 You're out of money! Game over!")
        
        print(f"\nThanks for playing! Final balance: ${self.balance:,}")
        self.display_stats()


def main():
    """Main function to start the rock paper scissors game."""
    try:
        game = RockPaperScissorsGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
