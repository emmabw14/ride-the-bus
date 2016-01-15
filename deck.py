'''
@author: henryre
'''

# Playing card class
class Card:
    # Initialize card with number and suit, both checked for validity
    def __init__(self, num, suit):
        if not (1 <= num <= 13):
            raise ValueError("Invalid card number: {}".format(num))
        suit = suit.lower()
        if not (suit in ['spades', 'clubs', 'hearts', 'diamonds']):
            raise ValueError("Invalid card suit: {}".format(suit))
        self.__n = num
        self.__suit = suit
        self.__is_black = ((suit == 'spades') or (suit == 'clubs'))
    # Getters for number, suit, color, and black or not 
    def num(self):
        return self.__n
    def suit(self):
        return self.__suit
    def color(self):
        if self.__is_black:
            return 'black'
        else:
            return 'red'
    def is_black(self):
        return self.__is_black
    # String representation with face cards
    def __repr__(self):
        name = None
        if 2 <= self.__n <= 10:
            name = str(self.__n)
        elif self.__n == 1:
            name = 'ace'
        elif self.__n == 11:
            name = 'jack'
        elif self.__n == 12:
            name = 'queen'
        elif self.__n == 13:
            name = 'king'
        return "{} of {}".format(name, self.__suit)
    # Card-card comparator (ace low, no suit order)
    def __cmp__(self, c):
        if self.__n < c.num():
            return -1
        elif self.__n == c.num():
            return 0
        else:
            return 1

# Playing card deck class
from random import shuffle as rshuf
class Deck:
    # Initialize cards in deck, hold as list
    def __init__(self, shuf):
        self.__cards = [(n,s) for n in range(1,14)
                        for s in ['spades', 'clubs', 'hearts', 'diamonds']]
        if shuf:
            self.shuffle()
    def shuffle(self):
        rshuf(self.__cards)
    # Draw a card
    def draw(self):
        if len(self.__cards) == 0:
            return None
        return Card(*self.__cards.pop())
    # Checker for empty deck
    def is_empty(self):
        return (len(self.__cards) == 0)
    
    
    
        
    

            
