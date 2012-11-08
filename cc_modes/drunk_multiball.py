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
## The Drunk Multiball
##

## basic gist
## inverted flippers
## hitting the beer mug lights jackpots
## after collecting jackpots, or maybe after all 5 are lit, shooting the saloon should do something

from procgame import dmd,game
import ep
import random

class DrunkMultiball(ep.EP_Mode):
    """Drunk multiball mode ... """
    def __init__(self,game,priority):
        super(DrunkMultiball, self).__init__(game,priority)
        anim = self.game.assets.dmd_dmbIdle
        self.overlay = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=8)
        self.shotModes = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.shots = ['leftLoopStage','leftRampStage','centerRampStage','rightLoopStage','rightRampStage']
        self.availableJackpots = ['leftLoop','leftRamp','centerRamp','rightLoop','rightRamp']
        # an animation for use in the intro
        anim = self.game.assets.dmd_reverse
        self.underLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)

    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add')
        # reset the jackpots
        self.active = []

    def ball_drained(self):
        # if we're dropping down to one ball, and drunk multiball is running - do stuff
        if self.game.trough.num_balls_in_play == 1 and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.end_save()
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.game.base.busy = True
            self.game.base.queued += 1
            self.end_drunk()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        self.process_shot('leftLoop',self.shotModes[0])

    def sw_leftRampEnter_active(self, sw):
        self.process_shot('leftRamp',self.shotModes[2])

    def sw_centerRampMake_active(self, sw):
        self.process_shot('centerRamp',self.shotModes[3])

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            self.process_shot('rightLoop',self.shotModes[1])

    def sw_rightRampMake_active(self, sw):
        self.process_shot('rightRamp',self.shotModes[4])

    def process_shot(self,shot,mode):
        if shot in self.active:
            self.collect_jackpot(shot,mode)
        else:
            self.game.score(2530)

    # beer mug lights jackpots
    def sw_beerMug_active(self,sw):
        if self.availableJackpots:
            self.light_jackpot()
        else:
            pass
        return game.SwitchStop

    # if it lands in the mine, just kick it out
    def sw_minePopper_active_for_390ms(self,sw):
        self.game.score(2530)


    def start_drunk(self):
        print "STARTING DRUNK ASS MULTIBALL"
        self.running = True
        # set the stack level
        self.game.stack_level(3,True)
        # update the tracking
        self.game.set_tracking('drunkMultiballStatus', "RUNNING")
        # update the lamps
        self.game.saloon.update_lamps()
        # disable the flippers
        self.game.enable_flippers(False)
        # enable the inverted flippers
        self.game.enable_inverted_flippers(True)
        # stop the music
        self.game.sound.stop_music()
        # turn the GI off
        self.game.gi_control("OFF")
        # update the lamps
        for mode in self.shotModes:
            mode.update_lamps()
        # play the drunk multiball song
        self.game.base.music_on(self.game.assets.music_drunkMultiball)
        # show some screens about the mode
        self.banner()

    def banner(self):
        # setup the pour mask
        # load up the animation
        anim = self.game.assets.dmd_pourMask
        # setup the animated layer
        pour = ep.EP_AnimatedLayer(anim)
        pour.hold=True
        pour.frame_time = 6
        pour.composite_op = "blacksrc"

        mug = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_beerMug1.frames[0])
        mug.composite_op = "blacksrc"
        words = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_drunkMultiball.frames[0])
        combined = dmd.GroupedLayer(128,32,[words,pour,mug])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_pour)
        self.delay(delay=1.3,handler=self.bannerTwo)

    def bannerTwo(self):
        self.game.base.play_quote(self.game.assets.quote_drunkDrinkToThat)
        mug = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_beerMug1.frames[0])
        mug.composite_op = "blacksrc"
        words = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_drunkMultiball.frames[0])
        combined = dmd.GroupedLayer(128,32,[words,mug])
        self.layer = combined
        self.delay(delay=1,handler=self.intro_display)

    def intro_display(self,step=1):
        ## show some junk about how the mode works
        if step == 1:
            flippers = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers1.frames[0])
            arrow = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers1.frames[0])
        elif step == 2 or step == 4 or step == 6 or step == 8 or step == 10:
            flippers = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers2.frames[0])
            arrowOne = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_rightArrow1.frames[0])
            arrowTwo = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_rightArrow2.frames[0])
            arrowThree = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_rightArrow3.frames[0])
            arrow = dmd.ScriptedLayer(128,32,[{'seconds':0.15,'layer':arrowOne},{'seconds':0.15,'layer':arrowTwo},{'seconds':0.15,'layer':arrowThree}])
            arrow.composite_op = "blacksrc"
        elif step == 3 or step == 5 or step == 7 or step == 9:
            flippers = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers3.frames[0])
            arrowOne = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_leftArrow1.frames[0])
            arrowTwo = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_leftArrow2.frames[0])
            arrowThree = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_leftArrow3.frames[0])
            arrow = dmd.ScriptedLayer(128,32,[{'seconds':0.15,'layer':arrowOne},{'seconds':0.15,'layer':arrowTwo},{'seconds':0.15,'layer':arrowThree}])
            arrow.composite_op = "blacksrc"
        else:
            # just to make the syntax checking happy
            flippers = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers1.frames[0])
            arrow = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_flippers1.frames[0])

        flippers.composite_op = "blacksrc"

        text = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_reverse.frames[0])

        if step == 2:
            self.game.base.play_quote(self.game.assets.quote_drunkNeverSeen)
        if step == 1:
            combined = dmd.GroupedLayer(128,32,[text,flippers])
        elif step == 2 or step == 3:
            combined = dmd.GroupedLayer(128,32,[text,flippers,arrow])
        else:
            combined = dmd.GroupedLayer(128,32,[self.underLayer,flippers,arrow])
        self.layer=combined
        if step <= 5:
            self.delay(delay=1,handler=self.intro_display,param=step+1)
        else:
            self.delay(delay=1,handler=self.get_going)

    def get_going(self):
        # turn off the saloon busy flag - should process check bounty and kick the ball out
        self.game.saloon.busy = False
        # eject more ball
        if self.game.trough.num_balls_in_play < 3:
            thisMany = 3 - self.game.trough.num_balls_in_play
            self.game.trough.balls_to_autoplunge = thisMany
            self.game.trough.launch_balls(thisMany)
        # eject the ball in the saloon
        self.game.saloon.kick()
        # start a ball save
        self.game.ball_save.start(num_balls_to_save=3, time=20, now=True, allow_multiple_saves=True)
        #self.delay(delay=2,handler=self.dmb_ball_save)
        self.update_display()

    def dmb_ball_save(self):
    # start a ball save
        self.game.ball_save.start(num_balls_to_save=3, time=20, now=True, allow_multiple_saves=True)

    def update_display(self):
        self.overlay.composite_op = "blacksrc"
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(80, 8, self.game.assets.font_7px_score, "center", opaque=False).set_text(scoreString,blink_frames=8)
        textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("DRUNK MULTIBALL")
        if self.active:
            textLine2 = dmd.TextLayer(80, 18, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOTS")
            textLine3 = dmd.TextLayer(80, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("WORTH 5,000,000")
        else:
            textLine2 = dmd.TextLayer(80, 18, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("HIT BEER MUG")
            textLine3 = dmd.TextLayer(80, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("TO LIGHT JACKPOTS")
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,scoreLine,self.overlay])
        self.layer = combined
        self.delay(name="Display",delay=0.2,handler=self.update_display)

    def light_jackpot(self):
        # pick a jackpot
        thisOne = random.choice(self.availableJackpots)
        # take it out of the available and make it active
        self.availableJackpots.remove(thisOne)
        self.active.append(thisOne)
        print self.active
        # and update the lamps
        for mode in self.shotModes:
            mode.update_lamps()

        print "LIGHTING JACKPOT"
        anim = self.game.assets.dmd_dmb
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 8
        animLayer.composite_op = "blacksrc"
        animLayer.add_frame_listener(3,self.game.sound.play,param=self.game.assets.sfx_ebDrink)
        animLayer.add_frame_listener(5,self.game.sound.play,param=self.game.assets.sfx_ebDrink)
        animLayer.opaque=False

        words = self.game.assets.dmd_dmbJackpotAdded
        myWait = len(words.frames) / 10.0
        wordsLayer = ep.EP_AnimatedLayer(words)
        wordsLayer.add_frame_listener(6,self.game.sound.play,param=self.game.assets.sfx_orchestraSet)
        wordsLayer.hold=True
        wordsLayer.frame_time = 6
        wordsLayer.opaque = True

        combined = dmd.GroupedLayer(128,32,[wordsLayer,animLayer])
        self.cancel_delayed("Display")
        self.layer = combined
        self.delay(name="Display",delay=myWait,handler=self.update_display)

    def collect_jackpot(self,shot,mode):
        # take it out of active and put it in  available
        self.active.remove(shot)
        self.availableJackpots.append(shot)
        # update the lamps for the hit ramp
        mode.update_lamps()
        # flash some lights
        self.game.lamps.gi01.schedule(0xFF00FF00,cycle_seconds=1)
        self.game.lamps.gi02.schedule(0x0FF00FF0,cycle_seconds=1)
        self.game.lamps.gi03.schedule(0x00FF00FF,cycle_seconds=1)

        # score some points
        self.game.score(5000000)
        # load up the animation
        anim = self.game.assets.dmd_beerSlide
        # setup the animated layer
        beerLayer = ep.EP_AnimatedLayer(anim)
        beerLayer.hold=True
        beerLayer.frame_time = 3
        beerLayer.composite_op = "blacksrc"

        anim = self.game.assets.dmd_dmbJackpot
        # setup the animated layer
        wordsLayer = ep.EP_AnimatedLayer(anim)
        wordsLayer.hold=True
        wordsLayer.frame_time = 3
        wordsLayer.composite_op = "blacksrc"

        if self.layer == None:
            self.layer = self.no_layer()

        combined = dmd.GroupedLayer(128,32,[self.layer,wordsLayer,beerLayer])
        self.cancel_delayed("Display")
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_slide)
        self.game.base.play_quote(self.game.assets.quote_drunkJackpot)
        self.delay(name="Display",delay=1.5,handler=self.jackpot_score)

    def jackpot_score(self):
        self.game.sound.play(self.game.assets.sfx_orchestraSpike)
        scoreString = "5,000,000*"
        scoreLine = dmd.TextLayer(64, 8, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text(scoreString)
        scoreLine.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dmbJackpot.frames[17])
        combined = dmd.GroupedLayer(128,32,[backdrop,scoreLine])
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.update_display)

    def end_save(self):
        # a ball saver to allow for reacclimation
        self.game.ball_save.start(num_balls_to_save=1, time=8, now=True, allow_multiple_saves=False)
        self.end_drunk()

    def end_drunk(self):
        print "ENDING DRUNK MULTIBALL"
        self.running = False
        self.wipe_delays()
        self.clear_layer()
        # update the tracking
        self.game.set_tracking('drunkMultiballStatus', "OPEN")
        # reset the flippers
        self.game.enable_inverted_flippers(False)
        self.game.enable_flippers(True)
        # reset the lamps
        for mode in self.shotModes:
            mode.update_lamps()
        # clear the layer
        self.layer = None
        # turn the GI back on
        self.game.gi_control("ON")
        # reset the mug hits for next time
        self.game.set_tracking('beerMugHits',0)
        # set the stack flag back off
        self.game.stack_level(3,False)
        stackLevel = self.game.show_tracking('stackLevel')
        # stop the music if there isn't a higher mode running
        if True not in stackLevel[4:]:
            self.game.sound.stop_music()
            # tick up the shots needed for next time
            self.game.base.music_on(self.game.assets.music_mainTheme)
        self.game.base.mug_shots += 3
        # remove the switch blocker
        self.game.switch_blocker('remove')
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload the mode
        self.unload()


