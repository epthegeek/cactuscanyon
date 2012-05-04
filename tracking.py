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

        self.player_stats['mineShots'] = 0
        ## balls currently locked
        self.player_stats['ballsLocked'] = 0
        ## running tally of locked balls
        self.player_stats['ballsLockedTotal'] = 0
        self.player_stats['isLockLit'] = False
        self.player_stats['isMultiballLit'] = False
        self.player_stats['jackpotsCollected'] = 0
        self.player_stats['motherLodesCollected'] = 0

        self.player_stats['bonusX'] = 1
        self.player_stats['isLeftBonusLaneLit'] = False
        self.player_stats['isRightBonusLaneLit'] = False

        self.player_stats['bountyCollected'] = 0
        self.player_stats['isBountyLit'] = False


        self.player_stats['rank'] = 1

        self.player_stats['isRightQuickDrawLit'] = False
        self.player_stats['isLeftQuickDrawLit'] = False
        self.player_stats['quickDrawsStarted'] = 0
        self.player_stats['quickDrawsWon'] = 0
        self.player_stats['badGuysDead'] = [False,False,False,False]


        self.player_stats['bartBrothersDefeated'] = 0
        self.player_stats['bartBrotherStage'] = 1
        self.player_stats['bartBrotherHits'] = 0
        self.player_stats['isBartBrotherActive'] = False


