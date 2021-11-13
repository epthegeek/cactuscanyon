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
## The Skill Shot mode for working the lasso ramp awards
##

from procgame import dmd,game
import random
import ep


class SkillShot(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(SkillShot, self).__init__(game, priority)
        self.myID = "SkillShot"
        # the lasso layer for overlaying on the icons
        self.lasso = dmd.TextLayer(129, 1, self.game.assets.font_skillshot, "right", opaque=False).set_text("A")
        self.lasso.composite_op = "blacksrc"
        self.mask = dmd.TextLayer(129,1,self.game.assets.font_skillshot,"right",opaque=False).set_text("B")
        self.mask.composite_op = "blacksrc"
        # offset for the icon layer
        self.x = 126
        self.super = False
        self.selecting = False
        self.live = False
        self.lcount = 0
        self.rcount = 0
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
        self.mineLamps = [self.game.lamps.extraBall,
                          self.game.lamps.mineLock]
        # there is no quote for zero or 5
        self.starQuotes = [False,
                           self.game.assets.quote_1light,
                           self.game.assets.quote_2lights,
                           self.game.assets.quote_3lights,
                           self.game.assets.quote_4lights,
                           False]
        self.shots = ['leftLoopTop','leftRampEnter','minePopper','centerRampMake']
        self.active = 0
        self.wasActive = 0
        # check the generosity setting
        if self.game.user_settings['Gameplay (Feature)']['Skillshot Boosts'] == 'Easy':
            self.easy = True
        else:
            self.easy = False
        self.mytValue = self.game.user_settings['Gameplay (Feature)']['Move Your Train Mode']

        self.keys_index = {'welcome':list(range(len(self.game.sound.sounds[self.game.assets.quote_welcomes]))),
                           'super':list(range(len(self.game.sound.sounds[self.game.assets.quote_superSkillShot])))}
        self.counts_index = {'welcome':0,'super':0}
        random.shuffle(self.keys_index['welcome'])
        random.shuffle(self.keys_index['super'])

    def tilted(self):
        # remove thyself if tilted
        self.unload()

    def ball_drained(self):
        # if somehow all the balls go away and this crap is still running, it should unload. SRSLY.
        if self.game.trough.num_balls_in_play == 0:
            self.wipe_delays()
            self.unload()

    def sw_flipperLwL_active(self, sw):
        if self.game.switches.flipperLwL.is_active():
            self.dub_flip()
        if self.selecting and self.game.switches.shooterLane.is_active():
            self.change_prizes(-1)
            return game.SwitchStop
        elif self.super and self.game.switches.shooterLane.is_active() and self.game.user_settings['Gameplay (Feature)']['Super Cheat'] == 'Enabled':
            #print "Left flipper hit - super is active"
            if self.rcount == 5:
                self.lcount += 1
                if self.lcount == 2:
                    self.enable_selecting()
            else:
                self.rcount = 0
                self.lcount = 0
            return game.SwitchStop
        else:
            #print "Left Flipper hit"
            pass

    def sw_flipperLwR_active(self, sw):
        if self.game.switches.flipperLwR.is_active():
            self.dub_flip()
        if self.selecting and self.game.switches.shooterLane.is_active():
            self.change_prizes(1)
            return game.SwitchStop
        elif self.super and self.game.switches.shooterLane.is_active() and self.game.user_settings['Gameplay (Feature)']['Super Cheat'] == 'Enabled':
            #print "right flipper hit - super is active"
            self.rcount += 1
            return game.SwitchStop
        else:
            #print "right flipper hit"
            pass

    def dub_flip(self):
        self.game.interrupter.show_player_scores()

    def sw_shooterLane_inactive(self,sw):
        # turn off selecting when the ball leaves the shooter lane
        if self.selecting:
            self.selecting = False

    def mode_started(self):
        #print "Skillshot Started"
        # reset the super just in case
        self.super = False
        self.kick = False
        self.selecting = False
        self.live = True
        self.lcount = 0
        self.rcount = 0
        self.prizeIndex = 0
        # clear any existing delays
        self.wipe_delays()
        # call the welcome quote - and start the theme song after on the first ball
        duration = self.game.sound.play(self.game.assets.music_drumRiff)
        if self.game.ball == 1 and not self.game.show_tracking('greeted'):
            # set the flag so we only do this onece
            self.game.set_tracking('greeted',True)
            # play a random voice call from a pre-set collection
            self.delay(delay=0.3,handler=lambda: self.play_ordered_quote(self.game.assets.quote_welcomes,'welcome'))
        else:
            # if we're on ball three and the player hasn't reached the replay score - show that
            if self.game.replays:
                if self.game.ball == self.game.balls_per_game and not self.game.show_tracking('replay_earned'):
                    self.game.interrupter.replay_score_display()
            # on any ball other than ball one, announce which players turn it is if there is more than one
            if len(self.game.players) > 1 and not self.game.interrupter.hush:
                playerQuotes = [self.game.assets.quote_playerOne, self.game.assets.quote_playerTwo, self.game.assets.quote_playerThree, self.game.assets.quote_playerFour]
                myDuration = self.game.sound.play(playerQuotes[self.game.current_player_index])
                self.delay(delay=myDuration+0.2, handler=self.star_callout)
            else:
                self.star_callout()
            if self.game.interrupter.hush:
                self.game.interrupter.hush = False
        # fire up the shooter lane groove - maybe should tie this to a ball on the shooter lane. meh.
        self.delay(delay=duration,handler=self.music_on,param=self.game.assets.music_shooterLaneGroove)
        self.generate_prizes()

    def star_callout(self):
        # count the number of un-lit star points
        points = self.game.show_tracking('starStatus')
        left = 0
        for value in points:
            if not value:
                left += 1
        #print "Unlit badge points: " + str(left)
        # set the quote based on left
        theQuote = self.starQuotes[left]
        # play a quote based on how many points are left
        if theQuote:
            self.delay(delay=0.3,handler=self.game.base.play_quote,param=theQuote)

    def generate_prizes(self):
        #print "SKILLSHOT GENERATE PRIZES"
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
            if self.game.ball != 1 and not self.game.max_extra_balls_reached():
                prizes.append("J")

            # increae rank (star) don't include if already at max rank
            if self.game.show_tracking('rank') < 4:
                prizes.append("K")

            # bonus X don't include if bonus already 6x or more
            if self.game.show_tracking('bonusX') < 6:
                # we're probably going to allow bonus x
                additem = True
                # BUT if we're limiting bonus max - check that
                if self.game.bonus_lanes.limited:
                    # If adding 3 would go over, then don't do that
                    if (self.game.show_tracking('bonusX') + 3) > self.game.bonus_lanes.max:
                        additem = False

                if additem:
                    prizes.append("L")

            # center ramp complete (train)
            if self.game.show_tracking('centerRampStage') < 3:
                prizes.append("M")

            # 1 million points (1M) is always available - except for flip count
            if self.game.party_setting == 'Flip Ct':
                # add 100 grand prize
                prizes.append("X")
            else:
                prizes.append("N")

            if self.game.user_settings['Gameplay (Feature)']['Franks N Beans'] == "Enabled" and not self.game.show_tracking('farted'):
                prizes.append("W")
        # here's the super skill shot prizes
        else:
            # 3 million points
            if self.game.user_settings['Gameplay (Feature)']['Super Skill 3 Million'] == "Enabled":
                prizes.append("O")
            # bonus 5x
            if self.game.show_tracking('bonusX') < 9 and\
               self.game.user_settings['Gameplay (Feature)']['Super Skill Bonus X'] == "Enabled":
                # we're probably going to add this item
                additem = True
                # But if bouns x is limited
                if self.game.bonus_lanes.limited:
                    # If adding 5 would go over, then don't do that
                    if (self.game.show_tracking('bonusX') + 5) > self.game.bonus_lanes.max:
                        additem = False

                if additem:
                    prizes.append("P")
            # light gunfight
            if self.game.show_tracking('gunfightStatus') != "READY" and \
               self.game.user_settings['Gameplay (Feature)']['Super Skill Gunfight'] == "Enabled":
                prizes.append("Q")
            # drunk multiball
            if self.game.show_tracking('drunkMultiballStatus') != "READY":
                prizes.append("R")
            # marshall multiball - if it hasn't already run and it is enabled
            if self.game.show_tracking('marshallMultiballRun') != "True" and self.game.badge.marshallValue == 'Enabled':
                prizes.append("U")
            # extra ball
            if not self.game.max_extra_balls_reached():
                prizes.append("J")
            # move your train
            if self.mytValue == "Enabled" and self.game.move_your_train not in self.game.modes and not self.game.train.mytFail:
                prizes.append("S")
            # cva
            prizes.append("T")
            # tribute mode
            if self.game.user_settings['Gameplay (Feature)']['Tribute Mode'] == "Enabled":
                prizes.append("V")

        # initialize some junk
        count = 0
        self.selectedPrizes = ""
        # run a loop to pick five prizes from the prizes list that was built
        if len(prizes) >= (5 - count):
            remove = True
        else:
            remove = False
        while count < 5:
            item = random.randrange(len(prizes))
            self.selectedPrizes += prizes[item]
            if remove:
                prizes.remove(prizes[item])
            else:
                if prizes[item] == "J" or prizes[item] == "W":
                    # only allow extra ball to show up one time, by removing it from the array if it gets picked
                    # same for franks and beans
                    #print "Found " + prizes[item] + " taking out of rotation"
                    prizes.remove(prizes[item])
            count += 1

        # if flip count is on, replace one award with the extra flips per ball
        if self.game.party_setting == 'Flip Ct':
            # pick a random spot for it
            position = random.randrange(4)
            # dict for which prize per ball
            flip_prize = {1: "Y", 2: "Z", 3: "a"}
            # insert the flip count prize at a random location
            self.selectedPrizes = self.selectedPrizes.replace(self.selectedPrizes[position],
                                                              flip_prize[self.game.ball],
                                                              1)

        # Tournament bit! uses the same 5 prizes - and 100,000 place holders if item is lit/unavailable
        if self.game.tournament:
            self.selectedPrizes = ""
            # light bounty? (money bag) don't add if bounty is already lit
            if not self.game.show_tracking('isBountyLit'):
                self.selectedPrizes += "E"
            else:
                self.selectedPrizes += "X"

            # bonus X don't include if bonus already 6x or more
            if self.game.show_tracking('bonusX') < 6:
                additem = True
                if self.game.bonus_lanes.limited:
                    # If adding 3 would go over, then don't do that
                    if (self.game.show_tracking('bonusX') + 3) > self.game.bonus_lanes.max:
                            additem = False

                if additem:
                    self.selectedPrizes += "L"
                else:
                    self.selectedPrizes += "X"

            # increae rank (star) don't include if already at max rank
            if self.game.show_tracking('rank') < 4:
                self.selectedPrizes += "K"
            else:
                self.selectedPrizes += "X"
            # if multiball is ready, then don't include light lock
            if self.game.show_tracking('mineStatus') != "READY":
                self.selectedPrizes += "D"
            else:
                self.selectedPrizes += "X"
            # light quick draw (gun w/ quick draw)
            if self.game.show_tracking('quickdrawStatus',key=1) != "READY":
                self.selectedPrizes += "H"
            else:
                self.selectedPrizes += "X"


        # add the far right symbol to the left side so that it can be slid right
        self.selectedPrizes = self.selectedPrizes[4:5] + self.selectedPrizes
        #print "Selected Prizes: " + self.selectedPrizes
        # if we're not in the super skillshot, update the display right away
        if not self.super:
            #print "UPDATING LAYER AFTER PRIZE GENERATE"
            #self.update_layer()
            self.intro_display()

    def enable_selecting(self):
        self.selecting = True
        self.lcount = 0
        self.rcount = 0
        self.game.sound.play(self.game.assets.quote_yippie)
        self.choices = []
        # dmb
        if self.game.show_tracking('drunkMultiballStatus') != "READY":
            self.choices.append("R")
        # marshal
        if self.game.badge.marshallValue == 'Enabled':
            self.choices.append("U")
        # extra ball
        if not self.game.max_extra_balls_reached():
            self.choices.append("J")
        # cva
        self.choices.append("T")
        # tribute
        if self.game.user_settings['Gameplay (Feature)']['Tribute Mode'] == "Enabled":
            self.choices.append("V")
        self.change_prizes()

    def change_prizes(self,value=0):
        if value != 0:
            self.game.sound.play(self.game.assets.sfx_chime10)
            self.prizeIndex += value
        # if we're over wrap to zero
        if self.prizeIndex >= len(self.choices):
            self.prizeIndex = 0
        # if we're under zero put back to the high end
        if self.prizeIndex < 0:
            self.prizeIndex = (len(self.choices) - 1)
        # build the new string
        letter = str(self.choices[self.prizeIndex])
        self.selectedPrizes = letter+letter+letter+letter+letter+letter
        # update the layer
        self.update_layer()

    def intro_display(self):
        #print "Copying the score layer"
        # copy the score layer
        scoreLayer = self.game.score_display.layer
        self.layer = scoreLayer
        self.delay("Display",delay=1.5,handler=self.intro_transition)

    def intro_transition(self):
        prizeDisplay = self.generate_layer()
        ep.EP_Transition(self,self.layer,prizeDisplay,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_SOUTH,callback=self.update_layer)

    def update_layer(self):
        # cancel any display delays - for the super startup anim
        self.cancel_delayed("Display")
        # set up the text layer of prizes
        self.layer = self.generate_layer()

    def generate_layer(self):
        prizeList = dmd.TextLayer(self.x, 1, self.game.assets.font_skillshot, "right", opaque=True).set_text(self.selectedPrizes)
        return dmd.GroupedLayer(128, 32, [prizeList,self.mask, self.lasso])

    # if the ramp switch gets hit - shift the prizes over
    # take the last prize off the string and stick it back on the front
    def sw_skillBowl_active(self, sw):
        if self.live:
            ## if we're in super, the jackpot shot has to move
            if self.super:
                self.active += 1
                # wrap back around after 3
                if self.active == 5:
                    self.active = 1
                self.super_update_lamps()
                #print "ACTIVE SHOT IS: " + str(self.active)
            ##
            self.game.score(7250,bonus=True)
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
        if self.live:
            self.skillshot_set()

    def skillshot_set(self):
        # don't allow the skillshot to get re-set
        self.live = False
        if not self.super:
            self.skillshot_award()
        else:
            # if we're doing tribute - bump the shot over if it was on the loop
            if self.selectedPrizes[5:] == "V" and self.active == 1:
                self.active = 2
            # update the lamps to start the blinking
            self.super_update_lamps(blink=True)
            if self.active == 1:
                awardStringTop = "SHOOT LEFT LOOP"
                quote = self.game.assets.quote_leftLoopSS
            elif self.active == 2:
                awardStringTop = "SHOOT LEFT RAMP"
                quote = self.game.assets.quote_leftRampSS
            elif self.active == 3:
                self.game.mountain.full_open()
                awardStringTop = "SHOOT THE MINE"
                quote = self.game.assets.quote_mineSS
            else:
                awardStringTop = "SHOOT CENTER RAMP"
                quote = self.game.assets.quote_centerRampSS
            awardStringBottom = "FOR AWARD"
            #self.game.sound.play(self.game.assets.sfx_flourish7)
            self.game.base.play_quote(quote)

            self.award_display(awardStringTop,awardStringBottom,start=False)


    def skillshot_award(self,switch=0):
        # stop the music
        self.stop_music(slice=1)
        # play the sound
        if self.selectedPrizes[5:] == "V":
            self.music_on(self.game.assets.music_tribute)
        else:
            self.game.sound.play(self.game.assets.sfx_flourish7)

        awardStringTop = None
        awardStringBottom = None

        # award the prize -
        if self.selectedPrizes[5:] == "C":
            self.game.score(10)
            awardStringTop = "BANK ROBBERY"
            awardStringBottom = "BOOST"
            # set the bank ramp to completed
            if self.easy:
                self.game.set_tracking('rightRampStage',3)
                self.game.score(250000)
                self.game.add_bonus(100000)
            else:
                self.game.increase_tracking('rightRampStage')
                self.game.score(100000)
                self.game.add_bonus(50000)

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
            if self.easy:
                self.game.set_tracking('leftRampStage',3)
                self.game.score(250000)
                self.game.add_bonus(100000)
            else:
                self.game.increase_tracking('leftRampStage')
                self.game.score(100000)
                self.game.add_bonus(50000)

        elif self.selectedPrizes[5:] == "G":
            # This one is the right loop
            awardStringTop = "TRICK SHOTS"
            awardStringBottom = "BOOST"
            if self.easy:
                self.game.set_tracking('rightLoopStage',4)
                self.game.score(250000)
                self.game.add_bonus(100000)
            else:
                self.game.increase_tracking('rightLoopStage')
                self.game.score(100000)
                self.game.add_bonus(50000)


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
            awardStringBottom ="BOOST"
            if self.easy:
                self.game.set_tracking('leftLoopStage',4)
                self.game.score(250000)
                self.game.add_bonus(100000)
            else:
                self.game.increase_tracking('leftLoopStage')
                self.game.score(100000)
                self.game.add_bonus(50000)


        elif self.selectedPrizes[5:] == "J":
            # audit
            self.game.game_data['Feature']['EB Lit Skillshot'] += 1
            awardStringTop = "EXTRA BALL"
            awardStringBottom ="IS LIT"
            # turn off the skill shot layer
            self.layer = None
          #  callback = None
            if self.super:
          #      callback = self.start_gameplay
                 self.kick = True
            self.game.mine.light_extra_ball(self.start_gameplay)
            return

        elif self.selectedPrizes[5:] == "K":
            # this one is the rank
            awardStringTop = "RANK INCREASED"
            # call the rank increase, which returns title and time
            newRank,duration = self.game.badge.increase_rank()
            awardStringBottom = "TO " + newRank

        elif self.selectedPrizes[5:] == "L":
            self.game.score(1000,bonus=True)
            awardStringTop = "BONUS X"
            awardStringBottom = "INCREASED +3"
            self.game.increase_tracking('bonusX',3)

        elif self.selectedPrizes[5:] == "M":
            awardStringTop = "TRAIN RESCUE"
            awardStringBottom = "BOOST"
            if self.easy:
                self.game.set_tracking('centerRampStage',3)
                self.game.score(250000)
                self.game.add_bonus(100000)
            else:
                self.game.increase_tracking('centerRampStage')
                self.game.score(100000)
                self.game.add_bonus(50000)

        # new 100 grand award
        elif self.selectedPrizes[5:] == "X":
            awardStringTop = ep.format_score(100000)
            awardStringBottom = "POINTS"
            self.game.score(100000)

        # the 1 million prize
        elif self.selectedPrizes[5:] == "N":
            self.game.score(1000000)
            self.game.add_bonus(2370)
            # setup the wipe animation and the text layer
            topText= dmd.TextLayer(128/2,2, self.game.assets.font_5px_bold_AZ, "center", opaque=True).set_text("ONE", blink_frames=5)
            million = ep.EP_TextLayer(128/2,9, self.game.assets.font_20px_az, "center", opaque=False).set_text("MILLION",blink_frames=5,color=ep.ORANGE)
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
            million = ep.EP_TextLayer(128/2,9, self.game.assets.font_20px_az, "center", opaque=False).set_text("MILLION",blink_frames=5,color=ep.ORANGE)
            anim = self.game.assets.dmd_cashWipe
            wipeLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            wipeLayer.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[topText,million,wipeLayer])
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play(self.game.assets.sfx_yeeHoo)
            self.kick = True
            self.delay("Gameplay Start",delay=1.6,handler=self.start_gameplay)
            return
        # bonus x
        elif self.selectedPrizes[5:] == "P":
            self.game.score(1000,bonus=True)
            awardStringTop = "BONUS X"
            awardStringBottom = "INCREASED +5"
            self.game.increase_tracking('bonusX',5)
            self.kick = True
        # gunfight
        elif self.selectedPrizes[5:] == "Q":
            # This one is the gunfight
            self.layer = None
            self.game.score(50000)
            self.game.add_bonus(1200)
            self.super = False
            self.kick = True
            self.game.saloon.light_gunfight(self.game.skill_shot.start_gameplay)
            return

        # drunk multiball
        elif self.selectedPrizes[5:] == "R":
            self.layer = None
            self.game.score(50000)
            self.game.add_bonus(1200)
            # light the dmb
            self.kick = True
            self.game.base.light_drunk_multiball(self.game.skill_shot.start_gameplay)
            return

        # move your train
        elif self.selectedPrizes[5:] == "S":
            awardStringTop = "MOVE"
            awardStringBottom = "YOUR TRAIN"
            # load the mode so the train starts moving
            self.game.modes.add(self.game.move_your_train)
            # if we hit the left loop, call start for MYT after a delay
            self.kick = True
            if switch == 1:
                self.delay("Operational",delay=1.5,handler=self.game.move_your_train.start)
            self.super = False

        # cva
        elif self.selectedPrizes[5:] == "T":
            awardStringTop = "COWBOYS"
            awardStringBottom = "VS ALIENS"
            self.game.set_tracking("cvaStatus", "READY")
            self.super = False
            if switch == 3:
                #if cva is hit on the mine, clear the skillshot display - backup for switches failing
                #self.clear_layer()
                self.game.mountain.busy = True
                self.game.modes.add(self.game.cva)
                self.game.cva.intro(entry = "mine")
                # unload skillshot after 2 seconds
                #self.delay(2,handler=self.unload)
                return

        # marshall multiball
        elif self.selectedPrizes[5:] == "U":
            awardStringTop = "MARSHALL"
            awardStringBottom = "MULTIBALL"
            self.game.base.kickoff_marshall(True)
            self.kick = True
            self.super = False

        # Tribute mode
        elif self.selectedPrizes[5:] == "V":
            awardStringTop = "THIS IS JUST"
            awardStringBottom = "A TRIBUTE"
            self.game.modes.add(self.game.tribute_launcher)
            self.game.tribute_launcher.shot = self.wasActive
            #print "Tribute Shot Set to: " + str(self.game.tribute_launcher.shot)
            self.super = False

        # franks n beans
        elif self.selectedPrizes[5:] == "W":
            awardStringTop = "FRANKS N"
            awardStringBottom = "BEANS"
            self.game.base.start_franks()

        # flip count + 5
        elif self.selectedPrizes[5:] == "Y":
            awardStringTop = "FIVE EXTRA"
            awardStringBottom = "FLIPS ADDED"
            self.game.increase_tracking('Flip Limit',5)

        # flip count + 10
        elif self.selectedPrizes[5:] == "Z":
            awardStringTop = "TEN EXTRA"
            awardStringBottom = "FLIPS ADDED"
            self.game.increase_tracking('Flip Limit',10)

        # flip count + 15
        elif self.selectedPrizes[5:] == "a":
            awardStringTop = "FIFTEEN EXTRA"
            awardStringBottom = "FLIPS ADDED"
            self.game.increase_tracking('Flip Limit',15)

        # call the lamp update so the prize is shown properly
        self.lamp_update()

        #print "SkillShot Awarded " + str(self.selectedPrizes[5:]) + ": " + str(awardStringTop) + " " + str(awardStringBottom)
        self.award_display(awardStringTop,awardStringBottom)

    def award_display(self,awardStringTop,awardStringBottom,start=True):
        # the award icon
        prizeList = dmd.TextLayer(126, 1, self.game.assets.font_skillshot, "right", opaque=False).set_text(self.selectedPrizes[5:])
        # the award text
        awardTextTop = ep.EP_TextLayer(6,10,self.game.assets.font_5px_bold_AZ,justify="left",opaque=False).set_text(awardStringTop,blink_frames=10,color=ep.ORANGE)
        awardTextBottom = ep.EP_TextLayer(6,18,self.game.assets.font_5px_bold_AZ,justify="left",opaque=True).set_text(awardStringBottom,blink_frames=10,color=ep.ORANGE)
        self.layer = dmd.GroupedLayer(128, 32, [awardTextBottom, awardTextTop, prizeList,self.mask, self.lasso])

        # remove after 2 seconds
        self.delay(delay=2,handler=self.clear_layer)
        # if we're in a super skill shot call start gameplay
        #if self.super and start:
        #    self.delay(delay = 2,handler=self.start_gameplay)
        # if we're not in a super, start gameplay now
        # clear the mine if a super was hit that wasn't tribute
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

    # holding flipper starts super skill shot - unless in tournament mode
    def sw_flipperLwL_active_for_2s(self,sw):
        if self.game.switches.shooterLane.is_active():
            if not self.super and not self.game.tournament and self.game.user_settings['Gameplay (Feature)']['Super Skill Shot'] == 'Enabled':
                #print "LEFT FLIPPER ACTIVATING SUPER AFTER 2 SEC"
                self.activate_super()

    def sw_flipperLwR_active_for_2s(self,sw):
        if self.game.switches.shooterLane.is_active():
            if not self.super and not self.game.tournament and self.game.user_settings['Gameplay (Feature)']['Super Skill Shot'] == 'Enabled':
                #print "RIGHT FLIPPER ACTIVATING SUPER AFTER 2 SEC"
                self.activate_super()

    def sw_rightReturnLane_active(self,sw):
        # this is how the actual CC tracks the end of
        # the skillshot and I'm not going to argue
        # if we're not in a super skill shot, start normal gameplay and unload
      #  if not self.super:
      #      self.start_gameplay()
        pass

    def start_gameplay(self,myDelay=2,music=True):
        # home the mine - in case it got used, reset does nothing if it didn't
        self.game.mountain.reset_toy()
        # clear the local layer just in case
        self.layer = None
        # turn off super mode
        self.super = False
        # start the main game music
        if True not in self.game.show_tracking('stackLevel'):
            self.music_on(self.game.assets.music_mainTheme)
        # clear the mine if needed
        if self.kick:
            self.kick = False
            if self.game.switches.minePopper.is_active():
                self.game.mountain.eject()
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
        self.stop_music(slice=1)
        # turn off the table lights
        self.game.set_tracking('lampStatus',"OFF")
        self.lamp_update()
        # pick a jackpot
        choices = [1,2,3,4]
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
        self.play_ordered_quote(self.game.assets.quote_superSkillShot,'super')
        self.delay(delay=myWait,handler=self.music_on,param=self.game.assets.music_drumRoll)
        # show the prizes
        self.delay(name="Display",delay=myWait+1,handler=self.update_layer)
        self.delay(delay=myWait+1,handler=self.unbusy)

    def super_hit(self,made=None,switch=0):
        # unload the switch trap
        self.game.super_filter.unload()
        # kill the active shot to free the mine just in case
        self.wasActive = self.active
        self.active = 0
        # kill the drum roll
        self.stop_music(slice=1)
        # turn the lights back on
        self.game.set_tracking('lampStatus',"ON")
        self.lamp_update()
        if made:
            # if a multiball mode is starting from teh super skillshot - don't turn on ball save
            if self.selectedPrizes[5:] == "T" or self.selectedPrizes[5:] == "U":
                pass
            else:
                self.game.trough.start_ball_save(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=False)
            # award the prize
            self.skillshot_award(switch)
        else:
            # this is to help the mine not get stupid after a miss
            self.wasActive = 0
            # if tribute was on, remove that
            if self.game.tribute_launcher in self.game.modes:
                self.game.tribute_launcher.remove_launcher()
            # start the ball saver
            self.game.trough.start_ball_save(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=False)
            # clear the prizes
            self.selectedPrizes = ""
            duration = self.game.base.priority_quote(self.game.assets.quote_superFail)
            self.start_gameplay(duration)

    def super_update_lamps(self,blink=False):
        self.super_disable_lamps()
        if self.game.lamp_control.lights_out:
            return
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
            for lamp in self.mineLamps:
                if blink:
                    lamp.schedule(0x0F0F0F0F)
                    # also flash the mine flasher
                    self.game.coils.mineFlasher.schedule(0x01010101)
                else:
                    lamp.enable()
        elif self.active == 4:
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
        for lamp in self.mineLamps:
            lamp.disable()
        self.game.coils.mineFlasher.disable()

