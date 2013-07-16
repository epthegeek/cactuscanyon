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

    def mode_started(self):
        self.myTimer = 0
        self.chain = 1

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            self.game.lamp_control.disable_combos()
            self.wipe_delays()

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
            self.lamp_update()
            self.delay(name="Combo Timer",delay=1,handler=self.timer)
    
    def end(self):
        self.lamp_update()
        #print "Combos have ENDED"
    
    def start(self):
        # due to the multi ramp combos, this has to be able to add combos
        if self.chain > 1:
            self.add_combo()
        #print "Combos are ON"
        # set the timer at the max settings from the game
        self.myTimer = self.default
        # turn the lights on
        self.lamp_update()
        #loop to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.timer)
        # send this back to what called it for use in determining if in a combo or not
        return False
    
    def hit(self):
        print "COMBO HIT"
        # cancel the current combo_timer delay
        self.cancel_delayed("Combo Timer")
        # add one to the combo total and reset the timer
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
        print "COMBOS: " + str(comboTotal)
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
        print "CHAIN VALUE: " + str(self.chain)
        if self.chain > 1:
            if ep.last_shot == "center":
                textString = str(self.chain) + "-WAY SUPER COMBO"
                points = 25000 * self.chain
            else:
                textString = str(self.chain) + "-WAY COMBO"
                points = 50000
            textString2 = str(ep.format_score(points)) + " POINTS"
            self.game.score(points)
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
        print "I MADE IT THROUGH COMBO DISPLAY"
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