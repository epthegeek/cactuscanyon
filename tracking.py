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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##  ____  _        _     _____               _    _
## / ___|| |_ __ _| |_  |_   _| __ __ _  ___| | _(_)_ __   __ _
## \___ \| __/ _` | __|   | || '__/ _` |/ __| |/ / | '_ \ / _` |
##  ___) | || (_| | |_    | || | | (_| | (__|   <| | | | | (_| |
## |____/ \__\__,_|\__|   |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
##                                                        |___/
##
## All the tracking defaults piggybacked onto the player object
##
from procgame import *

class Tracking(game.Player):
    """Object for tracking player stats - instantiates with add player"""
    # set some base values?
    # modes could set their own values?
    def __init__(self, name):
        super(Tracking, self).__init__(name)

        self.player_stats = {}

        # load up tracking stats for the player
        self.player_stats['bonus'] = 0
        self.player_stats['greeted'] = False
        self.player_stats['bozoBall'] = False

        self.player_stats['bumperHits'] = 0

        # Tumbleweed increases 5000 per shot - so the first one is actually 25000 when scored
        self.player_stats['tumbleweedValue'] = 20000
        self.player_stats['adventureCompleteValue'] = 20000

        self.player_stats['extraBallsTotal'] = 0
        # allows for stacking of extra balls - if pending > 0 then extra ball is lit
        self.player_stats['extraBallsPending'] = 0

        self.player_stats['beerMugHitsTotal'] = 0
        self.player_stats['beerMugHits'] = 0
        # drunk multiball - OPEN, READY, RUNNING
        self.player_stats['drunkMultiballStatus'] = "OPEN"

        self.player_stats['rightRampShots'] = 0
        self.player_stats['rightRampStage'] = 1

        self.player_stats['leftRampShots'] = 0
        self.player_stats['leftRampStage'] = 1

        self.player_stats['centerRampShots'] = 0
        self.player_stats['centerRampStage'] = 1

        self.player_stats['leftLoopShots'] = 0
        self.player_stats['leftLoopStage'] = 1

        self.player_stats['rightLoopShots'] = 0
        self.player_stats['rightLoopStage'] = 1

        self.player_stats['fullLoops'] = 0

        self.player_stats['saloonShots'] = 0

        self.player_stats['mineShotsTotal'] = 0
        # mine status - OPEN, LOCK, READY, (RUNNING == Gold mine multiball)
        self.player_stats['mineStatus'] = "OPEN"
        self.player_stats['goldMineStarted'] = 1
        self.player_stats['banditAttacks'] = 0
        # used for progression to lock
        self.player_stats['mineHits'] = 0
        # balls currently locked
        self.player_stats['ballsLocked'] = 0
        ## running tally of locked balls
        self.player_stats['ballsLockedTotal'] = 0
        self.player_stats['jackpotsCollected'] = 0
        self.player_stats['motherlodeMultiplier'] = 1
        self.player_stats['motherlodesCollected'] = 0
        self.player_stats['motherlodesCollectedTotal'] = 0
        self.player_stats['motherlodeValue'] = 0
        self.player_stats['motherlodeLit'] = False

        # lit status for jackpots: Left Loop, Left Ramp, Center Ramp, Right Loop, Right Ramp
        self.player_stats['jackpotStatus'] = [True,True,True,True,True]

        self.player_stats['bonusX'] = 1
        # bonus lane status OFF/ON - left is 0 right is 1
        self.player_stats['bonusLaneStatus'] = ["OFF","OFF"]

        self.player_stats['bountyCollected'] = 0
        self.player_stats['isBountyLit'] = False

        self.player_stats['rank'] = 0
        self.player_stats['combos'] = 0
        # needed for being able to reset the star
        self.player_stats['combosTotal'] = 0
        self.player_stats['bigChain'] = 0

        # Quickdraw status - OPEN, TOP/BOT (for hard difficulty), READY, RUNNING-- 0 is left, 1 is right
        self.player_stats['quickdrawStatus'] = ["OPEN","OPEN"]
        self.player_stats['quickdrawsStarted'] = 0
        self.player_stats['quickdrawsWon'] = 0
        self.player_stats['badGuysDead'] = [True,False,True,True]
        # these are separate because the bad guy can be dead (quickdraw) but also up (showdown/gunfight)
        self.player_stats['badGuyUp'] = [False,False,False,False]
        # showdown status - OPEN, READY, RUNNING, OVER (to hold until ambush)
        self.player_stats['showdownStatus'] = "OVER"
        self.player_stats['showdownTotal'] = 0
        self.player_stats['showdownPoints'] = 0
        # ambush status - OPEN, READY, RUNNING, OVER (for switching between showdown and ambush)
        self.player_stats['ambushStatus'] = "OPEN"
        self.player_stats['ambushTotal'] = 0
        self.player_stats['ambushPoints'] = 0
        # total kills for high noon
        self.player_stats['kills'] = 0

        # bartStatus: OPEN, RUNNING, LAST, DEAD
        self.player_stats['bartStatus'] = "OPEN"
        self.player_stats['bartHits'] = 0
        self.player_stats['bartsDefeated'] = 0
        self.player_stats['bartsDefeatedTotal'] = 0
        self.player_stats['currentBart'] = 0
        self.player_stats['gunfightsStarted'] = 0
        self.player_stats['gunfightsWon'] = 0
        # gunfight status, OPEN, READY, RUNNING
        self.player_stats['gunfightStatus'] = "OPEN"

        # highNoonStatus = OPEN, READY, RUNNING
        self.player_stats['highNoonStatus'] = "READY"
        # list to store the lit items for the star ?
        # Starts at the top of the star with 0, goes clockwise. 0 = motherlode, 1=combo, 2=barts, 3=showdown, 4=stampede
        self.player_stats['starStatus'] = [True,True,True,True,True]
        # Bionic Bart - OPEN / READY / RUNNING / DEAD
        self.player_stats['bionicStatus'] = "OPEN"

        # Move your train - OPEN / READY / RUNNING
        self.player_stats['mytStatus'] = "OPEN"

        self.player_stats['tiltStatus'] = 0
        # used to disable the playfield lights in an update lamps pass
        # lamp status modes: ON, OFF
        self.player_stats['lampStatus'] = "ON"

        # a new idea - stack level for tracking what can or can not start
        # Level 0 is Gunfight, Quick Draw and showdown - only one of these can run at a time, and can finish even if a level 2 starts
        # Level 1 is Stampede, and Save Polly - only one of these can run at a time, and they are allowed to run with level 0
        # Level 2 is goldmine multiball - should not start if a level 1 mode is active
        # Level 3 is high noon
        self.player_stats['stackLevel'] = [False,False,False,False]

