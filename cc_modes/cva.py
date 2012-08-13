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
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]

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
        if self.game.trough.num_balls_in_play == 1 or self.game.trough_num_balls_in_play:
            if self.game.show_tracking('cvaStatus') == "RUNNING":
                self.cancel_delayed("Display")
                self.game.base.busy = True
                self.end_cva()


    def mode_started(self):
        # set the stack level
        self.game.set_tracking('stackLevel',True,3)

        # resetting defaults
        # the transitions fail if they're too close together - this is for putting a 1 second delay in between
        self.beat = 0
        # saucer postion - starts off to the right
        self.saucerX = 104
        self.teleportX = 0
        # which shot is active
        self.activeShot = 9
        self.saucerHits = 0
        self.aliensKilled = 0
        self.aliensKilledRound = 0
        # set the mode
        self.mode = "SHIP"
        self.saucerMoving = False
        # starting saucer value
        self.saucerValue = 1000000
        self.saucerIncrement = 250000
        # starting alien value
        self.alienValue = 50000
        self.alienIncrement = 5000
        self.activeAliens = []
        self.teleporting = False
        self.teleportingAliens = []
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

    def update_mode_lamps(self):
        # update the lamps
        for mode in self.shotModes:
            mode.update_lamps()

    ### Jackpot switches

    def sw_leftLoopTop_active(self,sw):
        # pulse the coil to open the gate
        self.game.coils.rightLoopGate.pulse(240)

        self.process_shot(0,self.activeShot)
        ## -- set the last switch hit --
        ep.last_switch = "leftLoopTop"

        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot(1,self.activeShot)
        ## -- set the last switch hit --
        ep.last_switch = "leftRampEnter"

        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot(2,self.activeShot)
        ## -- set the last switch hit --
        ep.last_switch = "centerRampMake"

        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            # pulse the coil to open the gate
            self.game.coils.leftLoopGate.pulse(240)

            self.process_shot(3,self.activeShot)
            ## -- set the last switch hit --
            ep.last_switch = "rightLoopTop"

        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4,self.activeShot)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampMake"

        return game.SwitchStop

    # decide if this was a jackpot hit or a miss
    def process_shot(self,number,active):
        if active == number:
            # turn off moving, just in case
            self.saucerMoving = False
            # null the active shot
            self.activeShot = 9
            # update the lamps to turn them off
            self.update_mode_lamps()
            # count the hit
            self.saucerHits += 1
            # cancel the move timer
            self.cancel_delayed("Sacuer Timer")
            # cancel the display loop
            self.cancel_delayed("Display")
            # score the value
            points = self.point_value("SAUCER")
            self.game.score(points)
            # register the saucer hit
            self.saucer_hit_display()

    # Other switches
    # Ramp/Loop Entrances
    def sw_leftLoopBottom_active(self,sw):
        # play the sound effect if we're not coming from the top switch
        if ep.last_switch != 'leftLoopTop' and ep.last_switch != 'leftLoopBottom':
            stage = self.game.show_tracking('leftLoopStage')
            if stage != 4:
                self.game.sound.play(self.game.assets.sfx_cvsWoosh)
            # score come points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "leftLoopBottom"
        return game.SwitchStop

    def sw_centerRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_cvaWoosh)
        # score the arbitrary and wacky points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "centerRampEnter"
        return game.SwitchStop

    def sw_rightLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect if we're not coming from the top
        if ep.last_switch != 'rightLoopTop' and ep.last_switch != 'rightLoopBottom':
            stage = self.game.show_tracking('rightLoopStage')
            if stage != 4:
                # while working on completing, the sound plays
                self.game.sound.play(self.game.assets.sfx_cvaWoosh)
            # score come points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightLoopBottom"
        return game.SwitchStop

    def sw_rightRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_cvaWoosh)
        # score the arbitrary and wacky points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampEnter"
        return game.SwitchStop
    # quickdraws

    def sw_topLeftStandUp_active(self, sw):
        self.quickdraw_hit('TOP',0)
        ## -- set the last switch hit --
        ep.last_switch = "topLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None
        return game.SwitchStop

    def sw_bottomLeftStandUp_active(self,sw):
        self.quickdraw_hit('BOT',0)
        ## -- set the last switch hit --
        ep.last_switch = "bottomLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None
        return game.SwitchStop

    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('TOP',1)
        ## -- set the last switch hit --
        ep.last_switch = "topRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None
        return game.SwitchStop

    def sw_bottomRightStandUp_active(self,sw):
        self.quickdraw_hit('BOT',1)
        ## -- set the last switch hit --
        ep.last_switch = "bottomRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None
        return game.SwitchStop

    def quickdraw_hit(self,position,side):
        pass

    # beer mug
    def sw_beerMug_active(self,sw):
        self.game.score_with_bonus(2130)
        # play a sound
        #self.game.sound.play(self.game.assets.sfx_ricochetSet)
        ## -- set the last switch -- ##
        ep.last_switch = 'beerMug'
        ## kill the combo shot chain
        return game.SwitchStop

    # the mine
    def sw_minePopper_active_for_390ms(self,sw):
        self.game.score_with_bonus(2530)
        # kick the ball
        self.game.mountain.eject()
        return game.SwitchStop

    # the saloon
    def sw_saloonPopper_active_for_290ms(self,sw):
        self.game.score_with_bonus(2530)
        return game.SwitchStop

    def sw_saloonBart_active(self,sw):
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "saloonBart"
        return game.SwitchStop

    def sw_saloonGate_active(self,sw):
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "saloonGate"
        return game.SwitchStop

    def sw_jetBumpersExit_active(self,sw):
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "jetBumpersExit"
        return game.SwitchStop


    def intro(self,step=1,entry="inlane",onSide = 0):
        if step == 1:
            # trap the ball if needed
            if entry == "inlane":
                self.posts[onSide].patter(on_time=2,off_time=6,original_on_time=30)
            # then save the entry method and side for later
            self.entry = entry
            self.side = onSide
            # start the music
            self.game.sound.stop_music()
            # intro section
            duration = self.game.sound.play(self.game.assets.music_cvaIntro)
            # main loop
            self.delay(delay=duration,handler=self.game.base.music_on,param=self.game.assets.music_cvaLoop)
            self.delay(delay=duration,handler=self.gi_bloom,param=duration)
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
            # blink/kill the GI
            self.gi_flutter()

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
            self.game.gi_control("ON")
            self.delay(delay=1,handler=self.static_to_score)
        if self.beat == 2:
            self.gi_flutter()
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
        self.transition = ep.EP_Transition(self,self.staticShip,shipLayer,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_WEST,callback=self.one_beat)

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
        # set the running flag
        self.game.set_tracking("cvaStatus", "RUNNING")
        # start the saucer in motion
        self.saucerMoving = True
        # first saucer stop is position 4
        self.position = 5
        self.stopAt = self.positions[self.position]
        # update the lamps
        self.update_mode_lamps()
        # position the space ship
        # delay a move to the next spot
        # reassign the blank layer for later use
        self.blankLayer = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'blank.dmd').frames[0])
        # update the display
        self.update_display()
        # launch 2 more balls
        self.game.trough.balls_to_autoplunge = 2
        self.game.trough.launch_balls(2)
        # release the main ball
        if self.entry == "inlane":
            self.posts[self.side].disabled()
        elif self.entry == "mine":
            self.game.mountain.eject()
        elif self.entry == "saloon":
            self.game.saloon.kick()


    def update_display(self,once=False):
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLayer = dmd.TextLayer(64, 17, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=6)

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
                        return
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
                        return
                    else:
                        print "WAT?"

                # set the position of the ship
            self.smallShip.set_target_position(self.saucerX,0)
            # then build and show the layer
            combined = dmd.GroupedLayer(128,32,[self.smallShip,self.desert,scoreLayer])
            self.layer = combined
        if self.mode == "ALIEN":
            layers = []
            # blackout layer
            layers.append(self.blankLayer)
            # add the backdrop
            layers.append(self.desert)
            # and teh score
            layers.append(scoreLayer)
            # add teleporting aliens
            if self.teleporting:
                for x in self.teleportingAliens:
                    layers.append(x)
            else:
                #  add any standing aliens
                for x in self.activeAliens:
                    layers.append(self.alienLayers[x])
            combined = dmd.GroupedLayer(128,32,layers)
            self.layer = combined

        # if we're in aliens mode draw the combined aliens and desert
        # loop back in 0.1 to update the display again
        if not once:
            self.delay("Display",delay=0.1,handler=self.update_display)

    def sw_leftBonusLane_active(self,sw):
        self.teleportX += 1
        self.update_display()
        return game.SwitchStop

    def sw_rightBonusLane_active(self,sw):
        self.teleportX -= 1
        self.update_display()
        return game.SwitchStop


    def activate_shot(self,shot):
        # set the active shot
        self.activeShot = shot
        # set the next stop at
        self.stopAt = self.positions[self.position]
        # update the lamps
        self.update_mode_lamps()
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
            # and update the lamps
            self.update_mode_lamps()
            # set up the next saucer
            self.next_saucer()
            # reset the round count of aliens
            self.aliensKilledRound = 0
            # and send 'em down TA ERF
            self.teleport_aliens(1)
        if mode == "SHIP":
            # change the mode type
            self.mode = "SHIP"
            # set the ship in motion
            self.saucerMoving = True
            self.update_display()

    def next_saucer(self,go=False):
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
        if go:
            self.saucerMoving = True

    def teleport_aliens(self,wave):
        # a bunch of  bother just to make it so that the aliens don't come up the exact same every time
        print "TELEPORT DIRECTION - " + str(self.direction[0])
        if wave == 1:
            if self.direction[0] == "LEFT":
                aliens = ["Zero","Two"]
            else:
                aliens = ["One","Three"]
        else:
            if self.direction[0] == "LEFT":
                aliens = ["One","Three"]
            else:
                aliens = ["Zero","Two"]
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_teleport.dmd')
        myWait = len(anim.frames) / 10.0
        # setup the first teleporting alien
        teleport1 = ep.EP_AnimatedLayer(anim)
        teleport1.hold=True
        teleport1.frame_time = 6
        teleport1.composite_op = "blacksrc"
        # setup the second teleporting layer
        teleport2 = ep.EP_AnimatedLayer(anim)
        teleport2.hold=True
        teleport2.frame_time = 6
        teleport2.composite_op = "blacksrc"
        # adjust their positions
        if aliens[0] == "Zero":
            print "ALIEN 0 - " + str(aliens[0])
            teleport1.set_target_position(-4,0)
        else:
            print "ALIEN 0 - " + str(aliens[0])
            teleport1.set_target_position(28,0)
        if aliens[1] == "Two":
            teleport2.set_target_position(60,0)
        else:
            teleport2.set_target_position(92,0)
        # add them to the list
        self.teleportingAliens.append(teleport1)
        self.teleportingAliens.append(teleport2)
        # turn on the display flag
        self.teleporting = True
        # update the display
        self.update_display()
        self.game.sound.play(self.game.assets.sfx_cvaTeleport)
        # delay the actual activation of the targets
        self.delay(delay=myWait,handler=self.activate_aliens,param=aliens)

    def activate_aliens(self,aliens):
        # cancel the display delay
        self.cancel_delayed("Display")
        # remove the teleporting aliens
        self.teleportingAliens = []
        # raise the targets
        for target in aliens:
            if target == "Zero":
                target = 0
            elif target == "One":
                target = 1
            elif target == "Two":
                target = 2
            else:
                target = 3
            self.activeAliens.append(target)
            self.game.bad_guys.target_up(target)
        # turn off the teleporting flag
        self.teleporting = False
        # update the bad guy lamps
        self.game.bad_guys.update_lamps()
        self.update_display()

    def hit_alien(self,target):
        # flasher flourish
        self.game.base.red_flasher_flourish()
        # cancel the display
        self.cancel_delayed("Display")
        # remove the dead alien
        print "REMOVE ALIEN - " + str(target)
        self.activeAliens.remove(target)
        # count the kill
        self.aliensKilled += 1
        # and count it for the round
        self.aliensKilledRound += 1
        # do the display of the dying
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_shot.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        animLayer.composite_op = "blacksrc"
        myString = self.point_value("ALIEN")
        self.game.score(myString)
        titleLayer = dmd.TextLayer(64, 4, self.game.assets.font_7px_az, "center", opaque=False).set_text("ALIEN KILLED")
        scoreLayer = ep.pulse_text(self,64,14,ep.format_score(myString),align="center",myOpaque=True,size="12px",timing=0.1)
        combined = dmd.GroupedLayer(128,32,[scoreLayer,titleLayer,animLayer])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_cvaGroan)
        # delay the normal display and next saucer
        theDelay = myWait + 1.5
        # if all 4 are dead, we change modes to the ship
        if self.aliensKilledRound == 4:
            self.delay(delay=theDelay,handler=self.switch_modes,param="SHIP")
        elif self.aliensKilledRound == 2:
            print "WAVE 2 NOW"
            self.delay(delay=theDelay,handler=self.teleport_aliens,param=2)
        else:
            self.delay("Display",delay=theDelay,handler=self.update_display)


    def point_value(self,type):
        if type == "SAUCER":
            points = self.saucerValue
            # first saucer is worth the base, every additional adds some
            for i in range(1,self.saucerHits,1):
                points += self.saucerIncrement
        else:
            points = self.alienValue
            for i in range(1,self.aliensKilled,1):
                points += self.alienIncrement
        return points

    def saucer_hit_display(self):
        # lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.game.update_lamps)
        anim = dmd.Animation().load(ep.DMD_PATH+'cva_large_ship_explodes.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        animLayer.composite_op = "blacksrc"
        myString = self.point_value("SAUCER")
        titleLayer = dmd.TextLayer(64, 4, self.game.assets.font_7px_az, "center", opaque=False).set_text("SAUCER DESTROYED")
        scoreLayer = ep.pulse_text(self,64,14,ep.format_score(myString),align="center",myOpaque=True,size="12px",timing=0.1)
        combined = dmd.GroupedLayer(128,32,[scoreLayer,titleLayer,animLayer])
        self.layer = combined
        # play the boom
        self.game.sound.play(self.game.assets.sfx_cvaExplosion)
        # delay the normal display and next saucer
        theDelay = myWait + 1.5
        self.delay(delay=theDelay+0.1,handler=self.update_display)
        self.delay(delay=theDelay,handler=self.next_saucer,param=True)

    def end_cva(self):
        # stop the music
        self.game.sound.stop_music()
        # do the final display
        # ship frame and alien frame
        shipBorder = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'cva-ships-border.dmd').frames[0])
        alienBorder = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'cva-aliens-border.dmd').frames[0])
        # blank script
        script = []
        # math out the ship points total
        shipPoints = 0
        for i in range(0,self.saucerHits,1):
            # one mill per saucer
            shipPoints += 1000000
            # 250,000 bonus boost per saucer starting with 2
            shipPoints += 250000 * (i - 1)
        # math out the alien points total
        alienPoints = 0
        for i in range(0,self.aliensKilled,1):
            # 50,000 per alien
            alienPoints += 50000
            # 5000 point boost per alien starting with 2
            alienPoints += 5000 * (i -1)
        # set the saucer title line
        if self.saucerHits == 1:
            textString = "1 SAUCER DESTROYED"
        else:
            textString = str(self.saucerHits) + " SAUCERS DESTROYED"
        titleLayer = dmd.TextLayer(64, 4, self.game.assets.font_7px_az, "center", opaque=False)
        titleLayer.set_text(textString)
        # set the saucer score line
        scoreLayer = ep.pulse_text(self,64,14,ep.format_score(shipPoints),align="center",myOpaque=True,size="12px",timing=0.1)
        # build the layer
        page = dmd.GroupedLayer(128,32,[shipBorder,titleLayer,scoreLayer])
        # add it to the script
        script.append({'layer':page,'seconds':1.5})
        # set the aliens title line
        if self.aliensKilled == 0:
            textString = "1 ALIEN KILLED"
        else:
            textString = str(self.aliensKilled) + " ALIENS KILLED"
        titleLayer.set_text(textString)
        # set the aliens score line
        scoreLayer = ep.pulse_text(self,64,14,ep.format_score(alienPoints),align="center",myOpaque=True,size="12px",timing=0.1)
        # build the layer
        page = dmd.GroupedLayer(128,32,[alienBorder,titleLayer,scoreLayer])
        # add it to the script
        script.append({'layer':page,'seconds':1.5})
        # setup the script layer
        summary = dmd.ScriptedLayer(128,32,script)
        # and activate
        self.layer = summary
        # finish up after 3 seconds
        self.delay(delay = 3,handler=self.finish_up)

    def finish_up(self):
        # set the stack level
        self.game.set_tracking('stackLevel',False,3)
        # turn off the running flag
        self.game.set_tracking("cvaStatus","OPEN")
        # turn off the base busy
        self.game.base.busy = False
        # turn the music back on if appropriate
        # turn the music back on
        if not self.game.show_tracking('stackLevel',1) and self.game.trough.num_balls_in_play != 0:
            self.game.base.music_on(self.game.assets.music_mainTheme)

        # and then unload
        self.unload()

    def gi_flutter(self):
        self.game.gi_control("OFF")
        self.game.lamps.gi01.schedule(0x000C0F0F,cycle_seconds=1)
        self.game.lamps.gi02.schedule(0x000C0F0F,cycle_seconds=1)
        self.game.lamps.gi03.schedule(0x000C0F0F,cycle_seconds=1)

    def gi_bloom(self,duration):
        self.delay("Bloom",delay=duration,handler=self.gi_bloom,param=duration)
        self.game.lamps.gi01.schedule(0x00000FFF,cycle_seconds=1)
        self.game.lamps.gi01.schedule(0x00000FFF,cycle_seconds=1)
        self.game.lamps.gi01.schedule(0x00000FFF,cycle_seconds=1)
