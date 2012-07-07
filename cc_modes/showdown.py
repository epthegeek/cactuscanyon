###
###  ____  _                      _
### / ___|| |__   _____      ____| | _____      ___ __
### \___ \| '_ \ / _ \ \ /\ / / _` |/ _ \ \ /\ / / '_ \
###  ___) | | | | (_) \ V  V / (_| | (_) \ V  V /| | | |
### |____/|_| |_|\___/ \_/\_/ \__,_|\___/ \_/\_/ |_| |_|
###


from procgame import *
import cc_modes
import ep
import random

class Showdown(game.Mode):
    """Showdown code """
    def __init__(self,game,priority):
        super(Showdown, self).__init__(game,priority)
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]

    def mode_started(self):
        self.deathTally = 0
        self.showdownValue = 300000
        self.tauntTimer = 0

    def ball_drained(self):
        if self.game.trough.num_balls_in_play in (0,1) and self.game.show_tracking('showdownStatus') == "RUNNING":
            self.game.base_game_mode.busy = True
            self.end_showdown()

    def start_showdown(self,side):
        print "S H O W D O W N"
        # raise the post to hold the ball
        self.activeSide = side
        self.posts[self.activeSide].patter(on_time=4,off_time=12,original_on_time=30)

        # set the layer tracking
        self.game.set_tracking('stackLevel',True,0)
        # set the showdown tracking
        self.game.set_tracking('showdownStatus', "RUNNING")
        # kill the GI
        self.game.gi_control("OFF")
        # things, they go here
        self.deathTally = 0
        # kick out more ball
        # pop up the targets
        # play a startup animation
        anim = dmd.Animation().load(ep.DMD_PATH+'showdown.dmd')
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
        myWait = self.game.sound.play(self.game.assets.quote_showdown)
        self.delay(delay=myWait,handler=self.game.play_remote_sound,param=self.game.assets.quote_mobStart)
        # turn the GI back on
        self.game.gi_control("ON")
        # start the music
        self.game.base_game_mode.music_on(self.game.assets.music_showdown)
        #self.showdown_reset_guys()
        self.new_rack_pan()
        # drop the post
        self.delay(delay=1.5,handler=self.posts[self.activeSide].disable)


    def add_ball(self):
        self.game.autoPlunge = True
        self.game.trough.launch_balls(1)

    def new_rack(self):
        # kill the GI again
        self.game.gi_control("OFF")
        # play the interstitial animation
        # load up the lightning
        anim = dmd.Animation().load(ep.DMD_PATH+'cloud-lightning.dmd')
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        # keyframe sounds
        animLayer.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.sfx_lightning1)
        animLayer.add_frame_listener(2,self.game.lightning,param="top")
        animLayer.add_frame_listener(3,self.game.lightning,param="left")
        animLayer.add_frame_listener(6,self.game.play_remote_sound,param=self.game.assets.sfx_lightning2)
        animLayer.add_frame_listener(6,self.game.lightning,param="top")
        animLayer.add_frame_listener(7,self.game.lightning,param="left")
        animLayer.add_frame_listener(10,self.game.play_remote_sound,param=self.game.assets.sfx_lightningRumble)
        animLayer.add_frame_listener(10,self.game.lightning,param="top")
        animLayer.add_frame_listener(11,self.game.lightning,param="right")
        # turn it on
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.new_rack_pan)


    def new_rack_pan(self):
        # turn the GI back on here
        self.game.gi_control("ON")
        # setup the pan script
        script =[]
        for i in range(0,-52,-1):
            showdownStill = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'town-pan.dmd').frames[0])
            showdownStill.set_target_position(0,i)
            if i == -51:
                time = 1
            else:
                time = 0.015
            script.append({'seconds':time,'layer':showdownStill})
        showdownPan = dmd.ScriptedLayer(128,32,script)
        self.layer = showdownPan
        self.delay(delay=1.5,handler=self.new_rack_display)

    def new_rack_display(self):
        # if 2 balls are in play add another
        if self.game.trough.num_balls_in_play <= 2:
            self.add_ball()
            self.game.interrupter.ball_added()
        # if 3 balls are already in play
        elif self.game.trough.num_balls_in_play == 3:
            self.game.ball_save.start(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=False)
            self.game.interrupter.ball_save_activated()
            # this is where to show "ball added" or "ball saver on"
        self.new_rack_finish()

    def new_rack_finish(self):
    # reset the dudes
        self.showdown_reset_guys()

    def showdown_reset_guys(self):
        # pop up all the targets
        self.game.bad_guys.setup_targets()
        # then reset the display
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
        combined = dmd.GroupedLayer(128,32,self.guyLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined

    def hit(self,target):
        # reset the taunt timer
        self.tauntTimer = 0
        # handle a guy hit in a showdown
        print "KILLING GUY: " + str(target)
        # count the dead guy
        self.deathTally += 1
        # add one to the rolling high noon total
        self.game.increase_tracking('kills')
        # score points
        # after the 4th guy the point value goes up
        if self.deathTally > 4:
            self.showdownValue = 450000
        self.game.score(self.showdownValue)
        # increase the running total by that amount
        self.game.increase_tracking('showdownPoints',self.showdownValue)

        # swap out the appropriate layer
        shotguy = dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-full-body.dmd')
        if target == 0:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy0)
            self.badGuy0 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            self.badGuy0.set_target_position(-49,0)
            self.badGuy0.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy0)
        elif target == 1:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy1)
            self.badGuy1 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            self.badGuy1.set_target_position(-16,0)
            self.badGuy1.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy1)
        elif target == 2:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy2)
            self.badGuy2 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            self.badGuy2.set_target_position(15,0)
            self.badGuy2.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy2)
        else:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy3)
            self.badGuy3 = dmd.AnimatedLayer(frames=shotguy.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            self.badGuy3.set_target_position(47,0)
            self.badGuy3.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy3)

        myWait = len(shotguy.frames) / 10.0
        # put the new layer  in place
        combined = dmd.GroupedLayer(128,32,self.guyLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined
        # play a shot sound
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        # if the 4 dudes are dead, reset them
        myWait = len(shotguy.frames) / 10.0
        if self.deathTally % 4 == 0:
            print "THEY'RE ALL DEAD JIM"
            self.delay(delay=myWait,handler=self.new_rack)
        else:
            self.delay(delay=myWait,handler=self.game.interrupter.showdown_hit,param=self.showdownValue)

    def end_showdown(self):
        # drop all teh targets
        self.game.bad_guys.drop_targets()
        # kill the music
        self.game.sound.stop_music()
        # tally some score?
        # award the badge light - showdown/ambush is 3
        self.game.badge.update(3)

        # play a quote about bodycount
        bodycount = self.game.show_tracking('showdownTotal')
        # if the total for this round of showdown was higher stored, store it
        if self.deathTally > bodycount:
            self.game.set_tracking('showdownTotal',self.deathTally)
        # see if the death tally beats previous/existing and store in tracking if does - for showdown champ
        # set the showdown status to over and setup ambush
        self.game.set_tracking('showdownStatus',"OVER")
        self.game.set_tracking('ambushStatus',"OPEN")
        # turn off lights
        for i in range(0,4,1):
            print "END SHOWDOWN BAD GUYS " + str(i)
            self.game.set_tracking('badGuysDead',False,i)
            print "BAD GUY STATUS " + str(i) + " IS " + str(self.game.show_tracking('badGuysDead',i))
            # reset the badguy UP tracking just in case
        for i in range (0,4,1):
            self.game.set_tracking('badGuyUp',False,i)
        self.game.bad_guys.update_lamps()
        # start up the main themse again if a second level mode isn't running
        if not self.game.show_tracking('stackLevel',1):
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
            # turn off the level 1 flag
        self.game.set_tracking('stackLevel',False,0)
        # setup a display frame
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'single-cowboy-sideways-border.dmd').frames[0])
        textLine1 = dmd.TextLayer(128/2, 1, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "SHOWDOWN: " + str(self.deathTally) + " KILLS"
        textLine1.set_text(textString)
        textLine1.composite_op = "blacksrc"
        textLine2 = dmd.TextLayer(128/2,11, self.game.assets.font_12px_az, "center", opaque=False)
        textLine2.set_text(ep.format_score(self.game.show_tracking('showdownPoints')))
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
        self.layer = combined
        # play a quote
        self.game.sound.play(self.game.assets.quote_mobEnd)
        self.delay(name="Display",delay=2,handler=self.clear_layer)
        # reset the showdown points for next time
        self.game.set_tracking('showdownPoints',0)
        # see if the death tally beats previous/existing and store in tracking if does - for showdown champ
        # unset the base busy flag
        self.game.base_game_mode.busy = False

        # unload the mode
        self.delay(delay=2.1,handler=self.unload)

    def unload(self):
        self.game.modes.remove(self.game.showdown)

    def clear_layer(self):
        self.layer = None

    def mode_stopped(self):
        print "SHOWDOWN IS DISPATCHING DELAYS"
        self.dispatch_delayed()