##
## Mode for the left loop
## An always on mode, but separated for readability
##

from procgame import *
import cc_modes
import dp

class LeftLoop(game.Mode):
    """Cactus Canyon Left Loop"""
    def __init__(self, game, priority):
        super(LeftLoop, self).__init__(game, priority)
        # set up the animations they are to alternate
        self.anims = []
        anim1 = self.game.assets.anim_horseDrag
        self.anims.append({'layer':anim1,'direction':dp.DP_Transition.PARAM_WEST})
        anim2 = self.game.assets.anim_horseChase
        self.anims.append({'layer':anim2,'direction':dp.DP_Transition.PARAM_EAST})

    def mode_started(self):
    # this would have to turn on some lights and stuff
        pass

    def sw_leftLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
        # score come points
        self.game.score(2530)

    def sw_leftLoopTop_active(self,sw):
        # top end of the loop
        # award the loop reward
        self.award_loop_score()

    def award_loop_score(self):
        # if we're on stage one
        stage = self.game.show_tracking('leftLoopStage')
        if stage == 1:
            self.awardString = "BUCK N BRONCO"
            self.awardPoints = "125,000"
            self.game.score(125000)
            self.game.sound.play(self.game.assets.quote_prospectorGottaHurt)
        elif stage == 2:
            self.awardString = "WILD RIDE"
            self.awardPoints = "150,000"
            self.game.score(15000)
            # play the sound
            self.game.sound.play(self.game.assets.sfx_horseYell)
        elif stage == 3:
            self.awardString = "RIDE EM COWBOY"
            self.awardPoints = "175,000"
            self.game.score(175000)
            self.game.sound.play(self.game.assets.quote_mayorFineRideSir)
        # anything 4 or more is complete
        else:
            self.awardString = "BRONCO LOOPS COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(15000)

        # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('leftLoopStage')

        # load the animation based on which was last played
        anim = dmd.Animation().load(self.anims[0]['layer'])
        # then flip it for next time
        self.anims.reverse()

        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0 - .5
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        # run the animation
        self.layer = animLayer
        # then at the delay show the award
        self.delay(delay=myWait,handler=self.show_award_text)

    def show_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=True)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=blink,seconds=1)
            awardTextBottom.set_text(self.awardPoints,blink_frames=blink,seconds=1)
        else:
            awardTextTop.set_text(self.awardString)
            awardTextBottom.set_text(self.awardPoints)
            # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # swap in the new layer
        #self.layer = completeFrame
        myDirection = self.anims[1]['direction']
        self.transition = dp.DP_Transition(self,self.layer,completeFrame,dp.DP_Transition.TYPE_SLIDEOVER,myDirection)
        # clear in 2 seconds
        self.delay(delay=2,handler=self.clear_layer)

    def push_out(self):
        self.transition = dp.DP_Transition(self,self.layer,self.game.score_display.layer,dp.DP_Transition.TYPE_PUSH,self.anims[1]['direction'])
        self.transition.callback = self.clear_layer

    def clear_layer(self):
        self.layer = None
