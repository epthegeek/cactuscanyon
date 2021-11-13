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
###
###
### Save Poor Polly from getting run over by the train!
###

from procgame import dmd
import ep
import random

class SavePolly(ep.EP_Mode):
    """Polly Peril - Tied to the Tracks"""
    def __init__(self,game,priority):
        super(SavePolly, self).__init__(game,priority)
        self.myID = "Tied to the Tracks"
        self.shotsToWin = self.game.user_settings['Gameplay (Feature)']['Save Polly Shots - Train']
        self.showDeathAnimation = self.game.user_settings['Gameplay (Feature)']['Polly Dies Animation']
        self.winsRequired = 'Yes' == self.game.user_settings['Gameplay (Feature)']['Save Polly Wins Required']
        self.running = False
        self.halted = False
        self.won = False
        self.paused = False
        self.finishing_up = False
        self.keys_index = {'start':list(range(len(self.game.sound.sounds[self.game.assets.quote_ttttIntro])))}
        self.counts_index = {'start':0}
        random.shuffle(self.keys_index['start'])
        self.valueMultiplier = 1 # shot value multiplier

    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add',self.myID)
        # set the polly indicator
        self.game.peril = True
        self.shotsSoFar = 0
        self.cows = [self.game.assets.sfx_cow1, self.game.assets.sfx_cow2]
        self.modeTimer = 0
        # setup the 2 animations
        anim = self.game.assets.dmd_trainHeadOn
        self.trainLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=True,frame_time=6)
        anim = self.game.assets.dmd_cowOnTracks
        self.cowLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=6)
        self.pollyTitle = ep.EP_TextLayer(34, 0, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("POLLY PERIL",color=ep.MAGENTA)
        # if we haven't maxed extra balls, the prize is an extra ball light - otherwise, 5 mil
        if not self.game.max_extra_balls_reached():
            reward = "EXTRA BALL LIT"
        else:
            reward = str(ep.format_score(5000000))
        self.awardLine2 = ep.EP_TextLayer(34, 19, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(reward,color=ep.MAGENTA)
        self.awardLine2b= ep.EP_TextLayer(64, 23, self.game.assets.font_7px_az, "center", opaque=False).set_text(reward,color=ep.GREEN)
        self.scoreLine = ep.EP_TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("",blink_frames=8)
        # calculate the shot value
        self.shotValue = 250000
        # extra 250k for each ramp done
        if self.game.show_tracking('leftRampStage') == 5:
            self.shotValue += 50000
        if self.game.river_chase.won:
            self.shotValue += 200000
        if self.game.show_tracking('rightRampStage') == 5:
            self.shotValue += 50000
        if self.game.bank_robbery.won:
            self.shotValue += 200000
        self.running = False
        self.halted = False
        self.won = False
        self.paused = False
        self.finishing_up = False
        self.totalPoints = 0 # holder for total points for the mode earned
        self.valueMultiplier = 1 # shot value multiplier
        self.gotPaused = False # was the mode paused at any point
        self.winBonus = 0
        self.winMultiplier = 2
        self.lastPoints = 0

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            if self.game.show_tracking("centerRampStage") == 99:
                if not self.finishing_up:
                    self.game.base.busy = True
                    self.game.base.queued += 1
                    self.wipe_delays()
                    self.polly_died(drain=True)
                else:
                    self.game.base.busy = True
                    self.game.base.queued += 1

    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    def sw_rightBonusLane_active(self,sw):
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    def sw_rightJetBumper_active(self,sw):
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    def sw_bottomJetBumper_active(self,sw):
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_350ms(self,sw):
        #print "TTTT Mine Popper Register"
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    def sw_saloonPopper_active_for_250ms(self,sw):
        #print "TTTT Saloon Popper Register"
        if self.finishing_up:
            pass
        else:
            if not self.halted:
                self.halt_train()
            # if the train is already halted, cancel any pending resume delay
            else:
                self.cancel_delayed("Resume")

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted and not self.finishing_up:
            self.halted = False
            self.delay("Resume",delay=1,handler=self.in_progress)

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted and not self.finishing_up:
            # kill the halt flag
            self.halted = False
            self.delay("Resume",delay=1,handler=self.in_progress)

    def sw_centerRampMake_active(self,sw):
        if self.finishing_up:
            pass
        else:
            # kill the mode timer until x
            self.cancel_delayed("Mode Timer")
            self.cancel_delayed("Pause Timer")
            if self.running and not self.won:
                # score points
                self.game.score(self.shotValue)
                # center ramp pauses the train
                self.game.sound.play(self.game.assets.sfx_trainWhistle)
                self.pause_train()

    def sw_leftRampEnter_active(self,sw):
        if self.finishing_up:
            pass
        else:
            # kill the mode timer until x
            self.cancel_delayed("Mode Timer")
            self.cancel_delayed("Pause Timer")
            if self.running and not self.won:
                # score points
 #               self.game.score(self.shotValue)
                self.game.sound.play(self.game.assets.sfx_trainWhistle)
                self.advance_save_polly()

    def sw_rightRampMake_active(self,sw):
        if self.finishing_up:
            pass
        else:
            # kill the mode timer until x
            self.cancel_delayed("Mode Timer")
            self.cancel_delayed("Pause Timer")
            if self.running and not self.won:
                # score points
  #              self.game.score(self.shotValue)
                self.game.sound.play(self.game.assets.sfx_trainWhistle)
                self.advance_save_polly()

    def start_save_polly(self,step=1):
        if step == 1:
            # audit
            self.game.game_data['Feature']['Center Polly Started'] += 1
            # set the level 1 stack flag
            self.game.stack_level(2,True)
            # set the running flag
            self.running = True
            # clear any running music
            #self.stop_music()
            # set the center to crazy stage
            self.game.set_tracking('centerRampStage',99)
            self.lamp_update()
            ## TEMP PLAY INTRO
            duration = self.game.base.priority_quote(self.game.assets.quote_ttttDox)
            # Secondary intro quote
            self.delay("Operational",delay=duration+0.1,handler=self.secondary_intro_quote)

            # start the music
            self.music_on(self.game.assets.music_pollyPeril)
            # reset the train
            self.game.train.reset_toy(step=2)
            # run the animation
            anim = self.game.assets.dmd_pollyIntro
            myWait = len(anim.frames) / 30.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
            self.layer = animLayer

            # set the timer for the mode
            self.modeTimer = 30
            # setup some layers
            # alternate lines for the bottom
            script = []
            shotsLine1 = dmd.TextLayer(34, 11, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SHOTS WORTH:")
            shotsLine2 = ep.EP_TextLayer(34, 17, self.game.assets.font_7px_az, "center", opaque=False).set_text(str(ep.format_score(self.shotValue)),color=ep.MAGENTA)
            # group layer of the award lines
            textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
            self.prog_awardLine1 = dmd.TextLayer(34, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)
            page1 = dmd.GroupedLayer(128,32,[self.prog_awardLine1,self.awardLine2])
            page1.composite_op = "blacksrc"
            script.append({"seconds":2,"layer":page1})
            # group layer of the shot value info lines
            page2 = dmd.GroupedLayer(128,32,[shotsLine1,shotsLine2])
            page2.composite_op = "blacksrc"
            script.append({"seconds":2,"layer":page2})
            # scripted layer alternating between the info and award lines
            self.infoLayer = dmd.ScriptedLayer(128,32,script)
            self.infoLayer.composite_op = "blacksrc"

            # loop back for the title card
            self.delay("Operational",delay=myWait,handler=self.start_save_polly,param=2)
        if step == 2:
            # set up the title card
            titleCard = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_ttttBanner.frames[0])
            # transition to the title card
            self.transition = ep.EP_Transition(self,self.layer,titleCard,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_EAST)
            # delay the start process
            self.delay("Get Going",delay=2,handler=self.in_progress)

    def secondary_intro_quote(self):
        # play the intro quote
        duration = self.play_ordered_quote(self.game.assets.quote_ttttIntro,'start')
        # delay the long train whistle
        self.delay("Train Whistle",delay=duration,handler=self.game.sound.play,param=self.game.assets.sfx_longTrainWhistle)

    ## this is the main mode loop - not passing the time to the loop because it's global
    ## due to going in and out of pause
    def in_progress(self):
        if self.running:
            # start the train moving
            self.game.train.move()
            # setup the mode screen with the animated train
            # and all the text
            p = self.game.current_player()
            scoreString = ep.format_score(p.score)
            self.scoreLine.set_text(scoreString,blink_frames=999,color=ep.BROWN)
            timeString = "TIME: " + str(int(self.modeTimer))
            timeLine = ep.EP_TextLayer(34, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(timeString,color=ep.DARK_RED)

            # stick together the animation and static text with the dynamic text
            composite = dmd.GroupedLayer(128,32,[self.trainLayer,self.pollyTitle,self.scoreLine,self.infoLayer,timeLine])
            self.layer = composite
            ## tick down the timer
            self.modeTimer -= 0.1
            ## hurry quote at 5 seconds, plead at 15
            if abs(self.modeTimer - 15) < 0.00000001:
                self.game.base.play_quote(self.game.assets.quote_pollyPlead)
            if abs(self.modeTimer - 5) < 0.00000001:
                self.game.base.play_quote(self.game.assets.quote_pollyHurry)
            if self.modeTimer <= 0:
                # go to a grace period
                self.polly_died()
            # otherwise ...
            else:
                # set up a delay to come back in 1 second with the lowered time
                self.delay("Mode Timer",delay=0.1,handler=self.in_progress)

    # for a ramp hit - time and if advanced or not are conditional for side vs center ramps
    def pause_train(self,advanced=False):
        if self.running:
            #print "PAUSE TRAIN"
            self.paused = True
            # kill the in progress timer
            self.cancel_delayed("Mode Timer")
            # stop the train from moving
            self.game.train.stop()
            # if the thing that sent us here advanced save polly, we pause for 3 seconds
            time = 0
            if advanced:
                time = 3
            # if we're not advancing, there's more to do
            if not advanced:
                time = 5
                # play the pause display
                self.delay("Operational",delay=1.5,handler=self.game.sound.play,param=self.cows[0])
                # swap for the next shot
                self.cows.reverse()
                # setup the display
                border = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_tracksBorder.frames[0])
                awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
                awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
                awardTextTop.set_text("TRAIN",color=ep.BROWN)
                awardTextBottom.set_text("PAUSED",blink_frames=12,color=ep.GREEN)
                completeFrame = dmd.GroupedLayer(128, 32, [border,awardTextTop,awardTextBottom])
                transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)

            # set a delay to start the train again
            self.delay("Pause Timer",delay=1.5,handler=self.pause_timer,param=time)

    def pause_timer(self,time):
        # if the timer is at 0 start the train up again
        if time <= 0:
            #print "RESUMING POLLY"
            self.paused = False
            self.in_progress()
        else:
            #print "POLLY PAUSED: " + str(time)
            # set up the display
            self.pause_display()
            # if not, tick off one
            time -= 1
            # then reschedule 1 second later with the new time
            self.delay("Pause Timer",delay=1,handler=self.pause_timer,param=time)

    def halt_train(self):
        if self.won or self.modeTimer <= 0:
            return
        #print "HALTING TRAIN IN BUMPERS/MINE"
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        # this is the initial delay - have to include it in case of a straight shot to the mine off the ramp
        self.cancel_delayed("Get Going")
        # stop the train
        self.game.train.stop()
        # set the flag
        self.halted = True
        # leave the evidence
        self.gotPaused = True


    def pause_display(self):
        # set up the display
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = ep.EP_TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8,color=ep.BROWN)
        timeString = "TIME: PAUSED"
        timeLine = ep.EP_TextLayer(34, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(timeString,blink_frames=10,color=ep.DARK_RED)
        textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
        awardLine1 = dmd.TextLayer(34, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)

        # stick together the animation and static text with the dynamic text
        composite = dmd.GroupedLayer(128,32,[self.cowLayer,self.pollyTitle,scoreLine,awardLine1,self.awardLine2,timeLine])
        self.layer = composite


        # for a side ramp hit
    def advance_save_polly(self):
        self.game.train.stop()
        # add the sucessful shot
        self.shotsSoFar += 1
        textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
        self.prog_awardLine1.set_text(textString2)
        if self.shotsSoFar >= self.shotsToWin:
            # score points for last shot
            # figure in the multiplier
            points = self.shotValue * self.valueMultiplier
            self.game.score(points)
            # add to total
            self.totalPoints += points
            self.lastPoints = points

            self.polly_saved()
        else:
            # score points
            # figure in the multiplier
            points = self.shotValue * self.valueMultiplier
            self.game.score(points)
            # add to total
            self.totalPoints += points
            self.lastPoints = points
            # increase the multiplier
            self.raise_multiplier()
            # setup the display
            border = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_tracksBorder.frames[0])
            pollyTitle = ep.EP_TextLayer(64, 0, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("POLLY PERIL",color=ep.MAGENTA)
            scoreLine = dmd.TextLayer(64, 6, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(str(ep.format_score(self.lastPoints)))
            textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
            awardLine1 = ep.EP_TextLayer(64, 15, self.game.assets.font_6px_az, "center", opaque=False).set_text(textString2,color=ep.MAGENTA)
            completeFrame = dmd.GroupedLayer(128,32,[border,pollyTitle,scoreLine,awardLine1,self.awardLine2b])
            transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
            # pause the train briefly
            self.delay(name="Pause Timer",delay=1.5,handler=self.pause_timer,param=4)

    def raise_multiplier(self):
        # raise the multiplier value by 1
        self.valueMultiplier += 1
        # update the lamps
        self.lamp_update()
        # set the delay to reset the timer
        self.delay("Multiplier",delay=3,handler=self.reset_multiplier)

    def reset_multiplier(self):
        self.valueMultiplier = 1
        self.lamp_update()


    # success
    def polly_saved(self):
        # audit
        self.game.game_data['Feature']['Center Polly Won'] += 1
        # turn off the polly indicator
        self.game.peril = False
        self.won = True
        self.finishing_up = True
        self.game.train.stop()
        # kill the lights on the three ramps
        self.game.lamp_control.left_ramp('Base')
        self.game.lamp_control.center_ramp('Base')
        self.game.lamp_control.right_ramp('Base')

        self.wipe_delays()
        # play the train stopping animation and some sounds
        anim = self.game.assets.dmd_pollyOnTracks
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        animLayer.opaque = True
        animLayer.add_frame_listener(6,self.game.base.priority_quote,param=self.game.assets.quote_victory)
        stackLevel = self.game.show_tracking('stackLevel')
        # if something higher is running, throw the win display in a cut in
        if True in stackLevel[3:]:
            self.game.interrupter.cut_in(animLayer,myWait)
        else:
            self.layer = animLayer
        # play the train stop noise
        self.game.sound.play(self.game.assets.sfx_trainStop)
        # set the delay for the award
        self.delay("Operational",delay=myWait,handler=self.give_award)

    def give_award(self):
        #print "Giving Polly Award"
        if not self.game.max_extra_balls_reached():
            # light extra ball if not maxxed out
            self.game.mine.light_extra_ball()
        else:
            # if maxxed out, give 5 million points instead
            self.game.score(5000000)
        # then after a delay, reset train
        self.polly_finished() # should delay this

    # fail
    def polly_died(self, step=1, drain=False):
        #print "OMG POLLY IS DEAD"
        if step == 1:
            # turn off the polly indicator
            self.game.peril = False
            self.finishing_up = True
            # stop the train
            self.game.train.stop()
            #if we're showing the full animation, do that now
            if self.showDeathAnimation == 'Show':

                self.game.base.priority_quote(self.game.assets.quote_pollyStop)
                anim = self.game.assets.dmd_pollyMurder
                animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True, opaque=True,repeat=False,frame_time=6)
                myWait = len(anim.frames) / 10.0
                self.layer = animLayer
                self.game.sound.play(self.game.assets.sfx_trainChugShort)
                self.delay(delay=myWait, handler=self.polly_died,param=2)
            # if not, just move on to polly finished
            else:
                backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_poutySheriff.frames[0])
                textLine1 = ep.EP_TextLayer(25, 8, self.game.assets.font_12px_az, justify="center", opaque=False)
                if drain:
                    string = "OH"
                else:
                    string = "TOO"
                textLine1.set_text(string, color=ep.RED)
                textLine2 = ep.EP_TextLayer(98, 8, self.game.assets.font_12px_az, justify="center", opaque=False)
                if drain:
                    string = "NO!"
                else:
                    string = "LATE!"
                textLine2.set_text(string, color=ep.RED)
                combined = dmd.GroupedLayer(128, 32, [backdrop, textLine1, textLine2])
                self.layer = combined
                self.game.sound.play(self.game.assets.sfx_glumRiff)
                self.delay("Operational", delay=1.5, handler=self.polly_finished)
        if step == 2:
            if self.running:
                backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_pollyMurder.frames[7])
                awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ_outline,justify="center",opaque=False)
                awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az_outline,justify="center",opaque=False)
                awardTextBottom.composite_op = "blacksrc"
                awardTextTop.composite_op = "blacksrc"
                awardTextTop.set_text("POLLY")
                awardTextBottom.set_text("DIED")
                combined = dmd.GroupedLayer(128,32,[backdrop,awardTextTop,awardTextBottom])
                self.layer = combined
                duration = self.game.sound.play(self.game.assets.sfx_glumRiff)
                self.delay("Display",delay=duration,handler=self.clear_layer)
                self.delay("Operational",delay=1.5,handler=self.polly_finished)

    def polly_finished(self):
        self.running = False
        # only kill the music if there's not a higher level running
        # stop the polly music
        #self.stop_music(slice=3)
        self.game.train.reset_toy(type=2)
        # turn off the polly display
        self.layer = None
        # up the stampede value if won
        if self.won:
            self.game.increase_tracking('Stampede Addon',500000)
        # set the tracking on the ramps
        # if wins are required, and player did not win, reset ramp to stage 1
        if self.winsRequired and not self.won:
            self.game.set_tracking('centerRampStage',1)
        # if wins are not required then the ramp goes to 'done' even if lost
        else:
            self.game.set_tracking('centerRampStage',5)
        self.lamp_update()
        self.end_save_polly()

    # clean up and exit
    def end_save_polly(self):
        #print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.stack_level(2,False)
        # check to see if stampede is ready - if we're not ending due to ball fail
        if self.game.trough.num_balls_in_play >= 0:
            self.game.base.check_stampede()
            # turn the music back on - if we're not done
            self.music_on(self.game.assets.music_mainTheme,mySlice=3)
        # remove the switch blocker
        self.game.switch_blocker('remove',self.myID)
        self.finishing_up = False
        # unset the busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload the mode
        self.unload()

    def tilted(self):
        if self.running:
            if self.winsRequired and not self.won:
                self.game.set_tracking('centerRampStage',1)
            # if wins are not required then the ramp goes to 'done' even if lost
            else:
                self.game.set_tracking('centerRampStage',5)
            self.game.train.reset_toy(type=2)
        self.running = False
        self.unload()

    def mode_stopped(self):
        #print "SAVE POLLY IS DISPATCHING DELAYS"
        self.wipe_delays()
        self.clear_layer()
        self.paused = False
        if self.running:
            if self.won or self.modeTimer <= 0:
                self.running = False
                self.polly_finished()

    def clear_layer(self):
        if not self.finishing_up:
            self.layer = None
