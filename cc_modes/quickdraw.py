##
## The quickdraw gameplay action extravaganza
##
##
##  Drop Target info:
##  Left to right - 0,1,2,3
##  Switches = badGuySW#
##     Lamps = badGuyL#
##     Coils = badGuyC#

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
        self.side = side
        print "STARTING QUICKDRAW ON SIDE:" + str(side)
        # set the status of this side to running
        self.game.set_tracking('quickDrawStatus',"RUNNING",side)
        # figure out the available bad guys
        choices = []
        count = 0
        for x in self.game.show_tracking('badGuysDead'):
            if not x:
                choices.append(count)
            count += 1

        print "AVAILABLE BAD GUYS"
        print choices
        # pick one of them at random
        # kill the game music
        self.game.sound.stop_music()
        # start the music
        self.game.sound.play(self.game.assets.music_quickDrawBumper)
        self.delay(name="quickdraw music",delay=1.3,handler=self.game.play_remote_music,param=self.game.assets.music_quickDraw)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_quickDrawStart)
        # pop that sucker up
        # TODO doesn't actually pop the sucker up yet
        # Set up the display
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-start.dmd')
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)
        # Needs the text overlayed on it
        # activate the combined layer
        self.layer = animLayer
        # set the end time based on the config setting
        runtime = self.game.user_settings['Gameplay (Feature)']['Quickdraw Timer']
        # queue up a delay for when the timer should run out if the mode hasn't been won
        self.quickdraw_delay = self.delay(delay=runtime, handler=self.quickdraw_lost)

    def sw_badGuySW0_active(self):
        # far left bad guy target
        print "BAD GUY 1 HIT"

    def sw_badGuySW1_active(self):
        # center left badguy target
        print "BAD GUY 2 HIT"

    def sw_badGuySW2_active(self):
        # center right bad guy target
        print "BAD GUY 3 HIT"

    def sw_badGuySW3_active(self):
        print "BAD GUY 4 HIT"
        # far right bad guy target

    def quickdraw_won(self):
        # If the mode is won, we cancel the timer
        self.cancel_delayed(self.quickdraw_delay)

    def quickdraw_lost(self):
        # status passes won/lost?
        print "ENDING QUICKDRAW"
        # kill the mode music
        self.game.sound.stop_music()
        # set the status to OPEN
        self.game.set_tracking('quickDrawStatus',"OPEN",self.side)
        # turn off the layer
        self.layer = None
        # play a parting quote

        self.game.base_game_mode.music_on()
        # unload this piece
        self.game.modes.remove(self.game.quickdraw)
        pass