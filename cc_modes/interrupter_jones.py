##
##  The idea here is to have a really high priority layer that can but in over the top
##  of the regular display for things that are important
##

from procgame import *
from assets import *
import cc_modes
import ep

class Interrupter(game.Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Interrupter, self).__init__(game, priority)

    def display_player_number(self,idle=False):
        # for when the ball is sitting in the shooter lane with nothing going on
        myNumber = ("ONE<","TWO*","THREE<","FOUR>")
        # get the current player
        p = self.game.current_player_index
        print p
        # set up the text
        textString = "PLAYER> " + myNumber[p]
        textLayer = dmd.TextLayer(128/2, 7, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(textString)
        script = [{'seconds':0.3,'layer':textLayer},{'seconds':0.3,'layer':None}]
        display = dmd.ScriptedLayer(128,32,script)
        display.composite_op = "blacksrc"
        # turn the display on
        self.layer = display
        # todo add a quote if idle?
        self.delay(name="clearInterrupter",delay=1.5,handler=self.clear_layer)
        # with an idle call, set a repeat
        if idle:
            self.delay(name="idle",delay=10,handler=self.display_player_number,param=True)

    def abort_player_number(self):
        self.cancel_delayed("clearInterrupter")
        self.cancel_delayed("idle")
        self.layer = None

    def clear_layer(self):
        self.layer = None

    def tilt_danger(self,status):
        # if it puts us at 2, time for second warning
        if status == 2:
            print "DANGER DANGER"
            # double warning
            line1 = dmd.TextLayer(128/2, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            line2 = dmd.TextLayer(128/2, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            self.layer = dmd.GroupedLayer(128,32,[line1,line2])
            # play a sound
            myWait = self.play_tilt_sound()
            self.delay(delay=myWait,handler=self.play_tilt_sound())
            self.delay(delay=1,handler=self.clear_layer)

        # otherwise this must be the first warning
        else:
            print "DANGER"
            #add a display layer and add a delayed removal of it.
            self.layer = dmd.TextLayer(128/2, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            #play sound
            self.play_tilt_sound()
            self.delay(delay=1,handler=self.clear_layer)

    def tilt_display(self):
        # build a tilt graphic
        tiltLayer = dmd.TextLayer(128/2, 7, self.game.assets.font_20px_az, "center", opaque=True).set_text("TILT")
        # Display the tilt graphic
        self.layer = tiltLayer

    def play_tilt_sound(self):
        self.game.sound.play(self.game.assets.sfx_tiltDanger)

