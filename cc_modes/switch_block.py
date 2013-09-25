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
# This mode is to ride over the low end basic ramp shots whenever there's a stackable mode running
# to allow stacked modes to share the shots - but not progress the basic ramp shots.
#

from procgame import game
import ep

class SwitchBlock(ep.EP_Mode):
    """This is to load between the low ramp basic shots and higher level stackable modes"""
    def __init__(self, game,priority):
        super(SwitchBlock, self).__init__(game, priority)
        self.myID = "Switch Block"


    # The loops
    def sw_leftLoopTop_active(self,sw):
        stackLevel = self.game.show_tracking('stackLevel')
        if True in stackLevel[3:]:
            return game.SwitchStop

    # right loop top
    def sw_rightLoopTop_active(self,sw):
        stackLevel = self.game.show_tracking('stackLevel')
        if True in stackLevel[3:]:
            return game.SwitchStop

    # The ramps
    def sw_leftRampEnter_active(self,sw):
        if self.game.cv_tribute.running:
            self.game.cv_tribute.atmos("leftRamp")
        return game.SwitchStop

    def sw_leftRampMake_active(self,sw):
        return game.SwitchStop

    def sw_centerRampMake_active(self,sw):
        if self.game.cv_tribute.running:
            self.game.cv_tribute.atmos("centerRamp")
        return game.SwitchStop

    def sw_centerRampEnter_active(self,sw):
        return game.SwitchStop

    def sw_rightRampEnter_active(self,sw):
        if self.game.cv_tribute.running:
            self.game.cv_tribute.atmos("rightRamp")
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        return game.SwitchStop

    def sw_rightRampBottom_active(self,sw):
        return game.SwitchStop

