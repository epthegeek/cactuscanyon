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
## A P-ROC Project by Eric Priepke, Copyright 2012-2013
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
from procgame import dmd
import ep
import random

class StampedeContinued(ep.EP_Mode):
    """Cactus Canyon Stampede"""
    def __init__(self, game, priority):
        super(StampedeContinued, self).__init__(game, priority)
        self.myID = "Stampede"
        self.shotModes = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.shots = ['leftLoopStage','leftRampStage','centerRampStage','rightLoopStage','rightRampStage']
        # set up the cows layer
        anim = self.game.assets.dmd_cowsParading
        self.cowLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        # set up the animations they are to alternate
        self.anims = []
        anim0 = self.game.assets.dmd_cowsLeft
        self.anims.append(anim0)
        anim1 = self.game.assets.dmd_cowsRight
        self.anims.append(anim1)
        self.banners = []
        banner0 = self.game.assets.dmd_stampedeBannerLeft
        self.banners.append(banner0)
        banner1 = self.game.assets.dmd_stampedeBannerRight
        self.banners.append(banner1)
        self.alternate = True

    def mode_started(self):
        # log the hit in audits
        self.game.game_data['Feature']['Stampede Started'] += 1
        # which jackpot is active
        self.active = 2
        self.jackpots = 0
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add',self.myID)
        # add the stampede value and addon to get the points for this round
        self.jackpotValue = (self.game.show_tracking('Stampede Value') * 2) + self.game.show_tracking('Stampede Addon')
        # base value
        self.baseValue = self.game.show_tracking('Stampede Value')
        # set the total to 0
        self.game.set_tracking('Stampede Total',0)
        # The first center shot is a jackpot - but it has to be able to be lowered
        self.centerValue = self.jackpotValue
        # timers for pulling the jackpot back to center
        self.longTimer = 9
        self.shortTimer = 6
        self.time = 0
        self.halted = False
        # set up some display bits
        # title line
        self.titleLine = ep.EP_TextLayer(128/2, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("STAMPEDE MULTIBALL",color=ep.PURPLE)
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.mainScoreLine = ep.EP_TextLayer(64, 7, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,color=ep.YELLOW)
        self.mainScoreLine.composite_op = "blacksrc"
        # jackpot info line
        self.jackpotLine = ep.EP_TextLayer(64,1, self.game.assets.font_5px_AZ, "center", opaque=False)

    def ball_drained(self):
    # if we're dropping down to one ball, and stampede is running - do stuff
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('centerRampStage') == 89:
            self.game.base.busy = True
            self.game.base.queued += 1
            self.end_stampede()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        active = self.active
        self.process_shot(0,active)

    def sw_leftRampEnter_active(self, sw):
        active = self.active
        self.process_shot(1,active)

    def sw_centerRampMake_active(self, sw):
        active = self.active
        self.process_shot(2,active)

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            active = self.active
            self.process_shot(3,active)

    def sw_rightRampMake_active(self, sw):
        active = self.active
        self.process_shot(4,active)

   # bonus lanes pause timer
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    # bumpers also
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    # so does the mine and saloon
    def sw_minePopper_active_for_390ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_active_for_290ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.resume()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            self.resume()


    def start_stampede(self):
        # reset the jackpot count, just in case
        self.jackpots = 0
        # set the stack layer
        self.game.stack_level(4,True)
        self.running = True
        # stop the current music
        self.stop_music()
        # set the ramp status for lights -- outdated lamp_control doesn't use
        for shot in self.shots:
            #print "SETTING TRACKING FOR:" + shot
            self.game.set_tracking(shot,89)
        # udpate the lamps
        self.lamp_update()
        # If the multiball ball savers are a thing, do that
        self.game.base.multiball_saver()

        #play the opening anim
        anim = self.game.assets.dmd_stampede
        myWait = len(anim.frames) / 10 + 1.5
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # toss to the main display after the animation
        self.delay(name="Display",delay=myWait,handler=self.main_display)
        # play a quote
        self.game.base.priority_quote(self.game.assets.quote_stampedeStart)
        # start the music for stampede - delay this music start in case a quickdraw started at the same time
        self.delay(delay=1.5,handler=self.music_on,param=self.game.assets.music_stampede)
        # launch some more balls
        if self.game.trough.num_balls_in_play < 4:
            total = 4 - self.game.trough.num_balls_in_play
            # turn on autoplunge
            self.game.trough.balls_to_autoplunge = total
            # launch whatever it takes to get to 3 balls
            self.game.trough.launch_balls(total)

    def main_display(self):
        # this is the main score display for stampede - it's got score on it, so we'll have to loop
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.mainScoreLine.set_text(scoreString,color=ep.YELLOW)
        # jackpot info line
        # Center shot
        if self.active == 2:
            string = "JACKPOT = " + ep.format_score(self.centerValue)
            self.jackpotLine.set_text(string,color=ep.PURPLE)
        # One off center is 2x
        if self.active == 1 or self.active == 3:
            string = "JACKPOT = 2 X " + ep.format_score(self.jackpotValue)
            self.jackpotLine.set_text(string,color=ep.PURPLE)
        # two off center is 4x
        if self.active == 0 or self.active == 4:
            string = "JACKPOT = 4 X " + ep.format_score(self.jackpotValue)
            self.jackpotLine.set_text(string,color=ep.PURPLE,blink_frames=4)
        # group with cow layer
        combined = dmd.GroupedLayer(128,32,[self.cowLayer,self.mainScoreLine,self.jackpotLine])
        # set the layer active
        self.layer = combined
        # loop back again in .2 for score update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    # decide if this was a jackpot hit or a miss
    def process_shot(self,number,active):
         # cancel the display if any
        self.cancel_delayed("Display")
        # we hit the active shot
        if active == number:
            self.jackpots += 1
            # if it's the middle shot, it's 1x
            if active == 2:
                self.scored = self.centerValue
                # then set it to the base value for a second score
                self.centerValue = self.baseValue
            # if it's one off center, it's 2x
            if self.is_near():
                self.scored = self.jackpotValue * 2
            # if it's the far side shots, it's 4x
            if self.is_far():
                self.scored = self.jackpotValue * 4
            # then move the jackpot back to center
            if self.active != 2:
                self.active = 2
            # score the points
            self.game.score(self.scored)
            # update the lamps
            self.lamp_update()
            # add the points to the tracking
            self.game.increase_tracking('Stampede Total',self.scored)
            # and display the hit
            self.jackpot_hit()
        # if the number is higher than the active, move right
        elif number > active:
            self.game.score(self.baseValue)
            self.shift(1)
        # the other option is if it's lower, we move left
        else:
            self.game.score(self.baseValue)
            self.shift(0)

    def jackpot_hit(self,step=1):
        if step == 1:
        # log the hit in audits
            self.game.game_data['Feature']['Stampede Jackpots'] += 1

            # play an animation
            anim = self.game.assets.dmd_stampedeJackpot
            myWait = len(anim.frames) / 15.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=4)
            self.layer = animLayer
            self.game.base.play_quote(self.game.assets.quote_jackpot)
            # and some sounds
            self.game.sound.play(self.game.assets.sfx_revRicochet)
            # loop back to do the next part
            self.delay(name="Display",delay=myWait+0.5,handler=self.jackpot_hit,param=2)
        # second pass layers the score over the text
        if step == 2:
            self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_stampedeJackpot.frames[42])
            self.scoreLine = ep.EP_TextLayer(64, 8, self.game.assets.font_17px_score, "center", opaque=True).set_text(str(ep.format_score(self.scored)),color=ep.YELLOW)
