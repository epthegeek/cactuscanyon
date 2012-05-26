##
## This mode keeps track of the awards and points for making the center ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes
import ep

class CenterRamp(game.Mode):
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
        if lampStatus == "MULTIBALL":
            if self.game.show_tracking('jackpotStatus',2):
                self.game.lamps.centerRampCatchTrain.schedule(0xFFFFF39C)
                self.game.lamps.centerRampStopTrain.schedule(0x0FFFF39C)
                self.game.lamps.centerRampSavePolly.schedule(0x00FFF39C)
                self.game.lamps.centerRampJackpot.schedule(0x000FF39C)
        # if status is anything other than on, we bail here
        if lampStatus != "ON":
            return

        stage = self.game.show_tracking('centerRampStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
        elif stage == 2:
            # first light on
            self.game.lamps.centerRampCatchTrain.enable()
            # blink the second
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
        elif stage == 3:
            # first two on
            self.game.lamps.centerRampCatchTrain.enable()
            self.game.lamps.centerRampStopTrain.enable()
            # small change here - only blink the 3rd light if the other ramps are done
            if self.game.show_tracking('leftRampStage') == 4 and self.game.show_tracking('rightRampStage') == 4:
                # blink the third
                self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)

        # this is after polly peril - all three on
        elif stage == 4:
        # after polly, before stampede all three stay on
            self.game.lamps.centerRampCatchTrain.enable()
            self.game.lamps.centerRampStopTrain.enable()
            self.game.lamps.centerRampSavePolly.enable()
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
        self.game.score(2530)
        ## -- set the last switch hit --
        ep.last_switch = "centerRampEnter"

    def sw_centerRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('centerRampShots')
        ## -- set the last switch hit --
        ep.last_switch = "centerRampMake"

        # hitting this switch counts as a made ramp - really
        # score the points and mess with the combo
        if self.game.comboTimer > 0:
            # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()
        # award the ramp score
        self.award_ramp_score(combo)


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
            self.game.score(125000)
            self.game.sound.play(self.game.assets.quote_centerRamp1)
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

        ## TODO this should kick into polly peril I guess - don't want to start it with the side ramps
        ## TODO maybe provide a bonus for having them lit first - shots worth more points or something
        ## we're going to hold at stage 3 on the train ramp unless the other 2 are ready to start polly
        ## if the train gets hit again before the other two are ready, it's a repeat of stage 2
        elif stage == 3:
            if self.game.show_tracking('rightRampStage') >= 4 and self.game.show_tracking('leftRampStage') >= 4:
                self.game.modes.add(self.game.save_polly)
                self.game.save_polly.start_save_polly()
            else:
                self.train_stage_two(score=175000)
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
        if self.game.show_tracking('centerRampStage') < 3:
            self.game.increase_tracking('centerRampStage')
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
        # play the sound effect
        self.game.sound.play(self.game.assets.sfx_gunfightFlourish) # same noise from gunfight
        # swap in the new layer
        transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        # clear in 3 seconds
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def train_stage_two(self,score):
        self.awardString = "STOP TRAIN"
        self.awardPoints = str(ep.format_score(score))
        self.game.score(score)
        self.game.sound.play(self.game.assets.quote_centerRamp2)
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
        self.awardPoints = "150,000"
        self.game.score(150000)
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'train-brake-pull.dmd')
        # start the full on animation
        myWait = len(anim.frames) / 8.57
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 7
        # keyframe sounds
        animLayer.add_frame_listener(13,self.game.play_remote_sound,param=self.game.assets.sfx_trainStopWithBrakePull)
        # play the short chug
        self.game.sound.play(self.game.assets.sfx_trainChugShort)
        # turn on the animation
        self.layer = animLayer
        self.delay(name="Display",delay=myWait,handler=self.show_award_text)

    def clear_layer(self):
        self.layer = None

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")


