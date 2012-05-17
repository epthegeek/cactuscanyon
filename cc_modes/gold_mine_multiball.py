##
## The Gold Mine Multiball
##

from procgame import *
import cc_modes
import ep
import random

class GoldMine(game.Mode):
    """Mining for great justice - For the Gold Mine Multiball, and ... ? """
    def __init__(self,game,priority):
        super(GoldMine, self).__init__(game,priority)


    def start_multiball(self):
        # for now we'll just print a thing
        print "MULTIBALL STARTING"
        # and then end
        self.end_multiball()

    def intro_animation(self):
        pass

    def end_multiball(self):
        # set the status to open
        self.game.set_tracking('mineStatus','OPEN')
        print "MULTIBALL ENDED"
        # unload the mode
        self.game.modes.remove(self.game.gm_multiball)

