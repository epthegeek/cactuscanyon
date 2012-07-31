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
##  __  __       _          ____
## |  \/  | __ _(_)_ __    / ___| __ _ _ __ ___   ___
## | |\/| |/ _` | | '_ \  | |  _ / _` | '_ ` _ \ / _ \
## | |  | | (_| | | | | | | |_| | (_| | | | | | |  __/
## |_|  |_|\__,_|_|_| |_|  \____|\__,_|_| |_| |_|\___|

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from procgame import *
import cc_modes
import pinproc
import tracking
from assets import *
import ep
import pygame

## Define the config file locations
user_game_data_path = "config/game_data.yaml"
game_data_defaults_path = "config/game_data_template.yaml"
settings_defaults_path = "config/settings_template.yaml"
user_settings_path = "config/user_settings.yaml"

## Subclass BasicGame to create the main game
class CCGame(game.BasicGame):
    def __init__(self,machineType, fakePinProc = False):
        if (fakePinProc):
            config.values['pinproc_class'] = 'procgame.fakepinproc.FakePinPROC'
            self.fakePinProc = True
        else:
            self.fakePinProc = False

        super(CCGame, self).__init__(machineType)
        self.load_config('cc_machine.yaml')
        self.sound = sound.SoundController(self)
        self.lampctrl = lamps.LampController(self)
        self.assets = Assets(self)

        ## This resets the color mapping so my 1 value pixels are black - even on composite - HUGE WIN!
        self.proc.set_dmd_color_mapping([0,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

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
        self.previousVolume = 0


    def setup(self):
        """docstring for setup"""
        # load up the game data Game data
        self.load_game_data(game_data_defaults_path, user_game_data_path)
        # and settings Game settings
        self.load_settings(settings_defaults_path, user_settings_path)

        # Set the balls per game per the user settings
        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']

        # set up the ball search
        self.setup_ball_search()

        # set up the trough mode
        trough_switchnames = ['troughBallOne', 'troughBallTwo', 'troughBallThree', 'troughBallFour']
        early_save_switchnames = ['rightOutlane', 'leftOutlane']
        self.trough = cc_modes.Trough(self, trough_switchnames,'troughBallOne','troughEject', early_save_switchnames, 'shooterLane', self.ball_drained)
        # set up ball save
        self.ball_save = modes.BallSave(self, self.lamps.shootAgain, 'shooterLane')
        # this is what links the ball save to the trough.  I THINK.
        self.ball_save.trough_enable_ball_save = self.trough.enable_ball_save
        self.trough.num_balls_to_save = self.ball_save.get_num_balls_to_save
        # set the ball save callback
        self.trough.ball_save_callback = self.ball_saved
        self.trough.launch_callback = self.launch_callback

        # High Score stuff
        self.highscore_categories = []

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
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
        cat.score_for_player = lambda player: self.show_tracking('fullLoops')
        cat.titles = ['Tumbleweed Champ']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'UndertakerHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('kills')
        cat.titles = ['Undertaker']
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'BountyHunterHighScoreData'
        cat.score_for_player = lambda player: self.show_tracking('bartsDefeated')
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

        ## TODO later - and combo champ? ambush champ? ramp champ?

        for category in self.highscore_categories:
            category.load_from_game(self)


        # Instead of resetting everything here as well as when a user
        # initiated reset occurs, do everything in self.reset() and call it
        # now and during a user initiated reset.
        self.reset()

    def reset(self):
        # run the reset from proc.game.BasicGame
        super(CCGame,self).reset()

        # Create the objects for the basic modes
        self.base = cc_modes.BaseGameMode(game=self,priority=4)
        self.attract_mode = cc_modes.Attract(game=self,priority=5)
        self.train = cc_modes.Train(game=self,priority=6)
        self.mountain = cc_modes.Mountain(game=self,priority = 7)
        self.badge = cc_modes.Badge(game=self,priority = 7)

        self.combos = cc_modes.Combos(game=self,priority=9)
        self.right_ramp = cc_modes.RightRamp(game=self,priority=10)
        self.left_ramp = cc_modes.LeftRamp(game=self,priority=11)
        self.center_ramp = cc_modes.CenterRamp(game=self,priority=12)
        # save polly rides above the ramps, but below the loops
        self.save_polly = cc_modes.SavePolly(game=self,priority=13)
        self.left_loop = cc_modes.LeftLoop(game=self,priority=14)
        self.right_loop = cc_modes.RightLoop(game=self,priority=15)
        self.bonus_lanes = cc_modes.BonusLanes(game=self,priority=16)

        self.match = cc_modes.Match(game=self,priority=20)

        # mine and saloon have to stay high so they can interrupt other displays
        self.mine = cc_modes.Mine(game=self,priority=24)
        self.saloon = cc_modes.Saloon(game=self,priority=25)
        self.bart = cc_modes.Bart(game=self,priority=25)


        # Quickdraw battle and showdown
        self.bad_guys = cc_modes.BadGuys(game=self,priority=67)
        self.quickdraw = cc_modes.Quickdraw(game=self,priority=68)
        self.showdown = cc_modes.Showdown(game=self,priority=68)
        self.ambush = cc_modes.Ambush(game=self,priority=68)
        self.gunfight = cc_modes.Gunfight(game=self,priority=68)
        self.stampede = cc_modes.Stampede(game=self,priority=69)
        # this mode unloads when not in use
        self.skill_shot = cc_modes.SkillShot(game=self,priority=70)
        # gold mine multiball
        self.gm_multiball = cc_modes.GoldMine(game=self,priority=88)
        # drunk multiball
        self.drunk_multiball = cc_modes.DrunkMultiball(game=self,priority=88)
        # bionic bart
        self.bionic = cc_modes.BionicBart(game=self,priority=90)
        # High Noon
        self.high_noon = cc_modes.HighNoon(game=self,priority=90)
        # move your train
        self.move_your_train = cc_modes.MoveYourTrain(game=self,priority=90)
        # skillshot switch filter
        self.super_filter = cc_modes.SuperFilter(game=self,priority = 200)
        # Interrupter Jones
        self.interrupter = cc_modes.Interrupter(game=self,priority=200)

        ## try adding the score display font override
        self.score_display.font_18x12 = self.assets.font_score_x12

        # Setup and instantiate service mode
        self.service_mode = service.ServiceMode(self,100,self.assets.font_tiny7,[])

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
                         self.move_your_train]

        self.ep_modes.sort(lambda x, y: y.priority - x.priority)

        # Add in the modes that are active at start
        self.modes.add(self.trough)
        self.modes.add(self.ball_save)
        self.modes.add(self.ball_search)
        self.modes.add(self.attract_mode)
        self.modes.add(self.train)
        self.modes.add(self.mountain)
        self.modes.add(self.badge)
        self.modes.add(self.interrupter)

    def start_game(self):
        # remove the attract mode
        self.modes.remove(self.attract_mode)
        # tick up the audits
        self.game_data['Audits']['Games Started'] += 1
        # turn off all the ligths
        for lamp in self.lamps:
            lamp.disable()
        # run the start ball from parent
        super(CCGame,self).start_game()
        # Add the first player
        self.add_player()
        # load the base game mode
        self.modes.add(self.base)
        # Start the ball.  This includes ejecting a ball from the trough.
        self.start_ball()

    def start_ball(self):
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
        print "STARTING EXTRA BALL"
        self.interrupter.shoot_again()

    def ball_starting(self):
        print "BALL STARTING - number " + str(self.ball)
        ## run the ball_starting from proc.gameBasicGame
        super(CCGame, self).ball_starting()
        self.ballStarting = True
        # turn on the GI
        self.gi_control("ON")
        # launch a ball, unless there is one in the shooter lane already - but really, this shouldn't
        # happen because we're only starting if trough is full
        if not self.switches.shooterLane.is_active():
            self.trough.launch_balls(1) # eject a ball into the shooter lane
        else:
            self.trough.num_balls_in_play += 1

        # enable the ball search
        self.ball_search.enable()
        # turn the flippers on
        self.enable_flippers(True)
        # reset the tilt status
        self.set_tracking('tiltStatus',0)
        # reset the stack levels
        for i in range(0,4,1):
            self.set_tracking('stackLevel',False,i)
        # and load the skill shot
        self.modes.add(self.skill_shot)
        # and all the other modes
        print "CHECKING TRACKING Ball start LR: " + str(self.show_tracking('leftRampStage'))
        self.base.load_modes()
        # update the lamps
        self.update_lamps()

    def launch_callback(self):
        pass

    def ball_saved(self):
        if self.trough.ball_save_active:
            # tell interrupter jones to show the ball save
            print "GAME THINKS THE BALL WAS SAVED"
            self.interrupter.ball_saved()
            # kill the skillshot if it's running
            if self.skill_shot in self.modes:
                self.modes.remove(self.skill_shot)
            # if the ball was saved, we need a new one
            #self.trough.launch_balls(1)

    # Empty callback just incase a ball drains into the trough before another
     # drain_callback can be installed by a gameplay mode.
    def ball_drained(self):
        # if we're not ejecting a new ball, then it really drained
        if not self.trough.launch_in_progress:
            # Tell every mode a ball has drained by calling the ball_drained function if it exists
            if self.trough.num_balls_in_play == 0:
                # turn off the lights
                for lamp in self.lamps:
                    lamp.disable()
                # kill all the display layers
                for mode in self.ep_modes:
                    if getattr(mode, "clear_layer", None):
                        mode.clear_layer()
                print "BALL DRAINED IS KILLING THE MUSIC"
                self.sound.stop_music()

            ## and tell all the modes the ball drained no matter what
            for mode in self.ep_modes:
                if getattr(mode, "ball_drained", None):
                    mode.ball_drained()

    def ball_ended(self):
        """Called by end_ball(), which is itself called by base.trough_changed."""
        self.log("BALL ENDED")
        # reset the tilt
        self.set_tracking('tiltStatus',0)
        # stop the music
        print "BALL ENDED IS KILLING THE MUSIC"

        self.sound.stop_music()
        # unload the base add on modes
        self.base.remove_modes()

        #self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        self.game_data['Audits']['Balls Played'] += 1

        print "CHECKING TRACKING ball ended LR: " + str(self.show_tracking('leftRampStage'))

    # then call the ball_ended from proc.game.BasicGame
        self.end_ball()

    def game_ended(self):
        self.log("GAME ENDED")
        ## call the game_ended from proc.game.BasicGame
        super(CCGame, self).game_ended()

        # remove the base game mode
        self.modes.remove(self.base)

        # divert to the match before high score entry
        self.modes.add(self.match)
        self.match.run_match()

    def run_highscore(self):
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
        # play the music
        duration = self.sound.play(self.assets.music_highScoreLead)
        # follow up with the music
        self.interrupter.delayed_music_on(wait=duration,song=self.assets.music_goldmineMultiball)

    def highscore_banner_complete(self, banner_mode, highscore_entry_mode):
        self.modes.remove(banner_mode)
        highscore_entry_mode.prompt()

    def highscore_entry_finished(self, mode):
        self.modes.remove(mode)
        # Stop the music
        self.sound.stop_music()
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
        self.ball_search = cc_modes.BallSearch(self, priority=100,countdown_time=30, coils=self.ballsearch_coils,reset_switches=self.ballsearch_resetSwitches,stop_switches=self.ballsearch_stopSwitches,special_handler_modes=special_handler_modes)

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

    # score with bonus
    def score_with_bonus(self, points,percent=7):
        """Convenience method to add *points* to the current player."""
        p = self.current_player()
        p.score += points
        # divide the score by 100 to get what 1 % is (rounded), then multiply by the applied percent, then round to an even 10.
        # why? because that's what modern pinball does. Score always ends in 0
        bonus = points / 100 * percent / 10 * 10
        print "ADDING BONUS - " + str(bonus)
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
            if self.coils.has_key(inverted+'Hold'):
                style = 'wpc'
                self.logger.info("Enabling WPC style flipper")
                hold_coil = self.coils[inverted+'Hold']
            else:
                self.logger.info("Enabling Stern style flipper")
                style = 'stern'
            switch_num = self.switches[flipper].number

            drivers = []
            if enable:
                if style == 'wpc':
                    drivers += [pinproc.driver_state_pulse(main_coil.state(), main_coil.default_pulse_time)]
                    drivers += [pinproc.driver_state_pulse(hold_coil.state(), 0)]
                else:
                    drivers += [pinproc.driver_state_patter(main_coil.state(), 2, 18, main_coil.default_pulse_time, True)]
            self.proc.switch_update_rule(switch_num, 'closed_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            drivers = []
            if enable:
                drivers += [pinproc.driver_state_disable(main_coil.state())]
                if style == 'wpc':
                    drivers += [pinproc.driver_state_disable(hold_coil.state())]

            self.proc.switch_update_rule(switch_num, 'open_nondebounced', {'notifyHost':False, 'reloadActive':False}, drivers, len(drivers) > 0)

            if not enable:
                main_coil.disable()
                if style == 'wpc':
                    hold_coil.disable()

        # Enable the flipper relay on wpcAlphanumeric machines
        if self.machine_type == pinproc.MachineTypeWPCAlphanumeric:
            self.enable_alphanumeric_flippers(enable)

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
