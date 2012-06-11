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

    def ball_drained(self):
        # if we're dropping down to one ball, and drunk multiball is running - do stuff
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.end_drunk()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        self.process_shot('leftLoop')
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot('leftRamp')
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot('centerRamp')
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        self.process_shot('rightLoop')
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot('rightRamp')
        return game.SwitchStop

    def process_shot(self,shot):
        if shot in self.active:
            # take it out of active and put it in  available
            self.active.remove(shot)
            self.availableJackpots.append(shot)
            # score some points - TODO maybe make this double or more if all the jackpots got lit before collecting
            self.game.score(500000)
            # play a quote
            self.game.sound.play(self.game.assets.quote_jackpot)
        else:
            # TODO do something here
            self.game.score(2530)

    # beer mug lights jackpots
    def sw_beerMug_active(self,sw):
        self.light_jackpot()
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
        # play the drunk multiball song
        self.game.base_game_mode.music_on(self.game.assets.music_drunkMultiball)
        # show some screens about the mode
        self.intro_display()

    def intro_display(self):
        ## show some junk about how the mode works
        self.get_going()

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
        textLine1 = dmd.TextLayer(80, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("DRUNK MULTIBALL")
        combined = dmd.GroupedLayer(128,32,[textLine1,self.overlay])
        self.layer = combined

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
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=8)
        animLayer.composite_op = "blacksrc"
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
