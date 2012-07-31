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
## This mode keeps track of the awards and points for making the center ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes
import ep

class CenterRamp(ep.EP_Mode):
    """Cactus Canyon Center Ramp Mode"""
    def __init__(self, game, priority):
        super(CenterRamp, self).__init__(game, priority)
        self.border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'tracks-border.dmd').frames[0])

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
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)
            return

        # check goldmine active status
        if self.game.show_tracking('mineStatus') == "RUNNING":
            if self.game.show_tracking('jackpotStatus',2):
                self.game.lamps.centerRampJackpot.schedule(0x0F0FFE00)
                self.game.lamps.centerRampSavePolly.schedule(0x0F0F1F30)
                self.game.lamps.centerRampStopTrain.schedule(0x0F0F03F1)
                self.game.lamps.centerRampCatchTrain.schedule(0x0F0F007F)
            return
            # drunk multiball
        if self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
        ## right ramp is #4 in the stampede jackpot list
            if 'centerRamp' in self.game.drunk_multiball.active:
                self.game.lamps.centerRampJackpot.schedule(0xF000F000)
                self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.centerRampStopTrain.schedule(0xF0F0F0F0)
                self.game.lamps.centerRampCatchTrain.schedule(0xF00FF00F)
            return

        if self.game.show_tracking('bionicStatus') == "RUNNING":
            if 2 in self.game.bionic.activeShots:
                self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)
            return

        stage = self.game.show_tracking('centerRampStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.centerRampCatchTrain.schedule(0x0F0F0F0F)
        elif stage == 2:
            # first light on
            self.game.lamps.centerRampCatchTrain.enable()
            # blink the second
            self.game.lamps.centerRampStopTrain.schedule(0x0F0F0F0F)
        elif stage == 3:
            # first two on
            self.game.lamps.centerRampCatchTrain.enable()
            self.game.lamps.centerRampStopTrain.enable()
            # blink the third
            self.game.lamps.centerRampSavePolly.schedule(0x0F0F0F0F)

        # this is after polly peril - all three on
        elif stage == 5:
        # after polly, before stampede all three stay on
            self.game.lamps.centerRampCatchTrain.enable()
            self.game.lamps.centerRampStopTrain.enable()
            self.game.lamps.centerRampSavePolly.enable()
        # save polly
        elif stage == 99:
            self.game.lamps.centerRampSavePolly.schedule(0x00FFFF00)
            self.game.lamps.centerRampStopTrain.schedule(0x0000FFFF)
            self.game.lamps.centerRampCatchTrain.schedule(0xFF0000FF)
        # stampede
        elif stage == 89:
        ## center ramp is #2 in the stampede jackpot list
            if self.game.stampede.active == 2:
                self.game.lamps.centerRampJackpot.schedule(0xF000F000)
                self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.centerRampStopTrain.schedule(0xF0F0F0F0)
                self.game.lamps.centerRampCatchTrain.schedule(0xF00FF00F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.centerRampJackpot.schedule(0xFF00FF00)

        else:
            pass

    def disable_lamps(self):
        self.game.lamps.centerRampCatchTrain.disable()
        self.game.lamps.centerRampStopTrain.disable()
        self.game.lamps.centerRampSavePolly.disable()
        self.game.lamps.centerRampJackpot.disable()

    def sw_centerRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_centerRampEnter)
        # score the arbitrary and wacky points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "centerRampEnter"

    def sw_centerRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('centerRampShots')
        # check the chain status
        if ep.last_shot == "left" or ep.last_shot == "right":
            # if there have been at least 2 combo chain shots before, we take action
            if self.game.combos.chain >= 2:
            #  and that action is, increase the chain increase the chain
                self.game.combos.increase_chain()
        else:
            # if not, set it back to one
            self.game.combos.chain = 1

        # hitting this switch counts as a made ramp - really
        # score the points and mess with the combo
        if self.game.combos.myTimer > 0:
            # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()
        self.award_ramp_score(combo)

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
        ## completed is CURRENTLY 4 - to reset the awards
        ## reset the leftRampStage
        stage = self.game.show_tracking('centerRampStage')
        if stage == 1:
            self.awardString = "CATCH TRAIN"
            self.awardPoints = "125,000"
            self.game.score_with_bonus(125000)
            self.game.base.play_quote(self.game.assets.quote_centerRamp1)
            self.game.sound.play(self.game.assets.sfx_trainChugShort)
            self.game.sound.play(self.game.assets.sfx_leftLoopEnter) # same sound used on left loop so the name is funny
            anim = dmd.Animation().load(ep.DMD_PATH+'train-boarding.dmd')
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            # turn it on
            self.layer = animLayer
            # set the delay for the award
            self.delay(name="Display",delay=myWait,handler=self.show_award_text)

        elif stage == 2:
            self.train_stage_two(score=150000)

        ## stage three starts save polly peril train toy mode
        elif stage == 3:
                self.game.increase_tracking('centerRampStage')
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
            # do a little lamp flourish
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampStopTrain.schedule(0x0FF00FF0)
            self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
            self.delay(delay=1,handler=self.update_lamps)

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
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_gunfightFlourish) # same noise from gunfight
        # swap in the new layer
        transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        # clear in 3 seconds
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        # show combo display if the chain is high enough
        if self.game.combos.chain > 2:
            self.delay(name="Display",delay=2,handler=self.game.combos.display)

    def train_stage_two(self,score):
        self.awardString = "STOP TRAIN"
        self.awardPoints = str(ep.format_score(score))
        self.game.score(score)
        self.game.base.play_quote(self.game.assets.quote_centerRamp2)
        self.game.sound.play(self.game.assets.sfx_trainChugShort)
        self.game.sound.play(self.game.assets.sfx_trainWhistle)
        anim = dmd.Animation().load(ep.DMD_PATH+'train-running-on-top.dmd')
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # turn it on
        self.layer = animLayer
        # set the delay for the award
        self.delay(name="Display",delay=myWait,handler=self.show_award_text)

    def train_victory(self):
        self.awardString = "POLLY SAVED"
        value = self.game.increase_tracking('adventureCompleteValue',5000)
        self.awardPoints = str(ep.format_score(value))
        self.game.score_with_bonus(value)
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'train-brake-pull.dmd')
        # start the full on animation
        myWait = len(anim.frames) / 8.57
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 7
        # keyframe sounds
        animLayer.add_frame_listener(13,self.game.sound.play,param=self.game.assets.sfx_trainStopWithBrake)
        # play the short chug
        self.game.sound.play(self.game.assets.sfx_trainChugShort)
        # turn on the animation
        self.layer = animLayer
        self.delay(name="Display",delay=myWait,handler=self.show_award_text)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")


