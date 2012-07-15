###
###
### Save Poor Polly from getting run over by the train!
###

from procgame import *
import cc_modes
import ep

class SavePolly(ep.EP_Mode):
    """BadGuys for great justice - covers Quickdraw, Showdown, and ... ? """
    def __init__(self,game,priority):
        super(SavePolly, self).__init__(game,priority)
        self.shotsToWin = self.game.user_settings['Gameplay (Feature)']['Shots to save Polly']
        self.running = False
        self.halted = False

    def mode_started(self):
        self.shotsSoFar = 0
        self.cows = [self.game.assets.sfx_cow1, self.game.assets.sfx_cow2]
        self.modeTimer = 0
        # setup the 2 animations
        anim = dmd.Animation().load(ep.DMD_PATH+'train-head-on.dmd')
        self.trainLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=True,frame_time=6)
        anim = dmd.Animation().load(ep.DMD_PATH+'cow-on-tracks.dmd')
        self.cowLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=True,repeat=True,frame_time=6)
        self.pollyTitle = dmd.TextLayer(34, 0, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("POLLY PERIL")
        # if we haven't maxed extra balls, the prize is an extra ball light - otherwise, 5 mil
        if self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
            reward = "EXTRA BALL LIT"
        else:
            reward = "5,000,000"
        self.awardLine2 = dmd.TextLayer(34, 19, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(reward)
        self.awardLine2b= dmd.TextLayer(64, 23, self.game.assets.font_7px_az, "center", opaque=False).set_text(reward)
        # calculate the shot value
        self.shotValue = 250000
        # extra 250k for each ramp done
        if self.game.show_tracking('leftRampStage') == 4:
            self.shotValue += 250000
        if self.game.show_tracking('rightRampStage') == 4:
            self.shotValue += 250000

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            if self.game.show_tracking("centerRampStage") == 99:
                self.game.base_game_mode.busy = True
                self.polly_died()

    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt_train()

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt_train()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt_train()

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt_train()

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt_train()

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_390ms(self,sw):
        if not self.halted:
            self.halt_train()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            # give back 1 second grace
            self.modeTimer += 1
            self.in_progress()

    def sw_centerRampMake_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        if self.running:
            # score points
            self.game.score(self.shotValue)
            # center ramp pauses the train
            self.game.sound.play(self.game.assets.sfx_trainWhistle)
            self.pause_train()
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        if self.running:
            # score points
            self.game.score(self.shotValue)
            self.game.sound.play(self.game.assets.sfx_leftRampEnter)
            self.advance_save_polly()
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        if self.running:
            # score points
            self.game.score(self.shotValue)
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.advance_save_polly()
        return game.SwitchStop

    def start_save_polly(self):
        # set the level 1 stack flag
        self.game.set_tracking('stackLevel',True,1)
        # set the running flag
        self.running = True
        # clear any running music
        print "start_save_polly IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # set the center to crazy stage
        self.game.set_tracking('centerRampStage',99)
        self.game.right_ramp.update_lamps()
        self.game.center_ramp.update_lamps()
        self.game.left_ramp.update_lamps()

        # start the music
        self.game.base_game_mode.music_on(self.game.assets.music_pollyPeril)
        # reset the train
        self.game.train.reset_toy()
        # run the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'polly-peril.dmd')
        myWait = len(anim.frames) / 30 + 2
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
        self.layer = animLayer
        # then hand off to the main loop
        self.delay(delay=myWait,handler=self.get_going)

    # start the music, set up the static text lines an animations
    def get_going(self):
        print "POLLY GET GOING"
        # set the timer for the mode
        self.modeTimer = 30
        # setup some layers
        # alternate lines for the bottom
        script = []
        shotsLine1 = dmd.TextLayer(34, 11, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SHOTS WORTH:")
        shotsLine2 = dmd.TextLayer(34, 17, self.game.assets.font_7px_az, "center", opaque=False).set_text(str(ep.format_score(self.shotValue)))
        # group layer of the award lines
        textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
        awardLine1 = dmd.TextLayer(34, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)
        page1 = dmd.GroupedLayer(128,32,[awardLine1,self.awardLine2])
        page1.composite_op = "blacksrc"
        script.append({"seconds":2,"layer":page1})
        # group layer of the shot value info lines
        page2 = dmd.GroupedLayer(128,32,[shotsLine1,shotsLine2])
        page2.composite_op = "blacksrc"
        script.append({"seconds":2,"layer":page2})
        # scripted layer alternating between the info and award lines
        self.infoLayer = dmd.ScriptedLayer(128,32,script)
        self.infoLayer.composite_op = "blacksrc"

        # jump into the mode loop
        self.in_progress()

    ## this is the main mode loop - not passing the time to the loop because it's global
    ## due to going in and out of pause
    def in_progress(self):
        if self.running:
            print "POLLY IN PROGRESS - TIME:" + str(self.modeTimer)
            # start the train moving
            self.game.train.move()
            # setup the mode screen with the animated train
            # and all the text
            p = self.game.current_player()
            scoreString = ep.format_score(p.score)
            scoreLine = dmd.TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8)
            timeString = "TIME: " + str(self.modeTimer)
            timeLine = dmd.TextLayer(34, 25, self.game.assets.font_6px_az, "center", opaque=False).set_text(timeString)

            # stick together the animation and static text with the dynamic text
            composite = dmd.GroupedLayer(128,32,[self.trainLayer,self.pollyTitle,scoreLine,self.infoLayer,timeLine])
            self.layer = composite
            ## tick down the timer
            self.modeTimer -= 1
            ## TODO play some hurry quote at 5 seconds?
            # if we've run out of time
            if self.modeTimer == 0:
                # go to a grace period
                self.polly_died()
            # otherwise ...
            else:
                # set up a delay to come back in 1 second with the lowered time
                self.delay(name="Mode Timer",delay=1,handler=self.in_progress)

    # for a ramp hit - time and if advanced or not are conditional for side vs center ramps
    def pause_train(self,advanced=False):
        if self.running:
            print "PAUSE TRAIN"
            # kill the in progress timer
            self.cancel_delayed("Mode Timer")
            # stop the train from moving
            self.game.train.stop()
            # if the thing that sent us here advanced save polly, we pause for 3 seconds
            if advanced:
                time = 3
            # if we're not advancing, there's more to do
            if not advanced:
                time = 5
                # play the pause display
                self.delay(delay=1.5,handler=self.game.play_remote_sound,param=self.cows[0])
                # swap for the next shot
                self.cows.reverse()
                # setup the display
                border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'tracks-border.dmd').frames[0])
                awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
                awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
                awardTextTop.set_text("TRAIN")
                awardTextBottom.set_text("PAUSED",blink_frames=12)
                completeFrame = dmd.GroupedLayer(128, 32, [border,awardTextTop,awardTextBottom])
                transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)

            # set a delay to start the train again
            self.delay(delay=1.5,handler=self.pause_timer,param=time)

    def pause_timer(self,time):
        # if the timer is at 0 start the train up again
        if time <= 0:
            print "RESUMING POLLY"
            self.modeTimer += 1
            self.in_progress()
        else:
            print "POLLY PAUSED: " + str(time)
            # set up the display
            self.pause_display()
            # if not, tick off one
            time -= 1
            # then reschedule 1 second later with the new time
            self.delay(name="Pause Timer",delay=1,handler=self.pause_timer,param=time)

    def halt_train(self):
        print "HALTING TRAIN IN BUMPERS/MINE"
        # cancel delays
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        # stop the train
        self.game.train.stop()
        # set the flag
        self.halted = True

    def pause_display(self):
        # set up the display
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8)
        timeString = "TIME: PAUSED"
        timeLine = dmd.TextLayer(34, 25, self.game.assets.font_6px_az, "center", opaque=False).set_text(timeString,blink_frames=10)
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
        if self.shotsSoFar >= self.shotsToWin:
            self.polly_saved()
        else:
            # score points
            self.game.score(self.shotValue)
            # TODO play some sound?
            # setup the display
            border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'tracks-border.dmd').frames[0])
            pollyTitle = dmd.TextLayer(64, 0, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("POLLY PERIL")
            scoreLine = dmd.TextLayer(64, 6, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(str(ep.format_score(self.shotValue)))
            textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
            awardLine1 = dmd.TextLayer(64, 15, self.game.assets.font_6px_az, "center", opaque=False).set_text(textString2)
            completeFrame = dmd.GroupedLayer(128,32,[border,pollyTitle,scoreLine,awardLine1,self.awardLine2b])
            transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
            # pause the train briefly
            self.delay(name="Pause Timer",delay=1.5,handler=self.pause_timer,param=True)


    # success
    def polly_saved(self):
        # this is mostly for the lights
        self.running = False
        self.game.train.stop()
        self.dispatch_delayed()
        # sound for this is self.game.assets.sfx_trainStop
        # play the train stopping animation and some sounds
        # TODO needs sounds
        anim = dmd.Animation().load(ep.DMD_PATH+'train-polly-on-tracks.dmd')
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # turn it on
        self.layer = animLayer
        # play the train stop noise
        self.game.sound.play(self.game.assets.sfx_trainStop)
        # set the delay for the award
        self.delay(delay=myWait,handler=self.give_award)

    def give_award(self):
        if self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
            # light extra ball if not maxxed out
            self.game.mine.light_extra_ball()
        else:
            # if maxxed out, give 5 million points instead
            self.game.score(5000000)
        # then after a delay, reset train
        self.polly_finished() # should delay this

    # fail
    def polly_died(self):
        # this is mostly for the lights
        self.running = False
        self.game.train.stop()
        self.dispatch_delayed()
        self.polly_finished()

    def polly_finished(self):
        # stop the polly music
        print "polly_finished IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # start up the main theme again if a second level mode isn't running
        if not self.game.show_tracking('stackLevel',1) and self.game.trough.num_balls_in_play != 0:
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        self.game.train.reset_toy()
        # turn off the polly display
        self.layer = None
        # set the tracking on the ramps
        # this is mostly for the lights
        self.game.set_tracking('centerRampStage',5)
        self.game.update_lamps()
        self.end_save_polly()

    # clean up and exit
    def end_save_polly(self):
        print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.set_tracking('stackLevel',False,1)
        # check to see if stampede is ready - if we're not ending due to ball fail
        if self.game.trough.num_balls_in_play != 0:
            self.game.base_game_mode.check_stampede()
        # unset the busy flag
        self.game.base_game_mode.busy = False
        # unload the mode
        self.unload()

    def mode_stopped(self):
        print "SAVE POLLY IS DISPATCHING DELAYS"
        self.dispatch_delayed()