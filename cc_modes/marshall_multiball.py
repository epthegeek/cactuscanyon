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
## A P-ROC Project by Eric Priepke, Copyright 2012-2013
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The Marshall Multiball

from procgame import dmd,game
import ep

class MarshallMultiball(ep.EP_Mode):
    """Marshall Multiball for when player achieves maximum rank """
    def __init__(self,game,priority):
        super(MarshallMultiball, self).__init__(game,priority)
        self.myID = "Marshall Multiball"
        self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_marshallBorder.frames[0])
        self.jackpotTimer = self.game.user_settings['Gameplay (Feature)']['Marshall Jackpot Timer']

    def mode_started(self):
        #print "Starting Marshall Multiball"
        # reset the points
        self.pointTotal = 0
        self.running = True
        self.game.stack_level(5,True)
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
        # for the badge points
        self.badgeHits = 0
        # 'jackpot' mode
        self.jackpot = False
        # timer for targets
        self.targetTime = 7
        # active targets
        self.activeTargets = [False,False,False,False]
        # bonus lanes
        self.bonusLanes = [False,False]
        # kill the music
        self.stop_music()
        # turn off all the lights
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()
        # set up the main lights
        self.update_lamps()
        # chase the rank lamps
        if not self.game.lamp_control.lights_out:
            self.game.lamps.rankStranger.schedule(0xFFF00000)
            self.game.lamps.rankPartner.schedule(0x0FFF0000)
            self.game.lamps.rankDeputy.schedule(0x000FFF00)
            self.game.lamps.rankSheriff.schedule(0x0000FFF0)
            self.game.lamps.rankMarshall.schedule(0x00000FFF)
        # if there's a quickdraw running, shut it down
        if self.game.quickdraw.running:
            self.game.quickdraw.lost(self.game.quickdraw.side)


        # play the quote
        duration = self.game.base.priority_quote(self.game.assets.quote_marshallMultiball)
        # If the multiball ball savers are a thing, do that
        self.game.base.multiball_saver()
        self.start()
        # music is optional based on a setting
        if self.game.user_settings['Gameplay (Feature)']['Marshall Multiball Music'] == 'Yes':
            self.delay("Operational",delay=duration+0.2,handler=self.music_on,param=self.game.assets.music_drunkMultiball)

    def ball_drained(self):
        if self.running:
            #print "WELL MMB KNOWS IT IS RUNNING"
            if self.game.trough.num_balls_in_play == 0 or self.game.trough.num_balls_in_play == 1:
                self.game.base.busy = True
                self.game.base.queued += 1
                self.cancel_delayed("Operational")
                self.end_mmb()

    # lamps
    def update_lamps(self):
        # first reset everything
        self.disable_lamps()
        if self.game.lamp_control.lights_out:
            return
        # then turn on what's needed
        # left loop
        if self.leftLoopLevel == 0:
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
        if self.leftLoopLevel >= 1:
            self.game.lamps.leftLoopBuckNBronco.enable()
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
        if self.leftLoopLevel >= 2:
            self.game.lamps.leftLoopWildRide.enable()
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
        if self.leftLoopLevel >= 3:
            self.game.lamps.leftLoopRideEm.enable()
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)
        if self.leftLoopLevel >= 4:
            self.game.lamps.leftLoopJackpot.enable()
            self.game.lamps.leftLoopCombo.schedule(0x00FF00FF)
        if self.leftLoopLevel == 5 or self.jackpot:
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)
            self.game.lamps.leftLoopCombo.schedule(0x00FF00FF)
        # left ramp
        if self.leftRampLevel == 0:
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
        if self.leftRampLevel >= 1:
            self.game.lamps.leftRampWhiteWater.enable()
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
        if self.leftRampLevel >= 2:
            self.game.lamps.leftRampWaterfall.enable()
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
        if self.leftRampLevel >= 3:
            self.game.lamps.leftRampSavePolly.enable()
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)
        if self.leftRampLevel >= 4:
            self.game.lamps.leftRampJackpot.enable()
            self.game.lamps.leftRampCombo.schedule(0x00FF00FF)
        if self.leftRampLevel == 5 or self.jackpot:
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)
            self.game.lamps.leftRampCombo.schedule(0x00FF00FF)
        # center ramp
        if self.centerRampLevel == 0:
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
        if self.centerRampLevel >= 1:
            self.game.lamps.centerRampCatchTrain.enable()
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
        if self.centerRampLevel >= 2:
            self.game.lamps.centerRampStopTrain.enable()
            self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
        if self.centerRampLevel >= 3:
            self.game.lamps.centerRampSavePolly.enable()
            self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)
        if self.centerRampLevel >= 4:
            self.game.lamps.centerRampJackpot.enable()
            self.game.lamps.centerRampCombo.schedule(0x00FF00FF)
        if self.centerRampLevel == 5 or self.jackpot:
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)
            self.game.lamps.centerRampCombo.schedule(0x00FF00FF)
        # right loop
        if self.rightLoopLevel == 0:
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
        if self.rightLoopLevel >= 1:
            self.game.lamps.rightLoopGoodShot.enable()
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
        if self.rightLoopLevel >= 2:
            self.game.lamps.rightLoopGunslinger.enable()
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
        if self.rightLoopLevel >= 3:
            self.game.lamps.rightLoopMarksman.enable()
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
        if self.rightLoopLevel >= 4:
            self.game.lamps.rightLoopJackpot.enable()
            self.game.lamps.rightLoopCombo.schedule(0x00FF00FF)
        if self.rightLoopLevel == 5 or self.jackpot:
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopCombo.schedule(0x00FF00FF)
        # right ramp
        if self.rightRampLevel == 0:
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
        if self.rightRampLevel >= 1:
            self.game.lamps.rightRampSoundAlarm.enable()
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
        if self.rightRampLevel >= 2:
            self.game.lamps.rightRampShootOut.enable()
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
        if self.rightRampLevel >= 3:
            self.game.lamps.rightRampSavePolly.enable()
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)
        if self.rightRampLevel >= 4:
            self.game.lamps.rightRampJackpot.enable()
            self.game.lamps.rightRampCombo.schedule(0x00FF00FF)
        if self.rightRampLevel == 5 or self.jackpot:
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)
            self.game.lamps.rightRampCombo.schedule(0x00FF00FF)
        # badge lights
        if self.badgeHits >= 1:
            self.game.lamps.starMotherlode.enable()
        if self.badgeHits >= 2:
            self.game.lamps.starCombo.enable()
        if self.badgeHits >= 3:
            self.game.lamps.starBartBrothers.enable()
        if self.badgeHits >= 4:
            self.game.lamps.starShowdown.enable()
        if self.jackpot >= 5:
            self.game.lamps.starMotherlode.schedule(0x00FF00FF)
            self.game.lamps.starCombo.schedule(0x00FF00FF)
            self.game.lamps.starBartBrothers.schedule(0x00FF00FF)
            self.game.lamps.starShowdown.schedule(0x00FF00FF)
            self.game.lamps.starStampede.schedule(0x00FF00FF)
            self.game.lamps.starHighNoon.schedule(0x00FF00FF)
        # bonus lane lights
        if self.bonusLanes[0]:
            self.game.lamps.leftBonusLane.enable()
        if self.bonusLanes[1]:
            self.game.lamps.rightBonusLane.enable()

    def disable_lamps(self):
    # turn off all the lights
        self.game.lamps.leftLoopBuckNBronco.disable()
        self.game.lamps.leftLoopWildRide.disable()
        self.game.lamps.leftLoopRideEm.disable()
        self.game.lamps.leftLoopJackpot.disable()
        self.game.lamps.leftLoopCombo.disable()
        self.game.lamps.leftRampWhiteWater.disable()
        self.game.lamps.leftRampWaterfall.disable()
        self.game.lamps.leftRampSavePolly.disable()
        self.game.lamps.leftRampJackpot.disable()
        self.game.lamps.leftRampCombo.disable()
        self.game.lamps.centerRampCatchTrain.disable()
        self.game.lamps.centerRampStopTrain.disable()
        self.game.lamps.centerRampSavePolly.disable()
        self.game.lamps.centerRampJackpot.disable()
        self.game.lamps.centerRampCombo.disable()
        self.game.lamps.rightLoopGoodShot.disable()
        self.game.lamps.rightLoopGunslinger.disable()
        self.game.lamps.rightLoopMarksman.disable()
        self.game.lamps.rightLoopJackpot.disable()
        self.game.lamps.rightLoopCombo.disable()
        self.game.lamps.rightRampSoundAlarm.disable()
        self.game.lamps.rightRampShootOut.disable()
        self.game.lamps.rightRampSavePolly.disable()
        self.game.lamps.rightRampJackpot.disable()
        self.game.lamps.rightRampCombo.disable()
        self.game.lamps.starMotherlode.disable()
        self.game.lamps.starCombo.disable()
        self.game.lamps.starBartBrothers.disable()
        self.game.lamps.starShowdown.disable()
        self.game.lamps.starStampede.disable()
        self.game.lamps.starHighNoon.disable()
        self.game.lamps.leftBonusLane.disable()
        self.game.lamps.rightBonusLane.disable()


    # switches
    # left loop
    def sw_leftLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        if self.jackpot:
            self.jackpot_shot()
            return

        self.leftLoopLevel += 1
        self.main_shot_routine(self.leftLoopLevel)
        # then reset the level if over
        if self.leftLoopLevel == 6:
            self.leftLoopLevel = 0
            # turn on the rank light for this shot
            self.light_badge()
        return game.SwitchStop

    # left ramp
    def sw_leftRampEnter_active(self,sw):
        if self.jackpot:
            self.jackpot_shot()
            return

        self.leftLoopLevel += 1
        self.main_shot_routine(self.leftLoopLevel)
        # then reset the level if over
        if self.leftLoopLevel == 6:
            self.leftLoopLevel = 0
            # turn on the rank light for this shot
            self.light_badge()
        return game.SwitchStop

    def sw_leftRampMake_active(self,sw):
        return game.SwitchStop

    #center ramp
    def sw_centerRampEnter_active(self,sw):
        return game.SwitchStop

    def sw_centerRampMake_active(self,sw):
        if self.jackpot:
            self.jackpot_shot()
            return

        self.centerRampLevel += 1
        self.main_shot_routine(self.centerRampLevel)
        # then reset the level if over
        if self.centerRampLevel == 6:
            self.centerRampLevel = 0
            # turn on the rank light for this shot
            self.light_badge()
        return game.SwitchStop

    #right loop
    def sw_rightLoopBottom_active(self,sw):
        self.register(10)
        return game.SwitchStop

    def sw_rightLoopTop_active(self,sw):
        if self.jackpot:
            self.jackpot_shot()
            return

        self.rightLoopLevel += 1
        self.main_shot_routine(self.rightLoopLevel)
        # then reset the level if over
        if self.rightLoopLevel == 6:
            self.rightLoopLevel = 0
            # turn on the rank light for this shot
            self.light_badge()

        return game.SwitchStop

    #right ramp
    def sw_rightRampEnter_active(self,sw):
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        if self.jackpot:
            self.jackpot_shot()
            return

        self.rightRampLevel += 1
        self.main_shot_routine(self.rightRampLevel)
        # then reset the level if over
        if self.rightRampLevel == 6:
            self.rightRampLevel = 0
            # turn on the rank light for this shot
            self.light_badge()

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
        self.bonus_lane_hit(0)
        return game.SwitchStop

    def sw_rightBonusLane_active(self,sw):
        self.bonus_lane_hit(1)
        return game.SwitchStop

    # beer mug
    def sw_beerMug_active(self,sw):
        self.register(300)
        return game.SwitchStop

    # quickdraw targets
    def sw_topLeftStandUp_active(self,sw):
        self.register(10)
        self.game.bad_guys.target_up(0)
        return game.SwitchStop

    def sw_bottomLeftStandUp_active(self,sw):
        self.register(100)
        self.game.bad_guys.target_up(1)
        return game.SwitchStop

    def sw_topRightStandUp_active(self,sw):
        self.register(10)
        self.game.bad_guys.target_up(2)
        return game.SwitchStop

    def sw_bottomRightStandUp_active(self,sw):
        self.register(100)
        self.game.bad_guys.target_up(3)
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
        self.register(50)
        return game.SwitchStop

    # saloon
    def sw_saloonGate_active(self,sw):
        return game.SwitchStop

    def sw_saloonBart_active(self,sw):
        self.register(50)
        return game.SwitchStop

    def sw_saloonPopper_active_for_290ms(self,sw):
        self.register(20)
        return game.SwitchStop



        # startup
    def start(self):
        # audit
        self.game.game_data['Feature']['Marshall MB Started'] += 1
        # tag this player as having run the MB so it doesn't repeat - if we're actually at rank 4
        if self.game.show_tracking('rank') == 4:
            self.game.set_tracking('marshallMultiballRun',True)
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

    def main_shot_routine(self,shot):
        if shot == 1:
            self.register(10)
        elif shot == 2:
            self.register(50)
        elif shot == 3:
            self.register(100)
        elif shot == 4:
            self.register(500)
        elif shot == 5:
            self.register(1000)
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
        elif value == 50:
            self.game.sound.play(self.game.assets.sfx_chime50)
            self.score(50)
        elif value == 100:
            self.game.sound.play(self.game.assets.sfx_chime100)
            self.score(100)
        elif value == 200:
            self.game.sound.play(self.game.assets.sfx_chime200)
            self.score(200)
        elif value == 300:
            self.game.sound.play(self.game.assets.sfx_chime300)
            self.score(300)
        elif value == 500:
            self.game.sound.play(self.game.assets.sfx_chime500)
            self.score(500)
        elif value == 750:
            self.game.sound.play(self.game.assets.sfx_chimeOut)
            self.score(750)
        elif value == 1000:
            self.game.sound.play(self.game.assets.sfx_chime1000)
            self.score(1000)
        elif value == 1500:
            self.game.sound.play(self.game.assets.sfx_chime1500)
            self.score(1500)
        elif value == 2000:
            self.game.sound.play(self.game.assets.sfx_chime2000)
            self.score(2000)
        elif value == 2500:
            self.game.sound.play(self.game.assets.sfx_chime2500)
            self.score(2500)
        elif value == 3000:
            self.game.sound.play(self.game.assets.sfx_chime3000)
            self.score(3000)
        elif value == 3500:
            self.game.sound.play(self.game.assets.sfx_chime3500)
            self.score(3500)
        elif value == 4500:
            self.game.sound.play(self.game.assets.sfx_chime4500)
            self.score(4500)
        elif value == 5000:
            self.game.sound.play(self.game.assets.sfx_chime5000)
            self.score(5000)
        # update the score
        self.main_display()

    # score points
    def score(self,points):
        self.pointTotal += points

    def light_badge(self):
        # increase the lit badge points
        self.badgeHits += 1
        # if we're now at 5, it's jackpot time
        if self.badgeHits >= 5:
            self.jackpot_mode(True)
        # and then update the lights
        self.update_lamps()

    def jackpot_mode(self,value):
        # set the flag
        self.jackpot = value
        # update the lights
        self.update_lamps()
        # if jackpot is active, set the timer to turn it off
        if self.jackpot == True:
            self.delay(delay=self.jackpotTimer,handler=self.jackpot_mode,param=False)
            # fire off the big bell
            self.game.sound.play(self.game.assets.sfx_churchBell)
        # if jackpots are ending, reset some things
        else:
            self.badgeHits = 0

    def jackpot_shot(self):
        # all main shots in jakcpot mode score 5000
        self.register(5000)

    def bonus_lane_hit(self,side):
        # if lit - score 20
        if self.bonusLanes[side]:
            self.register(20)
        # if it's not lit
        else:
            # light it up
            self.bonusLanes[side] = True
            # if they're now both lit - that's 1500 and reset
            if False not in self.bonusLanes:
                self.register(1500)
                self.bonusLanes = [False,False]
            # if this is the first one lit, it's worth 500
            else:
                self.register(500)
            # and update the lamps
            self.update_lamps()

    def hit_bad_guy(self,target):
        self.register(3000)

    # finish up
    def end_mmb(self):
        # stop the score from updating
        self.cancel_delayed("Score Display")
        # clear the layer
        self.clear_layer()
        # store up the final score - if better than any previous run
        #print "Marshall Multiball points: " + str(self.pointTotal)
        #print "Current best: " + str(self.game.show_tracking('marshallBest'))
        if self.pointTotal > self.game.show_tracking('marshallBest'):
            #print "Setting marshallBest to " + str(self.pointTotal)
            self.game.set_tracking('marshallBest',self.pointTotal)
        # add the final total to the player's score
        self.game.score(self.pointTotal * 100)
        # kill the running flag
        self.running = False
        self.game.stack_level(5,False)
        # turn the music back on
        if True not in self.game.show_tracking('stackLevel') and self.game.trough.num_balls_in_play != 0:
            self.music_on(self.game.assets.music_mainTheme)
        # check bionic - to cover marshall required
        self.game.badge.check_bionic()
        # turn off the base busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload
        self.unload()

    def mode_stopped(self):
        # turn the lights back on
        self.game.update_lamps()
        # kill the drop targets
        self.game.bad_guys.drop_targets()
        self.wipe_delays()
