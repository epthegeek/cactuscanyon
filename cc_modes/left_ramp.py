##
## This mode keeps track of the awards and points for making the left ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes
import ep

class LeftRamp(game.Mode):
    """Cactus Canyon Right Ramp Mode"""
    def __init__(self, game, priority):
        super(LeftRamp, self).__init__(game, priority)
        # Set up the sounds
        # set up the animations
        self.game = game
        self.border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'woodcut-border.dmd').frames[0])

    def mode_started(self):
        self.update_lamps()

    def mode_stopped(self):
        self.disable_lamps()

    def update_lamps(self):
        self.disable_lamps()
        ## if status is off, we bail here
        lampStatus = self.game.show_tracking('lampStatus')
        # we bail here if the others don't match and it's not "ON"
        if lampStatus != "ON":
            return
        ## high noon check
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)
            return

        # check for goldmine multiball
        if self.game.show_tracking('mineStatus') == "RUNNING":
            if self.game.show_tracking('jackpotStatus',1):
                self.game.lamps.leftRampWhiteWater.schedule(0xFFFFF39C)
                self.game.lamps.leftRampWaterfall.schedule(0x0FFFF39C)
                self.game.lamps.leftRampSavePolly.schedule(0x00FFF39C)
                self.game.lamps.leftRampJackpot.schedule(0x000FF39C)
            return

        stage = self.game.show_tracking('leftRampStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
        elif stage == 2:
            # first light on
            self.game.lamps.leftRampWhiteWater.enable()
            # blink the second
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
        elif stage == 3:
            # first two on
            self.game.lamps.leftRampWhiteWater.enable()
            self.game.lamps.leftRampWaterfall.enable()
            # blink the third
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
        # this is completed - pulse the 3rd light
        elif stage == 4:
            # two on
            self.game.lamps.leftRampWhiteWater.enable()
            self.game.lamps.leftRampWaterfall.enable()
            # the pulse idea didn't really work - so we'll just turn it on
            self.game.lamps.leftRampSavePolly.enable()
        # after polly, before stampede all three stay on
        elif stage == 5:
            self.game.lamps.leftRampWhiteWater.enable()
            self.game.lamps.leftRampWaterfall.enable()
            self.game.lamps.leftRampSavePolly.enable()
        # save polly
        elif stage == 99:
            self.game.lamps.leftRampJackpot.schedule(0xFF00FF00)
            self.game.lamps.leftRampSavePolly.schedule(0x0FF00FF0)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampWhiteWater.schedule(0xF00FF00F)
        # stampede
        elif stage == 89:
        ## left ramp is #1 in the stampede jackpot list
            if self.game.stampede.active == 1 or 'leftRamp' in self.game.drunk_multiball.active:
                self.game.lamps.leftRampJackpot.schedule(0x000000FF)
                self.game.lamps.leftRampSavePolly.schedule(0x0000FFFF)
                self.game.lamps.leftRampWaterfall.schedule(0x00FFFFFF)
                self.game.lamps.leftRampWhiteWater.schedule(0xFFFFFFFF)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)

        else:
            pass

    def disable_lamps(self):
        self.game.lamps.leftRampWhiteWater.disable()
        self.game.lamps.leftRampWaterfall.disable()
        self.game.lamps.leftRampSavePolly.disable()
        self.game.lamps.leftRampJackpot.disable()

    def sw_leftRampEnter_active(self,sw):
        # hitting this switch counts as a made ramp - really
        # tick one onto the total of ramp shots
        self.game.increase_tracking('leftRampShots')
        # score the points and mess with the combo
        if self.game.comboTimer > 0:
            # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()
        # play the river ramp sound
        self.game.sound.play(self.game.assets.sfx_leftRampEnter)

        self.award_ramp_score(combo)
        ## -- set the last switch hit --
        ep.last_switch = "leftRampEnter"


    def sw_leftRampMake_active(self,sw):
        # in general gameplay this switch has no purpose
        # but I'm sure it adds points
        self.game.score(2530)
        ## -- set the last switch hit --
        ep.last_switch = "leftRampMake"


    def award_ramp_score(self, combo=False):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        ##
        ## For now, all the river runs use the same animation so it's in here
        ## would be nice to come up with additional animations - but making them good enough? fuggedaboutit
        ##
        # set the animation

        ## ramp award is determined by stage - starts at 1
        ## completed is CURRENTLY 4 - to reset the awards
        ## reset the leftRampStage
        stage = self.game.show_tracking('leftRampStage')
        if stage == 1:
            self.awardString = "WHITE WATER"
            self.awardPoints = "125,000"
            self.game.score(125000)
            self.game.sound.play_voice(self.game.assets.quote_leftRamp1)
            # load the 2 animations
            anim1 = dmd.Animation().load(ep.DMD_PATH+'blank-river.dmd')
            anim2 = dmd.Animation().load(ep.DMD_PATH+'rowboat.dmd')
            # set up the layers
            animLayer1 = dmd.AnimatedLayer(frames=anim1.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            animLayer2 = dmd.AnimatedLayer(frames=anim2.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            # layer 2 needs transparent
            animLayer2.composite_op = "blacksrc"
            # math out the wait
            myWait = len(anim1.frames) / 10.0
            # combine the 2 layers
            animLayer = dmd.GroupedLayer(128,32,[animLayer1,animLayer2])
            # turn it on
            self.layer = animLayer
            # set a delay to show the award
            self.delay(name="Display",delay=myWait,handler=self.show_award_text)
        elif stage == 2:
            self.awardString = "WATER FALL"
            self.awardPoints = "150,000"
            self.game.score(150000)
            self.game.sound.play_voice(self.game.assets.quote_leftRamp2)
            # load the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'river-chase.dmd')
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            # turn it on
            self.layer = animLayer
            # set the delay for the award
            self.delay(name="Display",delay=myWait,handler=self.show_award_text)

        elif stage == 3:
            self.awardString = "ADVENTURE COMPLETE"
            self.awardPoints = "175,000"
            self.game.score(175000)
            anim = dmd.Animation().load(ep.DMD_PATH+'sheriff-pan.dmd')
            # waith for the pan up to finish
            myWait = 1.14
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)
            # play sounds
            # play the river ramp sound
            self.game.sound.play(self.game.assets.sfx_leftRampEnter)
            self.game.sound.play(self.game.assets.quote_pollyThankYou)
            # play animation
            self.layer = animLayer
            self.delay(name="Display",delay=myWait,handler=self.anim_river_victory)
        else:
            self.awardString = "ADVENTURE COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(150000)
            # play sounds
            # play the river ramp sound
            self.game.sound.play_voice(self.game.assets.quote_victory)
            # play animation if we're not in a combo after level 4
            if combo:
                self.layer = None
                self.game.combos.display()
            else:
                self.anim_river_victory()

        # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('leftRampStage')
            # update the lamps
            self.update_lamps()

    # for now since this doesn't blink there's just one step
    def show_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=12)
            awardTextBottom.set_text(self.awardPoints,blink_frames=12)
        else:
            awardTextTop.set_text(self.awardString)
            awardTextBottom.set_text(self.awardPoints)
        # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.border,awardTextTop,awardTextBottom])
        # swap in the new layer
        #self.layer = completeFrame
        transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_WEST)
        # clear in 3 seconds
        self.delay(name="ClearLeftRamp",delay=2,handler=self.clear_layer)

    def anim_river_victory(self):
        print "RIVER VICTORY"
        anim = dmd.Animation().load(ep.DMD_PATH+'bank-victory-animation.dmd')
        myWait = len(anim.frames) / 8.57
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 7

        animLayer.add_frame_listener(7,self.game.play_remote_sound,param=self.game.assets.sfx_blow)
        animLayer.add_frame_listener(14,self.game.play_remote_sound,param=self.game.assets.sfx_grinDing)
        # play animation
        self.layer = animLayer
        self.game.sound.play(self.game.assets.sfx_leftRampEnter)
        self.delay(name="Display",delay=myWait,handler=self.show_award_text)

    def push_out(self):
        print "TRANSITION MF"
        blank = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'blank.dmd').frames[0])
        blank.composite_op = "blacksrc"
        transition = ep.EP_Transition(self,self.layer,blank,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_WEST)
        transition.callback = self.clear_layer

    def clear_layer(self):
        self.layer = None

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
