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
##
## The playfield toy mountain
##
import ep

class Mountain(ep.EP_Mode):
    """Cactus Canyon Mine Mountain Toy"""
    def __init__(self, game, priority):
        super(Mountain, self).__init__(game, priority)
        self.mineReset = False
        self.inMotion = False
        self.kickStrength = self.game.user_settings['Machine (Standard)']['Mine Kicker Strength']
        self.mineTicks = 0
        self.solidRun = False
        difficulty = self.game.user_settings['Gameplay (Feature)']['Mine Opening Difficulty']
        if difficulty == 'Easy':
            self.stopPoints = [4,6,7,8]
        else:
            self.stopPoints = [1,2,3,4,5,6,7,8]

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            self.stop()
            self.game.coils.mineFlasher.disable()

    def mode_started(self):
        # home the mine
        if not self.game.switches.mineHome.is_active():
            self.reset_toy()

    def stop(self):
        print "Mine Stop Called"
        self.game.coils.mineMotor.disable()
        self.solidRun = False
        self.inMotion = False

    def move(self):
        if not self.inMotion:
            print "Mine Mountain Move called"
            self.inMotion = True
            self.game.coils.mineMotor.enable()
        else:
            print "Mountain move called - but already in motion"

    def sw_mineEncoder_active(self,sw):
        self.mineTicks += 1
        #print "Mine Encoder :" + str(self.mineTicks)
        if not self.mineReset and not self.solidRun:
            if self.mineTicks in self.stopPoints:
                self.stop()

    def sw_mineHome_active(self,sw):
        print "Mine Home Active, resetting ticks - Reset = " + str(self.mineReset)
        self.mineTicks = 0
        # if the switch is active and we're supposed to be resetting, then stop here
        if self.mineReset:
            self.stop()
            self.mineReset = False

    def kick(self):
        self.game.coils.minePopper.pulse(self.kickStrength)

    def flash(self):
        self.game.coils.mineFlasher.schedule(0x00000025,cycle_seconds=1)
        # run the mine lamp update to turn the flasher back on if needed
        self.delay(delay=0.5,handler=self.lamp_update)

    def eject(self):
        if self.busy:
            print "MOUNTAIN BUSY, PASSING"
            return
        # flash the light and then kick out if there's a ball in there
        if self.game.switches.minePopper.is_active() and not self.game.fakePinProc:
            print "Mountain Ejecting wth Reset call"
            self.game.coils.mineFlasher.schedule(0x0000002B,cycle_seconds=1)
            self.delay(delay=0.06,handler=self.kick)
            # reset the mine
            self.reset_toy()

    def run(self):
        print "Mountain Solid Run Called"
        if not self.inMotion:
            self.inMotion = True
            self.solidRun = True
            self.game.coils.mineMotor.enable()

    def reset_toy(self,force=False):
        print "Mountain Reset Called - force = " + str(force)
        if not self.game.switches.mineHome.is_active() or force:
            self.game.coils.mineMotor.enable()
            self.mineReset = True
            self.inMotion = True
