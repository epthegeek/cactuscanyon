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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The Skill Shot mode for working the lasso ramp awards
##

from procgame import *
import cc_modes
import random
import ep


class SkillShot(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(SkillShot, self).__init__(game, priority)
        # the lasso layer for overlaying on the icons
        self.lasso = dmd.TextLayer(129, 1, self.game.assets.font_skillshot, "right", opaque=False).set_text("A")
        self.lasso.composite_op = "blacksrc"
        self.mask = dmd.TextLayer(129,1,self.game.assets.font_skillshot,"right",opaque=False).set_text("B")
        self.mask.composite_op = "blacksrc"
        # offset for the icon layer
        self.x = 126
        self.super = False
        self.leftLoopLamps = [self.game.lamps.leftLoopBuckNBronco,
                              self.game.lamps.leftLoopWildRide,
                              self.game.lamps.leftLoopRideEm,
                              self.game.lamps.leftLoopJackpot]
        self.leftRampLamps = [self.game.lamps.leftRampWhiteWater,
                              self.game.lamps.leftRampWaterfall,
                              self.game.lamps.leftRampSavePolly,
                              self.game.lamps.leftRampJackpot]
        self.centerRampLamps = [self.game.lamps.centerRampCatchTrain,
                                self.game.lamps.centerRampStopTrain,
                                self.game.lamps.centerRampSavePolly,
                                self.game.lamps.centerRampJackpot]
        self.rankSounds = [self.game.assets.quote_rankUpPartner,
                           self.game.assets.quote_rankUpPartner,
                           self.game.assets.quote_rankUpDeputy,
                           self.game.assets.quote_rankUpSheriff,
                           self.game.assets.quote_rankUpMarshall]
        self.shots = ['leftLoopTop','leftRampEnter','centerRampMake']
        self.active = 0

    def ball_drained(self):
        # if somehow all the balls go away and this crap is still running, it should unload. SRSLY.
        if self.game.trough.num_balls_in_play == 0:
            self.unload()

    def mode_started(self):
        # reset the super just in case
        self.super = False
        #print "THOOPER ITH FAHLTH"
        # call the welcome quote - and start the theme song after on the first ball
        duration = self.game.sound.play(self.game.assets.music_drumRiff)
        if self.game.ball == 1 and not self.game.show_tracking('greeted'):
            # set the flag so we only do this onece
            self.game.set_tracking('greeted',True)
            # play a random voice call from a pre-set collection
            self.delay(delay=0.3,handler=self.game.base.play_quote,param=self.game.assets.quote_welcomes)
        # fire up the shooter lane groove - maybe should tie this to a ball on the shooter lane. meh.
        self.delay(delay=duration,handler=self.game.base.music_on,param=self.game.assets.music_shooterLaneGroove)
        self.generate_prizes()

    def generate_prizes(self):
        print "SKILLSHOT GENERATE PRIZES"
        # set up a blank list for prizes
        prizes = []
        # completed items are not added to the random list
        # and maybe putting specific weight on certain items to make them more rare
        # but for now, randomly select 5 items to build the prize list
        if not self.super:
            # right ramp complete (bank)
            if self.game.show_tracking('rightRampStage') < 3:
                prizes.append("C")

            # light lock (padlock)
            # if multiball is ready, then don't include light lock
            if self.game.show_tracking('mineStatus') != "READY":
                prizes.append("D")

            # light bounty? (money bag) don't add if bounty is already lit
            if not self.game.show_tracking('isBountyLit'):
                prizes.append("E")

            # left ramp complete (boat)
            if self.game.show_tracking('leftRampStage') < 3:
                prizes.append("F")

            # right loop complete (gun)
            if self.game.show_tracking('rightLoopStage') < 4:
                prizes.append("G")

            # light quick draw (gun w/ quick draw)
            if self.game.show_tracking('quickdrawStatus',key=1) != "READY":
                prizes.append("H")

            # left loop complete (horse)
            if self.game.show_tracking('leftLoopStage') < 4:
                prizes.append("I")

            # extra ball (ball) don't include on ball 1 or if max extra balls is already hit
            if self.game.ball != 1 and self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
                prizes.append("J")

            # increae rank (star) don't include if already at max rank
            if self.game.show_tracking('rank') < 4:
                prizes.append("K")

            # bonus X don't include if bonus already 6x or more
            if self.game.show_tracking('bonusX') < 6:
                prizes.append("L")

            # center ramp complete (train)
            if self.game.show_tracking('centerRampStage') < 3:
                prizes.append("M")

            # 1 million points (1M) is always available
            prizes.append("N")
        # here's the super skill shot prizes
        else:
            # 3 million points
            prizes.append("O")
            # bonus 5x
            if self.game.show_tracking('bonusX') < 9:
                prizes.append("P")
            # light gunfight
            if self.game.show_tracking('gunfightStatus') != "READY":
                prizes.append("Q")
            # drunk multiball
            if self.game.show_tracking('drunkMultiballStatus') != "READY":
                prizes.append("R")
            # extra ball
            if self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
                prizes.append("J")
            # move your train
            prizes.append("S")
            # cva
            prizes.append("T")

        # initialize some junk
        count = 0
        self.selectedPrizes = ""
        # run a loop to pick five prizes from the prizes list that was built
        while count < 5:
            item = random.randrange(len(prizes))
            self.selectedPrizes += prizes[item]
            # add the far right symbol to the left side so that it can be slid right
            self.selectedPrizes = self.selectedPrizes[4:5] + self.selectedPrizes
            count += 1

        print "Selected Prizes: " + self.selectedPrizes
        # if we're not in the super skillshot, update the display right away
        if not self.super:
            print "UPDATING LAYER AFTER PRIZE GENERATE"
            self.update_layer()

    def update_layer(self):
        # cancel any display delays - for the super startup anim
        self.cancel_delayed("Display")
        # set up the text layer of prizes
        prizeList = dmd.TextLayer(self.x, 1, self.game.assets.font_skillshot, "right", opaque=True).set_text(self.selectedPrizes)
        self.layer = dmd.GroupedLayer(128, 32, [prizeList,self.mask, self.lasso])

    # if the ramp switch gets hit - shift the prizes over
    # take the last prize off the string and stick it back on the front
    def sw_skillBowl_active(self, sw):
        ## if we're in super, the jackpot shot has to move
        if self.super:
            self.active += 1
            # wrap back around after 3
            if self.active == 4:
                self.active = 1
            self.super_update_lamps()
            print "ACTIVE SHOT IS: " + str(self.active)
        ##
        self.game.score_with_bonus(7250)
        # slide the prize list over
        self.game.sound.play(self.game.assets.sfx_skillShotWoosh)
        # blink the flasher
        self.game.coils.middleRightFlasher.pulse(20)
        # shift the prizes over
        self.shift_right()
        # have to figure out some way to make this animate smoothly or something - this works for now
        # catches the first five in one variable and then the next in another and drops the far right
        # then builds a new target string with the new far right symbol at both ends, for shifting
        prizeTemp1 = self.selectedPrizes[0:4]
        prizeTemp2 = self.selectedPrizes[4:5]
        self.selectedPrizes = prizeTemp2 + prizeTemp1 + prizeTemp2

    # if the ramp bottom switch gets hit - award the prize and unload the mode
    def sw_rightRampBottom_active(self, sw):
        if not self.super:
            self.skillshot_award()
        else:
            # update the lamps to start the blinking
            self.super_update_lamps(blink=True)
            if self.active == 1:
                awardStringTop = "SHOOT LEFT LOOP"
                quote = self.game.assets.quote_leftLoopSS
            elif self.active == 2:
                awardStringTop = "SHOOT LEFT RAMP"
                quote = self.game.assets.quote_leftRampSS
            elif self.active == 3:
                awardStringTop = "SHOOT CENTER RAMP"
                quote = self.game.assets.quote_centerRampSS
            awardStringBottom = "FOR AWARD"
            #self.game.sound.play(self.game.assets.sfx_flourish7)
            self.game.base.play_quote(quote)

            self.award_display(awardStringTop,awardStringBottom,start=False)

    def skillshot_award(self):
        # stop the music
        self.game.sound.stop_music()
        # play the sound
        ## TODO might need to move this to specific awards
        self.game.sound.play(self.game.assets.sfx_flourish7)

        # award the prize -
        if self.selectedPrizes[5:] == "C":
            self.game.score(10)
            awardStringTop = "BANK ROBBERY"
            awardStringBottom = "BOOST"
            # set the bank ramp to completed
            self.game.set_tracking('rightRampStage',3)
            self.game.score(250000)
            self.game.add_bonus(100000)

        elif self.selectedPrizes[5:] == "D":
            self.game.score(20)
            # this one is the lock - going to be complicated
            # if no balls have been locked yet, this awards a free lock straight up
            # or if lock is lit, it locks the ball as well
            if self.game.show_tracking('ballsLockedTotal') == 0 or self.game.show_tracking('mineStatus') == "LOCK":
                # turn off the skillshot layer
                self.layer = None
                # run the lock ball routine
                self.game.mine.lock_ball(self.start_gameplay)
                return
            #  Otherwise we have to check some things
            # if it's not lit, are two balls locked
            elif self.game.show_tracking('ballsLocked') == 2:
                # if they are, light multiball
                self.game.mine.light_multiball()
                # set the award text appropriately
                awardStringTop = "MULTIBALL"
                awardStringBottom = "IS LIT"
            # If we get here, this is not the first lock of the game
            # and the lock is not lit, and there are not 2 balls locked
            # so we just light the lock
            else:
                self.game.mine.light_lock()
                # and set the award text
                awardStringTop = "LOCK"
                awardStringBottom = "IS LIT"

        elif self.selectedPrizes[5:] == "E":
            # this one is the bounty
            self.layer = None
            self.game.saloon.light_bounty(self.start_gameplay)
            return

        elif self.selectedPrizes[5:] == "F":
            awardStringTop = "RIVER RESCUE"
            awardStringBottom = "BOOST"
            self.game.set_tracking('leftRampStage',3)
            self.game.score(250000)
            self.game.add_bonus(100000)

        elif self.selectedPrizes[5:] == "G":
            # This one is the right loop
            awardStringTop = "TRICK SHOTS"
            awardStringBottom = "COMPLETE"
            self.game.set_tracking('rightLoopStage',4)
            self.game.score(250000)
            self.game.add_bonus(100000)

        elif self.selectedPrizes[5:] == "H":
            # This one is the quickdraw
            awardStringTop = "QUICK DRAW"
            awardStringBottom ="IS LIT"
            self.game.score(10000)
            self.game.add_bonus(2000)
            # turn on the right quickdraw
            self.game.base.light_quickdraw(1)

        elif self.selectedPrizes[5:] == "I":
            # this one is the left loop
            awardStringTop = "BUCK N BRONCO"
            awardStringBottom ="COMPLETE"
            self.game.set_tracking('leftLoopStage',4)
            self.game.score(250000)
            self.game.add_bonus(100000)

        elif self.selectedPrizes[5:] == "J":
            awardStringTop = "EXTRA BALL"
            awardStringBottom ="IS LIT"
            # turn off the skill shot layer
            self.layer = None
          #  callback = None
          #  if self.super:
          #      callback = self.start_gameplay
            self.game.mine.light_extra_ball(self.start_gameplay)
            return

        elif self.selectedPrizes[5:] == "K":
            # this one is the rank
            awardStringTop = "RANK INCREASED"
            newRank = self.game.increase_tracking('rank')
            ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHAL"]
            awardStringBottom = "TO " + ranks[newRank]
            # play the appropriate rank quote
            duration = self.game.base.priority_quote(self.rankSounds[newRank])
            # if we've made it to marshall, that should start
            if newRank == 4:
                self.delay(delay=duration+0.2,handler=self.game.base.kickoff_marshall)

        elif self.selectedPrizes[5:] == "L":
            self.game.score_with_bonus(1000)
            awardStringTop = "BONUS X"
            awardStringBottom = "INCREASED +3"
            self.game.increase_tracking('bonusX',3)

        # TODO need to ajust this perhaps - for handling polly peril
        elif self.selectedPrizes[5:] == "M":
            awardStringTop = "TRAIN RESCUE"
            awardStringBottom = "BOOST"
            self.game.set_tracking('centerRampStage',3)
            self.game.score(250000)
            self.game.add_bonus(100000)

        elif self.selectedPrizes[5:] == "N":
            self.game.score(1000000)
            self.game.add_bonus(2370)
            # setup the wipe animation and the text layer
            topText= dmd.TextLayer(128/2,2, self.game.assets.font_5px_bold_AZ, "center", opaque=True).set_text("ONE", blink_frames=5)
            million = dmd.TextLayer(128/2,9, self.game.assets.font_20px_az, "center", opaque=False).set_text("MILLION",blink_frames=5)
            anim = self.game.assets.dmd_cashWipe
            wipeLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            wipeLayer.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[topText,million,wipeLayer])
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play(self.game.assets.sfx_yeeHoo)
            self.delay(delay=1.6,handler=self.clear_layer)
            # start gameplay after the delay
            self.delay("Gameplay Start",delay=1.6,handler=self.start_gameplay)
            return

        # super prizes
        # three million
        elif self.selectedPrizes[5:] == "O":
            self.game.score(3000000)
            self.game.add_bonus(6930)
            # setup the wipe animation and the text layer
            topText= dmd.TextLayer(128/2,2, self.game.assets.font_5px_bold_AZ, "center", opaque=True).set_text("THREE", blink_frames=5)
            million = dmd.TextLayer(128/2,9, self.game.assets.font_20px_az, "center", opaque=False).set_text("MILLION",blink_frames=5)
            anim = self.game.assets.dmd_cashWipe
            wipeLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            wipeLayer.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[topText,million,wipeLayer])
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play(self.game.assets.sfx_yeeHoo)
            self.delay("Gameplay Start",delay=1.6,handler=self.start_gameplay)
            return
        # bonus x
        elif self.selectedPrizes[5:] == "P":
            self.game.score_with_bonus(1000)
            awardStringTop = "BONUS X"
            awardStringBottom = "INCREASED +5"
            self.game.increase_tracking('bonusX',5)
        # gunfight
        elif self.selectedPrizes[5:] == "Q":
            # This one is the gunfight
            self.layer = None
            self.game.score(50000)
            self.game.add_bonus(1200)
            # turn on the right quickdraw
            self.game.saloon.light_gunfight(self.game.skill_shot.start_gameplay)
            self.super = False
            return

        # drunk multiball
        elif self.selectedPrizes[5:] == "R":
            self.layer = None
            self.game.score(50000)
            self.game.add_bonus(1200)
            # light the dmb
            self.game.base.light_drunk_multiball(self.game.skill_shot.start_gameplay)
            return

        # move your train
        elif self.selectedPrizes[5:] == "S":
            awardStringTop = "MOVE"
            awardStringBottom = "YOUR TRAIN"
            # load the mode so the train starts moving
            self.game.modes.add(self.game.move_your_train)
            self.super = False

        # cva
        elif self.selectedPrizes[5:] == "T":
            awardStringTop = "COWBOYS"
            awardStringBottom = "VS ALIENS"
            self.game.set_tracking("cvaStatus", "READY")
            self.super = False

        # call the lamp update so the prize is shown properly
        self.game.update_lamps()

        self.award_display(awardStringTop,awardStringBottom)

    def award_display(self,awardStringTop,awardStringBottom,start=True):
        # the award icon
        prizeList = dmd.TextLayer(126, 1, self.game.assets.font_skillshot, "right", opaque=False).set_text(self.selectedPrizes[5:])
        # the award text
        awardTextTop = dmd.TextLayer(6,10,self.game.assets.font_5px_bold_AZ,justify="left",opaque=False).set_text(awardStringTop,blink_frames=10)
        awardTextBottom = dmd.TextLayer(6,18,self.game.assets.font_5px_bold_AZ,justify="left",opaque=True).set_text(awardStringBottom,blink_frames=10)
        self.layer = dmd.GroupedLayer(128, 32, [awardTextBottom, awardTextTop, prizeList,self.mask, self.lasso])

        # remove after 2 seconds
        self.delay(delay=2,handler=self.clear_layer)
        # if we're in a super skill shot call start gameplay
        #if self.super and start:
        #    self.delay(delay = 2,handler=self.start_gameplay)
        # if we're not in a super, start gameplay now
        if start:
            self.delay("Gameplay Start",delay = 2,handler=self.start_gameplay)

    def shift_right(self):
        ## routine to slide the prize display to the right
        # blank script and a counter
        script = []
        count = 0
        for i in range(4,20,4):
            # math out the new origin based on the step
            setX = 126 + i
            # generate the new prize layer with the shifted origin and store it in a list spot
            prizeList=dmd.TextLayer(setX, 1, self.game.assets.font_skillshot, "right", opaque=True).set_text(self.selectedPrizes)
            # combine with the lasso layer
            combined=dmd.GroupedLayer(128,32, [prizeList,self.mask, self.lasso])
            # stick those mothers in a script list
            script.append({'seconds':0.05,'layer':combined})
            count += 1
        # delay 0.2 seconds before updating to the 'new' prize list at the post shifted position
        self.delay(delay=0.2,handler=self.update_layer)
        # put the scripted shift in place!
        self.layer = dmd.ScriptedLayer(128, 32, script)

    def sw_flipperLwL_active_for_2s(self,sw):
        if self.game.switches.shooterLane.is_active():
            if not self.super:
                print "LEFT FLIPPER ACTIVATING SUPER AFTER 2 SEC"
                self.activate_super()

    def sw_flipperLwR_active_for_2s(self,sw):
        if self.game.switches.shooterLane.is_active():
            if not self.super:
                print "RIGHT FLIPPER ACTIVATING SUPER AFTER 2 SEC"
                self.activate_super()

    def sw_rightReturnLane_active(self,sw):
        # this is how the actual CC tracks the end of
        # the skillshot and I'm not going to argue
        # if we're not in a super skill shot, start normal gameplay and unload
      #  if not self.super:
      #      self.start_gameplay()
        pass

    def start_gameplay(self,myDelay=2,music=True):
        # clear the local layer just in case
        self.layer = None
        # turn off super mode
        self.super = False
        # start the main game music
        if True not in self.game.show_tracking('stackLevel'):
            self.game.base.music_on(self.game.assets.music_mainTheme)
        # check if the award finished stampede
        self.game.base.check_stampede()
        # unload in 2 seconds - to give
        # the award junk time to finish
        self.delay(delay=myDelay,handler=self.unload)

    def activate_super(self):
        # turn on a busy flag
        self.is_busy()
        # cancel the idle timer from interrupter jones
        self.game.interrupter.cancel_idle()
        # turn off the music
        self.game.sound.stop_music()
        # turn off the table lights
        self.game.set_tracking('lampStatus',"OFF")
        self.game.update_lamps()
        # pick a jackpot
        choices = [1,2,3]
        self.active = random.choice(choices)
        # then update the local lamps
        self.super_update_lamps()
        # kick the flag
        self.super = True
        # pick the new prizes
        self.generate_prizes()
        # load the switch filter
        self.game.modes.add(self.game.super_filter)

        anim1 = self.game.assets.dmd_superBlink
        anim2 = self.game.assets.dmd_superSkillShot

        # math out the wait
        myWait = len(anim2.frames) / 20.0
        # set the animation
        animLayer = ep.EP_AnimatedLayer(anim2)
        animLayer.hold=True
        animLayer.frame_time = 3
        animLayer.add_frame_listener(16,self.game.sound.play,param=self.game.assets.sfx_ropeCreak)
        animLayer.add_frame_listener(20,self.game.sound.play,param=self.game.assets.sfx_slide)
        animLayer.composite_op = "blacksrc"
        # and the 'super' text layer
        blinkLayer = ep.EP_AnimatedLayer(anim1)
        blinkLayer.hold=True
        blinkLayer.frame_time = 3
        blinkLayer.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_bountyBell)
        blinkLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_bountyBell)

        combined = dmd.GroupedLayer(128,32,[blinkLayer,animLayer])
        # play a lasso throw sound
        self.game.sound.play(self.game.assets.sfx_ropeWoosh)
        # turn it on
        self.layer = combined
        self.game.base.priority_quote(self.game.assets.quote_superSkillShot)
        self.delay(delay=myWait,handler=self.game.base.music_on,param=self.game.assets.music_drumRoll)
        # show the prizes
        self.delay(name="Display",delay=myWait+1,handler=self.update_layer)
        self.delay(delay=myWait+1,handler=self.unbusy)

    def super_hit(self,made=None):
        # unload the switch trap
        self.game.modes.remove(self.game.super_filter)
        # kill the drum roll
        self.game.sound.stop_music()
        # turn the lights back on
        self.game.set_tracking('lampStatus',"ON")
        self.game.update_lamps()
        if made:
            # award the prize
            self.skillshot_award()
        else:
            duration = self.game.base.priority_quote(self.game.assets.quote_superFail)
            self.start_gameplay(duration)

    def super_update_lamps(self,blink=False):
        self.super_disable_lamps()
        # one is the left loop
        if self.active == 1:
            for lamp in self.leftLoopLamps:
                if blink:
                    lamp.schedule(0x0F0F0F0F)
                else:
                    lamp.enable()
        elif self.active == 2:
            for lamp in self.leftRampLamps:
                if blink:
                    lamp.schedule(0x0F0F0F0F)
                else:
                    lamp.enable()
        elif self.active == 3:
            for lamp in self.centerRampLamps:
                if blink:
                    lamp.schedule(0x0F0F0F0F)
                else:
                    lamp.enable()
        else:
            pass

    def super_disable_lamps(self):
        for lamp in self.leftLoopLamps:
            lamp.disable()
        for lamp in self.leftRampLamps:
            lamp.disable()
        for lamp in self.centerRampLamps:
            lamp.disable()

