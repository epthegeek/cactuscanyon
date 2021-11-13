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
##

from procgame import *
import ep
import os

curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
DMD_PATH = curr_file_path + "/../dmd/"

class EP_CustomMessageFrame(object):
    def __init__(self):
        pass

    def make_frame(self,game,frame):
        self.game = game
        # a list so I can just use the font size number to reference the font
        self.fonts = [None,None,None,None,None,self.game.assets.font_5px_bold_AZ,None,self.game.assets.font_7px_bold_az,None,self.game.assets.font_9px_az,None,None,self.game.assets.font_12px_az]
        self.page = frame
        self.texts = [None,None,None,None]
        self.colors = [None,None,None,None]
        self.justify = [None,None,None,None]
        self.size = [0,0,0,0]
        self.totalHeight = 0
        self.totalLines = 0
        self.x_offsets = [0,0,0,0]
        self.y_offsets = [0,0,0,0]

        # get the border
        border = self.game.user_settings['Custom Message']['Page ' + str(self.page) + ' Border']
        if border == "ROPE":
            myBorder = self.game.assets.dmd_ropeBorder
        elif border == "SIMPLE":
            myBorder = self.game.assets.dmd_simpleBorder
        elif border == "GUNS":
            myBorder = self.game.assets.dmd_gunsBorder
        elif border == "SKULLS":
            myBorder = self.game.assets.dmd_skullsBorder
        elif border == "STARS":
            myBorder = self.game.assets.dmd_starsBorder
        elif border == "TRACKS":
            myBorder = self.game.assets.dmd_tracksBorder
        elif border == "THIN":
            myBorder = self.game.assets.dmd_stringBorder
        elif border == "PIXEL":
            myBorder = self.game.assets.dmd_singlePixelBorder
        # otherwise blank
        else:
            myBorder = self.game.assets.dmd_blank
        self.backdrop = dmd.FrameLayer(opaque=False, frame=myBorder.frames[0])

        # get all the bits
        # step through the lines getting the data
        for n in range (1,4,1):
            self.game.logger.debug("Generating Line " + str(n))
            line = 'Page ' + str(self.page) + ' Line ' + str(n) + ' '
            if self.game.user_settings['Custom Message'][line + 'Text'] != 'NONE':
                self.texts[n] = self.game.user_settings['Custom Message'][str(line) + 'Text']
                myColor = self.game.user_settings['Custom Message'][str(line) + 'Color']
                if myColor == 'BLUE':
                    self.colors[n] = ep.BLUE
                elif myColor == 'YELLOW':
                    self.colors[n] = ep.YELLOW
                elif myColor == 'MAGENTA':
                    self.colors[n] = ep.MAGENTA
                elif myColor == 'RED':
                    self.colors[n] = ep.RED
                elif myColor == 'CYAN':
                    self.colors[n] = ep.CYAN
                elif myColor == 'GREEN':
                    self.colors[n] = ep.GREEN
                elif myColor == 'ORANGE':
                    self.colors[n] = ep.ORANGE
                else:
                    self.colors[n] = ep.WHITE
                self.justify[n] = self.game.user_settings['Custom Message'][str(line) + 'Justify']
                if self.justify[n] == 'CENTER':
                    self.x_offsets[n] = 64
                elif self.justify[n] == 'LEFT':
                    if border == "GUNS" or border == "SKULLS":
                        self.x_offsets[n] = 24
                    elif border == "STARS" or border == "TRACKS":
                        self.x_offsets[n] = 18
                    else:
                        self.x_offsets[n] = 6
                # other option is right
                else:
                    if border == "GUNS" or border == "SKULLS":
                        self.x_offsets[n] = 104
                    elif border == "STARS" or border == "TRACKS":
                        self.x_offsets[n] = 110
                    else:
                        self.x_offsets[n] = 122

                size = self.game.user_settings['Custom Message'][str(line) + 'Size']
                self.size[n] = size
                self.totalHeight += size
                self.totalLines += 1
            else:
                self.game.logger.debug("No Line " + str(n))

        # generate the vertical offsets
        # if we didn't find any lines - return just the backdrop
        if self.totalLines == 0:
            return self.backdrop

        elif self.totalLines == 1:
            self.game.logger.debug("One Total Lines")
            # subtract the font height from the full height and divide by 2
            offset = ((32 - self.size[1]) / 2)
            self.y_offsets[1] = offset
        elif self.totalLines == 2:
            self.game.logger.debug("Two Total Lines")
            # add the fonts together, plus 2, subtract from 32, divide by 2 for first
            offset = ((32 - (self.size[1] + self.size[2] + 1)) / 2)
            self.y_offsets[1] = offset
            # second is font height plus 2
            offset += (self.size[1] + 2)
            self.y_offsets[2] = offset
        # three lines
        else:
            self.game.logger.debug("Three Total Lines")
            # add the fonts together, plus 2, subtract from 32, divide by 2 for the first - if total plus 2 is higher than 32, use 0
            tempOffset = (32 - (self.size[1] + self.size[2] + self.size[3] + 2))
            if tempOffset <= 0:
                offset = 0
            else:
                offset = tempOffset / 2
            self.y_offsets[1] = offset
            offset += (self.size[1] + 1)
            self.y_offsets[2] = offset
            offset += (self.size[2] + 1)
            self.y_offsets[3] = offset

        layers = []
        # add the backdrop
        layers.append(self.backdrop)
        # then generate the text lines
        for n in range (1,(self.totalLines+1),1):
            self.game.logger.debug("Layer line " + str(n) + " x offset " + str(self.x_offsets[n]) + " y offset " + str(self.y_offsets[n]))
            if self.size[n] == 7 or self.size[n] == 9:
                self.y_offsets[n] -= 1
            if self.size[n] == 12:
                self.y_offsets[n] -= 2
            layer = ep.EP_TextLayer(self.x_offsets[n], self.y_offsets[n], self.fonts[self.size[n]], str(self.justify[n]).lower(), opaque=False).set_text(self.texts[n],color=self.colors[n])
            layer.composite_op = "blacksrc"
            layers.append(layer)

        # and OUTPUT THAT THING
        self.game.logger.debug("building grouped layer")
        self.game.logger.debug(layers)
        composite = dmd.GroupedLayer(128,32,layers)
        return composite

class EP_MessagePreview(ep.EP_Mode):
    def __init__(self, game, priority, page,return_handler):
        super(EP_MessagePreview, self).__init__(game, priority)
        self.game = game
        self.page = page
        self.return_handler = return_handler

    def mode_started(self):
        self.layer = EP_CustomMessageFrame().make_frame(self.game,self.page)
        self.delay(delay = 4,handler=self.return_handler)

