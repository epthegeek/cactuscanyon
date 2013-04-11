import sys
import procgame
import pinproc
from threading import Thread
import random
import string
import time
import locale
import math
import copy
import ctypes
import itertools
from procgame.events import EventManager
import os

try:
    import pygame
    import pygame.locals
except ImportError:
    print "Error importing pygame; ignoring."
    pygame = None

if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
PyObject_AsWriteBuffer.restype = ctypes.c_int
PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes


class EP_Desktop():
    """The :class:`Desktop` class helps manage interaction with the desktop, providing both a windowed
    representation of the DMD, as well as translating keyboard input into pyprocgame events."""

    exit_event_type = 99
    """Event type sent when Ctrl-C is received."""

    key_map = {}

    def __init__(self):
        self.ctrl = 0
        self.i = 0

        if 'pygame' in globals():
            self.setup_window()
        else:
            print 'Desktop init skipping setup_window(); pygame does not appear to be loaded.'
        self.add_key_map(pygame.locals.K_LSHIFT, 3)
        self.add_key_map(pygame.locals.K_RSHIFT, 1)

    def load_images(self,dots_path):
        ## dot images
        dot_black = pygame.image.load(dots_path+ 'DotBlack.png')
        dot_dark_grey_low = pygame.image.load(dots_path+ 'DotDarkGreyLow.png')
        dot_dark_grey_mid = pygame.image.load(dots_path+ 'DotDarkGreyMid.png')
        dot_dark_grey = pygame.image.load(dots_path+ 'DotDarkGrey.png')
        dot_dark_red_low = pygame.image.load(dots_path+ 'DotDarkRedLow.png')
        dot_dark_red_mid = pygame.image.load(dots_path+ 'DotDarkRedMid.png')
        dot_dark_red = pygame.image.load(dots_path+ 'DotDarkRed.png')
        dot_grey_low = pygame.image.load(dots_path+ 'DotGreyLow.png')
        dot_grey_mid = pygame.image.load(dots_path+ 'DotGreyMid.png')
        dot_grey = pygame.image.load(dots_path+ 'DotGrey.png')
        dot_dark_brown_low = pygame.image.load(dots_path+ 'DotDarkBrownLow.png')
        dot_dark_brown_mid = pygame.image.load(dots_path+ 'DotDarkBrownMid.png')
        dot_dark_brown = pygame.image.load(dots_path+ 'DotDarkBrown.png')
        dot_brown_low = pygame.image.load(dots_path+ 'DotBrownLow.png')
        dot_brown_mid = pygame.image.load(dots_path+ 'DotBrownMid.png')
        dot_brown = pygame.image.load(dots_path+ 'DotBrown.png')
        dot_red_low = pygame.image.load(dots_path+ 'DotRedLow.png')
        dot_red_mid = pygame.image.load(dots_path+ 'DotRedMid.png')
        dot_red = pygame.image.load(dots_path+ 'DotRed.png')
        dot_dark_green_low = pygame.image.load(dots_path+ 'DotDarkGreenLow.png')
        dot_dark_green_mid = pygame.image.load(dots_path+ 'DotDarkGreenMid.png')
        dot_dark_green = pygame.image.load(dots_path+ 'DotDarkGreen.png')
        dot_flesh_low = pygame.image.load(dots_path+ 'DotFleshLow.png')
        dot_flesh_mid = pygame.image.load(dots_path+ 'DotFleshMid.png')
        dot_flesh = pygame.image.load(dots_path+ 'DotFlesh.png')
        dot_purple_low = pygame.image.load(dots_path+ 'DotPurpleLow.png')
        dot_purple_mid = pygame.image.load(dots_path+ 'DotPurpleMid.png')
        dot_purple = pygame.image.load(dots_path+ 'DotPurple.png')
        dot_green_low = pygame.image.load(dots_path+ 'DotGreenLow.png')
        dot_green_mid = pygame.image.load(dots_path+ 'DotGreenMid.png')
        dot_green = pygame.image.load(dots_path+ 'DotGreen.png')
        dot_yellow_low = pygame.image.load(dots_path+ 'DotYellowLow.png')
        dot_yellow_mid = pygame.image.load(dots_path+ 'DotYellowMid.png')
        dot_yellow = pygame.image.load(dots_path+ 'DotYellow.png')
        dot_blue_low = pygame.image.load(dots_path+ 'DotBlueLow.png')
        dot_blue_mid = pygame.image.load(dots_path+ 'DotBlueMid.png')
        dot_blue = pygame.image.load(dots_path+ 'DotBlue.png')
        dot_orange_low = pygame.image.load(dots_path+ 'DotOrangeLow.png')
        dot_orange_mid = pygame.image.load(dots_path+ 'DotOrangeMid.png')
        dot_orange = pygame.image.load(dots_path+ 'DotOrange.png')
        dot_cyan_low = pygame.image.load(dots_path+ 'DotCyanLow.png')
        dot_cyan_mid = pygame.image.load(dots_path+ 'DotCyanMid.png')
        dot_cyan = pygame.image.load(dots_path+ 'DotCyan.png')
        #dot_white_low = pygame.image.load(dots_path+ 'DotWhiteLow.png')
        #dot_white_mid = pygame.image.load(dots_path+ 'DotWhiteMid.png')
        #dot_white = pygame.image.load(dots_path+ 'DotWhite.png')
        dot_white_255 = pygame.image.load(dots_path+ 'DotWhite255.png')
        dot_white_238 = pygame.image.load(dots_path+ 'DotWhite238.png')
        dot_white_221 = pygame.image.load(dots_path+ 'DotWhite221.png')
        dot_white_204 = pygame.image.load(dots_path+ 'DotWhite204.png')
        dot_white_187 = pygame.image.load(dots_path+ 'DotWhite187.png')
        dot_white_170 = pygame.image.load(dots_path+ 'DotWhite170.png')
        dot_white_153 = pygame.image.load(dots_path+ 'DotWhite153.png')
        dot_white_136 = pygame.image.load(dots_path+ 'DotWhite136.png')
        dot_white_119 = pygame.image.load(dots_path+ 'DotWhite119.png')
        dot_white_102 = pygame.image.load(dots_path+ 'DotWhite102.png')
        dot_white_085 = pygame.image.load(dots_path+ 'DotWhite085.png')
        dot_white_068 = pygame.image.load(dots_path+ 'DotWhite068.png')
        dot_white_051 = pygame.image.load(dots_path+ 'DotWhite051.png')
        dot_white_034 = pygame.image.load(dots_path+ 'DotWhite034.png')
        dot_magenta_low = pygame.image.load(dots_path+ 'DotMagentaLow.png')
        dot_magenta_mid = pygame.image.load(dots_path+ 'DotMagentaMid.png')
        dot_magenta = pygame.image.load(dots_path+ 'DotMagenta.png')

        self.colors = [[None,None,None,None], # blank
                       [None,dot_grey_low,dot_grey_mid,dot_grey], # color 1 grey
                       [None,dot_dark_grey_low,dot_dark_grey_mid,dot_dark_grey], # color 2 dark grey
                       [None,dot_dark_green_low,dot_dark_green_mid,dot_dark_green], # color 3 dark green
                       [None,dot_flesh_low,dot_flesh_mid,dot_flesh], # color 4 flesh tone
                       [None,dot_purple_low,dot_purple_mid,dot_purple], # color 5 purple
                       [None,dot_dark_red_low,dot_dark_red_mid,dot_dark_red], # color 6 dark red
                       [None,dot_brown_low,dot_brown_mid,dot_brown], # color 7 - Brown
                       [None,dot_dark_brown_low,dot_dark_brown_mid,dot_dark_brown], # color 8 dark brown
                       [None,dot_red_low,dot_red_mid,dot_red], # color 9 - Red
                       [None,dot_green_low,dot_green_mid,dot_green], # color 10 - Green
                       [None,dot_yellow_low,dot_yellow_mid,dot_yellow], # color 11 - Yellow
                       [None,dot_blue_low,dot_blue_mid,dot_blue], # color 12 blue
                       [None,dot_orange_low,dot_orange_mid,dot_orange], # color 13 orange
                       [None,dot_cyan_low,dot_cyan_mid,dot_cyan], # color 14 - cyan
                       [None,dot_magenta_low,dot_magenta_mid,dot_magenta], # color 15 - magenta
                       #[None,dot_white_low,dot_white_mid,dot_white]] # default color - white
                       [None,None,dot_white_034,dot_white_051,dot_white_068,dot_white_085,dot_white_102,dot_white_119,dot_white_136,dot_white_153,dot_white_170,dot_white_187,dot_white_204,dot_white_221,dot_white_238,dot_white_255]]


    def add_key_map(self, key, switch_number):
        """Maps the given *key* to *switch_number*, where *key* is one of the key constants in :mod:`pygame.locals`."""
        self.key_map[key] = switch_number

    def clear_key_map(self):
        """Empties the key map."""
        self.key_map = {}

    def get_keyboard_events(self):
        """Asks :mod:`pygame` for recent keyboard events and translates them into an array
        of events similar to what would be returned by :meth:`pinproc.PinPROC.get_events`."""
        key_events = []
        for event in pygame.event.get():
            EventManager.default().post(name=self.event_name_for_pygame_event_type(event.type), object=self, info=event)
            key_event = {}
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_RCTRL or event.key == pygame.locals.K_LCTRL:
                    self.ctrl = 1
                if event.key == pygame.locals.K_c:
                    if self.ctrl == 1:
                        key_event['type'] = self.exit_event_type
                        key_event['value'] = 'quit'
                elif (event.key == pygame.locals.K_ESCAPE):
                    key_event['type'] = self.exit_event_type
                    key_event['value'] = 'quit'
                elif event.key in self.key_map:
                    key_event['type'] = pinproc.EventTypeSwitchClosedDebounced
                    key_event['value'] = self.key_map[event.key]
            elif event.type == pygame.locals.KEYUP:
                if event.key == pygame.locals.K_RCTRL or event.key == pygame.locals.K_LCTRL:
                    self.ctrl = 0
                elif event.key in self.key_map:
                    key_event['type'] = pinproc.EventTypeSwitchOpenDebounced
                    key_event['value'] = self.key_map[event.key]
            if len(key_event):
                key_events.append(key_event)
        return key_events


    event_listeners = {}

    def event_name_for_pygame_event_type(self, event_type):
        return 'pygame(%s)' % (event_type)

    screen = None
    """:class:`pygame.Surface` object representing the screen's surface."""
    screen_multiplier = 4

    def setup_window(self):
        pygame.init()
        xOffset = 43
        yOffset = 224
        #self.screen = pygame.display.set_mode((128*self.screen_multiplier, 32*self.screen_multiplier))
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xOffset,yOffset)
        self.screen = pygame.display.set_mode((1280,320))
        pygame.display.set_caption('Cactus Canyon Continued')

    def draw(self, frame):
        """Draw the given :class:`~procgame.dmd.Frame` in the window."""
        # Use adjustment to add a one pixel border around each dot, if
        # the screen size is large enough to accomodate it.
        if self.screen_multiplier >= 4:
            adjustment = -1
        else:
            adjustment = 0

        #bytes_per_pixel = 4
        #y_offset = 128*bytes_per_pixel*self.screen_multiplier*self.screen_multiplier
        #x_offset = bytes_per_pixel*self.screen_multiplier

        #surface_array = array(self.screen)

        frame_string = frame.get_data()

        x = 0
        y = 0
        # fill the screen black
        self.screen.fill((0,0,0))

        for dot in frame_string:
            dot_value = ord(dot)
            image = None
            # if we got something other than 0
            if dot_value != 0:
                # set the brightness and color
                brightness = (dot_value&0xf)
                # if we have a brightness but no color - use white
                if brightness and (dot_value >>4) == 0:
                    color = 16
                    bright_value = brightness
                # otherwise, find the color and set the brightness
                else:
                    if brightness <= 4:
                        bright_value = 0
                    elif brightness <= 9:
                        bright_value = 1
                    elif brightness <= 14:
                        bright_value = 2
                    else:
                        bright_value = 3
                    color = (dot_value >> 4)
                #print "Dot Value: " + str(derp) +" - color: " + str(color) + " - Brightness: " +str(brightness)
                # set the image based on color and brightness
                image = self.colors[color][bright_value]


            #color_val = ord(dot)*16
            #index = y*y_offset + x*x_offset
            #surface_array[index:index+bytes_per_pixel] = (color_val,color_val,color_val,0)
            if image:
                self.screen.blit(image, ((x*10), (y*10)))
            x += 1
            if x == 128:
                x = 0
                y += 1
        #del surface_array

        pygame.display.update()

    def __str__(self):
        return '<Desktop pygame>'

