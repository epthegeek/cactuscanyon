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
##
## This mode keeps track of the awards and points for making the right ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import dmd
import ep

class RightRamp(ep.EP_Mode):
    """Cactus Canyon Right Ramp Mode"""
    def __init__(self, game, priority):
        super(RightRamp, self).__init__(game, priority)
        self.myID = "Right Ramp"
        # Set up the sounds

    def mode_started(self):
        self.game.lamp_control.right_ramp()

    def mode_stopped(self):
        self.game.lamp_control.right_ramp('Disable')

    def sw_rightRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_rightRampEnter)
        # score the arbitrary and wacky points
        self.game.score(2530,bonus=True)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampEnter"

    def sw_rightRampMake_active(self,sw):
        # if we're tilted, ignore this switch:
        if self.game.show_tracking('tiltStatus') >= self.game.tilt_warnings:
            pass
        else:
            # the actual game doesn't care if enter was just hit
            # so I don't either
            # tick one on to the total of player shots on the right ramp
            self.game.increase_tracking('rightRampShots')

            # if a polly mode is running - let it go man
            if self.game.peril or self.game.showdown.running or self.game.ambush.running:
                if self.game.combos.chain > 1:
                    self.game.combos.mini_display()
            else:
                self.award_ramp_score(self.game.combos.comboStatus)

            ## -- set the last switch hit --
            ep.last_switch = "rightRampMake"
            ep.last_shot = "right"


    def sw_rightRampBottom_active(self,sw):
        self.game.score(2530,bonus=True)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampBottom"
        # if we're in a combo - play a noise on the bottom switch
        if self.game.combos.chain > 1:
            self.game.sound.play(self.game.assets.sfx_ricochetSet)

    def award_ramp_score(self,combo):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        stage = self.game.show_tracking('rightRampStage')
        if stage == 1:
            if combo:
                self.game.combos.mini_display()
            ## set the text lines for the display later
            self.awardString = "SOUND ALARM"
            self.awardPoints = str(ep.format_score(125000))
            self.game.score(125000,bonus=True)
            # load the animation
            anim = self.game.assets.dmd_bankExplodes
            # calcuate the wait time to start the next part of the display
            myWait = len(anim.frames) / 8.57
            # play the first sound
            self.game.sound.play(self.game.assets.sfx_explosion1)
            self.game.base.play_quote(self.game.assets.quote_rightRamp1)
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7
            animLayer.opaque = True

            # added a frame listener for the second sound effect
            animLayer.add_frame_listener(5, self.game.sound.play,param=self.game.assets.sfx_fallAndCrash1)
            # play the animation
            self.layer = animLayer
            # add some score
            # apply the calculated delay to the next step
            self.delay(name="Display",delay=myWait,handler=self.blink_award_text)
        elif stage == 2:
            if combo:
                self.game.combos.mini_display()
            # set the text lines for the display
            self.awardString = "SHOOT OUT"
            self.awardPoints = str(ep.format_score(150000))
            self.game.score(150000,bonus=True)
            # load the animation
            anim = self.game.assets.dmd_bankSheriff
            # calculate the wait time
            myWait = len(anim.frames) / 8.57
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7
            animLayer.opaque = True

            # add listener frames
            animLayer.add_frame_listener(15,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(17,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(19,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            # play the start sound
            self.game.base.play_quote(self.game.assets.quote_rightRamp2)
            # play the animation
            self.layer = animLayer
            # apply the delay
            self.delay(name="Display",delay=myWait,handler=self.blink_award_text)

        elif stage == 3:
            if combo:
                self.game.combos.mini_display()
        # if move your train is running, don't start save polly
            if self.game.move_your_train.running or \
                self.game.drunk_multiball.running:
                self.game.score(50000,bonus=True)
                return
            else:
                self.game.increase_tracking('rightRampStage')
                ## New logic branch - if this is the last item for stamepede, go straight there instead of polly
                ## *IF* we're on ball 3, *AND* player has no extra balls.
                if self.game.ball == self.game.balls_per_game and self.game.show_tracking('extraBallsTotal') == 0 \
                    and self.game.show_tracking('leftRampStage') == 5 \
                    and self.game.show_tracking('centerRampStage') == 5:
                    # increase the tracking again to "finish" the ramp
                    self.game.increase_tracking('rightRampStage')
                    # bump up the stampede score by 100k
                    self.game.increase_tracking('Stampede Value',100000)
                    # Then check stampede
                    self.game.base.check_stampede()
                else:
                    self.game.modes.add(self.game.bank_robbery)
                    self.game.bank_robbery.start_bank_robbery()


    ## for now, anything above 3 is 'complete'
        else:
            # vary the prize based on win/lose
            if self.game.bank_robbery.won:
                self.awardString = "ROBBERY FOILED"
                self.game.base.play_quote(self.game.assets.quote_victory)
                value = self.game.increase_tracking('rightRampValue',5000)
                frame = 0
            else:
                self.awardString = "BANK ROBBED"
                value = self.game.increase_tracking('rightRampValue',500)
                frame = 13
            self.awardPoints = str(ep.format_score(value))
            self.game.score(value,bonus=True)
            # play sounds
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            # play animation
            if combo:
                self.layer = None
                self.game.combos.display()
            else:
                self.anim_bank_visit(frame)

        # then tick the stage up for next time unless it's completed
        if self.game.show_tracking('rightRampStage') < 3:
            self.game.increase_tracking('rightRampStage')
            # do a little lamp flourish
            if not self.game.lamp_control.lights_out:
                self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
                self.game.lamps.rightRampShootOut.schedule(0x0FF00FF0)
                self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
            # update the lamps
            self.delay(delay=1,handler=self.lamp_update)

    def anim_bank_victory(self):
        if self.game.bank_robbery.won:
            #print "BANK VICTORY"
            self.game.sound.play(self.game.assets.sfx_grinDing)
            victoryLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_pollyVictory.frames[12])
            self.layer = victoryLayer
        else:
            backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_poutySheriff.frames[0])
            textLine1 = ep.EP_TextLayer(25,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("YOU",color=ep.RED)
            textLine2 = ep.EP_TextLayer(98,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("LOST!",color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
            self.layer = combined
            self.game.sound.play(self.game.assets.sfx_glumRiffShort)

        self.delay(name="Display",delay=1,handler=self.blink_award_text)

    def anim_bank_visit(self,frame):
        backdrop = dmd.FrameLayer(frame=self.game.assets.dmd_bankExplodes.frames[frame])
        self.layer = backdrop
        self.delay(delay=2,handler=self.blink_award_text)

    def blink_award_text(self):
        # stage one of showing the award text - this one blinks
        self.build_award_text(12)
        # switch to solid in 1 seconds
        self.delay(name="Display",delay=1,handler=self.show_award_text)

    def show_award_text(self):
        # stage 2 of showing the award text
        self.build_award_text()
        # turn it off in 1 seconds
        self.delay(name="Display",delay=1,handler=self.clear_layer)
        # show combo display if the chain is high enough
        if self.game.combos.chain > 1:
            self.delay(name="Display",delay=1,handler=self.game.combos.display)

    def build_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = ep.EP_TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ_outline,justify="center",opaque=False)
        awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az_outline,justify="center",opaque=False)
        awardTextBottom.composite_op = "blacksrc"
        awardTextTop.composite_op = "blacksrc"

        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=12,color=ep.DARK_GREEN)
            awardTextBottom.set_text(self.awardPoints,blink_frames=12,color=ep.GREEN)
        else:
            awardTextTop.set_text(self.awardString,color=ep.DARK_GREEN)
            awardTextBottom.set_text(self.awardPoints,color=ep.GREEN)
            #awardTextmask.set_text(self.awardPoints)
        # combine them
        if self.layer == None:
            self.layer = self.no_layer()

        completeFrame = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # swap in the new layer
        self.layer = completeFrame

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
