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
        self.songs = [self.game.assets.music_mb,self.game.assets.music_taf,self.game.assets.music_mm]
        self.shot = 0
        self.selecting = False
        self.method = self.game.user_settings['Gameplay (Feature)']['Tribute Selecting']
        self.Timer = 30

    def mode_started(self):
        # mode auto selects after 30 seconds to avoid holding the ball forever
        self.Timer = 30
        self.counter = 0
        self.selecting = False
        # set the stack level
        self.game.stack_level(5,True)
        choices = [0,1,2]
        self.index = random.choice(choices)
        # throw up a text thing telling player to hit flippers to select
        title = ep.EP_TextLayer(58, 3, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("TRIBUTE",color=ep.ORANGE)
        lineOne = ep.EP_TextLayer(58,15, self.game.assets.font_5px_AZ, "center", opaque = False)
        lineTwo = ep.EP_TextLayer(58,21, self.game.assets.font_5px_AZ, "center", opaque = False)
        # instructions on how to start are different
        if self.method == "Random":
            lineOne.set_text("THIS IS JUST",color=ep.YELLOW)
            lineTwo.set_text("A TRIBUTE", color=ep.YELLOW)
        else:
            lineOne.set_text("FLIPPERS = CHANGE",color=ep.YELLOW)
            lineTwo.set_text("START = SELECT", color=ep.YELLOW)
        icon = dmd.TextLayer(124,1, self.game.assets.font_skillshot, "right", opaque=True).set_text("V")
        combined = dmd.GroupedLayer(128,32,[icon,title,lineOne,lineTwo])
        self.layer = combined
        self.delay(delay=3,handler=self.start_selection)

    def sw_startButton_active(self,sw):
        if self.selecting and self.method == "Manual":
            self.make_selection()
        else:
            pass
        return game.SwitchStop

    def sw_flipperLwL_active(self,sw):
        if self.method == "Manual":
            # left flipper changes pages down one
            self.change_page(-1)
        return game.SwitchStop

    def sw_flipperLwR_active(self,sw):
        if self.method == "Manual":
            # right flipper changes pages up one
            self.change_page(1)
        return game.SwitchStop

    def start_selection(self):
        self.selecting = True
        # random shows each available method one time, then starts
        if self.method == "Random":
            self.update_layer()
        # manual plays the music that matches the showing logo
        else:
            # start the timer
            self.timer_loop()
            # and the music
            self.layer = self.slides[self.index]
            self.music_on(self.songs[self.index])

    # this is the random handler
    def update_layer(self):
        # bump up the index
        self.index += 1
        self.counter += 1
        # wrap if needed
        if self.index > (len(self.slides) -1):
            self.index= 0
        # set the layer
        self.layer = self.slides[self.index]
        if self.counter == len(self.slides):
            self.make_selection()
        else:
            # loop back to do it again
            self.delay("Display",delay=0.7,handler=self.update_layer)

    # this is the manual mode handler
    def change_page(self,value):
        # pad the timer
        if self.Timer < 25:
            self.Timer = 25
        self.index += value
        # if we're below zero, wrap
        if self.index < 0:
            self.index = (len(self.slides) - 1)
        # if we're over the total, go to zero
        elif self.index >= len(self.slides):
            self.index = 0
        # set the layer
        self.layer = self.slides[self.index]
        # manual plays the music that matches the showing logo
        self.music_on(self.songs[self.index])

    def make_selection(self):
        self.cancel_delayed("Timer")
        self.cancel_delayed("Display")
        if self.shot == 3:
            position = "Mine"
        else:
            position = "Lane"
        print "Ball is in the " + position
        # and then do some junk
        if self.index == 0:
            print "Selected Monster Bash"
            self.game.modes.add(self.game.mb_tribute)
        elif self.index == 1:
            print "Selected Addams Family"
            self.game.modes.add(self.game.taf_tribute)
        elif self.index == 2:
            print "Selected Medieval Madness"
            self.game.modes.add(self.game.mm_tribute)
        else:
            print "WAT"
        # and then unload -- tribute modes will unload this mode
        #self.delay(delay=4,handler=self.unload)

    def timer_loop(self):
        self.Timer -= 1
        if self.Timer < 0:
            self.make_selection()
        else:
            self.delay("Timer",delay=1, handler=self.timer_loop)

    def remove_launcher(self):
        self.selecting = False
        # turn the level 5 stack flag back off
        self.game.stack_level(5,False)
        self.unload()