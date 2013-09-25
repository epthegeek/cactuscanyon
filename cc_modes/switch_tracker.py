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
## A P-ROC Project by Eric Priepke, Copyright 2012-2013
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
#
# This mode is just a big switch list to trap action for the super skill shot
#
from procgame import game
import ep

class SwitchTracker(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(SwitchTracker, self).__init__(game, priority)
        self.myID = "Switch Tracker"

    def tilted(self):
        pass

    # flipper counts for audits
    def sw_flipperLwL_active(self,sw):
        self.game.game_data['Audits']['Left Flipper'] += 1
    def sw_flipperLwR_active(self,sw):
        self.game.game_data['Audits']['Right Flipper'] += 1



    # switches that get tracked
    def sw_shooterLane_active(self,sw):
        self.game.game_data['SwitchHits']['18 SHOOTER LANE'] = 0

    def sw_skillBowl_active(self,sw):
        self.game.game_data['SwitchHits']['67 SKILL BOWL'] = 0

    def sw_rightRampEnter_active(self,sw):
        self.game.game_data['SwitchHits']['66 R RAMP ENTER'] = 0
        self.multiball_status_check()

    def sw_rightRampMake_active(self,sw):
        self.game.game_data['Feature']['Right Ramp Hits'] += 1
        self.game.game_data['SwitchHits']['65 R RAMP MAKE'] = 0

    def sw_rightRampBottom_active(self,sw):
        self.game.game_data['SwitchHits']['68 R RAMP BOTTOM'] = 0

    def sw_rightReturnLane_active(self,sw):
        self.game.game_data['SwitchHits']['17 R RETURN LANE'] = 0
        self.multiball_status_check()

    def sw_rightOutlane_active(self,sw):
        self.game.game_data['Audits']['Right Drains'] += 1
        self.game.game_data['SwitchHits']['27 R OUTLANE'] = 0

    def sw_leftRampEnter_active(self,sw):
        self.game.game_data['Feature']['Left Ramp Hits'] += 1
        self.game.game_data['SwitchHits']['85 L RAMP ENTER'] = 0
        self.multiball_status_check()

    def sw_leftRampMake_active(self,sw):
        self.game.game_data['SwitchHits']['83 L RAMP MAKE'] = 0

    def sw_leftReturnLane_active(self,sw):
        self.game.game_data['SwitchHits']['26 L RETURN LANE'] = 0
        self.multiball_status_check()

    def sw_leftOutlane_active(self,sw):
        self.game.game_data['Audits']['Left Drains'] += 1
        self.game.game_data['SwitchHits']['16 L OUTLANE'] = 0

    def sw_centerRampEnter_active(self,sw):
        self.game.game_data['SwitchHits']['82 C RAMP ENTER'] = 0
        self.multiball_status_check()

    def sw_centerRampMake_active(self,sw):
        self.game.game_data['Feature']['Center Ramp Hits'] += 1
        self.game.game_data['SwitchHits']['84 C RAMP MAKE'] = 0

    def sw_leftLoopTop_active(self,sw):
        # left loop audit done in mode due to conditions
        self.game.game_data['SwitchHits']['58 L LOOP TOP'] = 0

    def sw_leftLoopBottom_active(self,sw):
        self.game.game_data['SwitchHits']['36 L LOOP BOT'] = 0
        self.multiball_status_check()

    def sw_rightLoopTop_active(self,sw):
        # right loop audit doen in mode due to conditions
        self.game.game_data['SwitchHits']['56 R LOOP TOP'] = 0

    def sw_rightLoopBottom_active(self,sw):
        self.game.game_data['SwitchHits']['37 R LOOP BOT'] = 0
        self.multiball_status_check()

    def sw_rightBonusLane_active(self,sw):
        self.game.game_data['SwitchHits']['57 R BONUS LANE'] = 0
        self.multiball_status_check()

    def sw_leftBonusLane_active(self,sw):
        self.game.game_data['SwitchHits']['47 L BONUS LANE'] = 0
        self.multiball_status_check()

    def sw_bottomRightStandUp_active(self,sw):
        self.game.game_data['SwitchHits']['28 BOT R QUICKDRAW'] = 0

    def sw_topRightStandUp_active(self,sw):
        self.game.game_data['SwitchHits']['44 TOP R QUICKDRAW'] = 0

    def sw_bottomLeftStandUp_active(self,sw):
        self.game.game_data['SwitchHits']['87 BOT L QUICKDRAW'] = 0

    def sw_topLeftStandUp_active(self,sw):
        self.game.game_data['SwitchHits']['86 TOP L QUICKDRAW'] = 0

    def sw_mineEntrance_active(self,sw):
        self.game.game_data['SwitchHits']['15 MINE ENTRANCE'] = 0
        self.multiball_status_check()

    def sw_beerMug_active(self,sw):
        self.game.game_data['SwitchHits']['46 BEER MUG'] = 0
        self.multiball_status_check()

    def sw_jetBumpersExit_active(self,sw):
        self.game.game_data['SwitchHits']['48 JETS EXIT'] = 0
        self.multiball_status_check()

    def sw_leftSlingshot_active(self,sw):
        self.game.game_data['SwitchHits']['51 L SLINGSHOT'] = 0

    def sw_rightSlingshot_active(self,sw):
        self.game.game_data['SwitchHits']['52 R SLINGSHOT'] = 0

    def sw_rightJetBumper_active(self,sw):
        self.game.game_data['SwitchHits']['54 R JET BUMPER'] = 0

    def sw_leftJetBumper_active(self,sw):
        self.game.game_data['SwitchHits']['53 L JET BUMPER'] = 0

    def sw_bottomJetBumper_active(self,sw):
        self.game.game_data['SwitchHits']['55 BOT JET BUMPER'] = 0

    def sw_saloonGate_active(self,sw):
        self.game.game_data['SwitchHits']['73 SALOON GATE'] = 0
        self.multiball_status_check()

    def sw_saloonBart_active(self,sw):
        self.game.game_data['SwitchHits']['75 BART TOY'] = 0

    # this is for killing the 'current status' display
    def multiball_status_check(self):
        if self.game.interrupter.statusDisplay != "Off":
            self.game.interrupter.status_off()
