##
## The playfield toy mountain
##
from procgame import *
from assets import *
import cc_modes
import ep

class Mountain(game.Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Mountain, self).__init__(game, priority)
        self.mineReset = False
        self.inMotion = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            self.stop()

    def mode_started(self):
        # home the train
        if not self.game.switches.mineHome.is_active():
            self.reset_toy()

    def ball_drained(self):
        # if the ball drains, turn off the mine
        self.game.coils.mineMotor.disable()
        self.game.coils.mineFlasher.disable()

    def sw_mineHome_active(self,sw):
        # if the switch is active and we're supposed to be resetting, then stop here
        if self.mineReset:
            self.game.coils.mineMotor.disable()
            self.mineReset = False
            self.inMotion = False

    def kick(self):
        self.game.coils.minePopper.pulse(20)

    def flash(self):
        self.game.coils.mineFlasher.pulse(30)

    def eject(self):
        # flash the light and then kick out
        self.flash()
        self.delay(delay=0.03,handler=self.kick)

    def stop(self):
        self.game.coils.mineMotor.disable()
        self.inMotion = False

    def twitch(self):
        # if the mine is already running for some reason, don't do the pulse
        if not self.inMotion:
            self.game.coils.mineMotor.pulse(255)

    def run(self):
        self.game.coils.mineMotor.enable()
        self.inMotion = True

    def reset_toy(self):
        if not self.game.switches.mineHome.is_active():
            self.game.coils.mineMotor.enable()
            self.mineReset = True
            self.inMotion = True
