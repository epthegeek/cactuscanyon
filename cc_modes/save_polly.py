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

    def sw_centerRampMake_active(self,sw):
        # center ramp pauses the train
        self.pause_train()
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        self.advance_save_polly()
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        self.advance_save_polly()
        return game.SwitchStop

    def sw_trainEncoder_active(self,sw):
        # this is the moving train
        # each time it hits increment the train progress
        self.trainProgress += 1
        print "TRAIN PROGRESS" + str(self.trainProgress)
        # when it gets to a certain number, polly dies
        if self.trainProgress >= 10:
            self.polly_died()

    def sw_trainHome_active(self,sw):
        # turn off the reverse motor
        self.game.coils.trainReverse.disable()
        # when we hit the home switch it's time to unload
        self.end_save_polly()

    def start_save_polly(self):
        # clear any running music
        self.game.sound.stop_music()
        # reset the train progress
        self.trainProgress = 0
        # play the intro animation
        # run the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'polly-peril.dmd')
        myWait = len(anim.frames) / 12 + 2
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=4)
        self.layer = animLayer
        # start up the music
        self.delay(delay=myWait,handler=self.in_progress)

    def in_progress(self):
        # start the music
        self.game.sound.play_music(self.game.assets.music_pollyPeril)
        # start the train moving
        self.move_train()
        # setup the mode screen with the animated train
        anim = dmd.Animation().load(ep.DMD_PATH+'train-head-on.dmd')
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=True,frame_time=6)
        self.layer = animLayer
        # this is a temporary mechanism for making the mode work for now
        self.delay(delay=30,handler=self.end_save_polly)

    # for moving the train forward - since we'll have to delay call it
    def move_train(self):
        self.game.coils.trainForward.enable()

    # for a center ramp hit
    def pause_train(self,advanced=False, time=5):
        print "PAUSE TRAIN"
        # stop the train from moving
        self.stop_train()
        # play the running on top animation
        anim = dmd.Animation().load(ep.DMD_PATH+'cow-on-tracks.dmd')
        # math out the wait
        myWait = len(anim.frames) / 8.57
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=7)
        if advanced:
            # this is the side ramp shot version
            pass
        else:
            # play the pause display
            self.game.sound.play(self.cows[0])
            # swap for the next shot
            self.cows.reverse()
            # set a delay to start the train again
        self.layer = dmd.GroupedLayer(128,32,[animLayer])
        self.pause_timer(time)

    def pause_timer(self,time):
        # if the timer is at 0 start the train up again
        if time <= 0:
            self.in_progress()
        else:
            # if not, tick off one
            time -= 1
            # then reschedule 1 second later with the new time
            self.delay(delay=1,handler=self.pause_timer,param=time)

    def reset_train(self):
        # turn on the reverse motor
        self.game.coils.trainReverse.enable()

    def stop_train(self):
        # turn off the moving train solenoid
        self.game.coils.trainForward.disable()

        # for a side ramp hit
    def advance_save_polly(self):
        # add the sucessful shot
        self.shotsSoFar += 1
        if self.shotsSoFar >= self.shotsToWin:
            self.polly_saved()
        else:
            # play the running on top animation
            anim = dmd.Animation().load(ep.DMD_PATH+'train-running-on-top.dmd')
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            # display something
            self.layer = animLayer
            # pause the train briefly
            self.delay(delay=myWait,handler=self.register_advance)

    def register_advance(self):
        self.pause_train(advanced=True,time=2)

    # success
    def polly_saved(self):
        # sound for this is self.game.assets.sfx_trainStop
        # play the train stopping animation and some sounds
        # light extra ball? or is that score extra ball?
        # then after a delay, reset train
        self.polly_finished() # should delay this

    # fail
    def polly_died(self):
        self.poly_finished()

    def polly_finished(self):
        # stop the polly music
        self.game.sound.stop_music()
        # turn the main game music back on
        self.game.base_game_mode.music_on()
        self.reset_train()
        # turn off the polly display
        self.layer = None
        # set the tracking on the ramps
        # this is mostly for the lights
        self.game.set_tracking('leftRampStage = 5')
        self.game.set_tracking('rightRampStage = 5')
        self.game.set_tracking('centerRampStage = 4')

    # clean up and exit
    def end_save_polly(self):
        # unload the mode
        self.game.modes.remove(self.game.save_polly)

