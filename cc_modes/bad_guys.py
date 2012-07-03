##
##  Bad guy Targets and their lamps
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
import procgame

class BadGuys(game.Mode):
    """BadGuys for great justice - covers Quickdraw, Showdown, and ... ? """
    def __init__(self,game,priority):
        super(BadGuys, self).__init__(game,priority)
        self.coils = [self.game.coils.badGuyC0,
                      self.game.coils.badGuyC1,
                      self.game.coils.badGuyC2,
                      self.game.coils.badGuyC3]
        self.lamps = [self.game.lamps.badGuyL0,
                       self.game.lamps.badGuyL1,
                       self.game.lamps.badGuyL2,
                       self.game.lamps.badGuyL3]
        self.posts = [self.game.coils.leftGunFightPost,
                      self.game.coils.rightGunFightPost]

    def ball_drained(self):
    # just in case, drop all the coils when ball ends
        if self.game.trough.num_balls_in_play == 0:
            self.kill_power()

    def mode_stopped(self):
        self.kill_power()

    def update_lamps(self):
        # reset first
        self.disable_lamps()
        status = self.game.show_tracking('lampStatus')
        if status != "ON":
            return
        # bad guy lights hopefully this sets any lamp that returns true to be on
        for lamp in range(0,4,1):
            status = self.game.show_tracking('badGuysDead',lamp)
            active = self.game.show_tracking('badGuyUp',lamp)
            if status:
                self.lamps[lamp].enable()
            if active:
                self.lamps[lamp].schedule(0x00FF00FF)

    def disable_lamps(self):
        for lamp in self.lamps:
            lamp.disable()


    def sw_badGuySW0_active(self,sw):
        # far left bad guy target
        if self.game.show_tracking('badGuyUp',0):
            print "BAD GUY 0 HIT"
            self.hit_bad_guy(0)

    def sw_badGuySW1_active(self,sw):
        # center left badguy target
        if self.game.show_tracking('badGuyUp',1):
            print "BAD GUY 1 HIT"
            self.hit_bad_guy(1)

    def sw_badGuySW2_active(self,sw):
        # center right bad guy target
        if self.game.show_tracking('badGuyUp',2):
            print "BAD GUY 2 HIT"
            self.hit_bad_guy(2)

    def sw_badGuySW3_active(self,sw):
        # far right bad guy target
        if self.game.show_tracking('badGuyUp',3):
            print "BAD GUY 3 HIT"
            self.hit_bad_guy(3)


    def hit_bad_guy(self,target):
        # stop the timer
        # kill the coil to the drop target based on position
        self.target_down(target)
        # call back to base to turn on the light for this bad guy?
        print "QD STATUS CHECK: " + str(self.game.show_tracking('quickdrawStatus'))
        # If there's a quickdraw running
        if "RUNNING" in self.game.show_tracking('quickdrawStatus'):
            # It's been won
            self.game.quickdraw.won(target)
        # Otherwise, if all badguys are dead, we're in a showdown
        elif self.game.show_tracking('showdownStatus') == "RUNNING":
            print "SHOWDOWN RUNNING OMG"
            self.game.showdown.hit(target)
            # showdown stuff would go here
        elif self.game.show_tracking('ambushStatus') == "RUNNING":
            self.game.ambush.hit(target)
        # option 3 is a gunfight
        else:
            self.game.gunfight.won()

    def target_up(self,target):
        print "TARGET RAISED " + str(target)
        print self.game.show_tracking('badGuyUp')
        self.coils[target].patter(on_time=4,off_time=8,original_on_time=20)
        self.lamps[target].schedule(0x00FF00FF)
        self.delay(delay=0.1,handler=self.target_activate,param=target)

    def target_down(self,target):
        print "DEACTIVATING TARGET " + str(target)
        # we'll still deactivate when the coil goes off, just to maintain sync
        self.game.set_tracking('badGuyUp',False,target)
        self.lamps[target].disable()
        self.delay(delay=0.02,handler=self.coils[target].disable)

    def target_activate(self,target):
        print "ACTIVATING TARGET " + str(target)
        self.game.set_tracking('badGuyUp',True,target)

    def setup_targets(self):
        # pop up the targets
        for i in range(0,4,1):
            self.target_up(i)

    def drop_targets(self):
        # drop all teh targets
        for i in range(0,4,1):
            self.target_down(i)

    def clear_layer(self):
        self.layer = None

    def kill_power(self):
        # stop any delays
        print "BAD_GUYS IS DISPATCHING DELAYS"

        self.dispatch_delayed()
        # drop all the targets
        self.drop_targets()
        for coil in self.posts:
            coil.disable()

