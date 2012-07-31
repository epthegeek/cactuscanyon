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
##  The idea here is to have a really high priority layer that can but in over the top
##  of the regular display for things that are important
##

from procgame import *
from assets import *
import cc_modes
import ep

class Interrupter(ep.EP_Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Interrupter, self).__init__(game, priority)
        self.rotator = [True,False,False,False,False]
        self.statusDisplay = "Off"
        self.page = 0

    def display_player_number(self,idle=False):
        # if the skillshot display is busy, we don't trample on it
        if not self.game.skill_shot.busy:
            # for when the ball is sitting in the shooter lane with nothing going on
            myNumber = ("ONE<","TWO*","THREE<","FOUR>")
            # get the current player
            p = self.game.current_player_index
            print p
            # set up the text
            textString = "PLAYER> " + myNumber[p]
            textLayer = dmd.TextLayer(128/2, 7, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(textString)
            script = [{'seconds':0.3,'layer':textLayer},{'seconds':0.3,'layer':None}]
            display = dmd.ScriptedLayer(128,32,script)
            display.composite_op = "blacksrc"
            # turn the display on
            self.layer = display
            # every fifth time razz them
            if self.rotator[0]:
                self.game.base.play_quote(self.game.assets.quote_dontJustStandThere)
            # then stick the current value on the end
            foo = self.rotator.pop(0)
            self.rotator.append(foo)
            ## then shift 0 to the end
            self.delay(name="clearInterrupter",delay=1.5,handler=self.clear_layer)
        # with an idle call, set a repeat
        if idle:
            self.delay(name="idle",delay=10,handler=self.display_player_number,param=True)

    def cancel_idle(self):
        self.cancel_delayed("idle")

    def abort_player_number(self):
        self.cancel_delayed("clearInterrupter")
        self.cancel_delayed("idle")
        self.layer = None

    def tilt_danger(self,status):
        # if it puts us at 2, time for second warning
        if status == 2:
            print "DANGER DANGER"
            # double warning
            line1 = dmd.TextLayer(128/2, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            line2 = dmd.TextLayer(128/2, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            self.layer = dmd.GroupedLayer(128,32,[line1,line2])
            # play a sound
            myWait = self.play_tilt_sound()
            self.delay(delay=0.5,handler=self.play_tilt_sound())
            self.delay(delay=1,handler=self.clear_layer)

        # otherwise this must be the first warning
        else:
            print "DANGER"
            #add a display layer and add a delayed removal of it.
            self.layer = dmd.TextLayer(128/2, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("DANGER")
            #play sound
            self.play_tilt_sound()
            self.delay(delay=1,handler=self.clear_layer)

    def tilt_display(self):
        # build a tilt graphic
        tiltLayer = dmd.TextLayer(128/2, 7, self.game.assets.font_20px_az, "center", opaque=True).set_text("TILT")
        # Display the tilt graphic
        self.layer = tiltLayer

    def play_tilt_sound(self):
        self.game.sound.play(self.game.assets.sfx_tiltDanger)

    def ball_saved(self):
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_dontMove)
        # show some display
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'skyline.dmd').frames[0])
        myLayer = dmd.TextLayer(128/2,14, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text("BALL SAVED")
        myLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[backdrop,myLayer])
        self.layer = combined
        self.delay(delay=1,handler=self.clear_layer)

    def closing_song(self,duration):
        self.delay(delay=duration+1,handler=self.game.base.music_on,param=self.game.assets.music_mainTheme)
        # and set a delay to fade it out after 2 minutes
        self.delay(delay=60,handler=self.game.sound.fadeout_music)

    def showdown_hit(self,points):
        pointString = ep.format_score(points)
        textLine1 = dmd.TextLayer(128/2, 0, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("BAD GUY SHOT!")
        textLine2 = dmd.TextLayer(128/2, 15, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text(pointString,blink_frames=8)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2])
        combined.composite_op = "blacksrc"
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.clear_layer)

    def ball_added(self):
        textLine = dmd.TextLayer(128/2, 9, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text("BALL ADDED",blink_frames=8)
        textLine.composite_op = "blacksrc"
        self.layer = textLine
        self.delay(name="Display",delay=1,handler=self.clear_layer)

    def ball_save_activated(self):
        textLine1 = dmd.TextLayer(128/2, 0, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("BALL SAVER")
        textLine2 = dmd.TextLayer(128/2, 15, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text("ACTIVATED",blink_frames=8)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2])
        combined.composite_op = "blacksrc"
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.clear_layer)

    def dude_escaped(self,amount):
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'escaped.dmd').frames[0])
        backdrop.composite_op = "blacksrc"
        if amount <= 0:
            textString = "THEY GOT AWAY - YOU LOSE"
        else:
            textString = str(amount) + " MORE AND YOU LOSE"
        textLine2 = dmd.TextLayer(128/2, 18, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString,blink_frames=8)
        textLine2.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine2])
        combined.composite_op = "blacksrc"
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.clear_layer)


    ## Status section, for the HALIBUT

    # hold a flipper for 5 seconds to start - but only turn it on if it's not already on
    def sw_flipperLwR_active_for_5s(self,sw):
        if self.statusDisplay == "Off":
            self.status_on('Right')

    def sw_flipperLwL_active_for_5s(self,sw):
        if self.statusDisplay == "Off":
            self.status_on('Left')

    # releasing the flipper you started with cancels the status
    def sw_flipperLwR_inactive(self,sw):
        if self.statusDisplay == "Right":
            self.status_off()

    def sw_flipperLwL_inactive(self,sw):
        if self.statusDisplay == "Left":
            self.status_off()

    # tapping a flipper should skip slides - if the other flipper has the status active
    def sw_flipperLwL_active(self,sw):
        if self.statusDisplay == "Right":
            self.status()

    def sw_flipperLwR_active(self,sw):
        if self.statusDisplay == "Left":
            self.status()

    def status_on(self,side):
        self.statusDisplay = side
        print "STATUS GOES HERE"
        # disable ball search
        self.game.ball_search.disable()
        # start the status display
        self.status()

    def status_off(self):
        self.statusDisplay = "Off"
        print "STATUS ENDING"
        self.cancel_delayed("Display")
        # enable ball search
        self.game.ball_search.enable()
        # clear the layer
        self.layer = None
        # reset the page to 0
        self.page = 0

    def status(self):
        # cancel the delay, in case we got pushed early
        self.cancel_delayed("Display")
        # first, tick up the page
        self.page += 1
        # roll back around if we get over the number of pages
        if self.page > 4:
            self.page = 1
        # then show some junk based on what page we're on
        if self.page == 1:
            textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_12px_az, "center", opaque=True).set_text("CURRENT")
            textLine2 = dmd.TextLayer(128/2, 16, self.game.assets.font_12px_az, "center", opaque=False).set_text("STATUS")
            textLine2.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[textLine1,textLine2])
            self.layer = combined
        # bonus information
        if self.page == 2:
            multiplier = self.game.show_tracking('bonusX')
            textString2 = str(multiplier) + "X MULTIPLIER"
            bonus = self.game.show_tracking('bonus')
            textString3 = "BONUS: " + ep.format_score(bonus)
            # default three line display
            self.tld("BONUS INFO:", textString2, textString3)
        if self.page == 3:
        # hits left to light drunk multiball
            locked = self.game.show_tracking('ballsLocked')
            if locked == 1:
                textString2 = str(locked) + " BALL LOCKED"
            else:
                textString2 = str(locked) + " BALLS LOCKED"
            shots = self.game.show_tracking('mineShotsTotal')
            textString3 = str(shots) + " MINE SHOTS TOTAL"
            # stock three line display
            self.tld("MINE STATUS:", textString2, textString3)
        if self.page == 4:
            # hits left to light drunk multiball
            left = self.game.user_settings['Gameplay (Feature)']['Beer Mug Hits For Multiball'] - self.game.show_tracking('beerMugHits')
            if left <= 0:
                textString2 = "DRUNK MULTIBALL"
                textString3 = "IS LIT"
            else:
                textString2 = str(left) + " MORE HITS"
                textString3 = "FOR MULTIBALL"
                # default three line display
            self.tld("BEER MUG:",textString2,textString3)
            # circle back and clear the layer
        self.delay(name="Display",delay=3,handler=self.status)

    def tld(self,textString1,textString2,textString3):
        textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString1)
        textLine2 = dmd.TextLayer(128/2, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)
        textLine3 = dmd.TextLayer(128/2, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString3)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3])
        self.layer = combined

    def shoot_again(self,step=1):
        # shown when starting an extra ball
        if step == 1:
            imageLayer = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'shoot-again.dmd').frames[0])
            self.game.base.play_quote(self.game.assets.quote_deepLaugh)
            self.game.sound.play(self.game.assets.sfx_incoming)
            self.layer = imageLayer
            self.delay(delay = 2,handler=self.shoot_again, param=2)
        if step == 2:
            anim = dmd.Animation().load(ep.DMD_PATH+'shoot-again.dmd')
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            animLayer.opaque = True
            animLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_lowBoom)
            animLayer.add_frame_listener(4,self.game.trough.launch_balls,param=1)
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.shoot_again,param=3)
        if step == 3:
            imageLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'shoot-again.dmd').frames[7])
            self.game.base.play_quote(self.game.assets.quote_shootAgain)
            textLine1 = dmd.TextLayer(80,5, self.game.assets.font_9px_az, "center", opaque= False).set_text("SHOOT")
            textLine2 = dmd.TextLayer(80,15, self.game.assets.font_9px_az, "center", opaque= False).set_text("AGAIN")
            combined = dmd.GroupedLayer(128,32,[imageLayer,textLine1,textLine2])
            self.layer = combined
            self.delay(delay = 1.5,handler=self.clear_layer)
            self.delay(delay = 1.5,handler=self.game.ball_starting)


    # delayed music on used by highscore
    def delayed_music_on(self,wait,song=None):
        self.delay(delay=wait, handler=self.music_on,param=song)

    def music_on(self,song=None):
        # if a song is passed, set that to the active song
        # if not, just re-activate the current
        if song:
            self.current_music = song
        self.game.sound.play_music(self.current_music, loops=-1)
