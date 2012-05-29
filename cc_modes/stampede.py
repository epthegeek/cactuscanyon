from procgame import *
from assets import *
import cc_modes
import ep

class Stampede(game.Mode):
    """Cactus Canyon Stampede"""
    def __init__(self, game, priority):
        super(Stampede, self).__init__(game, priority)
        stampShots = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        # which jackpot is active
        self.active = 0

    def start_stampede(self):
        # set the stack layer
        self.game.set_tracking('stackLayer',True,2)
        #play the opening anim
        # start the music
        self.end_stampede()

    def jackpot_shift(self):
        # bump up by one
        self.active += 1
        # then see if we went over
        if self.active == 5:
            self.active = 0
        # then come back in 6 seconds and do it all over again
        self.delay(name="Timer",delay=6,handler=jackpot_shift)

    def end_stampede(self):
        # set some tracking?
        # turn the music off?
        # unload?
        # unload the mode
        self.game.modes.remove(self.game.stampede)
        # clear the stack layer
        self.game.set_tracking('stackLayer',False,2)
