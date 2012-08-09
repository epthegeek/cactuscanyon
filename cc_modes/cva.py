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

from procgame import *
import cc_modes
import ep
import random

class CvA(ep.EP_Mode):
    """CvA code """
    def __init__(self,game,priority):
        super(CvA, self).__init__(game,priority)


    def ball_drained(self):
        # if we lose all but one the ball the mode ends
        if self.game.trough.num_balls_in_play == 1 and self.game.show_tracking('cvaStatus') == "RUNNING":
            self.cancel_delayed("Display")
            self.game.base.busy = True
            sefl.end_cva()


    def mode_started(self):
        # resetting defaults
        self.beat = 0

    def intro(self,step=1):
        if step == 1:
            # start the music
            self.game.sound.stop_music()
            # intro section
            duration = self.game.sound.play(self.game.assets.music_cvaIntro)
            # main loop
            self.delay(delay=duration,handler=self.game.base.music_on,param=self.game.assets.music_cvaLoop)
            self.delay(delay=duration,handler=self.intro,param=3)
            # load a blank frame to fade in from
            self.blankLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'blank.dmd').frames[0])
            self.blankLayer.composite_op = "blacksrc"
            # do the static display
            anim = dmd.Animation().load(ep.DMD_PATH+'cva_static.dmd')
            myWait = len(anim.frames) / 10.0
            self.staticLayer = ep.EP_AnimatedLayer(anim)
            self.staticLayer.hold=False
            self.staticLayer.repeat = True
            self.staticLayer.frame_time = 6
            self.staticLayer.composite_op = "blacksrc"
            self.layer = self.blankLayer
            # transition to static with a callback to a transition to the
            self.score_to_static()
        if step == 2:
            print "STEP 2"
            anim = dmd.Animation().load(ep.DMD_PATH+'cva_intro.dmd')
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            self.layer = animLayer
        if step == 3:
            anim = dmd.Animation().load(ep.DMD_PATH+'cva_blast_wipe.dmd')
            myWait = len(anim.frames) / 5.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 3
            animLayer.composite_op = "blacksrc"

            self.desert = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'cva_desert_empty.dmd').frames[0])
            combined = dmd.GroupedLayer(128,32,[self.desert,animLayer])
            self.layer = combined

    def one_beat(self):
        self.beat += 1
        if self.beat == 1:
            self.delay(delay=1,handler=self.static_to_score)
        if self.beat == 2:
            self.delay(delay=1,handler=self.score_to_static)
        if self.beat == 3:
            self.delay(delay=1,handler=self.static_to_ship)
        if self.beat == 4:
            self.delay(delay=1,handler=self.intro,param=2)


    def score_to_static(self):
        self.transition = ep.EP_Transition(self,self.blankLayer,self.staticLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)

    def static_to_score(self):
        self.transition = ep.EP_Transition(self,self.staticLayer,self.blankLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)

    def static_to_ship(self):
        print "STATIC TO SHIP"
        # transition to the ship
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_ship_behind_static.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=False
        animLayer.repeat = True
        animLayer.frame_time = 6

        self.transition = ep.EP_Transition(self,self.staticLayer,animLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)

