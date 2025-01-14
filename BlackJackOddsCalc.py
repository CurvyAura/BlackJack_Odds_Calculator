"""
Created by Brett S (CurvyAura) on 2025-01-13.

This program calculates the best move for the player to win a game of Blackjack based on the player's hand and the dealer's face-up card,
using a somewhat simplified version of the basic Blackjack strategy chart to determine the best move for the player.
"""

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [(rank, suit) for rank in RANKS for suit in SUITS]

# Function to get card input from user
def get_card_input(prompt):
    while True:
        card = input(prompt).strip().split()
        if len(card) == 2 and card[0] in RANKS and card[1] in SUITS:
            return (card[0], card[1])
        else:
            print("Invalid card. Please enter in the format 'Rank Suit' (e.g., '10 Hearts').")

def get_initial_hands():
    player_hand = [get_card_input("Enter your first card (Rank Suit): "), get_card_input("Enter your second card (Rank Suit): ")]
    dealer_hand = [get_card_input("Enter dealer's face-up card (Rank Suit): "), None]
    return player_hand, dealer_hand

def determine_hand_value(hand):
    """Calculate the total value of a Blackjack hand."""
    value = 0
    aces = 0

    for card in hand:
        rank = card[0]  # Extract the rank from the card tuple
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            aces += 1
            value += 1  # Add 1 for now; we'll adjust for soft hands later
        else:
            value += int(rank)  # Convert numeric ranks to integers

    # Adjust for aces (count some as 11 if it doesn't cause a bust)
    while aces > 0 and value + 10 <= 21:
        value += 10
        aces -= 1

    return value

def calc_player_move(player_hand, dealer_hand):
    """Determine the best move based on Blackjack strategy chart."""
    dealer_upcard = dealer_hand[0][0]  # Extract the rank of the dealer's upcard
    if dealer_upcard in ['J', 'Q', 'K']:
        dealer_upcard = 10
    elif dealer_upcard == 'A':
        dealer_upcard = 11
    else:
        dealer_upcard = int(dealer_upcard)  # Convert numeric ranks to an integer

    # Handle pairs
    if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0]:
        pair_value = player_hand[0][0]
        if pair_value in ['J', 'Q', 'K']:
            pair_value = 10
        elif pair_value == 'A':
            pair_value = 11
        else:
            pair_value = int(pair_value)  # Convert numeric ranks to an integer
        return handle_pair(pair_value, dealer_upcard)
    
    # Calculate player hand value
    player_value = determine_hand_value(player_hand)

    # Handle soft hands
    if 'A' in [card[0] for card in player_hand] and player_value < 21:
        return handle_soft_hand(player_hand, dealer_upcard)
    
    # Handle hard hands
    return handle_hard_hand(player_value, dealer_upcard)

def handle_hard_hand(player_value, dealer_upcard):
    """Determine the move for a hard hand."""
    if player_value >= 17:
        return 'stand'
    elif 13 <= player_value <= 16 and dealer_upcard in [2, 3, 4, 5, 6]:
        return 'stand'
    elif 12 == player_value and dealer_upcard in [4, 5, 6]:
        return 'stand'
    elif player_value == 11:
        return 'double down'
    elif player_value == 10 and dealer_upcard < 10:
        return 'double down'
    elif player_value == 9 and dealer_upcard in [3, 4, 5, 6]:
        return 'double down'
    else:
        return 'hit'

def handle_soft_hand(player_hand, dealer_upcard):
    """Determine the move for a soft hand."""
    player_value = determine_hand_value(player_hand)

    if player_value >= 19:
        return 'stand'
    elif player_value == 18:
        if dealer_upcard in [9, 10, 'A']:
            return 'hit'
        elif dealer_upcard in [2, 7, 8]:
            return 'stand'
        else:
            return 'double down'
    elif player_value == 17 and dealer_upcard in [3, 4, 5, 6]:
        return 'double down'
    elif player_value == 13 and dealer_upcard in [2, 3, 4, 5, 6]:
        return 'hit'  # Soft 13 case, no double down for dealer showing 4
    elif player_value == 14 and dealer_upcard in [2, 3, 4, 5, 6]:
        return 'hit'  # Soft 14 case, no double down for dealer showing 4
    else:
        return 'hit'

def handle_pair(pair_value, dealer_upcard):
    """Determine the move for a pair."""
    if pair_value in [8, 11]:  # Handle Aces (11) and 8s (always split)
        return 'split'
    elif pair_value == 10:  # Tens (never split)
        return 'stand'
    elif pair_value == 9:  # Nines
        if dealer_upcard in [2, 3, 4, 5, 6, 8, 9]:
            return 'split'
        else:  # Dealer has 7, 10, or Ace
            return 'stand'
    elif pair_value == 7 and dealer_upcard in [2, 3, 4, 5, 6, 7]:
        return 'split'
    elif pair_value == 6 and dealer_upcard in [2, 3, 4, 5, 6]:
        return 'split'
    elif pair_value == 5:  # Special handling for 5s
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9]:  # Double down if not 10 or Ace
            return 'double down'
        else:  # Hit against 10 or Ace
            return 'hit'
    elif pair_value == 4 and dealer_upcard in [5, 6]:
        return 'split'
    elif pair_value == 3 and dealer_upcard in [2, 3, 4, 5, 6, 7]:
        return 'split'
    elif pair_value == 2 and dealer_upcard in [2, 3, 4, 5, 6, 7]:
        return 'split'
    else:
        return 'hit'

def main():
    while True:
        player_hand, dealer_hand = get_initial_hands()
        print(f'Player hand: {player_hand}')
        print(f"Dealer's face-up card: {dealer_hand[0]}")
        
        player_value = determine_hand_value(player_hand)
        print("Player's hand value: ", player_value)

        # Get and print the suggested move
        suggested_move = calc_player_move(player_hand, dealer_hand)
        print(f"Suggested move: {suggested_move}")

        # Ask if the user wants to run again
        run_again = input("Do you want to run again? (y/n): ").strip().lower()
        if run_again != 'y':
            break

    # Wait for user input before closing
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()