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
## The Scared Stiff Tribute
##

from procgame import dmd,game
import ep
import random

class SS_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(SS_Tribute, self).__init__(game,priority)
        self.myID = "SS Tribute"
        # for timer halting in saloon/jets
        self.halted = False
        self.running = False
        self.hitsToWin = 4
        self.hitsSoFar = 0
        self.beerHit = False
        self.won = False

        script = []
        # set up the pause text layer
        textString = "< LEAPERS PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.ORANGE)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"

        self.titleLine = ep.EP_TextLayer(64,0,self.game.assets.font_7px_bold_az, "center", opaque=True).set_text("LEAPER MANIA",color=ep.GREEN)
        self.leftTimerLine = ep.EP_TextLayer(0,26,self.game.assets.font_5px_AZ, "left",False)
        self.rightTimerLine = ep.EP_TextLayer(128,26,self.game.assets.font_5px_AZ,"right",False)
        self.scoreLine = ep.EP_TextLayer(64,8,self.game.assets.font_9px_az,"center",opaque=False)
        self.infoLine = ep.EP_TextLayer(0,1,self.game.assets.font_5px_AZ,"center", opaque=False)
        # offset position for the frog layers based on index position
        self.offsets = [0,-9,-18,-28]
        self.keys_index = {'hit':list(range(len(self.game.sound.sounds[self.game.assets.quote_ssHit]))),
                           'urge':list(range(len(self.game.sound.sounds[self.game.assets.quote_ssUrge])))}
        self.counts_index = {'hit':0,
                             'urge':0}
        random.shuffle(self.keys_index['hit'])
        random.shuffle(self.keys_index['urge'])

    def mode_started(self):
        self.frogLayers = [None,None,None,None]
        self.availFrogs = [0,1,2,3]
        # sets of frog animations
        self.blue_frog = [self.game.assets.dmd_ssBlueLeft,"Left",self.game.assets.dmd_ssSquishBlue,"Right",self.game.assets.dmd_ssBlueRight]
        self.green_frog = [self.game.assets.dmd_ssGreenLeft,"Left",self.game.assets.dmd_ssSquishGreen,"Right",self.game.assets.dmd_ssGreenRight]
        self.orange_frog = [self.game.assets.dmd_ssOrangeLeft,"Left",self.game.assets.dmd_ssSquishOrange,"Right",self.game.assets.dmd_ssOrangeRight]
        self.purple_frog = [self.game.assets.dmd_ssPurpleLeft,"Left",self.game.assets.dmd_ssSquishPurple,"Right",self.game.assets.dmd_ssPurpleRight]
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add',self.myID)
        # unload the launcher
        self.game.tribute_launcher.unload()
        # first hit is 250, but it adds the bump first in the routine
        self.value = 175000
        self.bump = 75000
        self.running = True
        self.won = False
        self.halted = False
        self.hitsSoFar = 0
        # overall mode timer
        self.modeTimer = 20
        # score for the mode
        self.totalPoints = 0
        # reset the frogs
        self.liveFrogs = [self.blue_frog,self.green_frog,self.orange_frog,self.purple_frog]
        random.shuffle(self.liveFrogs)
        # pick 2 to go right
        righties = random.sample(self.liveFrogs,2)
        for frog in righties:
            # reverse their list order so that going the other way is first
            frog.reverse()
        self.intro()

    def ball_drained(self):
        # if we get to zero balls while running, finish
        if self.game.trough.num_balls_in_play == 0 and self.running:
            self.finish_frogs()

    # halt switches
    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_350ms(self,sw):
        #print "Frog Mine Popper Register"
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_active_for_250ms(self,sw):
        #print "Frog Saloon Popper Register"
        if not self.halted:
            self.halt_frogs()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_frogs)

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.delay("Resume",delay=1,handler=self.resume_frogs)

    # kill a frog if the beer GETS IT
    def sw_beerMug_active(self,sw):
        if self.beerHit:
            pass
        else:
            self.beerHit = True
            # delay to re-allow due to debounce being off
            self.delay(delay=0.050,handler=self.beer_unhit)
            #print "Beer Mug Hit - Kill Frog"
            if not self.won:
                self.kill_frog()
        return game.SwitchStop

    # kill a frog if the beer GETS IT
    def sw_phantomSwitch4_active(self,sw):
        if self.beerHit:
            pass
        else:
            self.beerHit = True
            # delay to re-allow due to debounce being off
            self.delay(delay=0.050,handler=self.beer_unhit)
            #print "Beer Mug Hit - Kill Frog"
            if not self.won:
                self.kill_frog()
        return game.SwitchStop

    def beer_unhit(self):
        self.beerHit = False

    def intro(self,step=1):
        if step == 1:
            self.stop_music()
            # intro riff
            duration = self.game.sound.play(self.game.assets.sfx_ssHeavyRiff)
            # set up the 2 frames for the transition
            logo = dmd.FrameLayer(opaque=True,frame=self.game.assets.dmd_ssLogo.frames[0])
            frog = dmd.FrameLayer(opaque=True,frame=self.game.assets.dmd_ssLeaperWipe.frames[0])
            # crossfade transition to the frog sitting
            self.transition = ep.EP_Transition(self,logo,frog,ep.EP_Transition.TYPE_CROSSFADE)
            # go to step 2 after duration expires
            self.delay(delay=duration - 0.8,handler=self.intro,param=2)

        if step == 2:
            anim = self.game.assets.dmd_ssLeaperWipe
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"
            # sounds ?
            animLayer.add_frame_listener(5,self.game.sound.play,param=self.game.assets.sfx_ssScream)
            # layers behind the wipe
            textLine1 = ep.EP_TextLayer(64,11,self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("HIT BEER MUG TO",color=ep.YELLOW)
            textLine2 = ep.EP_TextLayer(64,22,self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("SQUASH LEAPERS",color=ep.BROWN)
            combined = dmd.GroupedLayer(128,32,[self.titleLine,textLine2,textLine1,animLayer])
            self.layer = combined
            self.delay(delay = myWait,handler=self.intro,param=3)

        if step == 3:
            textLine1 = ep.EP_TextLayer(64,11,self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("HIT BEER MUG TO",blink_frames=8,color=ep.YELLOW)
            textLine2 = ep.EP_TextLayer(64,22,self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("SQUASH LEAPERS",color=ep.BROWN)
            combined = dmd.GroupedLayer(128,32,[self.titleLine,textLine2,textLine1])
            self.layer = combined
            self.game.sound.play(self.game.assets.quote_ssStart)
            self.delay(delay = 1.5,handler=self.get_going)


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
        self.music_on(self.game.assets.music_leapers)
        # start the timer
        self.modeTimer += 1
        self.time_frogs()
        # start the score updater
        self.score_update()
        # start the display
        self.display_frogs("idle")
        self.delay(delay = 0.6, handler=lambda: self.display_frogs(mode="jump",num=random.choice(self.availFrogs)))

    def display_frogs(self,mode=None,num=None,fade=False):
        if not self.won:
            self.cancel_delayed("Display")
            # set the frogs
            for n in self.availFrogs:
                if n != num:
                    # grab the last frame from the first slot animation
                    self.frogLayers[n] = dmd.FrameLayer(opaque=False,frame=self.liveFrogs[n][4].frames[5])
                    # set the composite op
                    self.frogLayers[n].composite_op = "blacksrc"
                    # adjust the position
                    self.frogLayers[n].set_target_position(self.offsets[n],0)

            if mode == "jump":
                anim = self.liveFrogs[num][0]
                myWait = len(anim.frames) / 10.0
                self.frogLayers[num] = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
                self.frogLayers[num].composite_op = "blacksrc"
                self.frogLayers[num].set_target_position(self.offsets[num],0)
                # reverse the order of that frog for next jump
                self.liveFrogs[num].reverse()
            else:
                # if we didn't get a cue to change cousin it, we don't mess with him
                pass

            # build the layer
            layers = []
            layers.append(self.titleLine)
            layers.append(self.leftTimerLine)
            layers.append(self.rightTimerLine)
            layers.append(self.scoreLine)
            for layer in self.frogLayers:
                layers.append(layer)
            combined = dmd.GroupedLayer(128,32,layers)
            # turn on the layer - crossfade at startup
            self.layer = combined
            # set the delay for fixing it after a hit or a miss
            if mode == "jump" and len(self.availFrogs) > 0:
                choices = [0.65,0.8,1.0,1.2,1.4]
                self.game.sound.play(self.game.assets.sfx_ssRibbit)
                self.delay("Display",delay=random.choice(choices),handler=lambda: self.display_frogs(mode="jump",num=random.choice(self.availFrogs)))


    def kill_frog(self,step=1):
        if step == 1:
            #print "Kill Frog"
            # cancel any display timer
            self.cancel_delayed("Display")
            # choose a frog to kill
            dead = random.choice(self.availFrogs)
            # remove it from the available frogs
            self.availFrogs.remove(dead)
            if len(self.availFrogs) == 0:
                self.won = True
                self.cancel_delayed("Display")
                #print "All frogs squashed!"
            # stop the timer
            self.cancel_delayed("Mode Timer")
            # on a hit, increase the value, and add the new value to the total and display the hit
            self.value += self.bump
            # score the points
            self.game.score(self.value)
            self.totalPoints += self.value
            # register the hit
            self.hitsSoFar += 1
            # sound ?
            # remove the live layer
            self.frogLayers[dead] = dmd.FrameLayer(opaque=False,frame=self.game.assets.dmd_blank.frames[0])
            self.frogLayers[dead].composite_op = "blacksrc"
            # setup the animation
            anim = self.liveFrogs[dead][2]
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            # sounds ?
            animLayer.add_frame_listener(1,self.game.sound.play,param=self.game.assets.sfx_ssScream)
            animLayer.add_frame_listener(1,self.game.sound.play,param=self.game.assets.sfx_ssSquish)
            self.layer = animLayer
            # call part 2 after the animation
            self.delay("Display",delay=myWait,handler=self.kill_frog,param=2)

        if step == 2:
            # play a hit quote
            self.play_ordered_quote(self.game.assets.quote_ssHit,'hit')
            # display the hit
            title = ep.EP_TextLayer(64,2,self.game.assets.font_9px_az, "center", opaque=False).set_text("LEAPER SQUASHED",color=ep.RED)
            score = ep.EP_TextLayer(64,13,self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.value),blink_frames=6,color=ep.GREEN)
            anim = self.game.assets.dmd_ssSquishWipe
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[title,score,animLayer])
            self.layer = combined
            self.delay("Display",delay=myWait +1,handler=self.kill_frog,param=3)

        if step == 3:
            if len(self.availFrogs) == 0:
                # we're out of frogs, party is over
                self.finish_frogs()
            else:
                self.modeTimer = 21
                self.time_frogs()
                self.display_frogs()
                self.delay("Display",delay=0.7, handler=lambda: self.display_frogs(mode="jump",num=random.choice(self.availFrogs)))


    def time_frogs(self):
        self.modeTimer -= 1
        # if we get to zero, end the mode
        if self.modeTimer < 0:
            self.cancel_delayed("Display")
            self.finish_frogs()
        # otherwise update the timer layers and loop back
        else:
            if self.modeTimer > 9:
                color = ep.GREEN
            elif self.modeTimer > 4:
                color = ep.YELLOW
            else:
                color = ep.RED
            if self.modeTimer == 12 or self.modeTimer == 5:
                self.play_ordered_quote(self.game.assets.quote_ssUrge,'urge')
            self.leftTimerLine.set_text(str(self.modeTimer),color=color)
            self.rightTimerLine.set_text(str(self.modeTimer),color=color)
            self.delay("Mode Timer",delay=1,handler=self.time_frogs)

    def score_update(self):
        # update the score line total every half second
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.scoreLine.set_text(scoreString,color=ep.RED)
        self.delay("Score Update",delay=0.5,handler=self.score_update)

    def halt_frogs(self):
        if self.modeTimer <= 0:
            return
        #print "HALTING LEAPERS IN BUMPERS/MINE"
        self.cancel_delayed("Display")
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # do the halted delay
        self.layer = self.pauseView
        # set the flag
        self.halted = True

    def resume_frogs(self):
        # turn the timer back on
        self.time_frogs()
        # turn the display back on
        self.display_frogs("idle")


    def finish_frogs(self,step=1):
        if step == 1:
            # kill the delays
            self.wipe_delays()
            # stop the music
            self.stop_music()
            anim = self.game.assets.dmd_ssBubbles
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = False
            animLayer.frame_time = 6
            animLayer.repeat = True
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"
            textLayer1 = ep.EP_TextLayer(64,2,self.game.assets.font_5px_AZ,"center",opaque=False).set_text("LEAPER TOTAL",color=ep.GREEN)
            textLayer2 = ep.EP_TextLayer(64,11,self.game.assets.font_9px_az,"center",opaque=False).set_text(str(ep.format_score(self.totalPoints)),color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,animLayer])
            self.layer = combined
            # play a final quote
            if len(self.availFrogs) == 0:
                self.delay(delay=0.3,handler=self.game.sound.play,param=self.game.assets.quote_ssWin)
            else:
                self.delay(delay=0.3,handler=self.game.sound.play,param=self.game.assets.quote_ssLose)
            self.game.sound.play(self.game.assets.sfx_ssBubbling)
            self.game.sound.play(self.game.assets.sfx_ssGong)
            self.delay(delay=1.5,handler=self.finish_frogs,param=2)
        if step == 2:
            # do the pop
            anim = self.game.assets.dmd_ssPop
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            animLayer.repeat = False
            animLayer.opaque = False
            animLayer.composite_op = "blacksrc"
            animLayer.add_frame_listener(6,self.game.sound.play,param=self.game.assets.sfx_ssPop)
            textLayer1 = ep.EP_TextLayer(64,2,self.game.assets.font_5px_AZ,"center",opaque=False).set_text("LEAPER TOTAL",color=ep.GREEN)
            textLayer2 = ep.EP_TextLayer(64,11,self.game.assets.font_9px_az,"center",opaque=False).set_text(str(ep.format_score(self.totalPoints)),color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,animLayer])
            self.layer = combined
            self.delay(delay=1.5,handler=self.done)

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
