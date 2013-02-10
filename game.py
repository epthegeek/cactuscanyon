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
##  __  __       _          ____
## |  \/  | __ _(_)_ __    / ___| __ _ _ __ ___   ___
## | |\/| |/ _` | | '_ \  | |  _ / _` | '_ ` _ \ / _ \
## | |  | | (_| | | | | | | |_| | (_| | | | | | |  __/
## |_|  |_|\__,_|_|_| |_|  \____|\__,_|_| |_| |_|\___|

#import logging
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from procgame import *
import cc_modes
import pinproc
import tracking
from assets import *
import ep
import pygame
import highscore
import time
import datetime
import os
import yaml
import copy

curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
## Define the config file locations
user_game_data_path = curr_file_path + "/config/game_data.yaml"
game_data_defaults_path = curr_file_path + "/config/game_data_template.yaml"
settings_defaults_path = curr_file_path + "/config/settings_template.yaml"
user_settings_path = curr_file_path + "/config/user_settings.yaml"

## Subclass BasicGame to create the main game
class CCGame(game.BasicGame):
    def __init__(self,machineType, fakePinProc = False):
        if (fakePinProc):
            self.fakePinProc = True
            config.values['pinproc_class'] = 'procgame.fakepinproc.FakePinPROC'
        else:
            self.fakePinProc = False
        self.restart = False
        # optional USB updater config settings
        self.usb_update = config.value_for_key_path(keypath='usb_update', default=False)
        if self.usb_update:
            self.usb_location = config.values['usb_location']
            self.game_location = config.values['game_location']
        # optional real knocker setting
        self.useKnocker = config.value_for_key_path(keypath='use_knocker', default=False)
        if self.useKnocker:
            print "Knocker Config Found!"
        # used to prevent the high score entry from restarting the music
        self.soundIntro = False
        self.shutdownFlag = config.value_for_key_path(keypath='shutdown_flag',default=False)
        self.buttonShutdown = config.value_for_key_path(keypath='power_button_combo', default=False)
        self.moonlightFlag = False

        super(CCGame, self).__init__(machineType)
        self.load_config('cc_machine.yaml')

    def setup(self):
        # Instead of resetting everything here as well as when a user
        # initiated reset occurs, do everything in self.reset() and call it
        # now and during a user initiated reset.
        ## This resets the color mapping so my 1 value pixels are black - even on composite - HUGE WIN!
        self.proc.set_dmd_color_mapping([0,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

        self.reset()

    def reset(self):
        # run the reset from proc.game.BasicGame
        #super(CCGame,self).reset()
        # game reset stuff - copied in
        """Reset the game state as a slam tilt might."""
        self.ball = 0
        self.old_players = []
        self.old_players = self.players[:]
        self.players = []
        self.current_player_index = 0
        self.modes.modes = []

        # basic game reset stuff, copied in

        ## init the sound
        self.sound = sound.SoundController(self)
        self.lampctrl = lamps.LampController(self)
        self.assets = Assets(self)
        self.current_music = self.assets.music_mainTheme

        # reset score display to mine
        self.score_display = cc_modes.ScoreDisplay(self,0)

        self.showcase = ep.EP_Showcase(self)

        # last switch variable for tracking
        self.lastSwitch = None
        # last ramp for combo tracking
        self.lastRamp = None

        self.ballStarting = False
        self.status = None
        # gi lamps set
        self.giLamps = [self.lamps.gi01,
                        self.lamps.gi02,
                        self.lamps.gi03]
        self.squelched = False
        # polly mode variable
        self.peril = False
        # status display ok ornot
        self.statusOK = False
        self.endBusy = False

        """docstring for setup"""
        # load up the game data Game data
        print "Loading game data"
        self.load_game_data(game_data_defaults_path, user_game_data_path)
        # and settings Game settings
        print "Loading game settings"
        self.load_settings(settings_defaults_path, user_settings_path)

        # set the volume per the settings
        self.sound.music_offset = self.user_settings['Sound']['Music volume offset']
        print "Setting initial offset: " + str(self.sound.music_offset)
        self.volume_to_set = (self.user_settings['Sound']['Initial volume'] / 10.0)
        print "Setting initial volume: " + str(self.volume_to_set)
        self.sound.set_volume(self.volume_to_set)
        self.previousVolume = self.volume_to_set

        self.immediateRestart = "Enabled" == self.user_settings['Gameplay (Feature)']['Immediate Restart After Game']

        # Set the balls per game per the user settings
        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']
        # Flipper pulse strength
        self.flipperPulse = self.user_settings['Machine (Standard)']['Flipper Pulse']
        # Moonlight window
        self.moonlightMinutes = self.user_settings['Gameplay (Feature)']['Moonlight Mins to Midnight']

        # set up the ball search
        self.setup_ball_search()

        # set up the trough mode
        trough_switchnames = ['troughBallOne', 'troughBallTwo', 'troughBallThree', 'troughBallFour']
        early_save_switchnames = ['rightOutlane', 'leftOutlane']
        self.trough = cc_modes.Trough(self, trough_switchnames,'troughBallOne','troughEject', early_save_switchnames, 'shooterLane', self.ball_drained)
        # set up ball save
#        self.ball_save = modes.BallSave(self, self.lamps.shootAgain, 'shooterLane')
        # set the ball save callback
        self.trough.ball_save_callback = self.ball_saved

        # High Score stuff
        self.highscore_categories = []

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'MarshallHighScoreData'
        cat.titles = ['Marshall Pinball 1','Marshall Pinball 2','Marshall Pinball 3']
        cat.score_for_player = lambda player: self.show_tracking('marshallBest')
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'LastCallHighScoreData'
        cat.titles = ['Last Call Champ']
        cat.score_for_player = lambda player: self.show_tracking('lastCallTotal')
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'QuickdrawChampHighScoreData'
        cat.titles = ['Quickdraw Champ']
        cat.score_for_player = lambda player: self.show_tracking('quickdrawsWon')
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ShowdownChampHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('showdownTotal')
        cat.titles = ['Showdown Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'AmbushChampHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('ambushTotal')
        cat.titles = ['Ambush Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'TownDrunkHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('beerMugHitsTotal')
        cat.titles = ['Town Drunk']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'TumbleweedChampHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('tumbleweedHitsTotal')
        cat.titles = ['Tumbleweed Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'UndertakerHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('kills')
        cat.titles = ['Undertaker']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'BountyHunterHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('bartsDefeatedTotal')
        cat.titles = ['Bounty Hunter']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'MotherlodeChampHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('motherlodeValue')
        cat.titles = ['Motherlode Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ComboChampHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('bigChain')
        cat.titles = ['Combo Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'MoonlightHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('moonlightTotal')
        cat.titles = ['Moonlight Champ']
        self.highscore_categories.append(cat)

        for category in self.highscore_categories:
            category.load_from_game(self)

        # Create the objects for the basic modes
        self.lamp_control = cc_modes.LampControl(game=self,priority=4)
        self.base = cc_modes.BaseGameMode(game=self,priority=4)
        self.attract_mode = cc_modes.Attract(game=self,priority=5)
        self.train = cc_modes.Train(game=self,priority=6)
        self.mountain = cc_modes.Mountain(game=self,priority = 7)
        self.badge = cc_modes.Badge(game=self,priority = 7)
        # the gun modes
        self.quickdraw = cc_modes.Quickdraw(game=self,priority=9)
        self.gunfight = cc_modes.Gunfight(game=self,priority=9)
        # basic ramp & loop handling
        self.right_ramp = cc_modes.RightRamp(game=self,priority=10)
        self.left_ramp = cc_modes.LeftRamp(game=self,priority=10)
        self.center_ramp = cc_modes.CenterRamp(game=self,priority=10)
        self.left_loop = cc_modes.LeftLoop(game=self,priority=10)
        self.right_loop = cc_modes.RightLoop(game=self,priority=10)
        # this is the layer that prevents basic ramp/loop shots from registering
        self.switch_block = cc_modes.SwitchBlock(game=self,priority=11)
        # combos should always register - so they ride above the switch block
        self.combos = cc_modes.Combos(game=self,priority=14)

        # save polly modes
        self.save_polly = cc_modes.SavePolly(game=self,priority=15)
        self.river_chase = cc_modes.RiverChase(game=self,priority=15)
        self.bank_robbery = cc_modes.BankRobbery(game=self,priority=15)
        # drunk multiball
        self.drunk_multiball = cc_modes.DrunkMultiball(game=self,priority=16)

        self.bonus_lanes = cc_modes.BonusLanes(game=self,priority=17)

        self.match = cc_modes.Match(game=self,priority=20)

        # mine and saloon have to stay high so they can interrupt other displays
        self.mine = cc_modes.Mine(game=self,priority=24)
        self.saloon = cc_modes.Saloon(game=self,priority=25)
        self.bart = cc_modes.Bart(game=self,priority=25)


        # general bad guy handling
        self.bad_guys = cc_modes.BadGuys(game=self,priority=67)
        # stampede multiball
        self.stampede = cc_modes.Stampede(game=self,priority=69)
        # this mode unloads when not in use
        self.skill_shot = cc_modes.SkillShot(game=self,priority=70)
        # gold mine multiball
        self.gm_multiball = cc_modes.GoldMine(game=self,priority=75)
        # the mob gun modes so they ride in front of most things
        self.showdown = cc_modes.Showdown(game=self,priority=80)
        self.ambush = cc_modes.Ambush(game=self,priority=80)

        # cva
        self.cva = cc_modes.CvA(game=self,priority=85)
        # marhsall multiball
        self.marshall_multiball = cc_modes.MarshallMultiball(game=self,priority=85)
        # bionic bart
        self.bionic = cc_modes.BionicBart(game=self,priority=90)
        # High Noon
        self.high_noon = cc_modes.HighNoon(game=self,priority=90)
        # move your train
        self.move_your_train = cc_modes.MoveYourTrain(game=self,priority=90)
        # last call
        self.last_call = cc_modes.LastCall(game=self,priority=90)
        # skillshot switch filter
        self.super_filter = cc_modes.SuperFilter(game=self,priority = 200)
        # Interrupter Jones
        self.interrupter = cc_modes.Interrupter(game=self,priority=200)
        # Switch Hit Tracker
        # moonlight madness
        self.moonlight = cc_modes.Moonlight(game=self,priority=200)
        self.switch_tracker = cc_modes.SwitchTracker(game=self,priority=201)

        ## try adding the score display font override
        #self.score_display.font_18x12 = self.assets.font_score_x12

        # Setup and instantiate service mode
        self.service_mode = ep.ep_service.ServiceMode(self,100,self.assets.font_tiny7,[])

        # set up an array of the modes
        self.ep_modes = [self.base,
                         self.attract_mode,
                         self.right_ramp,
                         self.right_loop,
                         self.center_ramp,
                         self.left_loop,
                         self.left_ramp,
                         self.saloon,
                         self.mine,
                         self.bad_guys,
                         self.save_polly,
                         self.skill_shot,
                         self.gm_multiball,
                         self.interrupter,
                         self.bonus_lanes,
                         self.stampede,
                         self.high_noon,
                         self.drunk_multiball,
                         self.quickdraw,
                         self.showdown,
                         self.ambush,
                         self.gunfight,
                         self.badge,
                         self.bionic,
                         self.bart,
                         self.move_your_train,
                         self.bank_robbery,
                         self.river_chase,
                         self.cva,
                         self.switch_block,
                         self.marshall_multiball,
                         self.moonlight]

        self.mode_list = [self.ambush,
                          self.attract_mode,
                          self.bad_guys,
                          self.badge,
                          self.ball_search,
                          self.bank_robbery,
                          self.bart,
                          self.base,
                          self.bionic,
                          self.bonus_lanes,
                          self.center_ramp,
                          self.combos,
                          self.cva,
                          self.drunk_multiball,
                          self.gm_multiball,
                          self.gunfight,
                          self.high_noon,
                          self.interrupter,
                          self.lamp_control,
                          self.last_call,
                          self.left_loop,
                          self.left_ramp,
                          self.marshall_multiball,
                          self.match,
                          self.mine,
                          self.moonlight,
                          self.mountain,
                          self.move_your_train,
                          self.quickdraw,
                          self.right_loop,
                          self.right_ramp,
                          self.river_chase,
                          self.saloon,
                          self.save_polly,
                          self.score_display,
                          self.showdown,
                          self.skill_shot,
                          self.stampede,
                          self.super_filter,
                          self.switch_block,
                          self.switch_tracker,
                          self.train,
                          self.trough]

        self.ep_modes.sort(lambda x, y: y.priority - x.priority)

        # Add in the modes that are active at start
        self.modes.add(self.lamp_control)
        self.modes.add(self.trough)
#        self.modes.add(self.ball_save)
        self.modes.add(self.ball_search)
        self.modes.add(self.attract_mode)
        self.modes.add(self.train)
        self.modes.add(self.mountain)
        self.modes.add(self.badge)
        self.modes.add(self.interrupter)
        self.modes.add(self.switch_tracker)
        self.modes.add(self.score_display)

    def start_game(self,forceMoonlight=False):
        # Check the time
        now = datetime.datetime.now()
        print "Hour: " + str(now.hour) + " Minutes: " + str(now.minute)
        # subtract the window minutes from 60
        window = 60 - self.moonlightMinutes
        print "Moonlight window time: " + str(window)
        # check for moonlight - always works at straight up midnight
        if now.hour == 0 & now.minute == 0:
            self.moonlightFlag = True
        # If not exactly midnight - check to see if we're within the time window
        elif now.hour == 23 & now.minute >= window:
            self.moonlightFlag = True
        # if force was passed - start it no matter what
        elif forceMoonlight:
            self.moonlightFlag = True
        else:
            self.moonlightFlag = False

        # remove the attract mode
        self.modes.remove(self.attract_mode)
        # kill the attract mode song fade delay just in case
        self.interrupter.cancel_delayed("Attract Fade")
        # tick up the audits
        self.game_data['Audits']['Games Started'] += 1
        # tick up all the switch hit tracking by one
        for switch in self.game_data['SwitchHits']:
            self.game_data['SwitchHits'][switch] +=1
            print switch + " " + str(self.game_data['SwitchHits'][switch])
        # turn off all the ligths
        for lamp in self.lamps:
            if 'gi' not in lamp.name:
                lamp.disable()
        # run the start ball from parent
        super(CCGame,self).start_game()
        # Add the first player
        self.add_player()
        self.order_mobs()
        # reset the music volume
        self.sound.set_volume(self.volume_to_set)
        # load the base game mode
        self.modes.add(self.base)
        # Start the ball.  This includes ejecting a ball from the trough.
        self.start_ball()
        # add the ability to see the status
        self.statusOK = True

    def start_ball(self):
        # reset the autoplunger count
        self.trough.balls_to_autoplunge = 0
        # run the start_ball from proc.game.BasicGame
        super(CCGame, self).start_ball()

    def create_player(self,name):
        # create an object wiht the Tracking Class - subclassed off game.Player
        return tracking.Tracking(name)

    def game_started(self):
        self.log("GAME STARTED")
        # run the game_started from proc.game.BasicGame
        super(CCGame, self).game_started()
        # Don't start_ball() here, since Attract does that after calling start_game().

    def shoot_again(self):
        self.interrupter.shoot_again()

    def ball_starting(self):
        # restore music, just in case
        self.restore_music()
        print "BALL STARTING - number " + str(self.ball)
        ## run the ball_starting from proc.gameBasicGame
        super(CCGame, self).ball_starting()
        self.ballStarting = True
        # turn on the GI
        self.gi_control("ON")
        # set peril (polly indicator) to false
        self.peril = False
        # reset the pop bumper count
        self.set_tracking('bumperHits',0)
        # reset the player bonus
        self.set_tracking('bonus', 0)
        # reset the train just in case - type 2, should only back the train up if it's out
        self.train.stop_at = 0
        self.train.reset_toy(step=2)
        # enable the ball search
        self.ball_search.enable()
        # turn the flippers on
        self.enable_flippers(True)
        # reset the tilt status
        self.set_tracking('tiltStatus',0)
        # reset the stack levels
        for i in range(0,7,1):
            self.set_tracking('stackLevel',False,i)

        # divert here if moonlight madness should run for this player
        #self.moonlightFlag = True
        if self.moonlightFlag and self.show_tracking('moonlightStatus') == False:
            self.modes.add(self.moonlight)
        else:
            # launch a ball, unless there is one in the shooter lane already
            if not self.switches.shooterLane.is_active():
                self.trough.launch_balls(1) # eject a ball into the shooter lane
            else:
                self.trough.num_balls_in_play += 1

            # if skillshot is already running for some lame reason, remove it
            if self.skill_shot in self.modes:
                self.modes.remove(self.skill_shot)
            # add teh skill shot.
            self.modes.add(self.skill_shot)
            # and all the other modes
            print "CHECKING TRACKING Ball start LR: " + str(self.show_tracking('leftRampStage'))
            self.base.load_modes()
            # if we're under 2 minutes and on the last ball, enable BOZO BALL (tm)
            if self.current_player().game_time < 120 and self.ball == self.balls_per_game:
                self.base.enable_bozo_ball()
            # update the lamps
            self.lamp_control.update()

    def ball_saved(self):
        if self.trough.ball_save_active:
            # tell interrupter jones to show the ball save
            print "GAME THINKS THE BALL WAS SAVED"
            # the ball saved display
            self.interrupter.ball_saved()
            # kill the skillshot if it's running
            if self.skill_shot in self.modes:
                self.modes.remove(self.skill_shot)
            # if the ball was saved, we need a new one
            #self.trough.launch_balls(1)

    # Empty callback just incase a ball drains into the trough before another
     # drain_callback can be installed by a gameplay mode.
    def ball_drained(self):
        print "BALL DRAINED ROUTINE RUNNING"
        # if we're not ejecting a new ball, then it really drained
        if not self.trough.launch_in_progress:
            # New abort for Last Call
            if self.last_call in self.modes:
                self.last_call.ball_drained()
                return
            if self.moonlight.running:
                self.moonlight.ball_drained()
                return
            # Tell every mode a ball has drained by calling the ball_drained function if it exists
            if self.trough.num_balls_in_play == 0:
                # kill all the display layers
                for mode in self.ep_modes:
                    if getattr(mode, "clear_layer", None):
                        mode.clear_layer()
                print "BALL DRAINED IS KILLING THE MUSIC"
                self.sound.stop_music()

            ## and tell all the modes the ball drained no matter what
            for mode in self.modes:
                if getattr(mode, "ball_drained", None):
                    mode.ball_drained()

    def ball_ended(self):
        """Called by end_ball(), which is itself called by base.trough_changed."""
        self.log("BALL ENDED")
        # reset the tilt
        self.set_tracking('tiltStatus',0)
        # stop the music
        print "BALL ENDED IS KILLING THE MUSIC"
        # disable ball save
        self.trough.disable_ball_save()

        self.sound.stop_music()
        # unload the base add on modes
        self.base.remove_modes()

        #self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        self.game_data['Audits']['Balls Played'] += 1

        print "CHECKING TRACKING ball ended LR: " + str(self.show_tracking('leftRampStage'))

        # then call the ball_ended from proc.game.BasicGame
        # Looping here? wha?
        self.end_ball()


    def end_ball(self):
        """Called by the implementor to notify the game that the current ball has ended."""

        self.ball_end_time = time.time()
        # Calculate ball time and save it because the start time
        # gets overwritten when the next ball starts.
        self.ball_time = self.get_ball_time()
        self.current_player().game_time += self.ball_time

        if self.current_player().extra_balls > 0:
            self.current_player().extra_balls -= 1
            #set the ball starting flag to help the trough not be SO STUPID
            self.ballStarting = True
            print "Starting extra ball - remaining extra balls:" + str(self.current_player().extra_balls)
            self.shoot_again()
            return
        if self.current_player_index + 1 == len(self.players):
            self.ball += 1
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        if self.ball > self.balls_per_game:
            self.end_game()
        else:
            self.start_ball() # Consider: Do we want to call this here, or should it be called by the game? (for bonus sequence)

    def game_reset(self):
        print("RESETTING GAME")
        # unload all the base modes, just in case
        self.base.remove_modes()
        # unload all the base mode
        self.modes.remove(self.base)
        # and the skillshot
        self.modes.remove(self.skill_shot)
        # throw up a message about restarting
        self.interrupter.restarting()
        # lot the end of the game
        self.log("GAME PREMATURELY ENDED")
        # set the Balls in play to 0
        self.trough.num_balls_in_play = 0
        # restart the game
        self.start_game()


    def game_ended(self):
        self.log("GAME ENDED")
        # kill the moonlight flag
        self.moonlightFlag = False
        ## call the game_ended from proc.game.BasicGame
        super(CCGame, self).game_ended()

        # remove the base game mode
        # self.modes.remove(self.base)
        # turn the flippers off
        self.enable_flippers(enable=False)

        # divert to the match before high score entry - unless last call is disabled
        lastCall = 'Enabled' == self.user_settings['Gameplay (Feature)']['Last Call Mode']
        if lastCall:
            self.modes.add(self.match)
            self.match.run_match()
        else:
            self.run_highscore()

    def run_highscore(self):
        # Remove the base mode here now instead - so that it's still available for last call
        self.modes.remove(self.base)

        ## TODO need to add some crap here to see if there's a high score to enter - and play the lead in
        # High Score Stuff
        self.seq_manager = highscore.EntrySequenceManager(game=self, priority=2)
        self.seq_manager.finished_handler = self.highscore_entry_finished
        self.seq_manager.logic = highscore.CategoryLogic(game=self, categories=self.highscore_categories)
        self.seq_manager.ready_handler = self.highscore_entry_ready_to_prompt
        self.modes.add(self.seq_manager)

    def highscore_entry_ready_to_prompt(self, mode, prompt):
        banner_mode = game.Mode(game=self, priority=8)
        textLine1 = "GREAT JOB"
        textLine2 = (prompt.left.upper())
        textLayer1 = dmd.TextLayer(58, 5, self.assets.font_10px_AZ, "center", opaque=False).set_text(textLine1)
        textLayer1.composite_op = "blacksrc"
        textLayer2 = dmd.TextLayer(58, 18, self.assets.font_10px_AZ, "center", opaque=False).set_text(textLine2)
        textLayer2.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2])
        banner_mode.layer = dmd.ScriptedLayer(width=128, height=32, script=[{'seconds':2.0, 'layer':combined}])
        banner_mode.layer.on_complete = lambda: self.highscore_banner_complete(banner_mode=banner_mode, highscore_entry_mode=mode)
        self.modes.add(banner_mode)
        # play the music - if it hasn't started yet
        if not self.soundIntro:
            self.soundIntro = True
            duration = self.sound.play(self.assets.music_highScoreLead)
            self.interrupter.delayed_music_on(wait=duration,song=self.assets.music_goldmineMultiball)

    def highscore_banner_complete(self, banner_mode, highscore_entry_mode):
        self.modes.remove(banner_mode)
        highscore_entry_mode.prompt()

    def highscore_entry_finished(self, mode):
        self.modes.remove(mode)
        # Stop the music
        self.sound.stop_music()
        # turn off the sound intro flag
        self.soundIntro = False
        # set a busy flag so that the start button won't restart the game right away
        if not self.immediateRestart:
            print "Immediate restart is disabled, killing start button"
            self.endBusy = True
        else:
            print "Immediate restart is enabled"
        # re-add the attract mode
        self.modes.add(self.attract_mode)
        # play a quote
        duration = self.sound.play(self.assets.quote_goodbye)
        # tally up the some audit data
        # Handle stats for last ball here
        #self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        self.game_data['Audits']['Balls Played'] += 1
        # Also handle game stats.
        for i in range(0,len(self.players)):
            game_time = self.get_game_time(i)
            #self.game_data['Audits']['Avg Game Time'] = self.calc_time_average_string( self.game_data['Audits']['Games Played'], self.game_data['Audits']['Avg Game Time'], game_time)
            self.game_data['Audits']['Games Played'] += 1
        # save the game data
        self.save_game_data()

        # play the closing song
        self.interrupter.closing_song(duration)

    def save_game_data(self):
        super(CCGame, self).save_game_data(user_game_data_path)

    def setup_ball_search(self):
        # No special handlers in starter game.
        special_handler_modes = []
        self.ball_search = cc_modes.BallSearch(self, priority=100,countdown_time=15, coils=self.ballsearch_coils,reset_switches=self.ballsearch_resetSwitches,stop_switches=self.ballsearch_stopSwitches,special_handler_modes=special_handler_modes)

    def schedule_lampshows(self,lampshows,repeat=True):
        self.scheduled_lampshows = lampshows
        self.scheduled_lampshows_repeat = repeat
        self.scheduled_lampshow_index = 0
        self.start_lampshow()

    def start_lampshow(self):
        self.lampctrl.play_show(self.scheduled_lampshows[self.scheduled_lampshow_index], False, self.lampshow_ended)

    def lampshow_ended(self):
            self.scheduled_lampshow_index = self.scheduled_lampshow_index + 1
            if self.scheduled_lampshow_index == len(self.scheduled_lampshows):
                if self.scheduled_lampshows_repeat:
                    self.scheduled_lampshow_index = 0
                    self.start_lampshow()
                else:
                    # Finished playing the lampshows and not repeating...
                    pass
            else:
                self.start_lampshow()

    def set_status(self,derp):
        self.status = derp

    ###  _____               _    _
    ### |_   _| __ __ _  ___| | _(_)_ __   __ _
    ###   | || '__/ _` |/ __| |/ / | '_ \ / _` |
    ###   | || | | (_| | (__|   <| | | | | (_| |
    ###   |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
    ###                                   |___/
    ### Player stats and progress tracking

    def set_tracking(self,item,amount,key="foo"):
        p = self.current_player()
        if key != "foo":
            p.player_stats[item][key] = amount
        else:
            p.player_stats[item] = amount

    # call from other modes to set a value
    def increase_tracking(self,item,amount=1,key="foo"):
        ## tick up a stat by a declared amount
        p = self.current_player()
        if key != "foo":
            p.player_stats[item][key] += amount
            return p.player_stats[item][key]
        else:
            p.player_stats[item] += amount
            # send back the new value for use
            return p.player_stats[item]

     # call from other modes to set a value
    def decrease_tracking(self,item,amount=1,key="foo"):
        ## tick up a stat by a declared amount
        p = self.current_player()
        if key != "foo":
            p.player_stats[item][key] -= amount
            return p.player_stats[item][key]
        else:
            p.player_stats[item] -= amount
            # send back the new value for use
            return p.player_stats[item]

    # return values to wherever
    def show_tracking(self,item,key="foo"):
      p = self.current_player()
      if key != "foo":
            return p.player_stats[item][key]
      else:
            return p.player_stats[item]

    # invert tracking only used for bonus lanes, wise? dunno
    def invert_tracking(self,item):
        p = self.current_player()
        p.player_stats[item].reverse()

    def stack_level(self,level,value,lamps=True):
        # just a routine for setting the stack level
        self.set_tracking('stackLevel',value,level)
        # that also calls a base lamp update
        if lamps:
            print "Stack set updating the lamps"
            self.lamp_control.update()
        else:
            print "Stack set not updating thh lamps"

    # score with bonus
    def score_with_bonus(self, points,percent=7):
        """Convenience method to add *points* to the current player."""
        p = self.current_player()
        p.score += points
        # divide the score by 100 to get what 1 % is (rounded), then multiply by the applied percent, then round to an even 10.
        # why? because that's what modern pinball does. Score always ends in 0
        bonus = points / 100 * percent / 10 * 10
        #print "ADDING BONUS - " + str(bonus)
        p.player_stats['bonus'] += bonus

    ## bonus stuff

    # extra method for adding bonus to make it shorter when used
    def add_bonus(self,points):
        p = self.current_player()
        p.player_stats['bonus'] += points
        print p.player_stats['bonus']

    def calc_time_average_string(self, prev_total, prev_x, new_value):
        prev_time_list = prev_x.split(':')
        prev_time = (int(prev_time_list[0]) * 60) + int(prev_time_list[1])
        avg_game_time = int((int(prev_total) * int(prev_time)) + int(new_value)) / (int(prev_total) + 1)
        avg_game_time_min = avg_game_time/60
        avg_game_time_sec = str(avg_game_time%60)
        if len(avg_game_time_sec) == 1:
            avg_game_time_sec = '0' + avg_game_time_sec

        return_str = str(avg_game_time_min) + ':' + avg_game_time_sec
        return return_str

    def calc_number_average(self, prev_total, prev_x, new_value):
        avg_game_time = int((prev_total * prev_x) + new_value) / (prev_total + 1)
        return int(avg_game_time)


    def save_settings(self):
        super(CCGame,self).save_settings(user_settings_path)

    ### Standard flippers
    def enable_flippers(self, enable):
        """Enables or disables the flippers AND bumpers."""

        for flipper in self.config['PRFlippers']:
            self.logger.info("Programming flipper %s", flipper)
            main_coil = self.coils[flipper+'Main']
            self.logger.info("Enabling WPC style flipper")
            hold_coil = self.coils[flipper+'Hold']
            switch_num = self.switches[flipper].number

            drivers = []
            if enable:
                drivers += [pinproc.driver_state_pulse(main_coil.state(), self.flipperPulse)]
                drivers += [pinproc.driver_state_pulse(hold_coil.state(), 0)]
            self.proc.switch_update_rule(switch_num, 'closed_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            drivers = []
            if enable:
                drivers += [pinproc.driver_state_disable(main_coil.state())]
                drivers += [pinproc.driver_state_disable(hold_coil.state())]

            self.proc.switch_update_rule(switch_num, 'open_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            if not enable:
                main_coil.disable()
                hold_coil.disable()

        self.enable_bumpers(enable)

    ### Flipper inversion

    def enable_inverted_flippers(self, enable):
        """Enables or disables the flippers AND bumpers."""

        print "ENABLE INVERTED FLIPPERS, YO"
        for flipper in self.config['PRFlippers']:

            ## add the invert value
            if flipper == 'flipperLwL':
                inverted = 'flipperLwR'
            if flipper == 'flipperLwR':
                inverted = 'flipperLwL'

            self.logger.info("Programming inverted flipper %s", flipper)
            main_coil = self.coils[inverted+'Main']
            self.logger.info("Enabling WPC style flipper")
            hold_coil = self.coils[inverted+'Hold']
            switch_num = self.switches[flipper].number

            drivers = []
            if enable:
                drivers += [pinproc.driver_state_pulse(main_coil.state(), self.flipperPulse)]
                drivers += [pinproc.driver_state_pulse(hold_coil.state(), 0)]
            self.proc.switch_update_rule(switch_num, 'closed_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            drivers = []
            if enable:
                drivers += [pinproc.driver_state_disable(main_coil.state())]
                drivers += [pinproc.driver_state_disable(hold_coil.state())]

            self.proc.switch_update_rule(switch_num, 'open_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            if not enable:
                main_coil.disable()
                hold_coil.disable()

        self.enable_bumpers(enable)

    ## GI LAMPS

    def gi_control(self,state):
        if state == "OFF":
            self.giState = "OFF"
            for lamp in self.giLamps:
                lamp.disable()
        else:
            self.giState = "ON"
            for lamp in self.giLamps:
                lamp.enable()


    def lightning(self,section):
        # set which section of the GI to flash
        if section == 'top':
            lamp = self.giLamps[0]
        elif section == 'right':
            lamp = self.giLamps[1]
        elif section == 'left':
            lamp = self.giLamps[2]
        else:
            pass
        # then flash it
        lamp.pulse(216)

    # controls for music volume

    def squelch_music(self):
        if not self.squelched:
            self.squelched = True
            self.previousVolume = pygame.mixer.music.get_volume()
            volume = self.previousVolume / 6
            pygame.mixer.music.set_volume(volume)

    def restore_music(self):
        if self.squelched:
            self.squelched = False
            pygame.mixer.music.set_volume(self.previousVolume)

    def music_on(self,song=None,caller="Not Specified",slice=0,execute=True):
    # if given a slice number to check - do that
        if slice != 0:
            stackLevel = self.show_tracking('stackLevel')
            # if there are balls in play and nothing active above the set slice, then kill the music
            if True not in stackLevel[slice:] and self.trough.num_balls_in_play != 0:
                pass
            else:
                print "Music stop called by " + str(caller) + " But passed - Busy"
                execute = False

        if execute:
            # if a song is passed, set that to the active song
            if song:
                print str(caller) + " changed song to " + str(song)
                self.current_music = song
            # if not, just re-activate the current
            else:
                print str(caller) + " restarting current song"
                # then start it up
            self.sound.play_music(self.current_music, loops=-1)


    # switch blocker load and unload - checks to be sure if it should do what it is told
    def switch_blocker(self,function,caller):
        if function == 'add':
            print "Switch Blocker Add Call from " + str(caller)
            if self.switch_block not in self.modes:
                print "Switch Blocker Added"
                self.modes.add(self.switch_block)
            else:
                print "Switch Blocker Already Present"
        elif function == 'remove':
            print "Switch Blocker Remove Call from " + str(caller)
            stackLevel = self.show_tracking('stackLevel')
            if True not in stackLevel[2:]:
                print "Switch Blocker Removed"
                self.modes.remove(self.switch_block)
            else:
                print "Switch Blocker NOT removed due to stack level"
                pass

    def volume_up(self):
        """ """
        if not self.sound.enabled: return
        #print "Current Volume: " + str(self.sound.volume)
        setting = self.user_settings['Sound']['Initial volume']
        if setting <= 9:
            setting += 1
            #print "new math value: " + str(self.sound.volume)
            self.sound.set_volume(setting / 10.0)
            #print "10 value: " + str(self.sound.volume*10)
            #print "Int value: " + str(int(self.sound.volume*10))
        return setting

    def volume_down(self):
        """ """
        if not self.sound.enabled: return
        #print "Current Volume: " + str(self.sound.volume)
        setting = self.user_settings['Sound']['Initial volume']
        if setting >= 2:
            setting -= 1
            #print "new math value: " + str(self.sound.volume)
            self.sound.set_volume(setting / 10.0)
            #print "10 value: " + str(self.sound.volume*10)
            #print "Int value: " + str(int(self.sound.volume*10))
        return setting


    def order_mobs(self):
        # set which mob mode comes first
        mobSetting = "Ambush" == self.user_settings['Gameplay (Feature)']['Ambush or Showdown First']
        if mobSetting:
            print "User settings put Ambush first - adjusting for player"
            self.set_tracking('ambushStatus',"OPEN")
            self.set_tracking('showdownStatus',"OVER")


    def load_settings(self, template_filename, user_filename):
        """Loads the YAML game settings configuration file.  The game settings
       describe operator configuration options, such as balls per game and
       replay levels.
       The *template_filename* provides default values for the game;
       *user_filename* contains the values set by the user.

       See also: :meth:`save_settings`
       """
        self.user_settings = {}
        self.settings = yaml.load(open(template_filename, 'r'))
        if os.path.exists(user_filename):
            self.user_settings = yaml.load(open(user_filename, 'r'))
            # check that we got something
            if self.user_settings:
                print "Found settings. All good"
            else:
                print "Settings broken, all bad, defaulting"
                self.user_settings = {}

        for section in self.settings:
            for item in self.settings[section]:
                if not section in self.user_settings:
                    self.user_settings[section] = {}
                    if 'default' in self.settings[section][item]:
                        self.user_settings[section][item] = self.settings[section][item]['default']
                    else:
                        self.user_settings[section][item] = self.settings[section][item]['options'][0]
                elif not item in self.user_settings[section]:
                    if 'default' in self.settings[section][item]:
                        self.user_settings[section][item] = self.settings[section][item]['default']
                    else:
                        self.user_settings[section][item] = self.settings[section][item]['options'][0]

    def load_game_data(self, template_filename, user_filename):
        """Loads the YAML game data configuration file.  This file contains
        transient information such as audits, high scores and other statistics.
        The *template_filename* provides default values for the game;
        *user_filename* contains the values set by the user.

        See also: :meth:`save_game_data`
        """
        self.game_data = {}
        template = yaml.load(open(template_filename, 'r'))
        if os.path.exists(user_filename):
            self.game_data = yaml.load(open(user_filename, 'r'))
            # check that we got something
            if self.game_data:
                print "Found settings. All good"
            else:
                print "Settings broken, all bad, defaulting"
                self.game_data = {}

        if template:
            for key, value in template.iteritems():
                if key not in self.game_data:
                       self.game_data[key] = copy.deepcopy(value)

