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
        self.comboLights = [self.game.lamps.rightRampCombo,
                            self.game.lamps.leftRampCombo,
                            self.game.lamps.centerRampCombo,
                            self.game.lamps.leftLoopCombo,
                            self.game.lamps.rightLoopCombo]
        # rank - set up the bulb list
        self.rankLamps = [self.game.lamps.rankStranger,
                          self.game.lamps.rankPartner,
                          self.game.lamps.rankDeputy,
                          self.game.lamps.rankSheriff,
                          self.game.lamps.rankMarshall]
        # bad guys
        self.badGuyLamps = [self.game.lamps.badGuyL0,
                            self.game.lamps.badGuyL1,
                            self.game.lamps.badGuyL2,
                            self.game.lamps.badGuyL3]
        self.giLamps = [self.game.lamps.gi01,
                        self.game.lamps.gi02,
                        self.game.lamps.gi03]


    def mode_started(self):
        ## Load up all the base modes
        self.game.modes.add(self.game.interrupter)
        self.game.modes.add(self.game.right_ramp)
        self.game.modes.add(self.game.left_ramp)
        self.game.modes.add(self.game.center_ramp)
        self.game.modes.add(self.game.left_loop)
        self.game.modes.add(self.game.right_loop)
        self.game.modes.add(self.game.mine)
        self.game.modes.add(self.game.saloon)
        # and update the lamps
        self.game.update_lamps()

    def mode_stopped(self):
        # Ensure flippers are disabled
        self.game.enable_flippers(enable=False)
        # Deactivate the ball search logic so it won't search due to no
        # switches being hit.
        self.game.ball_search.disable()
        # shut down all the modes
        self.game.modes.remove(self.game.interrupter)
        self.game.modes.remove(self.game.right_ramp)
        self.game.modes.remove(self.game.left_ramp)
        self.game.modes.remove(self.game.center_ramp)
        self.game.modes.remove(self.game.left_loop)
        self.game.modes.remove(self.game.right_loop)
        self.game.modes.remove(self.game.mine)
        self.game.modes.remove(self.game.saloon)

    def ball_drained(self):
        # if that was the last ball in play need to finish up
        if self.game.trough.num_balls_in_play == 0:
            # turn off all the lights
            for lamp in self.game.lamps:
                lamp.disable()
                # stop the music
            self.game.sound.stop_music()
            # turn off ball save
            self.game.ball_search.disable()
            # turn off the flippers
            self.game.enable_flippers(False)
            if self.game.show_tracking('tiltStatus') != 3:
                # go check the bonus - after that we'll finish the ball
                self.check_bonus()
            else:
                self.layer = None
                self.game.ball_ended()

    def update_lamps(self):
        # reset first
        self.disable_lamps()
        status = self.game.show_tracking('lampStatus')
        ## if status is off, we bail here
        if status == "OFF":
            return
        # the GI lamps
        for lamp in self.giLamps:
                lamp.enable()
        # if status is GI only, we bail here
        if status == "GIONLY":
            return
        # left side - either the playfield light is on or blinking, or the inlane light is on
        left = self.game.show_tracking('quickdrawStatus',0)
        if left == 'OPEN':
            self.game.lamps.leftQuickdraw.enable()
        elif left == 'TOP' or left == 'BOT':
            self.game.lamps.leftQuickdraw.schedule(0x00FF00FF)
        elif left == 'READY':
            self.game.lamps.leftReturnQuickdraw.enable()
        else:
            pass
        # right has 2 lights so if unhit the light appropriate is on, or the inlane if ready
        right = self.game.show_tracking('quickdrawStatus',1)
        if right == 'OPEN':
            self.game.lamps.topRightQuickdraw.enable()
            self.game.lamps.bottomRightQuickdraw.enable()
        elif right == 'TOP':
            self.game.lamps.bottomRightQuickdraw.enable()
        elif right == 'BOT':
            self.game.lamps.topRightQuickdraw.enable()
        elif right == 'READY':
            self.game.lamps.rightReturnQuickdraw.enable()
        else:
            pass
        # bonus lanes
        if self.game.show_tracking('bonusLaneStatus',0) == 'ON':
            self.game.lamps.leftBonusLane.enable()
        if self.game.show_tracking('bonusLaneStatus',1) == 'ON':
            self.game.lamps.rightBonusLane.enable()
        # the rank lights
        rank = self.game.show_tracking('rank')
        # loop through 0 through current rank and turn the lamps on
        for lamp in range(0,(rank +1),1):
            self.rankLamps[lamp].enable()
        # bad guy lights hopefully this sets any lamp that returns true to be on
        for lamp in range(0,4,1):
            status = self.game.show_tracking('badGuysDead',lamp)
            if status:
                self.badGuyLamps[lamp].enable()

    def disable_lamps(self):
        # combos are not disabled here currently
        for lamp in self.rankLamps:
            lamp.disable()
        for lamp in self.badGuyLamps:
            lamp.disable()
        for lamp in self.giLamps:
            lamp.disable()
        self.game.lamps.leftQuickdraw.disable()
        self.game.lamps.bottomRightQuickdraw.disable()
        self.game.lamps.topRightQuickdraw.disable()
        self.game.lamps.leftReturnQuickdraw.disable()
        self.game.lamps.rightReturnQuickdraw.disable()
        self.game.lamps.leftBonusLane.disable()
        self.game.lamps.rightBonusLane.disable()


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
        ## -- set the last switch hit --
        ep.last_switch = "startButton"

    def sw_shooterLane_open_for_1s(self,sw):
        if self.game.ballStarting:
            self.game.ballStarting = False
            ball_save_time = 10
            self.game.ball_save.start(num_balls_to_save=1, time=ball_save_time, now=True, allow_multiple_saves=False)
        else:
            self.game.ball_save.disable()

    def sw_beerMug_active(self,sw):
        # track it, because why not
        self.game.increase_tracking('beerMugHits')
        # score points
        self.game.score(2130)
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # play a quote on a random 1/3 choice
        weDo = random.choice([False,True,False])
        if weDo:
            self.game.sound.play(self.game.assets.quote_beerMug)
        ## -- set the last switch -- ##
        ep.last_switch = 'beerMug'

    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        self.game.modes.add(self.game.service_mode)
        return True

    def music_on(self):
            self.game.sound.play_music(self.game.assets.music_mainTheme, loops=-1)

    def delayed_music_on(self,wait):
        self.delay(delay=wait, handler=self.music_on)

    def clear_layer(self):
        self.layer = None

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
        # if that puts us at three, time to tilt
        if status == 3:
            self.tilt()
        # for 2 or 1 hand off to interrupter jones
        else:
            self.game.interrupter.tilt_danger(status)

    def tilt(self):
        # Process tilt.
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.game.show_tracking('tiltStatus') == 3:

            self.game.interrupter.tilt_display()
            # Disable flippers so the ball will drain.
            self.game.enable_flippers(enable=False)

            # Make sure ball won't be saved when it drains.
            self.game.ball_save.disable()

            # Make sure the ball search won't run while ball is draining.
            self.game.ball_search.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            # Kick balls out of places it could be stuck.
            if self.game.switches.minePopper.is_active():
                self.game.coils.minePopper.pulse(30)
            if self.game.switches.saloonPopper.is_active():
                self.game.coils.saloonPopper.pulse(30)
        #play sound
        #play video

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
        self.game.score(2530)
        # if gunfight is lit - run that passing which side started it
        if self.game.show_tracking('gunfightStatus') == "READY":
            ## TODO - haven't written gunfight yet
            self.game.modes.add(self.game.bad_guys)
            self.game.bad_guys.start_gunfight(side)
            pass
        # else if quickdraw is lit - run that passing which side started it
        elif self.game.show_tracking('quickdrawStatus',side) == "READY":
            # load up the mode
            self.game.modes.add(self.game.bad_guys)
            # fire the startup
            self.game.bad_guys.start_quickdraw(side)
        else:
            pass


    ###
    ###   ___        _   _
    ###  / _ \ _   _| |_| | __ _ _ __   ___  ___
    ### | | | | | | | __| |/ _` | '_ \ / _ \/ __|
    ### | |_| | |_| | |_| | (_| | | | |  __/\__\
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
        self.game.score(2530)
        self.game.sound.play(self.game.assets.sfx_outlane)

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
        ## -- set the last switch hit --
        ep.last_switch = "leftSlingshot"


    def sw_rightSlingshot_active(self,sw):
        self.slingshot_hit()
        ## -- set the last switch hit --
        ep.last_switch = "rightSlingshot"


    def slingshot_hit(self):
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # score points
        self.game.score(3770)

    ###  ____
    ### | __ ) _   _ _ __ ___  _ __   ___ _ __ ___
    ### |  _ \| | | | '_ ` _ \| '_ \ / _ \ '__/ __|
    ### | |_) | |_| | | | | | | |_) |  __/ |  \__\
    ### |____/ \__,_|_| |_| |_| .__/ \___|_|  |___/
    ###                       |_|

    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
        self.bumper_hit('bottom')

    def bumper_hit(self,bumper):
        # TODO add some more interesting purpose to the bumpers?
        # score some points
        self.game.score(5250)
        # play a noise


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
    ###

    def sw_leftBonusLane_active(self,sw):
        self.bonus_lane_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftBonusLane"


    def sw_rightBonusLane_active(self,sw):
        self.bonus_lane_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightBonusLane"


    def bonus_lane_hit(self,side):
        # lookup the status of the lane that got hit
        stat = self.game.show_tracking('bonusLaneStatus',side)
        # if the lane is off
        if stat == "OFF":
            # set the status to on for the lane that got hit
            self.game.set_tracking('bonusLaneStatus',"ON",side)
            self.update_lamps()
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
        self.update_lamps()

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
        self.delay(delay=1.5,handler=self.update_lamps)

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
        ## -- set the last switch hit --
        ep.last_switch = "topLeftStandup"


    def sw_bottomLeftStandUp_active(self,sw):
        self.quickdraw_hit('BOT',0)
        ## -- set the last switch hit --
        ep.last_switch = "bottomLeftStandup"


    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('TOP',1)
        ## -- set the last switch hit --
        ep.last_switch = "topRightStandup"


    def sw_bottomRightStandUp_active(self,sw):
        self.quickdraw_hit('BOT',1)
        ## -- set the last switch hit --
        ep.last_switch = "bottomRightStandup"



    def quickdraw_hit(self, position,side):
        # lookup the status of the side, and difficulty
        stat = self.game.show_tracking('quickdrawStatus',side)
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # if quickdraw is running or lit on the side hit, or position matches stat
        if "RUNNING" in self.game.show_tracking('quickdrawStatus') or stat == "READY" or stat == position:
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
            self.game.set_tracking('quickdrawStatus',position,side)
            self.update_lamps()

    def light_quickdraw(self,side):
        # add the rest of the points for lighting the quickdraw
        self.game.score(12500)
        # turn on the quickdraw light
        # play a quote from the stack
        self.game.sound.play_voice(self.game.assets.quote_quickdrawLit)
        # set the status for the hit side to READY
        self.game.set_tracking('quickdrawStatus',"READY",side)
        self.update_lamps()

    ###
    ###   ____                _
    ###  / ___|___  _ __ ___ | |__   ___  ___
    ### | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|
    ### | |__| (_) | | | | | | |_) | (_) \__\
    ###  \____\___/|_| |_| |_|_.__/ \___/|___/
    ###

    def combo_timer(self):
        # tick down the comboTimer
        self.game.comboTimer -= 1
        # see if it hit zero
        print "COMBO TIMER: " + str(self.game.comboTimer)
        if self.game.comboTimer == 0:
            self.end_combos()
        else:
            # two seconds left, speed up the blink
            if self.game.comboTimer == 2:
                for myLamp in self.comboLights:
                    myLamp.schedule(0x00FF00FF)
            # one second left, speed it up even more
            if self.game.comboTimer == 1:
                for myLamp in self.comboLights:
                    myLamp.schedule(0x0F0F0F0F)
            # if we're not at zero yet, come back in 1 second
            self.delay(name="Combo Timer",delay=1,handler=self.combo_timer)

    def end_combos(self):
        # turn off the lights
        for myLamp in self.comboLights:
            myLamp.disable()
        print "Combos have ENDED"

    def start_combos(self):
        print "Combos are ON"
        # set the timer at the max settings from the game
        self.game.comboTimer = self.game.user_settings['Gameplay (Feature)']['Combo Timer']
        # turn the lights on
        for myLamp in self.comboLights:
            myLamp.schedule(0x0000FFFF)
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
        self.cancel_delayed("clearCombo")
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'cactus-border.dmd').frames[0])
        # build and show the display of combos made & left
        textLine1 = dmd.TextLayer(64,3,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False).set_text("COMBO AWARDED")
        textLine2 = dmd.TextLayer(64,11,self.game.assets.font_9px_az,justify="center",opaque=False)
        textLine3 = dmd.TextLayer(64,25,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        combos = self.game.show_tracking('combos')
        textString2 = str(combos) + " COMBOS"
        textLine2.set_text(textString2,blink_frames=10)
        combosForStar = self.game.user_settings['Gameplay (Feature)']['Combos for Star']
        diff = combosForStar - combos
        if combos > combosForStar:
            comboString = "BADGE COMPLETE!"
        elif combos == combosForStar:
            comboString = "BADGE AWARDED"
        else:
            comboString = str(diff) + " MORE FOR BADGE!"
        textLine3.set_text(comboString)
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        self.layer = combined
        print "I MADE IT THROUGH COMBO DISPLAY"
        self.delay(name="clearCombo",delay=2,handler=self.clear_layer)

    ###
    ###  ____
    ### | __ )  ___  _ __  _   _ ___
    ### |  _ \ / _ \| '_ \| | | / __|
    ### | |_) | (_) | | | | |_| \__\
    ### |____/ \___/|_| |_|\__,_|___/
    ###

    def check_bonus(self):
        # get the bonus multiplier
        times = self.game.show_tracking('bonusX')
        # then reset it for next time
        self.game.set_tracking('bonusX',1)
        # then loop through the display
        # get the bonus points
        self.bonus = self.game.show_tracking('bonus')
        # and reset it
        self.game.set_tracking('bonus',0)
        # and clear the running total
        self.runningTotal = 0
        self.display_bonus(times)

    def display_bonus(self,times):
        background = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'cactus-border.dmd').frames[0])
        titleString = "BONUS " + str(times) + "X"
        titleLine = dmd.TextLayer(128/2, 2, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(titleString)
        # add the bonus amount to the running total
        self.runningTotal += self.bonus
        pointsLine = dmd.TextLayer(128/2, 16, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(ep.format_score(self.runningTotal))
        # turn the layer on
        self.layer = dmd.GroupedLayer(128,32,[background,titleLine,pointsLine])
        # play a sound
        self.game.sound.play(self.game.assets.sfx_bonusX)
        # tick down the counter of times
        times -= 1
        if times <= 0:
            # if we're at the last one, it's time to finish up
            self.reveal_bonus(self.runningTotal)
        else:
            # if not, loop back around after a delay
            self.delay(delay=0.5,handler=self.display_bonus,param=times)

    def reveal_bonus(self,points):
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe.dmd')
        # start the full on animation
        myWait = len(anim.frames) / 8.57
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 7
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.finish_bonus,param=points)

    def finish_bonus(self,points):
        # set up the text display
        titleString = "TOTAL BONUS:"
        titleLine = dmd.TextLayer(128/2, 2, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(titleString)
        pointsLine = dmd.TextLayer(128/2, 16, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(ep.format_score(points))
        newLayer = dmd.GroupedLayer(128,32,[titleLine,pointsLine])
        # crossfade from previous anim
        transition = ep.EP_Transition(self,self.layer,newLayer,ep.EP_Transition.TYPE_CROSSFADE)
        # add the points to the score
        self.game.score(points)
        # play a final sound
        self.game.sound.play(self.game.assets.sfx_flourish6)
        # then loop back to end ball
        self.delay(delay=1.5,handler=self.game.ball_ended)
        self.delay(delay=1.5,handler=self.clear_layer)