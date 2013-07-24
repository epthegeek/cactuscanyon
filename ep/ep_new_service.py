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
import highscore

class NewServiceSkeleton(ep.EP_Mode):
    """New Service Mode List base class with defaults."""
    def __init__(self, game, priority):
        super(NewServiceSkeleton, self).__init__(game, priority)
        self.busy = False
        self.index = 0
        self.section = []
        self.callback = None

    def sw_up_active(self,sw):
        if not self.busy:
            # play the sound for moving up
            self.game.sound.play(self.game.assets.sfx_menuUp)
            self.item_up()
        else:
            pass
        return game.SwitchStop

    def sw_down_active(self, sw):
        if not self.busy:
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
        if self.callback:
            self.callback()
        else:
            # then update the display
            self.selectionLine.set_text(str(self.section[self.index]))

    def item_up(self):
        self.index += 1
        # if we get too high, go to zero
        if self.index >= len(self.section):
            self.index = 0
        if self.callback:
            self.callback()
        else:
            # then update the display
            self.selectionLine.set_text(str(self.section[self.index]))

    # standard display structure
    def update_display(self,titleString,selectionString,infoString="",blinkInfo = False):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        background.set_target_position(0,-4)
        layers.append(background)
        self.titleLine = dmd.TextLayer(1,3,self.game.assets.font_5px_AZ_inverted,"Left").set_text(titleString.upper())
        self.titleLine.composite_op = "blacksrc"
        layers.append(self.titleLine)
        self.selectionLine = dmd.TextLayer(64,14,self.game.assets.font_9px_az,"center").set_text(selectionString)
        layers.append(self.selectionLine)
        self.infoLine = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center")
        if blinkInfo:
            self.infoLine.set_text(infoString,blink_frames=30)
        else:
            self.infoLine.set_text(infoString)
        layers.append(self.infoLine)
        self.layer = dmd.GroupedLayer(128,32,layers)


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
                mode_to_add = None
                if selection == "TESTS":
                    mode_to_add = NewServiceModeTests(game=self.game,priority=201)
                elif selection == "SETTINGS":
                    mode_to_add = NewServiceModeSettings(game=self.game,priority=201)
                elif selection == "STATS":
                    mode_to_add = NewServiceModeStats(game=self.game,priority=201)
                elif selection == "UTILITIES":
                    mode_to_add = NewServiceModeUtilities(game=self.game,priority=201)
                elif selection == "UPDATE":
                    mode_to_add = NewServiceModeUpdate(game=self.game,priority=201)
                elif selection == "SHUTDOWN":
                    self.update_display("","SHUTTING DOWN")
                    print "Powering off"
                    # exit with error code 69
                    sys.exit(69)
                else:
                    pass
                if mode_to_add:
                    self.game.modes.add(mode_to_add)
            else:
                pass
        return game.SwitchStop

    def sw_up_active(self,sw):
        if self.activeMode == "MENU":
            if not self.busy:
            # play the sound for moving down
                self.game.sound.play(self.game.assets.sfx_menuUp)
                self.item_up()
        else:
            pass

        return game.SwitchStop

    def sw_down_active(self,sw):
        if self.activeMode == "MENU":
            if not self.busy:
            # play the sound for moving down
                self.game.sound.play(self.game.assets.sfx_menuDown)
                self.item_down()
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
        self.section = ["SWITCHES","SINGLE LAMPS", "ALL LAMPS","SOLENOIDS","FLASHERS","DROP TARGETS","MINE","TRAIN"]
        self.update_display("Tests",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_menuEnter)
        selection = self.section[self.index]
        mode_to_add = None
        if selection == "SWITCHES":
            mode_to_add = NewServiceModeSwitchEdges(game=self.game,priority=202)
        elif selection == "DROP TARGETS":
            mode_to_add = NewServiceModeDropTargets(game=self.game,priority=202)
        elif selection == "MINE":
            mode_to_add = NewServiceModeMine(game=self.game,priority=202)
        elif selection == "ALL LAMPS":
            mode_to_add = NewServiceModeAllLamps(game=self.game,priority=202)
        elif selection == "SINGLE LAMPS":
            mode_to_add = NewServiceModeSingleLamps(game=self.game,priority=202)
        elif selection == "FLASHERS":
            mode_to_add = NewServiceModeFlashers(game=self.game,priority=202)
        elif selection == "SOLENOIDS":
            mode_to_add = NewServiceModeSolenoids(game=self.game,priority=202)
        elif selection == "TRAIN":
            mode_to_add = NewServiceModeTrain(game=self.game,priority=202)
        else:
            pass
        if mode_to_add:
           self.game.modes.add(mode_to_add)
        return game.SwitchStop

##   ____          _ _       _       _____         _
##  / ___|_      _(_) |_ ___| |__   |_   _|__  ___| |_
##  \___ \ \ /\ / / | __/ __| '_ \    | |/ _ \/ __| __|
##   ___) \ V  V /| | || (__| | | |   | |  __/\__ \ |_
##  |____/ \_/\_/ |_|\__\___|_| |_|   |_|\___||___/\__|

