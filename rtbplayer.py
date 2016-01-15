'''
@author: henryre
'''

from random import random as runif

class RTBPlayer:
    # Initialize player with skill level
    # Player keeps track of cards seen depending on skill and returns a guess
    # for each game. Skill of -1 yields completely random guesses
    def __init__(self, skill):
        if not (0 <= skill <= 1 or skill == -1):
            raise ValueError("Player skill needs to be between 0 and 1")
        self.__skill = skill
        self.__snums = [0 for i in xrange(13)]
        self.__ssuits = {s : 0 for s in 
                         ['spades', 'clubs', 'hearts', 'diamonds']}
    # Getter for skill
    def skill(self):
        return self.__skill
    # Add a card that the player has seen based on roll against skill
    def sees(self, card):
        if runif() <= self.__skill:
            self.__snums[card.num()-1] += 1
            self.__ssuits[card.suit()] += 1
    # Forget all cards seen
    def forget(self):
        self.__snums = [0 for i in xrange(13)]
        self.__ssuits = {s : 0 for s in 
                         ['spades', 'clubs', 'hearts', 'diamonds']}
    # Return a random guess ('spades' evaluates to true)
    def guess_rand(self):
        return 'spades'
    # Return a guess for game 1
    # Return true if we guess black (i.e. more reds seen than blacks)
    # Not dependent on previous games
    def guess_1(self):
        if self.__skill == -1:
            return True
        seen_black = self.__ssuits['clubs'] + self.__ssuits['spades']
        seen_red = self.__ssuits['diamonds'] + self.__ssuits['hearts']
        return (seen_black <= seen_red)
                
    # Return guess for game 2, true if guess card is higher than game 1 card
    # Player guesses by counting number of remaining cards higher and lower
    # than game 1 card
    def guess_2(self, c):
        if self.__skill == -1:
            return True
        seen_higher = sum(self.__snums[c.num():])
        nhigher = 4 * (13 - c.num()) - seen_higher
        seen_lower = sum(self.__snums[:c.num()-1])
        nlower = 4 * (c.num() - 1) - seen_lower
        return (nhigher >= nlower)
    # Return guess for game 3, true if guess card is between game 1 and 2 cards
    # Player guesses by counting number of remaining cards inside and outside
    # range of game 1 and game 2 cards
    def guess_3(self, c1, c2):
        if self.__skill == -1:
            return True
        (lo, hi) = (c1, c2) if (c1 < c2) else (c2, c1)
        seen_between = sum(self.__snums[lo.num():hi.num()-1])
        nbetween = max(0, 4 * (hi.num() - lo.num() - 1) - seen_between)
        seen_outside = (sum(self.__snums[:lo.num()-1]) +
                        sum(self.__snums[hi.num():]))
        noutside = 4 * ((lo.num() - 1) + (13 - hi.num())) - seen_outside
        return (nbetween >= noutside)
    # Return a guess for game 4, string indicating suit
    # Player guesses by counting remaining cards of each suit
    # Not dependent on previous games
    def guess_4(self):
        if self.__skill == -1:
            return 'spades'
        return min(self.__ssuits.iterkeys(), key=(lambda key: self.__ssuits[key]))
    