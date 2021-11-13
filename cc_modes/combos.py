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
###
###   ____                _
###  / ___|___  _ __ ___ | |__   ___  ___
### | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|
### | |__| (_) | | | | | | |_) | (_) \__\
###  \____\___/|_| |_| |_|_.__/ \___/|___/
###

from procgame import dmd
import ep

class Combos(ep.EP_Mode):
    """Cactus Canyon Combos"""
    def __init__(self, game, priority):
        super(Combos, self).__init__(game, priority)
        self.myID = "Combos"

        self.comboLights = [self.game.lamps.rightRampCombo,
                            self.game.lamps.leftRampCombo,
                            self.game.lamps.centerRampCombo,
                            self.game.lamps.leftLoopCombo,
                            self.game.lamps.rightLoopCombo]
        self.default = self.game.user_settings['Gameplay (Feature)']['Combo Timer']
        self.myTimer = 0
        self.comboStatus = False

    def mode_started(self):
        self.myTimer = 0
        self.chain = 1
        self.comboStatus = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            self.game.lamp_control.disable_combos()
            self.wipe_delays()
            self.myTimer = 0
            self.chain = 1
            self.layer = None

    # Switches for combos
    def sw_centerRampMake_active(self,sw):
        # check the chain status
        if ep.last_shot == "left" or ep.last_shot == "right":
            # if there have been at least 2 combo chain shots before, we take action
            if self.chain >= 2:
            #  and that action is, increase the chain increase the chain
                self.increase_chain()
        else:
            # if not, set it back to one
            self.chain = 1

        # hitting this switch counts as a made ramp - really
        # score the points and mess with the combo
        if self.myTimer > 0:
            # register the combo and reset the timer - returns true for use later
            self.comboStatus = self.hit()
        else:
            # and turn on the combo timer - returns false for use later
            self.comboStatus = self.start()
        ## -- set the last switch hit --
        ep.last_switch = "centerRampMake"
        ## -- set the last shot for combos
        ep.last_shot = "center"

    def sw_leftRampEnter_active(self,sw):
        # check the chain status
        if ep.last_shot == "right":
            # if we're coming from the right ramp, chain goes up
            self.increase_chain()
        else:
            # if we're not, reset the chain to one
            self.chain = 1
            # score the points and mess with the combo
        if self.myTimer > 0:
            # register the combo and reset the timer - returns true for use later
            self.comboStatus = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            self.comboStatus = self.game.combos.start()
        ## -- set the last switch hit --
        ep.last_switch = "leftRampEnter"
        ep.last_shot = "left"

    def sw_rightRampMake_active(self,sw):
    # check the chain status
        if ep.last_shot == "left":
            # if we're coming from the left ramp, increase the chain
            self.increase_chain()
        else:
            # if not, set it back to one
            self.chain = 1

            # score the points and mess with the combo
        if self.myTimer > 0:
            # register the combo and reset the timer - returns true for use later
            self.comboStatus = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            self.comboStatus = self.game.combos.start()
        ## -- set the last switch hit --
        ep.last_switch = "rightRampMake"
        ep.last_shot = "right"

    def timer(self):
        # just to be sure
        self.cancel_delayed("Combo Timer")
        # tick down the timer
        self.myTimer -= 1
        # see if it hit zero
        #print "COMBO TIMER: " + str(self.myTimer)
        if self.myTimer <= 0:
            self.end()
        else:
            # if we're at 2 or 1 second left, refresh the combo schedules.
            if self.myTimer == 2 or self.myTimer == 1:
                self.game.lamp_control.combos(mode='Timer')
            self.delay(name="Combo Timer",delay=1,handler=self.timer)
    
    def end(self):
        self.game.lamp_control.disable_combos()
        # set the chain back to one
        self.chain = 1
        ep.last_shot = "none"
        #print "Combos have ENDED"
    
    def start(self):
        # due to the multi ramp combos, this has to be able to add combos
        if self.chain > 1:
            self.add_combo()
        #print "Combos are ON"
        # set the timer at the max settings from the game
        self.myTimer = self.default
        # turn the lights on
        self.game.lamp_control.combos(mode='Timer')
        #loop to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.timer)
        # send this back to what called it for use in determining if in a combo or not
        return False
    
    def hit(self):
        #print "COMBO HIT - SCORING"
        # score the points here, not in the display, dummy
        if self.chain > 1:
            if ep.last_shot == "center":
                points = 25000 * self.chain
            else:
                points = 50000
            self.game.score(points)

        # cancel the current combo_timer delay
        self.cancel_delayed("Combo Timer")
        # add one to the combo total and reset the timer - if at 2 or less seconds already, refresh the lamps
        if self.myTimer <= 2:
            self.myTimer = self.default
            self.game.lamp_control.combos(mode='Timer')
        else:
            self.myTimer = self.default
        # add the new combo and check the badge
        self.add_combo()
        # then loop back to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.timer)
        # send this back to what called it for use in determining if in a combo or not
        return True

    def add_combo(self):
        # increase the combos
        combosForStar = self.game.increase_tracking('combos')
        # and the global total
        comboTotal = self.game.increase_tracking('combosTotal')
        # then see if it's time to light the badge
        #print "COMBOS: " + str(comboTotal)
        # if we've got enough combos to light the badge, do that
        if combosForStar == self.game.user_settings['Gameplay (Feature)']['Combos for Star']:
            ## actually award the badge - combos is # 1
            self.game.badge.update(1)

    def display(self):
        self.cancel_delayed("Display")
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_cactusBorder.frames[0])
        # build and show the display of combos made & left
        combos = self.game.show_tracking('combos')
        # if we've got a chain going, that affects display
        #print "CHAIN VALUE: " + str(self.chain)
        if self.chain > 1:
            if ep.last_shot == "center":
                textString = str(self.chain) + "-WAY SUPER COMBO"
                points = 25000 * self.chain
            else:
                textString = str(self.chain) + "-WAY COMBO"
                points = 50000
            textString2 = str(ep.format_score(points)) + " POINTS"
        else:
            textString = "COMBO AWARDED"
            textString2 = str(combos) + " COMBOS"
        textLine1 = ep.EP_TextLayer(64,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False).set_text(textString,color=ep.BROWN)
        textLine2 = ep.EP_TextLayer(64,11,self.game.assets.font_9px_az,justify="center",opaque=False)
        textLine3 = ep.EP_TextLayer(64,25,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        textLine2.set_text(textString2,blink_frames=10,color=ep.GREEN)
        combosForStar = self.game.user_settings['Gameplay (Feature)']['Combos for Star']
        diff = combosForStar - combos
        if combos > combosForStar:
            comboString = "BADGE COMPLETE!"
        elif combos == combosForStar:
            comboString = "BADGE AWARDED"
        else:
            comboString = str(diff) + " MORE FOR BADGE!"
        textLine3.set_text(comboString,color=ep.BROWN)
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        self.layer = combined
        #print "I MADE IT THROUGH COMBO DISPLAY"
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")

    def increase_chain(self):
        # up the count
        self.chain += 1
        # check it against the tracking and set the new if it's high - to be used for combo champ
        if self.chain > self.game.show_tracking('bigChain'):
            self.game.set_tracking('bigChain',self.chain)


    def mini_display(self):
        if self.chain > 1:
            string = "CHAIN COMBO " + str(self.chain) + " - " + ep.format_score(25000 * self.chain)
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_status_banner_magenta.frames[0])
            backdrop.composite_op = "blacksrc"
            textLayer = dmd.TextLayer(128/2, 26, self.game.assets.font_5px_AZ_inverted, "center", opaque=False).set_text(string)
            textLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32, [backdrop,textLayer])
            combined.composite_op = "blacksrc"
            self.game.interrupter.broadcast(combined,1.5)

