##   ____           _                ____
##  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
## | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
## | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
##  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
##                                                   |___/
##           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
##          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
##         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
##          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
##
## A P-ROC Project by Eric Priepke, Copyright 2012
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
#
# This mode is just a big switch list to trap action for the super skill shot
#
from procgame import game
import ep

class SuperFilter(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(SuperFilter, self).__init__(game, priority)
        self.myID = "Super Filter"

    # valid jackpot shots

    def sw_leftLoopTop_active(self,sw):
        if self.game.skill_shot.active == 1:
            self.game.skill_shot.super_hit(made=True,switch=1)
            return game.SwitchStop
        else:
            self.game.skill_shot.super_hit()

    def sw_leftLoopBottom_active(self,sw):
        # if we hit the bottom of the left loop, and it's not active
        if self.game.skill_shot.active != 1:
            # then fail
            self.game.skill_shot.super_hit()

    def sw_leftRampEnter_active(self,sw):
        if self.game.skill_shot.active == 2:
            self.game.skill_shot.super_hit(made=True,switch=2)
            return game.SwitchStop
        else:
            self.game.skill_shot.super_hit()


        # mine poppper
    def sw_minePopper_active_for_400ms(self,sw):
        if self.game.skill_shot.active == 3:
            self.game.skill_shot.super_hit(made=True,switch=3)
            self.game.mountain.eject()
            return game.SwitchStop
        else:
            self.game.skill_shot.super_hit()

    def sw_centerRampMake_active(self,sw):
        if self.game.skill_shot.active == 4:
            self.game.skill_shot.super_hit(made=True,switch=4)
            return game.SwitchStop
        else:
            self.game.skill_shot.super_hit()



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
    # right ramp enter
    def sw_rightRampEnter_active(self,sw):
        self.game.skill_shot.super_hit()
    # right loop top
    def sw_rightLoopTop_active(self,sw):
        self.game.skill_shot.super_hit()
    # right loop bottom
    def sw_rightLoopBottom_active(self,sw):
        self.game.skill_shot.super_hit()
    # mine entrance
    def sw_mineEntrance_active(self,sw):
        self.game.skill_shot.super_hit()
    # saloon popper
    def sw_saloonPopper_active_for_100ms(self,sw):
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
    # bad guys
    def sw_badGuySW0_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_badGuySW1_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_badGuySW2_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_badGuySW3_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_rightOutlane_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_leftOutlane_active(self,sw):
        self.game.skill_shot.super_hit()
    def sw_troughBallFour_active(self,sw):
        self.game.skill_shot.super_hit()
