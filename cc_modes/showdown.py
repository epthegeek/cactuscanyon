#   ____           _                ____
#  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
# | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
# | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
#  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
#                                                   |___/
#           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
#          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
#         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
#          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
#
# A P-ROC Project by Eric Priepke, Copyright 2012-2013
# Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
# Original Cactus Canyon software by Matt Coriale
#
#
#  ____  _                      _
# / ___|| |__   _____      ____| | _____      ___ __
# \___ \| '_ \ / _ \ \ /\ / / _` |/ _ \ \ /\ / / '_ \
#  ___) | | | | (_) \ V  V / (_| | (_) \ V  V /| | | |
# |____/|_| |_|\___/ \_/\_/ \__,_|\___/ \_/\_/ |_| |_|
#


from procgame import dmd
import ep


class Showdown(ep.EP_Mode):
    """Showdown code """
    def __init__(self, game, priority):
        super(Showdown, self).__init__(game, priority)
        self.myID = "Showdown"
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]
        # read the difficulty setting from the options
        self.difficulty = self.game.user_settings['Gameplay (Feature)']['Showdown Difficulty']
        self.death_tally = 0
        self.showdownValue = 300000
        self.tauntTimer = 0
        self.ballAdded = False
        self.racking = False
        self.startup = False

    def mode_started(self):
        self.running = True
        self.startup = True
        self.death_tally = 0
        self.showdownValue = 300000
        self.tauntTimer = 0
        self.ballAdded = False
        self.racking = False

    def mode_stopped(self):
        self.running = False
        #print "SHOWDOWN IS DISPATCHING DELAYS"
        self.wipe_delays()
        self.clear_layer()

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0 or self.game.trough.num_balls_in_play == 1 and not self.game.display_hold:
            # if we're not setting up a new rack, its ok to end.  Otherwise ignore
            if self.game.show_tracking('showdownStatus') == "RUNNING" and not self.racking:
                #print "Ending Showdown due to ball drain"
                self.game.base.busy = True
                self.game.base.queued += 1
                self.end_showdown()
        # if we lose balls during the intro - launch another
        if self.game.display_hold:
            self.game.trough.launch_balls(1)

    # add light & sound to flipper if we just came through the inlane
    def sw_flipperLwL_active(self, sw):
        self.game.sound.play(self.game.assets.sfx_explosion11)
        self.game.coils.leftGunFlasher.schedule(0x0000025F, cycle_seconds=1)

    def sw_flipperLwR_active(self, sw):
        self.game.sound.play(self.game.assets.sfx_explosion11)
        self.game.coils.rightGunFlasher.schedule(0x0000025F, cycle_seconds=1)


    def start_showdown(self,side):
        #print "S H O W D O W N"
        # turn on the display hold to catch ball drain during intro
        self.game.display_hold = True
        # audits
        self.game.game_data['Feature']['Showdown Started'] += 1
        # raise the post to hold the ball
        self.activeSide = side

        # set the layer tracking
        self.game.stack_level(1,True)
        # set the showdown tracking
        self.game.set_tracking('showdownStatus', "RUNNING")
        # kill the GI
        self.game.gi_control("OFF")
        # things, they go here
        self.death_tally = 0
        # kick out more ball
        # pop up the targets
        # play a startup animation
        anim = self.game.assets.dmd_showdown
        myWait = len(anim.frames) / 10.0
        anim_layer = ep.EP_AnimatedLayer(anim)
        anim_layer.hold=True
        anim_layer.frame_time = 6
        # keyframe sounds
        anim_layer.add_frame_listener(2, self.game.sound.play, param=self.game.assets.sfx_lightning1)
        anim_layer.add_frame_listener(2, self.game.lightning, param="top")
        anim_layer.add_frame_listener(4, self.game.lightning, param="top")
        anim_layer.add_frame_listener(5, self.game.lightning, param="left")
        anim_layer.add_frame_listener(8, self.game.sound.play, param=self.game.assets.sfx_lightningRumble)
        anim_layer.add_frame_listener(8, self.game.lightning, param="top")
        anim_layer.add_frame_listener(10, self.game.lightning, param="top")
        anim_layer.add_frame_listener(11, self.game.lightning, param="left")
        # setup the display
        self.layer = anim_layer
        # If the multiball ball savers are a thing, do that
        self.game.base.multiball_saver()
        self.delay("Operational", delay=myWait, handler=self.get_going)
        self.taunt_timer()

    def taunt_timer(self):
        # tick up by one
        self.tauntTimer += 1
        # if it's been long enough, play a taunt ant reset
        if self.tauntTimer >= 9:
            # play a taunt quote
            self.game.base.play_quote(self.game.assets.quote_mobTaunt)
            self.tauntTimer = 0
        self.delay("Taunt Timer", delay=1, handler=self.taunt_timer)

    def get_going(self):
        # turn off the startup flag
        self.startup = False
        # check if the ball drained during the intro and put one back if needed
        if self.game.trough.num_balls_in_play == 0:
            self.add_ball()
        myWait = self.game.base.play_quote(self.game.assets.quote_showdown)
        self.delay("Operational", delay=myWait, handler=self.game.base.play_quote, param=self.game.assets.quote_mobStart)
        # turn the GI back on
        self.game.gi_control("ON")
        # start the music
        self.music_on(self.game.assets.music_showdown)
        self.new_rack_pan()

    def add_ball(self):
        self.game.trough.balls_to_autoplunge += 1
        self.game.trough.launch_balls(1)

    def new_rack(self):
        self.racking = True
        # kill the GI again
        self.game.gi_control("OFF")
        # play the interstitial animation
        # load up the lightning
        anim = self.game.assets.dmd_cloudLightning
        # math out the wait
        myWait = len(anim.frames) / 10.0
        # set the animation
        anim_layer = ep.EP_AnimatedLayer(anim)
        anim_layer.hold=True
        anim_layer.frame_time = 6
        # keyframe sounds
        anim_layer.add_frame_listener(2, self.game.sound.play, param=self.game.assets.sfx_lightning1)
        anim_layer.add_frame_listener(2, self.game.lightning, param="top")
        anim_layer.add_frame_listener(3, self.game.lightning, param="left")
        anim_layer.add_frame_listener(3, self.game.lightning, param="right")
        anim_layer.add_frame_listener(6, self.game.sound.play, param=self.game.assets.sfx_lightning2)
        anim_layer.add_frame_listener(6, self.game.lightning, param="top")
        anim_layer.add_frame_listener(7, self.game.lightning, param="left")
        anim_layer.add_frame_listener(10, self.game.sound.play, param=self.game.assets.sfx_lightningRumble)
        anim_layer.add_frame_listener(10, self.game.lightning, param="top")
        anim_layer.add_frame_listener(11, self.game.lightning, param="right")
        # turn it on
        self.layer = anim_layer
        self.delay("Operational", delay=myWait, handler=self.new_rack_pan)

    def new_rack_pan(self):
        # turn the GI back on here
        self.game.gi_control("ON")
        # setup the pan script
        script =[]
        for i in range(0, -52, -1):
            showdown_still = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_townPan.frames[0])
            showdown_still.set_target_position(0,i)
            if i == -51:
                time = 1
            else:
                time = 0.015
            script.append({'seconds':time,'layer':showdown_still})
        showdown_pan = dmd.ScriptedLayer(128,32,script)
        self.layer = showdown_pan
        self.delay("Operational",delay=1.5,handler=self.new_rack_display)

    def new_rack_display(self):
        # if 2 balls are in play add another
        if self.game.trough.num_balls_in_play <= 2:
            if self.difficulty == 'Easy':
                self.add_ball()
                self.game.interrupter.ball_added()
            elif self.difficulty == 'Hard' and not self.ballAdded:
                # for hard setting you get one extra ball - add one and set the flag
                self.add_ball()
                self.ballAdded = True
                self.game.interrupter.ball_added()
            # hit this one if difficulty is hard and there's already been a ball added
            else:
                pass
        # if 3 balls are already in play - and difficulty is easy - you get a ball save
        elif self.game.trough.num_balls_in_play == 3 and self.difficulty == 'Easy':
            self.game.trough.start_ball_save(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=False)
            self.game.interrupter.ball_save_activated()
            # this is where to show "ball added" or "ball saver on"
        self.new_rack_finish()

    def new_rack_finish(self):
    # reset the dudes
        self.showdown_reset_guys()
        self.racking = False
        self.game.display_hold = False

    def showdown_reset_guys(self):
        # pop up all the targets
        self.game.bad_guys.setup_targets()
        # then reset the display
        self.guyLayers = []
        self.badGuy0 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShotFullBody.frames[0])
        self.badGuy0.set_target_position(-49,0)
        self.badGuy0.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy0)
        self.badGuy1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShotFullBody.frames[0])
        self.badGuy1.set_target_position(-16,0)
        self.badGuy1.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy1)
        self.badGuy2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShotFullBody.frames[0])
        self.badGuy2.set_target_position(15,0)
        self.badGuy2.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy2)
        self.badGuy3 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShotFullBody.frames[0])
        self.badGuy3.set_target_position(47,0)
        self.badGuy3.composite_op = "blacksrc"
        self.guyLayers.append(self.badGuy3)
        combined = dmd.GroupedLayer(128,32,self.guyLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined

    def hit(self, target):
        # reset the taunt timer
        self.tauntTimer = 0
        # handle a guy hit in a showdown
        #print "KILLING GUY: " + str(target)
        # count the dead guy
        self.death_tally += 1
        # add one to the rolling high noon total
        self.game.increase_tracking('kills')
        # score points
        # after the 4th guy the point value goes up
        if self.death_tally > 4:
            self.showdownValue = 450000
        self.game.score(self.showdownValue)
        # increase the running total by that amount
        self.game.increase_tracking('showdownPoints', self.showdownValue)

        # swap out the appropriate layer
        shotguy = self.game.assets.dmd_dudeShotFullBody
        if target == 0:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy0)
            self.badGuy0 = dmd.AnimatedLayer(frames=shotguy.frames ,hold=True, opaque=False, repeat=False, frame_time=6)
            self.badGuy0.set_target_position(-49, 0)
            self.badGuy0.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy0)
        elif target == 1:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy1)
            self.badGuy1 = dmd.AnimatedLayer(frames=shotguy.frames, hold=True, opaque=False, repeat=False, frame_time=6)
            self.badGuy1.set_target_position(-16, 0)
            self.badGuy1.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy1)
        elif target == 2:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy2)
            self.badGuy2 = dmd.AnimatedLayer(frames=shotguy.frames, hold=True, opaque=False, repeat=False, frame_time=6)
            self.badGuy2.set_target_position(15, 0)
            self.badGuy2.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy2)
        else:
            # take out the current hit guy
            self.guyLayers.remove(self.badGuy3)
            self.badGuy3 = dmd.AnimatedLayer(frames=shotguy.frames, hold=True, opaque=False, repeat=False, frame_time=6)
            self.badGuy3.set_target_position(47,0)
            self.badGuy3.composite_op = "blacksrc"
            # append on the new layer to the end to put it in the front
            self.guyLayers.append(self.badGuy3)

        myWait = len(shotguy.frames) / 10.0
        # put the new layer  in place
        combined = dmd.GroupedLayer(128, 32, self.guyLayers)
        combined.composite_op = "blacksrc"
        self.layer = combined
        # flash the guns
        self.game.base.guns_flash(1)
        # play a shot sound
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        # if the 4 dudes are dead, reset them
        myWait = len(shotguy.frames) / 10.0
        if self.death_tally % 4 == 0:
            #print "THEY'RE ALL DEAD JIM"
            self.delay("Operational", delay=myWait, handler=self.new_rack)
            # audit
            self.game.game_data['Feature']['Showdown Racks Clear'] += 1
        else:
            self.delay("Operational", delay=myWait, handler=self.game.interrupter.showdown_hit, param=self.showdownValue)

    def end_showdown(self):
        # drop all teh targets
        self.game.bad_guys.drop_targets()
        # turn off the level 1 flag
        self.game.stack_level(1, False)
        # kill the music - if nothing else is running
        # tally some score?
        # award the badge light - showdown/ambush is 3
        self.game.badge.update(3)
        # grab the showdown points before resetting
        totalPoints = self.game.show_tracking('showdownPoints')
        self.update_tracking()

        self.lamp_update()
        # start up the main theme again if a higher level mode isn't running
        if self.game.trough.num_balls_in_play > 0:
            self.music_on(self.game.assets.music_mainTheme,mySlice=2)
        # setup a display frame
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_singleCowboySidewaysBorder.frames[0])
        textLine1 = ep.EP_TextLayer(74, 1, self.game.assets.font_7px_bold_az, "center", opaque=False)
        textString = "SHOWDOWN: " + str(self.death_tally) + " KILLS"
        textLine1.set_text(textString, color=ep.RED)
        textLine1.composite_op = "blacksrc"
        textLine2 = ep.EP_TextLayer(74, 11, self.game.assets.font_12px_az, "center", opaque=False)
        textLine2.set_text(ep.format_score(totalPoints),color=ep.GREEN)
        combined = dmd.GroupedLayer(128, 32, [backdrop,textLine1,textLine2])
        self.layer = combined
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_mobEnd)
        self.delay("Display", delay=2, handler=self.clear_layer)
        # see if the death tally beats previous/existing and store in tracking if does - for showdown champ
        # unset the base busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # unload the mode
        self.delay(delay=2.1, handler=self.unload)

    def tilted(self):
        if self.running:
            self.game.badge.update(3)
            self.update_tracking()
            self.unload()
        self.running = False

    def update_tracking(self):
        bodycount = self.game.show_tracking('showdownTotal')
        # if the total for this round of showdown was higher stored, store it
        if self.death_tally > bodycount:
            self.game.set_tracking('showdownTotal', self.death_tally)
            # see if the death tally beats previous/existing and store in tracking if does - for showdown champ
        # set the showdown status to over and setup ambush
        self.game.set_tracking('showdownStatus', "OVER")
        self.game.set_tracking('ambushStatus', "OPEN")
        # turn off lights
        for i in range(0,4,1):
            #print "END SHOWDOWN BAD GUYS " + str(i)
            self.game.set_tracking('badGuysDead', False, i)
            #print "BAD GUY STATUS " + str(i) + " IS " + str(self.game.show_tracking('badGuysDead',i))
            # reset the badguy UP tracking just in case
        for i in range (0, 4, 1):
            self.game.set_tracking('badGuyUp', False, i)
        # reset the showdown points for next time
        self.game.set_tracking('showdownPoints', 0)
