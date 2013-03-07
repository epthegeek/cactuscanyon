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

import ep
from procgame import dmd, game
import sys

class NewServiceMode(ep.EP_Mode):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceMode, self).__init__(game, priority)
        self.mode = ["TESTS","SETTINGS","STATS","UTILITIES"]
        if self.game.usb_update:
            self.mode.append("UPDATE")
        if self.game.shutdownFlag:
            self.mode.append("SHUTDOWN")
        self.testSection = ["SWITCHES","SINGLE LAMPS", "ALL LAMPS","SOLENOIDS","FLASHERS","DROP TARGETS","MINE"]
        self.settingSection = ["STANDARD","FEATURE"]
        # set the active mode to menu
        self.activeMode = "STARTUP"

    def mode_started(self):
        # set some indexes
        self.modeIndex = 0
        self.testIndex = 0
        self.settingIndex = 0
        title = dmd.TextLayer(64,1,self.game.assets.font_7px_alt_az,"center",opaque=True).set_text("Cactus Canyon Continued")
        revision = dmd.TextLayer(64,10,self.game.assets.font_7px_alt_az,"center").set_text("Revision: " + self.game.revision)
        info = dmd.TextLayer(64,20,self.game.assets.font_7px_az,"center").set_text("Press ENTER for Menu")
        combo1 = dmd.GroupedLayer(128,32,[title,revision,info])
        combo2 = dmd.GroupedLayer(128,32,[title,revision])
        script = []
        script.append({'seconds':0.6,'layer':combo1})
        script.append({'seconds':0.6,'layer':combo2})
        display = dmd.ScriptedLayer(128,32,script)
        self.layer = display
        # play the service entrance noise
        self.game.sound.play(self.game.assets.sfx_serviceStart)


    def mode_stopped(self):
        self.game.sound.play(self.game.assets.sfx_menuExit)
        # save the data
        self.game.save_game_data()
        if self.game.service_mode not in self.game.modes:
            print "Service Mode Exiting"
            if self.game.usb_update:
                print "Reloading to pull in new files"
                sys.exit(42)
            else:
                print "Calling Reset"
                self.game.reset()

# switches

    def sw_enter_active(self,sw):
        # if we're at the startup, switch to menu
        if self.activeMode == "STARTUP":
            self.activeMode = "MENU"
            self.update_display()
        return game.SwitchStop

    def sw_up_active(self,sw):
        # play the sound for moving up
        self.game.sound.play(self.game.assets.sfx_menuUp)
        if self.activeMode == "MENU":
            self.item_up()
        else:
            pass
        return game.SwitchStop

    def sw_down_active(self, sw):
        # play the sound for moving down
        self.game.sound.play(self.game.assets.sfx_menuDown)
        if self.activeMode == "MENU":
            self.item_down()
        else:
            pass
        return game.SwitchStop

    def sw_exit_active(self, sw):
        if self.activeMode == "STARTUP" or self.activeMode == "MENU":
            self.unload()
        return game.SwitchStop

# display
    def update_display(self):
        if self.activeMode == "MENU":
            title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Service Menu")
            selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(str(self.mode[self.modeIndex]))
            self.layer = dmd.GroupedLayer(128,32,[title,selection])


# navigation
    def item_down(self):
        if self.activeMode == "MENU":
            self.modeIndex -= 1
            # if we get below zero, loop around
            if self.modeIndex < 0:
                self.modeIndex = (len(self.mode) - 1)
            # then update the display
            self.update_display()
        else:
            pass

    def item_up(self):
        if self.activeMode == "MENU":
            self.modeIndex += 1
            # if we get too high, go to zero
            if self.modeIndex >= len(self.mode):
                self.modeIndex = 0
            # then update the display
            self.update_display()
        else:
            pass