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
        self.border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'guns-border.dmd').frames[0])

    def mode_started(self):
        # this would have to turn on some lights and stuff
        pass

    def sw_rightLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_rightLoopEnter)
        # score come points
        self.game.score(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightLoopBottom"

    def sw_rightLoopTop_active(self,sw):
        # if we aren't coming through on a full loop - it's a natural hit and it counts
        if ep.last_switch != "leftLoopTop":
            # if we're complete open the gate for a full run through
            ## if the combo timer is on:
            if self.game.comboTimer > 0:
                # register the combo and reset the timer
                combo = self.game.base_game_mode.combo_hit()
                # if we're "complete" open the full loop
                if self.game.show_tracking('rightLoopStage') >= 4:
                    # pulse the coil to open the gate
                    pass
            # else the combo timer is NOT on so run award loop without the flag
            else:
                # and turn on the combo timer
                combo = self.game.base_game_mode.start_combos()

            # award the loop reward
            self.award_loop_score(combo)
        # otherwise it's a roll through so just add some points
        # maybe add tracking for full loops
        else:
            self.game.score(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightLoopTop"

    def award_loop_score(self,combo=False):
        # cancel the "Clear" delay if there is one
        self.cancel_delayed("Clear")
        self.cancel_delayed("Transition")
        # if we're on stage one
        stage = self.game.show_tracking('rightLoopStage')
        if stage == 1:
            self.awardString = "GOOD SHOT"
            self.awardPoints = "125,000"
            self.game.score(125000)
            # load the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'shot-bottles-animation.dmd')
            # calculate a wait
            myWait = len(anim.frames) / 10.0
            # create the layer
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time=6
            animLayer.opaque=True
            animLayer.add_frame_listener(4,self.game.play_remote_sound,param=self.game.assets.sfx_breakingGlass1)
            animLayer.add_frame_listener(7,self.game.play_remote_sound,param=self.game.assets.sfx_breakingGlass1)
            animLayer.add_frame_listener(13,self.game.play_remote_sound,param=self.game.assets.sfx_breakingGlass2)

            # put it in place
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_CROSSFADE
            self.direction = None
            # then delayed kickoff the text display
            self.delay(name="Transition",delay=myWait,handler=self.show_award_text)

        elif stage == 2:
            self.awardString = "GUNSLINGER"
            self.awardPoints = "150,000"
            self.game.score(15000)
            # play the animation and such
            anim = dmd.Animation().load(ep.DMD_PATH+'shot-candles-animation.dmd')
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_EXPAND
            self.delay(name="Transition",delay=myWait,handler=self.show_award_text)
        elif stage == 3:
            self.awardString = "MARKSMAN"
            self.awardPoints = "175,000"
            self.game.score(175000)
            #self.show_award_text()
            anim = dmd.Animation().load(ep.DMD_PATH+'shot-card-animation.dmd')
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=6)
            self.layer = animLayer
            self.delay(name="Transition",delay=myWait,handler=self.show_marksman_award)

        # anything 4 or more is complete
        else:
            self.awardString = "SHOTS COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(15000)
            # if we're not on a combo  show the award - combos after stage 4 should just show the combo
            if combo:
                self.layer = None
                self.game.base_game_mode.combo_display()
            else:
                self.show_award_text()
        # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('rightLoopStage')

    def show_marksman_award(self):
        anim = dmd.Animation().load(ep.DMD_PATH+'smoking-card-loop.dmd')
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
        #self.layer = completeFrame
        self.transition = ep.EP_Transition(self,self.layer,completeFrame,self.type)

        # clear in 2 seconds
        self.delay(name="ClearRightLoop",delay=2,handler=self.clear_layer)

    def push_out(self):
        # crap I had this then it stopped working
        print "TRANSITIONING WTF"
        self.transition = ep.EP_Transition(self,self.layer,self.game.score_display.layer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_SOUTH)
        self.transition.callback = self.clear_layer()

    def clear_layer(self):
        self.layer = None
        return True