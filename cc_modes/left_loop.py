##
## Mode for the left loop
## An always on mode, but separated for readability
##

from procgame import *
import cc_modes
import ep

class LeftLoop(game.Mode):
    """Cactus Canyon Left Loop"""
    def __init__(self, game, priority):
        super(LeftLoop, self).__init__(game, priority)
        # set up the animations they are to alternate
        self.anims = []
        anim0 = ep.DMD_PATH + "horse-run-left.dmd"
        self.anims.append({'layer':anim0,'direction':ep.EP_Transition.PARAM_WEST})
        anim1 = ep.DMD_PATH + "horse-drag.dmd"
        self.anims.append({'layer':anim1,'direction':ep.EP_Transition.PARAM_WEST})
        anim2 = ep.DMD_PATH + "horse-chase.dmd"
        self.anims.append({'layer':anim2,'direction':ep.EP_Transition.PARAM_EAST})
        anim3 = ep.DMD_PATH + "horse-run-right.dmd"
        self.anims.append({'layer':anim3,'direction':ep.EP_Transition.PARAM_EAST})


    def mode_started(self):
        self.update_lamps()

    def mode_stopped(self):
        self.disable_lamps()

    def update_lamps(self):
        self.disable_lamps()
        ## if status is off, we bail here
        if self.game.show_tracking('lampStatus') != "ON":
            return

        stage = self.game.show_tracking('leftLoopStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
        elif stage == 2:
            # first light on
            self.game.lamps.leftLoopBuckNBronco.enable()
            # blink the second
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
        elif stage == 3:
            # first two on
            self.game.lamps.leftLoopBuckNBronco.enable()
            self.game.lamps.leftLoopWildRide.enable()
            # blink the third
            self.game.lamps.leftLoopRideEm.schedule(0x0000FFFF)
        # this is completed
        elif stage == 4:
            # all three on
            self.game.lamps.leftLoopBuckNBronco.enable()
            self.game.lamps.leftLoopWildRide.enable()
            self.game.lamps.leftLoopRideEm.enable()
        else:
            pass

    def disable_lamps(self):
        self.game.lamps.leftLoopBuckNBronco.disable()
        self.game.lamps.leftLoopWildRide.disable()
        self.game.lamps.leftLoopRideEm.disable()

    def sw_leftLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
        # score come points
        self.game.score(2530)
        ## -- set the last switch hit --
        ep.last_switch = "leftLoopBottom"

    def sw_leftLoopTop_active(self,sw):

        # if we aren't coming through on a full loop - it's a natural hit and it counts
        if ep.last_switch == 'leftLoopBottom':
            # if we're complete open the gate for a full run through
            # if we're "complete" open the full loop
            if self.game.show_tracking('leftLoopStage') >= 4:
                # pulse the coil to open the gate
                self.game.coils.rightLoopGate.pulse(50)
            ## if the combo timer is on:
            if self.game.comboTimer > 0:
                # register the combo and reset the timer
                combo = self.game.base_game_mode.combo_hit()
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
            self.game.increase_tracking('fullLoops')
        ## -- set the last switch --
        ep.last_switch = "leftLoopTop"


    def award_loop_score(self,combo=False):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

            # if we're on stage one
        stage = self.game.show_tracking('leftLoopStage')
        if stage == 1:
            self.awardString = "BUCK N BRONCO"
            self.awardPoints = "125,000"
            self.game.score(125000)
            self.game.sound.play_voice(self.game.assets.quote_leftLoop1)
            # set the item to use, frame time to use, and amount to divide my wait by
            thisOne = 1
            frame_time = 6
            divisor = 10.0
        elif stage == 2:
            self.awardString = "WILD RIDE"
            self.awardPoints = "150,000"
            self.game.score(15000)
            thisOne = 1
            frame_time = 6
            divisor = 10.0
            # play the sound
            self.game.sound.play_voice(self.game.assets.quote_leftLoop1)
        elif stage == 3:
            self.awardString = "RIDE EM COWBOY"
            self.awardPoints = "175,000"
            self.game.score(175000)
            self.game.sound.play_voice(self.game.assets.quote_leftLoop2)
            thisOne = 0
            frame_time = 4
            divisor = 15
        # anything 4 or more is complete
        else:
            self.awardString = "BRONCO LOOPS COMPLETE"
            self.awardPoints = "150,000"
            self.game.score(15000)
            self.game.sound.play_voice(self.game.assets.quote_leftLoop2)
            thisOne = 0
            frame_time = 4
            divisor = 15

        # then tick the stage up for next time unless it's completed
        if stage < 4:
            self.game.increase_tracking('leftLoopStage')
            # update the lamps
            self.game.update_lamps()


        # break at this point if it was a combo hit on stage 4 or higher - dont' show the full display
        if stage >= 4 and combo:
            self.layer = None
            self.game.base_game_mode.combo_display()
            return

        # load the animation based on which was last played
        self.direction = self.anims[thisOne]['direction']
        anim = dmd.Animation().load(self.anims[thisOne]['layer'])

        # this works out ok because we play the 2 middle ones before the first
        # then flip it for next time
        self.anims.reverse()

        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / divisor - .5
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=frame_time)
        # run the animation
        self.layer = animLayer
        # then at the delay show the award
        self.delay(name="Display",delay=myWait,handler=self.show_award_text)

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
        #myDirection = self.anims[1]['direction']
        self.transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_SLIDEOVER,self.direction)
        # clear in 2 seconds
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def push_out(self):
        self.transition = ep.EP_Transition(self,self.layer,self.game.score_display.layer,ep.EP_Transition.TYPE_PUSH,self.anims[1]['direction'])
        self.transition.callback = self.clear_layer

    def clear_layer(self):
        self.layer = None

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
