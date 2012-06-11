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

class DrunkMultiball(game.Mode):
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
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
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
        self.process_shot('rightLoop',self.shotModes[1])
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot('rightRamp',self.shotModes[4])
        return game.SwitchStop

    def process_shot(self,shot,mode):
        if shot in self.active:
            # take it out of active and put it in  available
            self.active.remove(shot)
            self.availableJackpots.append(shot)
            # update the lamps for the hit ramp
            mode.update_lamps()
            # score some points - TODO maybe make this double or more if all the jackpots got lit before collecting
            self.game.score(500000)
            # play a quote
            self.game.sound.play(self.game.assets.quote_drunkJackpot)
        else:
            # TODO do something here
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
        thing1 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-1.dmd').frames[0])
        thing2 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-2.dmd').frames[0])
        thing3 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-3.dmd').frames[0])
        thing4 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-4.dmd').frames[0])
        thing5 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-5.dmd').frames[0])
        thing6 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-6.dmd').frames[0])
        thing7 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-7.dmd').frames[0])
        thing8 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-8.dmd').frames[0])
        thing9 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-9.dmd').frames[0])
        thing10 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-10.dmd').frames[0])
        thing11 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-11.dmd').frames[0])
        thing12 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-12.dmd').frames[0])
        thing13 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'pour-mask-13.dmd').frames[0])
        script = []
        script.append({'seconds':0.1,'layer':thing1})
        script.append({'seconds':0.1,'layer':thing2})
        script.append({'seconds':0.1,'layer':thing3})
        script.append({'seconds':0.1,'layer':thing4})
        script.append({'seconds':0.1,'layer':thing5})
        script.append({'seconds':0.1,'layer':thing6})
        script.append({'seconds':0.1,'layer':thing7})
        script.append({'seconds':0.1,'layer':thing8})
        script.append({'seconds':0.1,'layer':thing9})
        script.append({'seconds':0.1,'layer':thing10})
        script.append({'seconds':0.1,'layer':thing11})
        script.append({'seconds':0.1,'layer':thing12})
        script.append({'seconds':0.1,'layer':thing13})

        pour = dmd.ScriptedLayer(128,32,script)
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
            self.game.autoPlunge = True
            self.game.trough.launch_balls(thisMany)
        self.update_display()

    def update_display(self):
        self.overlay.composite_op = "blacksrc"
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(80, 8, self.game.assets.font_7px_az, "center", opaque=False).set_text(scoreString,blink_frames=8)
        textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("DRUNK MULTIBALL")
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
        anim = dmd.Animation().load(ep.DMD_PATH+'dmb.dmd')
        myWait = len(anim.frames) / 7.5
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 8
        animLayer.composite_op = "blacksrc"
        animLayer.add_frame_listener(3,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
        animLayer.add_frame_listener(5,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)

        textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOT ADDED")
        combined = dmd.GroupedLayer(128,32,[textLine1,animLayer])
        self.cancel_delayed("Display")
        self.layer = combined
        self.delay(name="Display",delay=myWait,handler=self.update_display)

    def end_drunk(self):
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
        # unload the mode
        self.game.modes.remove(self.game.drunk_multiball)
        # set the stack flag back off
        self.game.set_tracking('stackLevel',False,1)

