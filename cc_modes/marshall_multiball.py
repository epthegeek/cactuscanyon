##   ____           _                ____
##  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
## | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
## | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
##  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
##                                                   |___/
##           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
##          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
##         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
##          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
##
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The Marshall Multiball

from procgame import *
import cc_modes
import ep
import random

class MarshallMultiball(ep.EP_Mode):
    """Marshall Multiball for when player achieves maximum rank """
    def __init__(self,game,priority):
        super(MarshallMultiball, self).__init__(game,priority)
        self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_marshallBorder.frames[0])

    def mode_started(self):
        # reset the points
        self.pointTotal = 0
        self.running = True
        self.game.set_tracking('stackLevel',True,5)
        # kill the music
        self.game.sound.stop_music()
        self.game.sound.play(self.game.assets.sfx_chime3000)
        self.delay(delay=0.6,handler=self.game.sound.play,param=self.game.assets.sfx_chime3000)
        self.delay(delay=1.2,handler=self.game.sound.play,param=self.game.assets.sfx_chimeIntro)
        self.delay(delay=1.8,handler=self.start)

    def ball_drained(self):
        if self.game.trough.num_balls_in_play in (1,0) and self.running:
            self.game.base.busy = True
            self.end()

    # lamps
    def update_lamps(self):
        # first reset everything
        self.disable_lamps()
        # then turn on what's needed

    def disable_lamps(self):
    # turn off all the lights
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()

    # switches
    def sw_leftLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        self.register(100)
        return game.SwitchStop

    def sw_rightLoopTop_active(self,sw):
        self.register(100)
        return game.SwitchStop

    def sw_rightLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

        # startup
    def start(self):
        # tag this player as having run the MB so it doesn't repeat
        self.game.set_tracking('marshallMultiballRun',True)
        # play the quote
        self.game.base.priority_quote(self.game.assets.quote_marshallMultiball)
        # launch an extra ball
        if self.game.trough.num_balls_in_play < 2:
            self.game.trough.balls_to_autoplunge = 1
            self.game.trough.launch_balls(1)
        # run the display
        self.main_display()

    # display
    def main_display(self):
        scoreLayer = dmd.TextLayer(100, 17, self.game.assets.font_marshallScore, "right", opaque=False).set_text(str(self.pointTotal))

        combined = dmd.GroupedLayer(128,32,[self.backdrop,scoreLayer])
        self.layer = combined
        self.delay("Score Display",delay=0.5,handler=self.main_display)

    def register(self,value):
        if value == 10:
            self.game.sound.play(self.game.assets.sfx_chime10)
            self.score(10)
        elif value == 100:
            self.game.sound.play(self.game.assets.sfx_chime100)
            self.score(100)

    # score points
    def score(self,points):
        self.pointTotal += points


    # finish up
    def end(self):
        # store up the final score - if better than any previous run
        if self.pointTotal > self.game.show_tracking('marshallBest'):
            self.game.set_tracking('marshallBest',self.pointTotal)
        # add the final total to the player's score
        self.game.score(self.pointTotal)
        # kill the running flag
        self.running = False
        self.game.set_tracking('stackLevel',False,5)
        # unload
        self.unload()
