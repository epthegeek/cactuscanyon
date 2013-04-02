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
import time

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

    def set_target_position(self, x, y):
        """Setter for :attr:`target_x` and :attr:`target_y`."""
        self.target_x = x
        self.target_y = y

class EP_TextLayer(dmd.layers.Layer):
    """Layer that displays text."""

    fill_color = None
    """Dot value to fill the frame with.  Requres that ``width`` and ``height`` be set.  If ``None`` only the font characters will be drawn."""

    def __init__(self, x, y, font, justify="left", opaque=False, width=128, height=32, fill_color=None,font_color=0x0):
        super(EP_TextLayer, self).__init__(opaque)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.font = font
        self.started_at = None
        self.seconds = None # Number of seconds to show the text for
        self.frame = None # Frame that text is rendered into.
        self.frame_old = None
        self.justify = justify
        self.blink_frames = None # Number of frame times to turn frame on/off
        self.blink_frames_counter = 0
        #self.bitmap = font.bitmap
        #self.set_color(font_color)

    def set_color(self,color):
        w = self.bitmap.width
        h = self.bitmap.height
        frame = dmd.Frame(w,h)
        for y in range(h):
            for x in range(w):
                dot = self.bitmap.get_dot(x, y)
                newdot = ((color << 4) | (dot & 0xf))
                frame.set_dot(x,y,newdot)
        self.bitmap = frame

    def set_text(self, text, seconds=None, blink_frames=None,font_color=0x0):
        """Displays the given message for the given number of seconds."""
        self.started_at = None
        self.seconds = seconds
        self.blink_frames = blink_frames
        self.blink_frames_counter = self.blink_frames
        if text == None:
            self.frame = None
        else:
            (w, h) = self.font.size(text)
            x, y = 0, 0
            if self.justify == 'left':
                (x, y) = (0,0)
            elif self.justify == 'right':
                (x, y) = (-w,0)
            elif self.justify == 'center':
                (x, y) = (-w/2,0)

            if self.fill_color != None:
                self.set_target_position(0, 0)
                self.frame = dmd.Frame(width=self.width, height=self.height)
                self.frame.fill_rect(0, 0, self.width, self.height, self.fill_color)
                self.draw_font(self.frame, text, self.x + x, self.y + y)
            else:
                self.set_target_position(self.x, self.y)
                (w, h) = self.font.size(text)
                self.frame = dmd.Frame(w, h)
                self.draw_font(self.frame, text, 0, 0)
                (self.target_x_offset, self.target_y_offset) = (x,y)

        return self

    def draw_font(self, frame, text, x, y):
        """Uses this font's characters to draw the given string at the given position."""
        for ch in text:
            char_offset = ord(ch) - ord(' ')
            if char_offset < 0 or char_offset >= 96:
                continue
            char_x = self.font.char_size * (char_offset % 10)
            char_y = self.font.char_size * (char_offset / 10)
            width = self.font.char_widths[char_offset]
            dmd.Frame.copy_rect(dst=frame, dst_x=x, dst_y=y, src=self.bitmap, src_x=char_x, src_y=char_y, width=width, height=self.font.char_size, op=self.composite_op)
            x += width + self.font.tracking
        return x


    def next_frame(self):
        if self.started_at == None:
            self.started_at = time.time()
        if (self.seconds != None) and ((self.started_at + self.seconds) < time.time()):
            self.frame = None
        elif self.blink_frames > 0:
            if self.blink_frames_counter == 0:
                self.blink_frames_counter = self.blink_frames
                if self.frame == None:
                    self.frame = self.frame_old
                else:
                    self.frame_old = self.frame
                    self.frame = None
            else:
                self.blink_frames_counter -= 1
        return self.frame

    def is_visible(self):
        return self.frame != None
