#
# This mode is just a big switch list to trap action for the super skill shot
#

from procgame import *
import cc_modes
import random
import ep


class SuperFilter(game.Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(SuperFilter, self).__init__(game, priority)

    # valid jackpot shots

    def sw_leftLoopTop_active(self,sw):
        if self.game.skill_shot.active == 1:
            self.game.skill_shot.super_hit(made=True)
        else:
            self.game.skill_shot.super_hit()
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        if self.game.skill_shot.active == 2:
            self.game.skill_shot.super_hit(made=True)
        else:
            self.game.skill_shot.super_hit()
        return game.SwitchStop

    def sw_centerRampMake_active(self,sw):
        if self.game.skill_shot.active == 3:
            self.game.skill_shot.super_hit(made=True)
        else:
            self.game.skill_shot.super_hit()
        return game.SwitchStop

    # everything else
    # quickdraw targets
    def sw_topLeftStandUp_active(self, sw):
        self.game.skill_shot.super_hit()
    def sw_bottomLeftStandUp_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_topRightStandUp_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_bottomRightStandUp_active(self,sw):
        self.game.skill_shot.super_hit()
    # right ramp make
    def sw_rightRampMake_active(self,sw):
        self.game.skill_shot.super_hit()
    # right loop top
    def sw_rightLoopTop_active(self,sw):
        self.game.skill_shot.super_hit()
    # mine entrance
    def sw_mineEntrance_active(self,sw):
        self.game.skill_shot.super_hit()
    # saloon gate
    def sw_saloonGate_active(self,sw):
        self.game.skill_shot.super_hit()
    # beer mug
    def sw_beerMug_active(self,sw):
        self.game.skill_shot.super_hit()
    # slingshots
    def sw_leftSlingshot_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_rightSlingshot_active(self,sw):
        self.game.skill_shot.super_hit()
