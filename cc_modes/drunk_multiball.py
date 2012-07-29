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
##
## The Drunk Multiball
##

## basic gist
## inverted flippers
## hitting the beer mug lights jackpots
## after collecting jackpots, or maybe after all 5 are lit, shooting the saloon should do something

from procgame import *
import cc_modes
import ep
import random

class DrunkMultiball(ep.EP_Mode):
    """Mining for great justice - For the Gold Mine Multiball, and ... ? """
    def __init__(self,game,priority):
        super(DrunkMultiball, self).__init__(game,priority)
        anim = dmd.Animation().load(ep.DMD_PATH+'dmb-idle.dmd')
        self.overlay = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=8)
        self.shotModes = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.shots = ['leftLoopStage','leftRampStage','centerRampStage','rightLoopStage','rightRampStage']
        self.availableJackpots = ['leftLoop','leftRamp','centerRamp','rightLoop','rightRamp']
        self.active = []
        # an animation for use in the intro
        anim = dmd.Animation().load(ep.DMD_PATH+'reverse.dmd')
        self.underLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)


    def ball_drained(self):
        # if we're dropping down to one ball, and drunk multiball is running - do stuff
        if self.game.trough.num_balls_in_play == 1 and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.end_save()
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.end_drunk()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        self.process_shot('leftLoop',self.shotModes[0])
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot('leftRamp',self.shotModes[2])
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot('centerRamp',self.shotModes[3])
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            self.process_shot('rightLoop',self.shotModes[1])
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot('rightRamp',self.shotModes[4])
        return game.SwitchStop

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

    def start_drunk(self):
        print "STARTING DRUNK ASS MULTIBALL"
        # set the stack level
        self.game.set_tracking('stackLevel',True,1)
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
        self.game.base_game_mode.music_on(self.game.assets.music_drunkMultiball)
        # show some screens about the mode
        self.banner()

    def banner(self):
        # setup the pour mask
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'pour-mask.dmd')
        # setup the animated layer
        pour = ep.EP_AnimatedLayer(anim)
        pour.hold=True
        pour.frame_time = 6
        pour.composite_op = "blacksrc"

        mug = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'beer-mug-1.dmd').frames[0])
        mug.composite_op = "blacksrc"
        words = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'drunk-multiball.dmd').frames[0])
        combined = dmd.GroupedLayer(128,32,[words,pour,mug])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_pour)
        self.delay(delay=1.3,handler=self.bannerTwo)

    def bannerTwo(self):
        self.game.sound.play(self.game.assets.quote_drunkDrinkToThat)
        mug = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'beer-mug-1.dmd').frames[0])
        mug.composite_op = "blacksrc"
        words = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'drunk-multiball.dmd').frames[0])
        combined = dmd.GroupedLayer(128,32,[words,mug])
        self.layer = combined
        self.delay(delay=1,handler=self.intro_display)

    def intro_display(self,step=1):
        ## show some junk about how the mode works
        if step == 1:
            flippers = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'flippers1.dmd').frames[0])
        elif step == 2 or step == 4 or step == 6 or step == 8 or step == 10:
            flippers = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'flippers2.dmd').frames[0])
            arrowOne = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'right-arrow-1.dmd').frames[0])
            arrowTwo = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'right-arrow-2.dmd').frames[0])
            arrowThree = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'right-arrow-3.dmd').frames[0])
            arrow = dmd.ScriptedLayer(128,32,[{'seconds':0.15,'layer':arrowOne},{'seconds':0.15,'layer':arrowTwo},{'seconds':0.15,'layer':arrowThree}])
            arrow.composite_op = "blacksrc"
        elif step == 3 or step == 5 or step == 7 or step == 9:
            flippers = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'flippers3.dmd').frames[0])
            arrowOne = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'left-arrow-1.dmd').frames[0])
            arrowTwo = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'left-arrow-2.dmd').frames[0])
            arrowThree = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'left-arrow-3.dmd').frames[0])
            arrow = dmd.ScriptedLayer(128,32,[{'seconds':0.15,'layer':arrowOne},{'seconds':0.15,'layer':arrowTwo},{'seconds':0.15,'layer':arrowThree}])
            arrow.composite_op = "blacksrc"

        flippers.composite_op = "blacksrc"

        text = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'reverse.dmd').frames[0])

        if step == 2:
            self.game.sound.play(self.game.assets.quote_drunkNeverSeen)
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
        # start a ball save
        self.game.ball_save.start(num_balls_to_save=3, time=20, now=True, allow_multiple_saves=True)
        self.update_display()

    def update_display(self):
        self.overlay.composite_op = "blacksrc"
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(80, 8, self.game.assets.font_7px_score, "center", opaque=False).set_text(scoreString,blink_frames=8)
        textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("DRUNK MULTIBALL")
        if self.active:
            textLine2 = dmd.TextLayer(80, 18, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOTS")
            textLine3 = dmd.TextLayer(80, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("WORTH 500,000")
        else:
            textLine2 = dmd.TextLayer(80, 18, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("HIT BEER MUG")
            textLine3 = dmd.TextLayer(80, 25, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("TO LIGHT JACKPOTS")
        combined = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,scoreLine,self.overlay])
        self.layer = combined
        self.delay(name="Display",delay=0.2,handler=self.update_display)

    def light_jackpot(self):
        # TODO add handling for all jackpots lit !
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
        anim = dmd.Animation().load(ep.DMD_PATH+'dmb.dmd')
        #myWait = len(anim.frames) / 7.5
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 8
        animLayer.composite_op = "blacksrc"
        animLayer.add_frame_listener(3,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
        animLayer.add_frame_listener(5,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
        animLayer.opaque=False

        words = dmd.Animation().load(ep.DMD_PATH+'jackpot-added.dmd')
        myWait = len(words.frames) / 10.0
        wordsLayer = ep.EP_AnimatedLayer(words)
        wordsLayer.add_frame_listener(6,self.game.play_remote_sound,param=self.game.assets.sfx_orchestraSet)
        wordsLayer.hold=True
        wordsLayer.frame_time = 6
        wordsLayer.opaque = True

        #textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOT ADDED")
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

        # score some points - TODO maybe make this double or more if all the jackpots got lit before collecting
        self.game.score(500000)
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'beer-slide.dmd')
        # setup the animated layer
        beerLayer = ep.EP_AnimatedLayer(anim)
        beerLayer.hold=True
        beerLayer.frame_time = 3
        beerLayer.composite_op = "blacksrc"

        anim = dmd.Animation().load(ep.DMD_PATH+'dmb-jackpot.dmd')
        # setup the animated layer
        wordsLayer = ep.EP_AnimatedLayer(anim)
        wordsLayer.hold=True
        wordsLayer.frame_time = 3
        wordsLayer.composite_op = "blacksrc"

        combined = dmd.GroupedLayer(128,32,[self.layer,wordsLayer,beerLayer])
        self.cancel_delayed("Display")
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_slide)
        self.game.sound.play(self.game.assets.quote_drunkJackpot)
        self.delay(name="Display",delay=1.5,handler=self.jackpot_score)

    def jackpot_score(self):
        self.game.sound.play(self.game.assets.sfx_orchestraSpike)
        scoreString = "500,000*"
        scoreLine = dmd.TextLayer(64, 8, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text(scoreString)
        scoreLine.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'dmb-jackpot.dmd').frames[17])
        combined = dmd.GroupedLayer(128,32,[backdrop,scoreLine])
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.update_display)

    def end_save(self):
        # a ball saver to allow for reacclimation
        self.game.ball_save.start(num_balls_to_save=1, time=15, now=True, allow_multiple_saves=False)
        self.end_drunk()

    def end_drunk(self):
        self.cancel_delayed("Display")
        # update the tracking
        self.game.set_tracking('drunkMultiballStatus', "OPEN")
        # reset the flippers
        self.game.enable_inverted_flippers(False)
        self.game.enable_flippers(True)
        # reset the lamps
        for mode in self.shotModes:
            mode.update_lamps()
        # stop the music
        self.game.sound.stop_music()
        self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        # clear the layer
        self.layer = None
        # turn the GI back on
        self.game.gi_control("ON")
        # reset the mug hits for next time
        self.game.set_tracking('beerMugHits',0)
        # set the stack flag back off
        self.game.set_tracking('stackLevel',False,1)
        # unload the mode
        self.unload()


