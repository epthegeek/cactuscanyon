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
## The Monster Bash Tribute
##

from procgame import dmd,game
import ep
import random

class MB_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(MB_Tribute, self).__init__(game,priority)
        self.myID = "MB Tribute"
        # for timer halting in saloon/jets
        self.halted = False
        self.running = False
        self.hitsToWin = 5

        script = []
        # set up the pause text layer
        textString = "< DRAC ATTACK PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.RED)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"

        self.titleLine = ep.EP_TextLayer(64,1,self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("DRAC ATTACK",color=ep.RED)
        self.leftTimerLine = ep.EP_TextLayer(0,1,self.game.assets.font_7px_az, "left",True)
        self.rightTimerLine = ep.EP_TextLayer(128,1,self.game.assets.font_7px_az,"right",False)
        self.scoreLine = ep.EP_TextLayer(64,6,self.game.assets.font_12px_az,"center",opaque=False)
        self.infoLine = ep.EP_TextLayer(64,22,self.game.assets.font_5px_AZ,"center", opaque=False)
        self.infoLine.set_text(str(self.hitsToWin) + " - HITS TO FINISH - " + str(self.hitsToWin))
        # offset position for the drac layers based on index position
        self.offsets = [-51,-23,5,33]

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
        # drac movement timer
        self.moveTimer = 8
        # drac position
        self.index = 3
        # total drac hits
        self.hitsSoFar = 0
        # score for the mode
        self.totalPoints = 0
        # set the move direction
        self.direction = "Left"
        self.intro()

    def ball_drained(self):
        # if we get to zero balls while running, finish
        if self.game.trough.num_balls_in_play == 0 and self.running:
            self.finish_drac()

    def halt_test(self):
        if not self.halted:
            self.halt_drac()
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
        #print "Drac Mine Popper Register"
        self.halt_test()

    def sw_saloonPopper_active_for_250ms(self,sw):
        #print "Drac Saloon Popper Register"
        self.halt_test()

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_drac)

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_drac)

    def intro(self,step=1):
        if step == 1:
            self.stop_music()
            self.game.sound.play(self.game.assets.sfx_mbBats)
            anim = self.game.assets.dmd_mbDracIntro1
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = True
            animLayer.composite_op = "blacksrc"

            backdrop = dmd.FrameLayer(opaque=True,frame=self.game.assets.dmd_mbLogo.frames[0])
            combined = dmd.GroupedLayer(128,32,[backdrop,animLayer])
            self.layer = combined
            self.delay(delay = myWait,handler=self.intro,param=2)

        if step == 2:
            anim = self.game.assets.dmd_mbDracIntro2
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = True
            # sounds ?
            animLayer.add_frame_listener(23,self.game.sound.play,param=self.game.assets.sfx_mbCoffinCreak)
            animLayer.add_frame_listener(28,self.game.sound.play,param=self.game.assets.sfx_mbBangCrash)
            animLayer.add_frame_listener(36,self.game.base.play_quote,param=self.game.assets.quote_mbDracBleh)

            self.game.sound.play(self.game.assets.sfx_mbDracIntro)
            self.layer = animLayer
            self.delay(delay = myWait,handler=self.intro,param=3)

        if step == 3:
            self.game.base.music_on(self.game.assets.music_dracAttack)
            textLayer1 = ep.EP_TextLayer(64,5,self.game.assets.font_9px_az,"center",True).set_text("HIT DRACULA " + str(self.hitsToWin) + " TIMES",color=ep.RED)
            textLayer2 = ep.EP_TextLayer(64,16,self.game.assets.font_9px_az,"center",False).set_text("TO FINISH",color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2])
            current = self.layer
            transition = ep.EP_Transition(self,current,combined,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
            # sounds ?
            self.delay(delay = 3, handler=self.get_going)

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
        # start the music
        #self.music_on(self.game.assets.music_dracAttack)
        # start the timer
        self.modeTimer += 1
        self.time_drac()
        # start the score updater
        self.score_update()
        # start the display
        self.display_drac("idle",fade = True)
        # raise the first drac
        self.game.bad_guys.target_up(self.index)
        # start the move timer
        self.moveTimer += 1
        self.move_drac()

    def display_drac(self,mode=None,fade = False):
        self.cancel_delayed("Display")
        if mode == "idle":
            anim = self.game.assets.dmd_mbDracIdle
            myWait = len(anim.frames) / 10.0
            self.dracLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        elif mode == "hit":
            anim = self.game.assets.dmd_mbDracSmack
            myWait = len(anim.frames) / 10.0
            self.dracLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        else:
            # if we didn't get a cue to change cousin it, we don't mess with him
            myWait = 0
        # build the layer
        self.dracLayer.composite_op = "blacksrc"
        # set the drac position
        self.dracLayer.set_target_position(self.offsets[self.index],0)
        combined = dmd.GroupedLayer(128,32,[self.leftTimerLine,self.rightTimerLine,self.titleLine,self.scoreLine,self.infoLine,self.dracLayer])
        # turn on the layer - crossfade at startup
        if fade:
            current = self.layer
            transition = ep.EP_Transition(self,current,combined,ep.EP_Transition.TYPE_CROSSFADE)
        else:
            self.layer = combined
        # set the delay for fixing it after a hit or a miss
        if mode == "hit":
            self.delay("Display",delay=myWait,handler=self.hit_banner)

    def hit_banner(self):
        title = ep.EP_TextLayer(64,3,self.game.assets.font_7px_az,"center",False)
        # if we have enough hits to win
        if self.hitsSoFar >= self.hitsToWin:
            title.set_text("DRACULA DEFEATED",color=ep.RED)
        else:
            title.set_text("DRACULA DAMAGED", color=ep.RED)
        points = ep.EP_TextLayer(64,13,self.game.assets.font_12px_az,"center",False).set_text(ep.format_score(self.value))
        combined = dmd.GroupedLayer(128,32,[title,points])
        transition = ep.EP_Transition(self,self.layer,combined,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        if self.hitsSoFar >= self.hitsToWin:
            self.delay(delay=2,handler=self.finish_drac)
        else:
            self.delay("Display",delay=2,handler=self.post_hit_banner)

    def post_hit_banner(self):
        # restart the timer and reset
        self.modeTimer = 21
        self.time_drac()
        self.display_drac(mode="idle",fade=True)
        # put drac back up
        self.game.bad_guys.target_up(self.index)
        # restart the move timer
        self.move_drac()

    def hit_drac(self):
        #print "Hit Drac"
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
        remain = str(self.hitsToWin - self.hitsSoFar)
        self.infoLine.set_text(remain + " - HITS TO FINISH - " + remain)
        # sound ?

        self.modeTimer = 21
        # display the hit
        self.display_drac("hit")
        # play the hit sound
        myWait = self.game.sound.play(self.game.assets.sfx_mbSmack)
        self.delay(delay=myWait,handler=self.game.base.priority_quote,param=self.game.assets.quote_mbDracSmack)

    def time_drac(self):
        self.modeTimer -= 1
        # if we get to zero, end the mode
        if self.modeTimer < 0:
            self.finish_drac()
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
            self.delay("Mode Timer",delay=1,handler=self.time_drac)

    def move_drac(self):
        self.moveTimer -= 1
        if self.moveTimer <= 0:
            self.moveTimer = 8
            #print "Moving Dracula"
            # drop the target
            self.game.bad_guys.target_down(self.index)
            # move to the next target
            if self.direction == "Left":
                if self.index > 0:
                    self.index -= 1
                else:
                    self.direction = "Right"
                    self.index += 1
            else:
                if self.index < 3:
                    self.index += 1
                else:
                    self.direction = "Left"
                    self.index -= 1
            # raise the target
            self.game.bad_guys.target_up(self.index)
            self.game.base.play_quote(self.game.assets.quote_mbDracMove)
            # update the display
            self.display_drac()

        self.delay("Move Timer",delay=1,handler=self.move_drac)

    def score_update(self):
        # update the score line total every half second
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.scoreLine.set_text(scoreString,color=ep.RED)
        self.delay("Score Update",delay=0.5,handler=self.score_update)

    def halt_drac(self):
        if self.modeTimer <= 0:
            return
        #print "HALTING DRAC ATTACK IN BUMPERS/MINE"
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # do the halted delay
        self.layer = self.pauseView
        # set the flag
        self.halted = True

    def resume_drac(self):
        # turn the timer back on
        self.time_drac()
        # turn the display back on
        self.display_drac("idle")


    def finish_drac(self):
        # kill the delays
        self.wipe_delays()
        # drop the targets
        self.game.bad_guys.drop_targets()
        border = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mbStakeBorder.frames[0])
        textLayer1 = ep.EP_TextLayer(64,2,self.game.assets.font_5px_AZ,"center",opaque=False).set_text("DRAC ATTACK",color=ep.RED)
        textLayer3 = ep.EP_TextLayer(64,9,self.game.assets.font_5px_AZ,"center",opaque=False).set_text("TOTAL",color=ep.RED)
        textLayer2 = ep.EP_TextLayer(64,16,self.game.assets.font_9px_az,"center",opaque=False).set_text(str(ep.format_score(self.totalPoints)),color=ep.GREEN)
        combined = dmd.GroupedLayer(128,32,[border,textLayer1,textLayer2,textLayer3])
        self.layer = combined
        # play a final quote
        if self.hitsToWin == self.hitsSoFar:
            sound = self.game.assets.quote_mbDracWin
        elif self.hitsSoFar <= 1:
            sound = self.game.assets.quote_mbDracBad
        else:
            sound = self.game.assets.quote_mbDracLose
        myWait = self.game.base.play_quote(sound)
        self.delay(delay=myWait,handler=self.done)

    def done(self):
        self.running = False
        # turn the level 5 stack flag back off
        self.game.stack_level(5,False)
        # set the music back to the main loop
        self.music_on(self.game.assets.music_mainTheme,mySlice=5)
        # remove the switch blocker
        self.game.switch_blocker('remove',self.myID)
        # then unload
        self.unload()
