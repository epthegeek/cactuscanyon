##
## This Class is the mode that runs at all times during active play as a catch all
## Any general events that don't apply to any particular mode will end up handled here
## Like awarding points for hitting the slingshots - or the outlanes - or the start
## button is pressed - etc,
##
## Where to put combos? quickdraws? More modes? or stick them here?
## HMMMM


from procgame import *
from assets import *
import ep
import random

class BaseGameMode(game.Mode):
    """docstring for AttractMode"""
    def __init__(self, game,priority):
        super(BaseGameMode, self).__init__(game, priority)
        self.ball_starting = True

    def mode_started(self):
        pass
        # Disable any previously active lamp
        #for lamp in self.game.lamps:
        #    lamp.disable()

        # Turn on the GIs
        # Some games don't have controllable GI's (ie Stern games)
        #self.game.lamps.gi01.pulse(0)
        #self.game.lamps.gi02.pulse(0)
        #self.game.lamps.gi03.pulse(0)
        #self.game.lamps.gi04.pulse(0)

        # Enable the flippers
        #self.game.enable_flippers(enable=True)

        # Put the ball into play and start tracking it.
        # self.game.coils.trough.pulse(40)
        #self.game.trough.launch_balls(1, self.ball_launch_callback)

        # Enable ball search in case a ball gets stuck during gameplay.
        #self.game.ball_search.enable()

        # Reset tilt warnings and status
        #self.times_warned = 0;
        #self.tilt_status = 0

        # In case a higher priority mode doesn't install it's own ball_drained
        # handler.
        #self.game.trough.drain_callback = self.ball_drained_callback

        # Each time this mode is added to game Q, set this flag true.
        #self.ball_starting = True

    #def ball_launch_callback(self):
    #    if self.ball_starting:
    #        self.game.ball_save.start_lamp()

    def mode_stopped(self):

        # Ensure flippers are disabled
        self.game.enable_flippers(enable=False)

        # Deactivate the ball search logic so it won't search due to no
        # switches being hit.
        #self.game.ball_search.disable()

    #def ball_drained_callback(self):
    #    if self.game.trough.num_balls_in_play == 0:
    #        # End the ball
    #        self.finish_ball()


    def finish_ball(self):

        # Turn off tilt display (if it was on) now that the ball has drained.
        if self.tilt_status and self.layer == self.tilt_layer:
            self.layer = None

        self.end_ball()

    def end_ball(self):
        # Tell the game object it can process the end of ball
        # (to end player's turn or shoot again)
        self.game.end_ball()

    def sw_startButton_active(self, sw):
        # if start button is pressed during the game
        # if we're on the first ball and there are less than four players, add one.
        if self.game.ball == 1 and len(self.game.players) < 4:
            self.game.add_player()
            # and play a soundbyte
            if len(self.game.players) == 2:
                self.game.sound.play(self.game.assets.quote_playerTwo)
            elif len(self.game.players) == 3:
                self.game.sound.play(self.game.assets.quote_playerThree)
            elif len(self.game.players) == 4:
                self.game.sound.play(self.game.assets.quote_playerFour)

    #def sw_shooterLane_open_for_1s(self,sw):
    #    if self.ball_starting:
    #        self.ball_starting = False
    #        ball_save_time = 10
    #        self.game.ball_save.start(num_balls_to_save=1, time=ball_save_time, now=True, allow_multiple_saves=False)
        #else:
        #	self.game.ball_save.disable()

    # Note: Game specific item
    # Set the switch name to the launch button on your game.
    # If manual plunger, remove the whole section.

    def sw_beerMug_active(self,sw):
        ## TODO check this point value
        self.game.score(2130)
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # play a quote?
        weDo = random.choice([False,True,False])
        if weDo:
            self.game.sound.play(self.game.assets.quote_beerMug)
        ## -- set the last switch -- ##
        ep.last_switch = 'beerMug'

    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_tilt_active(self, sw):
        if self.times_warned == 2:
            self.tilt()
        else:
            self.times_warned += 1
            #play sound
            #add a display layer and add a delayed removal of it.
            self.game.set_status("Tilt Warning " + str(self.times_warned) + "!")

    def tilt(self):
        # Process tilt.
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.tilt_status == 0:

            # Display the tilt graphic
            self.layer = self.tilt_layer

            # Disable flippers so the ball will drain.
            self.game.enable_flippers(enable=False)

            # Make sure ball won't be saved when it drains.
            self.game.ball_save.disable()
            #self.game.modes.remove(self.ball_save)

            # Make sure the ball search won't run while ball is draining.
            self.game.ball_search.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            # Kick balls out of places it could be stuck.
            if self.game.switches.shooterR.is_active():
                self.game.coils.shooterR.pulse(50)
            if self.game.switches.shooterL.is_active():
                self.game.coils.shooterL.pulse(20)
            self.tilt_status = 1
        #play sound
        #play video

    def music_on(self):
        self.game.sound.play_music(self.game.assets.music_mainTheme, loops=-1)

    def delayed_music_on(self,wait):
        self.delay(delay=wait, handler=self.music_on)

    def clear_layer(self):
        self.layer = None

    ###
    ###  ___       _
    ### |_ _|_ __ | | __ _ _ __   ___  ___
    ###  | || '_ \| |/ _` | '_ \ / _ \/ __|
    ###  | || | | | | (_| | | | |  __/\__\
    ### |___|_| |_|_|\__,_|_| |_|\___||___/
    ###
    ###

    def sw_leftReturnLane_active(self, sw):
        # register a left return lane hit
        self.return_lane_hit(0)

    def sw_rightReturnLane_active(self,sw):
        # register a right return lane hit
        self.return_lane_hit(1)

    def return_lane_hit(self,side):
        # play the sound
        self.game.sound.play(self.game.assets.sfx_rattlesnake)
        # score the points
        self.game.score(2530)
        # if gunfight is lit - run that passing which side started it
        if self.game.show_tracking('gunfightStatus') == "READY":
            ## TODO - haven't written gunfight yet
            self.game.modes.add(self.game.bad_guys)
            self.game.bad_guys.start_gunfight(side)
            pass
        # else if quickdraw is lit - run that passing which side started it
        elif self.game.show_tracking('quickDrawStatus',side) == "READY":
            # load up the mode
            self.game.modes.add(self.game.bad_guys)
            # fire the startup
            self.game.bad_guys.start_quickdraw(side)
        else:
            pass

    ###
    ###  ____  _ _                 _           _
    ### / ___|| (_)_ __   __ _ ___| |__   ___ | |_ ___
    ### \___ \| | | '_ \ / _` / __| '_ \ / _ \| __/ __|
    ###  ___) | | | | | | (_| \__ \ | | | (_) | |_\__\
    ### |____/|_|_|_| |_|\__, |___/_| |_|\___/ \__|___/
    ###                  |___/
    ###

    def sw_leftSlingshot_active(self,sw):
        self.slingshot_hit()

    def sw_rightSlingshot_active(self,sw):
        self.slingshot_hit()

    def slingshot_hit(self):
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # score points
        self.game.score(3770)

    ###
    ###  _____ _ _
    ### |  ___| (_)_ __  _ __   ___ _ __ ___
    ### | |_  | | | '_ \| '_ \ / _ \ '__/ __|
    ### |  _| | | | |_) | |_) |  __/ |  \__\
    ### |_|   |_|_| .__/| .__/ \___|_|  |___/
    ###           |_|   |_|
    ###

    ## Flipper switch detection for flipping the bonus lanes
    def sw_flipperLwL_active(self,sw):
        # toggle the bonus lane
        self.flip_bonus_lane()

    def sw_flipperLwR_active(self,sw):
        # toggle the bonus lane
        self.flip_bonus_lane()

    ###
    ###  ____                          _
    ### | __ )  ___  _ __  _   _ ___  | |    __ _ _ __   ___  ___
    ### |  _ \ / _ \| '_ \| | | / __| | |   / _` | '_ \ / _ \/ __|
    ### | |_) | (_) | | | | |_| \__ \ | |__| (_| | | | |  __/\__\
    ### |____/ \___/|_| |_|\__,_|___/ |_____\__,_|_| |_|\___||___/
    ###
    ### TODO: this still needs to control the lights
    ###

    def sw_leftBonusLane_active(self,sw):
        self.bonus_lane_hit(0)

    def sw_rightBonusLane_active(self,sw):
        self.bonus_lane_hit(1)

    def bonus_lane_hit(self,side):
        # lookup the status of the lane that got hit
        stat = self.game.show_tracking('bonusLaneStatus',side)
        # if the lane is off
        if stat == "OFF":
            # set the status to on for the lane that got hit
            self.game.set_tracking('bonusLaneStatus',"ON",side)
            # light the light
            # points for lighting bonus lane
            self.game.score(35000)
            # then if they're both on now play the animation and turn them both off
            # and score points accordingly - 100k for completing the pair, 35,000 for one
            if self.is_time_to_increase_bonus():
                self.game.sound.play(self.game.assets.sfx_banjoTaDa)
                self.game.score(100000)
                self.increase_bonus()
            else:
                self.game.sound.play(self.game.assets.sfx_banjoTrillUp)
                self.game.score(35000)

        # if the lane is already on play the alternate sound and add points
        else:
            # play the alt sound
            self.game.sound.play(self.game.assets.sfx_banjoTrillDown)
            # add some points
            self.game.score(15000)

    def flip_bonus_lane(self):
        self.game.invert_tracking('bonusLaneStatus')

    def is_time_to_increase_bonus(self):
        # if neither one is off, IT IS TIME
        if "OFF" not in self.game.show_tracking('bonusLaneStatus'):
            return True

    def increase_bonus(self):
        # cancel the "Clear" delay if there is one
        self.cancel_delayed("ClearBonus")

        # play the cactus mashing animation
        anim = dmd.Animation().load(ep.DMD_PATH+'bonus-cactus-mash.dmd')
        # calculate the wait for displaying the text
        myWait = (len(anim.frames) / 8.57) - 0.4
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 7
        animLayer.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.sfx_cactusMash)
        # run the animation
        self.layer = animLayer
        # increase the bonus
        self.game.increase_tracking('bonusX')
        # turn both lights off
        self.game.set_tracking('bonusLaneStatus',"OFF",0)
        self.game.set_tracking('bonusLaneStatus',"OFF",1)
        # after the delay, show the award
        self.delay(delay=myWait,handler=self.show_bonus_award)

    def show_bonus_award(self):
        ## the top text line is just bonus
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextTop.set_text("BONUS:")
        ## The second line is the tracking value + X
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        awardTextBottom.set_text(str(self.game.show_tracking('bonusX')) + "X")
        # combine the text onto the held cactus animation
        newLayer = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # set the layer active
        self.layer = newLayer
        # then 1.5 seconds later, shut it off
        self.delay(name="ClearBonus",delay=1.5,handler=self.clear_layer)

    def play_sfx_cactusMash(self):
        self.game.sound.play(self.game.assets.sfx_cactusMash)

    ###
    ###   ___        _      _       _
    ###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      _____
    ### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / / __|
    ### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /\__\
    ###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/ |___/
    ###
    ### The handling of the Quickdraw targets and lights is here
    ### the actual game mode loads and unloads as needed to set it
    ### at a higher priority so it can take over the DMD -- maybe

    def sw_topLeftStandUp_active(self, sw):
        self.quickdraw_hit('TOP',0)

    def sw_bottomLeftStandUp_active(self,sw):
        self.quickdraw_hit('BOT',0)

    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('TOP',1)

    def sw_bottomRightStandUp_active(self,sw):
        self.quickdraw_hit('BOT',1)


    def quickdraw_hit(self, position,side):
        # lookup the status of the side, and difficulty
        stat = self.game.show_tracking('quickDrawStatus',side)
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # if quickdraw is running or lit on the side hit, or position matches stat
        if "RUNNING" in self.game.show_tracking('quickDrawStatus') or stat == "READY" or stat == position:
            print "QUICKDRAW IS RUNNING OR LIT"
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
            self.game.set_tracking('quickDrawStatus',position,side)

    def light_quickdraw(self,side):
        # add the rest of the points for lighting the quickdraw
        self.game.score(12500)
        # turn on the quickdraw light
        # play a quote from the stack
        self.game.sound.play_voice(self.game.assets.quote_quickDrawLit)
        # set the status for the hit side to READY
        self.game.set_tracking('quickDrawStatus',"READY",side)

    #
    ###   ____                _
    ###  / ___|___  _ __ ___ | |__   ___  ___
    ### | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|
    ### | |__| (_) | | | | | | |_) | (_) \__\
    ###  \____\___/|_| |_| |_|_.__/ \___/|___/
    #


    def combo_timer(self):
        # tick down the comboTimer
        self.game.comboTimer -= 1
        # see if it hit zero
        print "COMBO TIMER: " + str(self.game.comboTimer)
        if self.game.comboTimer == 0:
            self.end_combos()
        else:
            # if we're not at zero yet, come back in 1 second
            self.delay(name="Combo Timer",delay=1,handler=self.combo_timer)

    def end_combos(self):
        # turn off the lights
        print "Combos have ENDED"
        pass

    def start_combos(self):
        print "Combos are ON"
        # set the timer at the max settings from the game
        self.game.comboTimer = self.game.user_settings['Gameplay (Feature)']['Combo Timer']
        # turn the lights on
        pass
        #loop to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.combo_timer)
        # send this back to what called it for use in determining if in a combo or not
        return False

    def combo_hit(self):
        # cancel the current combo_timer delay
        self.cancel_delayed("Combo Timer")
        # add one to the combo total and reset the timer
        self.game.comboTimer = self.game.user_settings['Gameplay (Feature)']['Combo Timer']
        comboTotal = self.game.increase_tracking('combos')
        print "COMBOS: " + str(comboTotal)
        # show a display at this level? have the higher modes turn off their deisplay?
        # or do the display in the other modes? HMM
        # points? # TODO investigate points awarded for combos
        # if we've got enough combos to light the badge, do that
        if comboTotal == self.game.user_settings['Gameplay (Feature)']['Combos for Star']:
            ## TODO actually award the badge
            pass
        # loop back to the timer
        self.delay(name="Combo Timer",delay=1,handler=self.combo_timer)
        # send this back to what called it for use in determining if in a combo or not
        return True

    def combo_display(self):
        # TODO this needs to look a lot better
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'cactus-border.dmd').frames[0])
        # build and show the display of combos made & left
        textLine1 = dmd.TextLayer(64,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False).set_text("COMBO AWARDED")
        textLine2 = dmd.TextLayer(64,11,self.game.assets.font_9px_az,justify="center",opaque=False)
        textLine3 = dmd.TextLayer(64,25,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        combos = self.game.show_tracking('combos')
        textLine2.set_text(str(combos) +" COMBOS",blink_frames=10)
        combosForStar = self.game.user_settings['Gameplay (Feature)']['Combos for Star']
        diff = combosForStar - combos
        if combos > combosForStar:
            comboString = "BADGE COMPLETE!"
        elif combos == combosForStar:
            comboString = "BADGE AWARDED"
        else:
            comboString = str(diff) + " MORE FOR BADGE!"
        textLine3.set_text(comboString)
        display = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        self.layer = display
        self.delay(delay=2,handler=self.clear_layer)