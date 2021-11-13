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
## The Cirqus Voltaire Tribute
##
## CV TRIBUTE MODE IS NOT FINISHED AT THIS TIME

from procgame import dmd,game
import ep
import random

class CV_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(CV_Tribute, self).__init__(game,priority)
        self.myID = "CV Tribute"
        # for timer halting in saloon/jets
        self.halted = False
        self.running = False
        self.hitsToWin = 4

        script = []
        # set up the pause text layer
        textString = "< RINGMASTER PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.GREEN)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"

        self.titleLine = ep.EP_TextLayer(64,1,self.game.assets.font_5px_bold_AZ_outline, "center", opaque=False)
        self.titleLine.composite_op = "blacksrc"
        self.titleLine.set_text("HIT THE RINGMASTER",color=ep.MAGENTA)
        self.leftTimerLine = ep.EP_TextLayer(0,1,self.game.assets.font_5px_bold_AZ_outline, "left",False)
        self.leftTimerLine.composite_op = "blacksrc"
        self.rightTimerLine = ep.EP_TextLayer(128,1,self.game.assets.font_5px_bold_AZ_outline,"right",False)
        self.rightTimerLine.composite_op = "blacksrc"
        self.scoreLine = ep.EP_TextLayer(64,7,self.game.assets.font_12px_az_outline,"center",opaque=False)
        self.scoreLine.composite_op = "blacksrc"
        self.infoLine = ep.EP_TextLayer(64,23,self.game.assets.font_7px_az,"center", opaque=False)
        self.infoLine.set_text("{{{{",color=ep.MAGENTA)
        self.infoLine.composite_op = "blacksrc"
        self.hitLayers = [self.game.assets.dmd_cvBurst1,self.game.assets.dmd_cvBurst2,self.game.assets.dmd_cvBurst3]

    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add',self.myID)
        # unload the launcher
        self.game.tribute_launcher.unload()
        # first hit is 250, but it adds the bump first in the routine
        self.value = 175000
        self.bump = 75000
        self.running = True
        self.halted = False
        # overall mode timer
        self.modeTimer = 20
        # total ringmaster hits
        self.hitsSoFar = 0
        # score for the mode
        self.totalPoints = 0
        # create the hypno backdrop level
        anim = self.game.assets.dmd_cvHypno
        self.hypnoLayer = ep.EP_AnimatedLayer(anim)
        self.hypnoLayer.hold = False
        self.hypnoLayer.frame_time = 6
        self.hypnoLayer.repeat = True
        self.hypnoLayer.opaque = True
        self.won = False
        self.switchHit = False

        self.intro()

    def ball_drained(self):
        # if we get to zero balls while running, finish
        if self.game.trough.num_balls_in_play == 0 and self.running:
            self.done()

    def halt_test(self):
        if not self.halted:
            self.halt_ringmaster()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # halt switches
    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        self.halt_test()

    def sw_rightBonusLane_active(self,sw):
        self.halt_test()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        self.halt_test()

    def sw_rightJetBumper_active(self,sw):
        self.halt_test()

    def sw_bottomJetBumper_active(self,sw):
        self.halt_test()

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_350ms(self,sw):
        #print "Ringmaster Mine Popper Register"
        self.halt_test()

    def sw_leftLoopBottom_active(self,sw):
        self.atmos("loop")
        return game.SwitchStop

    def sw_rightLoopBottom_active(self,sw):
        self.atmos("loop")
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        # pulse the right gate
        self.game.coils.rightLoopGate.pulse(240)
        return game.SwitchStop

    def sw_rightLoopTop_active(self,sw):
        # pulse the left gate
        self.game.coils.leftLoopGate.pulse(240)
        return game.SwitchStop

    def sw_saloonGate_active(self,sw):
        if not self.switchHit:
            self.switchHit = True
            self.hit_ringmaster()
            self.delay("Reset Switch", delay=2,handler=self.enable_switch)
        return game.SwitchStop

    def enable_switch(self):
        self.switchHit = False

    def sw_saloonBart_active(self,sw):
        return game.SwitchStop

    def sw_saloonPopper_active_for_300ms(self,sw):
        #print "Ringmaster Saloon Popper Register"
        # if we haven't one yet, kick that mother
        if not self.hitsSoFar >= self.hitsToWin:
            self.kick_saloon()
        # if we have won, just sit tight and do nothing
        else:
            pass
        return game.SwitchStop

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.taunt_player()
            self.delay("Resume",delay=1,handler=self.resume_ringmaster)

    def taunt_player(self):
            self.game.bart.animate(2)
            self.game.base.play_quote(self.game.assets.quote_cvTaunt)
            self.tauntTimer = 10

    def taunt_timer(self):
            self.tauntTimer -= 1
            if self.tauntTimer <= 0:
                self.taunt_player()
            self.delay("Taunt Timer", delay=1, handler=self.taunt_timer)

    def intro(self,step=1):
        if step == 1:
            self.stop_music()
            anim = self.game.assets.dmd_cvIntro1
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = True
            animLayer.composite_op = "blacksrc"

            animLayer.add_frame_listener(31,self.stop_music)

            self.layer = animLayer
            self.game.sound.play(self.game.assets.sfx_cvStartRiff)
            self.delay(delay = 0.5, handler=self.music_on,param=self.game.assets.music_cvGear)
            self.delay(delay = 0.5,handler=self.game.sound.play,param=self.game.assets.quote_cvIntroLead)
            self.delay(delay = 0.5,handler=self.game.bart.animate,param=2)
            self.delay(delay = 2.75, handler = self.intro,param=2)

        if step == 2:
            myDelay = self.game.sound.play(self.game.assets.quote_cvIntro)
            self.game.bart.animate(2)
            self.delay(delay = myDelay, handler=self.intro,param=3)

        if step == 3:
            # start the score updater
            self.score_update()
            anim = self.game.assets.dmd_cvIntro2
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"
            # generate the backdrop
            mainLayer = self.display_main()
            self.layer = dmd.GroupedLayer(128,32,[mainLayer,animLayer])
            myDelay = self.game.sound.play(self.game.assets.sfx_cvMusicLead)
            self.delay(delay = myDelay, handler=self.music_on,param=self.game.assets.music_ringmaster)
            self.delay(delay = myWait,handler=self.intro,param=4)

        if step == 4:
            self.layer = self.display_main()
            self.get_going()

    def get_going(self):
        self.game.ball_search.enable()
        #print "RELEASE THE BALL FOR TRIBUTE"
        # release the ball
        if self.game.tribute_launcher.shot == 3:
            #print "TRIBUTE MINE EJECT"
            self.game.mountain.eject()
        else:
            #print "TRIBUTE POST DROP"
            self.game.coils.leftGunFightPost.disable()
        # start the timer
        self.modeTimer += 1
        self.time_ringmaster()
        self.tauntTimer = 10
        self.taunt_timer()
        # start the display
