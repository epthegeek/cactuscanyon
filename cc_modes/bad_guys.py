##
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
import random

class BadGuys(game.Mode):
    """BadGuys for great justice - covers QuickDraw, Showdown, and ... ? """
    def __init__(self,game,priority):
        super(BadGuys, self).__init__(game,priority)
        ## here's where things happen
        #self.game = game


    def sw_badGuySW0_active(self,sw):
        # far left bad guy target
        print "BAD GUY 1 HIT"
        self.hit_bad_guy(0)

    def sw_badGuySW1_active(self,sw):
        # center left badguy target
        print "BAD GUY 2 HIT"
        self.hit_bad_guy(1)

    def sw_badGuySW2_active(self,sw):
        # center right bad guy target
        print "BAD GUY 3 HIT"
        self.hit_bad_guy(2)

    def sw_badGuySW3_active(self,sw):
        print "BAD GUY 4 HIT"
        # far right bad guy target
        self.hit_bad_guy(3)

    def hit_bad_guy(self,position):
        # kill the coil to the drop target based on position
        # call back to base to turn on the light for this bad guy?
        # have to add cases for showdown vs quickdraw, right now, is just quickdraw
        self.quickdraw_won()


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
        target = random.choice(choices)
        print "BAD GUY ACTIVE IS: " + str(target)
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
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # Needs the text overlayed on it
        # activate the combined layer
        self.layer = animLayer
        # set the end time based on the config setting
        runtime = self.game.user_settings['Gameplay (Feature)']['Quickdraw Timer']
        # queue up a delay for when the timer should run out if the mode hasn't been won
        self.quickdraw_delay = self.delay(delay=runtime, handler=self.quickdraw_lost)

    def quickdraw_won(self):
        # If the mode is won, we cancel the timer
        self.cancel_delayed(self.quickdraw_delay)
        # kill the mode music
        self.game.sound.stop_music()
        # play the win animation
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-hit.dmd')
        ## todo needs souns
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.layer = animLayer
        myWait = len(anim.frames) / 10.0

        # stuff specific to winning
        # end the quickdraw after the animation bit - and maybe pad for sound
        self.delay(delay=myWait,handler=self.end_quickdraw)

    def quickdraw_lost(self):
        # kill the mode music
        self.game.sound.stop_music()
        # stuff specific to losing
        # if that was the fourth bad guy - showdown should start
        # else just end the quickdraw
        self.end_quickdraw()

    def end_quickdraw(self):
        # status passes won/lost?
        print "ENDING QUICKDRAW"
        # set the status to OPEN
        self.game.set_tracking('quickDrawStatus',"OPEN",self.side)
        # turn off the layer
        self.layer = None
        # play a parting quote?
        # turn the main music back on
        self.game.base_game_mode.music_on()
        # unload this piece
        self.game.modes.remove(self.game.quickdraw)

