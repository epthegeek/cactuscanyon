##
## This mode controls the mine and multiballs
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes

class Mine(game.Mode):
    """Game mode for controlling the mine and such"""
    def __init__(self, game,priority):
        super(Mine, self).__init__(game, priority)
        # set the hits to light the lock based on the config option
        # Settings are in triplets of "light lock 1, light lock 2, light multiball"
        # the last digit is for every step after The 'balls locked total' tracking item
        # can be used to get the digit
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # Easy version
        if difficulty == 'Easy':
            hitsToLightLock = [1,0,0,1,1,1,2,2,2,3]
        # Hard version
        else:
            hitsToLightLock = [1,1,1,2,2,2,3,3,3,4]

        # start the hits count at 0
        self.hits = 0


    # if the ball lands in the kicker -- for now, just get it out again
    def sw_minePopper_closed_for_200ms(self,sw):
        print "PULSE THE KICKER FOR THE MINE"

    def sw_mineEntrance_active(self,sw):
        pass


