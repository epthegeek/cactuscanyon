##
## This mode controls the saloon
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes

class Saloon(game.Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(Saloon, self).__init__(game, priority)



    def sw_saloonPopper_closed_for_200ms(self,sw):
        print "PULSE THE KICKER FOR THE SALOON"
