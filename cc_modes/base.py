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
## This Class is the mode that runs at all times during active play as a catch all
## Any general events that don't apply to any particular mode will end up handled here
## Like awarding points for hitting the slingshots - or the outlanes - or the start
## button is pressed - etc,
##
## Where to put combos? quickdraws? More modes? or stick them here?
## HMMMM


from procgame import dmd
import ep
import random
import time
import sys


class BaseGameMode(ep.EP_Mode):
    """docstring for AttractMode"""
    def __init__(self, game,priority):
        super(BaseGameMode, self).__init__(game, priority)
        self.myID = "Base"
        self.ball_starting = True
        self.current_music = self.game.assets.music_mainTheme
        self.unbusy()
        self.active_quotes = []
        # for aborting thebonus display
        self.doingBonus = False
        # skippable drunk multiball?
        #skip_dmb = self.game.user_settings['Gameplay (Feature)']['Can skip Drunk Multiball Intro']
        #if skip_dmb == 'Yes':
        #    self.skipDrunk = True
        #else:
        #    self.skipDrunk = False
        self.skipDrunk = 'Yes' == self.game.user_settings['Gameplay (Feature)']['Drunk Multiball Intro Skip']
        self.drunkStacking = 'Enabled' == self.game.user_settings['Gameplay (Feature)']['Drunk Multiball Stacking']
        # Multiball ball saver flag
        self.multiballSaver = 'Yes' == self.game.user_settings['Gameplay (Feature)']['Multiball Ball Savers']
        self.multiballSaverTimer = self.game.user_settings['Gameplay (Feature)']['Multiball Savers Timer']
        self.autoplungeStrength = self.game.user_settings['Machine (Standard)']['Autoplunger Strength']
        self.keys_index = {'beer_mug':list(range(len(self.game.sound.sounds[self.game.assets.quote_beerMug])))}
        self.counts_index = {'beer_mug':0}
        random.shuffle(self.keys_index['beer_mug'])

    def mode_started(self):
        ## cancel the closing song delay, just in case
        self.game.interrupter.cancel_delayed("Attract Fade")
        # and update the lamps
        self.lamp_update()
        # set the jet killed flag
        self.jetKilled = False
        self.jetCount = 0
        self.beerHit = False

    def mode_stopped(self):
        # Ensure flippers are disabled
        self.game.enable_flippers(enable=False)
        # Deactivate the ball search logic so it won't search due to no
        # switches being hit.
        self.game.ball_search.disable()
        # shut down all the modes
        self.remove_modes()

    def load_modes(self):
        self.game.modes.add(self.game.bonus_lanes)
        self.game.modes.add(self.game.combos)
        self.game.modes.add(self.game.right_ramp)
        self.game.modes.add(self.game.left_ramp)
        self.game.modes.add(self.game.center_ramp)
        self.game.modes.add(self.game.left_loop)
        self.game.modes.add(self.game.right_loop)
        self.game.modes.add(self.game.mine)
        self.game.modes.add(self.game.saloon)
        self.game.modes.add(self.game.bart)
        self.game.modes.add(self.game.bad_guys)

    def remove_modes(self):
        self.game.bonus_lanes.unload()
        self.game.combos.unload()
        self.game.right_ramp.unload()
        self.game.left_ramp.unload()
        self.game.center_ramp.unload()
        self.game.left_loop.unload()
        self.game.right_loop.unload()
        self.game.mine.unload()
        self.game.bart.unload()
        self.game.saloon.unload()
        self.game.bad_guys.unload()

    def ball_drained(self):
        print "CHECKING TRACKING ball drained LR: " + str(self.game.show_tracking('leftRampStage'))
        # if that was the last ball in play need to finish up - unless high noon is finishing up
        if self.game.trough.num_balls_in_play == 0:
            # check if we're in high noon - or boss bart fight
            status = self.game.show_tracking('highNoonStatus')
            if status == "RUNNING" or status == "FINISH" or self.game.bart.bossWin:
                print "HIGH NOON IS RUNNING - HOLD IT (or boss bart)"
                # do nothing, and bail
                return
            # if showdown is running and display hold is on - don't mess with things
            if self.game.showdown.running and self.game.display_hold:
                return
            # turn off all the lights
            for lamp in self.game.lamps.items_tagged('Playfield'):
                lamp.disable()
            # Kill the mine flasher if it's on
            self.game.coils.mineFlasher.disable()
            # stop the music
            self.stop_music()
            # turn off ball save
            self.game.ball_search.disable()
            # turn off the flippers
            self.game.enable_flippers(False)
            if self.game.show_tracking('tiltStatus') < self.game.tilt_warnings:
                # play the ball end riff
                self.game.sound.play(self.game.assets.sfx_ballEnd)
                # go check the bonus - after that we'll finish the ball
                # delay 1 second to give other modes time too set the busy if needed
                self.delay(delay=1,handler=self.check_bonus)
            # this is the last ball drain on a tilt
            else:
                self.wipe_delays()
                self.layer = None
                self.game.interrupter.clear_layer()
                # if we tilted out of a moonlight - we go to start ball, not ball ended
                if self.game.moonlight.tilted:
                    self.game.moonlight.tilted = False
                    self.delay(delay=2,handler=self.game.ball_starting)
                else:
                    self.delay(delay=2,handler=lambda: self.wait_for_queue(self.game.ball_ended))

    def sw_startButton_active(self, sw):
        # if start button is pressed during the game
        # if we're on the first ball and there are less than four players, add one.
        if self.game.ball == 1 and len(self.game.players) < 4:
            self.game.add_player()
            # set a random bart bro
            # barts: bandelero, bubba, big, rudy & boss
            if self.game.bart.guests:
                barts = [0,1,2,3]
            else:
                barts = [0,1,2]
            self.game.set_tracking('currentBart',random.choice(barts))

            # tick up the audits
            self.game.game_data['Audits']['Games Started'] += 1
            self.game.order_mobs()
            # and play a soundbyte
            if len(self.game.players) == 2:
                self.game.base.priority_quote(self.game.assets.quote_playerTwo)
            elif len(self.game.players) == 3:
                self.game.base.priority_quote(self.game.assets.quote_playerThree)
            elif len(self.game.players) == 4:
                self.game.base.priority_quote(self.game.assets.quote_playerFour)
            self.game.interrupter.add_player()
        elif self.game.match in self.game.modes and self.game.immediateRestart:
            self.game.sound.stop(self.game.assets.sfx_ragtimePiano)
            self.game.match.unload()
            self.game.game_reset()
        else:
            pass

        ## -- set the last switch hit --
        ep.last_switch = "startButton"

    # to allow restarting the game
    def sw_startButton_active_for_1s(self,sw):
        # if there's a ball in the shooter lane and we're on a ball after ball 1
        if self.game.switches.shooterLane.is_active() and self.game.ball > 1:
            self.game.game_reset()

    def sw_shooterLane_open_for_3s(self,sw):
        # don't start the ball saver if super skillshot is running
        if self.game.ballStarting:
            self.game.ballStarting = False
            if not self.game.skill_shot.super:
                self.game.trough.start_ball_save(num_balls_to_save=1, time=0, now=True, allow_multiple_saves=False)

    def beer_unhit(self):
        self.beerHit = False

    def sw_beerMug_active(self,sw):
        # track it, because why not
        if self.beerHit:
            pass
        else:
            if self.game.user_settings['Gameplay (Feature)']['Party Mode'] == 'Spiked':
                # set the tilt all the way up and then run it
                self.game.set_tracking('tiltStatus',self.game.tilt_warnings)
                self.tilt()
            else:
                print "Beer Mug Hit"
                self.beerHit = True
                # delay to re-allow due to debounce being off
                self.delay(delay=0.050,handler=self.beer_unhit)
                hits = self.game.increase_tracking('beerMugHits')
                self.game.increase_tracking('beerMugHitsTotal')
                # flash the light if present
                if not self.game.lamp_control.lights_out:
                    self.game.lamps.beerMug.schedule(0x00000CCC,cycle_seconds=1)
                # score points
                self.game.score(2130)
                # play a sound
                self.game.sound.play(self.game.assets.sfx_ricochetSet)
                # a little display action
                textLine1 = ep.EP_TextLayer(51, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("BEER MUG",color=ep.ORANGE)
                left = self.game.show_tracking('mug_shots') - hits
                ## if we're at zero, it's lit and the display shows it
                if left == 0:
                    self.light_drunk_multiball()
                ## if we're past zero then it shows a message
                elif left < 0:
                    textString = "SHOOT THE SALOON"
                    if self.game.drunk_multiball.enabled:
                        textString2 = "FOR MULTIBALL"
                    else:
                        textString2 = "FOR DRUNK BONUS"
                    textLine2 = ep.EP_TextLayer(51, 12, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString,blink_frames=8)
                    textLine3 = ep.EP_TextLayer(51, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2,color=ep.YELLOW)
                    self.mug_display(textLine1,textLine2,textLine3)

                ## if we're still not there yet, show how much is left
                else:
                    if left == 1:
                        textString = "1 MORE HIT FOR"
                    else:
                        textString = str(left) + " MORE HITS FOR"
                    if self.game.drunk_multiball.enabled:
                        textString2 = "DRUNK MULTIBALL"
                    else:
                        textString2 = "DRUNK BONUS"
                    textLine2 = ep.EP_TextLayer(51, 12, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString)
                    textLine3 = ep.EP_TextLayer(51, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2,color=ep.YELLOW)
                    self.mug_display(textLine1,textLine2,textLine3)

                if left != 0:
                    # play a quote on a random 1/3 choice
                    weDo = random.choice([False,True,False])
                    # if super skill shot is running, don't use a quote here
                    if self.game.skill_shot.super:
                        weDo = False
                    if weDo:
                        self.play_ordered_quote(self.game.assets.quote_beerMug,'beer_mug')
                ## -- set the last switch -- ##
                ep.last_switch = 'beerMug'
                ## kill the combo shot chain
                ep.last_shot = None


    def mug_display(self,textLine1,textLine2,textLine3):
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_beerMug.frames[0])
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        # kill any previous display
        self.cancel_delayed("Display")
        # turn on the layer
        self.layer = combined
        # set a delay to clear
        self.delay(name="Display", delay = 1.6, handler=self.clear_layer)

    def light_drunk_multiball(self,callback = None):
        # set the hits to the same number it takes to light - this is a catch for the super skillshot award
        self.game.set_tracking('beerMugHits',self.game.show_tracking('mug_shots'))
        # enable the multiball
        self.game.set_tracking('drunkMultiballStatus', "READY")
        self.lamp_update()
        textLine1 = ep.pulse_text(self,51,1,"DRUNK",color=ep.ORANGE)
        if self.game.drunk_multiball.enabled:
            string = "MULTIBALL"
        else:
            string = "BONUS"
        textLine2 = ep.pulse_text(self,51,12,string,color=ep.ORANGE)
        textLine3 = ep.EP_TextLayer(51, 23, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("IS LIT",color=ep.GREEN)
        self.repeat_ding(4)
        duration = self.game.base.play_quote(self.game.assets.quote_drunkMultiballLit)
        self.delay(delay=duration,handler=self.game.base.play_quote,param=self.game.assets.quote_shootSaloon)
        self.mug_display(textLine1,textLine2,textLine3)
        # so super can start gameplay
        if callback:
            self.delay(delay=1.7,handler=callback)
        self.delay(delay=1.7,handler=self.clear_layer)

###
###     _             _ _         ____  _ _
###    / \  _   _  __| (_) ___   | __ )(_) |_ ___
###   / _ \| | | |/ _` | |/ _ \  |  _ \| | __/ __|
###  / ___ \ |_| | (_| | | (_) | | |_) | | |_\__ \
### /_/   \_\__,_|\__,_|_|\___/  |____/|_|\__|___/
###

    # modified version of play voice from procgame.sound that stores a list of active quotes
    # even though more than one shouldn't be possible given the time checking
    def play_quote(self,key, loops=0, max_time=0, fade_ms=0,override=False,squelch=False,nr=999):
        if not self.game.sound.enabled:
            return 0
        current_time = time.time()
        # Make sure previous voice call is finished. unless override
        if not override:
            if current_time < self.game.sound.voice_end_time: return 0
        # if the key exists, stuff happens
        if key in self.game.sound.sounds:
            if squelch:
                # if we're squelching, turn down the music volume - but first, cancel any previous restore delay
                self.cancel_delayed("Squelch")
                self.game.squelch_music()
            # store the key in a list
            self.active_quotes.append(key)
            # allow the code to pick specific items out of batches of quotes if specified
            if nr != 999:
                n = nr
                print "Quote Specific Number is: " + str(n)
            elif len(self.game.sound.sounds[key]) > 0:
                l = list(range(len(self.game.sound.sounds[key])))
                n = random.choice(l)
                print "Randomized Quote Number is: " + str(n)
            else:
                print "Quote Number Defaulted to zero"
                n = 0
            # then play the quote based on the new selection
            self.game.sound.sounds[key][n].play(loops,max_time,fade_ms)
            duration = self.game.sound.sounds[key][n].get_length() * (loops+1)
            self.game.sound.voice_end_time = current_time + duration
            # delay a removal of the active quote from the list
            self.delay(delay=duration,handler=self.end_quote,param=key)
            if squelch:
                # if we're squelching, set a delay to restore the music
                self.delay("Squelch",delay=duration+0.2,handler=self.game.restore_music)
            return duration
        # if not, return zilch
        else:
            return 0

    def end_quote(self,key):
        self.active_quotes.remove(key)

    def priority_quote(self,quote,loops=0, max_time=0, fade_ms=0,squelch=False,nr=999):
        # cancel any other voice quote
        for key in self.active_quotes:
            print "STOPPING " + str(key)
            self.game.sound.stop(key)
        # then play the quote - overriding the voice delay timer
        duration = self.play_quote(quote,loops,max_time,fade_ms,override=True,squelch=squelch,nr=nr)
        return duration

    def repeat_ding(self,times):
        self.game.sound.play(self.game.assets.sfx_bountyBell)
        self.game.coils.saloonFlasher.pulse(ep.FLASHER_PULSE)
        times -= 1
        if times > 0:
            self.delay(delay=0.4,handler=self.repeat_ding,param=times)


    ###
    ###  _____ _ _ _
    ### |_   _(_) | |_
    ###   | | | | | __|
    ###   | | | | | |_
    ###   |_| |_|_|\__|
    ###

    def sw_plumbBobTilt_active(self, sw):
        # first, register the hit
        status = self.game.increase_tracking('tiltStatus')
        print "TILT STATUS: " + str(status)
        # if that puts us at three, time to tilt
        if status == self.game.tilt_warnings:
            self.tilt()
        # if it keeps banging, ignore it
        elif status > self.game.tilt_warnings:
            pass
        # for 2 or 1 hand off to interrupter jones
        else:
            self.game.interrupter.tilt_danger(status)

    def tilt(self):
        # Process tilt.
        # disable the ball save
        self.game.trough.disable_ball_save()
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.game.show_tracking('tiltStatus') >= self.game.tilt_warnings:
            # disable status
            self.game.statusOK = False

            self.game.game_data['Audits']['Tilts'] += 1

            self.game.interrupter.tilt_display()

            # Disable flippers so the ball will drain.
            self.game.enable_flippers(enable=False)

            # drop the targets
            self.game.bad_guys.drop_targets()

            # Make sure ball won't be saved when it drains.
            self.game.trough.disable_ball_save()

            # kill the gunfight pins
            self.game.coils.rightGunFightPost.disable()
            self.game.coils.leftGunFightPost.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            #play sound
            self.stop_music()
            self.game.sound.play(self.game.assets.sfx_spinDown)

            #clear the mine and the saloon in 4 seconds
            self.delay(name="Tilted Ejects",delay=4,handler=self.tilted_ejects)

            # tilt out all the modes
            modequeue_copy = list(self.game.modes)
            for mode in modequeue_copy:
                print "Tilt Roll Call: " + mode.myID
                if getattr(mode, "tilted", None):
                    mode.tilted()

    def tilted_ejects(self):
        if self.game.switches.saloonPopper.is_active():
            self.game.saloon.kick()
        if self.game.switches.minePopper.is_active():
            self.game.mountain.eject()
        # swing back in two seconds to re-check
        self.delay(name="Tilted Ejects",delay=2,handler=self.tilted_ejects)

    def tilted(self):
        pass

    ###
    ###  ___       _
    ### |_ _|_ __ | | __ _ _ __   ___  ___
    ###  | || '_ \| |/ _` | '_ \ / _ \/ __|
    ###  | || | | | | (_| | | | |  __/\__ \
    ### |___|_| |_|_|\__,_|_| |_|\___||___/
    ###
    ###

    def sw_leftReturnLane_active(self, sw):
        # register a left return lane hit
        self.return_lane_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftReturnLane"


    def sw_rightReturnLane_active(self,sw):
        # register a right return lane hit
        self.return_lane_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightReturnLane"

    def return_lane_hit(self,side):
        # play the sound
        self.game.sound.play(self.game.assets.sfx_rattlesnake)
        # score the points
        self.game.score(2530,bonus=True)
        # if the skillshot is still live at this point, end that
        if self.game.skill_shot.live:
            self.game.skill_shot.skillshot_set()
        # if tribute is starting, stop the ball
        elif self.game.tribute_launcher in self.game.modes:
            # if we hit a return lane when the launcher is running, pop the post
            print "Tribute raising post on left"
            self.game.coils.leftGunFightPost.patter(on_time=2,off_time=6,original_on_time=60)
        # if there's a running quickdraw or showdown - pass
        elif not self.guns_allowed():
            pass
            #print "PASSING - Guns disabled"
            #print self.game.show_tracking('stackLevel')
        # Everything beyond this point only registers if there's no other mode running - so no stack checking is needed
        # move your train
        elif self.game.show_tracking('mytStatus') == "READY":
            # if MYT is ready, start it and raise the post to catch the ball
            self.game.move_your_train.start(True,side)
        # cva
        elif self.game.show_tracking('cvaStatus') == "READY":
            self.game.modes.add(self.game.cva)
            self.game.cva.intro(entry="inlane",onSide = side)
        # if guns are allowed, and showdown is ready do that
       # CHANGING SHOWDOWN TO START IMMEDIATELY AFTER 4TH QD
       # elif self.game.show_tracking('showdownStatus') == "READY":
       #     self.game.modes.add(self.game.showdown)
       #     self.game.showdown.start_showdown(side)
        # if guns are allowed and ambush is ready, do that
        elif self.game.show_tracking('ambushStatus') == "READY":
            self.game.modes.add(self.game.ambush)
            self.game.ambush.start_ambush(side)
        # if there's no showdown ready, gunfight is possible
        elif self.game.show_tracking('gunfightStatus') == "READY":
            self.game.modes.add(self.game.gunfight)
            self.game.gunfight.start_gunfight(side)
        # else if quickdraw is lit - run that passing which side started it
        elif self.game.show_tracking('quickdrawStatus',side) == "READY":
            # fire the startup
            self.game.modes.add(self.game.quickdraw)
            self.game.quickdraw.start_quickdraw(side)
        else:
            # check stampede
            self.check_stampede()

    def guns_allowed(self):
        # this is for turning the guns back on if the conditions are good
        if True in self.game.show_tracking('stackLevel') or self.game.skill_shot.super or self.game.bart.bossFight:
        # if any stack level is active, new gunfight action is not allowed
            #print "Guns not allowed right now"
            return False
        else:
            #print "Guns allowed right now"
            return True


    ###
    ###   ___        _   _
    ###  / _ \ _   _| |_| | __ _ _ __   ___  ___
    ### | | | | | | | __| |/ _` | '_ \ / _ \/ __|
    ### | |_| | |_| | |_| | (_| | | | |  __/\__ \
    ###  \___/ \__,_|\__|_|\__,_|_| |_|\___||___/
    ###

    def sw_leftOutlane_active(self,sw):
        self.outlane_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftOutlane"


    def sw_rightOutlane_active(self,sw):
        self.outlane_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightOutlane"


    def outlane_hit(self, side):
        self.game.score(2530,bonus=True)
        if self.game.show_tracking('bozoBall'):
            # if bozo ball flag is on, award that
            self.collect_bozo_ball()
        else:
            # otherwise just play the noise
            self.game.sound.play(self.game.assets.sfx_outlane)

    ###
    ###  ____  _ _                 _           _
    ### / ___|| (_)_ __   __ _ ___| |__   ___ | |_ ___
    ### \___ \| | | '_ \ / _` / __| '_ \ / _ \| __/ __|
    ###  ___) | | | | | | (_| \__ \ | | | (_) | |_\__ \
    ### |____/|_|_|_| |_|\__, |___/_| |_|\___/ \__|___/
    ###                  |___/
    ###

    def sw_leftSlingshot_active(self,sw):
        self.slingshot_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftSlingshot"


    def sw_rightSlingshot_active(self,sw):
        self.slingshot_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightSlingshot"


    def slingshot_hit(self,side):
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # blink a flasher
        if side == 0:
            self.delay(delay=0.03,handler=self.game.coils.leftGunFlasher.pulse)
        else:
            self.delay(delay=0.03,handler=self.game.coils.rightGunFlasher.pulse)
        # score points
        self.game.score(3770)

    ###  ____
    ### | __ ) _   _ _ __ ___  _ __   ___ _ __ ___
    ### |  _ \| | | | '_ ` _ \| '_ \ / _ \ '__/ __|
    ### | |_) | |_| | | | | | | |_) |  __/ |  \__ \
    ### |____/ \__,_|_| |_| |_| .__/ \___|_|  |___/
    ###                       |_|

    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
        # count the hit
        self.jetCount += 1
        # if we're over six and not not killed, kill the jet
        if self.jetCount > 3 and not self.jetKilled:
            print "Max bumps, shut er down!"
            self.jetKilled = True
            self.game.enable_bottom_bumper(False)
        # otherwise, register the hit
        else:
            self.bumper_hit('bottom')

    def bumper_hit(self,bumper):
        # if combos are on, award grace
        if self.game.combos.myTimer > 0:
            self.game.combos.myTimer = self.game.combos.default
        hits = self.game.increase_tracking('bumperHits')
        # flash the back left flasher per hit
        self.game.coils.backLeftFlasher.pulse(30)
        if hits == 125:
            self.game.interrupter.bumpers_increased(25000)
        elif hits == 250:
            self.game.interrupter.bumpers_increased(50000)
        if self.game.show_tracking('cvaStatus') == "RUNNING":
            self.game.score(5250)
            self.game.base.play_quote(self.game.assets.sfx_cvaBumper)

        if hits < 125:
            # if we're under 75 points are low
            self.game.score(5250)
            # and the sound is a punch
            self.game.sound.play(self.game.assets.sfx_punch)
            self.display_bumper(hits,"SUPER")
        elif hits >= 125 and hits < 250:
            # if we're in super jets the score is more
            self.game.score(25000)
            # and the sound is an explosion
            self.game.sound.play(self.game.assets.sfx_smallExplosion)
            self.display_bumper(hits,"MEGA")
        elif hits >= 250:
            # mega jets
            self.game.score(50000)
            # and the sound is the futuristic ricochet
            self.game.sound.play(self.game.assets.sfx_futuristicRicochet)

    ## TODO add the displays for shots to increase level and the various active levels
    def display_bumper(self,hits,nextup):
        if nextup == "SUPER":
            textString1 = "< " + str(125 - hits) + " MORE HITS >"
            textString2 = "< FOR SUPER JETS >"
        else:
            textString1 = "<" + str(250 - hits) + " MORE HITS >"
            textString2 = "< FOR  MEGA  JETS >"
        textLayer1 = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString1,color=ep.BROWN)
        textLayer2 = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString2,color=ep.BROWN)
        textLayer1.composite_op = "blacksrc"
        textLayer2.compoaite_op = "blacksrc"
        self.cancel_delayed("Display")
        self.layer = textLayer1
        self.delay(name="Display",delay=.5,handler=self.change_layer,param=textLayer2)
        self.delay(name="Display",delay=1,handler=self.clear_layer)

    def change_layer(self,myLayer):
        self.layer = myLayer

    ###
    ###  _____ _ _
    ### |  ___| (_)_ __  _ __   ___ _ __ ___
    ### | |_  | | | '_ \| '_ \ / _ \ '__/ __|
    ### |  _| | | | |_) | |_) |  __/ |  \__ \
    ### |_|   |_|_| .__/| .__/ \___|_|  |___/
    ###           |_|   |_|
    ###

    ## Flipper switch detection for flipping the bonus lanes
    def sw_flipperLwL_active(self,sw):
        # if both flippers are hit, kill the bonus
        if self.game.switches.flipperLwR.is_active():
            #print "Both flippers pressed"
            self.dub_flip()
        # if no balls in play, don't do anything else.
        if self.game.trough.num_balls_in_play == 0:
            return
        # toggle the bonus lane
        self.game.bonus_lanes.flip()

    def sw_flipperLwR_active(self,sw):
        # if both flippers are hit kill the bonus
        if self.game.switches.flipperLwL.is_active():
            # if the bonus is active, kill that
            self.dub_flip()
        # if no balls in play, don't do anything else.
        if self.game.trough.num_balls_in_play == 0:
            return
        # toggle the bonus lane
        self.game.bonus_lanes.flip()

    def dub_flip(self):
        # if doing the bonus, abort
        if self.doingBonus:
            self.abort_bonus()
        # if the long form extra ball thing is running, kill that
        elif self.game.mine.collectingEB:
            self.game.mine.abort_extra_ball()
        # if the mine lock animation is running, kill that
        elif self.game.mine.lockAnimation:
            self.game.mine.abort_lock_animation()
        # if doing the DMB animation and disable is config'd - abort
        elif self.game.drunk_multiball.starting and self.skipDrunk:
            self.game.drunk_multiball.abort_intro()
        # kickoff last call
        elif self.game.last_call.starting:
            self.game.last_call.starting = False
            self.game.last_call.get_going()
        else:
            pass


