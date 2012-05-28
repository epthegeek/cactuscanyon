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

        self.player_stats['extraBallsTotal'] = 0
        # allows for stacking of extra balls - if pending > 0 then extra ball is lit
        self.player_stats['extraBallsPending'] = 0

        self.player_stats['beerMugHits'] = 0

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
        # mine status - OPEN, LOCK, READY, RUNNING
        self.player_stats['mineStatus'] = "OPEN"
        # used for progression to lock
        self.player_stats['mineHits'] = 0
        # balls currently locked
        self.player_stats['ballsLocked'] = 0
        ## running tally of locked balls
        self.player_stats['ballsLockedTotal'] = 0
        self.player_stats['jackpotsCollected'] = 0
        self.player_stats['motherLodePending'] = 0
        self.player_stats['motherLodesCollected'] = 0
        # lit status for jackpots: Left Loop, Left Ramp, Center Ramp, Right Loop, Right Ramp
        self.player_stats['jackpotStatus'] = [True,True,True,True,True]

        self.player_stats['bonusX'] = 1
        # bonus lane status OFF/ON - left is 0 right is 1
        self.player_stats['bonusLaneStatus'] = ["OFF","OFF"]

        self.player_stats['bountyCollected'] = 0
        self.player_stats['isBountyLit'] = False

        self.player_stats['rank'] = 0
        self.player_stats['combos'] = 0

        # Quickdraw status - OPEN, TOP/BOT (for hard difficulty), READY, RUNNING, SHOWDOWN -- 0 is left, 1 is right
        self.player_stats['quickdrawStatus'] = ["OPEN","OPEN"]
        self.player_stats['quickdrawsStarted'] = 0
        self.player_stats['quickdrawsWon'] = 0
        self.player_stats['badGuysDead'] = [True,False,True,True]
        # these are separate because the bad guy can be dead (quickdraw) but also up (showdown/gunfight)
        self.player_stats['badGuyUp'] = [False,False,False,False]
        self.player_stats['showdownTotal'] = 0

        # bartStatus: OPEN, RUNNING, LAST, DEAD
        self.player_stats['bartStatus'] = "OPEN"
        self.player_stats['bartHits'] = 0
        self.player_stats['bartsDefeated'] = 0
        self.player_stats['currentBart'] = 0
        self.player_stats['gunfightsStarted'] = 0
        self.player_stats['gunfightsWon'] = 0
        # gunfight status, OPEN, READY, RUNNING
        self.player_stats['gunfightStatus'] = "OPEN"

        # highNoonStatus = OPEN, READY, RUNNING
        self.player_stats['highNoonStatus'] = "OPEN"
        # list to store the lit items for the star ?
        self.player_stats['highNoonProgress'] = []

        self.player_stats['tiltStatus'] = 0
        # used to disable the GI in an update lamps pass
        # lamp status modes: ON, OFF, GIONLY .. ?
        self.player_stats['lampStatus'] = "ON"
        self.player_stats['activeMultiBall'] = False

