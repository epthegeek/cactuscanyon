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
        self.player_stats['extraBalls'] = 0
        self.player_stats['isExtraBallLit'] = False

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

        self.player_stats['saloonShots'] = 0

        self.player_stats['mineShotsTotal'] = 0
        # mine status - OPEN, LOCK, READY, RUNNING
        self.player_stats['mineStatus'] = "OPEN"
        self.player_stats['mineHits'] = 0
        ## balls currently locked
        self.player_stats['ballsLocked'] = 0
        ## running tally of locked balls
        self.player_stats['ballsLockedTotal'] = 0
        self.player_stats['isLockLit'] = False
        self.player_stats['isMultiballLit'] = False
        self.player_stats['jackpotsCollected'] = 0
        self.player_stats['motherLodesCollected'] = 0

        self.player_stats['bonusX'] = 1
        # bonus lane status OFF/ON - left is 0 right is 1
        self.player_stats['bonusLaneStatus'] = ["OFF","OFF"]

        self.player_stats['bountyCollected'] = 0
        self.player_stats['isBountyLit'] = False

        self.player_stats['rank'] = 1

        # Quickdraw status - OPEN, TOP/BOT (for hard difficulty), READY, RUNNING -- 0 is left, 1 is right
        self.player_stats['quickDrawStatus'] = ["OPEN","OPEN"]
        self.player_stats['quickDrawsStarted'] = 0
        self.player_stats['quickDrawsWon'] = 0
        self.player_stats['badGuysDead'] = [False,False,False,False]

        # bartStatus: OPEN, ACTIVE, DEAD
        self.player_stats['bartStatus'] = 1
        self.player_stats['bartHits'] = 0
        self.player_stats['bartDefeated'] = 0
        self.player_stats['gunfightsStarted'] = 0
        self.player_stats['gunfightsWon'] = 0
        # gunfight status, OPEN, READY, RUNNING
        self.player_stats['gunfightStatus'] = "OPEN"


