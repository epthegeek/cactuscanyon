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

    def ball_drained(self):
        # if we're dropping down to one ball, and drunk multiball is running - do stuff
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
            self.end_drunk()

    # switches

    # beer mug lights jackpots
    def sw_beerMug_active(self,sw):
        self.light_jackpot()
        return game.SwitchStop

    def start_drunk(self):
        print "STARTING DRUNK ASS MULTIBALL"
        # set the stack level
        self.game.set_tracking('stackLevel',True,2)
        # update the tracking
        self.game.set_tracking('drunkMultiballStatus', "RUNNING")
        # disable the flippers
        self.game.enable_flippers(False)
        # enable the inverted flippers
        self.game.enable_inverted_flippers(True)
        # stop the music
        self.game.sound.stop_music()
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
        # unload the mode
        self.game.modes.remove(self.game.drunk_multiball)
        # set the stack flag back off
        self.game.set_tracking('stackLevel',False,2)
