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

    def sw_up_active(self,sw):
        if self.activeMode == "MENU":
            if not self.busy:
                print "Item Down"
            # play the sound for moving down
            self.game.sound.play(self.game.assets.sfx_menuDown)
            self.item_down()
        else:
            pass

        return game.SwitchStop

    def sw_down_active(self,sw):
        if self.activeMode == "MENU":
            if not self.busy:
                print "Item Down"
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
        self.section = ["SWITCHES","SINGLE LAMPS", "ALL LAMPS","SOLENOIDS","FLASHERS","DROP TARGETS","MINE"]
        self.update_display("Tests",str(self.section[self.index]))

    def sw_enter_active(self,sw):
        selection = self.section[self.index]
        if selection == "SWITCHES":
            self.mode_to_add = NewServiceModeSwitchEdges(game=self.game,priority=202)
            self.game.modes.add(self.mode_to_add)
        elif selection == "DROP TARGETS":
            self.mode_to_add = NewServiceModeDropTargets(game=self.game,priority=202)
            self.game.modes.add(self.mode_to_add)
        else:
            pass
        # TODO: The rest of these sections
        return game.SwitchStop

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
        # TODO: check switch states to set row text
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

    def switch_handler(self, sw):
        if (sw.state):
            self.game.sound.play(self.game.assets.sfx_menuSwitchEdge)
            # set the last switch text string
            lastString = "LAST SWITCH: " + sw.tags[2] + sw.tags[1]
            self.lastText.set_text(lastString)
            # set the label text
            self.labelText.set_text(str(sw.label).upper())
            # set the row wire color text
            self.rowText.set_text(str(self.rowColors[int(sw.tags[2])]))
            # set the column color if applicable
            if int(sw.tags[1]) != 0:
                self.colText.set_text(str(self.colColors[int(sw.tags[1])]))
            else:
                pass
            # update the proper string position
            if "Grounded" in sw.tags:
                # grounded switch slice
                self.rowStrings[int(sw.tags[2])] = "A" + self.rowStrings[int(sw.tags[2])][1:]
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])
            elif "Dedicated" in sw.tags:
                # dedicated switch slice
                self.rowStrings[int(sw.tags[2])] = self.rowStrings[int(sw.tags[2])][:11] + "A"
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])
            else:
                # standard switch slice
                # find the slice positions
                left = int(sw.tags[1]) + 1
                right = int(sw.tags[1]) + 2
                self.rowStrings[int(sw.tags[2])] = self.rowStrings[int(sw.tags[2])][:left] + "A" + self.rowStrings[int(sw.tags[2])][right:]
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])
        else:
            # clear the label text
            self.labelText.set_text("")
            # update the proper string position
            if "Grounded" in sw.tags:
                # grounded switch slice
                self.rowStrings[int(sw.tags[2])] = "a" + self.rowStrings[int(sw.tags[2])][1:]
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])
            elif "Dedicated" in sw.tags:
                # dedicated switch slice
                self.rowStrings[int(sw.tags[2])] = self.rowStrings[int(sw.tags[2])][:11] + "a"
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])
            else:
                # standard switch slice
                # find the slice positions
                left = int(sw.tags[1]) + 1
                right = int(sw.tags[1]) + 2
                self.rowStrings[int(sw.tags[2])] = self.rowStrings[int(sw.tags[2])][:left] + "a" + self.rowStrings[int(sw.tags[2])][right:]
                self.rowLayers[int(sw.tags[2])].set_text(self.rowStrings[int(sw.tags[2])])

        return game.SwitchStop

    # TODO: set up all the switch methods for turning the images on and off

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
        # TODO: other row lines, info lines
        self.layer = combined
        self.rowLayers = [None,self.switchRow1,self.switchRow2,self.switchRow3,self.switchRow4,self.switchRow5,self.switchRow6,self.switchRow7,self.switchRow8]


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
            boxes[target].set_text("a")
        else:
            boxes[target].set_text("b")

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
        self.box0 = dmd.TextLayer(16,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        layers.append(self.box0)
        self.box1 = dmd.TextLayer(48,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        layers.append(self.box1)
        self.box2 = dmd.TextLayer(80,26,self.game.assets.font_5px_AZ,"center").set_text("a")
        layers.append(self.box2)
        self.box3 = dmd.TextLayer(112,26,self.game.assets.font_5px_AZ,"center").set_text("a")
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
        self.values = []

    def mode_started(self):
        # grab the audits section out of the game data
        itemlist = self.game.game_data["Audits"]
        # go through the audits and store the names and values
        for item in sorted(itemlist.iterkeys()):
            self.section.append(str(item).upper())
            print "Item: " + str(item)
            self.values.append(str(itemlist[item]))
            print "Value: " + str(itemlist[item])
        self.update_display("Statistics",self.section[self.index],self.values[self.index])

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
        self.titleLine = dmd.TextLayer(1,1,self.game.assets.font_7px_az,"Left",opaque=True).set_text(titleString)
        self.selectionLine = dmd.TextLayer(64,11,self.game.assets.font_9px_az,"center").set_text(selectionString)
        self.infoLine = dmd.TextLayer(64,22,self.game.assets.font_7px_az,"center")
        if blinkInfo:
            self.infoLine.set_text(infoString,blink_frames=30)
        else:
            self.infoLine.set_text(infoString)
        self.layer = dmd.GroupedLayer(128,32,[self.titleLine,self.selectionLine,self.infoLine])

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

