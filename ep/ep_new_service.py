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
import os
from distutils import dir_util

class NewServiceSkeleton(ep.EP_Mode):
    """New Service Mode List base class with defaults."""
    def __init__(self, game, priority):
        super(NewServiceSkeleton, self).__init__(game, priority)
        self.busy = False
        self.index = 0
        self.section = []

    def sw_up_active(self,sw):
        if not self.busy:
            print "Item Up"
            # play the sound for moving up
            self.game.sound.play(self.game.assets.sfx_menuUp)
            self.item_up()
        else:
            pass
        return game.SwitchStop

    def sw_down_active(self, sw):
        if not self.busy:
            print "Item Down"
            # play the sound for moving down
            self.game.sound.play(self.game.assets.sfx_menuDown)
            self.item_down()
        else:
            pass
        return game.SwitchStop

    # default behavior for exit switch is just to exit
    def sw_exit_active(self,sw):
        if not self.busy:
            self.game.sound.play(self.game.assets.sfx_menuExit)
            self.unload()
        return game.SwitchStop

    def item_down(self):
        self.index -= 1
        # if we get below zero, loop around
        if self.index < 0:
            self.index = (len(self.section) - 1)
        # then update the display
        self.update_display()

    def item_up(self):
        self.index += 1
        # if we get too high, go to zero
        if self.index >= len(self.section):
            self.index = 0
        # then update the display
        self.update_display()


class NewServiceMode(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceMode, self).__init__(game, priority)
        self.myID = "Service Mode"

    def mode_started(self):
        self.section = ["TESTS","SETTINGS","STATS","UTILITIES"]
        if self.game.usb_update:
            self.section.append("UPDATE")
        if self.game.shutdownFlag:
            self.section.append("SHUTDOWN")
            # set the active mode to menu
        self.activeMode = "STARTUP"
        self.index = 0

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
        # save the data
        self.game.save_game_data()
        print "Service Mode Exiting"
        if self.game.usb_update:
            print "Reloading to pull in new files"
            sys.exit(42)
        else:
            print "Calling Reset"
            self.game.reset()

# switches

    def sw_enter_active(self,sw):
        if not self.busy:
            # if we're at the startup, switch to menu
            if self.activeMode == "STARTUP":
                self.game.sound.play(self.game.assets.sfx_menuEnter)
                self.activeMode = "MENU"
                self.update_display()
            # if we're on the menu, we're selecting a sub-menu
            elif self.activeMode == "MENU":
                self.game.sound.play(self.game.assets.sfx_menuEnter)
                # set active mode to the currently selected mode
                self.activeMode = self.section[self.index]
                # Then create that mode
                if self.activeMode == "TESTS":
                    self.mode_to_add = NewServiceModeTests(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif self.activeMode == "SETTINGS":
                    self.mode_to_add = NewServiceModeSettings(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif self.activeMode == "STATS":
                    self.mode_to_add = NewServiceModeStats(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif self.activeMode == "UTILITIES":
                    self.mode_to_add = NewServiceModeUtilities(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif self.activeMode == "UPDATE":
                    self.mode_to_add = NewServiceModeUpdate(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif self.activeMode == "SHUTDOWN":
                    self.update_display()
                    print "Powering off"
                    # exit with error code 69
                    sys.exit(69)
            else:
                pass
        return game.SwitchStop

    # display
    def update_display(self):
        if self.activeMode == "MENU":
            title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Service Menu")
            selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(str(self.section[self.index]))
            self.layer = dmd.GroupedLayer(128,32,[title,selection])
        elif self.activeMode == "SHUTDOWN":
            title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("")
            selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text("SHUTTING DOWN")
            self.layer = dmd.GroupedLayer(128,32,[title,selection])


class NewServiceModeTests(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceModeTests, self).__init__(game, priority)
        self.myID = "Service Mode Tests"

    def mode_started(self):
        # set some indexes
        self.index = 0
        self.section = ["SWITCHES","SINGLE LAMPS", "ALL LAMPS","SOLENOIDS","FLASHERS","DROP TARGETS","MINE"]
        self.update_display()

    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

    def update_display(self):
        title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Tests")
        selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(str(self.section[self.index]))
        self.layer = dmd.GroupedLayer(128,32,[title,selection])


class NewServiceModeSettings(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceModeSettings, self).__init__(game, priority)
        self.myID = "Service Mode Settings"

    def mode_started(self):
        self.index = 0
        self.settingSection = ["STANDARD","FEATURE"]
        self.update_display()

    def update_display(self):
        title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Settings")
        selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(str(self.section[self.index]))
        self.layer = dmd.GroupedLayer(128,32,[title,selection])

class NewServiceModeStats(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceModeStats, self).__init__(game, priority)
        self.myID = "Service Mode Stats"

    def mode_started(self):
        self.index = 0
        self.section = ["PENDING","PENDING"]
        self.update_display()

    def update_display(self):
        title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Statistics")
        selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text("PENDING",blink_frames=40)
        self.layer = dmd.GroupedLayer(128,32,[title,selection])

class NewServiceModeUtilities(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceModeUtilities, self).__init__(game, priority)
        self.myID = "Service Mode Utilities"

    def mode_started(self):
        self.index = 0
        self.section = ["CLEAR AUDITS", "RESET HSTD"]
        self.update_display()

    def update_display(self):
        title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Utilities")
        selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(str(self.section[self.index]))
        self.layer = dmd.GroupedLayer(128,32,[title,selection])

class NewServiceModeUpdate(NewServiceSkeleton):
    """Service Mode List base class."""
    def __init__(self, game, priority):
        super(NewServiceModeUpdate, self).__init__(game, priority)
        self.myID = "Service Mode Updates"

    def mode_started(self):
        self.noItems = True
        self.check_update()

    def sw_enter_active(self,sw):
        if self.okToUpdate:
            self.busy = True
            # if enter is pressed, copy the files
            # update the layer to say copying files
            self.update_display("COPYING FILES","DO NOT POWER OFF")
            self.delay(delay=1,handler=self.copy_files)
        else:
            self.game.sound.play(self.game.assets.sfx_menuReject)

    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

    def update_display(self,textString1 = "",textString2 = ""):
        title = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text("Software Update")
        selection = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(textString1)
        info = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center").set_text(textString2,blink_frames=30)
        self.layer = dmd.GroupedLayer(128,32,[title,selection,info])

    def check_update(self):
        self.myLocation = None
        self.okToUpdate = False
        # list the contents of the USB path
        dirs = os.listdir(self.game.usb_location)
        # check them all for the update files
        for directory in dirs:
            checkThis = self.game.usb_location + directory + "/ccc_update_files"
            if os.path.isdir(checkThis):
                print "Found the update"
                self.myLocation = checkThis
        if self.myLocation != None:
            self.okToUpdate = True
            status ="FILES FOUND FOR UPDATE"
            info = "PRESS ENTER TO UPDATE"
        else:
            self.okToUpdate = False
            print "Didn't find the update"
            status = "FILES NOT FOUND"
            info = "CHECK USB DRIVE"
        # then update the display
        self.update_display(textString1=status,textString2=info)

    def copy_files(self):
        dir_util.copy_tree(self.myLocation,self.game.game_location)
        self.update_display(textString1="COPY FINISHED")
        self.busy = False

