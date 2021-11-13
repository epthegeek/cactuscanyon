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

from procgame import game, dmd
import ep

class PartyMode(ep.EP_Mode):
    """This is a filter layer to apply party mode rule changes"""
    def __init__(self, game,priority):
        super(PartyMode, self).__init__(game, priority)
        self.myID = "PartyMode"
        if self.game.party_setting == 'Flip Ct':
            self.flip_limit = self.game.user_settings['Gameplay (Feature)']['Party - Flip Count']
        else:
            self.flip_limit = 0
        self.left_flipper_active = True
        self.right_flipper_active = True
        self.party_check = False
        self.party_instructions = [("TRY A PARTY MODE","HOLD RIGHT FLIPPER","FOR MENU"),
                             ("FLIP COUNT","FLIPPERS LIMITED TO A", "SET NUMBER OF FLIPS"),
                             ("RELEASE TO FLIP","PRESS BUTTON TO DROP FLIPPER","RELEASE BUTTON TO FLIP"),
                             ("DRUNK","FLIPPERS REVERSED RIGHT/LEFT","FOR ENTIRE GAME"),
                             ("NEWBIE","PRESS EITHER FLIPPER BUTTON", "BOTH FLIPPERS ACTIVATE"),
                             ("NO HOLD","FLIPPER HOLD COILS DISABLED", "FLIPPERS DROP IMMEDIATELY"),
                             ("LIGHTS OUT","ALL PLAYFIELD INSERTS LIGHTS", "DISABLED DURING GAME"),
                             ("SPIKED","HITTING THE BEER MUG TARGET", "TILTS YOUR BALL!"),
                             ("RECTIFY","IF BOTH FLIPPERS ACTIVATED", "TOGETHER - TILT!")]

    def attract_display(self):
        # Banner for attract mode to alert that party mode is on
        script = []
        # set up the text layer
        textString = "< PARTY MODE ENABLED >"
        textLayer = ep.EP_TextLayer(64, 0, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.MAGENTA)
        script.append({'seconds':1.0,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.5,'layer':blank})
        # set up the type of mode text
        if self.game.party_setting == 'Flip Ct':
            textString1 = "< LIMITED FLIPS - " + self.game.user_settings['Gameplay (Feature)']['Party - Flip Count'] + " >"
        elif self.game.party_setting == 'Drunk':
            textString1 = "< DRUNK - FLIPS REVERSED >"
        # newbie mode - both flippers all the time
        elif self.game.party_setting == 'Newbie':
            textString1 = "< NEWBIE - BOTH FLIP >"
        # lights out mode
        elif self.game.party_setting == 'Lights Out':
            textString1 = "< LIGHTS OUT >"
        # spiked beer
        elif self.game.party_setting == 'Spiked':
            textString1 = "< SPIKED - BEER TILTS >"
        # rectify
        elif self.game.party_setting == 'Rectify':
            textString1 = "< RECTIFY - NO DUB FLIP >"
        # last case is release to flip
        else:
            textString1 = "< RELEASE TO FLIP >"
        textLayer1 = ep.EP_TextLayer(64,0, self.game.assets.font_6px_az_inverse, "center", opaque = False).set_text(textString1,color=ep.MAGENTA)
        script.append({'seconds':1.0,'layer':textLayer1})
        # and another blank
        script.append({'seconds':0.5,'layer':blank})
        # make a script layer with the two
        infoLine = dmd.ScriptedLayer(128,32,script)
        infoLine.composite_op = "blacksrc"
        self.layer = infoLine

    def null_display(self,timer):
        self.clear_layer()
        self.delay(delay = timer,handler=self.attract_display)

    def update_display(self):
        if self.game.party_setting == 'Flip Ct':
            remain = self.game.show_tracking('Flip Limit') - self.game.show_tracking('Total Flips')
            if remain <= 0:
                remain = 00
            if remain < 5:
                color = ep.RED
            elif remain < 10:
                color = ep.ORANGE
            elif remain < 15:
                color = ep.YELLOW
            else:
                color = ep.CYAN
            p = self.game.current_player_index
            if p == 0 or p == 2:
                align_side = "right"
                position = 128
            else:
                align_side ="left"
                position = 0
            textLayer = ep.EP_TextLayer(position,0, self.game.assets.font_12px_az_outline, align_side, opaque = False).set_text(str(remain),color=color)
            textLayer.composite_op = "blacksrc"
            self.layer = textLayer

    def sw_flipperLwL_active(self,sw):
        if self.game.party_setting == 'Flip Ct' and not self.game.skill_shot.live and self.game.base in self.game.modes and self.game.flippers_active:
            self.game.increase_tracking('Left Flips')
            self.game.increase_tracking('Total Flips')
            if self.game.show_tracking('Total Flips') > self.game.show_tracking('Flip Limit') and self.game.show_tracking('Flip Limit') != 0:
                # we're over the total, disable the flippers
                self.game.enable_flippers(False)
            self.update_display()
        else:
            self.game.logger.debug("No Match on Left")

    def sw_flipperLwR_active(self,sw):
        if self.game.party_setting == 'Flip Ct' and not self.game.skill_shot.live and self.game.base in self.game.modes and self.game.flippers_active:
            self.game.increase_tracking('Right Flips')
            self.game.increase_tracking('Total Flips')
            if self.game.show_tracking('Total Flips') > self.game.show_tracking('Flip Limit') and self.game.show_tracking('Flip Limit') != 0:
                # we're over the total disable the flippers
                self.game.enable_flippers(False)
            self.update_display()
        else:
            self.game.logger.debug("No match on Right")

    def left_flipper(self,action):
        if action == 'Activate':
            self.left_flipper_active = True
        elif action == 'Deactivate':
            self.left_flipper_active = False
        elif action == 'Toggle':
            self.left_flipper_active = not self.left_flipper_active
        else:
            pass

    def right_flipper(self,action):
        if action == 'Activate':
            self.right_flipper_active = True
        elif action == 'Deactivate':
            self.right_flipper_active = False
        elif action == 'Toggle':
            self.right_flipper_active = not self.right_flipper_active
        else:
            pass

    # Display for start pressed when party mode is active
    def party_started(self):
        # Turn the music on
        self.music_on("music_party")
        # Show the current party mode activated
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_starsBorder.frames[0])
        textLayer1 = ep.EP_TextLayer(64, 1, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("PARTY MODE START",color=ep.MAGENTA)
        self.ptextLayer2 = ep.EP_TextLayer(64, 12, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(self.game.party_setting.upper(),color=ep.YELLOW)
        instructions = dmd.TextLayer(64,23,self.game.assets.font_5px_AZ,"center").set_text("HOLD L. FLIPPER TO CONFIRM")
        instructions2 = dmd.TextLayer(64,23,self.game.assets.font_5px_AZ,"center").set_text("HOLD R. FLIPPER TO DISABLE")
        script = []
        script.append({'seconds':2,'layer':instructions})
        script.append({'seconds':2,'layer':instructions2})
        instruction_duo = dmd.ScriptedLayer(128,32,script)
        instruction_duo.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[background,textLayer1,self.ptextLayer2,instruction_duo])
        # start a bail delay
        self.reset_party_timeout()

    def reset_party_timeout(self):
        self.cancel_delayed("Party Timeout")
        self.delay("Party Timeout",delay = 30,handler=self.cancel_party)

    def sw_flipperLwL_active_for_1s(self,sw):
        if self.party_check:
            # confirming party start
            self.continue_party()
            return game.SwitchStop

    def sw_flipperLwR_active_for_1s(self,sw):
        if self.party_check:
            # cancel the party
            self.cancel_party()
            return game.SwitchStop

    def continue_party(self):
        #print "PARTY ON DUDES"
        self.cancel_delayed("Party Timeout")
        self.party_check = False
        self.game.attract_mode.normal_start()

    def cancel_party(self):
        #print "CANCEL PARTY"
        self.cancel_delayed("Party Timeout")
        #disable party and start game
        self.game.party_setting = 'Disabled'
        self.game.user_settings['Gameplay (Feature)']['Party Mode'] = 'Disabled'
        self.game.party_index = 0
        self.game.attract_mode.set_party_display_text()
        self.game.save_settings()
        self.party_check = False
        self.game.attract_mode.normal_start()
        # unload party mode
        self.unload()


    def tilted(self):
    # default tilt action is just to unload - this is here so it can be redefined
    # in each mode if something extra is needed
        self.game.logger.debug("Tilted: " + self.myID)
