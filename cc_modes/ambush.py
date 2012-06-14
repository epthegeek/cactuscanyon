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
        ## setup the shot guys
        self.shotLayers = []
        shotguy = dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd')
        self.deadGuy0 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.deadGuy0.set_target_position(-49,0)
        self.deadGuy0.composite_op = "blacksrc"
        self.shotLayers.append(self.deadGuy0)
        self.deadGuy1 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.deadGuy1.set_target_position(-16,0)
        self.deadGuy1.composite_op = "blacksrc"
        self.shotLayers.append(self.deadGuy1)
        self.deadGuy2 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.deadGuy2.set_target_position(15,0)
        self.deadGuy2.composite_op = "blacksrc"
        self.shotLayers.append(self.deadGuy2)
        self.deadGuy3 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.deadGuy3.set_target_position(47,0)
        self.deadGuy3.composite_op = "blacksrc"
        self.shotLayers.append(self.deadGuy3)
        self.escapeLayers = []
        shotguy = dmd.Animation().load(ep.DMD_PATH+'dude-shoots.dmd')
        self.eGuy0 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.eGuy0.set_target_position(-49,0)
        self.eGuy0.composite_op = "blacksrc"
        self.escapeLayers.append(self.eGuy0)
        self.eGuy1 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.eGuy1.set_target_position(-16,0)
        self.eGuy1.composite_op = "blacksrc"
        self.escapeLayers.append(self.eGuy1)
        self.eGuy2 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.eGuy2.set_target_position(15,0)
        self.eGuy2.composite_op = "blacksrc"
        self.escapeLayers.append(self.eGuy2)
        self.eGuy3 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        self.eGuy3.set_target_position(47,0)
        self.eGuy3.composite_op = "blacksrc"
        self.escapeLayers.append(self.eGuy3)



    def mode_started(self):
        self.deathTally = 0
        self.showdownValue = 300000
        self.tauntTimer = 0
        self.availableBadGuys = [0,1,2,3]
        self.activatedBadGuys = []
        self.misses = 0
        self.badGuyTimer = [None,None,None,None]
        self.busy = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play in (0,1) and self.game.show_tracking('ambushStatus') == "RUNNING":
            self.end_ambush()


    def start_ambush(self):
        print "A M B U S H"
        # set the layer tracking
        self.game.set_tracking('stackLevel',True,0)
        # set the showdown tracking
        self.game.set_tracking('ambushStatus', "RUNNING")
        # kill the GI
        self.game.gi_control("OFF")
        # things, they go here
        self.deathTally = 0
        # kick out more ball
        # pop up the targets
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
        # add two dudes
        self.busy = True
        self.add_guys(2)
        # start the dude poller
        self.poller()

    def add_guys(self,amount):
        # for adding dudes to the ambush
        # pick a guy from the available targets
        dude = random.choice(self.availableBadGuys)
        self.availableBadGuys.remove(dude)
        # put him in the active targets
        self.activatedBadGuys.append(dude)
        # pop that target up
        self.game.bad_guys.target_up(dude)
        # start a timer for that target
        self.badGuyTimer[dude] = 8
        self.targetTimer(dude)
        # reduce count of dudes to start by 1
        amount -= 1
        # if there are some left, repeat
        if amount != 0:
            self.add_guys(amount)
        else:
            self.busy = False
            self.update_display()

    def targetTimer(self,target):
        # tick one off the timer for that target
        self.badGuyTimer[target] -= 1
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
            # if we need to add some, fire away
            if thisMany != 0:
                # turn on the busy flag to stop the poller while adding
                self.busy = True
                self.add_guys(thisMany)
        # come back to the poller in 1 second
        self.delay(name="Poller",delay=1,handler=self.poller)


    def update_display(self,killed=99,escaped=99):
        # loop through the up bad guys and add them to the display
        activeLayers = []
        for x in self.activatedBadGuys:
            activeLayers.append(self.guyLayers[x])
        # if we're here because someone got killed, add them to the layers to die
        if killed != 99:
            activeLayers.append(self.shotLayers[killed])
            # play a shot sound
            self.game.sound.play(self.game.assets.sfx_gunfightShot)
        if escaped != 99:
            activeLayers.append(self.escapeLayers[escaped])
            self.game.sound.play(self.game.assets.sfx_gunfightShot)

        combined = dmd.GroupedLayer(128,32,activeLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined

    def guy_escapes(self,target):
        self.cancel_delayed("Poller")
        print "BAD GUY " + str(target) + " ESCAPES"
        # set drop the target
        self.game.bad_guys.target_down(target)
        # set the timer for that target to none
        self.badGuyTimer[target] = None
        # remove from active
        self.activatedBadGuys.remove(target)
        # add back to available
        self.availableBadGuys.append(target)
        # play some gunshot noise and a light flash of some kind
        # add the miss
        self.misses += 1
        # if we're at the max misses, the mode ends - TODO make this a config option
        if self.misses == 3:
            self.end_ambush()
        else:
            self.update_display(escaped=target)
        self.delay(name="Poller",delay=1.5,handler=self.poller)

    def hit(self,target):
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

        # remove from active
        self.activatedBadGuys.remove(target)
        # put it back in available
        self.availableBadGuys.append(target)
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
        elif section == 'left':
            lamp = self.game.giLamps[2]
        else:
            pass
            # then flash it
        lamp.pulse(216)


    def end_ambush(self):
        # drop all teh targets
        self.game.bad_guys.drop_targets()
        # kill the music
        self.game.sound.stop_music()
        # tally some score?

        # play a quote about bodycount
        bodycount = self.game.show_tracking('ambushTotal')
        # if the total for this round of showdown was higher stored, store it
        if self.deathTally > bodycount:
            self.game.set_tracking('ambushTotal',self.deathTally)
            # and reset the death tally
        self.deathTally = 0
        # see if the death tally beats previous/existing and store in tracking if does - for showdown champ
        # set the showdown status to over and setup ambush
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
        textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "AMBUSH: " + str(self.deathTally) + " KILLS"
        textLine1.set_text(textString)
        textLine1.composite_op = "blacksrc"
        textLine2 = dmd.TextLayer(128/2,11, self.game.assets.font_12px_az, "center", opaque=False)
        textLine2.set_text(ep.format_score(self.game.show_tracking('ambushPoints')))
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
        self.layer = combined
        # play a quote
        self.game.sound.play(self.game.assets.quote_mobEnd)
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        # reset the showdown points for next time
        self.game.set_tracking('ambushPoints',0)
        # unload the mode
        self.game.modes.remove(self.game.ambush)

    def clear_layer(self):
        self.layer = None