##
## This mode controls the mine and multiballs
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes
import ep

class Mine(ep.EP_Mode):
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
        self.hold = False

    def mode_started(self):
        self.update_lamps()

    def mode_stopped(self):
        self.disable_lamps()

    def update_lamps(self):
        self.disable_lamps()
        ## if status is off, we bail here
        lampStatus = self.game.show_tracking('lampStatus')
        if lampStatus != "ON" or self.game.show_tracking('bionicStatus') == "RUNNING":
            return

        stackLevel = self.game.show_tracking('stackLevel')

        eb = self.game.show_tracking('extraBallsPending')
        if eb > 0:
            self.game.lamps.extraBallLitBeacon.enable()
            self.game.lamps.extraBall.schedule(0x0F0F0F0F)
        status = self.game.show_tracking('mineStatus')
        if status == "LOCK":
            self.game.lamps.mineLock.enable()
        # if there is an active 0 or 1 mode, we don't allow multiball to start, so skip the light
        elif status == "READY" and True not in stackLevel[:2]:
            self.game.lamps.mineLock.schedule(0x0F0F0F0F)
        # if there's an extra ball waiting, and the mine status multiball is not running, flash the light
        if eb > 0 and status != "RUNNING":
            self.game.coils.mineFlasher.schedule(0x00100000)
        # if multiball is running and motherload is available - flash the light in the mine and blink the lock arrow
        if status == "RUNNING" and self.game.show_tracking('motherlodeLit'):
            self.game.coils.mineFlasher.schedule(0x00010001)
            self.game.lamps.mineLock.schedule(0x0F0F0F0F)

    def disable_lamps(self):
        self.game.lamps.extraBallLitBeacon.disable()
        self.game.lamps.extraBall.disable()
        self.game.lamps.mineLock.disable()
        self.game.coils.mineFlasher.disable()

        # if the ball lands in the kicker
    def sw_minePopper_active_for_400ms(self,sw):
        if self.game.show_tracking('bionicStatus') == "RUNNING":
            print "WAIT, HOW DID I GET HERE"
            return
        # if MYT is running just kick the ball
        if self.game.move_your_train.running == True:
            self.kick()
        # stock sound for the switch
        if self.game.show_tracking('highNoonStatus') != "READY":
            self.game.sound.play(self.game.assets.sfx_mineKicker)
        # if there's an extra ball waiting, collect one
        if self.game.show_tracking('extraBallsPending') > 0:
            # we'll be busy until this ends
            self.is_busy()
            self.collect_extra_ball()
        # then register the mine shot
        # if we're in a GM multiball, let that mode take it
        if self.game.show_tracking('mineStatus') == "RUNNING":
            self.wait_until_unbusy(self.game.gm_multiball.mine_shot)
        # otherwise handle it locally
        else:
            self.wait_until_unbusy(self.mine_shot)
        ## -- set the last switch hit --
        ep.last_switch = "minePopper"

    def sw_mineEntrance_active(self,sw):
        self.game.mountain.twitch()
        self.game.mountain.flash()
        # play the default sound
        self.game.sound.play(self.game.assets.sfx_mineEntrance)
        # award some points
        self.game.score_with_bonus(2530)
        ep.last_switch = "mineEntrance"
        ## kill the combo shot chain
        ep.last_shot = None


    def mine_shot(self):
        # if high noon is ready, we do that
        if self.game.show_tracking('highNoonStatus') == "READY":
            self.game.modes.add(self.game.high_noon)
            print "STARTING HIGH NOON"
            self.game.high_noon.start_highNoon()
        # otherwise it's a standard hit
        else:
            # first, record the mine shot in the running total
            self.game.increase_tracking('mineShotsTotal')
            # get the balls locked number for use
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
                ## If any level below is running, avoid multiball start
                stackLevel = self.game.show_tracking('stackLevel')
                if True in stackLevel[:2]:
                    self.game.mountain.kick()
                else:
                    self.start_multiball()
            # not start multiball? ok, lock ball perhaps?
            elif self.game.show_tracking('mineStatus') == "LOCK":
                self.lock_ball()
            # still nothing? Hm. Ok, register the hit
            else:
                self.mine_hit(lockedBalls)

    def mine_hit(self,lockedBalls):
        # register the hit
        myMineHits = self.game.increase_tracking('mineHits')
        print "MINE HITS: " + str(myMineHits)
        # now we have to see if that lights the lock
        # subtract the number of hits from the hitsToLight for the current lock position
        hitStatus = self.hitsToLightLock[lockedBalls] - myMineHits
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
            self.mine_update(hitStatus)

    def mine_update(self,hitStatus):
        # award some points ?
        # TODO fancy this up
        print str(hitStatus) + " shots left to light lock"
        # display a "shots left to light lock type thing
        # then kick the ball
        self.game.mountain.eject()

    def light_lock(self):
        # set the lock status
        self.game.set_tracking('mineStatus', "LOCK")
        # clear the hits to light lock
        self.game.set_tracking('mineHits', 0)
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'mine-entrance-border.dmd').frames[0])
        textLine = dmd.TextLayer(56, 9, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("LOCK IS LIT")
        composite = dmd.GroupedLayer(128,32,[backdrop,textLine])
        self.layer = composite
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_lockLit)
        print "LOCK IS LIT ... AND SO AM I"
        ## then kick the ball
        self.update_lamps()
        self.game.mountain.eject()


    def light_multiball(self):
        ## TODO sounds?
        # set the multiball status
        print "MULTIBALL IS LIT"
        self.game.set_tracking('mineStatus', "READY")
        # clear the hits to light
        self.game.set_tracking('mineHits', 0)
        # play a sound?
        # show some display?
        self.update_lamps()
        # then kick the ball
        self.game.mountain.eject()


    def lock_ball(self):
        # tick up the total balls locked because we just locked one
        myBallsLockedTotal = self.game.increase_tracking('ballsLockedTotal')
        # add one to the count of balls currently locked
        myBallsLocked = self.game.increase_tracking('ballsLocked')
        # turn off the lock lit action
        self.game.set_tracking('mineStatus',"OPEN")
        # reset the mine hits
        self.game.set_tracking('mineHits', 0)
        # play the appropriate lock animation
        if myBallsLocked == 1:
            self.play_ball_one_lock_anim()
        else:
            self.play_ball_two_lock_anim()
            # then kick out of the routine
        ## this applies to the easy setting
        ## in the event that the hits to light lock is 0, turn the lock back on right away
        if self.hitsToLightLock[myBallsLockedTotal] == 0:
            ## if two balls are now locked, light multiball
            if myBallsLocked == 2:
                self.game.set_tracking('mineStatus', "READY")
            else:
                self.game.set_tracking('mineStatus',"LOCK")
        self.update_lamps()

    def start_multiball(self):
        # tag on another ball to the locked total, even though it's not really referred to as a lock
        self.game.increase_tracking('ballsLockedTotal')
        # set the status
        self.game.set_tracking('mineStatus', "RUNNING")
        # reset the locked ball count
        self.game.set_tracking('ballsLocked', 0)
        # start multiball!!
        self.game.modes.add(self.game.gm_multiball)
        self.game.gm_multiball.start_multiball()

    def play_ball_one_lock_anim(self,passive=False):
        self.cancel_delayed("Display")
        # stop the music
        print "one lock anim IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        anim = dmd.Animation().load(ep.DMD_PATH+'ball-one-locked.dmd')
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
        self.delay(name="Display",delay=myWait,handler=self.lock_display_text)

    def play_ball_two_lock_anim(self):
        self.cancel_delayed("Display")
        # stop the music
        print "two lock anim IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        anim = dmd.Animation().load(ep.DMD_PATH+'ball-two-locked.dmd')
        # TODO add the sounds to this and determine if it needs listenrs
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        # keyframe some sounds
        animLayer.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.quote_gasp)
        animLayer.add_frame_listener(15,self.game.play_remote_sound,param=self.game.assets.sfx_lockTwoMinecart)
        animLayer.add_frame_listener(32,self.game.play_remote_sound,param=self.game.assets.sfx_lockTwoExplosion)

        # play the animation
        self.layer = animLayer
        self.delay(name="Display",delay=myWait,handler=self.lock_display_text,param=2)

    def lock_display_text(self,lock=1):
        if lock == 1:
            self.game.sound.play(self.game.assets.sfx_orchestraRiff)
        if lock == 2:
            self.game.sound.play(self.game.assets.sfx_lockTwoFlourish)
        textLine = dmd.TextLayer(128/2, 9, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("BALL " + str(self.game.show_tracking('ballsLocked')) + " LOCKED")
        textLine.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[self.layer,textLine])
        # kick the ball (if there's a ball in there) out and clear the layer
        if self.game.switches.minePopper.is_active():
            self.delay(delay=2,handler=self.game.mountain.eject)
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        self.delay(delay=2.1,handler=self.game.base_game_mode.music_on)

    def light_extra_ball(self,callback=None):
        # add the ball to the pending extra balls
        derp = self.game.increase_tracking('extraBallsPending')
        print "EXTRA BALLS PENDING: " + str(derp)
        # turn the light on
        self.update_lamps()
        # setup  a bunch of text
        textLine1 = dmd.TextLayer(28, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("EXTRA")
        textLine2 = dmd.TextLayer(28, 16, self.game.assets.font_9px_az, "center", opaque=False).set_text("BALL")
        textLine3 = ep.pulse_text(self,96,4,"IS")
        textLine4 = ep.pulse_text(self,96,16,"LIT",sequence=[1,3])
        # and a backdrop
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'ball.dmd').frames[0])
        # and the wipe animation
        anim = dmd.Animation().load(ep.DMD_PATH+'horse-wipe-right.dmd')
        myWait = len(anim.frames) / 10.0 + 1
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        animLayer.composite_op = "blacksrc"
        # slap it all together
        composite = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3,textLine4,animLayer])
        # and turn it on
        self.layer = composite
        # with a sound effect
        self.game.sound.play(self.game.assets.sfx_leftLoopEnter)
        # play a quote
        self.game.sound.play(self.game.assets.quote_extraBallLit)
        self.update_lamps()
        # callback process for calling from skill shot
        if callback:
            self.delay(delay=myWait,handler=callback)
        self.delay(delay=myWait,handler=self.clear_layer)
        print "EXTRA BALL LIT"

    def collect_extra_ball(self):
        self.cancel_delayed("Display")
        # stop the music
        print "collect_extra_ball IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # turn off the mine flasher
        # add one to the total of extra balls
        self.game.increase_tracking('extraBallsTotal')
        # take one off of the pending total
        self.game.decrease_tracking('extraBallsPending')
        self.update_lamps()
        # add one to the pending the player for use - using the framework standard for storing extra_balls
        self.game.current_player().extra_balls += 1
        # if they've already gotten an extra ball - it should divert to the short version
        # or if anything above stack level 1 is running
        stack = self.game.show_tracking('stackLevel')
        if self.game.current_player().extra_balls > 1 or True in stack[1:]:
            # play the short one
            self.extra_ball_ending(isLong=False)
        # otherwise play the whole animation
        else:
            # load up the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'extra-ball.dmd')
            # start the full on animation
            myWait = len(anim.frames) / 7.50
            # setup the animated layer
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 8
            # keyframe a bunch of sounds
            animLayer.add_frame_listener(13,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(15,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(17,self.game.play_remote_sound,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(23,self.game.play_remote_sound,param=self.game.assets.quote_whatThe)
            animLayer.add_frame_listener(25,self.game.play_remote_sound,param=self.game.assets.sfx_ebGunfire)
            animLayer.add_frame_listener(41,self.game.play_remote_sound,param=self.game.assets.sfx_ebLookRight)
            animLayer.add_frame_listener(45,self.game.play_remote_sound,param=self.game.assets.sfx_ebLookLeft)
            animLayer.add_frame_listener(46,self.game.play_remote_sound,param=self.game.assets.sfx_ebFallAndCrash)
            # play the intro sounds
            self.game.sound.play(self.game.assets.sfx_ebMusic)
            self.game.sound.play(self.game.assets.quote_thirsty)
            # turn that sucker on
            self.layer = animLayer
            # after a delay, play the ending
            self.delay(delay=myWait,handler=self.extra_ball_ending)

    def extra_ball_ending(self,isLong=True):
        # play a quote
        if isLong:
            # play this quote
            self.game.sound.play(self.game.assets.quote_extraBallGuy)
        else:
            # play this other quote
            self.game.sound.play(self.game.assets.quote_extraBallSet)
        # play a music riff
        self.game.sound.play(self.game.assets.sfx_ebFlourish)
        # setup the backdrop
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'extra-ball.dmd').frames[58])
        textLine = dmd.TextLayer(128/2, 10, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text("EXTRA>  BALL@")
        textLine.composite_op = "blacksrc"
        myLayer = dmd.GroupedLayer(128,32,[backdrop,textLine])
        self.layer = myLayer
        self.delay(delay=3,handler=self.clear_layer)
        self.delay(delay=3,handler=self.unbusy)
        self.delay(delay=3,handler=self.game.base_game_mode.music_on)
        # update lamps to turn on the EB light
        self.game.base_game_mode.update_lamps()

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")





