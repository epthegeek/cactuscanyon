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
## The Marshall Multiball

from procgame import *
import cc_modes
import ep
import random

class MarshallMultiball(ep.EP_Mode):
    """Marshall Multiball for when player achieves maximum rank """
    def __init__(self,game,priority):
        super(MarshallMultiball, self).__init__(game,priority)
        self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_marshallBorder.frames[0])

    def mode_started(self):
        # reset the points
        self.pointTotal = 0
        self.running = True
        self.game.set_tracking('stackLevel',True,5)
        # kill the music
        self.game.sound.stop_music()
        self.game.sound.play(self.game.assets.sfx_chime3000)
        self.delay(delay=0.6,handler=self.game.sound.play,param=self.game.assets.sfx_chime3000)
        self.delay(delay=1.2,handler=self.game.sound.play,param=self.game.assets.sfx_chimeIntro)
        self.delay(delay=1.8,handler=self.start)

        # set a bunch of defaults
        self.leftLoopLevel = 0
        self.leftRampLevel = 0
        self.centerRampLevel = 0
        self.rightLoopLevel = 0
        self.rightRampLevel = 0
        # tally 5 main shots gotten past level 4 to reset
        self.completedSets = 0
        # for the mine/saloon
        self.activeHole = 0

    def ball_drained(self):
        if self.game.trough.num_balls_in_play in (1,0) and self.running:
            self.game.base.busy = True
            self.end()

    # lamps
    def update_lamps(self):
        # first reset everything
        self.disable_lamps()
        # then turn on what's needed
        # left loop
        if self.leftLoopLevel == 0:
            pass
        if self.leftLoopLevel >= 1:
            self.game.lamps.leftLoopBuckNBronco.enable()
        if self.leftLoopLevel >= 2:
            self.game.lamps.leftLoopWildRide.enable()
        if self.leftLoopLevel >= 3:
            self.game.lamps.leftLoopRideEm.enable()
        if self.leftLoopLevel >= 4:
            self.game.lamps.leftLoopJackpot.enable()
        if self.leftLoopLevel == 5:
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)
        # left ramp
        if self.leftRampLevel == 0:
            pass
        if self.leftRampLevel >= 1:
            self.game.lamps.leftRampWhiteWater.enable()
        if self.leftRampLevel >= 2:
            self.game.lamps.leftRampWaterfall.enable()
        if self.leftRampLevel >= 3:
            self.game.lamps.leftRampSavePolly.enable()
        if self.leftRampLevel >= 4:
            self.game.lamps.leftRampJackpot.enable()
        if self.leftRampLevel == 5:
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)
        # center ramp
        if self.centerRampLevel == 0:
            pass
        if self.centerRampLevel >= 1:
            self.game.lamps.centerRampCatchTrain.enable()
        if self.centerRampLevel >= 2:
            self.game.lamps.centerRampStopTrain.enable()
        if self.centerRampLevel >= 3:
            self.game.lamps.centerRampSavePolly.enable()
        if self.centerRampLevel >= 4:
            self.game.lamps.centerRampJackpot.enable()
        if self.centerRampLevel == 5:
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)
        # right loop
        if self.rightLoopLevel == 0:
            pass
        if self.rightLoopLevel >= 1:
            self.game.lamps.rightLoopGoodShot.enable()
        if self.rightLoopLevel >= 2:
            self.game.lamps.rightLoopGunslinger.enable()
        if self.rightLoopLevel >= 3:
            self.game.lamps.rightLoopMarksman.enable()
        if self.rightLoopLevel >= 4:
            self.game.lamps.rightLoopJackpot.enable()
        if self.rightLoopLevel == 5:
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
        # right ramp
        if self.rightRampLevel == 0:
            pass
        if self.rightRampLevel >= 1:
            self.game.lamps.rightRampSoundAlarm.enable()
        if self.rightRampLevel >= 2:
            self.game.lamps.rightRampShootOut.enable()
        if self.rightRampLevel >= 3:
            self.game.lamps.rightRampSavePolly.enable()
        if self.rightRampLevel >= 4:
            self.game.lamps.rightRampJackpot.enable()
        if self.rightRampLevel == 5:
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)



    def disable_lamps(self):
    # turn off all the lights
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()

    # switches
    # left loop
    def sw_leftLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        self.leftLoopLevel += 1
        self.main_shot_routine(self.leftLoopLevel)
        # then reset the level if over
        if self.leftLoopLevel == 6:
            self.leftLoopLevel = 0
        return game.SwitchStop

    # left ramp
    def sw_leftRampEnter_active(self,sw):
        self.leftLoopLevel += 1
        self.main_shot_routine(self.leftLoopLevel)
        # then reset the level if over
        if self.leftLoopLevel == 6:
            self.leftLoopLevel = 0
        return game.SwitchStop

    def sw_leftRampMake_active(self,sw):
        return game.SwitchStop

    #center ramp
    def sw_centerRampEnter_active(self,sw):
        return game.SwitchStop

    def sw_centerRampMake_active(self,sw):
        self.centerRampLevel += 1
        self.main_shot_routine(self.centerRampLevel)
        # then reset the level if over
        if self.centerRampLevel == 6:
            self.centerRampLevel = 0
        return game.SwitchStop

    #right loop
    def sw_rightLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_rightLoopTop_active(self,sw):
        self.rightLoopLevel += 1
        self.main_shot_routine(self.rightLoopLevel)
        # then reset the level if over
        if self.rightLoopLevel == 6:
            self.rightLoopLevel = 0
        return game.SwitchStop

    #right ramp
    def sw_rightRampEnter_active(self,sw):
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        self.rightRampLevel += 1
        self.main_shot_routine(self.rightRampLevel)
        # then reset the level if over
        if self.rightRampLevel == 6:
            self.rightRampLevel = 0
        return game.SwitchStop

    def sw_rightRampBottom_active(self,sw):
        return game.SwitchStop

    # inlanes
    def sw_leftReturnLane_active(self,sw):
        self.register(300)
        return game.SwitchStop

    def sw_rightReturnLane_active(self,sw):
        self.register(300)
        return game.SwitchStop

    # outlanes
    def sw_leftOutlane_active(self,sw):
        self.register(750)
        return game.SwitchStop

    def sw_rightOutlane_active(self,sw):
        self.register(750)
        return game.SwitchStop

    # bonus lanes
    def sw_leftBonusLane_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_rightBonusLane_active(self,sw):
        self.register(10)
        return game.SwitchStop

    # beer mug
    def sw_beerMug_active(self,sw):
        self.register(250)
        return game.SwitchStop

    # quickdraw targets
    def sw_topLeftStandUp_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_bottomLeftStandUp_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_topRightStandUp_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_bottomRightStandUp_active(self,sw):
        self.register(10)
        return game.SwitchStop

    # slingshots
    def sw_leftSlingshot_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_rightSlingshot_active(self,sw):
        self.register(10)
        return game.SwitchStop

    # bumpers
    def sw_leftJetBumper_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_rightJetBumper_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_bottomJetBumper_active(self,sw):
        self.register(10)
        return game.SwitchStop

    # mine
    def sw_mineEntrance_active(self,sw):
        return game.SwitchStop

    def sw_minePopper_active_for_390ms(self,sw):
        self.register(10)
        return game.SwitchStop

    # saloon
    def sw_saloonGate_active(self,sw):
        return game.SwitchStop

    def sw_saloonBart_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_saloonPopper_active_for_290ms(self,sw):
        self.register(10)
        return game.SwitchStop



        # startup
    def start(self):
        # tag this player as having run the MB so it doesn't repeat
        self.game.set_tracking('marshallMultiballRun',True)
        # play the quote
        self.game.base.priority_quote(self.game.assets.quote_marshallMultiball)
        # launch an extra ball
        if self.game.trough.num_balls_in_play < 2:
            self.game.trough.balls_to_autoplunge = 1
            self.game.trough.launch_balls(1)
        # run the display
        self.main_display()

    # display
    def main_display(self):
        scoreLayer = dmd.TextLayer(100, 17, self.game.assets.font_marshallScore, "right", opaque=False).set_text(str(self.pointTotal))

        combined = dmd.GroupedLayer(128,32,[self.backdrop,scoreLayer])
        self.layer = combined
        self.delay("Score Display",delay=0.5,handler=self.main_display)

    def main_shot_routine(self,shot):
        if shot == 1:
            self.register(10)
        elif shot == 2:
            self.register(20)
        elif shot == 3:
            self.register(30)
        elif shot == 4:
            self.register(300)
        elif shot == 5:
            self.register(500)
        elif shot == 6:
            self.register(2500)
            # and count the completion
            self.completedSets += 1
        # then update the lights
        self.update_lamps()

    # point values and their chime
    def register(self,value):
        if value == 10:
            self.game.sound.play(self.game.assets.sfx_chime10)
            self.score(10)
        elif value == 20:
            self.game.sound.play(self.game.assets.sfx_chime20)
            self.score(20)
        elif value == 30:
            self.game.sound.play(self.game.assets.sfx_chime30)
            self.score(30)
        elif value == 100:
            self.game.sound.play(self.game.assets.sfx_chime100)
            self.score(100)
        elif value == 200:
            self.game.sound.play(self.game.assets.sfx_chime200)
            self.score(200)
        elif value == 250:
            self.game.sound.play(self.game.assets.sfx_chime250)
            self.score(250)
        elif value == 300:
            self.game.sound.play(self.game.assets.sfx_chime300)
            self.score(310)
        elif value == 500:
            self.game.sound.play(self.game.assets.sfx_chime500)
            self.score(510)
        elif value == 750:
            self.game.sound.play(self.game.assets.sfx_chimeOut)
            self.score(750)
        elif value == 1000:
            self.game.sound.play(self.game.assets.sfx_chime1000)
            self.score(1020)
        elif value == 1500:
            self.game.sound.play(self.game.assets.sfx_chime1500)
            self.score(1530)
        elif value == 2000:
            self.game.sound.play(self.game.assets.sfx_chime2000)
            self.score(2070)
        elif value == 2500:
            self.game.sound.play(self.game.assets.sfx_chime2500)
            self.score(2520)
        elif value == 3000:
            self.game.sound.play(self.game.assets.sfx_chime3000)
            self.score(3030)
        elif value == 3500:
            self.game.sound.play(self.game.assets.sfx_chime3500)
            self.score(3570)
        elif value == 4500:
            self.game.sound.play(self.game.assets.sfx_chime4500)
            self.score(4510)
        elif value == 5000:
            self.game.sound.play(self.game.assets.sfx_chime5000)
            self.score(5030)

    # score points
    def score(self,points):
        self.pointTotal += points


    # finish up
    def end(self):
        # stop the score from updating
        self.cancel_delayed("Score Display")
        # store up the final score - if better than any previous run
        if self.pointTotal > self.game.show_tracking('marshallBest'):
            self.game.set_tracking('marshallBest',self.pointTotal)
        # add the final total to the player's score
        self.game.score(self.pointTotal)
        # kill the running flag
        self.running = False
        self.game.set_tracking('stackLevel',False,5)
        # turn off the base busy flag
        self.game.base.busy = False
        # unload
        self.unload()
