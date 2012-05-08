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
        # this would have to turn on some lights and stuff
        pass

    def sw_leftRampEnter_active(self,sw):
        # hitting this switch counts as a made ramp - really
        # tick one onto the total of ramp shots
        self.game.increase_tracking('leftRampShots')
        # score the points
        self.award_ramp_score()

    def sw_leftRampMake_active(self,sw):
        # in general gameplay this switch has no purpose
        # but I'm sure it adds points
        self.game.score(2530)

    def award_ramp_score(self):
        # cancel the "Clear" delay if there is one
        self.cancel_delayed("ClearLeftRamp")

        ##
        ## For now, all the river runs use the same animation so it's in here
        ## would be nice to come up with additional animations - but making them good enough? fuggedaboutit
        ##
        # load the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'river-chase.dmd')
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the river ramp sound
        self.game.sound.play(self.game.assets.sfx_leftRampEnter)
        # set the animation
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # run the animation
        self.layer = animLayer

        ## ramp award is determined by stage - starts at 1
        ## completed is CURRENTLY 4 - to reset the awards
        ## reset the leftRampStage
        stage = self.game.show_tracking('leftRampStage')
        if stage == 1:
            self.awardString = "WHITE WATER"
            self.awardPoints = "125,000"
            self.game.score(125000)
            self.game.sound.play_voice(self.game.assets.quote_leftRamp1)
            self.delay(delay=myWait,handler=self.show_award_text)
        elif stage == 2:
            self.awardString = "WATER FALL"
            self.awardPoints = "150,000"
            self.game.score(150000)
            self.game.sound.play_voice(self.game.assets.quote_leftRamp2)
            self.delay(delay=myWait,handler=self.show_award_text)
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
            self.delay(delay=myWait,handler=self.anim_river_victory)
        else:
            self.awardString = "ADVENTURE COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(150000)
            # play sounds
            # play the river ramp sound
            self.game.sound.play_voice(self.game.assets.quote_victory)
            # play animation
            self.anim_river_victory()

    # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('leftRampStage')

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
        self.delay(delay=myWait,handler=self.show_award_text)

    def push_out(self):
        print "TRANSITION MF"
        blank = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'blank.dmd').frames[0])
        blank.composite_op = "blacksrc"
        transition = ep.EP_Transition(self,self.layer,blank,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_WEST)
        transition.callback = self.clear_layer

    def clear_layer(self):
        print "I GOT A CALL BACK"
        self.layer = None
