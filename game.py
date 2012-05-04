
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from procgame import *
import cc_modes
import pinproc
import tracking
from assets import *

## Define the config file locations
user_game_data_path = "config/game_data.yaml"
game_data_defaults_path = "config/game_data_template.yaml"
settings_defaults_path = "config/settings_template.yaml"
user_settings_path = "config/user_settings.yaml"

## Subclass BasicGame to create the main game
class CCGame(game.BasicGame):

    def __init__(self):
        super(CCGame, self).__init__(pinproc.MachineTypeWPC)
        self.load_config('cc_machine.yaml')
        self.sound = sound.SoundController(self)
        self.assets = Assets(self)

        ## This resets the color mapping so my 1 value pixels are black - even on composite - HUGE WIN!
        self.proc.set_dmd_color_mapping([0,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15])


    def setup(self):
        """docstring for setup"""
        # Game data
        self.load_game_data(game_data_defaults_path, user_game_data_path)
        # Game settings
        self.load_settings(settings_defaults_path, user_settings_path)

        # Set the balls per game per the user settings
        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']

        #self.setup_ball_search()

        # Note - Game specific item:
        # Here, trough6 is used for the 'eject_switchname'.  This must
        # be the switch of the next ball to be ejected.  Some games
        # number the trough switches in the opposite order; so trough1
        # might be the proper switchname to user here.
        trough_switchnames = ['troughBallOne', 'troughBallTwo', 'troughBallThree', 'troughBallFour']
        early_save_switchnames = ['rightOutlane', 'leftOutlane']
        # can't turn on the trough yet
        #self.trough = modes.Trough(self, trough_switchnames,'troughBallOne','troughEject', early_save_switchnames, 'shooterLane', self.ball_drained)
        # not dealing with ballsave yet either
        #self.ball_save = modes.BallSave(self, self.lamps.shootAgain, 'shooterLane')
        #self.ball_save.trough_enable_ball_save = self.trough.ballsave

        # High Score stuff
        self.highscore_categories = []

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
        self.highscore_categories.append(cat)

        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'QuickDrawChampHighScoreData'
        cat.titles = ['Quickdraw Champ']
        self.highscore_categories.append(cat)

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
        #self.trough = trough.Trough(game=self)
        self.base_game_mode = cc_modes.BaseGameMode(game=self,priority=4)
        self.attract_mode = cc_modes.Attract(game=self,priority=5)

        self.right_ramp = cc_modes.RightRamp(game=self,priority=10)
        self.left_ramp = cc_modes.LeftRamp(game=self,priority=11)
        self.center_ramp = cc_modes.CenterRamp(game=self,priority=12)
        self.left_loop = cc_modes.LeftLoop(game=self,priority=13)
        self.right_loop = cc_modes.RightLoop(game=self,priority=14)

        self.mine = cc_modes.Mine(game=self,priority=24)
        self.saloon = cc_modes.Saloon(game=self,priority=25)


        self.skill_shot = cc_modes.SkillShot(game=self,priority=50)


        ## try adding the score display font override
        self.score_display.font_18x12 = self.assets.font_score_x12

        # Setup and instantiate service mode
        self.service_mode = service.ServiceMode(self,100,self.assets.font_tiny7,[])

        # Add in the modes that are active at start
        # not running the trough yet
        # self.modes.add(self.trough)
        self.modes.add(self.attract_mode)


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

        # TODO: Check that there is not already a ball in the shooter lane.
        # TODO: Pulse the trough until we get a hit from the shooter lane switch.
        # self.coils.trough.pulse() # eject a ball into the shooter lane

        # turn the flippers on
        self.enable_flippers(True)
        # and load the skill_shot mode into the mode queue
        # load the base game mode here
        self.modes.add(self.base_game_mode)
        ## TODO maybe move all these to base game for starting stopping
        self.modes.add(self.right_ramp)
        self.modes.add(self.left_ramp)
        self.modes.add(self.center_ramp)
        self.modes.add(self.left_loop)
        self.modes.add(self.right_loop)
        self.modes.add(self.mine)

        self.modes.add(self.skill_shot)

    def ball_ended(self):
        """Called by end_ball(), which is itself called by base_game_mode.trough_changed."""
        self.log("BALL ENDED")
        # unload the base game mode from the queue
        # TODO hmm, should all modes be unloaded at the end of the ball?
        self.modes.remove(self.base_game_mode)
        # turn off the flippers
        self.enable_flippers(False)
        # then call the ball_ended from proc.game.BasicGame
        super(CCGame, self).ball_ended()

    def game_ended(self):
        self.log("GAME ENDED")
        ## call the game_ended from proc.game.BasicGame
        super(CCGame, self).game_ended()
        # remove the base game mode
        self.modes.remove(self.base_game_mode)
        # re-add the attract mode
        self.modes.add(self.attract_mode)

    ##
    ## Player Stats/progress tracking
    ##

    def set_tracking(self,item,amount):
        p = self.current_player()
        p.player_stats[item] = amount

    # call from other modes to set a value
    def increase_tracking(self,item,amount=1):
        ## tick up a stat by a declared amount
        p = self.current_player()
        p.player_stats[item] += amount

    # return values to wherever
    def show_tracking(self,item):
        p = self.current_player()
        return p.player_stats[item]

    # extra method for adding bonus to make it shorter when used
    def add_bonus(self,points):
        p = self.current_player()
        p.player_stats['bonus'] += points
        print p.player_stats['bonus']