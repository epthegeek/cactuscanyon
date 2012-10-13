import sys
sys.path.append(sys.path[0]+'/../..') # Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.

# Original code from Jim (myPinballs) and Koen (DutchPinball)
import locale
import yaml
from loader import *

game_locale = config.value_for_key_path('std_locale')
locale.setlocale(locale.LC_ALL, game_locale) # en_GB Used to put commas in the score.


machine_config_path = 'config/cc_machine.yaml'
fnt_path = "/data/proc/cactuscanyon/shared/dmd/"


class Game(game.BasicGame):
    """docstring for Game"""
    def __init__(self, machine_type):
        super(Game, self).__init__(machine_type)
        self.settings = {}

    def save_settings(self):
        super(Game, self).save_settings(settings_path)

    def save_game_data(self):
        super(Game, self).save_game_data(game_data_path)


    def setup(self):
        """docstring for setup"""
        self.load_config(self.yamlpath)



        self.loader = Loader(self,2)
        # Instead of resetting everything here as well as when a user
        # initiated reset occurs, do everything in self.reset() and call it
        # now and during a user initiated reset.
        self.reset()

    def enable_flippers(self,enable):
        if enable:
            self.coils.flipperEnable.pulse(0)
        else:
            self.coils.flipperEnable.disable()

    def reset(self):
        # Reset the entire game framework
        super(Game, self).reset()

        # Add the basic modes to the mode queue
        self.modes.add(self.loader)

        # Make sure flippers are off, especially for user initiated resets.
        self.enable_flippers(enable=True)


def main():

    config = yaml.load(open(machine_config_path, 'r'))
    print("Using config at: %s "%(machine_config_path))
    machine_type = config['PRGame']['machineType']
    config = 0
    game = None
    try:
        game = Game(machine_type)
        game.yamlpath = machine_config_path
        game.setup()
        game.run_loop()
    finally:
        del game


if __name__ == '__main__': main()
