##
## Mode for handling the right loop
##

from procgame import *
import cc_modes
import ep

class RightLoop(game.Mode):
    """Cactus Canyon Left Loop"""
    def __init__(self, game, priority):
        super(RightLoop, self).__init__(game, priority)
        # set up a frame layer with the guns border on it
        self.border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(game.assets.dmd_path+'guns-border.dmd').frames[0])

    def mode_started(self):
        # this would have to turn on some lights and stuff
        pass

    def sw_rightLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_rightLoopEnter)
        # score come points
        self.game.score(2530)

    def sw_rightLoopTop_active(self,sw):
        # top end of the loop
        # award the loop reward
        self.award_loop_score()

    def award_loop_score(self):
            # if we're on stage one
        stage = self.game.show_tracking('rightLoopStage')
        if stage == 1:
            self.awardString = "GOOD SHOT"
            self.awardPoints = "125,000"
            self.game.score(125000)
            # load the animation
            anim = dmd.Animation().load(self.game.assets.anim_goodShot)
            # calculate a wait
            myWait = len(anim.frames) / 10.0
            # create the layer
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            animLayer.add_frame_listener(4,self.play_glass_sound_one)
            animLayer.add_frame_listener(7,self.play_glass_sound_one)
            animLayer.add_frame_listener(13,self.play_glass_sound_two)

            # put it in place
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_CROSSFADE
            self.direction = None
            # then delayed kickoff the text display
            self.delay(delay=myWait,handler=self.show_award_text)

        elif stage == 2:
            self.awardString = "GUNSLINGER"
            self.awardPoints = "150,000"
            self.game.score(15000)
            # play the animation and such
            anim = dmd.Animation().load(self.game.assets.anim_gunslinger)
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_EXPAND
            self.delay(delay=myWait,handler=self.show_award_text)
        elif stage == 3:
            self.awardString = "MARKSMAN"
            self.awardPoints = "175,000"
            self.game.score(175000)
            #self.show_award_text()
            anim = dmd.Animation().load(self.game.assets.anim_marksman1)
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=6)
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.show_marksman_award)

    # anything 4 or more is complete
        else:
            self.awardString = "SHOTS COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(15000)
            self.show_award_text()
        # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('rightLoopStage')

    def show_marksman_award(self):
        anim = dmd.Animation().load(self.game.assets.anim_marksman2)
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=7)
        awardTextTop = dmd.TextLayer(128/3,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/3,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        awardTextTop.set_text(self.awardString)
        awardTextBottom.set_text(self.awardPoints)
        completeFrame = dmd.GroupedLayer(128, 32, [animLayer,awardTextTop,awardTextBottom])
        self.layer = completeFrame
        ## TODO this delay doesn't seem to be working
        self.delay(delay=2,handler=self.clear_layer)


    def show_award_text(self,blink=None):
    # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=blink,seconds=1)
            awardTextBottom.set_text(self.awardPoints,blink_frames=blink,seconds=1)
        else:
            awardTextTop.set_text(self.awardString)
            awardTextBottom.set_text(self.awardPoints)
            # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.border,awardTextTop,awardTextBottom])
        # swap in the new layer
        self.layer = completeFrame
        #self.transition = ep.EP_Transition(self,self.layer,completeFrame,self.type)

        # clear in 2 seconds
        self.delay(delay=2,handler=self.clear_layer)

    def push_out(self):
        # crap I had this then it stopped working
        print "TRANSITIONING WTF"
        self.transition = ep.EP_Transition(self,self.layer,self.game.score_display.layer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_SOUTH)
        self.transition.callback = self.clear_layer()

    def play_glass_sound_one(self):
        self.game.sound.play(self.game.assets.sfx_breakingGlass1)

    def play_glass_sound_two(self):
        self.game.sound.play(self.game.assets.sfx_breakingGlass2)

    def clear_layer(self):
        self.layer = None
        return True