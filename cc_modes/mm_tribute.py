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
## The Medieval Madness Tribute
##

from procgame import dmd,game
import ep
import random

class MM_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(MM_Tribute, self).__init__(game,priority)
        self.myID = "MM Tribute"
        self.halted = False
        self.running = False
        self.hitsToWin = 5
        self.won = False

        script = []
        # set up the pause text layer
        textString = "< TROLLS PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.GREEN)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"

    def mode_started(self):
        # overall mode timer
        self.modeTimer = 30
        self.timeLayer = ep.EP_TextLayer(64,22,self.game.assets.font_9px_az,"center",opaque=True).set_text(str(self.modeTimer),color=ep.GREEN)
        # unload the launcher
        self.game.tribute_launcher.unload()
        # first hit is 250, but it adds the bump first in the routine
        self.value = 175000
        self.running = True
        self.halted = False
        self.won = False
        # total left troll hits
        self.leftHitsSoFar = 0
        # total right troll hits
        self.rightHitsSoFar = 0
        # score for the mode
        self.totalPoints = 0
        # set up the text layers
        self.titleLine = ep.EP_TextLayer(64,2,self.game.assets.font_5px_az,"center",opaque=False)
        self.titleLine.set_text(str(self.hitsToWin) + " - TROLLS! - " + str(self.hitsToWin),color=ep.BROWN)
        self.scoreLayer = ep.EP_TextLayer(64,10,self.game.assets.font_5px_az,"center",opaque=False)
        self.intro()

    def ball_drained(self):
        # if we get to zero balls while running, finish
        if self.game.trough.num_balls_in_play == 0 and self.running:
            self.finish_trolls()

    # halt switches
    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_350ms(self,sw):
        print "Trolls It Mine Popper Register"
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_active_for_250ms(self,sw):
        print "Trolls It Saloon Popper Register"
        if not self.halted:
            self.halt_trolls()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_trolls)

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_trolls)

    def intro(self,step=1):
        if step == 1:
            self.stop_music()
            self.game.base.play_quote(self.game.assets.quote_mmTrolls)
            border = dmd.FrameLayer(opaque = True, frame=self.game.assets.dmd_singlePixelBorder.frame[0])
            titleLine = ep.EP_TextLayer(64,2,self.game.assets.font_9px_az,"center",False).set_text("TROLLS!",color=ep.GREEN)
            infoLine1 = ep.EP_TextLayer(64,14,self.game.assets.font_5px_AZ,"center",False).set_text("SHOOT EACH TROLL " + str(self.hitsToWin) + " TIMES")
            infoLine2 = ep.EP_TextLayer(64,20,self.game.assets.font_5px_AZ,"center",False).set_text("TO FINISH")
            combined = dmd.GroupedLayer(128,32,[border,titleLine,infoLine1,infoLine2])
            self.layer = combined
            self.delay(delay=2,handler=self.intro,param=2)
        if step == 2:
            startFrame = dmd.FrameLayer(opaque = True, frame=self.game.assets.dmd_mmTrollsIntro.frame[0])
            transition = ep.EP_Transition(self,self.layer,startFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
            self.delay(delay=1.5,handler=self.intro,param=3)
        if step == 3:
            anim = self.game.assets.dmd_mmTrollsIntro
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = True
            # sounds ?
        #    animLayer.add_frame_listener(19,self.game.sound.play,param=self.game.assets.sfx_mbDracIntro)
        #    animLayer.add_frame_listener(42,self.game.sound.play,param=self.game.assets.sfx_mbCoffinCreak)
        #    animLayer.add_frame_listener(47,self.game.sound.play,param=self.game.assets.sfx_mbBangCrash)
        #    animLayer.add_frame_listener(55,self.game.base.play_quote,param=self.game.assets.quote_mbDracBleh)

            self.layer = animLayer
            self.delay(delay = myWait,handler=self.get_going)
            self.delay(delay = 3, handler=self.get_going)

    def get_going(self):
        # release the ball
        if self.game.tribute_launcher.shot == 3:
            self.game.mountain.eject()
        else:
            self.game.coils.leftGunFightPost.disable()
        # start the music
        self.music_on(self.game.assets.music_trolls)
        # start the timer
        self.modeTimer += 1
        self.time_trolls()
        # start the score updater
        self.score_update()
        # start the display
        self.display_trolls("idle","both")
        # raise the two troll targets
        self.game.bad_guys.target_up(1)
        self.game.bad_guys.target_up(2)

    def display_trolls(self,mode="idle",troll="both"):
        self.cancel_delayed("Display")
        if troll == "left":
            self.cancel_delayed("Left Display")
        elif troll == "right":
            self.cancel_delayed("Right Display")

        if mode == "idle":
            if troll == "left" or troll == "both":
                anim = self.game.assets.dmd_mmTrollIdleLeft
                self.leftTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
                myWait = 0
            if troll == "right" or troll == "both":
                anim = self.game.assets.dmd_mmTrollIdleRight
                self.rightTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
                myWait = 0
        elif mode == "hit":
            if troll == "left":
                anim = self.game.assets.dmd_mmTrollHitLeft
                myWait = len(anim.frames) / 10.0
                self.leftTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            if troll == "right":
                anim = self.game.assets.dmd_mmTrollHitRight
                myWait = len(anim.frames) / 10.0
                self.rightTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        elif mode == "dead":
            if troll == "left":
                anim = self.game.assets.dmd_mmTrollDeadLeft
                myWait = len(anim.frames) / 10.0
                self.leftTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            if troll == "right":
                anim = self.game.assets.dmd_mmTrollDeadRight
                myWait = len(anim.frames) / 10.0
                self.rightTrollLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        else:
            # if we didn't get a cue to change trolls, don't mess with them
            myWait = 0
        # build the layer
        self.leftTrollLayer.composite_op = "blacksrc"
        self.rightTrollLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.timeLayer,self.titleLine,self.scoreLayer,self.leftTrollLayer,self.rightTrollLayer])
        self.layer = combined
        # set the delay for fixing it after a hit or a miss
        if mode == "hit":
            # if a troll got hit loop back to that one to set it to idle after the animation finishes
            if troll == "left":
                self.delay("Left Display",delay=myWait,handler=self.display_trolls,param="left")
            if troll == "right":
                self.delay("Right Display",delay=myWait,handler=self.display_trolls,param="right")
        if mode == "dead":
            if self.won:
                # if both trolls are dead, go to the finish
                self.delay(delay=myWait,handler=self.finish_trolls)

    def hit_troll(self,target):
        # score the points
        self.game.score(self.value)
        # add to the total
        self.totalPoints += self.value
        # play the smack sound
        self.game.sound.play(self.game.assets.sfx_mmTrollSmack)
        if target == 1:
            # register the hit
            self.leftHitsSoFar += 1
            if self.leftHitsSoFar >= self.hitsToWin:
                # troll is dead
                if self.rightHitsSoFar >= self.hitsToWin:
                    # both dead? Winner!
                    self.won = True
                # then display the troll dying
                self.display_trolls(mode="dead",troll="left")
                # play the death sound
                self.game.sound.play(self.game.assets.quote_mmLeftDeath)
            # if troll is not dead, just hit it
            else:
                self.display_trolls(mode="hit",troll="left")
                # and put the target back up
                self.game.bad_guys.target_up(1)
                # and play the pain sound
                self.game.sound.play(self.game.assets.quote_mmLeftPain)
        # other target is 2
        else:
            self.rightHitsSoFar += 1
            if self.rightHitsSoFar >= self.hitsToWin:
                # troll is dead
                if self.leftHitsSoFar >= self.hitsToWin:
                    # both dead? Winner!
                    self.won = True
                # then display the troll dying
                self.display_trolls(mode="dead",troll="right")
                # play the death sound
                self.game.sound.play(self.game.assets.quote_mmRightDeath)
            else:
                self.display_trolls(mode="hit",troll="right")
                # and put the target back up
                self.game.bad_guys.target_up(2)
                # and play the pain sound
                self.game.sound.play(self.game.assets.quote_mmRightPain)

    def score_update(self):
        # update the score line total every half second
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.scoreLayer.set_text(scoreString,color=ep.GREEN)
        self.delay("Score Update",delay=0.5,handler=self.score_update)

    def time_trolls(self):
        self.modeTimer -= 1
        # if we get to zero, end the mode
        if self.modeTimer < 0:
            self.finish_trolls()
        # otherwise update the timer layers and loop back
        else:
            if self.modeTimer > 9:
                color = ep.GREEN
            elif self.modeTimer > 4:
                color = ep.YELLOW
            else:
                color = ep.RED
            self.timeLayer.set_text(str(self.modeTimer),color=color)
            self.delay("Mode Timer",delay=1,handler=self.time_trolls)

    def halt_trolls(self):
        if self.modeTimer <= 0:
            return
        print "HALTING TROLLS IN BUMPERS/MINE"
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # do the halted delay
        self.layer = self.pauseView
        # set the flag
        self.halted = True

    def resume_trolls(self):
        # turn the timer back on
        self.time_trolls()
        # turn the display back on
        if self.leftHitsSoFar == self.hitsToWin:
            self.display_trolls(mode="idle",troll="right")
        elif self.rightHitsSoFar == self.hitsToWin:
            self.display_trolls(mode="idle",troll="left")
        else:
            self.display_trolls(mode="idle",troll="both")

    def finish_trolls(self):
        # kill the delays
        self.wipe_delays()
        border = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mmTrollFinalFrame.frames[0])
        textLayer1 = ep.EP_TextLayer(64,6,self.game.assets.font_5px_AZ,"center",opaque=False)
        if self.won:
            textLayer1.set_text("TROLLS DESTROYED",color=ep.DARK_GREEN)
            # add some extra points if won - to make it a cool 1.5 million
            self.game.score(450000)
            self.totalPoints += 450000
        else:
            textLayer1.set_text("TROLLS ESCAPED",color=ep.DARK_GREEN)
        textLayer2 = ep.EP_TextLayer(64,13,self.game.assets.font_9px_az,"center",opaque=False).set_text(str(ep.format_score(self.totalPoints)),color=ep.GREEN)
        combined = dmd.GroupedLayer(128,32,[border,textLayer1,textLayer2])
        self.layer = combined
        # play a final quote ?
        myWait = 2
        self.delay(delay=myWait,handler=self.done)

    def done(self):
        self.running = False
        # turn the level 5 stack flag back off
        self.game.stack_level(5,False)
        # set the music back to the main loop
        self.music_on(self.game.assets.music_mainTheme,mySlice=5)
        # then unload
        self.unload()

