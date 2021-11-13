#   ____           _                ____
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

from procgame import dmd,game
import ep
import random

class RiverChase(ep.EP_Mode):
    """Polly Peril - Rescue on the River"""
    def __init__(self,game,priority):
        super(RiverChase, self).__init__(game,priority)
        self.myID = "River Chase"
        self.shotsToWin = self.game.user_settings['Gameplay (Feature)']['Save Polly Shots - River']
        self.shotsSoFar = 0
        self.running = False
        self.halted = False
        self.won = False
        self.distance_value = int(30.0 / self.shotsToWin)
        self.valueMultiplier = 1 # shot value multiplier

        script = []
        # set up the text layer
        textString = "< SAVE POLLY PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.BLUE)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"
        self.keys_index = {'start':list(range(len(self.game.sound.sounds[self.game.assets.quote_rotrIntro])))}
        self.counts_index = {'start':0}
        random.shuffle(self.keys_index['start'])

    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add',self.myID)
        self.game.peril = True
        self.shotsSoFar = 0
        self.running = False
        self.halted = False
        self.won = False
        self.distance_value = int(30.0 / self.shotsToWin)
        self.totalPoints = 0 # holder for total points for the mode earned
        self.valueMultiplier = 1 # shot value multiplier
        self.extendedCount = 0
        self.gotPaused = False # was the mode paused at any point
        self.lastPoints = 0
        self.winMultiplier = 3
        self.winBonus = 0

        # position for the horse
        self.x_pos = 6
        # point value for shots
        self.shotValue = 100000
        # movement distance value
        self.distance = 0
        self.banner = False
        self.won = False
        # set the timer
        self.modeTimer = self.game.user_settings['Gameplay (Feature)']['Save Polly Timer - River']
        self.modeTimer += 1

        # set up the layers
        anim = self.game.assets.dmd_blankRiverLoop
        self.backdrop = dmd.AnimatedLayer(frames=anim.frames, repeat=True, opaque=True,frame_time=6)
        anim = self.game.assets.dmd_horseLoop
        self.horse = dmd.AnimatedLayer(frames=anim.frames,repeat=True, frame_time = 6)
        self.horse.composite_op = "blacksrc"
        anim = self.game.assets.dmd_rowboatLoop
        self.boat = dmd.AnimatedLayer(frames=anim.frames,repeat = True,frame_time = 6)
        self.boat.composite_op = "blacksrc"

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0:
            if self.running:
                self.game.base.busy = True
                self.game.base.queued += 1
                self.polly_died(drain=True)


    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_390ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_active_for_290ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.in_progress()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.in_progress()

    def sw_centerRampMake_active(self,sw):
        if self.running:
            self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
            self.process_shot()

    def sw_leftRampEnter_active(self,sw):
        if self.running:
            self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
            self.process_shot()

    def sw_rightRampMake_active(self,sw):
        if self.running:
            self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
            self.process_shot()

    def sw_leftRampMake_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_horse)

    def sw_rightRampBottom_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_horse)

    # quickdraw switch bits
    def sw_topLeftStandUp_active(self,sw):
        self.add_time()
        return game.SwitchStop
    def sw_bottomLeftStandUp_active(self,sw):
        self.add_time()
        return game.SwitchStop
    def sw_topRightStandUp_active(self,sw):
        self.add_time()
        return game.SwitchStop
    def sw_bottomRightStandUp_active(self,sw):
        self.add_time()
        return game.SwitchStop

    def process_shot(self):
        # count the shot
        self.shotsSoFar += 1
        if self.shotsSoFar >= self.shotsToWin and not self.won:
            # winner winner, chicken dinner
            self.polly_saved()
            # this has to be reset or the display abort screws with stuff later
            self.shotsSoFar = 0
        elif self.won:
            pass
        else:
            # set the banner flag
            self.banner = True
            self.cancel_delayed("Multiplier")
            # score points
            points = self.shotValue * self.valueMultiplier
            self.game.score(points)
            #print "SCORING POINTS " + str(points) + " Multiplier " + str(self.valueMultiplier)
            # add the points to the total
            self.totalPoints += points
            # save the last points for the display
            self.lastPoints = points
            #print "LAST POINTS VALUE " + str(self.lastPoints)
            # nudge the multiplier
            self.raise_multiplier()
            # increase the shot value .... for the fuck of it
            self.shotValue += 50000
            # set the distance to move
            #print "MOVING HORSE " + str(self.distance_value)
            self.distance += self.distance_value

    def raise_multiplier(self):
        # raise the multiplier value by 1
        self.valueMultiplier += 1
        #print "RAISING MULTIPLIER OVER HERE - now it's " + str(self.valueMultiplier)
        # update the lamps
        self.lamp_update()
        #print "River chase - UPDATING THE LAMPS"
        # set the delay to reset the timer
        self.delay("Multiplier",delay=3,handler=self.reset_multiplier)

    def reset_multiplier(self):
        self.valueMultiplier = 1
        self.lamp_update()

    def start_river_chase(self,step=1):
        if step == 1:
            # audit
            self.game.game_data['Feature']['Left Polly Started'] += 1
            # set the level 1 stack flag
            self.game.stack_level(2,True)

            # set the running flag
            self.running = True
            # clear any running music
            #self.stop_music()
            self.lamp_update()
            ## TEMP PLAY INTRO
            duration = self.game.base.priority_quote(self.game.assets.quote_rotrDox)
            ## secondary intro clip
            self.delay("Operational",delay=duration+0.1,handler=lambda: self.play_ordered_quote(self.game.assets.quote_rotrIntro,'start'))


        # start the music
            self.music_on(self.game.assets.music_altPeril)
            # run the animation
            anim = self.game.assets.dmd_pollyIntro
            myWait = len(anim.frames) / 30
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
            self.layer = animLayer

            # loop back for the title card
            self.delay("Operational",delay=myWait,handler=self.start_river_chase,param=2)
        if step == 2:
            # set up the title card
            titleCard = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_rotrTitle.frames[0])
            # transition to the title card
            self.transition = ep.EP_Transition(self,self.layer,titleCard,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_EAST)
            # delay the start process
            self.delay("Get Going",delay=2,handler=self.in_progress)

    ## this is the main mode loop - not passing the time to the loop because it's global
    ## due to going in and out of pause
    def in_progress(self):
        if self.running:
            # and all the text
            p = self.game.current_player()
            scoreString = ep.format_score(p.score)
            scoreLine = dmd.TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8)
            timeString = "TIME: " + str(int(self.modeTimer))
            self.timeLine = dmd.TextLayer(128,26, self.game.assets.font_5px_AZ, "right", opaque=False).set_text(timeString)

            # moving the horse
            if self.distance > 0:
                # change the x_position
                self.x_pos -= 2
                # tick down the distance
                self.distance -= 1
            if self.banner and self.distance == 0:
                #print "I SHOULD DO THE BANNER MON"
                self.hit_banner()
            else:
                # set the horse layer position
                self.horse.set_target_position(self.x_pos,0)
                # stick together the animation and static text with the dynamic text
                composite = dmd.GroupedLayer(128,32,[self.backdrop,self.horse,self.boat,self.timeLine])
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

    def halt(self):
        #print "HALTING -- BUMPERS/MINE/SALOON"
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # this is the initial delay - have to include it in case of a straight shot to the mine off the ramp
        self.cancel_delayed("Get Going")
        # set the flag
        self.halted = True
        # flag the penalty for using pause
        self.gotPaused = True
        self.layer = self.pauseView

    def add_time(self):
        # add to the time if we haven't hit the max
        if self.extendedCount < 4:
            # increase the timer by 4 seconds
            self.modeTimer += 4
            # play a sound
            self.game.sound.play(self.game.assets.sfx_quickdrawOff)
            # score some points
            self.game.score(3750)
            # increment the extendedCount
            self.extendedCount += 1
        else:
            # play a thunk
            self.game.sound.play(self.game.assets.sfx_quickdrawOn)
            # score some points
            self.game.score(3750)

    # success
    def polly_saved(self):
        # audit
        self.game.game_data['Feature']['Left Polly Won'] += 1
        self.game.peril = False
        #self.game.score(500000)
        # score the shot value x the current multiplier
        points = self.shotValue * self.valueMultiplier
        # add the points to the total
        self.totalPoints += points
        # score the 3rd hit points
        self.game.score(points)
        # immediately calculate and score the win bonus - in case the end stuff gets interrupted
        # if the timer was paused at all, remove one multiplier
        if self.gotPaused:
            self.winMultiplier -= 1
            # if extra time was added, remove one multiplier
        if self.extendedCount > 0:
            self.winMultiplier -=1
            # mode bonus is total points x remaining multiplier
        self.winBonus = self.totalPoints * self.winMultiplier
        # score those points, pronto
        self.game.score(self.winBonus)

        # set the left ramp value up
        self.game.set_tracking('leftRampValue',20000)
        self.running = False
        self.wipe_delays()
        #self.stop_music(slice=3)
        self.won = True
        # kill the lights on the three ramps
        self.game.lamp_control.left_ramp('Base')
        self.game.lamp_control.center_ramp('Base')
        self.game.lamp_control.right_ramp('Base')
        self.win_display()

    # fail
    def polly_died(self, drain=False):
        self.game.peril = False
        self.running = False
        self.wipe_delays()
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
        self.delay("Operational", delay=1.5, handler=self.end_river_chase)

    def win_display(self,step=1):
        if step == 1:
            self.game.base.priority_quote(self.game.assets.quote_victory)
            # frame layer of the dead guy
            self.layer = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_ourHero.frames[0])
            self.delay("Win Display",delay=0.5,handler=self.win_display,param=2)
        if step == 2:
            # the pan up
            anim = self.game.assets.dmd_ourHero
            # math out the wait
            myWait = len(anim.frames) / 60.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=1)
            # turn it on
            self.layer = animLayer
            # loop back for the finish animation
            self.delay("Win Display",delay=myWait,handler=self.win_display,param=3)
        if step == 3:
            anim = self.game.assets.dmd_pollyVictory
            myWait = len(anim.frames) / 8.57
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 7
            animLayer.opaque = True

            animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_blow)
            animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_grinDing)
            # play animation
            self.layer = animLayer
            self.delay("Win Display",delay=myWait,handler=self.win_display,param=4)
        if step == 4:
            # saved banner goes here
            awardTextString = "POLLY SAVED BONUS"
            # set the display string with commas
            awardScoreString = str(ep.format_score(self.winBonus))
            # combine them
            completeFrame = self.build_display(awardTextString,awardScoreString)
            stackLevel = self.game.show_tracking('stackLevel')
            # if something higher is running, throw the win display in a cut in
            if True in stackLevel[3:]:
                self.game.interrupter.cut_in(completeFrame,1)
            else:
                # swap in the new layer
                self.layer = completeFrame
            self.delay(name="Operational",delay=2,handler=self.end_river_chase)
            # show combo display if the chain is high enough
            if self.game.combos.chain > 1:
                self.delay(name="Display",delay=2,handler=self.game.combos.display)

    def build_display(self,awardTextString,awardScoreString):
    # create the two text lines
        #print "BUILDING DISPLAY"
        #print "Award Text/ScoreString " + str(awardTextString) + "/" + str(awardScoreString)
        awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        awardTextTop.set_text(awardTextString,color=ep.BLUE)
        awardTextBottom.set_text(awardScoreString,color=ep.CYAN)
        # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.game.left_ramp.border,awardTextTop,awardTextBottom])
        return completeFrame

    def hit_banner(self):
        #print "HIT BANNER GOES HERE"
        # turn off the banner flag
        self.banner = False
        # cancel the mode timer during the display
        self.cancel_delayed("Mode Timer")
        shotsLeftText = str(self.shotsToWin - self.shotsSoFar) + " MORE TO GO"
        display = self.build_display(shotsLeftText,str(ep.format_score(self.lastPoints)))
        transition = ep.EP_Transition(self,self.layer,display,ep.EP_Transition.TYPE_CROSSFADE)
        self.delay("Display",delay=1.5,handler=self.in_progress)

    def end_river_chase(self):
        # only kill the music if there's not a higher level running
        #self.stop_music(slice=3)
        self.layer = None
        # up the stampede value if won
        if self.won:
            self.game.increase_tracking('Stampede Addon',250000)
        # set the tracking on the ramps
        if self.game.save_polly.winsRequired and not self.won:
            self.game.set_tracking('leftRampStage',1)
        # if wins are not required then the ramp goes to 'done' even if lost
        else:
            self.game.set_tracking('leftRampStage',5)
        self.shotsSoFar = 0
        self.lamp_update()
        self.end_save_polly()

    def tilted(self):
        if self.running:
        # set the tracking on the ramps
            if self.game.save_polly.winsRequired and not self.won:
                self.game.set_tracking('leftRampStage',1)
            # if wins are not required then the ramp goes to 'done' even if lost
            else:
                self.game.set_tracking('leftRampStage',5)
        self.running = False
        # then unload
        self.unload()

    # clean up and exit
    def end_save_polly(self):
        #print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.stack_level(2,False)
        # check to see if stampede is ready - if we're not ending due to ball fail
        if self.game.trough.num_balls_in_play >= 0:
            self.game.base.check_stampede()
            # turn the music back on
            self.music_on(self.game.assets.music_mainTheme,mySlice=3)
        # remove the switch blocker
        self.game.switch_blocker('remove',self.myID)
        # unset the busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload the mode
        self.unload()


    def abort_display(self):
        # if we're done, we should quit
        if self.shotsSoFar >= self.shotsToWin and self.running:
            self.running = False
            self.end_river_chase()
        self.cancel_delayed("Display")
        self.layer = None
