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
        self.inMotion = False
        self.trainReset = False

    def mode_started(self):
        # home the train
        if not self.game.switches.trainHome.is_active():
            self.reset_toy()
        self.trainProgress = 0
        self.stopAt = 0

    def sw_trainHome_active(self,sw):
        if self.trainReset:
            self.stop()
            self.trainReset = False
            self.trainProgress = 0

    def sw_trainEncoder_active(self,sw):
        # this is the moving train
        # each time it hits increment the train progress
        self.trainProgress += 1
        if self.stopAt > 0:
            if self.trainProgress >= self.stopAt:
                # reset stop at so it doesn't interfere
                self.stopAt = 0
                # reset the progress
                self.trainProgress = 0
                self.stop()

    def move(self):
        self.inMotion = True
        self.game.coils.trainForward.patter(on_time=3,off_time=8)

    def stop(self):
        # turn off the moving train solenoids
        self.game.coils.trainForward.disable()
        self.game.coils.trainReverse.disable()
        self.inMotion = False

    def fast_forward(self):
        self.inMotion = True
        self.game.coils.trainForward.enable()

    def forward(self):
        self.inMotion = True
        # TODO need to tweak this out for speed later
        self.game.coils.trainForward.patter(on_time=6,off_time=6)

    def reverse(self):
        self.inMotion = True
        # TODO need to tweak this for speed later
        self.game.coils.trainReverse.patter(on_time=6,off_time=6)

    def reset_toy(self):
        # check this again because save polly requests the reset directly
        if not self.game.switches.trainHome.is_active():
            self.game.coils.trainForward.disable()
            self.inMotion = True
            self.game.coils.trainReverse.enable()
            self.trainReset = True

    def progress(self):
        return self.trainProgress



