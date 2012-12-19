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
## The playfield toy train
##
import ep

class Train(ep.EP_Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Train, self).__init__(game, priority)
        self.trainProgress = 0
        self.inMotion = False
        self.trainReset = False
        self.trainDisabled = True

    def mode_started(self):
        # home the train
        #if not self.game.switches.trainHome.is_active():
        self.reset_toy()
        self.trainProgress = 0
        self.stopAt = 0

    def sw_trainHome_active(self,sw):
        if self.trainReset:
            self.stop()
            self.trainReset = False
            self.trainProgress = 0
            if self.trainDisabled:
                # if the train didn't enable due to the encoder - its dead
                print("Encoder not registering - Train Disabled")
                self.game.interrupter.train_disabled()

    def sw_trainEncoder_active(self,sw):
        # this is the moving train
        # if this switch isn't working, the train will be disabled.
        # any registration of the encoder turns the train back on
        if self.trainDisabled:
            self.trainDisabled = False
        # each time it hits increment the train progress
        self.trainProgress += 1
        if self.stopAt > 0:
            # if progress exceeds stop at
            if self.trainProgress >= self.stopAt:
                # stop the train
                self.stop()
                # reset stop at so it doesn't interfere
                self.delay("Zero",delay=0.5,handler=self.zero_out)

    def zero_out(self):
        self.stopAt = 0
        self.trainProgress = 0

    def move(self):
        if not self.trainDisabled:
            self.inMotion = True
            self.game.coils.trainForward.patter(on_time=3,off_time=8)

    def stop(self):
        print("Stopping Train")
        # turn off the moving train solenoids
        self.game.coils.trainForward.disable()
        self.game.coils.trainReverse.disable()
        self.inMotion = False

    def fast_forward(self):
        print("Train Fast Forwrd")
        if not self.trainDisabled or self.trainReset:
            print("Train Moving Fast Forward")
            self.inMotion = True
            self.game.coils.trainForward.enable()

    def forward(self):
        if not self.trainDisabled:
            self.inMotion = True
            # TODO need to tweak this out for speed later
            self.game.coils.trainForward.patter(on_time=6,off_time=6)

    def fast_reverse(self):
        if not self.trainDisabled:
            self.inMotion = True
            self.game.coils.trainReverse.enable()

    def reverse(self):
        if not self.trainDisabled:
            print("Backing train up")
            self.inMotion = True
            self.game.coils.trainReverse.patter(on_time=6,off_time=6)

    def reset_toy(self,step=1,type=1):
        # set the reset flag
        self.trainReset = True

        if step == 1:
            print("Resetting Train - Step 1")
            # move the train forward
            immediate = False
            if type == 1:
                self.fast_forward()
            if type == 2:
                # on type 2, only move forward if the switch is currently held down
                if self.game.switches.trainHome.is_active():
                    self.fast_forward()
                else:
                    immediate = True
            # if we didn't move forward, reverse right away
            if immediate:
                self.reset_toy(step = 2)
            else:
                # delay a stop, and step 2 of the check
                self.delay(delay=1,handler=self.stop)
                self.delay(delay=1.5,handler=self.reset_toy,param=2)
        if step == 2:
            print("Resetting Train - Step 2")
            # check this again because save polly requests the reset directly
            if not self.game.switches.trainHome.is_active():
                self.game.coils.trainForward.disable()
                self.inMotion = True
                self.game.coils.trainReverse.enable()
            else:
                print "Game thinks the train is home already"

    def progress(self):
        return self.trainProgress



