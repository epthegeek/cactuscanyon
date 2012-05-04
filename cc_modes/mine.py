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
        if difficulty == 'Easy':
            self.hitsToLightLock = [1,0,0,1,1,1,2,2,2,3]
        # Hard version
        else:
            self.hitsToLightLock = [1,1,1,2,2,2,3,3,3,4]

        # start the hits count at 0
        self.hits = 0


    # if the ball lands in the kicker -- for now, just get it out again
    def sw_minePopper_closed_for_200ms(self,sw):
        print "PULSE THE KICKER FOR THE MINE"
        # check if we should lock the ball or start multiball
        # kick the ball out

    def sw_mineEntrance_active(self,sw):
        pass

    def light_lock(self):
        # set the lock status
        self.game.set_tracking('isLockLit', True)
        # clear the its to light lock
        self.game.set_tracking('mineHits', 0)
        ## TODO lights and sounds

    def light_multiball(self):
        # set the multiball status
        self.game.set_tracking('isMultiballLit', True)
        # clear the hits to light
        self.game.set_tracking('mineHits', 0)
        ## TODO lights and sounds

    def lock_ball(self):
        # tick up the total balls locked because we just locked one
        self.game.increase_tracking('ballsLockedTotal')
        # add one to the count of balls currently locked
        self.game.increase_tracking('ballsLocked')
        # turn off the lock lit action
        self.game.set_tracking('isLockLit',False)
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
                self.game.set_tracking('isMultiballLit', True)
            else:
                self.game.set_tracking('isLockLit',True)

    def play_ball_one_lock_anim(self):
        anim = dmd.Animation().load(self.game.assets.anim_ballOneLocked)
        # TODO add the sounds to this and determine if it needs listenrs
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the first sound
        self.game.sound.play(self.game.assets.sfx_ballOneLock)
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # added a frame listener for the second sound effect
        #animLayer.add_frame_listener(5, self.play_stage_one_sound)
        # play the animation
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.lock_display_text)

    def play_ball_two_lock_anim(self):
        anim = dmd.Animation().load(self.game.assets.anim_ballTwoLocked)
        # TODO add the sounds to this and determine if it needs listenrs
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the first sound
        #self.game.sound.play(self.game.assets.sfx_explosion1)
        #self.game.sound.play(self.game.assets.quote_mayorMyMoneysInThere)
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # added a frame listener for the second sound effect
        #animLayer.add_frame_listener(5, self.play_stage_one_sound)
        # play the animation
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.clear_layer)

    def lock_display_text(self):
        self.game.sound.play(self.game.assets.sfx_orchestraRiff)
        textLine = dmd.TextLayer(128/2, 10, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("BALL " + str(self.game.show_tracking('ballsLocked')) + " LOCKED")
        textLine.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[self.layer,textLine])
        self.delay(delay=2,handler=self.clear_layer)

    def clear_layer(self):
        self.layer = None




