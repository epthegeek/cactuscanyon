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
        # the shots and their modes for ship mode
        self.shotModes = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.shots = ['leftLoopStage','leftRampStage','centerRampStage','rightLoopStage','rightRampStage']
        self.positions = [-58,-31,-4,23,50,77,104]
        self.direction = ["LEFT","RIGHT"]

        self.targetNames = ['Left','Left Center','Right Center','Right']
        # setup the standing aliens
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_standing_alien0.dmd')
        self.alienLayers = []
        self.alien0 = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        self.alien0.composite_op = "blacksrc"
        self.alienLayers.append(self.alien0)
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_standing_alien1.dmd')
        self.alien1 = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        self.alien1.composite_op = "blacksrc"
        self.alienLayers.append(self.alien1)
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_standing_alien2.dmd')
        self.alien2 = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        self.alien2.composite_op = "blacksrc"
        self.alienLayers.append(self.alien2)
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_standing_alien3.dmd')
        self.alien3 = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        self.alien3.composite_op = "blacksrc"
        self.alienLayers.append(self.alien3)
        # the small ship layer
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_small_ship.dmd')
        self.smallShip = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)

        ## lamps
        self.lamps = [self.game.lamps.badGuyL0,
                      self.game.lamps.badGuyL1,
                      self.game.lamps.badGuyL2,
                      self.game.lamps.badGuyL3]


    def ball_drained(self):
        # if we lose all but one the ball the mode ends
        if self.game.trough.num_balls_in_play == 1 and self.game.show_tracking('cvaStatus') == "RUNNING":
            self.cancel_delayed("Display")
            self.game.base.busy = True
            self.end_cva()


    def mode_started(self):
        # resetting defaults
        # the transitions fail if they're too close together - this is for putting a 1 second delay in between
        self.beat = 0
        # saucer postion - starts off to the right
        self.saucerX = 104
        # which shot is active
        self.activeShot = 9
        self.saucerHits = 0
        # set the mode
        self.mode = "SHIP"
        self.saucerMoving = False

        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()


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
            self.desert.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[self.desert,animLayer])
            self.layer = combined
            self.delay(delay=myWait,handler = self.get_going)

    def one_beat(self):
        self.beat += 1
        if self.beat == 1:
            self.delay(delay=1,handler=self.static_to_score)
        if self.beat == 2:
            self.delay(delay=1,handler=self.score_to_static)
        if self.beat == 3:
            self.delay(delay=1,handler=self.static_to_ship)
        if self.beat == 4:
            self.delay(delay=1,handler=self.clear_ship)
        if self.beat == 5:
            self.delay(delay=1,handler=self.intro,param=2)

    def score_to_static(self):
        self.transition = ep.EP_Transition(self,self.blankLayer,self.staticLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)

    def static_to_score(self):
        self.transition = ep.EP_Transition(self,self.staticLayer,self.blankLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)

    def clear_ship(self):
        shipLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'cva_large_ship.dmd').frames[0])
        self.transition = ep.EP_Transition(self,self.staticShip,shipLayer,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_SOUTH,callback=self.one_beat)

    def static_to_ship(self):
        # transition to the ship
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_ship_behind_static.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=False
        animLayer.repeat = True
        animLayer.frame_time = 6
        self.staticShip = animLayer
        self.transition = ep.EP_Transition(self,self.staticLayer,animLayer,ep.EP_Transition.TYPE_CROSSFADE,callback=self.one_beat)


    def get_going(self):
        # start the saucer in motion
        self.saucerMoving = True
        # first saucer stop is position 4
        self.position = 5
        self.stopAt = self.positions[self.position]
        # update the lamps
        # position the space ship
        # delay a move to the next spot
        # update the display
        self.update_display()

    def update_display(self):
        # if we're in ship mode, draw a combined layer of the ship and desert
        if self.mode == "SHIP":
            # if the saucer is moving - change it's position for the next pass if we haven't reached the target yet
            if self.saucerMoving:
                # tick over 3 spots - in the direction we're going
                if self.direction[0] == "LEFT":
                    self.saucerX -= 3
                else:
                    self.saucerX += 3
                # if we've made it to the destination spot, activate the shot
                if self.stopAt == self.saucerX:
                    # saucer is not moving
                    self.saucerMoving = False
                    # set the next position
                    if self.direction[0] == "LEFT":
                        print "MOVING LEFT"
                        self.position -= 1
                    else:
                        print "MOVING RIGHT"
                        self.position += 1
                    # activate the shot
                    # off screen to the right
                    if self.stopAt == self.positions[6]:
                        self.switch_modes("ALIEN")
                    # right ramp
                    elif self.stopAt == self.positions[5]:
                        self.activate_shot(4)
                    # right loop
                    elif self.stopAt == self.positions[4]:
                        self.activate_shot(3)
                    # center ramp
                    elif self.stopAt == self.positions[3]:
                        self.activate_shot(2)
                    # left ramp
                    elif self.stopAt == self.positions[2]:
                        self.activate_shot(1)
                    # left loop
                    elif self.stopAt == self.positions[1]:
                        self.activate_shot(0)
                    # off screen to the left
                    elif self.stopAt == self.positions[0]:
                        self.switch_modes("ALIEN")
                    else:
                        print "WAT?"

                # set the position of the ship
            self.smallShip.set_target_position(self.saucerX,0)
            # set a text line showing the current offset
            string = "STOP " + str(self.stopAt) + " POS " + str(self.position) + " X " + str(self.saucerX)
            textLayer1 = dmd.TextLayer(64, 15, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(string)
            # then build and show the layer
            combined = dmd.GroupedLayer(128,32,[self.smallShip,self.desert,textLayer1])
            self.layer = combined
        # if we're in aliens mode draw the combined aliens and desert
        # loop back in 0.1 to update the display again
        self.delay("Display",delay=0.1,handler=self.update_display)


    def activate_shot(self,shot):
        # set the active shot
        self.activeShot = shot
        # set the next stop at
        self.stopAt = self.positions[self.position]
        # update the lamps
        for mode in self.shotModes:
            mode.update_lamps()
        # start a timer to move the ship again
        self.ship_timer(4)

    def ship_timer(self,time):
        # a simple countdown loop to move the ship
        time -= 1
        if time == 0:
            self.saucerMoving = True
        else:
            self.delay("Saucer Timer",delay=1,handler=self.ship_timer,param=time)


    def switch_modes(self,mode):
        # switching to alien mode
        if mode == "ALIEN":
            self.mode = "ALIEN"
            # turn off the active shot
            self.activeShot = 9
            # flip the direction of the ship
            self.direction.reverse()
            # set the starting position of the ship
            if self.direction[0] == "LEFT":
                self.position = 6
                self.saucerX = self.positions[self.position]
                self.position -= 1
                self.stopAt = self.positions[self.position]
            else:
                self.position = 0
                self.saucerX = self.positions[self.position]
                self.position += 1
                self.stopAt = self.positions[self.position]
            ## TEMPORARY LOOP
            self.switch_modes("SHIP")
        if mode == "SHIP":
            # change the mode type
            self.mode = "SHIP"
            # set the ship in motion
            self.saucerMoving = True