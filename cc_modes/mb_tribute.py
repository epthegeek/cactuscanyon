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
## The Monster Bash Tribute
##

from procgame import dmd,game
import ep
import random

class MB_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(MB_Tribute, self).__init__(game,priority)
        self.myID = "MB Tribute"


# after intro - push up with "Hit dracula 5 times" / " to finish" 7px

# running screen: timers in both corners 7px, info line at the bottom "x - hits to finish - x" 5px
# title line " drac attack" 5px bold - score in the middle 12 px
#
# after a hit, push up - "Dracula damaged" 7px - score - large - crossfade back to drac display
# last one says dracula defeated
# drac-attack total screen - stake boarder 'drac-attack / total:' w/ score in 9px
