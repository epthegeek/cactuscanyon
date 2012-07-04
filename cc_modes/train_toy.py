##
## The playfield toy train
##
from procgame import *
from assets import *
import cc_modes
import ep

class Train(game.Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Train, self).__init__(game, priority)
        self.trainProgress = 0
        self.trainReset = False

    def mode_started(self):
        # home the train
        if not self.game.switches.trainHome.is_active():
            self.reset_toy()

    def sw_trainHome_active(self,sw):
        if self.trainReset:
            self.game.coils.trainReverse.disable()
            self.trainReset = False
            self.trainProgress = 0

    def sw_trainEncoder_active(self,sw):
        # this is the moving train
        # each time it hits increment the train progress
        self.trainProgress += 1

    def sw_rightReturnLane_active(self,sw):
        self.stop()

    def move(self):
        self.game.coils.trainForward.patter(on_time=3,off_time=8)

    def stop(self):
        # turn off the moving train solenoid
        self.game.coils.trainForward.disable()

    def reset_toy(self):
        # check this again because save polly requests the reset directly
        if not self.game.switches.trainHome.is_active():
            self.game.coils.trainForward.disable()
            self.game.coils.trainReverse.enable()
            self.trainReset = True


    def progress(self):
        return self.trainProgress



