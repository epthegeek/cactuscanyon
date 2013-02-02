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
## A P-ROC Project by Eric Priepke, Copyright 2012
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The Moonlight Madness Multiball
##

## This multiball comes up when the game is played around midnight

from procgame import dmd,game
import ep
import random

class Moonlight(ep.EP_Mode):
    """Moonlight Madness multiball mode ... """
    def __init__(self,game,priority):
        super(Moonlight, self).__init__(game,priority)
        self.myID = "Moonlight Madness"
        self.starting = False
        self.ending = False
        self.bonanza = False
        # index for available shots
        self.liveShots = []
        self.availableShots = [0,1,2,3,4,5,6,7,8]
        # available shots and corresponding lights

        self.lampList = [ [self.game.lamps.leftQuickdraw],
                          [self.game.lamps.topRightQuickdraw,self.game.lamps.bottomRightQuickdraw],
                          [self.game.lamps.leftLoopBuckNBronco,self.game.lamps.leftLoopRideEm,self.game.lamps.leftLoopWildRide,self.game.lamps.leftLoopBuckNBronco],
                          [self.game.lamps.leftRampJackpot,self.game.lamps.leftRampSavePolly,self.game.lamps.leftRampWaterfall,self.game.lamps.leftRampWhiteWater],
                          [self.game.lamps.centerRampJackpot,self.game.lamps.centerRampSavePolly,self.game.lamps.centerRampStopTrain,self.game.lamps.centerRampCatchTrain],
                          [self.game.lamps.rightLoopJackpot,self.game.lamps.rightLoopMarksman,self.game.lamps.rightLoopGunslinger,self.game.lamps.rightLoopGoodShot],
                          [self.game.lamps.rightRampJackpot,self.game.lamps.rightRampSavePolly,self.game.lamps.rightRampShootOut,self.game.lamps.rightRampSoundAlarm],
                          [self.game.lamps.mineLock],
                          [self.game.lamps.saloonArrow,self.game.lamps.bountySaloon] ]
        self.enable = 0
        banner1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmBang.frames[0])
        banner2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmBoom.frames[0])
        banner3 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmCrash.frames[0])
        banner4 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmDOHO.frames[0])
        banner5 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmPowie.frames[0])
        banner6 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mmZap.frames[0])
        self.banners = [ banner1,banner2,banner3,banner4,banner5,banner6 ]
        self.booms = [self.game.assets.sfx_glassSmash,
                      self.game.assets.sfx_hitBionicBart,
                      self.game.assets.sfx_glassSmash,
                      self.game.assets.sfx_hitBionicBart,
                      self.game.assets.sfx_cow3,
                      self.game.assets.sfx_hitBionicBart,
                      self.game.assets.sfx_glassSmash,
                      self.game.assets.sfx_hitBionicBart,
                      self.game.assets.sfx_glassSmash]
        self.shotsAtStart = self.game.user_settings['Gameplay (Feature)']['Moonlight Shots at Start']


    ## switches
    def sw_rightRampBottom_active(self,sw):
        if self.starting:
            self.starting = False
            # switch the music
            self.music_on(self.game.assets.music_mmMainLoopOne)
            # launch 2 more balls
            self.game.trough.balls_to_autoplunge = 3
            self.game.trough.launch_balls(3)
            self.update_display()
            self.game.trough.start_ball_save(num_balls_to_save=5,time=20)
        return game.SwitchStop

    def sw_topLeftStandUp_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(0)
        return game.SwitchStop

    def sw_bottomLeftStandUp_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(0)
        return game.SwitchStop

    def sw_topRightStandUp_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(1)
        return game.SwitchStop

    def sw_bottomRightStandUp_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(1)
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(2)
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(3)
        return game.SwitchStop

    def sw_centerRampMake_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(4)
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(5)
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(6)
        return game.SwitchStop

    def sw_minePopper_active_for_290ms(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(7)
        self.game.mountain.eject()
        return game.SwitchStop

    def sw_saloonBart_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(8)
        return game.SwitchStop

    def sw_saloonPopper_active_for_290ms(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        else:
            self.switch_hit(8)
        self.game.saloon.kick()
        return game.SwitchStop

    # not lightable - still scorable in bonanza
    def sw_leftBonusLane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_rightBonusLane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_beerMug_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_leftSlingshot_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_rightSlingshot_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_jetBumpersExit_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_rightOutlane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop

    def sw_leftOutlane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit()
        return game.SwitchStop


    # chaff that doesn't do much
    def sw_leftReturnLane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_rightReturnLane_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_leftJetBumper_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_rightJetBumper_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_bottomJetBumper_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_centerRampEnter_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_rightRampEnter_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_leftRampMake_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_leftLoopBottom_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def sw_rightLoopBottom_active(self,sw):
        if self.bonanza:
            self.bonanza_hit(False)
        return game.SwitchStop

    def mode_started(self):
        self.moonlightTotal = 0
        self.running = True
        self.starting = True
        # kill the GI - and all the lights
        self.game.gi_control("OFF")
        self.game.lamp_control.disable_all_lamps()
        # pick a random shot to light to start with
        self.enable += self.shotsAtStart
        self.enable_shots()
        duration = self.game.sound.play(self.game.assets.sfx_churchBell)
        # start the intro music
        self.delay(delay=duration-1,handler=self.launch)
        # throw up an intro display
        anim = self.game.assets.dmd_moonIntro
        backdrop = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=12)
        topLine = dmd.TextLayer(74, 5, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("MOONLIGHT")
        topLine.composite_op = "blacksrc"
        bottomLine = dmd.TextLayer(74, 18, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("MADNESS")
        bottomLine.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[backdrop,topLine,bottomLine])
        self.layer = combined
        self.delay("Display",delay=duration+2,handler=self.update_display)

    def launch(self):
        self.music_on(self.game.assets.music_mmOpeningLoop)
        # launch a ball, unless there is one in the shooter lane already
        if not self.game.switches.shooterLane.is_active():
            self.game.trough.launch_balls(1) # eject a ball into the shooter lane
        else:
            self.game.trough.num_balls_in_play += 1

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 1:
            # force the ending
            self.ending = True
            self.darken()
        if self.game.trough.num_balls_in_play == 0:
            self.cancel_delayed("Display")
            # wrap up the mode
            self.final_display()

    def update_display(self):
        self.cancel_delayed("Display")
        titleString = "MOONLIGHT MADNESS"
        titleLine = dmd.TextLayer(128/2, 0, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(titleString)
        # score line
        points = self.moonlightTotal
        scoreString = ep.format_score(points)
        if self.bonanza:
            scoreLine = dmd.TextLayer(64, 9, self.game.assets.font_13px_thin_score, "center", opaque = False).set_text(scoreString,blink_frames=4)
            if self.ending:
                textString = "FINISHING UP"
            else:
                textString = "ALL SWITCHES = 3 MILLION"
            infoLine = dmd.TextLayer(64,25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString)
            layers = [titleLine, scoreLine, infoLine]
        else:
            scoreLine = dmd.TextLayer(64, 7, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4)
            infoLine = dmd.TextLayer(64,18,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SHOOT LIT ITEMS")
            amount = 9 - len(self.liveShots)
            textString = str(amount) + " MORE FOR BONANZA"
            infoLine2 = dmd.TextLayer(64,24,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString)
            layers = [titleLine, scoreLine, infoLine, infoLine2]
        self.layer = dmd.GroupedLayer(128,32,layers)
        # loop back to update the score and whatnot
        self.delay("Display", delay=0.5, handler=self.update_display)

    def final_display(self):
        # kill all the stuff, just in case we went from 2 balls to 0
        self.darken()
        self.ending = False
        # play the closing riff
        self.game.sound.play_music(self.game.assets.music_mmClosing,loops=1)
        titleString = "MOONLIGHT MADNESS TOTAL"
        titleLine = dmd.TextLayer(128/2, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(titleString)
        points = self.moonlightTotal
        scoreString = ep.format_score(points)
        scoreLine = dmd.TextLayer(64, 9, self.game.assets.font_13px_thin_score, "center", opaque = False).set_text(scoreString)
        infoLine = dmd.TextLayer(64,24,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("NOW BACK TO THE GAME")
        self.layer = dmd.GroupedLayer(128,32,[titleLine,scoreLine,infoLine])
        # delay a bit before starting the real ball
        self.delay(delay=5,handler=self.finish_up)

    def enable_shots(self):
        # if there are shots to add, do that
        print "To Enable is: " + str(self.enable)
        if self.enable > 0:
            if len(self.availableShots) > 0:
                shot = random.choice(self.availableShots)
                # put it in the live shots
                print "Enabled Shot: " + str(shot)
                self.availableShots.remove(shot)
                print "Available: "
                print self.availableShots
                self.liveShots.append(shot)
                print "Live:"
                print self.liveShots
                # tick off the enabled shot - try to stay above zero
                if self.enable > 0:
                    self.enable -= 1
                    print "Shots left to enable: " + str(self.enable)
                    if self.enable > 0:
                        self.enable_shots()
                    else:
                        # refresh the lights
                        self.refresh_lights()
                else:
                # all shots enabled! Kick into bonanza
                    print "No Shots available to Enable"
                if len(self.availableShots) == 0:
                    self.start_bonanza()

    def switch_hit(self,theSwitch=9):
        if theSwitch > 8:
            # this is for non important switches
            pass
        elif theSwitch in self.liveShots:
            # it's live, that's a hit
            self.liveShots.remove(theSwitch)
            self.availableShots.append(theSwitch)
            self.game.sound.play(self.game.assets.sfx_ricochetSet)
            # kill the lights for that switch
            for lamp in self.lampList[theSwitch]:
                lamp.disable()
            # score points
            self.moonlightTotal += 1000000
            self.game.increase_tracking('moonlightTotal',1000000)
            # enable more shots
            print "Enabling 2 more shots"
            self.enable += 2
            self.enable_shots()
        else:
            # if it's not active, just pass
            pass

    def bonanza_hit(self,display=True):
        # this is a hit during the mayhem
        # score 3 mil
        self.moonlightTotal += 3000000
        self.game.increase_tracking('moonlightTotal',3000000)
        # show a random banner display
        if display:
            boom = random.choice(self.booms)
            self.game.sound.play(boom)
            self.cancel_delayed("Display")
            banner = random.choice(self.banners)
            self.layer = banner
            self.delay("Display",delay=0.6,handler=self.update_display)

    def start_bonanza(self):
        self.bonanza = True
        # start the crazy lightshow
        #self.game.lampctrl.play_show(self.game.assets.lamp_slowSparkle, repeat=True)
        self.game.schedule_lampshows([self.game.assets.lamp_slowSparkle],True)
        # turn on the GI
        self.game.gi_control("ON")
        # kick in the third stage music
        self.music_on(self.game.assets.music_mmMainLoopTwo)

    def refresh_lights(self):
        for item in self.liveShots:
            # for each lamp, schedule it to blink
            for lamp in self.lampList[item]:
                lamp.schedule(0x00FF00FF)

    def darken(self):
        # stop the lampshow
        self.game.lampctrl.stop_show()
        # kill all the lights
        self.game.lamp_control.disable_all_lamps()
        # disable the flippers
        self.game.gi_control("OFF")
        self.game.enable_flippers(False)

    def finish_up(self):
        # stop the music
        self.stop_music()
        # set the tracking so this player doesn't moonlight again
        self.game.set_tracking('moonlightStatus', True)
        # turn off the running flag
        self.running = False
        # turn on the GI just in case
        self.game.gi_control("ON")
        self.bonanza = False
        # unload the mode
        self.unload()

    # when the mode unloads, re-run ball starting
    def mode_stopped(self):
        self.game.ball_starting()
