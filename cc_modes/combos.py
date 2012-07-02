###
###   ____                _
###  / ___|___  _ __ ___ | |__   ___  ___
### | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|
### | |__| (_) | | | | | | |_) | (_) \__\
###  \____\___/|_| |_| |_|_.__/ \___/|___/
###

from procgame import *
from assets import *
import cc_modes
import ep

class Combos(game.Mode):
    """Cactus Canyon Combos"""
    def __init__(self, game, priority):
        super(Combos, self).__init__(game, priority)

        self.comboLights = [self.game.lamps.rightRampCombo,
                            self.game.lamps.leftRampCombo,
                            self.game.lamps.centerRampCombo,
                            self.game.lamps.leftLoopCombo,
                            self.game.lamps.rightLoopCombo]
        self.default = self.game.user_settings['Gameplay (Feature)']['Combo Timer']
        self.myTimer = 0
        
    def update_lamps(self):
        self.disable_lamps()
        lampStatus = self.game.show_tracking('lampStatus')

        # high noon check
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
            for lamp in self.comboLights:
                lamp.schedule(0x00FF00FF)
            return
        # if status is multiball ...
        if self.game.show_tracking('mineStatus') == "RUNNING":
            # loop through and turn on the appropriate lights
            for i in range(0,5,1):
                if self.game.show_tracking('jackpotStatus',i):
                    self.comboLights[i].schedule(0x0F0FF000)
            return
        ## if status is anything other than ON bail here
        if self.game.show_tracking('lampStatus') != "ON":
            return

        # if timer is greater than 2, slow blink
        if self.myTimer > 2:
            for myLamp in self.comboLights:
                myLamp.schedule(0x0000FFFF)
        # if timer is AT 2, speed it up
        elif self.myTimer == 2:
            for myLamp in self.comboLights:
                myLamp.schedule(0x00FF00FF)
        # one second left, speed it up even more
        elif self.myTimer == 1:
            for myLamp in self.comboLights:
                myLamp.schedule(0x0F0F0F0F)
          
    def disable_lamps(self):
        for myLamp in self.comboLights:
            myLamp.disable()

    def timer(self):
        # just to be sure
        self.cancel_delayed("Combo Timer")
        # tick down the timer
        self.myTimer -= 1
        # see if it hit zero
        print "COMBO TIMER: " + str(self.myTimer)
        if self.myTimer <= 0:
            self.end()
        else:
            self.update_lamps()
            self.delay(name="Combo Timer",delay=1,handler=self.timer)
    
    def end(self):
        self.update_lamps()
        print "Combos have ENDED"
    
    def start(self):
        print "Combos are ON"
        # set the timer at the max settings from the game
        self.myTimer = self.default
        # turn the lights on
        self.update_lamps()
        #loop to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.timer)
        # send this back to what called it for use in determining if in a combo or not
        return False
    
    def hit(self):
        # cancel the current combo_timer delay
        self.cancel_delayed("Combo Timer")
        # add one to the combo total and reset the timer
        self.myTimer = self.default
        comboTotal = self.game.increase_tracking('combos')
        print "COMBOS: " + str(comboTotal)
        # show a display at this level? have the higher modes turn off their deisplay?
        # or do the display in the other modes? HMM
        # points? # TODO investigate points awarded for combos
        # if we've got enough combos to light the badge, do that
        if comboTotal == self.game.user_settings['Gameplay (Feature)']['Combos for Star']:
            ## actually award the badge
            self.game.set_tracking('starStatus',True,1)
            # Then run the check to see if it's high noon time
            self.game.base_game_mode.check_high_noon()
            self.game.base_game_mode.update_lamps()
            # loop back to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.timer)
        # send this back to what called it for use in determining if in a combo or not
        return True
    
    def display(self):
        self.cancel_delayed("Display")
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'cactus-border.dmd').frames[0])
        # build and show the display of combos made & left
        textLine1 = dmd.TextLayer(64,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False).set_text("COMBO AWARDED")
        textLine2 = dmd.TextLayer(64,11,self.game.assets.font_9px_az,justify="center",opaque=False)
        textLine3 = dmd.TextLayer(64,25,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        combos = self.game.show_tracking('combos')
        textString2 = str(combos) + " COMBOS"
        textLine2.set_text(textString2,blink_frames=10)
        combosForStar = self.game.user_settings['Gameplay (Feature)']['Combos for Star']
        diff = combosForStar - combos
        if combos > combosForStar:
            comboString = "BADGE COMPLETE!"
        elif combos == combosForStar:
            comboString = "BADGE AWARDED"
        else:
            comboString = str(diff) + " MORE FOR BADGE!"
        textLine3.set_text(comboString)
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        self.layer = combined
        print "I MADE IT THROUGH COMBO DISPLAY"
        self.delay(name="Display",delay=2,handler=self.clear_layer)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")

    def clear_layer(self):
        self.layer = None