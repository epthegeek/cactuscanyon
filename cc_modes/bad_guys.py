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
        # stop the timer
        # kill the coil to the drop target based on position
        # call back to base to turn on the light for this bad guy?

        # If there's a quickdraw running
        if "RUNNING" in self.game.show_tracking('quickDrawStatus'):
            # kill the timer
            self.cancel_delayed("Timer Delay")
            # It's been won
            self.quickdraw_won()
        # Otherwise, we must be in a showdown.
        else:
            print "QUICKDRAW ISNT RUNNING OMG"
            # showdown stuff would go here

    ###
    ###   ___        _      _       _
    ###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      __
    ### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / /
    ### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /
    ###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/
    ###

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
        # start the mode music
        self.game.sound.play(self.game.assets.music_quickDrawBumper)
        self.delay(name="quickdraw music",delay=1.3,handler=self.game.play_remote_music,param=self.game.assets.music_quickDraw)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_quickDrawStart)
        # pop that sucker up
        # TODO doesn't actually pop the sucker up yet
        # Set up the display
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-start.dmd')
        self.animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # set the end time based on the config setting
        # set up the point value
        value = [500000,750000,1000000,1500000,2000000]
        # based on rank
        rank = self.game.show_tracking('rank')
        self.points = value[rank]
        scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text(ep.format_score(self.points))
        # combine the score and animation and turn it on
        self.layer = dmd.GroupedLayer(128,32,[self.animLayer,scoreLayer])
        # read the run time from the settings
        self.runtime = self.game.user_settings['Gameplay (Feature)']['Quickdraw Timer']
        # set the amount to subtract per 10th of a second
        # I hope this is right - divide the points by 10, divide by 5 times the amount of seconds, times 10 again to get an even number
        # then take off 370 to get a more interesting countdown
        self.portion = ((self.points / 10) / int(self.runtime * 5) * 10) - 370
        # queue up a delay for when the timer should run out if the mode hasn't been won
        # then start the timer after a 1 second grace period
        self.delay(delay=1,handler=self.quickdraw_timer)

    def quickdraw_timer(self):
        # ok, so this has to control the score and display?
        # for now stepping in 1/5 second
        self.runtime -= 0.2
        if self.runtime <= 0:
            self.quickdraw_lost()
        else:
            # take points off the score
            self.points -= self.portion
            # update the score text layer
            scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text(ep.format_score(self.points))
            self.layer = dmd.GroupedLayer(128,32,[self.layer,scoreLayer])
            # update the group layer
            # make it active
            self.layer = dmd.GroupedLayer(128,32,[self.animLayer,scoreLayer])
            # delay the next iteration
            self.delay("Timer Delay", delay = 0.2, handler = self.quickdraw_timer)

    def quickdraw_won(self):
        # kill the mode music
        self.game.sound.stop_music()
        # play the win animation
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-hit.dmd')
        ## todo needs souns
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.layer = animLayer
        myWait = len(anim.frames) / 10.0

        # stuff specific to winning
        # score the points
        self.game.score(self.points)
        # end the quickdraw after the animation bit - and maybe pad for sound
        self.delay(delay=myWait,handler=self.end_quickdraw)

    def quickdraw_lost(self):
        # kill the mode music
        self.game.sound.stop_music()
        # stuff specific to losing
        # TODO if that was the fourth bad guy - showdown should start
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
        self.game.modes.remove(self.game.bad_guys)

    ###
    ###  ____  _                      _
    ### / ___|| |__   _____      ____| | _____      ___ __
    ### \___ \| '_ \ / _ \ \ /\ / / _` |/ _ \ \ /\ / / '_ \
    ###  ___) | | | | (_) \ V  V / (_| | (_) \ V  V /| | | |
    ### |____/|_| |_|\___/ \_/\_/ \__,_|\___/ \_/\_/ |_| |_|
    ###