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
    """This is to load between the low ramp basic shots and higher level stackable modes"""
    def __init__(self, game,priority):
        super(PartyMode, self).__init__(game, priority)
        self.myID = "PartyMode"
        if self.game.party_setting == 'Flip Ct':
            self.flip_limit = self.game.user_settings['Gameplay (Feature)']['Party - Flip Count']
        else:
            self.flip_limit = 0

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
            textString1 = "< LIMITED FLIPS - " + str(self.flip_limit) + " >"
        elif self.game.party_setting == 'Drunk':
            textString1 = "< DRUNK - FLIPPERS REVERSED >"
        # last case is release to flip
        elif self.game.party_setting == 'Newbie':
            textString1 = "< NEWBIE - DOUBLE FLIP >"
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
            remain = self.flip_limit - self.game.show_tracking('Total Flips')
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
            textLayer = ep.EP_TextLayer(0,0, self.game.assets.font_12px_az, "left", opaque = False).set_text(str(remain),color=color)
            textLayer.composite_op = "blacksrc"
            self.layer = textLayer

    def sw_flipperLwL_active(self,sw):
        if self.game.party_setting == 'Flip Ct' and not self.game.skill_shot.live and self.game.base in self.game.modes:
            self.game.increase_tracking('Left Flips')
            self.game.increase_tracking('Total Flips')
            if self.game.show_tracking('Total Flips') > self.flip_limit and self.flip_limit != 0:
                # we're over the total, disable the flippers
                self.game.enable_flippers(False)
            self.update_display()
        else:
            print "No Match on Left"

    def sw_flipperLwR_active(self,sw):
        if self.game.party_setting == 'Flip Ct'and not self.game.skill_shot.live and self.game.base in self.game.modes:
            self.game.increase_tracking('Right Flips')
            self.game.increase_tracking('Total Flips')
            if self.game.show_tracking('Total Flips') > self.flip_limit and self.flip_limit != 0:
                # we're over the total disable the flippers
                self.game.enable_flippers(False)
            self.update_display()
        else:
            print "No match on Right"

    def tilted(self):
    # default tilt action is just to unload - this is here so it can be redefined
    # in each mode if something extra is needed
        print "Tilted: " + self.myID
