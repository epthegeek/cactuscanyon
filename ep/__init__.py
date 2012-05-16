__all__ = [
    'ep_layers',
    'ep_transition'
]
from ep_layers import *
from ep_transition import *

import locale

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")


DMD_PATH = "dmd/"
LAMPSHOWS_PATH = "lampshows/"
SOUNDS_PATH = "sounds/"
SFX_PATH = "sounds/sfx/"
MUSIC_PATH = "sounds/music/"
QUOTES_PATH = "sounds/quotes/"

# set up a property for last switch tracking
def get_last_switch(self):
    return self.game.lastSwitch

def set_last_switch(self,value):
    self.game.lastSwitch = value

last_switch = property(get_last_switch,set_last_switch)

def format_score(score):
    """Returns a string representation of the given score value.
         Override to customize the display of numeric score values."""
    if score == 0:
        return '00'
    else:
        return locale.format("%d", score, True)


def pulse_9px(self,x,y,text,sequence=False,align="center",myOpaque=False):
    if not sequence:
        # default sequence
        sequence = [3,1,3,1,3,1,3]
    # fonts to use
    levels = [0,self.game.assets.font_9px_az_dim,self.game.assets.font_9px_az_mid,self.game.assets.font_9px_az]
    # blank list for frames
    script = []
    # iterate through the sequence creating text layers and appending them to anim.frames
    for i in sequence:
        frame = dmd.TextLayer(x, y, levels[i], align,opaque=myOpaque).set_text(text)
        frame.composite_op = "blacksrc"
        script.append({'seconds':0.2,'layer':frame})
    # create an animated layer with the frames
    scriptLayer  = dmd.ScriptedLayer(128,32,script)
    scriptLayer.composite_op = "blacksrc"
    return scriptLayer