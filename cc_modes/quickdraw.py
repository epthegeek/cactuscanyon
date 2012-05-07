##
## The quickdraw gameplay action extravaganza
##
from procgame import *
import cc_modes
import ep

class QuickDraw(game.Mode):
    """Quickdraws for great justice"""
    def __init__(self,game,priority):
        super(QuickDraw, self).__init__(game,priority)
        ## here's where things happen
        #self.game = game

    def start_quickdraw(self,side):
        print "STARTING QUICKDRAW ON SIDE:" + str(side)
        # set the status of this side to running
        self.game.set_tracking('quickDrawStatus',"RUNNING",side)
        self.delay(delay=4,handler=self.end_quickdraw,param=side)

        # figure out the available bad guys
        # pick one of them at random
        # kill the game music
        self.game.sound.stop_music()
        # start the music
        self.game.sound.play(self.game.assets.music_quickDrawBumper)
        self.delay(name="quickdraw music",delay=1.3,handler=self.game.play_remote_music,param=self.game.assets.music_quickDraw)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_quickDrawStart)
        # pop that sucker up
        anim = dmd.Animation().load(self.game.assets.anim_quickDrawStart)
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)
        self.layer = animLayer
        # Needs the text overlayed on it
    # start the countdown
        pass

    def sw_badGuyLeft_active(self):
        # far left bad guy target
        print "BAD GUY 1 HIT"

    def sw_badGuyLeftCenter_active(self):
        # center left badguy target
        print "BAD GUY 2 HIT"

    def sw_badGuyRightCenter_active(self):
        # center right bad guy target
        print "BAD GUY 3 HIT"

    def sw_badGuyRight_active(self):
        print "BAD GUY 4 HIT"
        # far right bad guy target

    def end_quickdraw(self,side):
        # status passes won/lost?
        print "ENDING QUICKDRAW"
        # set the status to OPEN
        self.game.set_tracking('quickDrawStatus',"OPEN",side)
        self.layer = None
        self.game.base_game_mode.music_on()
        # unload this piece
        self.game.modes.remove(self.game.quickdraw)
        pass