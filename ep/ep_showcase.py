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
##

from procgame import *
import ep

DMD_PATH = "dmd/"

font_showcase_ll_0 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_LL_0.dmd")
font_showcase_ll_1 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_LL_1.dmd")
font_showcase_ll_2 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_LL_2.dmd")
font_showcase_ll_3 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_LL_3.dmd")
LL_FONT = [font_showcase_ll_0,
           font_showcase_ll_1,
           font_showcase_ll_2,
           font_showcase_ll_3]

font_showcase_ur_0 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_UR_0.dmd")
font_showcase_ur_1 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_UR_1.dmd")
font_showcase_ur_2 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_UR_2.dmd")
font_showcase_ur_3 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Outline_UR_3.dmd")
UR_FONT = [font_showcase_ur_0,
           font_showcase_ur_1,
           font_showcase_ur_2,
           font_showcase_ur_3]

font_showcase_fill_0 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Fill_0.dmd")
font_showcase_fill_1 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Fill_1.dmd")
font_showcase_fill_2 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Fill_2.dmd")
font_showcase_fill_3 = dmd.Font(DMD_PATH + "Font_Custom_Showcase_Fill_3.dmd")
FILL_FONT = [font_showcase_fill_0,
             font_showcase_fill_1,
             font_showcase_fill_2,
             font_showcase_fill_3]

class EP_Showcase(object):

    def make_string(self,ll,ur,fill,x=64,y=0,align="center",isOpaque=False,text="",isTransparent=False,condensed=False):
        print "MY TEXT: " + text
        print "ALIGN: " + str(align)
        if condensed:
            LL_FONT[ll].tracking = -1
            UR_FONT[ur].tracking = -1
            FILL_FONT[fill].tracking = -1
        lowerLeftLayer = dmd.TextLayer(x, y, LL_FONT[ll], align, opaque=False).set_text(text)
        lowerLeftLayer.composite_op = "blacksrc"
        upperRightLayer = dmd.TextLayer(x,y, UR_FONT[ur], align, opaque=False).set_text(text)
        upperRightLayer.composite_op = "blacksrc"
        fillLayer = dmd.TextLayer(x, y, FILL_FONT[fill], align, opaque=False).set_text(text)
        fillLayer.composite_op="blacksrc"
        myLayer = dmd.GroupedLayer(128,32,[lowerLeftLayer,upperRightLayer,fillLayer])
        myLayer.opaque = isOpaque
        if isTransparent:
            myLayer.composite_op = "blacksrc"
        # reset the tracking if we shifted it ?
        if condensed:
            LL_FONT[ll].tracking = 0
            UR_FONT[ur].tracking = 0
            FILL_FONT[fill].tracking = 0
        return myLayer

    def chase_outline(self,outline_start,outline_fin,fill,speed,x=64,y=0,align="center",isOpaque=False,text="",isTransparent=False,condensed=False,hold=0):
        # emtpy script
        script = []
        # make a lower case string
        alt = str.lower(text)
        # make the first frame
        layer = self.make_string(outline_start,outline_start,fill,x,y,align,False,text,True,condensed)
        script.append({'seconds':speed,'layer':layer})
        # loop through the chase part
        for i in range(0,len(text),1):
            string1 = text[:i] + alt[i:i+1] + text[i+1:]
            string2 = alt[:i] + text[i:i+1] + alt[i+1:]
            # generate the 2 lines
            layer1 = self.make_string(outline_start,outline_start,fill,x,y,align,False,string1,True,condensed)
            layer2 = self.make_string(outline_fin, outline_fin,fill,x,y,align,False,string2,True,condensed)
            # make a grouped layer
            combined = dmd.GroupedLayer(128,32,[layer1,layer2])
            # add it to the script
            script.append({'seconds':speed,'layer':combined})

        # then after the loop generate the final frame
        layer = self.make_string(outline_start,outline_start,fill,x,y,align,False,text,True,condensed)
        # check if it's held or not
        if hold == 0:
            hold = speed
        # and add that to the script
        script.append({'seconds':hold,'layer':layer})
        # then make the scripted layer
        myLayer = dmd.ScriptedLayer(128,32,script)
        # set blacksrc if called for
        if isTransparent:
            myLayer.composite_op = "blacksrc"
        # if it's opaque, set that
        if isOpaque:
            myLayer.opaque = True

        ## and return the layer
        return myLayer