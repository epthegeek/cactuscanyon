##
## This mode keeps track of the awards and points for making the center ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes

class CenterRamp(game.Mode):
    """Cactus Canyon Center Ramp Mode"""
    def __init__(self, game, priority):
        super(CenterRamp, self).__init__(game, priority)

    def mode_started(self):
        # this would have to turn on some lights and stuff
        pass

    def sw_centerRampEnter_active(self,sw):
        # play the switch sound
        # TODO this should be the train noise
        self.game.sound.play(self.game.assets.sfx_rightRampEnter)
        # score the arbitrary and wacky points
        self.game.score(2530)

    def sw_centerRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('centerRampShots')
        self.award_ramp_score()

    def award_ramp_score(self):
        ## ramp award is determined by stage - starts at 1
        ## completed is CURRENTLY 4 - to reset the awards
        ## reset the leftRampStage
        stage = self.game.show_tracking('centerRampStage')
        if stage == 1:
            self.game.score(10)
        elif stage == 2:
            self.game.score(20)
        elif stage == 3:
            self.game.score(30)
        else:
            self.game.score(30)

        # then tick the stage up for next time unless it's completed
        if self.game.show_tracking('centerRampStage') < 4:
            self.game.increase_tracking('centerRampStage')
