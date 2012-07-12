from procgame import *
import ep
import locale

class EP_Mode(game.Mode):
    def __init__(self, game, priority):
        super(EP_Mode, self).__init__(game, priority)
        self.busy = False

    # busy flag set and unset
    def busy(self):
        self.busy = True

    def unbusy(self):
        self.busy = False

    # wait for busy to be over routine
    def wait_until_unbusy(self,myHandler):
        if not self.busy:
            myHandler()
        else:
            self.delay(delay=0.1,handler=self.wait_until_unbusy,param=myHandler)

    # standard clear layer
    def clear_layer(self):
        self.layer = None

    # simple mode shutdown
    def unload(self):
        self.game.modes.remove(self)
