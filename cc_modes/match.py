##
## The match animation routine
##

from procgame import *
from assets import *
import cc_modes
import random
import ep

class Match(game.Mode):
    """Cactus Canyon AttractMode"""
    def __init__(self, game, priority):
        super(Match, self).__init__(game, priority)

    def run_match(self):
        # pick a random number
        selection = random.choice(0,1,2,3,4,5,6,7,8,9)
        # grab the last two digits of the scores  ... somehow?
        # put up the end of the scores
        # put up the bottles
        # put up the match number
        # run the animation with sound
        # award the match if hit

        # for now just exit
        self.finish_up()

    def finish_up(self):
        # run the high score routine after the match
        self.game.run_highscore()
        # and remove thyself.
        self.game.modes.remove(self.match)