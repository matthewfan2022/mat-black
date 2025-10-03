#!/usr/bin/env python3
"""
Tic Tac Toe Game
A command-line tic-tac-toe betting game against AI.
Starting balance: $10,000
"""

import random
import sys
from typing import List, Optional, Tuple


class TicTacToeGame:
    """Tic Tac Toe betting game against AI."""
    
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
            'total_moves': 0,
            'games_won_in_moves': {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0},
            'games_lost_in_moves': {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
        }
        self.board = [' ' for _ in range(16)]  # 4x4 board
        self.player_symbol = 'X'
        self.ai_symbol = 'O'
        self.current_player = 'player'  # 'player' or 'ai'
        self.move_count = 0
    
    def display_board(self):
        """Display the current game board."""
        print("\n" + "="*33)
        print("TIC TAC TOE BOARD (4x4)")
        print("="*33)
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} | {self.board[3]} ")
        print("---+---+---+---")
        print(f" {self.board[4]} | {self.board[5]} | {self.board[6]} | {self.board[7]} ")
        print("---+---+---+---")
        print(f" {self.board[8]} | {self.board[9]} | {self.board[10]} | {self.board[11]} ")
        print("---+---+---+---")
        print(f" {self.board[12]} | {self.board[13]} | {self.board[14]} | {self.board[15]} ")
        print("\nPosition numbers:")
        print(" 1 | 2 | 3 | 4 ")
        print("---+---+---+---")
        print(" 5 | 6 | 7 | 8 ")
        print("---+---+---+---")
        print(" 9 |10 |11 |12 ")
        print("---+---+---+---")
        print("13 |14 |15 |16 ")
        print("="*33)
    
    def reset_board(self):
        """Reset the board for a new game."""
        self.board = [' ' for _ in range(16)]  # 4x4 board
        self.current_player = 'player'
        self.move_count = 0
    
    def is_valid_move(self, position: int) -> bool:
        """Check if a move is valid."""
        return 1 <= position <= 16 and self.board[position - 1] == ' '
    
    def make_move(self, position: int, symbol: str) -> bool:
        """Make a move on the board."""
        if self.is_valid_move(position):
            self.board[position - 1] = symbol
            self.move_count += 1
            self.stats['total_moves'] += 1
            return True
        return False
    
    def check_winner(self) -> Optional[str]:
        """Check if there's a winner. Returns 'X', 'O', 'tie', or None."""
        # Check rows (4 in a row)
        for i in range(0, 16, 4):
            if (self.board[i] == self.board[i+1] == self.board[i+2] == self.board[i+3] != ' '):
                return self.board[i]
        
        # Check columns (4 in a column)
        for i in range(4):
            if (self.board[i] == self.board[i+4] == self.board[i+8] == self.board[i+12] != ' '):
                return self.board[i]
        
        # Check main diagonal (top-left to bottom-right)
        if (self.board[0] == self.board[5] == self.board[10] == self.board[15] != ' '):
            return self.board[0]
        
        # Check anti-diagonal (top-right to bottom-left)
        if (self.board[3] == self.board[6] == self.board[9] == self.board[12] != ' '):
            return self.board[3]
        
        # Check for tie
        if self.move_count == 16:
            return 'tie'
        
        return None
    
    def get_ai_move(self) -> int:
        """Get AI's move using a simple strategy."""
        # First, check if AI can win
        for i in range(16):
            if self.board[i] == ' ':
                self.board[i] = self.ai_symbol
                if self.check_winner() == self.ai_symbol:
                    self.board[i] = ' '  # Undo the move
                    return i + 1
                self.board[i] = ' '  # Undo the move
        
        # Then, check if AI needs to block player
        for i in range(16):
            if self.board[i] == ' ':
                self.board[i] = self.player_symbol
                if self.check_winner() == self.player_symbol:
                    self.board[i] = ' '  # Undo the move
                    return i + 1
                self.board[i] = ' '  # Undo the move
        
        # If center positions are available, take them (positions 6, 7, 10, 11)
        center_positions = [6, 7, 10, 11]
        available_centers = [pos for pos in center_positions if self.board[pos-1] == ' ']
        if available_centers:
            return random.choice(available_centers)
        
        # Take corners (positions 1, 4, 13, 16)
        corners = [1, 4, 13, 16]
        available_corners = [pos for pos in corners if self.board[pos-1] == ' ']
        if available_corners:
            return random.choice(available_corners)
        
        # Take any available position
        available_positions = [i+1 for i in range(16) if self.board[i] == ' ']
        return random.choice(available_positions)
    
    def get_player_move(self) -> int:
        """Get player's move."""
        while True:
            try:
                position = int(input(f"Enter position (1-16) for your {self.player_symbol}: "))
                if self.is_valid_move(position):
                    return position
                else:
                    print("Invalid move! Position is either taken or out of range.")
            except ValueError:
                print("Please enter a valid number (1-16).")
    
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
            # Track games won in specific number of moves
            if self.move_count in self.stats['games_won_in_moves']:
                self.stats['games_won_in_moves'][self.move_count] += 1
        elif result == 'ai':
            self.stats['losses'] += 1
            if self.stats['current_streak'] <= 0:
                self.stats['current_streak'] -= 1
            else:
                self.stats['current_streak'] = -1
            self.stats['longest_loss_streak'] = max(
                self.stats['longest_loss_streak'], 
                abs(self.stats['current_streak'])
            )
            # Track games lost in specific number of moves
            if self.move_count in self.stats['games_lost_in_moves']:
                self.stats['games_lost_in_moves'][self.move_count] += 1
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
        
        if self.stats['total_games'] > 0:
            avg_moves = self.stats['total_moves'] / self.stats['total_games']
            print(f"Average moves per game: {avg_moves:.1f}")
        
        print("\nGames won by move count:")
        for moves, count in self.stats['games_won_in_moves'].items():
            if count > 0:
                print(f"  {moves} moves: {count} games")
        
        print("\nGames lost by move count:")
        for moves, count in self.stats['games_lost_in_moves'].items():
            if count > 0:
                print(f"  {moves} moves: {count} games")
        
        print("="*50)
    
    def play_round(self):
        """Play one round of tic-tac-toe."""
        print("\n" + "="*40)
        print("TIC TAC TOE ROUND")
        print("="*40)
        
        # Get bet amount
        bet = self.get_bet_amount()
        print(f"\nYou bet ${bet:,}")
        print("You are X, AI is O. You go first!")
        
        # Reset board for new game
        self.reset_board()
        
        # Game loop
        while True:
            self.display_board()
            
            if self.current_player == 'player':
                # Player's turn
                position = self.get_player_move()
                self.make_move(position, self.player_symbol)
                self.current_player = 'ai'
            else:
                # AI's turn
                print(f"\nAI ({self.ai_symbol}) is thinking...")
                position = self.get_ai_move()
                self.make_move(position, self.ai_symbol)
                print(f"AI chose position {position}")
                self.current_player = 'player'
            
            # Check for winner
            winner = self.check_winner()
            if winner:
                self.display_board()
                break
        
        # Determine result and update balance
        if winner == self.player_symbol:
            print("🎉 You win!")
            self.balance += bet
            print(f"You won ${bet:,}")
            result = 'player'
        elif winner == self.ai_symbol:
            print("😞 AI wins!")
            self.balance -= bet
            print(f"You lost ${bet:,}")
            result = 'ai'
        else:  # tie
            print("🤝 It's a tie!")
            print("Your bet is returned.")
            result = 'tie'
        
        # Update statistics
        self.update_stats(result)
        
        print(f"Your new balance: ${self.balance:,}")
    
    def play_game(self):
        """Main game loop."""
        print("❌⭕ Welcome to Tic Tac Toe! ⭕❌")
        print(f"Starting balance: ${self.balance:,}")
        print("Beat the AI to win your bet!")
        print("You are X, AI is O. You always go first.")
        
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
    """Main function to start the tic-tac-toe game."""
    try:
        game = TicTacToeGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
