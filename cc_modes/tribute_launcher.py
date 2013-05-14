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
#
# This mode is a small transitional thing for choosing which tribute mode to launch for the super skill shot
#
from procgame import game, dmd
import random
import ep

class TributeLauncher(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(TributeLauncher, self).__init__(game, priority)
        self.myID = "Tribute Launcher"

        mb_logo = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mbLogo.frames[0])
        taf_logo = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_tafLogo.frames[0])
        mm_logo = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mmLogo.frames[0])
        self.slides = [mb_logo,taf_logo,mm_logo]
        self.shot = 0

    def mode_started(self):
        self.selecting = False
        # set the stack level
        self.game.stack_level(5,True)
        choices = [0,1,2]
        self.index = random.choice(choices)
        # throw up a text thing telling player to hit flippers to select
        title = ep.EP_TextLayer(58, 1, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("TRIBUTE",color=ep.ORANGE)
        lineOne = ep.EP_TextLayer(58,12, self.game.assets.font_5px_AZ, "center", opaque = False).set_text("HIT BOTH FLIPPERS",color=ep.YELLOW)
        lineTwo = ep.EP_TextLayer(58,19, self.game.assets.font_5px_AZ, "center", opaque = False).set_text("TO SELECT MODE", color=ep.YELLOW)
        icon = dmd.TextLayer(124,1, self.game.assets.font_skillshot, "right", opaque=True).set_text("V")
        combined = dmd.GroupedLayer(128,32,[icon,title,lineOne,lineTwo])
        self.layer = combined
        self.delay(delay=2,handler=self.start_selection)

    def start_selection(self):
        self.selecting = True
        self.update_layer()

    def update_layer(self):
        # bump up the index
        self.index += 1
        # wrap if needed
        if self.index > 2:
            self.index= 0
        # set the layer
        self.layer = self.slides[self.index]
        # loop back to do it again
        self.delay("Display",delay=0.5,handler=self.update_layer)

    def make_selection(self):
        self.cancel_delayed("Display")
        if self.shot == 3:
            position = "Mine"
        else:
            position = "Lane"
        print "Ball is in the " + position
        # and then do some junk -- all selections launch TAF for now
        if self.index == 0:
            print "Selected Monster Bash"
            self.game.modes.add(self.game.taf_tribute)
        elif self.index == 1:
            print "Selected Addams Family"
            self.game.modes.add(self.game.taf_tribute)
        elif self.index == 2:
            print "Selected Medieval Madness"
            self.game.modes.add(self.game.taf_tribute)
        else:
            print "WAT"
        # and then unload -- tribute modes will unload this mode
        #self.delay(delay=4,handler=self.unload)

