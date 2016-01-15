'''
@author: henryre
'''

import deck
from rtbplayer import RTBPlayer as RTBP

import matplotlib as mpl
from matplotlib import pyplot as plt

class RTBGame:
    # Initialize game with player and empty deck/board    
    def __init__(self, player):
        self.__player = player
        self.__deck = None
        self.__board = None
    # Helper method to discard and replace card
    def __discard(self, rd):
        c = self.__board[rd-1]
        self.__player.sees(c)
        self.__board[rd-1] = self.__deck.draw()
        return c
    # Play game and return number of drinks taken and rounds played
    def play_game(self):
        self.__player.forget()
        self.__deck = deck.Deck(True)
        self.__board = [self.__deck.draw() for _ in xrange(4)]
        ndrinks, nrounds = 0, 0
        while not self.__deck.is_empty():
            nrounds += 1
            # Play first round
            g1 = self.__player.guess_1()
            c1 = self.__discard(1)
            if g1 != c1.is_black():
                ndrinks += 2
                continue
            # Play second round
            g2 = self.__player.guess_2(c1)
            c2 = self.__discard(2)
            if (g2 and (c2 < c1)) or ((not g2) and (c1 < c2)):
                ndrinks += 4
                continue
            # Play third round
            g3 = self.__player.guess_3(c1, c2)
            c3 = self.__discard(3)
            (lo, hi) = (c1, c2) if (c1 < c2) else (c2, c1)
            if ((g3 and ((c3 < lo) or (c3 > hi))) or
                ((not g3) and ((c3 > lo) and (c3 < hi)))):
                ndrinks += 6
                continue
            # Play fourth round
            g4 = self.__player.guess_4()
            c4 = self.__discard(4)
            if g4 != c4.suit():
                ndrinks += 8
                continue
            else:
                break
        return ndrinks, nrounds
    # Return number of drinks taken for each of n games played
    def play_games(self, n):
        return [self.play_game()[0] for _ in xrange(n)]
        
        
def mean_along(x):
    ma = [None for _ in xrange(len(x))]
    ma[0] = float(x[0])
    for i in xrange(len(x)-1):
        ma[i+1] = float(ma[i] + x[i+1])
    for i in xrange(len(ma)):
        ma[i] /= float(i+1)
    return ma

if __name__ == '__main__':
    ng = 2500
    grid = [x+1 for x in xrange(ng)]
    skillz = [-1, 0, 0.25, 0.5, 1]
    games = {s : mean_along(RTBGame(RTBP(s)).play_games(ng)) for s in skillz}
    
    for s in skillz:
        plt.plot(grid, games[s], linewidth=2,
                 label=("{:20}{:.1f} drinks".
                        format("Skill {} player:".format(s), games[s][-1])))
    plt.axis([1, ng, 20, 80])
                        
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.xlabel("Number of games played")
    plt.ylabel("Average number of drinks")
    plt.title("Convergence of average number of drinks per game")

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 16}
    mpl.rc('font', **font)