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

    ## inlanes
    def sw_rightReturnLane_active(self,sw):
        self.game.sound.play(self.game.assets.sfx_rattlesnake)
        self.game.score(2530)

    def sw_leftReturnLane_active(self, sw):
        self.game.sound.play(self.game.assets.sfx_rattlesnake)
        self.game.score(2530)

    ## Flipper switch detection for flipping the bonus lanes
    def sw_flipperLwR_active(self,sw):
        # toggle the bonus lane
        self.flip_bonus_lane()

    def sw_flipperLwL_active(self,sw):
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
        if not self.game.show_tracking('isLeftBonusLaneLit'):
            # light the light
            # set the lane to on
            self.game.set_tracking('isLeftBonusLaneLit',True)
            # then if they're both on, play the animation and turn them both off
            # and score points accordingly - 100k for completing the pair, 35,000 for one
            if self.is_time_to_increase_bonus():
                self.game.sound.play(self.game.assets.sfx_banjoTaDa)
                self.game.score(100000)
                # play the animation
                self.increase_bonus()
            else:
                self.game.sound.play(self.game.assets.sfx_banjoTrillUp)
                self.game.score(35000)
        # if the lane is already on play the alt sound and add points
        else:
            # play the alt sound
            self.game.sound.play(self.game.assets.sfx_banjoTrillDown)
            # add some points
            self.game.score(15000)

    def sw_rightBonusLane_active(self,sw):
        if not self.game.show_tracking('isRightBonusLaneLit'):
            # play the noise
            # light the light
            # set the lane to on
            self.game.set_tracking('isRightBonusLaneLit',True)
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
        # if the left one is on, turn it off and turn on the right one
        if self.game.show_tracking('isLeftBonusLaneLit'):
            self.game.set_tracking('isLeftBonusLaneLit', False)
            self.game.set_tracking('isRightBonusLaneLit', True)
        # if the right one is on, turn it off and turn on the left one
        elif self.game.show_tracking('isRightBonusLaneLit'):
            self.game.set_tracking('isRightBonusLaneLit', False)
            self.game.set_tracking('isLeftBonusLaneLit', True)
        # if they're both off, do nothing
        else:
            pass

    def is_time_to_increase_bonus(self):
        # if both bonus lanes are lit, return true
        if self.game.show_tracking('isLeftBonusLaneLit') and self.game.show_tracking('isRightBonusLaneLit'):
                return True

    def increase_bonus(self):
        # play the cactus mashing animation
        anim = dmd.Animation().load(self.game.assets.anim_increaseBonusX)
        # calculate the wait for displaying the text
        myWait = (len(anim.frames) / 8.57) - 0.4
        # set the animation
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=7)
        animLayer.add_frame_listener(2,self.play_sfx_cactusMash)
        # run the animation
        self.layer = animLayer
        # increase the bonus
        self.game.increase_tracking('bonusX')
        # turn both lights off
        self.game.set_tracking('isLeftBonusLaneLit', False)
        self.game.set_tracking('isRightBonusLaneLit', False)
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
        self.delay(delay=1.5,handler=self.clear_layer)

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
    ### the actual game mode loads and unloads as needed

    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('topRight')

    def sw_bottomRightStandUp_active(self,sw):
        self.quickdraw_hit('bottomRight')

    def sw_topLeftStandUp_active(self, sw):
        self.quickdraw_hit('topLeft')

    def sw_bottomLeftStandUp_active(self,sw):
        self.quickdraw_hit('bottomLeft')

    def quickdraw_hit(self, target):
        # if quickdraw is not running
        # if the quick draw on that side is lit score points and play alt sound
        # if it's not lit and we're on easy difficulty turn it on
        # if we're on hard difficulty check if both were hit
        # if not just register this hit and set the status
        # if they were both hit, turn it on
        pass