class NewServiceModeSwitchEdges(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeSwitchEdges, self).__init__(game, priority)
        self.myID = "Service Mode Switch Test"
        self.index = 0

    def mode_started(self):
        self.rowColors = ["","WHT-BRN","WHT-RED","WHT-ORG","WHT-YEL","WHT-GRN","WHT-BLU","WHT-VLT","WHT-GRY"]
        self.colColors = ["","GRN-BRN","GRN-RED","GRN-ORG","GRN-WHT","GRN-BLK","GRN-BLU","GRN-VLT","GRN-GRY"]
        self.dedColors = ["","ORG-BRN","ORG-RED","ORG-BLK","ORG-YEL","ORG-GRN","ORG-BLU","ORG-VLT","ORG-GRY"]
        self.grndColors = ["","BLK-GRN","BLU-VLT","BLK-BLU","BLU-GRY","BLK-VLT","BLK-YEL","BLK-GRY","BLK-BLU"]
        self.row1text = "a-aaaaaaaa-a"
        self.row2text = "a-aaaaaaaa-a"
        self.row3text = "a-aaaaaaaa-a"
        self.row4text = "a-aaaaaaaa-a"
        self.row5text = "a-aaaaaaaa-a"
        self.row6text = "a-aaaaaaaa-a"
        self.row7text = "a-aaaaaaaa-a"
        self.row8text = "a-aaaaaaaa-a"
        # build the display
        self.update_display()
        # make a list of the row layers
        self.rowStrings = [None,self.row1text,self.row2text,self.row3text,self.row4text,self.row5text,self.row6text,self.row7text,self.row8text]
        # setup the switches
        for switch in self.game.switches:
            if self.game.machine_type == 'sternWhitestar':
                add_handler = 1
            elif switch != self.game.switches.exit:
                add_handler = 1
            else:
                add_handler = 0
            if add_handler:
                self.add_switch_handler(name=switch.name, event_type='inactive', delay=None, handler=self.switch_handler)
                self.add_switch_handler(name=switch.name, event_type='active', delay=None, handler=self.switch_handler)
            # set the switch to active on the grid if active
                if switch.is_active():
                    self.update_row(switch,"A")

    def switch_handler(self, sw):
        # set the row & col ints
        myRow = int(sw.tags[2])
        myCol = int(sw.tags[1])

        if (sw.state):
            self.game.sound.play(self.game.assets.sfx_menuSwitchEdge)
            # set the label text
            self.labelText.set_text(str(sw.label).upper())
            # set the row wire color text
            self.rowText.set_text(str(self.rowColors[myRow]))
            # set the column color if applicable
            if myCol != 0:
                self.colText.set_text(str(self.colColors[myCol]))
            else:
                self.colText.set_text("GROUND")
            # update the proper string position
            if "Grounded" in sw.tags:
                # set the last switch text string
                lastString = "LAST SWITCH: F" + sw.tags[2]
                self.lastText.set_text(lastString)
            elif "Dedicated" in sw.tags:
                # set the last switch text string
                lastString = "LAST SWITCH: D" + sw.tags[2]
                self.lastText.set_text(lastString)
            else:
                lastString = "LAST SWITCH: " + sw.tags[1] + sw.tags[2]
                self.lastText.set_text(lastString)
            self.update_row(sw,"A")
        else:
            # clear the label text
            self.labelText.set_text("")
            # turn off the row
            self.update_row(sw,"a")
        return game.SwitchStop

    def update_row(self,sw,char):
        myRow = int(sw.tags[2])
        myCol = int(sw.tags[1])
        left = myCol + 1
        right = myCol + 2
        # substitute the row position
        if "Grounded" in sw.tags:
            # grounded switch slice
            self.rowStrings[myRow] = char + self.rowStrings[myRow][1:]
        elif "Dedicated" in sw.tags:
            # dedicated switch slice
            self.rowStrings[myRow] = self.rowStrings[myRow][:11] + char
        else:
            # standard switch slice
            self.rowStrings[myRow] = self.rowStrings[myRow][:left] + char + self.rowStrings[myRow][right:]
            # then update the row text
        self.rowLayers[myRow].set_text(self.rowStrings[myRow])

    def sw_enter_active(self,sw):
        self.switch_handler(sw)
        return game.SwitchStop

    # redefine the exit switch so we can get out
    def sw_exit_active(self,sw):
        if not self.busy:
            self.game.sound.play(self.game.assets.sfx_menuExit)
            self.unload()
        return game.SwitchStop

    def sw_up_active(self,sw):
        self.switch_handler(sw)
        return game.SwitchStop

    def sw_down_active(self,sw):
        self.switch_handler(sw)
        return game.SwitchStop

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_switchMatrix.frames[0])
        layers.append(background)
        self.switchRow1 = dmd.TextLayer(0,4,self.game.assets.font_matrix,"left").set_text(self.row1text)
        self.switchRow1.composite_op = "blacksrc"
        layers.append(self.switchRow1)
        self.switchRow2 = dmd.TextLayer(0,7,self.game.assets.font_matrix,"left").set_text(self.row2text)
        self.switchRow2.composite_op = "blacksrc"
        layers.append(self.switchRow2)
        self.switchRow3 = dmd.TextLayer(0,10,self.game.assets.font_matrix,"left").set_text(self.row3text)
        self.switchRow3.composite_op = "blacksrc"
        layers.append(self.switchRow3)
        self.switchRow4 = dmd.TextLayer(0,13,self.game.assets.font_matrix,"left").set_text(self.row4text)
        self.switchRow4.composite_op = "blacksrc"
        layers.append(self.switchRow4)
        self.switchRow5 = dmd.TextLayer(0,16,self.game.assets.font_matrix,"left").set_text(self.row5text)
        self.switchRow5.composite_op = "blacksrc"
        layers.append(self.switchRow5)
        self.switchRow6 = dmd.TextLayer(0,19,self.game.assets.font_matrix,"left").set_text(self.row6text)
        self.switchRow6.composite_op = "blacksrc"
        layers.append(self.switchRow6)
        self.switchRow7 = dmd.TextLayer(0,22,self.game.assets.font_matrix,"left").set_text(self.row7text)
        self.switchRow7.composite_op = "blacksrc"
        layers.append(self.switchRow7)
        self.switchRow8 = dmd.TextLayer(0,25,self.game.assets.font_matrix,"left").set_text(self.row8text)
        self.switchRow8.composite_op = "blacksrc"
        layers.append(self.switchRow8)
        title = dmd.TextLayer(81,0,self.game.assets.font_5px_AZ,"center").set_text("SWITCH EDGES")
        layers.append(title)
        self.rowText = dmd.TextLayer(35,26,self.game.assets.font_5px_AZ,"left").set_text("")
        layers.append(self.rowText)
        self.colText = dmd.TextLayer(125,26,self.game.assets.font_5px_AZ,"right").set_text("")
        layers.append(self.colText)
        self.lastText = dmd.TextLayer(81,18,self.game.assets.font_5px_AZ,"center").set_text("")
        layers.append(self.lastText)
        self.labelText = dmd.TextLayer(81,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("")
        self.labelText.composite_op = "blacksrc"
        layers.append(self.labelText)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined
        self.rowLayers = [None,self.switchRow1,self.switchRow2,self.switchRow3,self.switchRow4,self.switchRow5,self.switchRow6,self.switchRow7,self.switchRow8]

##   ____  _             _        _                            _____         _
##  / ___|(_)_ __   __ _| | ___  | |    __ _ _ __ ___  _ __   |_   _|__  ___| |_
##  \___ \| | '_ \ / _` | |/ _ \ | |   / _` | '_ ` _ \| '_ \    | |/ _ \/ __| __|
##   ___) | | | | | (_| | |  __/ | |__| (_| | | | | | | |_) |   | |  __/\__ \ |_
##  |____/|_|_| |_|\__, |_|\___| |_____\__,_|_| |_| |_| .__/    |_|\___||___/\__|
##                 |___/                              |_|

class NewServiceModeSingleLamps(NewServiceSkeleton):
    """Service Mode Single Lamp Test."""
    def __init__(self, game, priority):
        super(NewServiceModeSingleLamps, self).__init__(game, priority)
        self.myID = "Service Mode Single Lamps Test"
        self.section = []
        for lamp in self.game.lamps:
            if lamp.label:
                self.section.append(lamp)

    def mode_started(self):
        self.callback = self.change_lamp
        self.index = 0
        self.mode = 0
        self.update_display()
        self.change_lamp()

    def mode_stopped(self):
        # Kill the lights
        for lamp in self.section:
            lamp.disable()

    def sw_enter_active(self,sw):
        if self.mode == 0:
            self.mode = 1
            self.infoLine.set_text("SOLID ON")
        else:
            self.mode = 0
            self.infoLine.set_text("FLASHING",blink_frames=30)
        # refresh the lamp
        self.change_lamp()
        return game.SwitchStop

    def change_lamp(self):
        lamp = self.section[self.index]
        lampString = lamp.label.upper()
        print "Change Lamp " + lamp.name + " - " + lampString
        # kill everything!
        for everyLamp in self.section:
            everyLamp.disable()
        # then update the display
        self.lampName.set_text(lampString)
        # if we're flashing, schedule the new one
        if self.mode == 0:
            lamp.schedule(0x0000FFFF)
        else:
            lamp.enable()

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("SINGLE LAMPS")
        layers.append(title)
        self.lampName = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("")
        self.lampName.composite_op = "blacksrc"
        layers.append(self.lampName)
        instructions = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("+/- TO SELECT LAMP")
        instructions2 = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("'ENTER' TO CHANGE MODE")
        script = []
        script.append({'seconds':2,'layer':instructions})
        script.append({'seconds':2,'layer':instructions2})
        instruction_duo = dmd.ScriptedLayer(128,32,script)
        instruction_duo.composite_op = "blacksrc"
        layers.append(instruction_duo)
        self.infoLine = dmd.TextLayer(64,21,self.game.assets.font_7px_az,"center").set_text("FLASHING",blink_frames=30)
        layers.append(self.infoLine)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined


##
##      _    _ _   _                                _____         _
##     / \  | | | | |    __ _ _ __ ___  _ __  ___  |_   _|__  ___| |_
##    / _ \ | | | | |   / _` | '_ ` _ \| '_ \/ __|   | |/ _ \/ __| __|
##   / ___ \| | | | |__| (_| | | | | | | |_) \__ \   | |  __/\__ \ |_
##  /_/   \_\_|_| |_____\__,_|_| |_| |_| .__/|___/   |_|\___||___/\__|
##                                     |_|

class NewServiceModeAllLamps(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeAllLamps, self).__init__(game, priority)
        self.myID = "Service Mode All Lamps Test"
        self.index = 0
        self.mode = 0

    def mode_started(self):
        self.update_display()
        self.update_mode()

    def mode_stopped(self):
        for lamp in self.game.lamps:
            lamp.disable()

    def sw_enter_active(self,sw):
        self.update_mode()
        return game.SwitchStop

    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

    def update_mode(self):
        if self.mode == 0:
            self.mode = 1
            for lamp in self.game.lamps:
                lamp.schedule(0x0000FFFF)
            self.infoLine.set_text("FLASHING",blink_frames=30)
        else:
            self.mode = 0
            for lamp in self.game.lamps:
                lamp.enable()
            self.infoLine.set_text("SOLID ON")

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("ALL LAMPS")
        layers.append(title)
        targetLine = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("'ENTER' TO CHANGE MODE")
        targetLine.composite_op = "blacksrc"
        layers.append(targetLine)
        self.infoLine = dmd.TextLayer(64,16,self.game.assets.font_12px_az,"center").set_text("FLASHING",blink_frames=30)
        layers.append(self.infoLine)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined

##   ____        _                  _     _   _____         _
##  / ___|  ___ | | ___ _ __   ___ (_) __| | |_   _|__  ___| |_
##  \___ \ / _ \| |/ _ \ '_ \ / _ \| |/ _` |   | |/ _ \/ __| __|
##   ___) | (_) | |  __/ | | | (_) | | (_| |   | |  __/\__ \ |_
##  |____/ \___/|_|\___|_| |_|\___/|_|\__,_|   |_|\___||___/\__|

class NewServiceModeSolenoids(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeSolenoids, self).__init__(game, priority)
        self.myID = "Service Mode Solenoids Test"
        self.index = 0
        self.section = []
        # grab the solenoids from the coil list
        for solenoid in self.game.coils:
            if "Solenoid" in solenoid.tags:
                self.section.append(solenoid)

    def mode_started(self):
        self.callback = self.change_coil
        self.mode = 0
        self.update_display()
        self.change_coil()

    def mode_stopped(self):
        for coil in self.section:
            coil.disable()

    def sw_enter_active(self,sw):
        if self.mode == 0:
            self.mode = 1
            self.infoLine.set_text("REPEAT")
        else:
            self.mode = 0
            self.infoLine.set_text("STOPPED")
        self.change_coil()
        return game.SwitchStop

    def change_coil(self):
        coil = self.section[self.index]
        coilString = coil.label.upper()
        # kill everything!
        for everyCoil in self.section:
            everyCoil.disable()
        # then update the display
        self.coilName.set_text(coilString)
        # if we're running, schedule the new one
        if self.mode == 1:
            coil.schedule(0x00000001)
        else:
            coil.disable()

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("SOLENOIDS")
        layers.append(title)
        self.coilName = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("")
        self.coilName.composite_op = "blacksrc"
        layers.append(self.coilName)
        instructions = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("+/- TO SELECT SOLENOID")
        instructions2 = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("'ENTER' TO CHANGE MODE")
        script = []
        script.append({'seconds':2,'layer':instructions})
        script.append({'seconds':2,'layer':instructions2})
        instruction_duo = dmd.ScriptedLayer(128,32,script)
        instruction_duo.composite_op = "blacksrc"
        layers.append(instruction_duo)
        self.infoLine = dmd.TextLayer(64,21,self.game.assets.font_7px_az,"center").set_text("STOPPED")
        layers.append(self.infoLine)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined

##   _____ _           _                 _____         _
##  |  ___| | __ _ ___| |__   ___ _ __  |_   _|__  ___| |_
##  | |_  | |/ _` / __| '_ \ / _ \ '__|   | |/ _ \/ __| __|
##  |  _| | | (_| \__ \ | | |  __/ |      | |  __/\__ \ |_
##  |_|   |_|\__,_|___/_| |_|\___|_|      |_|\___||___/\__|

class NewServiceModeFlashers(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeFlashers, self).__init__(game, priority)
        self.myID = "Service Mode Flashers Test"
        self.index = 0
        self.section = []
        # grab the flashers from the coil list
        for flasher in self.game.coils:
            if "Flasher" in flasher.tags:
                self.section.append(flasher)

    def mode_started(self):
        self.callback = self.change_flasher
        self.update_display()
        self.change_flasher()

    def mode_stopped(self):
        for flasher in self.section:
            flasher.disable()

    def sw_enter_active(self,sw):
        # null the enter button
        return game.SwitchStop

    def change_flasher(self):
        flasher = self.section[self.index]
        flasherString = flasher.label.upper()
        # kill everything!
        for everyflasher in self.section:
            everyflasher.disable()
            # then update the display
        self.flasherName.set_text(flasherString)
        # if we're flashing, schedule the new one
        flasher.schedule(0x00010001)

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("FLASHERS")
        layers.append(title)
        self.flasherName = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("")
        self.flasherName.composite_op = "blacksrc"
        layers.append(self.flasherName)
        instructions = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("+/- TO SELECT FLASHER")
        layers.append(instructions)
        self.infoLine = dmd.TextLayer(64,21,self.game.assets.font_7px_az,"center").set_text("FLASHING",blink_frames=30)
        layers.append(self.infoLine)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined


##   ____                    _____                    _         _____         _
##  |  _ \ _ __ ___  _ __   |_   _|_ _ _ __ __ _  ___| |_ ___  |_   _|__  ___| |_
##  | | | | '__/ _ \| '_ \    | |/ _` | '__/ _` |/ _ \ __/ __|   | |/ _ \/ __| __|
##  | |_| | | | (_) | |_) |   | | (_| | | | (_| |  __/ |_\__ \   | |  __/\__ \ |_
##  |____/|_|  \___/| .__/    |_|\__,_|_|  \__, |\___|\__|___/   |_|\___||___/\__|
##                  |_|                    |___/

class NewServiceModeDropTargets(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeDropTargets, self).__init__(game, priority)
        self.myID = "Service Mode Drop Target Test"
        self.index = 0
        self.targets = ["LEFT DROP TARGET","LEFT CENTER DROP TARGET","RIGHT CENTER DROP TARGET","RIGHT DROP TARGET"]
        self.coils = [self.game.coils.badGuyC0,
                      self.game.coils.badGuyC1,
                      self.game.coils.badGuyC2,
                      self.game.coils.badGuyC3]

    def mode_started(self):
        self.update_display()
        self.targetUp = [False,False,False,False]
        self.on_time = self.game.user_settings['Machine (Standard)']['Drop Target Boost']

    def sw_exit_active(self,sw):
        if not self.busy:
            self.game.sound.play(self.game.assets.sfx_menuExit)
            self.drop_targets()
            self.unload()
        return game.SwitchStop

    def sw_up_active(self,sw):
        print "Targets:"
        print self.targetUp
        self.index += 1
        if self.index > 3:
            self.index = 0
        print "Index is: " + str(self.index)
        self.targetLine.set_text(self.targets[self.index])
        self.update_instruction(self.index)
        return game.SwitchStop

    def sw_down_active(self,sw):
        print "Targets:"
        print self.targetUp
        self.index -= 1
        if self.index < 0:
            self.index = 3
        print "Index is: " + str(self.index)
        self.targetLine.set_text(self.targets[self.index])
        self.update_instruction(self.index)
        return game.SwitchStop

    def sw_enter_active(self,sw):
        print "Enter Pressed"
        print "Index is: " + str(self.index)
        print "targetUp is: " + str(self.targetUp[self.index])
        # if the selected target is down
        if self.targetUp[self.index] == False:
            # raise the target
            print "Raise target " + str(self.index)
            self.target_up(self.index)
            # update the insruction line
        else:
            print "Target is up, killing target"
            print "Lower Target" +  str(self.index)
            self.target_down(self.index)
        return game.SwitchStop

    def sw_badGuySW0_active(self,sw):
        # far left bad guy target
        if self.targetUp[0]:
            self.update_box(0)
        return game.SwitchStop

    def sw_badGuySW0_inactive_for_180ms(self,sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc:
            self.target_activate(0)
            self.update_box(0)
        return game.SwitchStop

    def sw_badGuySW1_active(self,sw):
        # center left badguy target
        if self.targetUp[1]:
            self.update_box(1)
        return game.SwitchStop

    def sw_badGuySW1_inactive_for_180ms(self,sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc:
            self.target_activate(1)
            self.update_box(1)
        return game.SwitchStop

    def sw_badGuySW2_active(self,sw):
        # center right bad guy target
        if self.targetUp[2]:
            self.update_box(2)
        return game.SwitchStop

    def sw_badGuySW2_inactive_for_180ms(self,sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc:
            self.target_activate(2)
            self.update_box(2)
        return game.SwitchStop

    def sw_badGuySW3_active(self,sw):
        # far right bad guy target
        if self.targetUp[3]:
            self.update_box(3)
        return game.SwitchStop

    def sw_badGuySW3_inactive_for_180ms(self,sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc:
            self.target_activate(3)
            self.update_box(3)
        return game.SwitchStop

    def update_box(self,target):
        print "Updating checkbox " + str(target)
        boxes = [self.box0,self.box1,self.box2,self.box3]
        # if the bad guy is down, the box is empty
        if self.targetUp[target] == False:
            boxes[target].set_text("b")
        else:
            boxes[target].set_text("a")

    def update_instruction(self,target):
        print "Update instruction for target " + str(target) + "Target val: " + str(self.targetUp[target])
        if self.targetUp[target] == False:
            self.instructionLine.set_text("PRESS ENTER TO RAISE TARGET")
        else:
            self.instructionLine.set_text("PRESS ENTER TO LOWER TARGET")


    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("DROP TARGETS")
        layers.append(title)
        self.targetLine = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text(str(self.targets[self.index]))
        self.targetLine.composite_op = "blacksrc"
        layers.append(self.targetLine)
        self.instructionLine = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ,"center").set_text("PRESS ENTER TO RAISE TARGET")
        layers.append(self.instructionLine)
        label0 = dmd.TextLayer(16,20,self.game.assets.font_5px_AZ,"center").set_text("SW.61")
        layers.append(label0)
        label1 = dmd.TextLayer(48,20,self.game.assets.font_5px_AZ,"center").set_text("SW.62")
        layers.append(label1)
        label2 = dmd.TextLayer(80,20,self.game.assets.font_5px_AZ,"center").set_text("SW.63")
        layers.append(label2)
        label3 = dmd.TextLayer(112,20,self.game.assets.font_5px_AZ,"center").set_text("SW.64")
        layers.append(label3)
        self.box0 = dmd.TextLayer(16,26,self.game.assets.font_5px_AZ,"center").set_text("b")
        layers.append(self.box0)
        self.box1 = dmd.TextLayer(48,26,self.game.assets.font_5px_AZ,"center").set_text("b")
        layers.append(self.box1)
        self.box2 = dmd.TextLayer(80,26,self.game.assets.font_5px_AZ,"center").set_text("b")
        layers.append(self.box2)
        self.box3 = dmd.TextLayer(112,26,self.game.assets.font_5px_AZ,"center").set_text("b")
        layers.append(self.box3)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined

    # raise target
    def target_up(self,target):
        print "TARGET RAISED " + str(target)
        # new coil raise based on research with on o-scope by jim (jvspin)
        self.coils[target].patter(on_time=2,off_time=2,original_on_time=self.on_time)
        # If fakepinproc is true, activate the target right away
        if self.game.fakePinProc:
            self.target_activate(target)

    # drop target
    def target_down(self,target):
        print "DEACTIVATING TARGET " + str(target)
        self.coils[target].disable()
        self.targetUp[target] = False
        self.update_box(target)
        self.update_instruction(target)
        print "Targets:"
        print self.targetUp

    def target_activate(self,target):
        if self.targetUp[target] == False:
            print "ACTIVATING TARGET " + str(target)
            self.coils[target].patter(on_time=2,off_time=10)
            self.targetUp[target] = True
            if self.game.fakePinProc:
                self.update_box(target)
                self.update_instruction(target)
        print "Targets:"
        print self.targetUp


    def drop_targets(self):
        # drop all teh targets
        for i in range(0,4,1):
            self.target_down(i)

##   __  __ _              _____         _
##  |  \/  (_)_ __   ___  |_   _|__  ___| |_
##  | |\/| | | '_ \ / _ \   | |/ _ \/ __| __|
##  | |  | | | | | |  __/   | |  __/\__ \ |_
##  |_|  |_|_|_| |_|\___|   |_|\___||___/\__|

class NewServiceModeMine(NewServiceSkeleton):
    """Service Mode Tests Section."""
    def __init__(self, game, priority):
        super(NewServiceModeMine, self).__init__(game, priority)
        self.myID = "Service Mode Mine Test"
        self.index = 0

    def mode_started(self):
        self.kickStrength = self.game.user_settings['Machine (Standard)']['Mine Kicker Strength']
        self.update_display()
        self.inMotion = False
        self.resetFlag = False


    def sw_enter_active(self,sw):
        self.reset()
        return game.SwitchStop

    def sw_up_active(self,sw):
        self.jog()
        return game.SwitchStop

    def sw_down_active(self,sw):
        self.jog()
        return game.SwitchStop

    # entrance switch
    def sw_mineEntrance_active(self,sw):
        self.box0.set_text("b")
        self.game.sound.play(self.game.assets.sfx_menuSwitchEdge)
        return game.SwitchStop

    def sw_mineEntrance_inactive(self,sw):
        self.box0.set_text("a")
        return game.SwitchStop

    # popper
    def sw_minePopper_active(self,sw):
        self.busy = True
        self.box1.set_text("b")
        self.game.sound.play(self.game.assets.sfx_menuSwitchEdge)
        return game.SwitchStop

    def sw_minePopper_active_for_1000ms(self,sw):
        self.clear_mine()
        return game.SwitchStop

    def clear_mine(self):
        if self.game.switches.coinDoorClosed.is_active():
            self.game.coils.minePopper.pulse(self.kickStrength)
            self.busy = False
            self.instructionLine.set_text("+/- TO JOG   'ENTER' TO HOME")
        # If the door isn't closed, we can't kick
        else:
            self.instructionLine.set_text("CLOSE DOOR OR HOLD DOOR SWITCH",blink_frames=15)
            self.game.sound.play(self.game.assets.sfx_menuReject)
            # loop back in 1 second to try again
            self.delay(delay=1,handler=self.clear_mine)


    def sw_minePopper_inactive(self,sw):
        self.box1.set_text("a")
        return game.SwitchStop

    # encoder opto
    def sw_mineEncoder_active(self,sw):
        self.box2.set_text("b")
        return game.SwitchStop

    def sw_mineEncoder_inactive(self,sw):
        self.box2.set_text("a")
        return game.SwitchStop

    # home opto
    def sw_mineHome_active(self,sw):
        if self.resetFlag:
            self.stop()
            self.resetFlag = False
            self.game.sound.play(self.game.assets.sfx_menuSwitchEdge)
            self.box3.set_text("b")
        return game.SwitchStop

    def sw_mineHome_inactive(self,sw):
        self.box3.set_text("a")
        return game.SwitchStop


    def jog(self):
        if not self.inMotion:
            self.inMotion = True
            self.game.coils.mineMotor.enable()
            self.delay(delay=1,handler=self.stop)
        else:
            pass

    def stop(self):
        self.game.coils.mineMotor.disable()
        self.inMotion = False

    def reset(self):
        if not self.inMotion:
            self.resetFlag = True
            self.inMotion = True
            self.game.coils.mineMotor.enable()

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("MINE TEST")
        layers.append(title)
        self.instructionLine = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("+/- TO JOG   'ENTER' TO HOME")
        self.instructionLine.composite_op = "blacksrc"
        layers.append(self.instructionLine)
        name0 = dmd.TextLayer(16,14,self.game.assets.font_5px_AZ,"center").set_text("ENTER")
        layers.append(name0)
        name1 = dmd.TextLayer(47,14,self.game.assets.font_5px_AZ,"center").set_text("POPPER")
        layers.append(name1)
        name2 = dmd.TextLayer(81,14,self.game.assets.font_5px_AZ,"center").set_text("ENCODE")
        layers.append(name2)
        name3 = dmd.TextLayer(112,14,self.game.assets.font_5px_AZ,"center").set_text("HOME")
        layers.append(name3)
        label0 = dmd.TextLayer(16,20,self.game.assets.font_5px_AZ,"center").set_text("SW.15")
        layers.append(label0)
        label1 = dmd.TextLayer(47,20,self.game.assets.font_5px_AZ,"center").set_text("SW.41")
        layers.append(label1)
        label2 = dmd.TextLayer(81,20,self.game.assets.font_5px_AZ,"center").set_text("SW.78")
        layers.append(label2)
        label3 = dmd.TextLayer(112,20,self.game.assets.font_5px_AZ,"center").set_text("SW.77")
        layers.append(label3)
        self.box0 = dmd.TextLayer(16,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        if self.game.switches.mineEntrance.is_active():
            self.box0.set_text("b")
        layers.append(self.box0)
        self.box1 = dmd.TextLayer(47,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        if self.game.switches.minePopper.is_active():
            self.box1.set_text("b")
        layers.append(self.box1)
        self.box2 = dmd.TextLayer(81,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        if self.game.switches.mineEncoder.is_active():
            self.box2.set_text("b")
        layers.append(self.box2)
        self.box3 = dmd.TextLayer(112,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        if self.game.switches.mineHome.is_active():
            self.box3.set_text("b")
        layers.append(self.box3)
        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined

##   _____          _         _____         _
##  |_   _| __ __ _(_)_ __   |_   _|__  ___| |_
##    | || '__/ _` | | '_ \    | |/ _ \/ __| __|
##    | || | | (_| | | | | |   | |  __/\__ \ |_
##    |_||_|  \__,_|_|_| |_|   |_|\___||___/\__|

class NewServiceModeTrain(NewServiceSkeleton):
    """Service Mode Train Test."""
    def __init__(self, game, priority):
        super(NewServiceModeTrain, self).__init__(game, priority)
        self.myID = "Service Mode Settings"
        self.index = 0

    def mode_started(self):
        self.mode = 0
        self.update_display()
        self.inMotion = False

    def mode_stopped(self):
        # just in case
        self.stop()

    def sw_enter_active(self,sw):
        if self.mode == 0:
            self.mode = 1
            self.speedLayer.set_text("SPEED: FAST")
        else:
            self.mode = 0
            self.speedLayer.set_text("SPEED: SLOW")
        return game.SwitchStop

    def sw_up_active(self,sw):
        if not self.inMotion:
            self.move("FORWARD")
        return game.SwitchStop

    def sw_up_inactive(self,sw):
        self.stop()
        return game.SwitchStop

    def sw_down_active(self,sw):
        if not self.inMotion:
            self.move("BACKWARD")
        return game.SwitchStop

    def sw_down_inactive(self,sw):
        self.stop()
        return game.SwitchStop

    def sw_trainHome_active(self,sw):
        self.stop()
        self.box1.set_text('HOME b')
        return game.SwitchStop

    def sw_trainHome_inactive(self,sw):
        self.box1.set_text('HOME a')
        return game.SwitchStop

    def sw_trainEncoder_active(self,sw):
        self.box0.set_text('ENCODER b')
        return game.SwitchStop

    def sw_trainEncoder_inactive(self,sw):
        self.box0.set_text('ENCODER a')
        return game.SwitchStop

    def stop(self):
        self.game.coils.trainForward.disable()
        self.game.coils.trainReverse.disable()
        self.inMotion = False
        self.directionLayer.set_text("STOPPED")

    def move(self,direction):
        self.inMotion = True
        self.directionLayer.set_text(direction)
        if direction == "FORWARD":
            coil = self.game.coils.trainForward
        else:
            coil = self.game.coils.trainReverse

        # if we're trying to back up, but already home - don't do that
        if direction == "BACKWARD" and self.game.switches.trainHome.is_active():
            self.inMotion = False
        else:
            if self.mode == 0:
                coil.patter(on_time=6,off_time=6)
            else:
                coil.enable()

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text("TRAIN TEST")
        layers.append(title)
        self.speedLayer = dmd.TextLayer(32,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("SPEED: SLOW")
        self.speedLayer.composite_op = "blacksrc"
        layers.append(self.speedLayer)
        dash = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("-")
        dash.composite_op = "blacksrc"
        layers.append(dash)
        self.directionLayer = dmd.TextLayer(96,7,self.game.assets.font_5px_AZ_inverted,"center").set_text("STOPPED")
        self.directionLayer.composite_op = "blacksrc"
        layers.append(self.directionLayer)
        instructions = dmd.TextLayer(64,16,self.game.assets.font_5px_AZ,"center").set_text("HOLD + TO GO FORWARD")
        instructions2 = dmd.TextLayer(64,16,self.game.assets.font_5px_AZ,"center").set_text("HOLD - TO GO BACKWARD")
        instructions3 = dmd.TextLayer(64,16,self.game.assets.font_5px_AZ,"center").set_text("'ENTER' TO CHANGE SPEED")
        script = []
        script.append({'seconds':2,'layer':instructions})
        script.append({'seconds':2,'layer':instructions2})
        script.append({'seconds':2,'layer':instructions3})
        instruction_trio = dmd.ScriptedLayer(128,32,script)
        instruction_trio.composite_op = "blacksrc"
        layers.append(instruction_trio)
        self.box0 = dmd.TextLayer(13,24,self.game.assets.font_5px_AZ,"left").set_text("ENCODER a")
        if self.game.switches.trainEncoder.is_active():
            self.box0.set_text("ENCODER b")
        layers.append(self.box0)
        self.box1 = dmd.TextLayer(78,24,self.game.assets.font_5px_AZ,"left").set_text("HOME a")
        if self.game.switches.trainHome.is_active():
            self.box1.set_text("HOME b")
        layers.append(self.box1)
        combined = dmd.GroupedLayer(128,32,layers)
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
        self.section = ["STANDARD","FEATURE","AUDIO","CUSTOM MESSAGE"]
        self.update_display("Settings",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_menuEnter)
        if self.section[self.index] == "STANDARD":
            selection = "Machine (Standard)"
        elif self.section[self.index] == "FEATURE":
            selection = "Gameplay (Feature)"
        elif self.section[self.index] == "CUSTOM MESSAGE":
            selection = "Custom Message"
        else:
            selection = "Sound"
        mode_to_add = NewServiceModeSettingsEditor(game=self.game,priority=202,itemlist=self.game.settings[selection],name=selection)
        self.game.modes.add(mode_to_add)
        return game.SwitchStop

##   ____       _   _   _                   _____    _ _ _
##  / ___|  ___| |_| |_(_)_ __   __ _ ___  | ____|__| (_) |_ ___  _ __
##  \___ \ / _ \ __| __| | '_ \ / _` / __| |  _| / _` | | __/ _ \| '__|
##   ___) |  __/ |_| |_| | | | | (_| \__ \ | |__| (_| | | || (_) | |
##  |____/ \___|\__|\__|_|_| |_|\__, |___/ |_____\__,_|_|\__\___/|_|
##                              |___/

class NewServiceModeSettingsEditor(NewServiceSkeleton):
    """Service Mode Settings Section."""
    def __init__(self, game, priority,itemlist,name):
        super(NewServiceModeSettingsEditor, self).__init__(game, priority)
        self.myID = "Service Mode Settings Editor"
        self.index = 0
        self.name = name
        self.title = name + " Settings"
        print self.title
        self.items = []
        for item in sorted(itemlist.iterkeys()):
            if 'increments' in itemlist[item]:
                num_options = (itemlist[item]['options'][1]-itemlist[item]['options'][0]) / itemlist[item]['increments']
                option_list = []
                for i in range(0,num_options):
                    option_list.append(itemlist[item]['options'][0] + (i * itemlist[item]['increments']))
                self.items.append( EditItem(str(item), option_list, self.game.user_settings[self.name][item]) )
            else:
                self.items.append( EditItem(str(item), itemlist[item]['options'], self.game.user_settings[self.name][item]) )

    def mode_started(self):
        self.state = 'nav'
        self.item = self.items[0]
        self.option_index = self.item.options.index(self.item.value)
        self.update_display()

    def sw_enter_active(self,sw):
        if self.state == 'nav':
            self.game.sound.play(self.game.assets.sfx_menuEnter)
            self.state = 'edit'
            self.revert_value = self.item.value
            if self.items[self.index].name.endswith('Text'):
                print "This is a text entry"
                self.state = 'text'
                self.text_entry = highscore.InitialEntryMode(game=self.game, priority=self.priority+1, left_text=self.items[self.index].name, right_text='', entered_handler=self.set_text,max_inits=16,extended=True)
                self.game.modes.add(self.text_entry)
            elif self.items[self.index].name.endswith('Preview'):
                print "This is a preview"
                self.state = 'preview'
                self.preview = ep.EP_MessagePreview(self.game,self.priority+1,self.item.value,self.end_preview)
                self.game.modes.add(self.preview)
            else:
                self.change_item()
                self.change_instructions()
        elif self.state == 'text' or self.state == 'preview':
            pass

        else:
            self.state = 'nav'
            self.change_item()
            self.infoLine.set_text("NOW SET TO:")
            self.game.sound.play(self.game.assets.sfx_menuSave)
            self.game.user_settings[self.name][self.item.name]=self.item.value
            self.game.save_settings()
            self.change_instructions()
        return game.SwitchStop

    def set_text(self,mode,inits):
        # set the text string - if there is none, set to NONE
        if len(inits) == 0:
            inits = "NONE"
        self.game.user_settings[self.name][self.item.name]=str(inits)
        self.game.modes.remove(self.text_entry)
        self.game.save_settings()
        self.state = 'nav'

    def end_preview(self):
        self.state = 'nav'
        self.preview.unload()

    def sw_exit_active(self,sw):
        if self.state == 'nav':
            self.game.sound.play(self.game.assets.sfx_menuExit)
            self.unload()
        elif self.state == 'preview':
            pass
        else:
            # if we're in text edit, bail and close that mode
            if self.state == 'text':
                self.game.modes.remove(self.text_entry)
            self.item.value = self.revert_value
            self.change_item()
            # don't update these lines if we're coming out of text
            if self.state != 'text':
                self.infoLine.set_text("REMAINS:")
                self.currentSetting.set_text(str(self.item.value).upper())
            self.state = 'nav'
            self.game.sound.play(self.game.assets.sfx_menuCancel)
        return game.SwitchStop

    def sw_up_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_menuUp)
        if self.state == 'nav':
            self.index += 1
            print "Up - Index size: " + str(len(self.items)) + " - Current index: " + str(self.index)
            # if we get too high, go to zero
            if self.index >= len(self.items):
                self.index = 0
                print "Passed max - index now 0"
                self.game.sound.play(self.game.assets.sfx_menuUp)
            self.change_item()
        elif self.state == 'text' or self.state == 'preview':
            pass
        else:
            self.option_index += 1
            if self.option_index >= (len(self.item.options)):
                self.option_index = 0
            self.item.value = self.item.options[self.option_index]
            self.change_item()
        return game.SwitchStop

    def sw_down_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_menuDown)
        if self.state == 'nav':
            self.index -= 1
            print "Down - Index size: " + str(len(self.items)) + " - Current index: " + str(self.index)
            # if we get below zero, loop around
            if self.index < 0:
                self.index = (len(self.items) - 1)
                print "Passed max - index now " + str(self.index)
            self.game.sound.play(self.game.assets.sfx_menuDown)
            self.change_item()
        elif self.state == 'text' or self.state == 'preview':
            pass
        else:
            self.option_index -= 1
            if self.option_index < 0:
                self.option_index = (len(self.item.options) -1)
            self.item.value = self.item.options[self.option_index]
            self.change_item()
        return game.SwitchStop

    def change_item(self):
        self.item = self.items[self.index]
        self.settingName.set_text(self.item.name.upper())

        if self.state == 'nav':
            if self.item.name.endswith('Text'):
                print "This is a text item"
                self.infoLine.set_text("ENTER TO")
                self.currentSetting.set_text(" EDIT")
            elif self.item.name.endswith('Preview'):
                self.infoLine.set_text("ENTER TO")
                self.currentSetting.set_text(" VIEW")
            else:
                self.option_index = self.item.options.index(self.item.value)
                self.infoLine.set_text("CURRENT:")
                self.currentSetting.set_text(str(self.item.value).upper())
        else:
            self.infoLine.set_text("CHANGE TO:")
            self.currentSetting.set_text(str(self.item.value).upper(),blink_frames=10)

    def change_instructions(self):
            print "Change Instructions"
            if self.state == 'nav':
                print "Nav Version"
                self.instructions.set_text("+/- TO SELECT")
                self.instructions2.set_text("'ENTER' TO MODIFY")
            else:
                print "Edit Version"
                self.instructions.set_text("+/- TO CHANGE")
                self.instructions2.set_text("'ENTER' TO SAVE")

    def update_display(self):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        layers.append(background)
        title = dmd.TextLayer(64,0,self.game.assets.font_5px_AZ,"center").set_text(self.title.upper())
        layers.append(title)
        self.settingName = dmd.TextLayer(64,7,self.game.assets.font_5px_AZ_inverted,"center").set_text(self.item.name.upper())
        self.settingName.composite_op = "blacksrc"
        layers.append(self.settingName)
        self.infoLine = dmd.TextLayer(72,14,self.game.assets.font_9px_az_mid,"right").set_text(str("CURRENT:"))
        layers.append(self.infoLine)
        self.currentSetting = dmd.TextLayer(74,14,self.game.assets.font_9px_az,"left").set_text(str(self.item.value).upper())
        layers.append(self.currentSetting)
        self.instructions = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center").set_text("+/- TO SELECT")
        self.instructions2 = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center").set_text("'ENTER' TO MODIFY")
        script = []
        script.append({'seconds':2,'layer':self.instructions})
        script.append({'seconds':2,'layer':self.instructions2})
        self.instruction_duo = dmd.ScriptedLayer(128,32,script)
        self.instruction_duo.composite_op = "blacksrc"
        layers.append(self.instruction_duo)

        combined = dmd.GroupedLayer(128,32,layers)
        self.layer = combined

# edit item object thing
class EditItem:
    """Service Mode Items."""
    def __init__(self, name, options, value):
        self.name = name
        self.options = options
        self.value = value

##   ____  _        _         ____            _   _
##  / ___|| |_ __ _| |_ ___  / ___|  ___  ___| |_(_) ___  _ __
##  \___ \| __/ _` | __/ __| \___ \ / _ \/ __| __| |/ _ \| '_ \
##   ___) | || (_| | |_\__ \  ___) |  __/ (__| |_| | (_) | | | |
##  |____/ \__\__,_|\__|___/ |____/ \___|\___|\__|_|\___/|_| |_|

class NewServiceModeStats(NewServiceSkeleton):
    """Service Stats Menu Section."""
    def __init__(self, game, priority):
        super(NewServiceModeStats, self).__init__(game, priority)
        self.myID = "Service Mode Stats Menu"
        self.index = 0

    def mode_started(self):
        # set some indexes
        self.section = ["STANDARD AUDITS","FEATURE AUDITS"]
        self.update_display("Statistics",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_menuEnter)
        selection = self.section[self.index]
        mode_to_add = None
        if selection == "STANDARD AUDITS":
            mode_to_add = NewServiceModeStatsDisplay(game=self.game,priority=202,title=selection,category="Audits")
        elif selection == "FEATURE AUDITS":
            mode_to_add = NewServiceModeStatsDisplay(game=self.game,priority=202,title=selection,category="Feature")
        else:
            pass
        if mode_to_add:
            self.game.modes.add(mode_to_add)
        return game.SwitchStop

class NewServiceModeStatsDisplay(NewServiceSkeleton):
    """Service Stats Display Section."""
    def __init__(self, game, priority,title,category):
        super(NewServiceModeStatsDisplay, self).__init__(game, priority)
        self.myID = "Service Mode Stats Display"
        self.index = 0
        self.values = []
        self.category = category
        self.title = title

    def mode_started(self):
        # grab the audits section out of the game data
        itemlist = self.game.game_data[self.category]
        # go through the audits and store the names and values
        for item in sorted(itemlist.iterkeys()):
            self.section.append(str(item).upper())
            #print "Item: " + str(item)
            self.values.append(str(itemlist[item]))
            #print "Value: " + str(itemlist[item])
        self.update_display(self.title,self.section[self.index],self.values[self.index])

    def sw_enter_active(self,sw):
        # null the enter switch
        return game.SwitchStop

    def item_down(self):
        self.index -= 1
        # if we get below zero, loop around
        if self.index < 0:
            self.index = (len(self.section) - 1)
            # then update the display
        self.selectionLine.set_text(str(self.section[self.index]))
        self.infoLine.set_text(str(self.values[self.index]))

    def item_up(self):
        self.index += 1
        # if we get too high, go to zero
        if self.index >= len(self.section):
            self.index = 0
            # then update the display
        self.selectionLine.set_text(str(self.section[self.index]))
        self.infoLine.set_text(str(self.values[self.index]))


    # standard display structure
    def update_display(self,titleString,selectionString,infoString="",blinkInfo = False):
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        background.set_target_position(0,-4)
        layers.append(background)
        self.titleLine = dmd.TextLayer(1,3,self.game.assets.font_5px_AZ_inverted,"Left").set_text(titleString.upper())
        self.titleLine.composite_op = "blacksrc"
        layers.append(self.titleLine)
        self.selectionLine = dmd.TextLayer(64,11,self.game.assets.font_9px_az,"center").set_text(selectionString)
        layers.append(self.selectionLine)
        self.infoLine = dmd.TextLayer(64,22,self.game.assets.font_7px_az,"center").set_text(infoString)
        layers.append(self.infoLine)
        self.layer = dmd.GroupedLayer(128,32,layers)

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
        self.section = ["CLEAR STD. AUDITS", "CLEAR FEAT. AUDITS", "RESET HIGH SCORES","RESTORE SETTINGS","RESET CUSTOM MSG","RESET SWITCH COUNT","EMPTY TROUGH"]
        self.update_display("Utilities",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        selection = self.section[self.index]
        mode_to_add = NewServiceModeUtility(game=self.game,priority=202,tool=selection)
        self.game.modes.add(mode_to_add)
        return game.SwitchStop

##   _   _ _   _ _ _ _              _        _   _
##  | | | | |_(_) (_) |_ _   _     / \   ___| |_(_) ___  _ __
##  | | | | __| | | | __| | | |   / _ \ / __| __| |/ _ \| '_ \
##  | |_| | |_| | | | |_| |_| |  / ___ \ (__| |_| | (_) | | | |
##   \___/ \__|_|_|_|\__|\__, | /_/   \_\___|\__|_|\___/|_| |_|
##                       |___/

class NewServiceModeUtility(NewServiceSkeleton):
    """Service Mode Utilities Section."""
    def __init__(self, game, priority,tool):
        super(NewServiceModeUtility, self).__init__(game, priority)
        self.myID = "Service Mode Utilities"
        self.tool = tool
        self.mode = 0

    def mode_started(self):
        self.game.sound.play(self.game.assets.sfx_menuReject)
        self.update_display()

    def sw_enter_active(self,sw):
        # prevent this happening more than once by setting the busy flag
        if not self.busy:
            self.busy = True
            # do the reset
            self.perform_action()
        else:
            pass
        return game.SwitchStop

    def sw_exit_active(self,sw):
        # allow to exit from clearing trough
        if not self.busy and self.tool != "EMTPY TROUGH":
            self.game.sound.play(self.game.assets.sfx_menuExit)
            self.unload()
        return game.SwitchStop

    def sw_up_active(self,sw):
        return game.SwitchStop

    def sw_down_active(self,sw):
        return game.SwitchStop

    def perform_action(self):
        # play a sound
        self.game.sound.play(self.game.assets.sfx_menuSave)
        # clear audits
        if self.tool == "CLEAR STD. AUDITS":
            self.game.remote_load_game_data(restore="Audits")
            self.clear_instructions()
            self.selectionLine.set_text("AUDITS RESET",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        elif self.tool == "CLEAR FEAT. AUDITS":
            self.game.remote_load_game_data(restore="Feature")
            self.clear_instructions()
            self.selectionLine.set_text("AUDITS RESET",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        # reset hstd
        elif self.tool == "RESET HIGH SCORES":
            self.game.remote_load_game_data(restore="HighScoreData")
            self.clear_instructions()
            self.selectionLine.set_text("SCORES RESET",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        elif self.tool == "RESET SWITCH COUNT":
            self.game.remote_load_game_data(restore="SwitchHits")
            self.clear_instructions()
            self.selectionLine.set_text("SWITCH COUNTS RESET",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        # restore defaults
        elif self.tool == "RESTORE SETTINGS":
            self.game.remote_load_settings(restore=True)
            self.clear_instructions()
            self.selectionLine.set_text("DEFAULTS RESTORED",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        # reset custom message
        elif self.tool == "RESET CUSTOM MSG":
            self.game.remote_load_settings(restore=True,type='message')
            self.clear_instructions()
            self.selectionLine.set_text("MESSAGES RESET",blink_frames=15)
            self.delay(delay=2,handler=self.unload)
        # empty trough
        else:
            self.eject_balls()

    def clear_instructions(self):
        self.instructions.set_text("")
        self.instructions2.set_text("")

    def eject_balls(self):
        if self.game.switches.coinDoorClosed.is_active():
            self.selectionLine.set_text("CLOSE COIN DOOR",blink_frames=10)
        else:
            self.selectionLine.set_text("COLLECT BALLS NOW")
        # kick out a ball
        if self.game.switches.troughBallOne.is_active():
            print "Ejecting Ball"
            self.game.coils.troughEject.pulse(35)
        # if they're all gone, we're done here
        else:
            self.unload()
        # the beatings will continue until the trough is empty
        self.delay(delay=1.5,handler=self.eject_balls)


    def update_display(self):
    # standard display structure
        layers = []
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_testBackdrop.frames[0])
        background.set_target_position(0,-4)
        layers.append(background)
        self.titleLine = dmd.TextLayer(1,3,self.game.assets.font_5px_AZ_inverted,"Left").set_text(str(self.tool).upper())
        self.titleLine.composite_op = "blacksrc"
        layers.append(self.titleLine)
        self.selectionLine = dmd.TextLayer(64,12,self.game.assets.font_9px_az,"center").set_text("ARE YOU SURE?",blink_frames=10)
        layers.append(self.selectionLine)
        self.instructions = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center").set_text("'EXIT' TO CANCEL")
        self.instructions2 = dmd.TextLayer(64,25,self.game.assets.font_5px_AZ,"center").set_text("'ENTER' TO EXECUTE")
        script = []
        script.append({'seconds':2,'layer':self.instructions})
        script.append({'seconds':2,'layer':self.instructions2})
        instruction_duo = dmd.ScriptedLayer(128,32,script)
        instruction_duo.composite_op = "blacksrc"
        layers.append(instruction_duo)
        self.layer = dmd.GroupedLayer(128,32,layers)

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
        return game.SwitchStop

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
        self.infoLine.set_text("PRESS 'EXIT' BUTTON")
        self.busy = False

