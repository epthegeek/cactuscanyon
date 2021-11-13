##   ____           _                ____
##  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
## | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
## | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
##  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
##                                                   |___/
##           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
##          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
##         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
##          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
##
## A P-ROC Project by Eric Priepke, Copyright 2012-2013
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## This mode controls the mine and multiballs
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import dmd
import ep
import random

class Mine(ep.EP_Mode):
    """Game mode for controlling the mine and such"""
    def __init__(self, game,priority):
        super(Mine, self).__init__(game, priority)
        self.myID = "Mine"
        # set the hits to light the lock based on the config option
        # Settings are in triplets of "light lock 1, light lock 2, light multiball"
        # the last digit is for every step after The 'balls locked total' tracking item
        # can be used to get the digit
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # Easy version
        #print "Difficulty is set to - " + difficulty
        if difficulty == 'Easy':
            self.hitsToLightLock = [1,0,0,1,1,1,2,2,2,3]
        # Hard version
        else:
            self.hitsToLightLock = [1,1,1,2,2,2,3,3,3,4]
        self.hold = False
        self.callback = None
        self.collectingEB = False
        self.lockAnimation = False
        self.keys_index = {'lit_extra_ball':list(range(len(self.game.sound.sounds[self.game.assets.quote_extraBallLit])))}
        self.counts_index = {'lit_extra_ball':0}
        random.shuffle(self.keys_index['lit_extra_ball'])

        # if the ball lands in the kicker
    def sw_minePopper_active_for_400ms(self,sw):
        # somehow this falls through despite switch stop
        # do nothing if there's an active super on the mine
        if self.game.skill_shot.wasActive == 3:
            self.game.skill_shot.wasActive = 0
            return
        # for MMB just kick out and last call
        if self.game.marshall_multiball.running or self.game.last_call.running or self.game.moonlight.running:
            self.game.mountain.eject()
            return
        # for bionic & cva - still collect extra ball
        if self.game.show_tracking('bionicStatus') == "RUNNING" or \
           self.game.show_tracking('cvaStatus') == "RUNNING" or \
           self.game.high_noon.running or \
           self.game.showdown.running or \
           self.game.ambush.running or \
           self.game.stampede.running:
            # if there's an extra ball pending, award it
            eb = self.game.show_tracking('extraBallsPending')
            if eb > 0:
                # force the short extra ball collect
                self.collect_extra_ball(type=1)
            self.game.mountain.eject()
            return
        # stock sound for the switch
        if self.game.show_tracking('highNoonStatus') != "READY" and self.game.show_tracking('mineStatus') != "RUNNING":
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
        # new routine to move the mine to open and stay there until hit
        if self.game.mountain.mineTicks < 8 and not self.game.mountain.inMotion:
            self.game.mountain.move()
        self.game.mountain.flash()
        # play the default sound
        self.game.sound.play(self.game.assets.sfx_mineEntrance)
        # award some points
        self.game.score(2530,bonus=True)
        ep.last_switch = "mineEntrance"
        ## kill the combo shot chain
        ep.last_shot = None

    def mine_shot(self):
        stackLevel = self.game.show_tracking('stackLevel')
        #print stackLevel

        # if cva is ready, we do that - as long as no mode above guns is running
        if self.game.show_tracking('cvaStatus') == "READY" and True not in stackLevel[1:] and not self.game.bart.bossFight:
            self.game.mountain.busy = True
            self.game.modes.add(self.game.cva)
            self.game.cva.intro(entry = "mine")
            return
        # if high noon is ready, we do that - as long as no mode at all is running
        if self.game.show_tracking('highNoonStatus') == "READY" and True not in stackLevel[1:]:
            # if quickdraw is running, kill that
            if self.game.quickdraw.running:
                self.game.quickdraw.lost(self.game.quickdraw.target)
            self.game.modes.add(self.game.high_noon)
            #print "STARTING HIGH NOON"
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
            #print "LOCKED BALLS: " + str(lockedBalls)
            # check if we should lock the ball or start multiball
            # if multiball is running - that handles hits to the mine
            if self.game.show_tracking('mineStatus') == "RUNNING":
                pass
            # if ready, we might have to start it
            elif self.game.show_tracking('mineStatus') == "READY":
                # if CVA, Bionic Bart or High Noon are running, just kick back out
                if True in stackLevel[5:]:
                    self.game.mountain.kick()
                else:
                    # if DMB is running, and stacking is disabled - don't start Goldmine
                    if self.game.drunk_multiball.running and not self.game.base.drunkStacking:
                        self.game.mountain.kick()
                    elif self.game.ambush.running or self.game.showdown.running:
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
        #print "MINE HITS: " + str(myMineHits)
        # now we have to see if that lights the lock
        # subtract the number of hits from the hitsToLight for the current lock position
        hitStatus = self.hitsToLightLock[lockedBalls] - myMineHits
        # if that's zero (or god forbid, less) then light the lock
        #print "HITS TO LIGHT THIS LOCK: " + str(self.hitsToLightLock[lockedBalls])
        #print "HITSTATUS: " + str(hitStatus)
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
        #print str(hitStatus) + " shots left to light lock"
        # display a "shots left to light lock type thing
        textLine = str(hitStatus) + " MORE TO"
        textLine2 = "LIGHT LOCK"
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mineEntranceBorder.frames[0])
        textLayer = dmd.TextLayer(56, 2, self.game.assets.font_9px_az, "center", opaque=False).set_text(textLine)
        textLayer2 = dmd.TextLayer(56, 13, self.game.assets.font_9px_az, "center", opaque=False).set_text(textLine2)
        textLayer2.composite_op = "blacksrc"
        composite = dmd.GroupedLayer(128,32,[backdrop,textLayer,textLayer2])
        self.layer = composite
        # then kick the ball
        self.game.mountain.eject()
        # clear layer in 2
        self.delay(name="Display",delay = 2, handler=self.clear_layer)

    def light_lock(self):
        # set the lock status
        self.game.set_tracking('mineStatus', "LOCK")
        # clear the hits to light lock
        self.game.set_tracking('mineHits', 0)
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mineEntranceBorder.frames[0])
        textLine = ep.EP_TextLayer(56, 9, self.game.assets.font_12px_az, "center", opaque=False).set_text("LOCK IS LIT",color=ep.GREEN)
        composite = dmd.GroupedLayer(128,32,[backdrop,textLine])
        self.layer = composite
        self.delay(name="Display",delay=1.5,handler=self.clear_layer)
        # play a quote
        duration = self.game.base.priority_quote(self.game.assets.quote_lockLit)
        #print "LOCK IS LIT ... AND SO AM I"
        ## then kick the ball
        self.lamp_update()
        self.delay(delay=duration + 0.5,handler=self.game.mountain.eject)


    def light_multiball(self):
        # set the multiball status
        #print "MULTIBALL IS LIT"
        self.game.set_tracking('mineStatus', "READY")
        # clear the hits to light
        self.game.set_tracking('mineHits', 0)
        # play a sound?
        self.game.base.priority_quote(self.game.assets.quote_mineOpen)
        # show some display?
        self.lamp_update()
        # then kick the ball
        self.game.mountain.eject()


    def lock_ball(self,myCallback=None):
        # if we got a callback, set that self so we can use it later
        if myCallback:
            self.callback = myCallback
        # tick up the total balls locked because we just locked one
        myBallsLockedTotal = self.game.increase_tracking('ballsLockedTotal')
        # add one to the count of balls currently locked
        myBallsLocked = self.game.increase_tracking('ballsLocked')
        # turn off the lock lit action
        self.game.set_tracking('mineStatus',"OPEN")
        # reset the mine hits
        self.game.set_tracking('mineHits', 0)
        # play the appropriate lock animation
        self.lockAnimation = True
        if myBallsLocked == 1:
            self.play_ball_one_lock_anim()
        else:
            self.play_ball_two_lock_anim()
            # then kick out of the routine
        ## this applies to the easy setting
        ## in the event that the hits to light lock is 0, turn the lock back on right away
        ## have to cap the myBallsLockedTotal at 9 for this
        if myBallsLockedTotal > 9:
            myBallsLockedTotal = 9
        # then we check for zeros
        if self.hitsToLightLock[myBallsLockedTotal] == 0:
            ## if two balls are now locked, light multiball
            if myBallsLocked >= 2:
                self.game.set_tracking('mineStatus', "READY")
            else:
                self.game.set_tracking('mineStatus',"LOCK")
        ## if there's more than one shot needed to lock the next ball, home the mountain
        else:
            self.game.mountain.reset_toy()

        self.lamp_update()

    def start_multiball(self):
        # tag on another ball to the locked total, even though it's not really referred to as a lock
        self.game.increase_tracking('ballsLockedTotal')
        # set the status
        self.game.set_tracking('mineStatus', "RUNNING")
        # tick up the count of times GoldMine Started
        self.game.increase_tracking('goldMineStarted')
        # reset the locked ball count
        self.game.set_tracking('ballsLocked', 0)
        # start multiball!!
        self.game.modes.add(self.game.gm_multiball)
        self.game.gm_multiball.start_multiball()

    def play_ball_one_lock_anim(self,passive=False):
        self.cancel_delayed("Display")
        # quiet the music
        self.game.squelch_music()
        anim = self.game.assets.dmd_lockOne
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # play the first sound
        self.game.sound.play(self.game.assets.sfx_ballOneLock)
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        # play the animation
        self.layer = animLayer
        self.lockedNumber = 1
        self.delay("Lock Anim",delay=1,handler=self.game.base.play_quote,param=self.game.assets.quote_pollyHelp)
        self.delay("Display",delay=myWait,handler=self.lock_display_text)

    def play_ball_two_lock_anim(self):
        self.cancel_delayed("Display")
        # quiet the music
        self.game.squelch_music()
        anim = self.game.assets.dmd_lockTwo
        # calcuate the wait time to start the next part of the display
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        animLayer.opaque = True
        # keyframe some sounds
        animLayer.add_frame_listener(2,self.game.base.play_quote,param=self.game.assets.quote_gasp)
        animLayer.add_frame_listener(15,self.game.sound.play,param=self.game.assets.sfx_lockTwoMinecart)
        animLayer.add_frame_listener(32,self.game.sound.play,param=self.game.assets.sfx_lockTwoExplosion)
        animLayer.add_frame_listener(32,self.game.base.red_flasher_flourish)

        # play the animation
        self.layer = animLayer
        self.lockedNumber = 2
        self.delay("Display",delay=myWait,handler=self.lock_display_text,param=self.lockedNumber)

    def abort_lock_animation(self):
        self.cancel_delayed("Display")
        self.cancel_delayed("Lock Anim")
        self.lockAnimation = False
        self.lock_display_text(self.lockedNumber)

    def lock_display_text(self,lock=1):
        self.lockAnimation = False
        if lock == 1:
            self.game.sound.play(self.game.assets.sfx_orchestraRiff)
        if lock == 2:
            self.game.sound.play(self.game.assets.sfx_lockTwoFlourish)
        textLine = ep.EP_TextLayer(128/2, 9, self.game.assets.font_12px_az_outline, "center", opaque=False)
        textLine.composite_op = "blacksrc"
        textLine.set_text("BALL " + str(self.game.show_tracking('ballsLocked')) + " LOCKED",color=ep.GREEN)
        if self.layer == None:
            self.layer = self.no_layer()

        self.layer = dmd.GroupedLayer(128,32,[self.layer,textLine])
        # kick the ball (if there's a ball in there) out and clear the layer
        if self.game.switches.minePopper.is_active():
            self.delay(delay=2,handler=self.game.mountain.eject)
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        self.delay(delay=2.1,handler=self.game.restore_music)
        #if we had a callback, process that - it's for the skillshot ending
        if self.callback:
            self.delay(delay=2,handler=self.callback)
            # then clear the callback
            self.callback = None

    def light_extra_ball(self,callback=None):
        # add the ball to the pending extra balls
        derp = self.game.increase_tracking('extraBallsPending')
        #print "EXTRA BALLS PENDING: " + str(derp)
        # audit tick
        self.game.game_data['Audits']['Extra Balls Earned'] += 1
        # open the mine
        if self.game.mountain.mineTicks != 8:
            self.game.mountain.full_open()
        # setup  a bunch of text
        textLine1 = ep.EP_TextLayer(28, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("EXTRA",color=ep.ORANGE)
        textLine2 = ep.EP_TextLayer(28, 16, self.game.assets.font_9px_az, "center", opaque=False).set_text("BALL",color=ep.ORANGE)
        textLine3 = ep.pulse_text(self,96,4,"IS",color=ep.GREEN)
        textLine4 = ep.pulse_text(self,96,16,"LIT",sequence=[1,3],color=ep.GREEN)
        # and a backdrop
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_ball.frames[0])
        # and the wipe animation
        anim = self.game.assets.dmd_horseWipeRight
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
        self.play_ordered_quote(self.game.assets.quote_extraBallLit,'lit_extra_ball')
        self.lamp_update()
        # callback process for calling from skill shot
        if callback:
            self.delay(delay=myWait,handler=callback)
        self.delay("Display",delay=myWait,handler=self.clear_layer)
        #print "EXTRA BALL LIT"

    def collect_extra_ball(self,type=0):
        self.cancel_delayed("Display")
        # stop the music
        self.game.squelch_music()
        # turn off the mine flasher ?
        # add one to the total of extra balls
        ebt = self.game.increase_tracking('extraBallsTotal')
        #print "Extra balls total: " + str(ebt)
        # take one off of the pending total
        self.game.decrease_tracking('extraBallsPending')
        self.lamp_update()
        # add one to the pending the player for use - using the framework standard for storing extra_balls
        self.game.current_player().extra_balls += 1
        # if they've already gotten an extra ball - it should divert to the short version
        # or if anything above stack level 1 is running
        stack = self.game.show_tracking('stackLevel')
        if self.game.current_player().extra_balls > 1 or True in stack[1:] or self.game.show_tracking('bozoBall') or type == 1:
            # play the short one
            self.extra_ball_ending(isLong=False)
        # otherwise play the whole animation
        else:
            # set the flag here for being able to abort
            self.collectingEB = True
            # load up the animation
            anim = self.game.assets.dmd_extraBall
            # start the full on animation
            myWait = len(anim.frames) / 7.50
            # setup the animated layer
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 8
            animLayer.opaque = True
            # keyframe a bunch of sounds
            animLayer.add_frame_listener(13,self.game.sound.play,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(15,self.game.sound.play,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(17,self.game.sound.play,param=self.game.assets.sfx_ebDrink)
            animLayer.add_frame_listener(23,self.game.base.play_quote,param=self.game.assets.quote_whatThe)
            animLayer.add_frame_listener(25,self.game.sound.play,param=self.game.assets.sfx_ebGunfire)
            animLayer.add_frame_listener(25,lambda: self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.game.lamp_control.feature_lamps_on))
            animLayer.add_frame_listener(41,self.game.sound.play,param=self.game.assets.sfx_ebLookRight)
            animLayer.add_frame_listener(45,self.game.sound.play,param=self.game.assets.sfx_ebLookLeft)
            animLayer.add_frame_listener(46,self.game.sound.play,param=self.game.assets.sfx_ebFallAndCrash)
            animLayer.add_frame_listener(46,lambda: self.game.lampctrl.play_show(self.game.assets.lamp_wipeToBottom, repeat=False,callback=self.lamp_update))
            # play the intro sounds
            self.game.sound.play(self.game.assets.sfx_ebMusic)
            self.game.base.play_quote(self.game.assets.quote_thirsty)
            # turn that sucker on
            self.layer = animLayer
            # after a delay, play the ending
            self.delay("Collecting",delay=myWait,handler=self.extra_ball_ending)
            # update lamps to turn on the EB light
            self.lamp_update()
        # Disable the bozo ball if one was awarded some other way
        self.game.set_tracking('bozoBall',False)

    def extra_ball_ending(self,isLong=True):
        # reset the collecting flagg for later
        self.collectingEB = False
        # hit the knocker
        self.game.interrupter.knock(1,realOnly = True)
        # play a quote
        if isLong:
            # play this quote
            self.game.base.priority_quote(self.game.assets.quote_extraBallGuy)
        else:
            # play this other quote
            self.game.base.priority_quote(self.game.assets.quote_extraBallSet)
        # play a music riff
        self.game.sound.play(self.game.assets.sfx_ebFlourish)
        # setup the backdrop
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_extraBall.frames[58])
        textLine = ep.EP_TextLayer(128/2, 10, self.game.assets.font_12px_az_outline, "center", opaque=False)
        textLine.composite_op ="blacksrc"
        textLine.set_text("EXTRA   BALL",color=ep.GREEN)
        myLayer = dmd.GroupedLayer(128,32,[backdrop,textLine])
        self.layer = myLayer
        # turn off the bozo ball if it's on
        if self.game.show_tracking('bozoBall'):
            self.game.base.disable_bozo_ball()
        self.delay(delay=3,handler=self.clear_layer)
        self.delay(delay=3,handler=self.unbusy)
        self.delay(delay=3,handler=self.game.restore_music)

    def abort_extra_ball(self):
        #print "Aborting extra ball display"
        self.collectingEB = False
        self.clear_layer()
        self.cancel_delayed("Collecting")
        self.extra_ball_ending(False)

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
        # kick teh ball out of the mine if there's one in there
        if self.game.switches.minePopper.is_active():
            self.game.mountain.eject()





