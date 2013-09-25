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
## Starter script
## shamelessly cribbed from Koen Hetzels's Bride of Pinbot 2.0

#from procgame import *
import locale
import yaml
import sys

import logging
logging.basicConfig(level=logging.WARN, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# Import the actual game script
from game import *
import os

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

# the config file
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
yaml_path = curr_file_path + "/config/cc_machine.yaml"

def main():
    # Load up the config file
    config = yaml.load(open(yaml_path, 'r'))
    # set a variable for the machine type
    machineType = config['PRGame']['machineType']

    config = 0
    game = None
    fakePinProc = (len(sys.argv) >= 1 and 'fakepinproc' in sys.argv)
    #recording = (len(sys.argv) > 1 and 'record' in sys.argv)
    #playback = (len(sys.argv) > 1 and 'playback' in sys.argv)

    #if playback:
    #    # this covers if fakepinproc was not specified
    #    fakePinProc = True

    try:
        # create the game object
        game = CCGame(machineType,fakePinProc)
        # set the game's config path
        game.yamlpath = yaml_path
        # fire off the setup
        game.setup()
        # then run that sucker
        game.run_loop()
    finally:
        del game

if __name__ == '__main__': main()