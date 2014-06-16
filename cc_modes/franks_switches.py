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
#
# This mode is just a big switch list to trap action for the beans and franks
#
from procgame import game
import ep

class FranksSwitches(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(FranksSwitches, self).__init__(game, priority)
        self.myID = "Beans And Franks Switches"
        # Install early ball_save switch handlers.
        for switch in self.game.switches:
            self.add_switch_handler(name=switch.name, event_type='active', delay=None, handler=self.switch_action)
        self.running = False
        self.excluded = ["trough1","trough2","trough3","trough4","flipperLwL","flipperLwR","mineEncoder","mineHome","trainEncoder"]

    def mode_started(self):
        self.running = True
        self.game.sound.franks = True

    def switch_action(self,sw):
        if sw.name in self.excluded:
            return
        # score 20k points
        self.game.score(20000)
        # play a sound
        self.game.sound.play(self.game.assets.sfx_franks)

    def end(self):
        self.running = False
        self.game.sound.franks = False
        self.unload()