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

__all__ = [
    'ep_layers',
    'ep_transition',
    'ep_mode',
    'ep_showcase',
#    'ep_service',
    'ep_lamps',
    'ep_new_service',
    'ep_pygame_desktop',
    'ep_font',
    'ep_custom_message'
]
from ep_layers import *
from ep_transition import *
from ep_mode import *
from ep_showcase import *
#from ep_service import *
from ep_lamps import *
from ep_new_service import *
from ep_desktop_pygame import *
from ep_font import *
from ep_custom_message import *

import locale

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")


DMD_PATH = "dmd/"
LAMPSHOWS_PATH = "lampshows/"
SOUNDS_PATH = "sounds/"
SFX_PATH = "sounds/sfx/"
MUSIC_PATH = "sounds/music/"
QUOTES_PATH = "sounds/quotes/"
FLASHER_PULSE = int(1000 / 32)

WHITE = 0x0
GREY = 0x1
DARK_GREY = 0x2
DARK_GREEN = 0x3
FLESH = 0x4
PURPLE = 0x5
DARK_RED = 0x6
BROWN = 0x7
DARK_BROWN = 0x8
RED = 0x9
GREEN = 0xA
YELLOW = 0xB
BLUE = 0xC
ORANGE = 0xD
CYAN = 0xE
MAGENTA = 0xF



# set up a property for last switch tracking
def get_last_switch(self):
    return self.game.lastSwitch

def set_last_switch(self,value):
    self.game.lastSwitch = value

last_switch = property(get_last_switch,set_last_switch)
# set up a property for last ramp tracking for combos
def get_last_shot(self):
    return self.game.lastShot

def set_last_shot(self,value):
    self.game.lastShot = value

last_shot = property(get_last_shot, set_last_shot)

def format_score(score):
    """Returns a string representation of the given score value.
         Override to customize the display of numeric score values."""
    if score == 0:
        return '00'
    else:
        return locale.format("%d", score, True)


def pulse_text(self,x,y,text,sequence=False,align="center",myOpaque=False,size="9px",timing=0.2,color=None):
    """This method returns a scripted layer of flashing dim/bright text"""
    if not sequence:
        # default sequence
        sequence = [3,1]
    # fonts to use
    if size == "9px":
        levels = [0,self.game.assets.font_9px_az_dim,self.game.assets.font_9px_az_mid,self.game.assets.font_9px_az]
    elif size == "12px":
        # only have two of these for now
        levels = [0,self.game.assets.font_12px_az_dim,0,self.game.assets.font_12px_az]
    # blank list for frames
    script = []
    # iterate through the sequence creating text layers and appending them to anim.frames
    for i in sequence:
        frame = EP_TextLayer(x, y, levels[i], align,opaque=myOpaque)
        if color:
            frame.set_text(text,color=color)
        else:
            frame.set_text(text)
        frame.composite_op = "blacksrc"
        script.append({'seconds':timing,'layer':frame})
    # create an animated layer with the frames
    scriptLayer  = dmd.ScriptedLayer(128,32,script)
    scriptLayer.composite_op = "blacksrc"
    return scriptLayer

