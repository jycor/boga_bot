import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def get_card(self):
        return self.value + " of " + self.suit

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

class Deck:
    def __init__(self):
        self.cards = []
        self.generate_deck()

    def generate_deck(self):
        suits = ["hearts", "diamonds", "clubs", "spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for suit in suits:
            for value in values:
                self.cards.append(Card(value, suit))
    
    def get_deck(self):
        return self.cards

    def pull_card(self):
        random_index = random.randint(0, len(self.cards) - 1)
        card = self.cards[random_index]
        self.cards.pop(random_index)
        return card


reactions = [ [":red_circle:", ":black_circle:"] ,  [":arrow_up:", ":arrow_down:"],  [":inbox_tray:", ":outbox_tray:"],  [":heart:", ":diamonds:", ":clubs:", ":spades:"]]