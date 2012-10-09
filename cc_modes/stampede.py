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
from procgame import *
from assets import *
import cc_modes
import ep
import random

class Stampede(ep.EP_Mode):
    """Cactus Canyon Stampede"""
    def __init__(self, game, priority):
        super(Stampede, self).__init__(game, priority)
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

    def mode_started(self):
        # which jackpot is active
        self.active = 9
        self.jackpots = 0
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

    def ball_drained(self):
    # if we're dropping down to one ball, and stampede is running - do stuff
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('centerRampStage') == 89:
            self.game.base.busy = True
            self.end_stampede()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        self.process_shot(0,self.active)
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot(1,self.active)
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot(2,self.active)
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            self.process_shot(3,self.active)
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4,self.active)
        return game.SwitchStop

    def start_stampede(self):
        # reset the jackpot count, just in case
        self.jackpots = 0
        # set the stack layer
        self.game.set_tracking('stackLevel',True,1)
        # stop the current music
        self.game.sound.stop_music()
        # turn on a starting jackpot
        choices = [0,1,2,3,4]
        self.active = random.choice(choices)
        # set the ramp status for lights
        for shot in self.shots:
            print "SETTING TRACKING FOR:" + shot
            self.game.set_tracking(shot,89)
        # udpate the lamps
        for shot in self.shotModes:
            print "UPDATING LAMPS FOR STAMPEDE"
            shot.update_lamps()

        # start the timer for the moving jackpot
        self.jackpot_shift()
        #play the opening anim
        anim = self.game.assets.dmd_stampede
        myWait = len(anim.frames) / 10 + 1.5
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # toss to the main display after the animation
        self.delay(name="Display",delay=myWait,handler=self.main_display)
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_stampedeStart)
        # start the music for stampede
        self.game.base.music_on(self.game.assets.music_stampede)
        # launch some more balls
        if self.game.trough.num_balls_in_play < 3:
            total = 3 - self.game.trough.num_balls_in_play
            # turn on autoplunge
            self.game.trough.balls_to_autoplunge = total
            # launch whatever it takes to get to 3 balls
            self.game.trough.launch_balls(total)

    def main_display(self):
        # this is the main score display for stampede - it's got score on it, so we'll have to loop
        # title line
        titleLine = dmd.TextLayer(128/2, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("STAMPEDE MULTIBALL")
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(64, 7, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString)
        scoreLine.composite_op = "blacksrc"
        # group with cow layer
        combined = dmd.GroupedLayer(128,32,[self.cowLayer,titleLine,scoreLine])
        # set the layer active
        self.layer = combined
        # loop back again in .2 for score update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    # decide if this was a jackpot hit or a miss
    def process_shot(self,number,active):
         # cancel the display if any
        self.cancel_delayed("Display")
        if active == number:
            self.jackpots += 1
            self.jackpot_hit()
        else:
            self.jackpot_wiff()

    def jackpot_hit(self,step=1):
        if step == 1:
            # play an animation
            anim = self.game.assets.dmd_stampedeJackpot
            myWait = len(anim.frames) / 15.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=4)
            self.layer = animLayer
            # and some sounds
            self.game.sound.play(self.game.assets.sfx_revRicochet)
            # and award points
            self.game.score(500000)
            # loop back to do the next part
            self.delay(name="Display",delay=myWait,handler=self.jackpot_hit,param=2)
        # second pass layers the score over the text
        if step == 2:
            self.backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_stampedeJackpot.frames[42])
            self.scoreLine = dmd.TextLayer(64, 10, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("500,000")
            self.scoreLine.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[self.backdrop,self.scoreLine])
            self.game.base.play_quote(self.game.assets.quote_jackpot)
            # loop back to cleear
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

    def jackpot_wiff(self,step=1):
        if step == 1:
            # load the animation based on which was last played
            anim = self.anims[0]
            banner = self.banners[0]
            myWait = len(banner.frames) / 12.0
            # reverse them for next time
            self.anims.reverse()
            self.banners.reverse()
            # play an animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=5)
            animLayer.composite_op = "blacksrc"
            bannerLayer = dmd.AnimatedLayer(frames=banner.frames,hold=True, opaque=False,repeat=False,frame_time=5)
            bannerLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[bannerLayer,animLayer])
            combined.composite_op = "blacksrc"
            self.layer = combined
            # and some sounds
            self.game.base.play_quote(self.game.assets.quote_stampedeWiff)
            # and award points
            self.game.score(250000)
            self.delay(name="Display", delay=myWait, handler=self.main_display)

    def jackpot_shift(self):
        # bump up by one
        self.active += 1
        # then see if we went over
        if self.active >= 5:
            self.active = 0
        # update the lamps
        for shot in self.shotModes:
            shot.update_lamps()
        # then come back in 6 seconds and do it all over again
        self.delay(name="Timer",delay=6,handler=self.jackpot_shift)

    def end_stampede(self):
        print "ENDING S T A M P E D E"
        # stop the music
        self.game.sound.stop_music()
        # do a final display
        # setup a display frame
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_skullsBorder.frames[0])
        textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "STAMPEDE: " + str(self.jackpots) + " JACKPOTS"
        textLine1.set_text(textString)
        textLine1.composite_op = "blacksrc"
        textLine2 = dmd.TextLayer(128/2,11, self.game.assets.font_12px_az, "center", opaque=False)
        totalPoints = self.jackpots * 500000
        textLine2.set_text(ep.format_score(totalPoints))
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
        # and update the lamps
        for mode in self.shotModes:
            mode.update_lamps()
        # badge light - stampede is 4
        self.game.badge.update(4)
        # unset the base busy flag
        self.game.base.busy = True
        # clear the stack layer
        self.game.set_tracking('stackLevel',False,1)
        # turn the main music back on
        if self.game.trough.num_balls_in_play != 0:
            self.game.base.music_on(self.game.assets.music_mainTheme)
        # unload the mode
        self.unload()

    def abort_display(self):
        self.cancel_delayed('Display')
        self.clear_layer()
