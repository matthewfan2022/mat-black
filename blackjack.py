#!/usr/bin/env python3
"""
Blackjack CLI Game
A simple command-line blackjack game with betting system.
Starting balance: $10,000.00
"""

import random
import sys
from typing import List, Optional


class Card:
    """Represents a playing card."""
    
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
    def value(self) -> int:
        """Returns the blackjack value of the card."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Will be adjusted for soft/hard aces
        else:
            return int(self.rank)


class Deck:
    """Represents a deck of 52 playing cards."""
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """Reset the deck with all 52 cards."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
    
    def deal_card(self) -> Card:
        """Deal one card from the deck."""
        if not self.cards:
            self.reset()
        return self.cards.pop()


class Hand:
    """Represents a hand of cards."""
    
    def __init__(self):
        self.cards = []
    
    def add_card(self, card: Card):
        """Add a card to the hand."""
        self.cards.append(card)
    
    def get_value(self) -> int:
        """Calculate the blackjack value of the hand."""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                value += 11
            else:
                value += card.value()
        
        # Adjust for aces (convert from 11 to 1 if needed)
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self) -> bool:
        """Check if the hand is a blackjack (21 with exactly 2 cards)."""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        """Check if the hand is bust (over 21)."""
        return self.get_value() > 21
    
    def __str__(self) -> str:
        return ', '.join(str(card) for card in self.cards)


class Player:
    """Represents a player with money and betting capability."""
    
    def __init__(self, name: str, balance: int = 10000):
        self.name = name
        self.balance = balance
        self.hand = Hand()
        self.bet = 0
    
    def place_bet(self, amount: int) -> bool:
        """Place a bet. Returns True if successful, False otherwise."""
        if amount > self.balance:
            return False
        self.bet = amount
        self.balance -= amount
        return True
    
    def win_bet(self, multiplier: float = 1.0):
        """Win the bet and add winnings to balance."""
        winnings = int(self.bet * multiplier)
        self.balance += winnings + self.bet
        self.bet = 0
    
    def lose_bet(self):
        """Lose the bet."""
        self.bet = 0
    
    def reset_hand(self):
        """Reset the hand for a new round."""
        self.hand = Hand()


class BlackjackGame:
    """Main blackjack game class."""
    
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
    
    def display_hand(self, hand: Hand, hide_first: bool = False):
        """Display a hand of cards."""
        if hide_first and len(hand.cards) > 0:
            print(f"  {hand.cards[0]}")
            print("  [Hidden Card]")
        else:
            for card in hand.cards:
                print(f"  {card}")
    
    def get_bet_amount(self) -> int:
        """Get bet amount from player."""
        while True:
            try:
                print(f"\nYour balance: ${self.player.balance:,}")
                bet = int(input("Enter your bet amount: $"))
                
                if bet <= 0:
                    print("Bet must be positive!")
                    continue
                
                if bet > self.player.balance:
                    print("Insufficient funds!")
                    continue
                
                return bet
            except ValueError:
                print("Please enter a valid number!")
    
    def deal_initial_cards(self):
        """Deal initial two cards to player and dealer."""
        self.player.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())
        self.player.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())
    
    def player_turn(self) -> bool:
        """Handle player's turn. Returns True if player busts."""
        while True:
            print(f"\nYour hand: {self.player.hand}")
            print(f"Your hand value: {self.player.hand.get_value()}")
            
            if self.player.hand.is_bust():
                print("Bust! You lose!")
                return True
            
            if self.player.hand.is_blackjack():
                print("Blackjack!")
                return False
            
            choice = input("\nHit (h) or Stand (s)? ").lower().strip()
            
            if choice == 'h':
                self.player.hand.add_card(self.deck.deal_card())
                print(f"You drew: {self.player.hand.cards[-1]}")
            elif choice == 's':
                return False
            else:
                print("Invalid choice! Enter 'h' for hit or 's' for stand.")
    
    def dealer_turn(self):
        """Handle dealer's turn."""
        print(f"\nDealer's hand: {self.dealer.hand}")
        print(f"Dealer's hand value: {self.dealer.hand.get_value()}")
        
        while self.dealer.hand.get_value() < 17:
            self.dealer.hand.add_card(self.deck.deal_card())
            print(f"Dealer draws: {self.dealer.hand.cards[-1]}")
            print(f"Dealer's hand value: {self.dealer.hand.get_value()}")
    
    def determine_winner(self) -> str:
        """Determine the winner and return result."""
        player_value = self.player.hand.get_value()
        dealer_value = self.dealer.hand.get_value()
        
        if self.player.hand.is_bust():
            return "dealer"
        elif self.dealer.hand.is_bust():
            return "player"
        elif self.player.hand.is_blackjack() and not self.dealer.hand.is_blackjack():
            return "player_blackjack"
        elif self.dealer.hand.is_blackjack() and not self.player.hand.is_blackjack():
            return "dealer"
        elif player_value > dealer_value:
            return "player"
        elif dealer_value > player_value:
            return "dealer"
        else:
            return "push"
    
    def play_round(self):
        """Play one round of blackjack."""
        print("\n" + "="*50)
        print("NEW ROUND")
        print("="*50)
        
        # Reset hands
        self.player.reset_hand()
        self.dealer.reset_hand()
        
        # Get bet
        bet = self.get_bet_amount()
        self.player.place_bet(bet)
        
        # Deal initial cards
        self.deal_initial_cards()
        
        print(f"\nDealer's hand:")
        self.display_hand(self.dealer.hand, hide_first=True)
        
        print(f"\nYour hand:")
        self.display_hand(self.player.hand)
        
        # Player turn
        player_bust = self.player_turn()
        
        if not player_bust:
            # Dealer turn
            self.dealer_turn()
        
        # Determine winner
        result = self.determine_winner()
        
        # Display results and update balance
        print("\n" + "="*30)
        print("RESULTS")
        print("="*30)
        
        if result == "player_blackjack":
            print("🎉 BLACKJACK! You win 3:2!")
            self.player.win_bet(1.5)
        elif result == "player":
            print("🎉 You win!")
            self.player.win_bet(1.0)
        elif result == "dealer":
            print("😞 Dealer wins!")
            self.player.lose_bet()
        else:  # push
            print("🤝 Push! Your bet is returned.")
            self.player.balance += self.player.bet
            self.player.bet = 0
        
        print(f"Your new balance: ${self.player.balance:,}")
    
    def play_game(self):
        """Main game loop."""
        print("🎰 Welcome to Blackjack! 🎰")
        print(f"Starting balance: ${self.player.balance:,}")
        print("Dealer stands on 17, Blackjack pays 3:2")
        
        while self.player.balance > 0:
            self.play_round()
            
            if self.player.balance == 0:
                print("\n💸 You're out of money! Game over!")
                break
            
            play_again = input("\nPlay another round? (y/n): ").lower().strip()
            if play_again != 'y':
                break
        
        print(f"\nThanks for playing! Final balance: ${self.player.balance:,}")


def main():
    """Main function to start the game."""
    try:
        game = BlackjackGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
