from procgame import *
from assets import *
import cc_modes
import ep

class Stampede(game.Mode):
    """Cactus Canyon Stampede"""
    def __init__(self, game, priority):
        super(Stampede, self).__init__(game, priority)
        self.stampShots = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.shots = ['leftLoop','leftRamp','centerRamp','rightLoop','rightRamp']
        # which jackpot is active
        self.active = 0
        # set up the cows layer
        anim = dmd.Animation().load(ep.DMD_PATH+'cows-parading.dmd')
        self.cowLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        # set up the animations they are to alternate
        self.anims = []
        anim0 = ep.DMD_PATH + "cows-left.dmd"
        self.anims.append({'layer':anim0,'direction':ep.EP_Transition.PARAM_WEST})
        anim1 = ep.DMD_PATH + "cows-right.dmd"
        self.anims.append({'layer':anim1,'direction':ep.EP_Transition.PARAM_EAST})


    def ball_drained(self):
    # if we're dropping down to one ball, and stampede is running - do stuff
        if self.game.trough.num_balls_in_play in (0,1) and self.game.show_tracking('centerRampStatus') == 89:
            self.end_stampede()

    ### switches

    def sw_leftLoopTop_active(self,sw):
        self.process_shot(0,self.active)
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot(1,self.active)
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot(2,self.active)
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        self.process_shot(3,self.active)
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4,self.active)
        return game.SwitchStop

    def start_stampede(self):
        # set the stack layer
        self.game.set_tracking('stackLevel',True,1)
        # stop the current music
        self.game.sound.stop_music()
        # set the ramp status for lights
        for shot in self.shots:
            self.game.set_tracking(shot,89)
        # start the timer for the moving jackpot
        self.jackpot_shift()
        #play the opening anim
        anim = dmd.Animation().load(ep.DMD_PATH+'stampede-animation.dmd')
        myWait = len(anim.frames) / 10 + 1.5
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # toss to the main display after the animation
        self.delay(name="Display",delay=myWait,handler=self.main_display)
        # play a quote
        self.game.sound.play(self.game.assets.quote_stampedeStart)
        # start the music for stampede
        self.game.base_game_mode.music_on(self.game.assets.music_stampede)
        # launch some more balls
        if self.game.trough.num_balls_in_play < 3:
            total = 3 - self.game.trough.num_balls_in_play
            # turn on autoplunge
            self.game.autoPlunge = True
            # launch whatever it takes to get to 3 balls
            self.game.trough.launch_balls(total)

    def main_display(self):
        # this is the main score display for stampede - it's got score on it, so we'll have to loop
        # title line
        titleLine = dmd.TextLayer(128/2, 1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("STAMPEDE MULTIBALL")
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(64, 7, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString)
        scoreLine.composite_op = "blacksrc"
        # group with cow layer
        combined = dmd.GroupedLayer(128,32,[self.cowLayer,titleLine,scoreLine])
        # set the layer active
        self.layer = combined
        # loop back again in .2 for score update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    # decide if this was a jackpot hit or a miss
    def process_shot(self,number,active):
         # cancel the display if any
        self.cancel_delayed("Display")
        if active == number:
            self.jackpot_hit()
        else:
            self.jackpot_wiff()

    def jackpot_hit(self,step=1):
        if step == 1:
            # play an animation
            anim = dmd.Animation().load(ep.DMD_PATH+'stampede-jackpot.dmd')
            myWait = len(anim.frames) / 12
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=5)
            self.layer = animLayer
            # and some sounds
            self.game.sound.play(self.game.assets.sfx_revRicochet)
            # and award points
            self.game.score(500000)
            # loop back to do the next part
            self.delay(name="Display",delay=myWait,handler=self.jackpot_hit,param=2)
        # second pass layers the score over the text
        if step == 2:
            self.backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'stampede-jackpot.dmd').frames[42])
            self.scoreLine = dmd.TextLayer(64, 10, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("500,000")
            self.scoreLine.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[self.backdrop,self.scoreLine])
            self.game.sound.play(self.game.assets.quote_jackpot)
            # loop back to cleear
            self.delay(name="Display",delay=2,handler=self.jackpot_hit,param=3)
        # third pass plays the wipe
        if step == 3:
            anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe.dmd')
            myWait = len(anim.frames) / 6
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=10)
            self.layer = dmd.GroupedLayer(128,32,[self.backdrop,self.scoreLine,animLayer])
            # play a sound on delay
            self.delay(name="Display",delay=myWait,handler=self.game.play_remote_sound,param=self.game.assets.sfx_explosion1)
            # then do the main display
            self.delay(name="Display",delay=myWait,handler=self.main_display)

    def jackpot_wiff(self,step=1):
        if step == 1:
            # load the animation based on which was last played
            self.direction = self.anims[0]['direction']
            anim = dmd.Animation().load(self.anims[0]['layer'])
            myWait = len(anim.frames) / 12
            # reverse them for next time
            self.anims.reverse()
            # play an animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=5)
            animLayer.composite_op = "blacksrc"
            self.layer = animLayer
            # cow shuffle animation
            # and some sounds
            self.game.sound.play(self.game.assets.quote_stampedeWiff)
            # and award points
            self.game.score(250000)
            # loop back to drag in the score
            self.delay(name="Display", delay=myWait, handler=self.jackpot_wiff,param=2)
        if step == 2:
            # score display
            textLine = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False).set_text("250,000")
            # run the transition to bring in the text
            transition = ep.EP_Transition(self,self.layer,textLine,ep.EP_Transition.TYPE_SLIDEOVER,self.direction)
            # clear in 2 seconds
            self.delay(name="Display",delay=2,handler=self.main_display)

    def jackpot_shift(self):
        # bump up by one
        self.active += 1
        # then see if we went over
        if self.active == 5:
            self.active = 0
        # update the lamps
        for shot in self.stampShots:
            shot.update_lamps()
        # then come back in 6 seconds and do it all over again
        self.delay(name="Timer",delay=6,handler=self.jackpot_shift)

    def end_stampede(self):
        # stop the music
        self.game.sound.stop_music()
        # kill the timer loop that moves the jackpot
        self.cancel_delayed("Timer")
        # set some tracking?
        # reset the ramp status
        for each in self.shots:
            self.game.set_tracking(each,1)
        # unload?
        # unload the mode
        self.game.modes.remove(self.game.stampede)
        # clear the stack layer
        self.game.set_tracking('stackLevel',False,1)
        # turn the main music back on
        self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)

    def clear_layer(self):
        self.layer=None

    def abort_display(self):
        self.cancel_delayed('Display')
        self.clear_layer()
