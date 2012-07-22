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
##
## Mode for the left loop
## An always on mode, but separated for readability
##

from procgame import *
import cc_modes
import ep

class LeftLoop(ep.EP_Mode):
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
        lampStatus = self.game.show_tracking('lampStatus')
        # we bail here if the others don't match and it's not "ON"
        if lampStatus != "ON":
            return

        ## high noon check
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)
            return
        ## goldmine check - if stack level 2 is true, it's on
        if self.game.show_tracking('mineStatus') == "RUNNING":
            # check if this jackpot shot is active
            if self.game.show_tracking('jackpotStatus',0):
                self.game.lamps.leftLoopJackpot.schedule(0x0F0FFE00)
                self.game.lamps.leftLoopRideEm.schedule(0x0F0F1F30)
                self.game.lamps.leftLoopWildRide.schedule(0x0F0F03F1)
                self.game.lamps.leftLoopBuckNBronco.schedule(0x0F0F007F)
            return

            # drunk multiball
        if self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
        ## right ramp is #4 in the stampede jackpot list
            if 'leftLoop' in self.game.drunk_multiball.active:
                self.game.lamps.leftLoopJackpot.schedule(0xF000F000)
                self.game.lamps.leftLoopRideEm.schedule(0xFF00FF00)
                self.game.lamps.leftLoopWildRide.schedule(0xF0F0F0F0)
                self.game.lamps.leftLoopBuckNBronco.schedule(0xF00FF00F)
            return

        if self.game.show_tracking('bionicStatus') == "RUNNING":
            if 0 in self.game.bionic.activeShots:
                self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
                self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
                self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
                self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)
            return

        stage = self.game.show_tracking('leftLoopStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.leftLoopBuckNBronco.schedule(0x0F0F0F0F)
        elif stage == 2:
            # first light on
            self.game.lamps.leftLoopBuckNBronco.enable()
            # blink the second
            self.game.lamps.leftLoopWildRide.schedule(0x0F0F0F0F)
        elif stage == 3:
            # first two on
            self.game.lamps.leftLoopBuckNBronco.enable()
            self.game.lamps.leftLoopWildRide.enable()
            # blink the third
            self.game.lamps.leftLoopRideEm.schedule(0x0F0F0F0F)
        # this is completed
        elif stage == 4:
            # all three on
            self.game.lamps.leftLoopBuckNBronco.enable()
            self.game.lamps.leftLoopWildRide.enable()
            self.game.lamps.leftLoopRideEm.enable()
        ## 89 is stampede
        elif stage == 89:
        ## left loop is #0 in the stampede jackpot list
            if self.game.stampede.active == 0:
                self.game.lamps.leftLoopJackpot.schedule(0xF000F000)
                self.game.lamps.leftLoopRideEm.schedule(0xFF00FF00)
                self.game.lamps.leftLoopWildRide.schedule(0xF0F0F0F0)
                self.game.lamps.leftLoopBuckNBronco.schedule(0xF00FF00F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.leftLoopJackpot.schedule(0xFF00FF00)

        else:
            pass

    def disable_lamps(self):
        self.game.lamps.leftLoopBuckNBronco.disable()
        self.game.lamps.leftLoopWildRide.disable()
        self.game.lamps.leftLoopRideEm.disable()
        self.game.lamps.leftLoopJackpot.disable()

    def sw_leftLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect if we're not coming from the top switch
        if ep.last_switch != 'leftLoopTop':
            stage = self.game.show_tracking('leftLoopStage')
            if stage != 4:
                self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
        # score come points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "leftLoopBottom"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_leftLoopTop_active(self,sw):
        # turn off the left loop gate by default
        self.game.coils.leftLoopGate.disable()
        # if we aren't coming through on a full loop - it's a natural hit and it counts
        if ep.last_switch == 'leftLoopBottom':
            # cancel any other displays
            for mode in self.game.ep_modes:
                if getattr(mode, "abort_display", None):
                    mode.abort_display()

                # if we're complete open the gate for a full run through
            # if we're "complete" open the full loop
            if self.game.show_tracking('leftLoopStage') >= 4:
                # pulse the coil to open the gate
                self.game.coils.rightLoopGate.pulse(150)
                # play a lampshow
                self.game.lampctrl.play_show(self.game.assets.lamp_leftToRight, repeat=False,callback=self.game.update_lamps)
            ## if the combo timer is on:
            if self.game.combos.myTimer > 0:
                # register the combo and reset the timer
                combo = self.game.combos.hit()
            # else the combo timer is NOT on so run award loop without the flag
            else:
                # and turn on the combo timer
                combo = self.game.combos.start()

            # award the loop reward
            self.award_loop_score(combo)
        # if it's a roll through so just add some points
        elif ep.last_switch == 'rightLoopTop':
            self.game.score_with_bonus(2530)
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
            self.game.score_with_bonus(125000)
            self.game.sound.play_voice(self.game.assets.quote_leftLoop1)
            # set the item to use, frame time to use, and amount to divide my wait by
            thisOne = 1
            frame_time = 6
            divisor = 10.0
        elif stage == 2:
            self.awardString = "WILD RIDE"
            self.awardPoints = "150,000"
            self.game.score_with_bonus(15000)
            thisOne = 1
            frame_time = 6
            divisor = 10.0
            # play the sound
            self.game.sound.play_voice(self.game.assets.quote_leftLoop1)
        elif stage == 3:
            self.awardString = "RIDE EM COWBOY"
            self.awardPoints = "175,000"
            self.game.score_with_bonus(175000)
            self.game.sound.play_voice(self.game.assets.quote_leftLoop2)
            thisOne = 0
            frame_time = 4
            divisor = 15
        # anything 4 or more is complete
        else:
            self.awardString = "BRONCO LOOPS COMPLETE"
            self.awardPoints = "150,000"
            thisOne = 0
            frame_time = 4
            divisor = 15

        # then tick the stage up for next time unless it's completed
        if stage < 4:
            newstage = self.game.increase_tracking('leftLoopStage')
            # do a little lamp flourish
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x0FF00FF0)
            self.game.lamps.leftLoopRideEm.schedule(0xFF00FF00)
            # update the lamps
            self.delay(delay=1,handler=self.update_lamps)
            self.game.center_ramp.update_lamps()
            # if we're complete, check the stampede tally
            if newstage == 4:
                self.game.base_game_mode.check_stampede()


        # break at this point if it was a combo hit on stage 4 or higher - dont' show the full display
        if stage >= 4:
            if combo:
                self.layer = None
                self.game.combos.display()
            else:
                # New thing - Tumbleweed!
                value = self.game.increase_tracking('tumbleweedValue',5000)
                self.game.score_with_bonus(value)
                self.tumbleweed_display(value)
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
        self.transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_SLIDEOVER,self.direction)
        # clear in 2 seconds
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def push_out(self):
        self.transition = ep.EP_Transition(self,self.layer,self.game.score_display.layer,ep.EP_Transition.TYPE_PUSH,self.anims[1]['direction'])
        self.transition.callback = self.clear_layer

    def tumbleweed_display(self,value):
        banner = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'tumbleweed-banner.dmd').frames[0])
        scoreLayer = dmd.TextLayer(64,22,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(ep.format_score(value)),blink_frames=6)
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'tumbleweed-right.dmd')
        # start the full on animation
        myWait = len(anim.frames) / 15.0 + 0.5
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 4
        animLayer.opaque=False
        animLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[banner,scoreLayer,animLayer])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_tumbleWind)
        self.delay(name="Display",delay=myWait,handler=self.clear_layer)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