#            self.scoreLine.composite_op = "blacksrc"
#            self.layer = dmd.GroupedLayer(128,32,[self.backdrop,self.scoreLine])
            # loop back to cleear
            # transition to the score
            transition = ep.EP_Transition(self,self.backdrop,self.scoreLine,ep.EP_Transition.TYPE_CROSSFADE)
            self.delay(name="Display",delay=2,handler=self.jackpot_hit,param=3)
        # third pass plays the wipe
        if step == 3:
            anim = self.game.assets.dmd_burstWipe
            myWait = len(anim.frames) / 15.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 4
            animLayer.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[self.backdrop,self.scoreLine,animLayer])
            # play a sound on delay
            self.delay(name="Display",delay=myWait,handler=self.game.sound.play,param=self.game.assets.sfx_explosion1)
            # then do the main display
            self.delay(name="Display",delay=myWait,handler=self.main_display)

    def shift(self,direction):
        # move the active shot
        # Going right
        if direction == 1:
            self.active += 1
            # just in case
            if self.active > 4:
                self.active = 4
        # going Left
        else:
            self.active -= 1
            # just in case
            if self.active < 0:
                self.active = 0

        # update the lamps
        self.lamp_update()
        # now we need to start a timer for pulling back to center
        # If we're in the One away, set the long timer
        if self.is_near():
            self.time = self.longTimer + 1
            self.shift_timer()
        # If we're two away, set the short timer
        if self.is_far():
            self.time = self.shortTimer + 1
            self.shift_timer()

        layerCopy = self.layer
        # Set the cow animation
        anim = self.anims[direction]
        banner = self.banners[direction]
        myWait = len(banner.frames) / 12.0
        # play an animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=5)
        animLayer.composite_op = "blacksrc"
        bannerLayer = dmd.AnimatedLayer(frames=banner.frames,hold=True, opaque=False,repeat=False,frame_time=5)
        textLayer = ep.EP_TextLayer(64,13,self.game.assets.font_13px_score,"center",opaque=False)
        textLayer.composite_op = "blacksrc"
        # frame listener to set the text on the score display
        animLayer.add_frame_listener(19, lambda: textLayer.set_text(ep.format_score(self.baseValue),color=ep.MAGENTA,blink_frames=8))
        #bannerLayer.composite_op = "blacksrc"
        if layerCopy:
            combined = dmd.GroupedLayer(128,32,[layerCopy,bannerLayer,textLayer,animLayer])
        else:
            combined = dmd.GroupedLayer(128,32,[bannerLayer,textLayer,animLayer])
        combined.composite_op = "blacksrc"
        self.layer = combined
        # and some sounds
        self.game.sound.play(self.game.assets.sfx_flyByNoise)
        self.delay(delay=1,handler=self.game.base.play_quote,param=self.game.assets.quote_stampedeWiff)
        self.delay(name="Display", delay=myWait, handler=self.main_display)

    def jackpot_shift(self):
        # if off to the right, pull back by one
        if self.active > 2:
            self.active -= 1
        # if off to the left, pull back by one
        elif self.active < 2:
            self.active += 1
        # if we're already in the middle, do nothing
        else:
            pass
        #print "Shifting - active jackpot is now " + str(self.active)
        # update the lamps
        self.lamp_update()

    def shift_timer(self):
        # cancel any other shift timer
        self.cancel_delayed("Shift Timer")
        # decrement by one
        self.time -= 1
        # are we out of time?
        if self.time <= 0:
            self.jackpot_shift()
        # if not, loop back in one second
        else:
            self.delay(name="Shift Timer", delay=1,handler=self.shift_timer)

    def halt(self):
        # stop the timer
        self.cancel_delayed("Shift Timer")
        self.halted = True

    def resume(self):
        self.halted = False
        # resume counting after 1 second
        if self.time > 0:
            self.delay("Shift Timer",delay = 1,handler = self.shift_timer)

    def end_stampede(self):
        #print "ENDING S T A M P E D E"
        # stop the music
        #self.stop_music(slice=5)
        # do a final display
        # setup a display frame
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_skullsBorder.frames[0])
        textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "STAMPEDE TOTAL"
        textLine1.set_text(textString)
        textLine1.composite_op = "blacksrc"
        textLine2 = dmd.TextLayer(128/2,11, self.game.assets.font_12px_az, "center", opaque=False)
        totalPoints = self.game.show_tracking('Stampede Total')
        textLine2.set_text(ep.format_score(totalPoints))
        # if the total is higher than best, set best
        if self.game.show_tracking('Stampede Best') < totalPoints:
            self.game.set_tracking('Stampede Best',totalPoints)
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
        self.layer = combined
        self.delay(name="Display",delay=2,handler=self.clear_layer)

        # set the active jackpot out of range
        self.active = 9
        # kill the timer loop that moves the jackpot
        self.cancel_delayed("Timer")
        # set some tracking?
        # reset the ramp status
        for each in self.shots:
            self.game.set_tracking(each,1)
        # set the values for the ramp shots back down
        self.game.set_tracking('leftRampValue',2000)
        self.game.set_tracking('rightRampValue',2000)
        self.game.set_tracking('centerRampValue',2000)
        # unset the base busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # clear the stack layer - if goldmine isn't running. This covers balls draining while the gold mine starts. Rare, but possible.
        if self.game.show_tracking('mineStatus') == "RUNNING":
            #print "Goldmine is running"
            pass
        else:
            #print "Gold mine is not running"
            self.game.stack_level(4,False)
            # turn the main music back on
            self.music_on(self.game.assets.music_mainTheme,mySlice=5)
            # remove the switch blocker
            self.game.switch_blocker('remove',self.myID)
            self.lamp_update()

        # Reset the stampede value
        self.game.set_tracking('Stampede Value', 250000)
        self.game.set_tracking('Stamepde Addon', 0)
        self.running = False
        # badge light - stampede is 4
        self.game.badge.update(4)
        # unload the mode
        self.delay(delay=2,handler=self.unload)

    def tilted(self):
        if self.running:
            # reset the ramp status
            for each in self.shots:
                self.game.set_tracking(each,1)
            # badge light - stampede is 4
            self.game.badge.update(4)
        self.running = False
        self.unload()

    def abort_display(self):
        self.cancel_delayed('Display')
        self.clear_layer()

    def is_near(self):
        if self.active == 1 or self.active == 3:
            return True
        else:
            return False

    def is_far(self):
        if self.active == 0 or self.active == 4:
            return True
        else:
            return False
