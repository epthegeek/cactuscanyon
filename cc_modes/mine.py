##
## This mode controls the mine and multiballs
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes

class Mine(game.Mode):
    """Game mode for controlling the mine and such"""
    def __init__(self, game,priority):
        super(Mine, self).__init__(game, priority)
        # set the hits to light the lock based on the config option
        # Settings are in triplets of "light lock 1, light lock 2, light multiball"
        # the last digit is for every step after The 'balls locked total' tracking item
        # can be used to get the digit
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # Easy version
        print "Difficulty is set to - " + difficulty
        if difficulty == 'Easy':
            self.hitsToLightLock = [1,0,0,1,1,1,2,2,2,3]
        # Hard version
        else:
            self.hitsToLightLock = [1,1,1,2,2,2,3,3,3,4]



    # if the ball lands in the kicker
    def sw_minePopper_closed_for_200ms(self,sw):
        # first, record the mine shot in the running total
        self.game.increase_tracking('mineShotsTotal')
        # set the balls locked number for use
        lockedBalls = self.game.show_tracking('ballsLockedTotal')
        # if it's over 9, cap it back to 9
        if lockedBalls > 9:
            lockedBalls = 9
        print "LOCKED BALLS: " + str(lockedBalls)
        # check if we should lock the ball or start multiball
        # should we start multiball?
        # multiball itself will be a separate mode with switchstop that loads above this
        # so we don't have to handle 'RUNNING' here
        if self.game.show_tracking('mineStatus') == "READY":
            self.start_multiball()
        # not start multiball? ok, lock ball perhaps?
        elif self.game.show_tracking('mineStatus') == "LOCK":
            self.lock_ball()
        # still nothing? Hm. Ok, register the hit
        else:
            # register the hit
            self.game.increase_tracking('mineHits')
            print "MINE HITS: " + str(self.game.show_tracking('mineHits'))
            # now we have to see if that lights the lock
            # subtract the number of hits from the hitsToLight for the current lock position
            hitStatus = self.hitsToLightLock[lockedBalls] - self.game.show_tracking('mineHits')
            # if that's zero (or god forbid, less) then light the lock
            print "HITS TO LIGHT THIS LOCK: " + str(self.hitsToLightLock[lockedBalls])
            print "HITSTATUS: " + str(hitStatus)
            if hitStatus <= 0:
                ## Ok so we're lighting something
                if self.game.show_tracking('ballsLocked') == 2:
                    # if 2 balls are locked, light multiball
                    self.light_multiball()
                else:
                    # otherwise just light the next lock
                    self.light_lock()
            # if we haven't hit our total hits needed yet move on
            else:
                # award some points
                print str(hitStatus) + " shots left to light lock"
        # kick the ball out
        print "PULSE THE MINE KICKER"

    def sw_mineEntrance_active(self,sw):
        pass

    def light_lock(self):
        # set the lock status
        self.game.set_tracking('mineStatus', "LOCK")
        # clear the hits to light lock
        self.game.set_tracking('mineHits', 0)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_lockLit)
        print "LOCK IS LIT ... AND SO AM I"
        ## TODO lights and sounds

    def light_multiball(self):
        ## TODO lights and sounds
        # set the multiball status
        print "MULTIBALL IS LIT"
        self.game.set_tracking('mineStatus', "READY")
        # clear the hits to light
        self.game.set_tracking('mineHits', 0)

    def lock_ball(self):
        # tick up the total balls locked because we just locked one
        self.game.increase_tracking('ballsLockedTotal')
        # add one to the count of balls currently locked
        self.game.increase_tracking('ballsLocked')
        # turn off the lock lit action
        self.game.set_tracking('mineStatus',"OPEN")
        # reset the mine hits
        self.game.set_tracking('mineHits', 0)
        # play the appropriate lock animation

        if self.game.show_tracking('ballsLocked') == 1:
            self.play_ball_one_lock_anim()
        else:
            self.play_ball_two_lock_anim()
            # then kick out of the routine
        ## this applies to the easy setting
        ## in the event that the hits to light lock is 0, turn the lock back on right away
        if self.hitsToLightLock[self.game.show_tracking('ballsLockedTotal')] == 0:
            ## if two balls are now locked, light multiball
            if self.game.show_tracking('ballsLocked') == 2:
                self.game.set_tracking('mineStatus', "READY")
            else:
                self.game.set_tracking('mineStatus',"LOCK")

    def start_multiball(self):
        # tag on another ball to the locked total, even though it's not really referred to as a lock
        self.game.increase_tracking('ballsLockedTotal')
        # set the status
        self.game.set_tracking('mineStatus', "RUNNING")
        # reset the locked ball count
        self.game.set_tracking('ballsLocked', 0)
        # start multiball!!
        # TODO a thing would go here like self.game.modes.add(self.game.multiball)
        # for now we'll just print a thing
        print "MULTIBALL STARTING"
        # and wait a bit to turn it off, that'd be cool, right?
        self.delay(delay=3,handler=self.temp_end_multiball)

    def temp_end_multiball(self):
        self.game.set_tracking('mineStatus','OPEN')
        print "MULTIBALL ENDED"

    def play_ball_one_lock_anim(self):
        anim = dmd.Animation().load(self.game.assets.anim_ballOneLocked)
        # TODO add the sounds to this and determine if it needs listenrs
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the first sound
        self.game.sound.play(self.game.assets.sfx_ballOneLock)
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # play the animation
        self.layer = animLayer
        self.delay(delay=1,handler=self.game.play_remote_sound,param=self.game.assets.quote_pollyHelp)
        self.delay(delay=myWait,handler=self.lock_display_text)

    def play_ball_two_lock_anim(self):
        anim = dmd.Animation().load(self.game.assets.anim_ballTwoLocked)
        # TODO add the sounds to this and determine if it needs listenrs
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the first sound
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # play the animation
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.clear_layer)

    def lock_display_text(self):
        self.game.sound.play(self.game.assets.sfx_orchestraRiff)
        textLine = dmd.TextLayer(128/2, 9, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("BALL " + str(self.game.show_tracking('ballsLocked')) + " LOCKED")
        textLine.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[self.layer,textLine])
        self.delay(delay=2,handler=self.clear_layer)

    def clear_layer(self):
        self.layer = None




