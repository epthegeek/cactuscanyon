##
## This mode keeps track of the awards and points for making the right ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes
import ep

class RightRamp(game.Mode):
    """Cactus Canyon Right Ramp Mode"""
    def __init__(self, game, priority):
        super(RightRamp, self).__init__(game, priority)
        # Set up the sounds

    def mode_started(self):
        # this would have to turn on some lights and stuff
        pass

    def sw_rightRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_rightRampEnter)
        # score the arbitrary and wacky points
        self.game.score(2530)

    def sw_rightRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('rightRampShots')
        self.award_ramp_score()

    def sw_rightRampBottom_active(self,sw):
        self.game.score(2530)

    def award_ramp_score(self):
        # cancel the "Clear" delay if there is one
        self.cancel_delayed("ClearRightRamp")

        # TODO these all need fleshing out with sounds and final animations
        stage = self.game.show_tracking('rightRampStage')
        if stage == 1:
            ## set the text lines for the display later
            self.awardString = "SOUND ALARM"
            self.awardPoints = "125,000*"
            self.game.score(125000)
            # load the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'bank-explodes.dmd')
            # calcuate the wait time to start the next part of the display
            myWait = len(anim.frames) / 8.57
            # play the first sound
            self.game.sound.play(self.game.assets.sfx_explosion1)
            self.game.sound.play_voice(self.game.assets.quote_rightRamp1)
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7

            # added a frame listener for the second sound effect
            animLayer.add_frame_listener(5, self.game.play_remote_sound,param=self.game.assets.sfx_fallAndCrash1)
            # play the animation
            self.layer = animLayer
            # add some score
            # apply the calculated delay to the next step
            self.delay(delay=myWait,handler=self.blink_award_text)
        elif stage == 2:
            # set the text lines for the display
            self.awardString = "SHOOT OUT"
            self.awardPoints = "150,000*"
            self.game.score(150000)
            # load the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'bank-sherrif-arrives.dmd')
            # calculate the wait time
            myWait = len(anim.frames) / 8.57
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7

            # add listener frames
            animLayer.add_frame_listener(15,self.game.play_remote_sound,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(17,self.game.play_remote_sound,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(19,self.game.play_remote_sound,param=self.game.assets.sfx_explosion11)
            # play the start sound
            self.game.sound.play_voice(self.game.assets.quote_rightRamp2)
            # play the animation
            self.layer = animLayer
            # apply the delay
            self.delay(delay=myWait,handler=self.blink_award_text)

        elif stage == 3:
            self.awardString = "ROBBERY FOILED"
            self.awardPoints = "175,000*"
            self.game.score(175000)
            anim = dmd.Animation().load(ep.DMD_PATH+'sheriff-pan.dmd')
            # waith for the pan up to finish
            myWait = 1.14
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)
            # play sounds
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play(self.game.assets.quote_pollyThankYou)
            # play animation
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.anim_bank_victory)

        ## for now, anything above 3 is 'complete'
        else:
            self.awardString = "ROBBERY FOILED"
            self.awardPoints = "150,000*"
            self.game.score(150000)
            # play sounds
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play_voice(self.game.assets.quote_victory)
            # play animation
            self.anim_bank_victory()

        # then tick the stage up for next time unless it's completed
        if self.game.show_tracking('rightRampStage') < 4:
            self.game.increase_tracking('rightRampStage')

    def clear_layer(self):
        self.layer = None

    def anim_bank_victory(self):
        print "BANK VICTORY"
        anim = dmd.Animation().load(ep.DMD_PATH+'bank-victory-animation.dmd')
        myWait = len(anim.frames) / 8.57
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 7

        animLayer.add_frame_listener(7,self.game.play_remote_sound,param=self.game.assets.sfx_blow)
        animLayer.add_frame_listener(14,self.game.play_remote_sound,param=self.game.assets.sfx_grinDing)
        # play animation
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.blink_award_text)

    def blink_award_text(self):
        # stage one of showing the award text - this one blinks
        self.build_award_text(12)
        # switch to solid in 1 seconds
        self.delay(delay=1,handler=self.show_award_text)

    def show_award_text(self):
        # stage 2 of showing the award text
        self.build_award_text()
        # turn it off in 1 seconds
        self.delay(name="ClearRightRamp",delay=1,handler=self.clear_layer)

    def build_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ_outline,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az_outline,justify="center",opaque=False)
        awardTextBottom.composite_op = "blacksrc"
        awardTextTop.composite_op = "blacksrc"

        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=12)
            awardTextBottom.set_text(self.awardPoints,blink_frames=12)
        else:
            awardTextTop.set_text(self.awardString)
            awardTextBottom.set_text(self.awardPoints)
            #awardTextmask.set_text(self.awardPoints)
        # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # swap in the new layer
        self.layer = completeFrame
