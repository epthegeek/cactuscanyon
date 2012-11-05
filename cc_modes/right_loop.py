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
## Mode for handling the right loop
##

from procgame import *
import cc_modes
import ep

class RightLoop(ep.EP_Mode):
    """Cactus Canyon Left Loop"""
    def __init__(self, game, priority):
        super(RightLoop, self).__init__(game, priority)
        # set up a frame layer with the guns border on it
        self.border = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_gunsBorder.frames[0])
        self.layer = None
        self.weedsForCvA = 3

    def mode_started(self):
        self.update_lamps()

    def mode_stopped(self):
        self.disable_lamps()

    def update_lamps(self):
        self.disable_lamps()
        ## if status is multiball check the jackpot and take actions
        lampStatus = self.game.show_tracking('lampStatus')
        # we bail here if the others don't match and it's not "ON"
        if lampStatus != "ON":
            return

        ## high noon check
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
            return

        # goldmine active check
        if self.game.show_tracking('mineStatus') == "RUNNING":
            if self.game.show_tracking('jackpotStatus',3):
                self.game.lamps.rightLoopJackpot.schedule(0x0F0FFE00)
                self.game.lamps.rightLoopMarksman.schedule(0x0F0F1F30)
                self.game.lamps.rightLoopGunslinger.schedule(0x0F0F03F1)
                self.game.lamps.rightLoopGoodShot.schedule(0x0F0F007F)
            return
            # drunk multiball
        if self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
        ## right ramp is #4 in the stampede jackpot list
            if 'rightLoop' in self.game.drunk_multiball.active:
                self.game.lamps.rightLoopJackpot.schedule(0xF000F000)
                self.game.lamps.rightLoopMarksman.schedule(0xFF00FF00)
                self.game.lamps.rightLoopGunslinger.schedule(0xF0F0F0F0)
                self.game.lamps.rightLoopGoodShot.schedule(0xF00FF00F)
            return

        # bionic bart
        if self.game.show_tracking('bionicStatus') == "RUNNING":
            if 3 in self.game.bionic.activeShots:
                self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
                self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
                self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
                self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
            return

        # cva
        if self.game.show_tracking('cvaStatus') == "RUNNING":
            if self.game.cva.activeShot == 3:
                self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
                self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
                self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
                self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
            return


        stage = self.game.show_tracking('rightLoopStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.rightLoopGoodShot.schedule(0x0F0F0F0F)
        elif stage == 2:
            # first light on
            self.game.lamps.rightLoopGoodShot.enable()
            # blink the second
            self.game.lamps.rightLoopGunslinger.schedule(0x0F0F0F0F)
        elif stage == 3:
            # first two on
            self.game.lamps.rightLoopGoodShot.enable()
            self.game.lamps.rightLoopGunslinger.enable()
            # blink the third
            self.game.lamps.rightLoopMarksman.schedule(0x0F0F0F0F)
        # this is completed
        elif stage == 4:
            # all three on
            self.game.lamps.rightLoopGoodShot.enable()
            self.game.lamps.rightLoopGunslinger.enable()
            self.game.lamps.rightLoopMarksman.enable()
        # stampede
        elif stage == 89:
        ## right loop is #3 in the stampede jackpot list
            if self.game.stampede.active == 3:
                self.game.lamps.rightLoopJackpot.schedule(0xF000F000)
                self.game.lamps.rightLoopMarksman.schedule(0xFF00FF00)
                self.game.lamps.rightLoopGunslinger.schedule(0xF0F0F0F0)
                self.game.lamps.rightLoopGoodShot.schedule(0xF00FF00F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.rightLoopJackpot.schedule(0xFF00FF00)

        else:
            pass

    def disable_lamps(self):
        self.game.lamps.rightLoopGoodShot.disable()
        self.game.lamps.rightLoopGunslinger.disable()
        self.game.lamps.rightLoopMarksman.disable()
        self.game.lamps.rightLoopJackpot.disable()

    def sw_rightLoopBottom_active(self,sw):
        # low end of the loop
        # play the sound effect if we're not coming from the top
        if ep.last_switch != 'rightLoopTop':
            stage = self.game.show_tracking('rightLoopStage')
            if stage != 4:
                # while working on completing, the sound plays
                self.game.sound.play(self.game.assets.sfx_rightLoopEnter)
        # score come points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightLoopBottom"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_rightLoopTop_active(self,sw):
        # this switch only matters if bart isn't moving - he trips it sometimes
        if not self.game.bart.moving:
            print "RIGHT LOOP TOP HIT"
            # by default turn off the right side loop gate when we get to this switch
            self.game.coils.rightLoopGate.disable()
            # if we aren't coming through on a full loop - it's a natural hit and it counts
            if ep.last_switch == 'rightLoopBottom':
                # cancel any other displays
                for mode in self.game.ep_modes:
                    if getattr(mode, "abort_display", None):
                        mode.abort_display()
                        # if we're complete open the gate for a full run through

                if self.game.show_tracking('rightLoopStage') >= 4:
                    # pulse the coil to open the gate
                    self.game.coils.leftLoopGate.pulse(240)
                    # play a lampshow
                    self.game.lampctrl.play_show(self.game.assets.lamp_rightToLeft, repeat=False,callback=self.game.update_lamps)
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
            elif  ep.last_switch == "leftLoopTop":
                self.game.score_with_bonus(2530)
                self.game.increase_tracking('fullLoops')
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
            self.game.score_with_bonus(125000)
            # load the animation
            anim = self.game.assets.dmd_shotBottles
            # calculate a wait
            myWait = len(anim.frames) / 10.0
            # create the layer
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time=6
            animLayer.opaque=True
            animLayer.add_frame_listener(4,self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
            animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
            animLayer.add_frame_listener(13,self.game.sound.play,param=self.game.assets.sfx_breakingGlass2)

            # put it in place
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_CROSSFADE
            self.direction = None
            # then delayed kickoff the text display
            self.delay(name="Display",delay=myWait,handler=self.show_award_text)

        elif stage == 2:
            self.awardString = "GUNSLINGER"
            self.awardPoints = "150,000"
            self.game.score_with_bonus(150000)
            # play the animation and such
            anim = self.game.assets.dmd_shotCandles
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            self.layer = animLayer
            self.type = ep.EP_Transition.TYPE_EXPAND
            self.delay(name="Display",delay=myWait,handler=self.show_award_text)
        elif stage == 3:
            self.awardString = "MARKSMAN"
            self.awardPoints = "175,000"
            self.game.score_with_bonus(175000)
            #self.show_award_text()
            anim = self.game.assets.dmd_shotCard
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=6)
            self.layer = animLayer
            self.delay(name="Display",delay=myWait,handler=self.show_marksman_award)

        # anything 4 or more is complete
        else:
            #self.awardString = "SHOTS COMPLETE"
            #self.awardPoints = "150,000"
            #self.game.score(15000)
            #self.type = ep.EP_Transition.TYPE_CROSSFADE
            # if we're not on a combo  show the award - combos after stage 4 should just show the combo
            #self.show_award_text()
            # New thing - Tumbleweed!
            points = self.game.increase_tracking('tumbleweedValue',5000)
            # this number can reset for re-starting cva
            value = self.game.increase_tracking('tumbleweedHits')
            # this one is a running total
            self.game.increase_tracking('tumbleweedHitsTotal')
            # compare the number to light cva with the current number
            left = self.game.base.tumbleweedShots - value
            if left == 0:
                # enable cva
                self.game.set_tracking('cvaStatus',"READY")
            self.game.score_with_bonus(points)
            self.tumbleweed_display(points,combo)

        # then tick the stage up for next time unless it's completed
        if stage < 4:
            newstage = self.game.increase_tracking('rightLoopStage')
            # do a little lamp flourish
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x0FF00FF0)
            self.game.lamps.rightLoopMarksman.schedule(0xFF00FF00)
            # update the lamps
            self.delay(delay=1,handler=self.update_lamps)
            # if we're now complete, check stampede
            if newstage == 4:
                self.game.base.check_stampede()



    def show_marksman_award(self):
        anim = self.game.assets.dmd_smokingCard
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=7)
        awardTextTop = dmd.TextLayer(128/3,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/3,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        awardTextTop.set_text(self.awardString)
        awardTextBottom.set_text(self.awardPoints)
        completeFrame = dmd.GroupedLayer(128, 32, [animLayer,awardTextTop,awardTextBottom])
        self.layer = completeFrame
        self.delay(name="Display",delay=2,handler=self.clear_layer)


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
        currentLayer = self.layer
        self.transition = ep.EP_Transition(self,currentLayer,completeFrame,self.type)

        # clear in 2 seconds
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def push_out(self):
        # crap I had this then it stopped working
        print "TRANSITIONING WTF"
        self.transition = ep.EP_Transition(self,self.layer,self.game.score_display.layer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_SOUTH)
        self.transition.callback = self.clear_layer()

    def tumbleweed_display(self,value,combo):
        banner = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_tumbleweedBanner.frames[0])
        scoreLayer = dmd.TextLayer(64,22,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(ep.format_score(value)),blink_frames=6)
        # load up the animation
        anim = self.game.assets.dmd_tumbleweedLeft
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
        if combo:
            self.delay(name="Display",delay=myWait,handler=self.game.combos.display)


    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
