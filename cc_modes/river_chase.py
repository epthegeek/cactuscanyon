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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
###
###
### Save Poor Polly from getting run over by the train!
###

from procgame import *
import cc_modes
import ep

class RiverChase(ep.EP_Mode):
    """Polly Peril - Rescue on the River"""
    def __init__(self,game,priority):
        super(RiverChase, self).__init__(game,priority)
        self.shotsToWin = self.game.user_settings['Gameplay (Feature)']['Save Polly Shots - River']
        self.shotsSoFar = 0
        self.running = False
        self.halted = False
        self.won = False
        self.distance_value = int(30.0 / self.shotsToWin)
    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add')
        self.game.peril = True
        self.modeTimer = 0
        self.shotsSoFar = 0
        # position for the horse
        self.x_pos = 6
        # point value for shots
        self.shotValue = 100000
        # movement distance value
        self.distance = 0
        self.banner = False
        self.won = False

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
                self.polly_died()


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

    def process_shot(self):
        # combos
        if self.game.combos.myTimer > 0:
        # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()

        # count the shot
        self.shotsSoFar += 1
        if self.shotsSoFar == self.shotsToWin:
            # winner winner, chicken dinner
            self.polly_saved()
        else:
            # set the banner flag
            self.banner = True
            # score points
            self.game.score(self.shotValue)
            # set the distance to move
            print "MOVING HORSE " + str(self.distance_value)
            self.distance += self.distance_value

    def start_river_chase(self,step=1):
        if step == 1:
            # set the level 1 stack flag
            self.game.set_tracking('stackLevel',True,2)
            # set the running flag
            self.running = True
            # clear any running music
            print "start_river_chase IS KILLING THE MUSIC"
            self.game.sound.stop_music()
            self.game.right_ramp.update_lamps()
            self.game.center_ramp.update_lamps()
            self.game.left_ramp.update_lamps()
            self.game.saloon.update_lamps()


            # start the music
            self.game.base.music_on(self.game.assets.music_pollyPeril)
            # run the animation
            anim = self.game.assets.dmd_pollyIntro
            myWait = len(anim.frames) / 30
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
            self.layer = animLayer

            # set the timer for the mode
            self.modeTimer = 30
            # loop back for the title card
            self.delay(delay=myWait,handler=self.start_river_chase,param=2)
        if step == 2:
            # set up the title card
            titleCard = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_rotrTitle.frames[0])
            # transition to the title card
            self.transition = ep.EP_Transition(self,self.layer,titleCard,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_EAST)
            # delay the start process
            self.delay("Get Going",delay=2,handler=self.in_progress)
            self.delay(delay=2,handler=self.game.base.play_quote,param=self.game.assets.quote_rotrIntro)

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
                print "I SHOULD DO THE BANNER MON"
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
                    self.delay(name="Mode Timer",delay=0.1,handler=self.in_progress)

    def halt(self):
        print "HALTING -- BUMPERS/MINE/SALOON"
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # this is the initial delay - have to include it in case of a straight shot to the mine off the ramp
        self.cancel_delayed("Get Going")
        # set the flag
        self.halted = True
        textString = "< SAVE POLLY PAUSED >"
        self.layer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)


    # success
    def polly_saved(self):
        self.game.score(500000)
        self.running = False
        self.dispatch_delayed()
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        self.won = True
        self.win_display()

    # fail
    def polly_died(self):
        self.running = False
        self.dispatch_delayed()
        self.end_river_chase()

    def win_display(self,step=1):
        if step == 1:
            self.game.base.play_quote(self.game.assets.quote_victory)
            # frame layer of the dead guy
            self.layer = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_ourHero.frames[0])
            self.delay("Display",delay=0.5,handler=self.win_display,param=2)
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
            self.delay("Display",delay=myWait,handler=self.win_display,param=3)
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
            self.delay("Display",delay=myWait,handler=self.win_display,param=4)
        if step == 4:
            # saved banner goes here
            awardTextString = "POLLY SAVED"
            awardScoreString = "500,000"
            # combine them
            completeFrame = self.build_display(awardTextString,awardScoreString)
             # swap in the new layer
            self.layer = completeFrame
            self.delay(name="Display",delay=2,handler=self.end_river_chase)
            # show combo display if the chain is high enough
            if self.game.combos.chain > 1:
                self.delay(name="Display",delay=2,handler=self.game.combos.display)

    def build_display(self,awardTextString,awardScoreString):
    # create the two text lines
        print "BUILDING DISPLAY"
        awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        # if blink frames we have to set them
        awardTextTop.set_text(awardTextString)
        awardTextBottom.set_text(awardScoreString)
        # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.game.left_ramp.border,awardTextTop,awardTextBottom])
        return completeFrame

    def hit_banner(self):
        print "HIT BANNER GOES HERE"
        # turn off the banner flag
        self.banner = False
        # cancel the mode timer during the display
        self.cancel_delayed("Mode Timer")
        shotsLeftText = str(self.shotsToWin - self.shotsSoFar) + " MORE TO GO"
        display = self.build_display(shotsLeftText,"100,000")
        transition = ep.EP_Transition(self,self.layer,display,ep.EP_Transition.TYPE_CROSSFADE)
        self.delay("Display",delay=1.5,handler=self.in_progress)

    def end_river_chase(self):
        # stop the polly music
        print "end_river_chase IS KILLING THE MUSIC"
        # only kill the music if there's not a higher level running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        self.layer = None
        # set the tracking on the ramps
        self.game.set_tracking('leftRampStage',5)
        self.game.update_lamps()
        self.end_save_polly()

    # clean up and exit
    def end_save_polly(self):
        print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.set_tracking('stackLevel',False,2)
        # check to see if stampede is ready - if we're not ending due to ball fail
        if self.game.trough.num_balls_in_play != 0:
            self.game.base.check_stampede()
            # unset the busy flag
        self.game.base.busy = False
        # turn the music back on
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.base.music_on(self.game.assets.music_mainTheme)
        self.game.peril = False
        # remove the switch blocker
        self.game.switch_blocker('remove')
        # unload the mode
        self.unload()


    def abort_display(self):
        # if we're done, we should quit
        if self.shotsToWin == self.shotsSoFar:
            self.end_river_chase()
        self.cancel_delayed("Display")
        self.layer = None
