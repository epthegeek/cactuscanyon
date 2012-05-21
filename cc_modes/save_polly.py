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


    def sw_centerRampMake_active(self,sw):
        # center ramp pauses the train
        self.pause_train()
        self.game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        self.advance_save_polly()
        self.game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        self.advance_save_polly()
        self.game.SwitchStop

    def sw_trainEncoder_active(self,sw):
        # this is the moving train
        # each time it hits increment the train progress
        self.trainProgress += 1
        # when it gets to a certain number, polly dies
        if self.trainProgress >= 30:
            self.polly_died()

    def sw_trainHome_active(self,sw):
        # turn off the reverse motor
        pass

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
        # start the train moving
        self.move_train()
        # setup the mode screen with the animated train
        anim = dmd.Animation().load(ep.DMD_PATH+'train-head-on.dmd')
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=True,frame_time=6)
        self.layer = animLayer
        self.delay(delay=10,handler=self.end_save_polly)

    # for moving the train forward - since we'll have to delay call it
    def move_train(self):
        pass

    # for a center ramp hit
    def pause_train(self):
        print "PAUSE TRAIN"
        # stop the train from moving
        # play the pause display
        # set a delay to start the train again
        pass

    def reset_train(self):
        # turn on the reverse motor
        pass

    def stop_train(self,direction):
        # turn off the moving train solenoid
        pass

        # for a side ramp hit
    def advance_save_polly(self):
        # add the sucessful shot
        self.shotsSoFar += 1
        if self.shotsSoFar >= self.shotsToWin:
            self.polly_saved()
        else:
        # display something
        # go back to the in progress display
            pass

    # success
    def polly_saved(self):
        # play the train stopping animation and some sounds
        # light extra ball? or is that score extra ball?
        # then after a delay, reset train
        pass

    # fail
    def polly_died(self):
        pass

    # clean up and exit
    def end_save_polly(self):
        self.game.sound.stop_music()
        # turn the main game music back on
        self.game.base_game_mode.music_on()
        # unload the mode
        self.game.modes.remove(self.game.save_polly)


    # loop for timer?
    def timer(self):
        pass