### shooter lane stuff

    def sw_shooterLane_active_for_800ms(self,sw):
        # if we're dealing with a saved ball, plunge like the wind
        if self.game.trough.balls_to_autoplunge > 0:
            self.game.trough.balls_to_autoplunge -= 1
            print "AUTOPLUNGE, MF - Left to autoplunge " + str(self.game.trough.balls_to_autoplunge)
            self.game.coils.autoPlunger.pulse(self.autoplungeStrength)


    def sw_shooterLane_inactive_for_100ms(self,sw):
        # play the ball lanuch noise
        self.game.sound.play(self.game.assets.sfx_shooterLaunch)
        # kill the player number display if active
        self.game.interrupter.abort_player_number()

    def sw_shooterLane_active_for_3s(self,sw):
        if self.game.drunk_multiball.running:
            self.autoplunge_correct("Drunk Multiball")
        elif self.game.gm_multiball.running:
            self.autoplunge_correct("Goldmine Multiball")
        elif self.game.cva.running:
            self.autoplunge_correct("Cowboys VS Aliens")
        elif self.game.stampede.running:
            self.autoplunge_correct("Stampede Multiball")
        elif self.game.marshall_multiball.running:
            self.autoplunge_correct("Marshall Multiball")
        elif self.game.last_call.running:
            self.autoplunge_correct("Last Call")
        elif self.game.showdown.running:
            self.autoplunge_correct("Showdown")
        elif self.game.moonlight.running and not self.game.moonlight.starting:
            self.autoplunge_correct("Moonlight Madness")
        elif self.game.high_noon.running:
            self.autoplunge_correct("High Noon")
        else:
            pass

    def sw_shooterLane_active_for_5s(self,sw):
        status = self.game.show_tracking('highNoonStatus')
        if status == "RUNNING" or status == "FINISH":
            # do nothing and bail
            return
        # if the ball sits in the shooter lane, flash the player number
        self.game.interrupter.display_player_number(idle=True)

    ### stampede
    def check_stampede(self):
        print "CHECKING STAMPEDE"
        # if both loops are done and the save polly is finished, then it's time to stampede
        if self.game.show_tracking('leftLoopStage') == 4 and \
            self.game.show_tracking('rightLoopStage') == 4 and \
            self.game.show_tracking('centerRampStage') == 5 and \
            self.game.show_tracking('leftRampStage') == 5 and \
            self.game.show_tracking('rightRampStage') == 5:
            # don't start stampede during CVA, Bionic Bart, or High noon
            stackLevel = self.game.show_tracking('stackLevel')
            if True in stackLevel[5:]:
                print "CVA, BB, or High Noon Running - no stampede"
                pass
            elif self.game.trough.num_balls_in_play == 0:
                print "Balls drained before action, pass"
                pass
            elif self.game.gunfight.running:
                print "Stampede check: Gunfight in the way, delaying to try again"
                self.delay(delay=2,handler=self.check_stampede)
            else:
                # if DMB is running and stacking is disabled, don't allow it to start
                if self.game.drunk_multiball.running and not self.drunkStacking:
                    pass
                # this check hopefully prevents concurrent checks from colliding
                if self.game.stampede not in self.game.modes:
                    self.game.modes.add(self.game.stampede)
                    self.game.stampede.start_stampede()
        else:
            pass

    ###
    ###   ___        _      _       _
    ###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      _____
    ### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / / __|
    ### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /\__ \
    ###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/ |___/
    ###
    ### The handling of the Quickdraw targets and lights is here
    ### the actual game mode loads and unloads as needed to set it
    ### at a higher priority so it can take over the DMD -- maybe

    def sw_topLeftStandUp_active(self, sw):
        self.quickdraw_hit('TOP',0)
        ## -- set the last switch hit --
        ep.last_switch = "topLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_bottomLeftStandUp_active(self,sw):
        if self.game.save_polly.paused:
            self.game.interrupter.mad_cow()
        else:
            self.quickdraw_hit('BOT',0)
        ## -- set the last switch hit --
        ep.last_switch = "bottomLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('TOP',1)
        ## -- set the last switch hit --
        ep.last_switch = "topRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_bottomRightStandUp_active(self,sw):
        if self.game.save_polly.paused:
            self.game.interrupter.mad_cow()
        else:
            self.quickdraw_hit('BOT',1)
        ## -- set the last switch hit --
        ep.last_switch = "bottomRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None


    def quickdraw_hit(self, position,side):
        # if the doubler is running, pass on quickdraw hits
        if self.game.doubler in self.game.modes:
            print "Doubler enabled - Passing QD Hit"
        else:
            # lookup the status of the side, and difficulty
            stat = self.game.show_tracking('quickdrawStatus',side)
            difficulty = self.game.user_settings['Gameplay (Feature)']['Quickdraws Lit Difficulty']
            # if quickdraw is running or lit on the side hit, or position matches stat, or bionic bart is running
            if "RUNNING" in self.game.show_tracking('quickdrawStatus') or \
              stat == "READY" or  \
              stat == position or \
              self.game.show_tracking('bionicStatus') == "RUNNING":
                #print "QUICKDRAW IS RUNNING OR LIT"
                # register a lit hit
                self.quickdraw_lit_hit()
            # otherwise quickdraw is NOT running or LIT
            else:
                # register an unlit hit
                self.quickdraw_unlit_hit(position,side,stat,difficulty)

    def quickdraw_lit_hit(self):
        #play the alt sound
        self.game.sound.play(self.game.assets.sfx_quickdrawOn)
        # award some points
        self.game.score(10000)

    def quickdraw_unlit_hit(self,position,side,stat,difficulty):
        # play the sound
        self.game.sound.play(self.game.assets.sfx_quickdrawOff)
        # award the points -- dividing the normal 22500 for lighting quickdraw into 2 parts to acccount for "Hard" difficulty
        self.game.score(10000)
        # if the status is already BOT/TOP or the difficulty is easy
        if stat == "BOT" or stat == "TOP" or  difficulty == "Easy":
            # light quickdraw
            self.light_quickdraw(side)
        # else set the status to the hit target sending the position for the amount and side for the key
        else:
            # will also need to do something with lights here
            self.game.set_tracking('quickdrawStatus',position,side)
            self.lamp_update()

    def light_quickdraw(self,side=9):
        # this is for handling a call to light quickdraw with no side favor the right
        if side == 9:
            target = self.game.show_tracking('quickdrawStatus')
            if target[1] == "READY":
                side = 0
                self.game.game_data['Feature']['Left Quickdraw Lit'] += 1
            else:
                self.game.game_data['Feature']['Right Quickdraw Lit'] += 1
                side = 1
        # add the rest of the points for lighting the quickdraw
        self.game.score(12500)
        # turn on the quickdraw light
        # play a quote from the stack
        self.game.base.play_quote(self.game.assets.quote_quickdrawLit)
        # set the status for the hit side to READY
        self.game.set_tracking('quickdrawStatus',"READY",side)
        self.lamp_update()

    ###
    ###  ____
    ### | __ )  ___  _ __  _   _ ___
    ### |  _ \ / _ \| '_ \| | | / __|
    ### | |_) | (_) | | | | |_| \__ \
    ### |____/ \___/|_| |_|\__,_|___/
    ###

    def check_bonus(self):
        # we have to wait until other things finish
        #self.wait_until_unbusy(self.do_bonus)
        self.wait_for_queue(self.do_bonus)

    def do_bonus(self):
        # unload the modes
        self.remove_modes()
        self.wipe_delays()

        # do the bonus right up front so it's on the score
        bonus_points = self.game.show_tracking('bonus') * self.game.show_tracking('bonusX')
        # add the points to the score
        self.game.score(bonus_points)
        # set  a flag for interrupting
        self.doingBonus = True
        # turn off the status OK
        self.game.statusOK = False
        # get the bonus multiplier
        times = self.game.show_tracking('bonusX')
        print "BONUS TIMES: " + str(times)
        # then reset it for next time
        self.game.set_tracking('bonusX',1)
        # then loop through the display
        # get the bonus points
        self.bonus = self.game.show_tracking('bonus')
        # and reset it
        self.game.set_tracking('bonus',0)
        # and clear the running total
        self.runningTotal = 0
    # Original Bonus Display
    #    # throw up a  layer that says bonus as an interstitial
    #    self.layer = self.game.showcase.blink_fill(2,2,3,1,0.3,isOpaque=True,text="BONUS")
    #    # then 1.5 seconds later, move on
    #    self.delay("Bonus Display",delay=1.5,handler=self.display_bonus,param=times)
    # End Original Bonus Display

    # New Test version
        # Blank Track
        trackLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_emptyTrack.frames[0])
        trackLayer.composite_op = "blacksrc"
        # Train animation
        anim = self.game.assets.dmd_bonusTrain
        myWait = len(anim.frames) / 30.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 2
        animLayer.composite_op = "blacksrc"
        # Text Placeholders
        self.bonusTopLine = ep.EP_TextLayer(64,1,self.game.assets.font_7px_az, "center",opaque=True)
        self.bonusTopLineText = str(times) + " X " + ep.format_score(self.bonus) + " ="
        self.bonusScoreLine = ep.EP_TextLayer(64,11,self.game.assets.font_13px_score,"center")
        self.bonusScoreLineText = ep.format_score(bonus_points)
        # Play the train whistle
        self.game.sound.play(self.game.assets.sfx_longTrainWhistle)
        # Play the train sound
        self.game.sound.play(self.game.assets.sfx_trainChugLong)
        # setup the layer
        combined = dmd.GroupedLayer(128,32,[self.bonusTopLine, self.bonusScoreLine,trackLayer,animLayer])
        self.layer = combined
        # Delay the setting the text part
        self.delay("Bonus Display",delay=1.5,handler=lambda: self.bonusTopLine.set_text(self.bonusTopLineText,color=ep.ORANGE))
        self.delay("Bonus Display",delay=1.5,handler=lambda: self.bonusScoreLine.set_text(self.bonusScoreLineText,color=ep.YELLOW))
        # Finish the bonus
        self.delay("Bonus Display",delay=myWait+0.3, handler=self.finish_bonus)


    def display_bonus(self,times):
        background = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_cactusBorder.frames[0])
        titleString = "BONUS " + str(times) + "X"
        titleLine = ep.EP_TextLayer(128/2, 5, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(titleString,color=ep.YELLOW)
        # add the bonus amount to the running total
        self.runningTotal += self.bonus
        pointsLine = dmd.TextLayer(128/2, 17, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(ep.format_score(self.runningTotal))
        # turn the layer on
        self.layer = dmd.GroupedLayer(128,32,[background,titleLine,pointsLine])
        # play a sound
        self.game.sound.play(self.game.assets.sfx_bonusX)
        # tick down the counter of times
        times -= 1
        if times <= 0:
            # if we're at the last one, it's time to finish up
            self.delay("Bonus Display",delay=1.5,handler=self.reveal_bonus)
        else:
            # if not, loop back around after a delay
            self.delay("Bonus Display",delay=0.5,handler=self.display_bonus,param=times)

    def reveal_bonus(self):
        # load up the animation
        anim = self.game.assets.dmd_burstWipe
        myWait = len(anim.frames) / 15.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 4
        self.layer = animLayer
        self.delay("Bonus Display",delay=myWait,handler=self.finish_bonus)

    def finish_bonus(self):
        # Clear the party mode display
        if self.game.party_setting != 'Disabled':
            self.game.party_mode.clear_layer()
     #   # set up the text display
     #   anim = self.game.assets.dmd_burstWipe2
     #   myWait = len(anim.frames) / 15.0 + 1.5
     #   animLayer = ep.EP_AnimatedLayer(anim)
     #   animLayer.hold = True
     #   animLayer.frame_time = 4
     #   animLayer.composite_op = "blacksrc"
     #
     #   titleString = "TOTAL SCORE:"
     #   titleLine = ep.EP_TextLayer(128/2, 5, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(titleString,color=ep.ORANGE)
     #   pointsLine = dmd.TextLayer(128/2, 17, self.game.assets.font_10px_AZ, "center", opaque=False).set_text(ep.format_score(self.game.current_player().score))
     #   self.layer = dmd.GroupedLayer(128,32,[titleLine,pointsLine,animLayer])
        # play a final sound
        self.game.sound.play(self.game.assets.sfx_flourish6)
        # unset the flag
        self.doingBonus = False
     # New Display
        trackLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_emptyTrack.frames[0])
        trackLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.bonusTopLine, self.bonusScoreLine,trackLayer])
        self.bonusTopLine.set_text(self.bonusTopLineText,color=ep.ORANGE)
        self.bonusScoreLine.set_text(self.bonusScoreLineText,blink_frames=10,color=ep.YELLOW)
        self.layer = combined

        # then loop back to end ball
        self.delay("Bonus Display",delay=2,handler=self.game.ball_ended)
        self.delay("Bonus Display",delay=2,handler=self.clear_layer)

    def abort_bonus(self):
        # unset the flag
        self.doingBonus = False
        # cancel the display
        self.cancel_delayed("Bonus Display")
        # and do the end bits
        self.finish_bonus()

    # bozo ball action
    def enable_bozo_ball(self):
        self.game.set_tracking('bozoBall',True)

    def disable_bozo_ball(self):
        self.game.set_tracking('bozoBall',False)

    def collect_bozo_ball(self):
        self.is_busy()
        # add a fake pending extra ball
        self.game.increase_tracking('extraBallsPending')
        # and then collect it
        self.game.mine.collect_extra_ball()
        # and turn off the bozo ball flag
        self.game.set_tracking('bozoBall', False)
        # unbusy in 3 seconds to allow bonus to play after
        self.delay(delay=3,handler=self.unbusy)

    # red flasher flourish thing
    ## a flasher flourish
    def red_flasher_flourish(self,foo='bar'):
        self.flash(self.game.coils.middleRightFlasher)
        self.delay(delay=0.03,handler=self.flash,param=self.game.coils.backRightFlasher)
        self.delay(delay=0.06,handler=self.flash,param=self.game.coils.backLeftFlasher)
        self.delay(delay=0.09,handler=self.flash,param=self.game.coils.middleRightFlasher)
        self.delay(delay=0.12,handler=self.flash,param=self.game.coils.backRightFlasher)
        self.delay(delay=0.15,handler=self.flash,param=self.game.coils.backLeftFlasher)

    def flash(self,bulb):
        bulb.pulse(30)

    # for starting marshall multiball, so other modes can reference it and then quit if necessary
    def kickoff_marshall(self,super=False):
        print "Marshall Multiball Kickoff Attempt"
        # if all the balls drained before this happens - bail
        if self.game.trough.num_balls_in_play == 0:
            print "Well you blew that. Marshall aborted"
            return
        # if we haven't already run marshall multiball - or if it's coming from the super skill shot
        if not self.game.show_tracking('marshallMultiballRun') or super:
            # and nothing else is running
            if True not in self.game.show_tracking('stackLevel'):
                if self.game.marshall_multiball not in self.game.modes:
                    self.game.modes.add(self.game.marshall_multiball)
            else:
                print "Game is busy - Marshall Kickoff Queued"
                self.wait_for_stackLevel(self.kickoff_marshall)

    def wait_for_stackLevel(self,callback):
        # if stack level is clear, run that sucker
        if True not in self.game.show_tracking('stackLevel'):
            callback()
        # if not, loop back
        else:
            self.delay("wait for", delay=1,handler=self.wait_for_stackLevel,param=callback)

    def sw_phantomSwitch_active(self,sw):
        # on a first press, end multiball if we're above 1 ball in play
        if self.game.trough.num_balls_in_play > 1:
            self.game.trough.num_balls_in_play = 1
        # if only one ball is in play, end ball
        else:
            self.game.trough.num_balls_in_play = 0
        self.game.ball_drained()

    def sw_phantomSwitch2_active(self,sw):
        print "ADDING FREE EXTRA BALL"
        # free instant extra ball
        self.game.current_player().extra_balls += 1
        # update the lamps to show extra ball
        self.lamp_update()

    def sw_phantomSwitch3_active(self,sw):
        print ""
        print "******************************"
        print "* SOMETHING ODD/BAD HAPPENED *"
        print "*   JUST BEFORE THIS POINT   *"
        print "******************************"
        print ""

    def sw_phantomSwitch4_active(self,sw):
        pass

    def guns_flash(self,type=1):
        if type == 1:
            self.game.coils.leftGunFlasher.schedule(0x00101010,cycle_seconds=1)
            self.game.coils.rightGunFlasher.schedule(0x00010101,cycle_seconds=1)

    def autoplunge_correct(self,string):
        # if it's still there now, and there's supposed to be balls in play - launch
        if self.game.switches.shooterLane.is_active() and self.game.trough.num_balls_in_play > 0:
            print "AUTO PLUNGE CORRECTION - Triggered by " + string
            self.game.coils.autoPlunger.pulse(self.autoplungeStrength)

    def abort_display(self):
        # fix the audio volume if it's down
        if self.game.squelched:
            self.game.restore_music()


    # multiball saver
    def multiball_saver(self):
        # if multiball ball savers are not enabled - do nothing
        if not self.multiballSaver:
            pass
        else:
            self.game.trough.start_ball_save(num_balls_to_save=8, time=self.multiballSaverTimer, now=True, allow_multiple_saves=True)

    def start_franks(self):
        if self.game.franks_display.running:
            self.game.franks_display.time = 31
        else:
            self.game.modes.add(self.game.franks_display)
