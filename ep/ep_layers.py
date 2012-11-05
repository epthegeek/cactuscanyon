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
## This is originally Koen at dutchpinball.com's dp_layers
## I tweaked it to add params for frame listeners
##
from procgame import *
from time import *

class EP_UpdateLayer(dmd.dmd.Layer):

    def __init__(self, callbackFunction = None):
        super(EP_UpdateLayer, self).__init__(False)
        self.callbackFunction = callbackFunction

    def next_frame(self):
        if self.callbackFunction:
            self.callbackFunction()
        return None

class EP_AnimatedLayer(dmd.layers.AnimatedLayer):
    """Collection of frames displayed sequentially, as an animation.  Optionally holds the last frame on-screen."""

    # TODO not currently using the callback feature Koen does - maybe add that later
    def __init__(self, animation, callback=None):
        super(EP_AnimatedLayer, self).__init__(opaque=False, hold=False, repeat=False, frame_time=6, frames=animation.frames)

        if callback:
            self.add_frame_listener(-1, callback)

        self.reset_timer()

    def clear_frame_listeners(self):
            self.frame_listeners = []

    def next_frame(self):
        self.framerate_counter += 1
        return super(EP_AnimatedLayer, self).next_frame()

    def reset_timer(self):
        self.framerate_counter = 0


    def add_frame_listener(self, frame_index, listener, param=None):
        # redoing frame listener to allow for passing a prameter, I hope
        self.frame_listeners.append((frame_index,listener,param))

    def notify_frame_listeners(self):
        for frame_listener in self.frame_listeners:
            (index, listener,param) = frame_listener
            if index >= 0 and self.frame_pointer == index:
                if param != None:
                    listener(param)
                else:
                    listener()
            elif self.frame_pointer == (len(self.frames) + index):
                if param != None:
                    listener(param)
                else:
                    listener()
