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
##  ____  _             _        ____             _
## | __ )(_) ___  _ __ (_) ___  | __ )  __ _ _ __| |_
## |  _ \| |/ _ \| '_ \| |/ __| |  _ \ / _` | '__| __|
## | |_) | | (_) | | | | | (__  | |_) | (_| | |  | |_
## |____/|_|\___/|_| |_|_|\___| |____/ \__,_|_|   \__|
##

from procgame import dmd,game
import ep
import random

class BionicBart(ep.EP_Mode):
    """Bionic Bart code """
    def __init__(self,game,priority):
        super(BionicBart, self).__init__(game,priority)
        self.myID = "Bionic Bart"
        self.hitsToDefeat = self.game.user_settings['Gameplay (Feature)']['Shots to defeat Bionic Bart']
        self.shotModes = [self.game.left_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_loop,self.game.right_ramp,self.game.saloon]
        self.banners = [self.game.assets.dmd_bamBanner,
                        self.game.assets.dmd_biffBanner,
                        self.game.assets.dmd_ouchBanner,
                        self.game.assets.dmd_powBanner,
                        self.game.assets.dmd_whamBanner,
                        self.game.assets.dmd_zoinkBanner]
        self.ballSave = "Enabled" == self.game.user_settings['Gameplay (Feature)']['Bionic Bart Ball Save']
        self.saveDuration = self.game.user_settings['Gameplay (Feature)']['Bionic Bart Ball Save Timer']
        self.won = False

    def ball_drained(self):
        # if we lose all the balls the battle is lost
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('bionicStatus') == "RUNNING":
            self.cancel_delayed("Display")
            self.game.base.busy = True
            self.game.base.queued += 1
            #print "BALL DRAINED - BIONIC IS ENDING"
            self.bionic_failed()

    def mode_started(self):
        #print "Starting bionic bart battle"
        # audit
        self.game.game_data['Feature']['Bionic Bart Started'] += 1
        # set the stack level
        self.game.stack_level(6,True)
        # if there's a quickdraw running - kill that
        if self.game.quickdraw.running:
            self.game.quickdraw.lost(self.game.quickdraw.target)
        # set up the standard display stuff
        script = []
        idleLayer1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[0])
        script.append({'layer':idleLayer1,'seconds':11})
        idleLayer2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[5])
        script.append({'layer':idleLayer2,'seconds':0.1})
        idleLayer3 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[6])
        script.append({'layer':idleLayer3,'seconds':0.1})
        script.append({'layer':idleLayer2,'seconds':0.1})
        self.idleLayer = dmd.ScriptedLayer(128,32,script)
        script = []
        talkLayer1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[1])
        script.append({'layer':talkLayer1,'seconds':0.16})
        talkLayer2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[2])
        script.append({'layer':talkLayer2,'seconds':0.16})
        self.talkingLayer = dmd.ScriptedLayer(128,32,script)
        script = []
        hurtLayer1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[3])
        script.append({'layer':hurtLayer1,'seconds':0.16})
        hurtLayer2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bionicCombo.frames[4])
        script.append({'layer':hurtLayer2,'seconds':0.16})
        self.whineLayer = dmd.ScriptedLayer(128,32,script)
        self.title = dmd.TextLayer(46, 3, self.game.assets.font_15px_bionic, "center", opaque=False).set_text("BIONIC BART")
        self.title2 = ep.EP_TextLayer(46,20, self.game.assets.font_6px_az, "center", opaque=False).set_text("CHALLENGES YOU!",color=ep.RED)
        self.title2.composite_op = "blacksrc"
        # bart hit layer
        anim = self.game.assets.dmd_bionicHit
        self.stunnedLayer = ep.EP_AnimatedLayer(anim)
        self.stunnedLayer.hold=False
        self.stunnedLayer.repeat=True
        self.stunnedLayer.frame_time = 6
        self.defeatLamps = 0

        # intialize some layers
        self.set_bart_layer(self.idleLayer)
        self.set_action_line()
        self.set_status_line()

        self.loaded = False
        self.shots = 0
        self.shotsToLoad = 2
        self.hits = 0
        self.hitValue = 500000
        self.activeShots = []
        self.won = False

    # switches
    def sw_leftLoopTop_active(self,sw):
        # pulse the coil to open the gate
        self.game.coils.rightLoopGate.pulse(240)
        self.process_shot(0)
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot(1)
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot(2)
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            # pulse the coil to open the gate
            self.game.coils.leftLoopGate.pulse(240)
            self.process_shot(3)
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4)
        return game.SwitchStop

    def sw_saloonPopper_active_for_300ms(self,sw):
        self.cancel_delayed("Display")
        if self.loaded:
            self.hit()
        else:
            self.miss()
        return game.SwitchStop

    # jet bumpers exit - trapping for bionic bart
    def sw_jetBumpersExit_active(self,sw):
        self.game.score(2530)
        return game.SwitchStop

    # mine - trapping for bionic bart
    def sw_minePopper_active_for_390ms(self,sw):
        self.game.score(2530)
        self.miss()
        # kick the ball
        self.game.mountain.eject()
        return game.SwitchStop

    def process_shot(self,shot):
        self.cancel_delayed("Display")
        self.game.squelch_music()
        # if the shot is active, register it as such
        if shot in self.activeShots:
            #print "Bionic Bart active shot hit " + str(shot)
            if self.loaded == False:
                self.shots += 1
                # play a lamp show based on shot number
                # left loop
                if shot == 0:
                # play a lamp show
                    show = self.game.assets.lamp_leftToRight
                # left ramp
                elif shot == 1:
                    show = self.game.assets.lamp_rightToLeft
                # center ramp
                elif shot == 2:
                    show = self.game.assets.lamp_bottomToTop
                # right loop
                elif shot == 3:
                    show = self.game.assets.lamp_rightToLeft
                # right ramp
                else:
                    show = self.game.assets.lamp_leftToRight

                self.game.lampctrl.play_show(show, repeat=False,callback=self.lamp_update)

               # if we're up to the required shots, load the weapon
                if self.shots >= self.shotsToLoad:
                    # score points for loaded
                    self.game.score(53370)
                    self.load_weapon()
                # otherwise tick up the shots and update the status
                else:
                    # score points for loading
                    self.game.score(25730)
                    self.loading()
            # if we're already loaded, then what? - this might be moot now
            else:
                # score points for already loaded
                self.game.score(2530)
                self.weapon_loaded(prompt=True)
        # if it's not an active shot, it's a miss
        else:
            self.game.score(2530)
            # but if the gun is loaded, urge player to shoot the bad guy
            if self.loaded:
                #print "WEAPON IS LOADED THIS IS A MISS"
                self.weapon_loaded(prompt=True)
            else:
                #print "WEAPON IS NOT LOADED THIS IS A MISS"
                self.miss()

    def activate_shots(self,amount):
        #print "ACTIVATING SHOTS - VALUE: " + str(amount)
        # pick the active shot
        if amount == 0:
            self.activeShots = []
        if amount == 1:
            self.activeShots = [2]
        if amount == 2:
            self.activeShots = [0,3]
        if amount == 3:
            self.activeShots = [1,4]
        # update the lamps
        self.lamp_update()

    def start_bionic(self):
        # kill the music
        self.stop_music()
        # set bionic to running
        self.game.set_tracking('bionicStatus',"RUNNING")
        # kick off the intro
        self.intro(1)

    def intro(self,step):
        # initial display/sound
        # step 1
        if step == 1:
            # kill the lights!
            self.game.lamp_control.disable_all_lamps()
            # kill the GI
            self.game.gi_control("OFF")
            # play the 'deal with this' quote
            duration = self.game.base.play_quote(self.game.assets.quote_bionicIntroQuote)
            self.delay(delay=duration,handler=self.intro,param=2)
        if step == 2:
        # load up the lightning
            anim = self.game.assets.dmd_cloudLightning
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            # keyframe sounds
            animLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_lightning1)
            animLayer.add_frame_listener(2,self.game.lightning,param="top")
            animLayer.add_frame_listener(3,self.game.lightning,param="left")
            animLayer.add_frame_listener(3,self.game.lightning,param="right")
            animLayer.add_frame_listener(6,self.game.sound.play,param=self.game.assets.sfx_lightning2)
            animLayer.add_frame_listener(6,self.game.lightning,param="top")
            animLayer.add_frame_listener(7,self.game.lightning,param="left")
            animLayer.add_frame_listener(10,self.game.sound.play,param=self.game.assets.sfx_lightningRumble)
            animLayer.add_frame_listener(10,self.game.lightning,param="top")
            animLayer.add_frame_listener(11,self.game.lightning,param="right")
            # turn it on
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.intro,param=3)
        if step == 3:
            # turn the GI back on
            self.game.gi_control("ON")
            combined = dmd.GroupedLayer(128,32,[self.idleLayer,self.title,self.title2])
            self.layer = combined
            self.delay(delay=1,handler=self.intro,param=4)
        if step == 4:
            # play the intro quote
            duration = self.game.base.play_quote(self.game.assets.quote_introBionicBart)
            # show the talking layer
            combined = dmd.GroupedLayer(128,32,[self.talkingLayer,self.title,self.title2])
            self.layer = combined
            # loop back for step 3
            self.delay(delay=duration,handler=self.intro,param=5)
        if step == 5:
            combined = dmd.GroupedLayer(128,32,[self.idleLayer,self.title,self.title2])
            self.layer = combined
            duration = self.game.sound.play(self.game.assets.music_bionicBartIntro)
            # loop back to start the music
            self.delay(delay = duration, handler=self.intro,param=6)
        if step == 6:
            # start the music
            self.music_on(self.game.assets.music_bionicBart)
            self.update_display()
            # set the active shots
            self.activate_shots(2)
            # update the lamps to turn the rest back on
            self.lamp_update()
            # kick the ball out
            self.game.saloon.kick()
            # start a ball save if configured
            if self.ballSave:
                self.game.trough.start_ball_save(num_balls_to_save=1, time=self.saveDuration, now=True, allow_multiple_saves=False)

    def update_display(self):
        self.cancel_delayed("Display")
        # set up the display during multiball
        # whateve the current bart layer is, default is idle
        backdrop = self.bartLayer
        # title line
        titleLine = ep.EP_TextLayer(46, -1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("BIONIC BART",color=ep.GREY)
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = ep.EP_TextLayer(46, 5, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4,color=ep.YELLOW)
        scoreLine.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,scoreLine,self.actionLine,self.statusLine])
        self.layer = combined
        # loop back in .2 to update
        self.delay(name="Display",delay=0.2,handler=self.update_display)

    def set_bart_layer(self,layer):
        self.bartLayer = layer

    def set_action_line(self,string="LOAD WEAPON"):
        self.actionLine = ep.EP_TextLayer(46, 16, self.game.assets.font_7px_az, "center", opaque=False).set_text(string,color=ep.RED)
        self.actionLine.composite_op = "blacksrc"

    def set_status_line(self,amount=2,style="LOAD"):
        if amount > 1:
            shotWord = "SHOTS"
            hitWord = "HITS"
        else:
            shotWord = "SHOT"
            hitWord = "HIT"
        if style == "LOAD":
            theWord = shotWord
            theEnd = "LOAD"
        else:
            theWord = hitWord
            theEnd = "DEFEAT"
        if style == "HIT":
            string = "NICE SHOT!"
        else:
            string = str(amount) + " " + theWord + " TO " + theEnd
        self.statusLine = ep.EP_TextLayer(46, 24, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(string,color=ep.GREEN)

    def load_weapon(self):
        amount = self.hitsToDefeat - self.hits
        self.set_status_line(amount, "SHOOT")
        self.set_action_line("HIT BIONIC BART")
        # set the flag
        self.loaded = True
        # update lamps
        self.lamp_update()
        # next round takes more hits - max at 3 for now
        if self.shotsToLoad < 3:
            self.shotsToLoad += 1
        anim = self.game.assets.dmd_bionicGunClose
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        self.layer = animLayer
        self.game.sound.play(self.game.assets.sfx_gunCock)
        # kill the active shots and activate the bart lamp
        self.activate_shots(0)
        self.delay(name="Display",delay=0.6,handler=self.weapon_loaded)

    def weapon_loaded(self,prompt=False):
        # show some display
        line1 = dmd.TextLayer(64, 3, self.game.assets.font_15px_bionic, "center", opaque=True).set_text("LOADED")
        line2 = ep.EP_TextLayer(64, 22, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SHOOT BIONIC BART",color=ep.YELLOW)
        combined = dmd.GroupedLayer(128,32,[line1,line2])
        self.layer = combined
        if prompt:
            duration = self.game.base.play_quote(self.game.assets.quote_bionicUrge)
        else:
            duration = self.game.sound.play(self.game.assets.sfx_orchestraSpike)
        self.delay(name="Display",delay=1.5,handler=self.update_display)
        if duration < 1.5:
            duration = 1.5
        self.delay(delay=duration,handler=self.game.restore_music)

    def loading(self):
        amount = self.shotsToLoad - self.shots
        self.set_status_line(amount,"LOAD")
        if amount == 1:
            anim = self.game.assets.dmd_bionicGunLoad
            string = "NEW AMMO"
            sound = self.game.assets.sfx_orchestraSet
        elif amount == 2:
            anim = self.game.assets.dmd_bionicGunUnload
            string = "UNLOADED"
            sound = self.game.assets.sfx_orchestraBump2
        else:
            anim = self.game.assets.dmd_bionicGunOpen
            string = "GUN OPEN"
            sound = self.game.assets.sfx_orchestraBump1
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        textLine = dmd.TextLayer(127,1,self.game.assets.font_15px_bionic,"right", opaque=False).set_text(string)
        textLine.composite_op = "blacksrc"
        string = "<" + str(amount) + " MORE>"
        textLine2 = ep.EP_TextLayer(127,18,self.game.assets.font_6px_az_inverse,"right",opaque=False).set_text(string,color=ep.YELLOW)
        combined = dmd.GroupedLayer(128,32,[animLayer,textLine,textLine2])
        self.layer = combined
        self.game.sound.play(sound)
        # activate the current shots
        self.activate_shots(amount)
        self.delay(name="Display",delay=1.5,handler=self.update_display)
        self.delay(delay=1.5,handler=self.game.restore_music)

    def hit(self,step=1):
        #print "Hitting bionic bart"
        if step == 1:
            # audit
            self.game.game_data['Feature']['Bionic Bart Hits'] += 1
            # turn off loaded and the lights
            self.loaded = False
            self.lamp_update()
            anim = self.game.assets.dmd_burstWipe
            myWait = len(anim.frames) / 14.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 4
            # hit the knocker
            self.game.interrupter.knock(1,realOnly=True)
            self.game.sound.play(self.game.assets.sfx_explosion11)
            self.layer = animLayer
            # move the hat and bart
            self.game.bart.animate(3)
            # tick up the hits
            self.hits +=1
            if self.hits >= self.hitsToDefeat:
                self.bionic_defeated()
            else:
                # a flourish lampshow
                self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.lamp_update)
                self.delay(delay=myWait,handler=self.hit,param=2)
        if step == 2:
            # pick a random banner to use
            banner = random.choice(self.banners)
            # set up the banner layer
            bannerLayer = dmd.FrameLayer(opaque=False, frame=banner.frames[0])
            bannerLayer.composite_op = "blacksrc"
            fadeTo = dmd.GroupedLayer(128,32,[self.stunnedLayer,bannerLayer])
            self.game.sound.play(self.game.assets.sfx_hitBionicBart)
            transition = ep.EP_Transition(self,self.layer,fadeTo,ep.EP_Transition.TYPE_CROSSFADE)
            self.delay(delay=0.8,handler=self.hit,param=3)
        if step == 3:
            self.set_bart_layer(self.stunnedLayer)
            self.game.score(self.hitValue,bonus=True)
            self.set_action_line(str(ep.format_score(self.hitValue)))
            self.set_status_line(style="HIT")
            # increase the hit value for next time
            self.hitValue += 250000
            self.update_display()
            self.delay(delay=0.8,handler=self.hit,param=4)
        if step == 4:
            self.game.squelch_music()
            self.set_bart_layer(self.whineLayer)
            self.flash()
            self.update_display()
            duration = self.game.base.play_quote(self.game.assets.quote_hitBionicBart)
            self.delay(delay=duration,handler=self.hit,param=5)
        if step == 5:
            self.cancel_delayed("Flashing")
            self.game.restore_music()
            self.set_bart_layer(self.idleLayer)
            self.shots = 0
            self.set_action_line()
            self.set_status_line(self.shotsToLoad)
            self.update_display()
            # activate the current shots
            self.activate_shots(self.shotsToLoad - self.shots)
            # kick the ball
            #print "Bionic Hit Saloon Kick"
            self.game.saloon.kick()
            # start a ball save if configured
            if self.ballSave:
                self.game.trough.start_ball_save(num_balls_to_save=1, time=self.saveDuration, now=True, allow_multiple_saves=False)

    def miss(self,step=1):
        if step == 1:
            self.set_bart_layer(self.talkingLayer)
            self.update_display()
            duration = self.game.base.play_quote(self.game.assets.quote_tauntBionicBart)
            self.delay(delay=duration,handler=self.miss,param=2)
            self.flash()
        if step == 2:
            self.cancel_delayed("Flashing")
            self.set_bart_layer(self.idleLayer)
            self.update_display()
            self.game.restore_music()
            self.game.saloon.kick()

    def flash(self):
        self.game.coils.saloonFlasher.pulse(20)
        self.delay(name="Flashing",delay=0.2,handler=self.flash)

    def bionic_defeated(self,step=1):
        # VICTOLY!
        if step == 1:
            # audit
            self.game.game_data['Feature']['Bionic Bart Kills'] += 1
            self.won = True
            # stop the music
            self.stop_music()
            # load up the defeated animation
            anim = self.game.assets.dmd_bionicDeath
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=False
            animLayer.repeat=True
            animLayer.frame_time = 6
            fadeTo = animLayer
            transition = ep.EP_Transition(self,self.layer,fadeTo,ep.EP_Transition.TYPE_CROSSFADE)
            # run a lamp set
            self.defeat_lamps()
            duration = self.game.sound.play(self.game.assets.sfx_hitBionicBart)
            self.delay(delay=duration,handler=self.bionic_defeated,param=2)
        if step == 2:
            # play the beeping noise
            duration = self.game.sound.play(self.game.assets.sfx_dieBionicBart)
            self.delay(delay=duration,handler=self.bionic_defeated,param=3)
        if step == 3:
            # load a black layer to cover the score
          #  blank = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'blank.dmd').frames[0])
          #  # play the death quote over the whine bot
          #  self.whineLayer.set_target_position(-43,0)
            self.flash()
          #  combined = dmd.GroupedLayer(128,32,[blank,self.whineLayer])
            # load up the defeated animation
            anim = self.game.assets.dmd_bionicDeathTalking
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=False
            animLayer.repeat=True
            animLayer.frame_time = 6

            self.layer = animLayer
            # play the quote
            duration = self.game.base.play_quote(self.game.assets.quote_defeatBionicBart)
            self.delay(delay=duration,handler=self.bionic_defeated,param=4)
        if step == 4:
            self.cancel_delayed("Flashing")
            # this is the part where we blow up
            anim = self.game.assets.dmd_bionicExplode
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            myWait = len(anim.frames) / 10.0
            self.layer = animLayer
            # play the explosion
            self.game.sound.play(self.game.assets.sfx_heavyExplosion)
            self.delay(delay=myWait,handler=self.bionic_defeated,param=5)
        if step == 5:
            # reset the whine layer target in case it comes back up in this game
            self.whineLayer.set_target_position(0,0)
            # then do the text display
            line1 = dmd.TextLayer(64, 3, self.game.assets.font_15px_bionic, "center", opaque=True).set_text("DEFEATED!")
            scoreString = str(ep.format_score(5000000)) + " POINTS"
            line2 = ep.EP_TextLayer(64, 22, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8,color=ep.ORANGE)
            combined = dmd.GroupedLayer(128,32,[line1,line2])
            self.layer = combined

            # score points
            self.game.score(5000000)
            # light high noon
            self.game.badge.light_high_noon()

            self.leader_final_quote("win")

    def defeat_lamps(self):
        if self.defeatLamps <= 2:
        # a flourish lampshow
            self.defeatLamps +=1
            self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.defeat_lamps)
            return

        else:
        # a flourish lampshow
            self.game.gi_control("OFF")
            self.game.lampctrl.play_show(self.game.assets.lamp_topToBottom, repeat=False,callback=self.lamp_update)


    def bionic_failed(self):
        # Lose the balls during a bionic fight and you lose
        # show some display
        line1 = dmd.TextLayer(64, 3, self.game.assets.font_15px_bionic, "center", opaque=True).set_text("FAILED")
        line2 = dmd.TextLayer(64, 22, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("BIONIC BART ESCAPED!")
        combined = dmd.GroupedLayer(128,32,[line1,line2])
        self.layer = combined

        # play the fail quote
        duration = self.game.base.play_quote(self.game.assets.quote_failBionicBart)
        # reset all the star status
        self.game.badge.reset()

        self.delay(delay=duration,handler=self.leader_final_quote,param="fail")

    def tilted(self):
        # reset all the star status
        self.game.badge.reset()
        # set bionic
        self.game.set_tracking('bionicStatus',"OPEN")
        self.unload()

    def leader_final_quote(self,condition):
        if condition == "win":
            duration = self.game.sound.play(self.game.assets.sfx_cheers)
            duration2 = self.game.base.play_quote(self.game.assets.quote_leaderWinBionic)
            if duration2 > duration:
                duration = duration2
            self.delay(delay=duration,handler=self.high_noon_lit)
        elif condition == "fail":
            duration = self.game.base.play_quote(self.game.assets.quote_leaderFailBionic)
            self.delay(delay=duration,handler=self.finish_up)

    def high_noon_lit(self):
        line1 = dmd.TextLayer(64, 3, self.game.assets.font_15px_bionic, "center", opaque=True).set_text("HIGH NOON LIT")
        line2 = ep.EP_TextLayer(64, 22, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SHOOT THE MINE!",color=ep.ORANGE)
        combined = dmd.GroupedLayer(128,32,[line1,line2])
        self.layer = combined
        self.repeat_ding(3)
        self.delay(delay=1.2,handler=self.finish_up)

    def repeat_ding(self,times):
        self.game.sound.play(self.game.assets.sfx_bountyBell)
        self.game.coils.mineFlasher.pulse(30)
        times -= 1
        if times > 0:
            self.delay(delay=0.4,handler=self.repeat_ding,param=times)


    def finish_up(self):
        # turn the gi back on
        self.game.gi_control("ON")
        # as is tradition
        self.layer = None
        # clear the stack level
        self.game.stack_level(6,False)
        # turn the main music back on
        if self.game.trough.num_balls_in_play != 0:
            self.music_on(self.game.assets.music_mainTheme)
        if self.won:
            # set bart flag to dead
            self.game.set_tracking('bionicStatus', "DEAD")
        else:
            # set bionic
            self.game.set_tracking('bionicStatus',"OPEN")

        # Turn the lights back on
        self.lamp_update()
        # kick the ball if it's held
        #print "Bionic Finish Up Saloon Kick"
        self.game.saloon.kick()
        # unset the base busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload the mode
        self.unload()
