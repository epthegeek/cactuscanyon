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
##  The idea here is to have a really high priority layer that can but in over the top
##  of the regular display for things that are important
##

from procgame import dmd
import ep
import random

class Interrupter(ep.EP_Mode):
    """Cactus Canyon Interrupter Jones"""
    def __init__(self, game, priority):
        super(Interrupter, self).__init__(game, priority)
        self.myID = "Interrupter Jones"
        self.rotator = [True,False,False,False,False]
        self.statusDisplay = "Off"
        self.page = 0
        self.playing = False
        self.hush = False
        self.knockerStrength = self.game.user_settings['Machine (Standard)']['Real Knocker Strength']
        self.idle = False
        self.keys_index = {'shoot_again':list(range(len(self.game.sound.sounds[self.game.assets.quote_shootAgain])))}
        self.counts_index = {'shoot_again':0}
        random.shuffle(self.keys_index['shoot_again'])


    def display_player_number(self,idle=False):
        # if the skillshot display is busy, we don't trample on it
        if not self.game.skill_shot.busy:
            # for when the ball is sitting in the shooter lane with nothing going on
            myNumber = ("ONE","TWO","THREE","FOUR")
            # get the current player
            p = self.game.current_player_index
            # set up the text
            textString = "PLAYER> " + myNumber[p]
            textLayer = ep.EP_TextLayer(128/2, 7, self.game.assets.font_12px_az_outline, "center", opaque=False)
            textLayer.composite_op = "blacksrc"
            textLayer.set_text(textString)
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
            self.delay(name="Display",delay=1.5,handler=self.clear_layer)
        # with an idle call, set a repeat
        if idle:
            self.idle = True
            self.delay(name="idle",delay=10,handler=self.display_player_number,param=True)

    def cancel_idle(self):
        self.idle = False
        self.cancel_delayed("idle")

    def abort_player_number(self):
        if self.idle:
            self.cancel_delayed("Display")
            self.cancel_delayed("idle")
            self.idle = False
            self.layer = None

    def score_overlay(self,points,multiplier,textColor):
        # points is the shot value, multiplier is the active combo multiplier
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False)
        string = "< " + str(ep.format_score(points))
        if multiplier > 1:
            string = string + " X " + str(multiplier)
        string = string + " >"
        textLayer.set_text(string,color=textColor)
        self.layer = textLayer
        self.delay("Display",delay=1.5,handler=self.clear_layer)

    def tilt_danger(self,status):
        self.cancel_delayed("Display")
        # if it puts us at 2, time for second warning
        if status == 2:
            print "DANGER DANGER"
            # double warning
            line1 = ep.EP_TextLayer(128/2, 1, self.game.assets.font_dangerFont, "center", opaque=False).set_text("D A N G E R",color=ep.RED)
            line1.composite_op = "blacksrc"
            line2 = ep.EP_TextLayer(128/2, 16, self.game.assets.font_dangerFont, "center", opaque=False).set_text("D A N G E R",color=ep.RED)
            line2.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[line1,line2])
            combined.composite_op = "blacksrc"
            self.layer = combined
            # play a sound
            myWait = self.play_tilt_sound()
            self.delay(delay=0.5,handler=self.play_tilt_sound)
            self.delay("Display",delay=1,handler=self.clear_layer)

        # otherwise this must be the first warning
        else:
            print "Display"
            #add a display layer and add a delayed removal of it.
            if status > 2:
                string = "DANGER X " + str(status)
            else:
                string = "D A N G E R"
            line1 = ep.EP_TextLayer(128/2, 10, self.game.assets.font_dangerFont, "center", opaque=False).set_text(string,color=ep.RED)
            line1.composite_op = "blacksrc"
            self.layer = line1
            #play sound
            self.play_tilt_sound()
            self.delay("Display",delay=1,handler=self.clear_layer)

    def tilt_display(self,slam=False):
        self.cancel_delayed("Display")

        if slam:
            # kill all delays
            for mode in self.game.modes:
                mode.__delayed = []
            self.game.mute = True
            self.stop_music()
            self.game.sound.play(self.game.assets.sfx_slam)
            # slam display goes here
            tiltLayer = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_slammed.frames[0])
            textLayer = self.game.showcase.make_string(2,3,0,x=64,y=0,align="center",isOpaque=False,text="S L A M",isTransparent=True,condensed=False)

            # Display the tilt graphic
            self.layer = dmd.GroupedLayer(128,32,[tiltLayer,textLayer])
            self.delay(delay=1.8,handler=self.game.sound.play,param=self.game.assets.quote_dejected)
            self.delay(delay=3.5,handler=self.game.reset)
        else:
            # if in rectify party mode show rectify instead of tilt
            if self.game.party_setting == 'Rectify':
                displayString = "RECTIFY"
                tiltSound = self.game.assets.sfx_spinDown
                soundDelay = 0
            else:
                displayString = "TILT"
                tiltSound = self.game.assets.quote_tilt
                soundDelay = 1.5
            # build a tilt graphic
            tiltLayer = ep.EP_TextLayer(128/2, 7, self.game.assets.font_20px_az, "center", opaque=True).set_text(displayString,color=ep.RED)
            # Display the tilt graphic
            self.layer = tiltLayer
            # play the tilt quote
            self.delay(delay=soundDelay,handler=self.game.sound.play,param=tiltSound)

    def tilted(self):
        print "Interrupter Passing Tilt"
        pass

    def play_tilt_sound(self):
        self.game.sound.play(self.game.assets.sfx_tiltDanger)

    def ball_saved(self):
    # don't show in certain situations
        if self.game.drunk_multiball.running or \
           self.game.moonlight.running or \
           self.game.marshall_multiball.running or \
           self.game.gm_multiball.running or \
           self.game.stampede.running or \
           self.game.cva.running or \
           self.game.last_call.running:
            return
        # otherwise, party on
        # play a quote
        self.game.base.priority_quote(self.game.assets.quote_dontMove)
        # show some display
        anim = self.game.assets.dmd_ballSaved
        myWait = len(anim.frames) / 12.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 5
        animLayer.opaque = True
        # add listener frames
        animLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_ballSaved)

        self.cancel_delayed("Display")
        self.layer = animLayer
        self.delay(delay=myWait + 0.5,handler=self.clear_layer)

    def closing_song(self,duration):
        attractMusic = 'Yes' == self.game.user_settings['Gameplay (Feature)']['Attract Mode Music']
        if attractMusic:
            print "Playing Closing Song"
            self.delay(delay=duration+1,handler=self.music_on,param=self.game.assets.music_goldmineMultiball)
            # and set a delay to fade it out after 2 minutes
            self.delay("Attract Fade",delay=60,handler=self.game.sound.fadeout_music,param=2000)
            # new line to reset the volume after fade because it may affect new game
            self.delay("Attract Fade",delay=62.5,handler=self.reset_volume)
        # play a flasher lampshow
        self.game.GI_lampctrl.play_show(self.game.assets.lamp_flashers, repeat=False)
        # set a 2 second delay to allow the start button to work again
        print "Setting delay for start button"
        self.delay(delay=duration+2,handler=self.enable_start)

    def enable_start(self):
        print "Game start enabled again"
        self.game.endBusy = False

    def reset_volume(self):
        self.game.sound.set_volume(self.game.volume_to_set)

    def showdown_hit(self,points):
        pointString = str(ep.format_score(points))
        textLine1 = ep.EP_TextLayer(128/2, 2, self.game.assets.font_9px_AZ_outline, "center", opaque=False).set_text("<BAD> <GUY> <SHOT!>",color=ep.ORANGE)
        textLine2 = ep.EP_TextLayer(128/2, 14, self.game.assets.font_12px_az_outline, "center", opaque=False)
        textLine2.composite_op = "blacksrc"
        textLine2.set_text(pointString,blink_frames=8,color=ep.RED)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2])
        combined.composite_op = "blacksrc"
        self.layer = combined
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)

    def ball_added(self):
        textLine = dmd.TextLayer(64, 12, self.game.assets.font_9px_AZ_outline, "center", opaque=False).set_text("<BALL> <ADDED>",blink_frames=8)
        textLine.composite_op = "blacksrc"
        self.layer = textLine
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)

    def ball_save_activated(self):
        textLine1 = dmd.TextLayer(128/2, 2, self.game.assets.font_9px_AZ_outline, "center", opaque=False).set_text("<BALL> <SAVER>")
        textLine2 = ep.EP_TextLayer(128/2, 14, self.game.assets.font_12px_az_outline, "center", opaque=False)
        textLine2.composite_op = "blacksrc"
        textLine2.set_text("ACTIVATED",blink_frames=8,color=ep.GREEN)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2])
        combined.composite_op = "blacksrc"
        self.layer = combined
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)

    def dude_escaped(self,amount):
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_escaped.frames[0])
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
        if self.game.combos in self.game.modes:
            self.statusDisplay = side
            print "STATUS GOES HERE"
            # start the status display
            self.status()
        else:
            pass

    def status_off(self):
        self.statusDisplay = "Off"
        print "STATUS ENDING"
        self.cancel_delayed("Display")
        # clear the layer
        self.layer = None
        # reset the page to 0
        self.page = 0

    def status(self):
        # cancel the delay, in case we got pushed early
        self.cancel_delayed("Display")
        # hide the replay page if replays are disabled
        max_page = 7
        # by bumping up the max page by one if replays are enabled
        if self.game.replays:
            max_page += 1
        # first, tick up the page
        self.page += 1
        # roll back around if we get over the number of pages
        if self.page > max_page:
            self.page = 1
        # then show some junk based on what page we're on
        if self.page == 1:
            textLine1 = ep.EP_TextLayer(128/2, 1, self.game.assets.font_12px_az, "center", opaque=True).set_text("CURRENT",color=ep.YELLOW)
            textLine2 = ep.EP_TextLayer(128/2, 16, self.game.assets.font_12px_az, "center", opaque=False).set_text("STATUS",color=ep.YELLOW)
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
            self.tld("BONUS INFO:", textString2, textString3, color2=ep.ORANGE,color3=ep.ORANGE)
        if self.page == 3:
        # Multiball/Mine information
            locked = self.game.show_tracking('ballsLocked')
            if locked == 1:
                textString2 = str(locked) + " BALL LOCKED"
            else:
                textString2 = str(locked) + " BALLS LOCKED"
            shots = self.game.show_tracking('mineShotsTotal')
            textString3 = str(shots) + " MINE SHOTS TOTAL"
            # stock three line display
            self.tld("MINE STATUS:", textString2, textString3, color2=ep.ORANGE,color3=ep.ORANGE)
        # drunk multiball status
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
            self.tld("BEER MUG:",textString2,textString3, color2=ep.ORANGE,color3=ep.ORANGE)
            # circle back and clear the layer
        # CVA Information & Tumbleweeds
        if self.page == 5:
            left = self.game.show_tracking('tumbleweedShots') - self.game.show_tracking('tumbleweedHits')
            if left <= 0:
                textString2 = "COWBOYS V ALIENS"
                textString3 = "IS LIT"
            else:
                textString2 = str(left) + " MORE WEEDS FOR"
                textString3 = "COWBOYS V ALIENS"
            self.tld("TUMBLEWEEDS:",textString2,textString3,color2=ep.ORANGE,color3=ep.ORANGE)
        # combos information
        if self.page == 6:
            # combos to light badge
            needed = self.game.user_settings['Gameplay (Feature)']['Combos for Star']
            # combos so far
            have = self.game.show_tracking('combos')
            left = needed - have
            if left <= 0:
                textString2 = str(have) + " COMBOS"
                textString3 = "BADGE IS LIT!"
            else:
                textString2 = str(have) + " COMBOS"
                textString3 = str(left) + " MORE FOR BADGE"
            self.tld("COMBO SHOTS:",textString2,textString3, color2=ep.ORANGE,color3=ep.ORANGE)
        # Kills so far
        if self.page == 7:
            # quickdraws so far
            quickdrawKills = self.game.show_tracking('quickdrawsWon')
            # gunfights
            gunfightKills = self.game.show_tracking('gunfightsWon')
            textString2 = "QUICKDRAWS: " + str(quickdrawKills)
            textString3 = "GUNFIGHTS: " + str(gunfightKills)
            self.tld("GUN BATTLE WINS:",textString2,textString3, color2=ep.ORANGE,color3=ep.ORANGE)
        # replay score
        if self.page == 8:
            self.layer = self.replay_score_page()

        self.delay(name="Display",delay=3,handler=self.status)

    def tld(self,textString1,textString2,textString3,color1=ep.WHITE,color2=ep.WHITE,color3=ep.WHITE):
        textLine1 = ep.EP_TextLayer(128/2, 1, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString1,color=color1)
        textLine2 = ep.EP_TextLayer(128/2, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2,color=color2)
        textLine3 = ep.EP_TextLayer(128/2, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString3,color=color3)
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3])
        self.layer = combined

    def shoot_again(self,step=1):
        # shown when starting an extra ball
        if step == 1:
            imageLayer = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_shootAgain.frames[0])
            self.game.base.play_quote(self.game.assets.quote_deepLaugh)
            self.game.sound.play(self.game.assets.sfx_incoming)
            self.layer = imageLayer
            self.delay(delay = 2,handler=self.shoot_again, param=2)
        if step == 2:
            anim = self.game.assets.dmd_shootAgain
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            animLayer.opaque = True
            animLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_lowBoom)
            #animLayer.add_frame_listener(4,self.game.trough.launch_balls,param=1)
            # this flag tells the player intro quote to not play
            self.hush = True
            animLayer.add_frame_listener(4,self.game.ball_starting)
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.shoot_again,param=3)
        if step == 3:
            imageLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_shootAgain.frames[7])
            self.play_ordered_quote(self.game.assets.quote_shootAgain,'shoot_again')
            textLine1 = ep.EP_TextLayer(80,5, self.game.assets.font_9px_az, "center", opaque= False).set_text("SHOOT",color=ep.GREEN)
            textLine2 = ep.EP_TextLayer(80,15, self.game.assets.font_9px_az, "center", opaque= False).set_text("AGAIN",color=ep.GREEN)
            combined = dmd.GroupedLayer(128,32,[imageLayer,textLine1,textLine2])
            self.layer = combined
            self.delay(delay = 1.5,handler=self.clear_layer)

    def train_disabled(self):
        line1 = dmd.TextLayer(128/2, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("TRAIN DISABLED")
        line2 = dmd.TextLayer(128/2, 15, self.game.assets.font_9px_az, "center", opaque=False).set_text("CHECK ENCODER SWITCH")
        self.layer = dmd.GroupedLayer(128,32,[line1,line2])
        self.game.base.repeat_ding(3)
        self.delay(delay=2,handler=self.clear_layer)

    def restarting(self):
        line1 = dmd.TextLayer(128/2, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("NEW")
        line2 = dmd.TextLayer(128/2, 15, self.game.assets.font_9px_az, "center", opaque=False).set_text("GAME")
        self.layer = dmd.GroupedLayer(128,32,[line1,line2])
        self.game.base.repeat_ding(3)
        self.delay(delay=2,handler=self.clear_layer)

    def add_player(self):
        # show the score layer for a second
        self.layer = self.game.score_display.layer
        self.delay(delay = 1,handler=self.clear_layer)

    # this for low priority modes to throw a display over something else that is running
    def cut_in(self,layer,timer):
        # cancel any already running cut in
        self.cancel_delayed("Cut In")
        # set the layer to the one given
        self.layer = layer
        # set the timer for clearing
        self.delay("Cut In",delay=timer,handler=self.clear_layer)

    # this throws a message if the coin door is opened
    def sw_coinDoorClosed_inactive(self,sw):
        line1 = dmd.TextLayer(128/2, 3, self.game.assets.font_7px_az, "center", opaque=True).set_text("COIN DOOR OPEN")
        line2 = dmd.TextLayer(128/2, 15, self.game.assets.font_7px_az, "center", opaque=False).set_text("HIGH VOLTAGE DISABLED")
        self.layer = dmd.GroupedLayer(128,32,[line1,line2])
        self.game.base.repeat_ding(3)
        self.delay(delay=3,handler=self.clear_layer)

    # Jets increased display
    def bumpers_increased(self,value):
        backdrop = dmd.FrameLayer(opaque=True,frame=self.game.assets.dmd_singleCactusBorder.frames[0])
        topLine = dmd.TextLayer(60,1,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JET BUMPERS VALUE")
        increasedLine1 = dmd.TextLayer(60,8,self.game.assets.font_12px_az, "center", opaque=False).set_text("INCREASED")
        increasedLine2 = dmd.TextLayer(60,8,self.game.assets.font_15px_az_outline, "center", opaque=False)
        increasedLine1.composite_op = "blacksrc"
        increasedLine2.composite_op = "blacksrc"
        increasedLine2.set_text("INCREASED")
        pointsLine = dmd.TextLayer(60,18,self.game.assets.font_12px_az_outline,"center",opaque=False)
        pointsLine.composite_op = "blacksrc"
        pointsLine.set_text(str(ep.format_score(value)))
        script = []
        layer1 = dmd.GroupedLayer(128,32,[backdrop,topLine,increasedLine1,pointsLine])
        layer2 = dmd.GroupedLayer(128,32,[backdrop,topLine,pointsLine,increasedLine2])
        script.append({'seconds':0.3,'layer':layer1})
        script.append({'seconds':0.3,'layer':layer2})
        self.game.base.play_quote(self.game.assets.quote_yippie)
        self.layer = dmd.ScriptedLayer(128,32,script)
        self.delay("Display",delay=2,handler=self.clear_layer)

    # mad cow display
    def mad_cow(self,step=1):
        backdrop = ep.EP_AnimatedLayer(self.game.assets.dmd_cows)
        backdrop.hold = False
        backdrop.repeat = True
        backdrop.frame_time = 6
        backdrop.opaque = True
        if step == 1:
            noises = [self.game.assets.sfx_cow1,self.game.assets.sfx_cow2]
            sound = random.choice(noises)
            self.game.sound.play(sound)
            textLine1 = dmd.TextLayer(64,1,self.game.assets.font_12px_az_outline, "center", opaque=False)
            textLine2 = dmd.TextLayer(64,16,self.game.assets.font_12px_az_outline, "center", opaque=False)
            textLine1.composite_op = "blacksrc"
            textLine2.composite_op = "blacksrc"
            textLine1.set_text("MAD",blink_frames=15)
            textLine2.set_text("COW",blink_frames=15)
            combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
            self.layer = combined
            self.delay("Display",delay=1.5,handler=self.mad_cow,param=2)
        elif step == 2:
            textLine1 = dmd.TextLayer(64,9,self.game.assets.font_12px_az_outline, "center",opaque=False)
            textLine1.composite_op = "blacksrc"
            textLine1.set_text(str(ep.format_score(50000)))
            combined = dmd.GroupedLayer(128,32,[backdrop,textLine1])
            self.layer = combined
            self.delay("Display",delay=1.5,handler=self.clear_layer)
        else:
            pass

    # volume controls
    # Outside of the service mode, up/down control audio volume.
    def sw_down_active(self, sw):
        print "Volume Down"
        if self.game.new_service not in self.game.modes:
            # set the volume down one
            volume = self.game.volume_down()
            # save the value
            print "New volume: " + str(volume)
            self.game.user_settings['Sound']['Initial volume']= volume
            self.game.save_settings()
            # if we're not in a game, turn on some music and throw a display
            self.volume_display(volume)
            return True

    def sw_up_active(self, sw):
        print "Volume Up"
        if self.game.new_service not in self.game.modes:
            # set the volume up one
            volume = self.game.volume_up()
            print "New volume: " + str(volume)
            self.game.user_settings['Sound']['Initial volume'] = volume
            self.game.save_settings()
            self.volume_display(volume)
            return True

    def volume_display(self,volume):
        # cancel any previous delay
        self.cancel_delayed("Volume")
        # start a song if one isn't already playing
        if not self.playing and self.game.base not in self.game.modes:
            self.playing = True
            self.game.sound.play_music(self.game.assets.music_shooterLaneGroove,loops=-1)
        # throw some display action
        topLine = dmd.TextLayer(64,3,self.game.assets.font_7px_az, "center", opaque=True)
        string = "VOLUME: " + str(volume)
        topLine.set_text(string)
        volumeLine = dmd.TextLayer(64,13,self.game.assets.font_13px_score, "center", opaque=False)
        volumeString = ""
        while len(volumeString) < volume:
            volumeString += "A"
        while len(volumeString) < 10:
            volumeString += "B"
        volumeString += "C"
        volumeLine.set_text(volumeString)
        self.layer = dmd.GroupedLayer(128,32,[topLine,volumeLine])
        # set a delay to cancel
        self.delay("Volume",delay = 2,handler=self.clear_volume_display)

    def clear_volume_display(self):
        # turn the music off
        if self.game.base not in self.game.modes:
            self.stop_music()
        # turn off the playing flag
        self.playing = False
        # clear the layer
        self.clear_layer()

    def switch_warning(self,switches):
        script = []
        switchCount = len(switches)
        # set up the text layer
        textString = "< CHECK SWITCHES >"
        textLayer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)
        textLayer.composite_op = 'blacksrc'
        script.append({'seconds':1.8,'layer':textLayer})

        # then loop through the bad switches
        for i in range(0,switchCount,1):
            name = switches[i]['switchName']
            count = switches[i]['count']
            textString = "< " + name + " >"
            textLayer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)
            textLayer.composite_op = 'blacksrc'
            script.append({'seconds':1.8,'layer':textLayer})
        display = dmd.ScriptedLayer(128,32,script)
        display.composite_op = "blacksrc"
        self.layer = display

    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        print "ENTERING NEW SERVICE MODE"
        # clear the interrupter layer - just in case
        self.clear_layer()
        # if attract mode is running, stop the lampshow
        if self.game.attract_mode in self.game.modes:
            # kill the lampshow
            self.game.lampctrl.stop_show()
            self.game.attract_mode.unload()
        self.game.lamp_control.disable_all_lamps()
        # stop the music
        self.stop_music()
        # stop the train
        self.game.train.stop()
        # stop the mine
        self.game.mountain.stop()
        # drop the bad guys
        self.game.bad_guys.slay()
        # kill the gunfight pins
        self.game.coils.rightGunFightPost.disable()
        self.game.coils.leftGunFightPost.disable()
        # remove all the active modes
        modequeue_copy = list(self.game.modes)
        for mode in modequeue_copy:
            mode.unload()
            # then add the service mode
        self.game.modes.add(self.game.new_service)
        self.unload()
        return True

    # knocker
    def knock(self,value,realOnly = False):
        if self.game.useKnocker:
            self.game.coils.knocker.pulse(self.knockerStrength)
            print "Fired knocker!"
        else:
            if realOnly:
                pass
            else:
                self.game.sound.play(self.game.assets.sfx_knocker)
        value -= 1
        # if there's more than one, come back
        if value > 0:
            self.delay(delay=0.5,handler=self.knock,param=value)


    # replay score display
    def replay_score_display(self):
        self.layer = self.replay_score_page()
        self.delay(delay=1.5,handler=self.clear_layer)

    def replay_score_page(self):
        replay_text = ep.format_score(self.game.user_settings['Machine (Standard)']['Replay Score'])
        score_text = ep.format_score(self.game.current_player().score)
        textLine1 = ep.EP_TextLayer(64, 1, self.game.assets.font_5px_bold_AZ, "center", opaque=True).set_text("REPLAY SCORE:",color=ep.ORANGE)
        textLine2 = ep.EP_TextLayer(64, 7, self.game.assets.font_7px_az, "center", opaque=False).set_text(replay_text,color=ep.GREEN)
        textLine3 = ep.EP_TextLayer(64, 17, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("YOUR SCORE:",color=ep.ORANGE)
        textLine4 = ep.EP_TextLayer(64, 23, self.game.assets.font_7px_az, "center", opaque=False).set_text(score_text,blink_frames=8,color=ep.RED)
        layer = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,textLine4])
        return layer

    def replay_award_display(self):
        anim = self.game.assets.dmd_fireworks
        myWait = (len(anim.frames) / 10.0) + 1
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 6
        # firework sounds keyframed
        animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_fireworks1)
        animLayer.add_frame_listener(17,self.game.sound.play,param=self.game.assets.sfx_fireworks2)
        animLayer.add_frame_listener(21,self.game.sound.play,param=self.game.assets.sfx_fireworks3)
        animLayer.add_frame_listener(24,self.game.sound.play,param=self.game.assets.quote_replay)
        animLayer.composite_op = "blacksrc"
        textLine1 = "REPLAY AWARD"
        textLayer1 = ep.EP_TextLayer(58, 5, self.game.assets.font_10px_AZ, "center", opaque=True).set_text(textLine1,color=ep.BLUE)
        textLayer1.composite_op = "blacksrc"
        textLine2 = self.game.user_settings['Machine (Standard)']['Replay Award']
        if textLine2.upper == "EXTRA BALL" and self.game.max_extra_balls_reached():
            textLine2 = ep.format_score(500000)
        textLayer2 = dmd.TextLayer(58, 18, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(textLine2.upper())
        textLayer2.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,animLayer])
        self.layer = combined
        self.delay(delay=myWait,handler=self.game.sound.play,param=self.game.assets.sfx_cheers)
        self.delay("Display", delay=myWait,handler=self.clear_layer)

    def tournament_start_display(self):
        textLine1 = ep.EP_TextLayer(64, 1, self.game.assets.font_7px_az, "center", opaque=True).set_text("TOURNAMENT MODE",color=ep.RED)
        textLine2 = ep.EP_TextLayer(64, 11, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("PRESS START",blink_frames=8,color=ep.YELLOW)
        textLine3 = ep.EP_TextLayer(64, 17, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("NOW FOR",color=ep.YELLOW)
        textLine4 = ep.EP_TextLayer(64, 23, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("TOURNAMENT PLAY",color=ep.YELLOW)
        self.tournamentTimerLayer = ep.EP_TextLayer(122,8,self.game.assets.font_17px_score, "right",opaque=False).set_text("9",color=ep.GREEN)
        self.tournamentTimerLayer2 = ep.EP_TextLayer(6,8,self.game.assets.font_17px_score, "left",opaque=False).set_text("9",color=ep.GREEN)
        self.layer = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,textLine4,self.tournamentTimerLayer,self.tournamentTimerLayer2])

    def broadcast(self,layer,time):
        # take a layer sent in and show it for x seconds
        self.cancel_delayed("Display")
        self.layer = layer
        self.delay("Display",delay = time,handler = self.clear_layer)
