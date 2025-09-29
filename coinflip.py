#!/usr/bin/env python3
"""
Coin Flip Simulator
A simple command-line coin flip betting game.
Starting balance: $10,000
"""

import random
import sys
from typing import Dict


class CoinFlipGame:
    """Coin flip betting game."""
    
    def __init__(self, starting_balance: int = 10000):
        self.balance = starting_balance
        self.stats = {
            'total_flips': 0,
            'wins': 0,
            'losses': 0,
            'current_streak': 0,
            'longest_win_streak': 0,
            'longest_loss_streak': 0,
            'heads_flipped': 0,
            'tails_flipped': 0
        }
    
    def flip_coin(self) -> str:
        """Flip a coin and return 'Heads' or 'Tails'."""
        result = random.choice(['Heads', 'Tails'])
        self.stats['total_flips'] += 1
        
        if result == 'Heads':
            self.stats['heads_flipped'] += 1
        else:
            self.stats['tails_flipped'] += 1
        
        return result
    
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
    
    def get_prediction(self) -> str:
        """Get player's prediction (Heads or Tails)."""
        while True:
            choice = input("Choose Heads (h) or Tails (t): ").lower().strip()
            if choice == 'h':
                return 'Heads'
            elif choice == 't':
                return 'Tails'
            else:
                print("Invalid choice! Enter 'h' for Heads or 't' for Tails.")
    
    def update_stats(self, won: bool):
        """Update game statistics."""
        if won:
            self.stats['wins'] += 1
            if self.stats['current_streak'] >= 0:
                self.stats['current_streak'] += 1
            else:
                self.stats['current_streak'] = 1
            self.stats['longest_win_streak'] = max(
                self.stats['longest_win_streak'], 
                self.stats['current_streak']
            )
        else:
            self.stats['losses'] += 1
            if self.stats['current_streak'] <= 0:
                self.stats['current_streak'] -= 1
            else:
                self.stats['current_streak'] = -1
            self.stats['longest_loss_streak'] = max(
                self.stats['longest_loss_streak'], 
                abs(self.stats['current_streak'])
            )
    
    def display_stats(self):
        """Display current game statistics."""
        print("\n" + "="*40)
        print("GAME STATISTICS")
        print("="*40)
        print(f"Total flips: {self.stats['total_flips']}")
        print(f"Wins: {self.stats['wins']}")
        print(f"Losses: {self.stats['losses']}")
        
        if self.stats['total_flips'] > 0:
            win_rate = (self.stats['wins'] / self.stats['total_flips']) * 100
            print(f"Win rate: {win_rate:.1f}%")
        
        if self.stats['current_streak'] > 0:
            print(f"Current streak: {self.stats['current_streak']} wins")
        elif self.stats['current_streak'] < 0:
            print(f"Current streak: {abs(self.stats['current_streak'])} losses")
        else:
            print("Current streak: None")
        
        print(f"Longest win streak: {self.stats['longest_win_streak']}")
        print(f"Longest loss streak: {self.stats['longest_loss_streak']}")
        print(f"Heads flipped: {self.stats['heads_flipped']}")
        print(f"Tails flipped: {self.stats['tails_flipped']}")
        print("="*40)
    
    def play_round(self):
        """Play one round of coin flip."""
        print("\n" + "="*30)
        print("COIN FLIP ROUND")
        print("="*30)
        
        # Get bet and prediction
        bet = self.get_bet_amount()
        prediction = self.get_prediction()
        
        print(f"\nYou bet ${bet:,} on {prediction}")
        print("Flipping the coin...")
        
        # Flip the coin
        result = self.flip_coin()
        print(f"🎯 The coin landed on: {result}")
        
        # Check if player won
        won = (prediction == result)
        
        if won:
            print("🎉 You win!")
            self.balance += bet
            print(f"You won ${bet:,}")
        else:
            print("😞 You lose!")
            self.balance -= bet
            print(f"You lost ${bet:,}")
        
        # Update statistics
        self.update_stats(won)
        
        print(f"Your new balance: ${self.balance:,}")
    
    def play_game(self):
        """Main game loop."""
        print("🪙 Welcome to Coin Flip Simulator! 🪙")
        print(f"Starting balance: ${self.balance:,}")
        print("Bet on Heads or Tails - even money payout!")
        
        while self.balance > 0:
            print("\nOptions:")
            print("1. Flip coin")
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
    """Main function to start the coin flip game."""
    try:
        game = CoinFlipGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
