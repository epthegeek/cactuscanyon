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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##

from procgame import *
import ep
import locale
import inspect

class EP_Mode(game.Mode):
    def __init__(self, game, priority):
        super(EP_Mode, self).__init__(game, priority)
        self.busy = False
        self.POSTS = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]
        self.running = False
        self.queued = 0

    # busy flag set and unset
    def is_busy(self):
        self.busy = True

    def unbusy(self):
        self.busy = False

    # wait for busy to be over routine
    def wait_until_unbusy(self,myHandler):
        #print "BUSY LOOP WAIT - BUSY IS " + str(self.busy)
        if not self.busy:
            #print myHandler
            myHandler()
        else:
            #print "BUSY LOOP - SETTING A NEW DELAY"
            self.delay(delay=0.1,handler=self.wait_until_unbusy,param=myHandler)

    def wait_for_queue(self,myHandler):
    # if the queue is clear move ahead
        if self.queued <= 0:
            # reset to zero, just to be sure
            self.queued = 0
            # then do this thing
            myHandler()
        else:
            self.delay(delay=0.5,handler=self.wait_for_queue,param=myHandler)

    # standard clear layer
    def clear_layer(self):
        self.layer = None

    # simple mode shutdown
    def unload(self):
        self.game.modes.remove(self)
