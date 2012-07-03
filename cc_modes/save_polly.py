###
###
### Save Poor Polly from getting run over by the train!
###

from procgame import *
import cc_modes
import ep

class SavePolly(game.Mode):
    """BadGuys for great justice - covers Quickdraw, Showdown, and ... ? """
    def __init__(self,game,priority):
        super(SavePolly, self).__init__(game,priority)
        self.shotsToWin = self.game.user_settings['Gameplay (Feature)']['Shots to save Polly']
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


    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            if self.game.show_tracking("centerRampStage") == 99:
                self.game.train.stop()
                self.polly_finished()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        self.pause_train(True)

    def sw_rightJetBumper_active(self,sw):
        self.pause_train(True)

    def sw_bottomJetBumper_active(self,sw):
        self.pause_train(True)

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_400ms(self,sw):
        self.pause_train(True)

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        self.cancel_delayed("Pause Timer")
        self.in_progress()

    def sw_centerRampMake_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        # center ramp pauses the train
        self.game.sound.play(self.game.assets.sfx_trainWhistle)
        self.pause_train()
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        self.game.sound.play(self.game.assets.sfx_leftRampEnter)
        self.advance_save_polly()
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        # kill the mode timer until x
        self.cancel_delayed("Mode Timer")
        self.cancel_delayed("Pause Timer")
        self.game.sound.play(self.game.assets.sfx_thrownCoins)
        self.advance_save_polly()
        return game.SwitchStop

    def start_save_polly(self):
        # set the level 1 stack flag
        self.game.set_tracking('stackLevel',True,1)
        # clear any running music
        print "start_save_polly IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # set the ramps to crazy stage
        self.game.set_tracking('leftRampStage',99)
        self.game.set_tracking('rightRampStage',99)
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
        # jump into the mode loop
        self.in_progress()

    ## this is the main mode loop - not passing the time to the loop because it's global
    ## due to going in and out of pause
    def in_progress(self):
        print "POLLY IN PROGRESS"
        # start the train moving
        self.game.train.move()
        # setup the mode screen with the animated train
        # and all the text
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8)
        timeString = "TIME: " + str(self.modeTimer)
        timeLine = dmd.TextLayer(34, 25, self.game.assets.font_6px_az, "center", opaque=False).set_text(timeString)
        textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
        awardLine1 = dmd.TextLayer(34, 11, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)

        # stick together the animation and static text with the dynamic text
        composite = dmd.GroupedLayer(128,32,[self.trainLayer,self.pollyTitle,scoreLine,awardLine1,self.awardLine2,timeLine])
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
    def pause_train(self,advanced=False, time=5):
        print "PAUSE TRAIN"
        # stop the train from moving
        self.game.train.stop()
        if not advanced:
            # play the pause display
            self.game.sound.play(self.cows[0])
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
            self.in_progress()
        else:
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

            # if not, tick off one
            time -= 1
            # then reschedule 1 second later with the new time
            self.delay(name="Pause Timer",delay=1,handler=self.pause_timer,param=time)

        # for a side ramp hit
    def advance_save_polly(self):
        # add the sucessful shot
        self.shotsSoFar += 1
        if self.shotsSoFar >= self.shotsToWin:
            self.polly_saved()
        else:
            # score points
            self.game.score(500000)
            # TODO play some sound?
            # setup the display
            border = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'tracks-border.dmd').frames[0])
            pollyTitle = dmd.TextLayer(64, 0, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("POLLY PERIL")
            scoreLine = dmd.TextLayer(64, 6, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("500,000")
            textString2 = str((self.shotsToWin - self.shotsSoFar)) + " SHOTS FOR"
            awardLine1 = dmd.TextLayer(64, 15, self.game.assets.font_6px_az, "center", opaque=False).set_text(textString2)
            awardLine2 = dmd.TextLayer(64, 23, self.game.assets.font_7px_az, "center", opaque=False).set_text("EXTRA BALL LIT")
            completeFrame = dmd.GroupedLayer(128,32,[border,pollyTitle,scoreLine,awardLine1,awardLine2])
            transition = ep.EP_Transition(self,self.layer,completeFrame,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
            # pause the train briefly
            self.delay(name="Pause Timer",delay=1.5,handler=self.pause_timer,param=2)


    # success
    def polly_saved(self):
        self.game.train.stop()
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
        self.game.train.stop()
        self.polly_finished()

    def polly_finished(self):
        # stop the polly music
        print "polly_finished IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # turn the main game music back on if showdown isn't running
        if self.game.show_tracking('showdownStatus') != "RUNNING":
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        self.game.train.reset_toy()
        # turn off the polly display
        self.layer = None
        # set the tracking on the ramps
        # this is mostly for the lights
        self.game.set_tracking('leftRampStage',5)
        self.game.set_tracking('rightRampStage',5)
        self.game.set_tracking('centerRampStage',5)
        self.game.update_lamps()
        self.end_save_polly()

    # clean up and exit
    def end_save_polly(self):
        print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.set_tracking('stackLevel',False,1)
        # check to see if stampede is ready
        self.game.base_game_mode.check_stampede()
        # unload the mode
        self.game.modes.remove(self.game.save_polly)

    def clear_layer(self):
        self.layer = None

    def mode_stopped(self):
        print "SAVE POLLY IS DISPATCHING DELAYS"
        self.dispatch_delayed()