#        self.display_main()

    def display_main(self):
        self.cancel_delayed("Display")

        mainLayer = dmd.GroupedLayer(128,32,[self.hypnoLayer,self.leftTimerLine,self.rightTimerLine,self.titleLine,self.scoreLine,self.infoLine])
        return mainLayer

    def post_hit(self):
        # restart the timer and reset
        self.modeTimer = 21
        self.time_ringmaster()
        self.titleLine.set_text("HIT THE RINGMASTER",color=ep.MAGENTA)
        # check to see if we're done
        if self.hitsSoFar >= self.hitsToWin:
            self.finish_ringmaster()
        else:
            self.layer = self.display_main()

    def hit_ringmaster(self):
        #print "Hit Ringmaster"
        # stop the timer
        self.cancel_delayed("Mode Timer")
        # stop the movement for now
        self.cancel_delayed("Move Timer")
        # on a hit, increase the value, and add the new value to the total and display the hit
        self.value += self.bump
        # score the points
        self.game.score(self.value)
        self.totalPoints += self.value
        # register the hit
        self.hitsSoFar += 1
        remain = self.hitsToWin - self.hitsSoFar
        if remain <= 0 and not self.won:
            # flag so this only happens once
            self.won = True
            # end this sucker
            self.infoLine.set_text("}}}}",color=ep.MAGENTA)
            self.finish_ringmaster()
        elif remain == 1:
            self.infoLine.set_text("}}}{",color=ep.MAGENTA)
        elif remain == 2:
            self.infoLine.set_text("}}{{",color=ep.MAGENTA)
        elif remain == 3:
            self.infoLine.set_text("}{{{",color=ep.MAGENTA)
        else:
            pass
        self.titleLine.set_text(ep.format_score(self.value),color=ep.CYAN)

        self.modeTimer = 21
        # display the hit
        anim = random.choice(self.hitLayers)
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 6
        animLayer.repeat = False
        animLayer.opaque = False
        animLayer.composite_op = "blacksrc"
        mainLayer = self.display_main()
        self.layer = dmd.GroupedLayer(128,32,[mainLayer,animLayer])
        # play the hit sound
        myWait = self.game.sound.play(self.game.assets.sfx_cvHit)
        self.delay(delay=0.5,handler=self.game.base.priority_quote,param=self.game.assets.quote_cvHit)
        self.delay(delay=0.5,handler=self.game.bart.animate,param=2)
        self.delay(delay=1,handler=self.post_hit)

    def time_ringmaster(self):
        self.modeTimer -= 1
        # if we get to zero, end the mode
        if self.modeTimer < 0:
            self.game.sound.play(self.game.assets.sfx_cvMonkey)
            self.done()
        # otherwise update the timer layers and loop back
        else:
            if self.modeTimer > 9:
                color = ep.GREEN
            elif self.modeTimer > 4:
                color = ep.YELLOW
            else:
                color = ep.RED
            self.leftTimerLine.set_text(str(self.modeTimer),color=color)
            self.rightTimerLine.set_text(str(self.modeTimer),color=color)
            self.delay("Mode Timer",delay=1,handler=self.time_ringmaster)

    def score_update(self):
        # update the score line total every half second
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.scoreLine.set_text(scoreString)
        self.delay("Score Update",delay=0.5,handler=self.score_update)

    def halt_ringmaster(self):
        if self.modeTimer <= 0:
            return
        #print "HALTING Ringmaster IN BUMPERS/MINE"
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # do the halted delay
        self.layer = self.pauseView
        # set the flag
        self.halted = True

    def resume_ringmaster(self):
        # turn the timer back on
        self.time_ringmaster()
        # turn the display back on
        self.display_main()


    def finish_ringmaster(self,step=1):
        if step == 1:
            # kill the delays
            self.wipe_delays()
            self.stop_music()
            self.game.score(1000000)

            anim = self.game.assets.dmd_cvFinale
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = True
            # add sound keyframes for fireworks
            animLayer.add_frame_listener(8,self.game.sound.play,param=self.game.assets.sfx_cvDoubleBoom)
            animLayer.add_frame_listener(10,self.music_on,param=self.game.assets.music_cvGear)
            animLayer.add_frame_listener(13,self.game.sound.play,param=self.game.assets.sfx_cvElephant)
            animLayer.add_frame_listener(15,self.game.sound.play,param=self.game.assets.quote_cvEnd)
            animLayer.add_frame_listener(29,self.game.sound.play,param=self.game.assets.sfx_cvAcrobats)
            animLayer.add_frame_listener(52,self.game.sound.play,param=self.game.assets.sfx_cvSqueakyWheel)
            animLayer.add_frame_listener(52,self.game.sound.play,param=self.game.assets.sfx_cvCrash)
            animLayer.add_frame_listener(59,self.game.sound.play,param=self.game.assets.sfx_cvClowns)

            self.layer = animLayer
            self.delay(delay=myWait,handler=self.finish_ringmaster,param=2)

        if step == 2:
            anim = self.game.assets.dmd_cvExplosion
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"

            anim = self.game.assets.dmd_cvFireworks
            myWait = len(anim.frames) / 10.0
            animLayer2 = ep.EP_AnimatedLayer(anim)
            animLayer2.hold = True
            animLayer2.frame_time = 6
            animLayer2.repeat = False
            animLayer2.opaque = False
            animLayer2.composite_op = "blacksrc"

            animLayer2.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_cvFireworkLaunch)
            animLayer2.add_frame_listener(10,self.game.sound.play,param=self.game.assets.sfx_cvFireworkLaunch)
            animLayer2.add_frame_listener(11,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(12,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_cvFireworkLaunch)
            animLayer2.add_frame_listener(15,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(16,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(19,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(21,self.game.sound.play,param=self.game.assets.sfx_cvFireworkLaunch)
            animLayer2.add_frame_listener(24,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)
            animLayer2.add_frame_listener(26,self.game.sound.play,param=self.game.assets.sfx_cvFireworkBang)


            pointsLayer = ep.EP_TextLayer(64,17,self.game.assets.font_12px_az,"center",opaque=False).set_text(str(ep.format_score(1000000)),color=ep.MAGENTA)
            combined = dmd.GroupedLayer(128,32,[pointsLayer,animLayer2,animLayer])
            self.layer = combined
            self.stop_music()
            self.game.sound.play(self.game.assets.sfx_cvExplosion)
            self.delay(delay = myWait, handler=self.done)

    def done(self):
        self.wipe_delays()
        self.running = False
        # turn the level 5 stack flag back off
        self.game.stack_level(5,False)
        # set the music back to the main loop
        self.music_on(self.game.assets.music_mainTheme,mySlice=5)
        # remove the switch blocker
        self.game.switch_blocker('remove',self.myID)
        # check the saloon
        if self.game.switches.saloonPopper.is_active():
            self.kick_saloon()
        #or unload
        else:
            self.unload()

    def atmos(self,sound):
        self.game.score(3750)
        if sound == "leftRamp":
            self.game.sound.play(self.game.assets.sfx_cvWhip)
        elif sound == "rightRamp":
            self.game.sound.play(self.game.assets.sfx_cvAcrobats)
        elif sound == "centerRamp":
            self.game.sound.play(self.game.assets.sfx_cvArc)
        else:
            self.game.sound.play(self.game.assets.sfx_cvRatchet)

    def kick_saloon(self):
            myWait = self.game.sound.play(self.game.assets.sfx_cvEject)
            self.delay(delay = myWait, handler=self.game.saloon.kick)
            if not self.running:
                self.unload()
