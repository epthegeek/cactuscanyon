from procgame import *
import cc_modes
import ep
import random

class BionicBart(game.Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(BionicBart, self).__init__(game,priority)


    def ball_drained(self):
        # if we lose all the balls the battle is lost
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('bionicStatus') == "RUNNING":
            self.bionic_failed()

    def mode_started(self):
        # set the stack level
        self.game.set_tracking('stackLevel',True,3)
        # set up the standard display stuff

    # switches
     # ramps
     # loops
    # process - bart hits here? seems like a lot of redundant

    def start_bionic(self):
        # kill the music
        self.game.sound.stop_music()
        # kick off the intro
        self.intro(1)

    def intro(self,step):
        # initial display/sound
        # step 1
         # play the 'deal with this' quote
         # show the 'challenges you' screen
        # step 2
         # play the intro quote
         # show the talking layer
        # step 3
         # start the music
        pass


    def bionic_defeated(self):
        # VICTOLY!
        # set bart flag to dead
        self.game.set_tracking('bionicStatus', "DEAD")
        # light high noon
        self.game.badge.light_high_noon()

        # TODO - lots. points? final display? WAT?

        self.finish_up()

    def bionic_failed(self):
        # Lose the balls during a bionic fight and you lose
        # reset all the star status
        self.game.badge.reset()
        # set bionic
        self.game.set_tracking('bionicStatus',"OPEN")

        self.finish_up()

    def finish_up(self):
        # as is tradition
        # clear the stack level
        self.game.set_tracking('stackLevel',False,3)
        # unload the mode
        self.game.modes.remove(self.game.bionic)

    def clear_layer(self):
        self.layer = None
