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
# This mode controls the double scoring that can be earned during multiball
#

from procgame import game, dmd
import ep

class Doubler(ep.EP_Mode):
    """This is to load between the low ramp basic shots and higher level stackable modes"""
    def __init__(self, game,priority):
        super(Doubler, self).__init__(game, priority)
        self.myID = "Doubler"
        self.baseTime = self.game.user_settings['Gameplay (Feature)']['2X Scoring Timer'] + 1
        self.timer = 0
        self.hitsRequired = self.game.user_settings['Gameplay (Feature)']['2X Scoring Hits']
        self.ready = False

    def mode_started(self):
        # set up the status
        self.leftHits = 0
        self.rightHits = 0
        self.ready = False
        self.running = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            self.unload()

    # switch bits
    def sw_topLeftStandUp_active(self,sw):
        self.hit('Left')
    def sw_bottomLeftStandUp_active(self,sw):
        self.hit('Left')
    def sw_topRightStandUp_active(self,sw):
        self.hit('Right')
    def sw_bottomRightStandUp_active(self,sw):
        self.hit('Right')
    def sw_saloonPopper_active_for_290ms(self,sw):
        if self.ready:
            # kick off double scoring if we're ready
            self.start()
        else:
            pass

    def hit(self,side):
        # If not already ready or running, these hits matter
        if not self.ready and not self.running:
            dud = False
            if side == 'Left':
                self.leftHits += 1
                if self.leftHits > self.hitsRequired:
                    dud = True
            if side == 'Right':
                self.rightHits += 1
                if self.rightHits > self.hitsRequired:
                    dud = True
            # play a sound
            if dud:
                self.game.sound.play(self.game.assets.sfx_quickdrawOn)
            else:
                self.game.sound.play(self.game.assets.sfx_quickdrawOff)
            # set the lights
            if side == 'Left':
                if self.leftHits == self.hitsRequired - 1:
                    self.game.lamps.leftQuickdraw.schedule(0x0F0F0F0F)
                elif self.leftHits >= self.hitsRequired:
                    self.game.lamps.leftQuickdraw.enable()
            if side == 'Right':
                if self.rightHits == self.hitsRequired -1:
                    self.game.lamps.topRightQuickdraw.schedule(0x0F0F0F0F)
                    self.game.lamps.bottomRightQuickdraw.schedule(0x0F0F0F0F)
                elif self.leftHits >= self.hitsRequired:
                    self.game.lamps.topRightQuickdraw.enable()
                    self.game.lamps.bottomRightQuickdraw.enable()
            # check ready status
            if self.rightHits >= self.hitsRequired and self.leftHits >= self.hitsRequired and not self.running:
                # set the ready flag
                self.ready = True
                # flash the light
                self.game.lamps.saloonArrow.schedule(0x0F0F0F0F)
        elif self.ready:
            # if ready just play the dud hit noise
            self.game.sound.play(self.game.assets.sfx_quickdrawOn)
        else:
            pass

    # Start the 2x scoring - set the multiplier and start the time loop
    def start(self):
        # set the running flag
        self.running = True
        # remove the ready flag
        self.ready = False
        # Turn off the lights
        self.game.lamps.leftQuickdraw.disable()
        self.game.lamps.topRightQuickdraw.disable()
        self.game.lamps.bottomRightQuickdraw.disable()
        self.game.lamps.saloonArrow.disable()
        # set the running flag
        self.running = True
        # used by self.game.score to multiply base points
        self.game.multiplier = 2
        # put up the 2x display
        self.display()
        # Play some sort of a sound?
        self.game.sound.play(self.game.assets.sfx_fanfare1)
        # Start the timer
        self.timer = self.baseTime
        self.timerLoop()

    def display(self,step=1):
        # banner to announce is first
        if step == 1:
            textLine1 = ep.EP_TextLayer(64,0,self.game.assets.font_12px_az_outline,"center")
            textLine2 = ep.EP_TextLayer(64,15,self.game.assets.font_12px_az_outline,"center")
            textLine1.composite_op = "blacksrc"
            textLine2.composite_op = "blacksrc"
            textLine1.set_text("DOUBLE",color=ep.BLUE)
            textLine2.set_text("SCORING")
            combined1 = dmd.GroupedLayer(128,32,[textLine1,textLine2])
            combined1.composite_op = "blacksrc"
            textLine3 = ep.EP_TextLayer(64,0,self.game.assets.font_12px_az_outline,"center")
            textLine4 = ep.EP_TextLayer(64,15,self.game.assets.font_12px_az_outline,"center")
            textLine3.composite_op = "blacksrc"
            textLine4.composite_op = "blacksrc"
            textLine3.set_text("DOUBLE")
            textLine4.set_text("SCORING",color=ep.BLUE)
            combined2 = dmd.GroupedLayer(128,32,[textLine3,textLine4])
            combined2.composite_op = "blacksrc"
            finalproduct = dmd.ScriptedLayer(128,32,[{'seconds':0.2,'layer':combined1},{'seconds':0.2,'layer':combined2}])
            finalproduct.composite_op = "blacksrc"
            self.layer = finalproduct
            # Delay the change to the simple 2x bar
            self.delay("Operational",delay=2,handler=self.display,param=2)
        # step 2 puts up a smaller overlay to indicate 2x
        if step == 2:
            textLine1 = ep.EP_TextLayer(64,-1,self.game.assets.font_5px_bold_AZ_outline,"center")
            textLine1.composite_op = "blacksrc"
            textLine1.set_text("2X                                              2X",color=ep.BLUE)
            self.layer = textLine1

    # one second loop to tick down the remaining time
    def timerLoop(self):
        self.timer -= 1
        if self.timer <= 0:
            self.unload()
        else:
            self.delay("Operational",delay=1,handler=self.timerLoop)

    def unload(self):
        # clear the layer
        self.clear_layer()
        # set the multiplier back to one
        self.game.multiplier = 1
        # wipe delays
        self.wipe_delays()
        # Turn off the running flag
        self.running = False
        # disabled the associated lights
        if self.leftHits > 0:
            self.game.lamps.leftQuickdraw.disable()
        if self.rightHits > 0:
            self.game.lamps.topRightQuickdraw.disable()
            self.game.lamps.bottomRightQuickdraw.disable()
        if self.ready:
            self.game.lamps.saloonArrow.disable()
        # unload
        self.game.modes.remove(self)