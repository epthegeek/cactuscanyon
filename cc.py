## Cactus Canyon Starter script
## shamelessly cribbed from Koen's Bride of Pinbot 2.0

from procgame import *
import locale
import yaml
import sys


# Import the actual game script
from game import *

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

# the config file
yaml_path = "config/cc_machine.yaml"

def main():
    # Load up the config file
    config = yaml.load(open(yaml_path, 'r'))
    # set a variable for the machine type
    machineType = config['PRGame']['machineType']

    config = 0
    game = None
    fakePinProc = (len(sys.argv) > 1 and sys.argv[1] == 'fakepinproc')
    try:
        # create the game object
        game = CCGame()
        # set the game's config path
        game.yamlpath = yaml_path
        # fire off the setup
        game.setup()
        # then run that sucker
        game.run_loop()
    finally:
        del game

if __name__ == '__main__': main()