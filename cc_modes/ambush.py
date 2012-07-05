###
### Ambush
###


from procgame import *
import cc_modes
import ep
import random


class Ambush(game.Mode):
    """Showdown code """
    def __init__(self,game,priority):
        super(Ambush, self).__init__(game,priority)
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]

        self.targetNames = ['Left','Left Center','Right Center','Right']
        # setup the standing guys
        self.guyLayers = []
        self.badGuy0 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd').frames[0])
        self.badGuy0.set_target_position(-49,0)
        self.badGuy0.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy0)
        self.badGuy1 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd').frames[0])
        self.badGuy1.set_target_position(-16,0)
        self.badGuy1.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy1)
        self.badGuy2 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd').frames[0])
        self.badGuy2.set_target_position(15,0)
        self.badGuy2.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy2)
        self.badGuy3 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd').frames[0])
        self.badGuy3.set_target_position(47,0)
        self.badGuy3.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy3)
        ## lamps
        self.lamps = [self.game.lamps.badGuyL0,
                      self.game.lamps.badGuyL1,
                      self.game.lamps.badGuyL2,
                      self.game.lamps.badGuyL3]
        # number of guys that can escape before you lose
        self.LOSE = self.game.user_settings['Gameplay (Feature)']['Ambush Escapes to Lose']
        # how long the bad guys wait before disappearing
        self.SECONDS = self.game.user_settings['Gameplay (Feature)']['Ambush Target Timer']

    # bumpers pause ambush
    def sw_leftJetBumper_active(self,sw):
            self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
            self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
            self.bumper_hit('bottom')

    # so does the mine
    def sw_minePopper_active_for_400ms(self,sw):
        self.pause()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.paused:
            self.paused = False
            self.resume()

    def bumper_hit(self,bumper):
        if not self.paused:
            self.pause()

    def mode_started(self):
        self.deathTally = 0
        self.showdownValue = 300000
        self.tauntTimer = 0
        self.availableBadGuys = [0,1,2,3]
        self.activatedBadGuys = []
        self.misses = 0
        self.badGuyTimer = [None,None,None,None]
        self.busy = False
        self.paused = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('ambushStatus') == "RUNNING":
            self.end_ambush()

    def start_ambush(self,side):
        # raise the post to hold the ball
        self.activeSide = side
        self.posts[self.activeSide].patter(on_time=4,off_time=12,original_on_time=30)

        print "A M B U S H"
        # kill the music
        self.game.sound.stop_music()
        # set the layer tracking
        self.game.set_tracking('stackLevel',True,0)
        # set the showdown tracking
        self.game.set_tracking('ambushStatus', "RUNNING")
        # kill the GI
        self.game.gi_control("OFF")
        # turn off the bad guy lights
        for lamp in self.lamps:
            lamp.disable()
        # things, they go here
        self.deathTally = 0
        # play a startup animation
        anim = dmd.Animation().load(ep.DMD_PATH+'ambush.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        # keyframe sounds
        animLayer.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.sfx_lightning1)
        animLayer.add_frame_listener(2,self.lightning,param="top")
        animLayer.add_frame_listener(4,self.lightning,param="top")
        animLayer.add_frame_listener(5,self.lightning,param="left")
        animLayer.add_frame_listener(8,self.game.play_remote_sound,param=self.game.assets.sfx_lightningRumble)
        animLayer.add_frame_listener(8,self.lightning,param="top")
        animLayer.add_frame_listener(10,self.lightning,param="top")
        animLayer.add_frame_listener(11,self.lightning,param="left")
        # setup the display
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.get_going)
        self.taunt_timer()

    def taunt_timer(self):
        # tick up by one
        self.tauntTimer += 1
        # if it's been long enough, play a taunt ant reset
        if self.tauntTimer >= 9:
            # play a taunt quote
            self.game.sound.play(self.game.assets.quote_mobTaunt)
            self.tauntTimer = 0
        self.delay(name="Taunt Timer",delay=1,handler=self.taunt_timer)

    def get_going(self):
        self.game.play_remote_sound(self.game.assets.quote_mobStart)
        # turn the GI back on
        self.game.gi_control("ON")
        # start the music
        self.game.base_game_mode.music_on(self.game.assets.music_showdown)
        # kick out more ball
        #self.game.trough.launch_balls(1)
        # add two dudes - one here, one later
        self.busy = True
        self.add_guys(1)
        # drop the post
        self.posts[self.activeSide].disable()

        # delay adding the second guy for 2 seconds to stagger them a bit
        self.delay(delay=2,handler=self.add_guys,param=1)

    def add_guys(self,amount):
        # for adding dudes to the ambush
        # pick a guy from the available targets
        dude = random.choice(self.availableBadGuys)
        # activate target
        self.activate_guy(dude)
        # pop that target up
        self.game.bad_guys.target_up(dude)
        # start a timer for that target
        self.badGuyTimer[dude] = self.SECONDS
        self.targetTimer(dude)
        # reduce count of dudes to start by 1
        amount -= 1
        self.update_display()
        # if there are some left, repeat in 1 second to avoid popping them all up at once
        if amount != 0:
            self.delay(name="Add Guys",delay=.5,handler=self.add_guys,param=amount)
        else:
            self.busy = False

    def pause(self):
        # if we're already paused, skip this
        if self.paused:
            pass
        # if we're not - set the pause flag and cancel timers
        else:
            self.paused = True
            # loop through and cancel all the target timers
            for target in range(0,4,1):
                if self.badGuyTimer[target] != 0 and self.badGuyTimer[target] != None:
                    print "CANCEL TIMER: " + self.targetNames[target] + " HAD: " + str(self.badGuyTimer[target])
                    self.cancel_delayed(self.targetNames[target])
            textString = "< AMBUSH PAUSED >"
            self.layer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)


    def resume(self):
        for target in range(0,4,1):
            # loop through and restart any timer that has value
            if self.badGuyTimer[target] != 0 and self.badGuyTimer[target] != None:
                print "RESTARTING TARGET: " + str(target) + " TIME: " + str(self.badGuyTimer[target])
                self.targetTimer(target)
        self.update_display()

    def targetTimer(self,target):
        # tick one off the timer for that target
        self.badGuyTimer[target] -= 1
        print "TIMER WORKING ON TARGET: " + str(target) + " - TIME: " + str(self.badGuyTimer[target])
        # if the time is almost up change the light schedule
        if self.badGuyTimer[target] == 1:
            self.lamps[target].schedule(0x0F0F0F0F)
        # if he's out of time, he shoots back and goes away
        if self.badGuyTimer[target] <= 0:
            self.guy_escapes(target)
        # if he has time left, come back later
        else:
            self.delay(name=self.targetNames[target],delay=1,handler=self.targetTimer,param=target)

    def poller(self):
        # this checks how many guys are up and adds more if needed
        if not self.busy:
            # default is 2 dudes
            amount = 2
            # if we're at or above 5 kills, go to three
            if self.deathTally >= 5:
                amount += 1
            # if we're at or above 9, add another
            if self.deathTally >= 9:
                amount += 1
            # we should add whatever it takes to get back to amount
            thisMany = amount - len(self.activatedBadGuys)
            # if we need to add some, fire away - if we haven't lost yet
            if thisMany != 0 and self.misses < self.LOSE:
                # turn on the busy flag to stop the poller while adding
                self.busy = True
                self.add_guys(thisMany)

    def update_display(self,killed=99,escaped=99):
        # have to load the animations here so they can be used more than once

        ## setup the shot guys
        shotLayers = []
        shotguy = dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd')
        escapeLayers = []
        guyShoots = dmd.Animation().load(ep.DMD_PATH+'dude-shoots.dmd')
        for position in [-49,-16,15,47]:
            # the gets shot animation per position
            deadGuy0 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            deadGuy0.set_target_position(position,0)
            deadGuy0.composite_op = "blacksrc"
            shotLayers.append(deadGuy0)
            # the shoots back animation per position
            eGuy0 = ep.EP_AnimatedLayer(guyShoots)
            eGuy0.hold=True
            eGuy0.frame_time=6
            eGuy0.set_target_position(position,0)
            eGuy0.composite_op = "blacksrc"
            eGuy0.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.sfx_explosion11)
            eGuy0.add_frame_listener(4,self.game.play_remote_sound,param=self.game.assets.sfx_explosion11)
            # on any escape other than the last one, taunt the player - the last one would get stepped on by the final quote
            if self.misses != self.LOSE:
                eGuy0.add_frame_listener(5,self.game.play_remote_sound,param=self.game.assets.quote_gunFail)
            escapeLayers.append(eGuy0)

        # loop through the up bad guys and add them to the display
        activeLayers = []
        for x in self.activatedBadGuys:
            activeLayers.append(self.guyLayers[x])
        # if we're here because someone got killed, add them to the layers to die
        if killed != 99:
            activeLayers.append(shotLayers[killed])
            # play a shot sound
            self.game.sound.play(self.game.assets.sfx_gunfightShot)
        if escaped != 99:
            activeLayers.append(escapeLayers[escaped])
            amount = self.LOSE - self.misses
            self.game.base_game_mode.red_flasher_flourish()
            self.delay(delay=0.5,handler=self.game.interrupter.dude_escaped,param=amount)

        combined = dmd.GroupedLayer(128,32,activeLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined

    def guy_escapes(self,target):
        # only process this if we haven't already lost
        if self.misses < self.LOSE:
            self.tauntTimer = 0
            self.cancel_delayed("Poller")
            print "BAD GUY " + str(target) + " ESCAPES"
            # set drop the target
            self.game.bad_guys.target_down(target)
            # set the timer for that target to none
            self.badGuyTimer[target] = None
            # move target from active to available
            self.deactivate_guy(target)

            # play some gunshot noise and a light flash of some kind
            # add the miss
            self.misses += 1
            # update the display
            self.update_display(escaped=target)
            # if we're at the max misses, the mode ends

            if self.misses >= self.LOSE:
                print "AMBUSH LOST"
                # cancel any remaining timers for dudes
                for dude in range(0,4,1):
                    self.cancel_delayed(self.targetNames[dude])
                # then close up shop in 1.5 seconds to give the display time to finish up
                self.delay(delay=1.5,handler=self.end_ambush)
            else:
                self.delay(name="Poller",delay=1.5,handler=self.poller)

    def hit(self,target):
        # check to make sure the last guy hasn't already fled - there's a small delay while the last gunshot animation plays
        if self.misses < self.LOSE:
            self.cancel_delayed("Poller")
            # reset the taunt timer
            self.tauntTimer = 0
            # handle a guy hit in a showdown
            print "KILLING GUY: " + str(target)

            ## cancel the timer delay for this dude
            self.cancel_delayed(self.targetNames[target])
            # add the hit to the death tally
            self.deathTally += 1
            # add one to the rolling high noon total
            self.game.increase_tracking('kills')
            # score points
            # after the 4th guy the point value goes up
            if self.deathTally > 4:
                self.showdownValue = 450000
            self.game.score(self.showdownValue)
            # increase the running total by that amount
            self.game.increase_tracking('ambushPoints',self.showdownValue)
            print self.game.show_tracking('ambushPoints')
            # move target from active to available
            self.deactivate_guy(target)
            # play some sound
            # do something with lights
            # throw a display thing or whatever
            self.update_display(killed=target)
            self.delay(name="Poller",delay=1.5,handler=self.poller)

    def lightning(self,section):
        # set which section of the GI to flash
        if section == 'top':
            lamp = self.game.giLamps[0]
        elif section == 'right':
            lamp = self.game.giLamps[1]
        else:
            # the only other option is left
            lamp = self.game.giLamps[2]
            # then flash it

        lamp.pulse(216)


    def end_ambush(self):
        # clear the layer
        self.clear_layer()
        # drop all the targets
        self.game.bad_guys.drop_targets()
        # kill the music
        self.game.sound.stop_music()
        # tally some score?

        # play a quote about bodycount
        bodycount = self.game.show_tracking('ambushTotal')
        # see if the death tally beats previous/existing and store in tracking if does - for ambush champ
        # if the total for this round of ambush was higher than the stored, store it
        if self.deathTally > bodycount:
            self.game.set_tracking('ambushTotal',self.deathTally)
        # set the ambush status to over and setup showdown
        self.game.set_tracking('showdownStatus',"OPEN")
        self.game.set_tracking('ambushStatus',"OVER")
        # turn off lights
        for i in range(0,4,1):
            print "END AMBUSH BAD GUYS " + str(i)
            self.game.set_tracking('badGuysDead',False,i)
            print "BAD GUY STATUS " + str(i) + " IS " + str(self.game.show_tracking('badGuysDead',i))
            # reset the badguy UP tracking just in case
        for i in range (0,4,1):
            self.game.set_tracking('badGuyUp',False,i)
        self.game.bad_guys.update_lamps()
        # start up the main theme again if a second level mode isn't running
        if not self.game.show_tracking('stackLevel',1):
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
            # turn off the level 1 flag
        self.game.set_tracking('stackLevel',False,0)
        # setup a display frame
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'single-cowboy-sideways-border.dmd').frames[0])
        textLine1 = dmd.TextLayer(76, 2, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "AMBUSH: " + str(self.deathTally) + " KILLS"
        textLine1.set_text(textString)
        textLine1.composite_op = "blacksrc"
        textLine2 = dmd.TextLayer(76,11, self.game.assets.font_12px_az, "center", opaque=False)
        print "TOTAL AMBUSH: " + str(self.game.show_tracking('ambushPoints'))
        textLine2.set_text(ep.format_score(self.game.show_tracking('ambushPoints')))
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
        self.layer = combined
        # play a quote
        self.game.sound.play(self.game.assets.quote_mobEnd)
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        # reset the showdown points for next time
        self.game.set_tracking('ambushPoints',0)

        # award the badge light - showdown/ambush is 3
        self.game.badge.update(3)

        # unload the mode
        self.delay(delay=2.1,handler=self.unload)

    def unload(self):
        self.game.modes.remove(self.game.ambush)

    def clear_layer(self):
        self.layer = None

    def mode_stopped(self):
        print "AMBUSH IS DISPATCHING DELAYS"
        self.dispatch_delayed()

    def deactivate_guy(self,target):
        print "DEACTIVATING BAD GUY: " + str(target)
        # remove from active
        if target in self.activatedBadGuys:
            self.activatedBadGuys.remove(target)
        # put it back in available
        if target not in self.availableBadGuys:
            self.availableBadGuys.append(target)

    def activate_guy(self,dude):
        print "ACTIVATING BAD GUY:" + str(dude)
        if dude in self.availableBadGuys:
            self.availableBadGuys.remove(dude)
        # put him in the active targets
        if dude not in self.activatedBadGuys:
            self.activatedBadGuys.append(dude)
