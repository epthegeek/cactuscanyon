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
## This mode keeps track of the awards and points for making the center ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import dmd
import ep

class CenterRamp(ep.EP_Mode):
    """Cactus Canyon Center Ramp Mode"""
    def __init__(self, game, priority):
        super(CenterRamp, self).__init__(game, priority)
        self.myID = "Center Ramp"
        self.border = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_tracksBorder.frames[0])

    def mode_started(self):
        self.game.lamp_control.center_ramp()

    def mode_stopped(self):
        self.game.lamp_control.center_ramp('Disable')

    def sw_centerRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_centerRampEnter)
        # score the arbitrary and wacky points
        self.game.score(2530,bonus=True)
        ## -- set the last switch hit --
        ep.last_switch = "centerRampEnter"

    def sw_centerRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('centerRampShots')

        # if a polly mode is runnning, let it go, man
        if self.game.peril or self.game.showdown.running or self.game.ambush.running:
            pass
        else:
            self.award_ramp_score(self.game.combos.comboStatus)

        ## -- set the last switch hit --
        ep.last_switch = "centerRampMake"
        ## -- set the last shot for combos
        ep.last_shot = "center"

    def award_ramp_score(self,combo):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        ## ramp award is determined by stage - starts at 1
        ## completed is CURRENTLY 4
        stage = self.game.show_tracking('centerRampStage')
        if stage == 1:
            self.awardString = "CATCH TRAIN"
            self.awardPoints = str(ep.format_score(125000))
            self.game.score(125000,bonus=True)
            self.game.base.play_quote(self.game.assets.quote_centerRamp1)
            self.game.sound.play(self.game.assets.sfx_trainChugShort)
            self.game.sound.play(self.game.assets.sfx_leftLoopEnter) # same sound used on left loop so the name is funny
            anim = self.game.assets.dmd_trainBoarding
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            # turn it on
            self.layer = animLayer
            # set the delay for the award
            self.delay("Display",delay=myWait,handler=self.show_award_text)

        elif stage == 2:
            self.train_stage_two(score=150000)

        ## stage three starts save polly peril train toy mode
        elif stage == 3:
        # if move your train is running, don't start save polly
            if self.game.move_your_train.running or \
                self.game.drunk_multiball.running:
                self.game.score(50000,bonus=True)
                return
            else:
                self.game.increase_tracking('centerRampStage')
                ## New logic branch - if this is the last item for stamepede, go straight there instead of polly
                ## *IF* we're on ball 3, *AND* player has no extra balls.
                if self.game.ball == self.game.balls_per_game and self.game.show_tracking('extraBallsTotal') == 0 \
                    and self.game.show_tracking('leftRampStage') == 5 \
                    and self.game.show_tracking('rightRampStage') == 5:
                    # increase the tracking again to "finish" the ramp
                    self.game.increase_tracking('centerRampStage')
                    # bump up the stampede score by 100k
                    self.game.increase_tracking('Stampede Value',100000)
                    # Then check stampede
                    self.game.base.check_stampede()
                else:
                    self.game.modes.add(self.game.save_polly)
                    self.game.save_polly.start_save_polly()
        # complete - after polly peril
        # after polly is saved, before high noon, show the pull brakes animation
        # and 'polly saved'
        else:
            if combo:
                self.layer = None
                self.game.combos.display()
            else:
                # if we're not in a combo we show the animation
                self.train_victory()
        # then tick the stage up for next time unless it's completed
        # we're holding at 3, save polly peril will set it to 4
        if stage < 3:
            # if we're at stage 2 and MYT is running, don't increase - stay at two
            if stage == 2 and self.game.move_your_train.running:
                pass
            else:
                self.game.increase_tracking('centerRampStage')
            if not self.game.lamp_control.lights_out:
                # do a little lamp flourish
                self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampStopTrain.schedule(0x0FF00FF0)
                self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
                self.delay(delay=1,handler=self.lamp_update)

    # for now since this doesn't blink there's just one step
    def show_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=12,color=ep.DARK_BROWN)
            awardTextBottom.set_text(self.awardPoints,blink_frames=12,color=ep.BROWN)
        else:
            awardTextTop.set_text(self.awardString,color=ep.DARK_BROWN)
            awardTextBottom.set_text(self.awardPoints,color=ep.BROWN)
            # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.border,awardTextTop,awardTextBottom])
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_gunfightFlourish) # same noise from gunfight
        # swap in the new layer
        transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        # clear in 3 seconds
        self.delay("Display",delay=2,handler=self.clear_layer)
        # show combo display if the chain is high enough
        if self.game.combos.chain > 2:
            self.delay("Display",delay=2,handler=self.game.combos.display)

    def train_stage_two(self,score):
        self.awardString = "STOP TRAIN"
        self.awardPoints = str(ep.format_score(score))
        self.game.score(score)
        self.game.base.play_quote(self.game.assets.quote_centerRamp2)
        self.game.sound.play(self.game.assets.sfx_trainChugShort)
        self.game.sound.play(self.game.assets.sfx_trainWhistle)
        anim = self.game.assets.dmd_trainRunning
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        # turn it on
        self.layer = animLayer
        # set the delay for the award
        self.delay("Display",delay=myWait,handler=self.show_award_text)

    def train_victory(self):
        start_value = self.game.increase_tracking('adventureCompleteValue',5000)
        if self.game.save_polly.won:
            self.awardString = "POLLY SAVED"
            value = start_value
            complete_color = ep.GREEN
            # play the short chug
            self.game.sound.play(self.game.assets.sfx_trainChugShort)
        else:
            self.awardString = "POLLY DIED"
            value = start_value / 10
            self.game.sound.play(self.game.assets.sfx_glumRiffShort)
            complete_color = ep.RED

        anim = self.game.assets.dmd_trainHeadOn
        trainLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=True,frame_time=6)
        textLine1 = ep.EP_TextLayer(37,1,self.game.assets.font_7px_az,justify="center",opaque=False).set_text("TIED TO",color=ep.YELLOW)
        textLine2 = ep.EP_TextLayer(37,9,self.game.assets.font_7px_az,justify="center",opaque=False).set_text("THE TRACKS",color=ep.YELLOW)
        textLine3 = ep.EP_TextLayer(37,20,self.game.assets.font_7px_az,justify="center",opaque=False).set_text("COMPLETED",color=complete_color)
        combined = dmd.GroupedLayer(128,32,[trainLayer,textLine1,textLine2,textLine3])
        self.layer = combined

        myWait = 1.5

        self.delay(name="Display",delay=myWait,handler=self.show_award_text)
        self.awardPoints = str(ep.format_score(value))
        self.game.score(value,bonus=True)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")


