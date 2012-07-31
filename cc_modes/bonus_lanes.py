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
###
###  ____                          _
### | __ )  ___  _ __  _   _ ___  | |    __ _ _ __   ___  ___
### |  _ \ / _ \| '_ \| | | / __| | |   / _` | '_ \ / _ \/ __|
### | |_) | (_) | | | | |_| \__ \ | |__| (_| | | | |  __/\__\
### |____/ \___/|_| |_|\__,_|___/ |_____\__,_|_| |_|\___||___/
###
###
from procgame import *
from assets import *
import cc_modes
import ep

class BonusLanes(ep.EP_Mode):
    """Cactus Canyon Bonus Lanes"""
    def __init__(self, game, priority):
        super(BonusLanes, self).__init__(game, priority)

    def mode_started(self):
        # reset the bonus multiplier
        self.game.set_tracking('bonusX',1)

    def update_lamps(self):
        # reset first
        self.disable_lamps()
        status = self.game.show_tracking('lampStatus')
        ## if status is off, we bail here
        if status != "ON":
            return
            # bonus lanes
        if self.game.show_tracking('bonusLaneStatus',0) == 'ON':
            self.game.lamps.leftBonusLane.enable()
        if self.game.show_tracking('bonusLaneStatus',1) == 'ON':
            self.game.lamps.rightBonusLane.enable()

    def disable_lamps(self):
        self.game.lamps.leftBonusLane.disable()
        self.game.lamps.rightBonusLane.disable()

    def sw_leftBonusLane_active(self,sw):
        self.hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftBonusLane"

    def sw_rightBonusLane_active(self,sw):
        self.hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightBonusLane"

    def hit(self,side):
        # lookup the status of the lane that got hit
        stat = self.game.show_tracking('bonusLaneStatus',side)
        # if the lane is off
        if stat == "OFF":
            # set the status to on for the lane that got hit
            self.game.set_tracking('bonusLaneStatus',"ON",side)
            self.update_lamps()
            # light the light
            # points for lighting bonus lane
            self.game.score(35000)
            # then if they're both on now play the animation and turn them both off
            # and score points accordingly - 100k for completing the pair, 35,000 for one
            if self.is_time_to_increase():
                self.game.sound.play(self.game.assets.sfx_banjoTaDa)
                self.game.score(100000)
                self.increase()
            else:
                self.game.sound.play(self.game.assets.sfx_banjoTrillUp)
                self.game.score(35000)

        # if the lane is already on play the alternate sound and add points
        else:
            # play the alt sound
            self.game.sound.play(self.game.assets.sfx_banjoTrillDown)
            # add some points
            self.game.score(15000)

    def flip(self):
        self.game.invert_tracking('bonusLaneStatus')
        self.update_lamps()

    def is_time_to_increase(self):
        # if neither one is off, IT IS TIME
        if "OFF" not in self.game.show_tracking('bonusLaneStatus'):
            return True

    def increase(self):
        # cancel the "Clear" delay if there is one
        self.abort_display()

        # play the cactus mashing animation
        anim = dmd.Animation().load(ep.DMD_PATH+'bonus-cactus-mash.dmd')
        # calculate the wait for displaying the text
        myWait = (len(anim.frames) / 8.57) - 0.4
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 7
        animLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_cactusMash)
        animLayer.add_frame_listener(4,self.game.base.red_flasher_flourish)
        # run the animation
        self.layer = animLayer
        # increase the bonus
        self.game.increase_tracking('bonusX')
        # turn both lights off
        self.game.set_tracking('bonusLaneStatus',"OFF",0)
        self.game.set_tracking('bonusLaneStatus',"OFF",1)
        # after the delay, show the award
        self.delay(name="Display",delay=myWait,handler=self.show_bonus_award)

    def show_bonus_award(self):
        ## the top text line is just bonus
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextTop.set_text("BONUS:")
        ## The second line is the tracking value + X
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        awardTextBottom.set_text(str(self.game.show_tracking('bonusX')) + "X")
        # combine the text onto the held cactus animation
        newLayer = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # set the layer active
        self.layer = newLayer
        # then 1.5 seconds later, shut it off
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)
        self.delay(delay=1.5,handler=self.update_lamps)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
