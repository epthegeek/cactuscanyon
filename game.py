
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from procgame import *
import cc_modes
import pinproc
import tracking
from assets import *
import ep

## Define the config file locations
user_game_data_path = "config/game_data.yaml"
game_data_defaults_path = "config/game_data_template.yaml"
settings_defaults_path = "config/settings_template.yaml"
user_settings_path = "config/user_settings.yaml"

## Subclass BasicGame to create the main game
class CCGame(game.BasicGame):
    def __init__(self,machineType, fakePinProc = False):
        #if (fakePinProc):
            #config.values['pinproc_class'] = 'procgame.fakepinproc.FakePinPROC'

        super(CCGame, self).__init__(machineType)
        self.load_config('cc_machine.yaml')
        self.sound = sound.SoundController(self)
        self.lampctrl = lamps.LampController(self)
        self.assets = Assets(self)

        ## This resets the color mapping so my 1 value pixels are black - even on composite - HUGE WIN!
        self.proc.set_dmd_color_mapping([0,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

        # combo timer variable
        self.comboTimer = 0
        # last switch variable for tracking
        self.lastSwitch = None
        self.ballStarting = False
        self.runLampShows = False
        self.status = None

    def setup(self):
        """docstring for setup"""
        # Game data
        self.load_game_data(game_data_defaults_path, user_game_data_path)
        # Game settings
        self.load_settings(settings_defaults_path, user_settings_path)

        # Set the balls per game per the user settings
        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']

        # set up the ball search - not using this yet
        self.setup_ball_search()

        # set up the trough mode
        trough_switchnames = ['troughBallOne', 'troughBallTwo', 'troughBallThree', 'troughBallFour']
        early_save_switchnames = ['rightOutlane', 'leftOutlane']
        # can't turn on the trough yet
        self.trough = modes.Trough(self, trough_switchnames,'troughBallOne','troughEject', early_save_switchnames, 'shooterLane', self.ball_drained)
        # set up ball save
        self.ball_save = modes.BallSave(self, self.lamps.shootAgain, 'shooterLane')

        # High Score stuff
        self.highscore_categories = []

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'QuickdrawChampHighScoreData'
        cat.titles = ['Quickdraw Champ']
        self.highscore_categories.append(cat)

        ## TODO later - add showdown and combo champ

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
        self.base_game_mode = cc_modes.BaseGameMode(game=self,priority=4)
        self.attract_mode = cc_modes.Attract(game=self,priority=5)

        self.right_ramp = cc_modes.RightRamp(game=self,priority=10)
        self.left_ramp = cc_modes.LeftRamp(game=self,priority=11)
        self.center_ramp = cc_modes.CenterRamp(game=self,priority=12)
        self.left_loop = cc_modes.LeftLoop(game=self,priority=13)
        self.right_loop = cc_modes.RightLoop(game=self,priority=14)

        # mine and saloon have to stay high so they can interrupt other displays
        self.mine = cc_modes.Mine(game=self,priority=24)
        self.saloon = cc_modes.Saloon(game=self,priority=25)

        # Quickdraw battle and showdown
        self.bad_guys = cc_modes.BadGuys(game=self,priority=67)
        # Svae Polly
        self.save_polly = cc_modes.SavePolly(game=self,priority=68)
        # this mode unloads when not in use
        self.skill_shot = cc_modes.SkillShot(game=self,priority=70)
        # gold mine multiball
        self.gm_multiball = cc_modes.GoldMine(game=self,priority=88)
        # High Noon
        #self.high_noon = cc_modes.HighNoon(game=self,priority=90)

        ## try adding the score display font override
        self.score_display.font_18x12 = self.assets.font_score_x12

        # Setup and instantiate service mode
        self.service_mode = service.ServiceMode(self,100,self.assets.font_tiny7,[])

        # set up an array of the modes
        self.ep_modes = [self.base_game_mode,
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
                         self.gm_multiball]

        self.ep_modes.sort(lambda x, y: y.priority - x.priority)

        # Add in the modes that are active at start
        self.modes.add(self.trough)
        self.modes.add(self.ball_save)
        self.modes.add(self.ball_search)
        self.modes.add(self.attract_mode)

    def start_game(self):
        # remove the attract mode
        self.modes.remove(self.attract)
        # turn off all the ligths
        for lamp in self.lamps:
            lamp.disable()
        # load the base game mode
        self.modes.add(self.base_game_mode)
        # run the start ball from parent
        super(CCGame,self).start_game()
        # Add the first player
        self.add_player()
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

    def ball_starting(self):
        self.log("BALL STARTING")
        ## run the ball_starting from proc.gameBasicGame
        super(CCGame, self).ball_starting()
        self.ballStarting = True
        # launch a ball, unless there is one in the shooter lane already - but really, this shouldn't
        # happen because we're only starting if trough is full
        if not self.switches.shooterLane.is_active():
            self.trough.launch_balls(1) # eject a ball into the shooter lane

        # enable the ball search
        self.ball_search.enable()
        # turn the flippers on
        self.enable_flippers(True)
        # reset the tilt status
        self.set_tracking('tiltStatus',0)

        # and load the skill shot
        self.modes.add(self.skill_shot)

    # Empty callback just incase a ball drains into the trough before another
     # drain_callback can be installed by a gameplay mode.
    def ball_drained(self):
        # Tell every mode a ball has drained by calling the ball_drained function if it exists
        if self.game.trough.num_balls_in_play == 0:
            # kill all the display layers
            for mode in self.ep_modes:
                if getattr(mode, "clear_layer", None):
                    mode.clear_layer()
        ## and tell all the modes the ball drained no matter what
        for mode in self.ep_modes:
            if getattr(mode, "ball_drained", None):
                mode.ball_drained()

    def ball_ended(self):
        """Called by end_ball(), which is itself called by base_game_mode.trough_changed."""
        self.log("BALL ENDED")
        # reset the tilt
        self.game.set_tracking('tiltStatus',0)
        # then call the ball_ended from proc.game.BasicGame
        super(CCGame, self).ball_ended()
        self.end_ball()

    def game_ended(self):
        self.log("GAME ENDED")
        ## call the game_ended from proc.game.BasicGame
        super(CCGame, self).game_ended()
        # remove the base game mode
        self.modes.remove(self.base_game_mode)
        # re-add the attract mode
        self.modes.add(self.attract_mode)

    def setup_ball_search(self):
        # No special handlers in starter game.
        special_handler_modes = []
        self.ball_search = modes.BallSearch(self, priority=100,countdown_time=30, coils=self.ballsearch_coils,reset_switches=self.ballsearch_resetSwitches,stop_switches=self.ballsearch_stopSwitches,special_handler_modes=special_handler_modes)

    def schedule_lampshows(self,lampshows,repeat=True):
        self.scheduled_lampshows = lampshows
        self.scheduled_lampshows_repeat = repeat
        self.scheduled_lampshow_index = 0
        self.start_lampshow()

    def start_lampshow(self):
        self.lampctrl.play_show(self.scheduled_lampshows[self.scheduled_lampshow_index], False, self.lampshow_ended)

    def lampshow_ended(self):
        if self.runLampShows:
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
        else:
            pass

    def enable_lampshow(self):
        self.runLampShows = True

    def disable_lampshow(self):
        self.runLampShows = False

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


    ## this is for frame listeners and delays
    def play_remote_sound(self,param):
        print param
        self.sound.play(param)

    def play_remote_music(self,param):
        print "ITS TIME TO START THE MUSIC"
        print param
        self.sound.play_music(param, loops=-1)

    ## bonus stuff

    # extra method for adding bonus to make it shorter when used
    def add_bonus(self,points):
        p = self.current_player()
        p.player_stats['bonus'] += points
        print p.player_stats['bonus']

