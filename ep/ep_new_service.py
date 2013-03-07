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
        self.selectionLine.set_text(str(self.section[self.index]))

    def item_up(self):
        self.index += 1
        # if we get too high, go to zero
        if self.index >= len(self.section):
            self.index = 0
        # then update the display
        self.selectionLine.set_text(str(self.section[self.index]))

    # standard display structure
    def update_display(self,titleString,selectionString,infoString="",blinkInfo = False):
        self.titleLine = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text(titleString)
        self.selectionLine = dmd.TextLayer(64,13,self.game.assets.font_9px_az,"center").set_text(selectionString)
        self.infoLine = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center")
        if blinkInfo:
            self.infoLine.set_text(infoString,blink_frames=30)
        else:
            self.infoLine.set_text(infoString)
        self.layer = dmd.GroupedLayer(128,32,[self.titleLine,self.selectionLine,self.infoLine])


##   __  __       _         __  __
##  |  \/  | __ _(_)_ __   |  \/  | ___ _ __  _   _
##  | |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |
##  | |  | | (_| | | | | | | |  | |  __/ | | | |_| |
##  |_|  |_|\__,_|_|_| |_| |_|  |_|\___|_| |_|\__,_|

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
                self.update_display("Service Menu",str(self.section[self.index]))
            # if we're on the menu, we're selecting a sub-menu
            elif self.activeMode == "MENU":
                self.game.sound.play(self.game.assets.sfx_menuEnter)
                # set active mode to the currently selected mode
                selection = self.section[self.index]
                # Then create that mode
                if selection == "TESTS":
                    self.mode_to_add = NewServiceModeTests(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif selection == "SETTINGS":
                    self.mode_to_add = NewServiceModeSettings(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif selection == "STATS":
                    self.mode_to_add = NewServiceModeStats(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif selection == "UTILITIES":
                    self.mode_to_add = NewServiceModeUtilities(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif selection == "UPDATE":
                    self.mode_to_add = NewServiceModeUpdate(game=self.game,priority=201)
                    self.game.modes.add(self.mode_to_add)
                elif selection == "SHUTDOWN":
                    self.update_display("","SHUTTING DOWN")
                    print "Powering off"
                    # exit with error code 69
                    sys.exit(69)
            else:
                pass
        return game.SwitchStop

##   _____         _         ____            _   _
##  |_   _|__  ___| |_ ___  / ___|  ___  ___| |_(_) ___  _ __
##    | |/ _ \/ __| __/ __| \___ \ / _ \/ __| __| |/ _ \| '_ \
##    | |  __/\__ \ |_\__ \  ___) |  __/ (__| |_| | (_) | | | |
##    |_|\___||___/\__|___/ |____/ \___|\___|\__|_|\___/|_| |_|

class NewServiceModeTests(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeTests, self).__init__(game, priority)
        self.myID = "Service Mode Tests"
        self.index = 0

    def mode_started(self):
        # set some indexes
        self.section = ["SWITCHES","SINGLE LAMPS", "ALL LAMPS","SOLENOIDS","FLASHERS","DROP TARGETS","MINE"]
        self.update_display("Tests",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        selection = self.section[self.index]
        if selection == "SWITCHES":
            self.mode_to_add = NewServiceModeSwitchEdges(game=self.game,priority=202)
            self.game.modes.add(self.mode_to_add)
        else:
            pass
        # TODO: The rest of these sections

class NewServiceModeSwitchEdges(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeSwitchEdges, self).__init__(game, priority)
        self.myID = "Service Mode Switch Test"
        self.index = 0

    def mode_started(self):
        # TODO: check switch states to set row text
        self.row1text = "aaaAaAaa"
        self.row2text = "AAaaaaaA"
        self.update_display()

    # TODO: set up all the switch methods for turning the images on and off

    # null the up and down switches
    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

    def update_display(self):
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_switchMatrix.frames[0])
        self.switchRow1 = dmd.TextLayer(4,4,self.game.assets.font_matrix,"left").set_text(self.row1text)
        self.switchRow1.composite_op = "blacksrc"
        self.switchRow2 = dmd.TextLayer(4,7,self.game.assets.font_matrix,"left").set_text(self.row2text)
        self.switchRow2.composite_op = "blacksrc"
        title = dmd.TextLayer(80,1,self.game.assets.font_5px_AZ,"center").set_text("SWITCH EDGES")
        combined = dmd.GroupedLayer(128,32,[background,title,self.switchRow1,self.switchRow2])
        # TODO: other row lines, info lines
        self.layer = combined

##   ____       _   _   _                   ____            _   _
##  / ___|  ___| |_| |_(_)_ __   __ _ ___  / ___|  ___  ___| |_(_) ___  _ __
##  \___ \ / _ \ __| __| | '_ \ / _` / __| \___ \ / _ \/ __| __| |/ _ \| '_ \
##   ___) |  __/ |_| |_| | | | | (_| \__ \  ___) |  __/ (__| |_| | (_) | | | |
##  |____/ \___|\__|\__|_|_| |_|\__, |___/ |____/ \___|\___|\__|_|\___/|_| |_|
##                              |___/

class NewServiceModeSettings(NewServiceSkeleton):
    """Service Mode Settings Section."""
    def __init__(self, game, priority):
        super(NewServiceModeSettings, self).__init__(game, priority)
        self.myID = "Service Mode Settings"
        self.index = 0

    def mode_started(self):
        self.section = ["STANDARD","FEATURE"]
        self.update_display("Settings",str(self.section[self.index]))

##   ____  _        _         ____            _   _
##  / ___|| |_ __ _| |_ ___  / ___|  ___  ___| |_(_) ___  _ __
##  \___ \| __/ _` | __/ __| \___ \ / _ \/ __| __| |/ _ \| '_ \
##   ___) | || (_| | |_\__ \  ___) |  __/ (__| |_| | (_) | | | |
##  |____/ \__\__,_|\__|___/ |____/ \___|\___|\__|_|\___/|_| |_|

class NewServiceModeStats(NewServiceSkeleton):
    """Service Stats Section."""
    def __init__(self, game, priority):
        super(NewServiceModeStats, self).__init__(game, priority)
        self.myID = "Service Mode Stats"
        self.index = 0

    def mode_started(self):
        self.section = ["PENDING","PENDING"]
        self.update_display("Statistics",str(self.section[self.index]))

##   _   _ _   _ _ _ _   _             ____            _   _
##  | | | | |_(_) (_) |_(_) ___  ___  / ___|  ___  ___| |_(_) ___  _ __
##  | | | | __| | | | __| |/ _ \/ __| \___ \ / _ \/ __| __| |/ _ \| '_ \
##  | |_| | |_| | | | |_| |  __/\__ \  ___) |  __/ (__| |_| | (_) | | | |
##   \___/ \__|_|_|_|\__|_|\___||___/ |____/ \___|\___|\__|_|\___/|_| |_|

class NewServiceModeUtilities(NewServiceSkeleton):
    """Service Mode Utilities Section."""
    def __init__(self, game, priority):
        super(NewServiceModeUtilities, self).__init__(game, priority)
        self.myID = "Service Mode Utilities"

    def mode_started(self):
        self.index = 0
        self.section = ["CLEAR AUDITS", "RESET HSTD"]
        self.update_display("Utilities",str(self.section[self.index]))

##   _   _           _       _         ____            _   _
##  | | | |_ __   __| | __ _| |_ ___  / ___|  ___  ___| |_(_) ___  _ __
##  | | | | '_ \ / _` |/ _` | __/ _ \ \___ \ / _ \/ __| __| |/ _ \| '_ \
##  | |_| | |_) | (_| | (_| | ||  __/  ___) |  __/ (__| |_| | (_) | | | |
##   \___/| .__/ \__,_|\__,_|\__\___| |____/ \___|\___|\__|_|\___/|_| |_|
##        |_|

class NewServiceModeUpdate(NewServiceSkeleton):
    """Service Mode Update Section."""
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
            self.selectionLine.set_text("COPYING FILES")
            self.infoLine.set_text("DO NOT POWER OFF",blink_frames=15)
            self.delay(delay=1,handler=self.copy_files)
        else:
            self.game.sound.play(self.game.assets.sfx_menuReject)

    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

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
        self.update_display("Software Update",status,info,blinkInfo=True)

    def copy_files(self):
        dir_util.copy_tree(self.myLocation,self.game.game_location)
        self.selectionLine.set_text("COPY FINISHED")
        self.infoLine.set_text("")
        self.busy = False

