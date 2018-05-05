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
## The Gold Mine Multiball
##

from procgame import dmd
import ep
import random

class GoldMine(ep.EP_Mode):
    """Mining for great justice - For the Gold Mine Multiball, and ... ? """
    def __init__(self,game,priority):
        super(GoldMine, self).__init__(game,priority)
        self.myID = "Gold Mine Multiball"
        self.gmShots = [self.game.left_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_loop,self.game.right_ramp,self.game.mine,self.game.combos]
        motherlodeDifficulty = self.game.user_settings['Gameplay (Feature)']['Motherlode Badge Difficulty']
        if motherlodeDifficulty == 'Easy':
            self.motherlodesForStar = 1
        else:
            self.motherlodesForStar = 3
        self.restartFlag = False
        self.moo = False
        self.keys_index = {'jackpot':list(range(len(self.game.sound.sounds[self.game.assets.quote_jackpot])))}
        self.counts_index = {'jackpot':0}
        random.shuffle(self.keys_index['jackpot'])

    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.restartFlag = False
        self.restarted = False
        self.game.switch_blocker('add',self.myID)
        self.set_motherlode_value()
        self.displayMotherlodeValue = 0
        self.counter = 0
        self.multiplier = False
        self.bandits = False
        self.banditTimer = 0
        self.banditsUp = 0
        self.jackpots = 0
        self.moo = False
        self.halted = False
        # reset the jackpots to false to prevent lights until the mode really starts
        for i in range(0,5,1):
            self.game.set_tracking('jackpotStatus',False,i)
        # set the restart timer based on user settings
        self.restartTimer = self.game.user_settings['Gameplay (Feature)']['Gold Mine Restart Timer']
        # check the difficulty setting for restart
        value = self.game.user_settings['Gameplay (Feature)']['Gold Mine Multiball Restart']
        if value == "No":
            # if not allowed, set the flag to true right from the start
            self.restarted = True
        # Bring in the doubler if it's enabled
        self.game.load_doubler()

    def ball_drained(self):
        # if we're dropping down to one ball, and goldmine multiball is running - do stuff
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('mineStatus') == "RUNNING":
            self.game.base.busy = True
            self.game.base.queued += 1
            self.end_multiball()
        elif self.game.trough.num_balls_in_play == 1 and self.running:
            print "Down to one ball"
            if not self.restarted and not self.game.show_tracking("starStatus",0):
                self.restartFlag = True
                self.restarted = True
                self.cancel_delayed("Display")
                # drop the bad guys in case there are bandits up
                if self.bandits:
                    self.end_bandits(win=False)
                self.game.sound.play_music(self.game.assets.music_tensePiano1,loops=-1)
                self.clear_layer()
                self.lamp_update()
                # stop the mountain just in case motherlode is lit
                self.stop_mountain()
                # open the mountain for an easy shot
                self.game.mountain.full_open()
                self.restart_option()
            # otherwise, end just like no ball action
            else:
                print "Second 1 ball drain routine"
                self.game.base.busy = True
                self.game.base.queued += 1
                self.end_multiball()
        else:
            pass

    ### switches
    def sw_leftLoopTop_active(self,sw):
        if not self.restartFlag:
            self.process_shot(0)

    def sw_leftRampEnter_active(self, sw):
        if not self.restartFlag:
            self.process_shot(1)

    def sw_centerRampMake_active(self, sw):
        if not self.restartFlag:
            self.process_shot(2)

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving and not self.restartFlag:
            self.process_shot(3)

    def sw_rightRampMake_active(self, sw):
        if not self.restartFlag:
            self.process_shot(4)

    # bumpers for restart pause
    def sw_leftJetBumper_active(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    def sw_rightJetBumper_active(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    # mine for restart pause
    def sw_minePopper_active_for_150ms(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    # saloon popper for restart pause
    def sw_saloonPopper_active_for_150ms(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    # bonus lanes restart pause
    def sw_leftBonusLane_active(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    def sw_rightBonusLane_active(self,sw):
        if not self.halted and self.restartFlag:
            self.halt()

    # the halt routine
    def halt(self):
        self.halted = True
        self.cancel_delayed("Restart Timer")
        self.restart_hold_display()

    # restart switches - jet bumpers exit and saloon clear
    def sw_jetBumpersExit_active(self,sw):
        if self.halted and self.restartFlag:
            self.remove_halt()

    def sw_saloonPopper_inactive(self,sw):
        if self.halted and self.restartFlag:
            self.remove_halt()

    # restart the timer after 1.5 seconds
    def remove_halt(self):
        self.halted = False
        self.delay("Restart Timer",delay=1.5,handler=self.restart_option)

    def process_shot(self,shot):
        # we've hit a potential jackpot
        print "JACKPOT STATUS: " + str(self.game.show_tracking('jackpotStatus',shot))
        # if 0 and 3 are out, for the loop shots, pop the gate for a roll through
        if self.game.show_tracking('jackpotStatus',0) == False and \
            self.game.show_tracking('jackpotStatus',3) == False:
            if shot == 0:
                # left loop, pulse the right gate
                self.game.coils.rightLoopGate.pulse(240)
            elif shot == 3:
                # right loop, pulse the left gate
                self.game.coils.leftLoopGate.pulse(240)
            else:
                pass

        # check to see if it was an active jackpot - if bandits aren't about
        if self.game.show_tracking('jackpotStatus',shot) and not self.bandits:
            # if it was, set the flag
            self.game.set_tracking('jackpotStatus',False,shot)
            # and add one to the jackpots collected
            self.game.increase_tracking('jackpotsCollected')
            # and update the lamps for that shot
            self.lamp_update()
            # and then award it properly
            self.jackpot_hit()
        # if it wasn't then do something else
        else:
            if shot == 1:
                # left ramp
                self.game.sound.play(self.game.assets.sfx_leftRampEnter)
            elif shot == 2:
                # center ramp
                self.game.sound.play(self.game.assets.sfx_trainWhistle)
            elif shot == 4:
                # right ramp
                self.game.sound.play(self.game.assets.sfx_thrownCoins)
            else:
                pass
            # if a jackpot is already hit, it's just points.
            self.game.score(2530)

    def start_multiball(self):
        # set the stack level flag - since right now only GM Multiball is on stack 3
        self.game.stack_level(4,True)
        print "MULTIBALL STARTING"
        # kill the music
        #self.stop_music()
        # play the multiball intro music
        self.music_on(self.game.assets.music_multiball_intro)
        self.intro_animation()

    def intro_animation(self):
        # load up the animation
        anim = self.game.assets.dmd_multiballStart
        # math out how long it is in play time
        myWait = len(anim.frames) / 10.0
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        animLayer.opaque = True
        animLayer.add_frame_listener(12,self.game.base.priority_quote,param=self.game.assets.quote_gold)
        animLayer.add_frame_listener(24,self.game.base.priority_quote,param=self.game.assets.quote_mine)
        animLayer.add_frame_listener(34,self.ta_da)
        animLayer.add_frame_listener(43,self.game.sound.play,param=self.game.assets.sfx_smashingWood)
        # turn it on
        self.layer = animLayer
        # start the lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_gmStart, repeat=False,callback=self.reset_lamps)
        # when the animation is over go to the next step
        self.delay(delay=myWait,handler=self.intro_banner)

    def reset_lamps(self):
        self.lamp_update()
        self.game.gi_control("ON")

    def ta_da(self):
        self.stop_music()
        self.game.sound.play(self.game.assets.sfx_orchestraFlourish)

    def intro_banner(self):
        # play the sound
        self.game.base.priority_quote(self.game.assets.quote_multiball)
        # generate a flashing thing
        inverse = dmd.FrameLayer(True, frame=self.game.assets.dmd_multiballBannerInverse.frames[0])
        normal = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_multiballBanner.frames[0])
        script = [{'seconds':0.1,'layer':inverse},{'seconds':0.1,'layer':normal}]
        myLayer = dmd.ScriptedLayer(128,32,script)
        self.layer = myLayer

        # show it for a bit - then move on
        self.delay(delay=1.5,handler=self.get_going)

    def get_going(self):
        self.game.game_data['Feature']['Gold Mine Started'] += 1
        self.running = True
        # kick the ball out of the mine
        self.game.mountain.eject()
        # launch up to 2 more balls - or more if drunk multiball or stampede is also running
        if self.game.drunk_multiball.running or self.game.stampede.running:
            ballNumber = 4
        else:
            ballNumber = 3
        if self.game.trough.num_balls_in_play < ballNumber:
            total = ballNumber - self.game.trough.num_balls_in_play
            # turn on the autoplunge
            print("Goldmine Multiball - Launching " + str(total) + "balls")
            self.game.trough.balls_to_autoplunge = total
            self.game.trough.launch_balls(total)
        # reset the jackpot status to available - just in case
        for i in range(0,5,1):
            self.game.set_tracking('jackpotStatus',True,i)
        # update the lamps
        self.lamp_update()
        # kill the intro music and start the multiball music
        #self.stop_music()
        self.music_on(self.game.assets.music_goldmineMultiball)
        # kick into the MB display
        self.main_display()
        # If the multiball ball savers are a thing, do that
        self.game.base.multiball_saver()

    def main_display(self):
        # set up the display during multiball
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_multiballFrame.frames[0])
        # title line
        titleString = "GOLD MINE MULTIBALL"
        if self.game.drunk_multiball.running:
            titleString = "DRUNK MINE MULTIBALL"
        titleLine = ep.EP_TextLayer(128/2, -1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(titleString,color=ep.YELLOW)
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = ep.EP_TextLayer(64, 5, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4,color=ep.DARK_BROWN)
        scoreLine.composite_op = "blacksrc"
        # motherlode line
        # if no motherlode is lit
        if self.game.show_tracking('motherlodeLit') and not self.bandits:
            textString = "MOTHERLODE " + ep.format_score(self.motherlodeValue) + " X " + str(self.game.show_tracking('motherlodeMultiplier'))
        # if the bandits showed up
        elif self.bandits:
            textString = "SHOOT THE BANDITS!"
        else:
            textString = "JACKPOTS LIGHT MOTHERLODE"

        motherLine = ep.EP_TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString,color=ep.YELLOW)
        # jackpot value line
        if self.bandits:
            jackString = "TIME REMAINING: " + str(self.banditTimer)
        else:
            if self.game.drunk_multiball.running:
                jackString = "JACKPOTS = " + str(ep.format_score(1000000))
            else:
                jackString = "JACKPOTS = " + str(ep.format_score(500000))
        jackpotLine = ep.EP_TextLayer(128/2,22,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(jackString,color=ep.DARK_BROWN)
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,scoreLine,motherLine,jackpotLine])
        self.layer = combined
        # loop back in .2 to update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    def jackpot_hit(self,step=1):
        if step == 1:
            # audit
            self.game.game_data['Feature']['Gold Mine Jackpots'] += 1
            # clear the display
            self.abort_display()
            # award the points
            points = 500000
            if self.game.drunk_multiball.running:
                points += 500000
            self.game.score(points)

            # count the jackpot
            self.jackpots += 1
            # increase the motherlode value
            self.motherlodeValue += 250000
            if self.game.drunk_multiball.running:
                self.motherlodeValue += 250000
            # see if the multiplier goes up
            self.multiplier = self.check_multiplier()
            # play the animation
            anim = self.game.assets.dmd_mineCarCrash
            # calcuate the wait time to start the next part of the display
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            animLayer.opaque = True
            self.layer = animLayer
            # play a quote
            self.game.sound.play(self.game.assets.sfx_revRicochet)
            # loop back to step 2
            self.delay(name="Display",delay=myWait,handler=self.jackpot_hit,param=2)
        if step == 2:
            # grab the last frame of the minecart crash
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_mineCarCrash.frames[9])
            # and setup the text layer to say jackpot
            jackpotLine = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_goldmineJackpot.frames[0])
            # then do the transition
            transition = ep.EP_Transition(self,backdrop,jackpotLine,ep.EP_Transition.TYPE_CROSSFADE)
            # play a quote
            self.play_ordered_quote(self.game.assets.quote_jackpot,'jackpot',priority=True)
            # and loop back for step 3
            self.delay(name="Display",delay=.8,handler=self.jackpot_hit,param=3)
        if step == 3:
            # then show 'multiball jackpot' with points
            awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=True)
            awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
            awardTextTop.set_text("MULTIBALL JACKPOT",color=ep.ORANGE)
            bottomString = str(ep.format_score(500000))
            if self.game.drunk_multiball.running:
                bottomString = str(ep.format_score(1000000))
            awardTextBottom.set_text(bottomString,blink_frames=4,color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[awardTextTop,awardTextBottom])
            self.layer = combined
            # turn on the motherlode if needed
            self.check_motherlode()
            # if multipier went up, we go there, not, it's back to main
            if self.multiplier:
                handler = self.display_multiplier
                # and reset the jackpots
                for i in range(0,5,1):
                    self.game.set_tracking('jackpotStatus',True,i)
                # and refresh all the lamps
                self.lamp_update()

            else:
                handler = self.main_display
            # go back to the main display
            self.delay(name="Display",delay=1.5,handler=handler)

    def mine_shot(self):
        # if we're restarting - do that
        if self.restartFlag:
            self.restartFlag = False
            self.cancel_delayed("Restart Timer")
            self.cancel_delayed("Restart Music")
            # play the quote
            self.game.base.priority_quote(self.game.assets.quote_multiball)
            self.get_going()

        elif self.game.show_tracking('motherlodeLit') and not self.bandits:
            # if motherlode is lit, collect it on the first multiball, otherwise divert to the bandits if enabled
            if self.game.show_tracking('goldMineStarted') >= 2 and self.game.user_settings['Gameplay (Feature)']['Gold Mine Bandits'] == 'Enabled':
                self.bandits = True
            self.motherlode_hit()
        else:
            # if no motherlode, score some points and kick the ball out
            self.game.score(2530)
            self.game.mountain.kick()

    def check_motherlode(self):
        # is the motherlode already lit?
        if not self.game.show_tracking('motherlodeLit'):
            # if not, turn some junk on because it should be
            self.game.set_tracking('motherlodeLit',True)
            # log the hit in audits
            self.game.game_data['Feature']['Motherlodes Lit'] += 1

            self.game.mountain.run()
            self.lamp_update()
            self.game.base.play_quote(self.game.assets.quote_motherlodeLit)

    def check_multiplier(self):
        if True not in self.game.show_tracking("jackpotStatus"):
            # if all the jackpots have been hit increase the multiplier
            self.game.increase_tracking('motherlodeMultiplier')
            # and return true to be used to queue the display
            return True
        else:
            return False

    def display_multiplier(self):
            multiplier = self.game.show_tracking('motherlodeMultiplier')
            # and do a display thing
            backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mineEntranceBorder.frames[0])
            awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextBottom = ep.EP_TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
            awardTextTop.set_text("MOTHERLODE",color=ep.YELLOW)
            awardTextBottom.set_text(str(multiplier) + "X",color=ep.GREEN)
            combined = dmd.GroupedLayer(128,32,[backdrop,awardTextTop,awardTextBottom])
            self.layer = combined
            self.delay(name="Display",delay=1.5,handler=self.main_display)

    def motherlode_hit(self):
        # log the hit in audits
        self.game.game_data['Feature']['Motherlode Hits'] += 1
        # stop the mountain
        self.stop_mountain()
        # if the bandits attack, divert there
        if self.bandits:
            self.bandits_arrive()
        else:
            self.collect_motherlode()

    def stop_mountain(self):
        # stop the mountain
        self.game.mountain.stop()
        # turn off the flasher
        self.game.coils.mineFlasher.disable()

    def bandits_arrive(self):
        # clear the display
        self.abort_display()
        # tick up the number of bandit attacks
        attack = self.game.increase_tracking('banditAttacks')
        # show some display
        self.layer = self.game.showcase.make_string(1,2,3,text="BANDITS")
        # play a quote
        self.game.base.priority_quote(self.game.assets.quote_ambushUrge)
        # pop up some targets
        available = [0,1,2,3]
        # the first few attacks are less than 4 guys
        if attack <= 4:
            # the first 2 times is 2 guys
            if attack <= 2:
                myRange = 2
            # the next 2 are 3 guys
            else:
                myRange = 1
            # remove the selected number of bad guys from the choices
            for i in range(0,myRange,1):
                choice = random.choice(available)
                available.remove(choice)
        # raise the available guys at this points
        for i in available:
            self.game.bad_guys.target_up(i)
        # set a counter for how many are up
        self.banditsUp = len(available)
        # set the timer
        self.banditTimer = self.game.user_settings['Gameplay (Feature)']['Gold Mine Bandits Timer'] + 1
        # delay a bit for the display and whatnot, then move on
        self.delay(delay=1.5,handler=self.bandits_begin)

    def bandits_begin(self):
        # play one of the ambush urge quotes
        quotes = [self.game.assets.quote_ambushUrge,self.game.assets.quote_mobStart]
        picked = random.choice(quotes)
        self.game.base.play_quote(picked)
        # kick the ball out
        self.game.mountain.kick()
        # and start it
        self.bandit_timer()
        # update the main display
        self.main_display()


    def bandit_timer(self):
        self.banditTimer -= 1
        # if we get to zero, player lost
        if self.banditTimer <= 0:
            self.end_bandits(False)
        # if we're not at zero yet, loop back around
        else:
            self.delay(name="Bandit Timer", delay=1,handler=self.bandit_timer)

    def hit_bandit(self,target):
        # tick down the bandits up number
        self.banditsUp -= 1
        # play a hit sound
        self.game.sound.play(self.game.assets.sfx_quickdrawHit)
        # if they're all down, end with a win
        if self.banditsUp <= 0:
            self.end_bandits()

    def end_bandits(self,win=True):
        # if it's a win, collect the motherlode
        if win:
            # cancel the timer
            self.cancel_delayed("Bandit Timer")
            self.collect_motherlode()
        # if it's not, just turn motherlode off
        else:
            self.game.set_tracking('motherlodeLit', False)
            # and turn off the bandits flag here
            self.bandits = False
        self.lamp_update()

    def collect_motherlode(self):
        # turn motherlode off
        self.game.set_tracking('motherlodeLit', False)
        # Check mootherlode
        j = self.game.show_tracking('jackpotStatus')
        if not j[0] and j[1] and j[2] and not j[3] and j[4]:
            self.moo = True
        # clear the display
        self.abort_display()
        # add one to the motherlodes collected - this resets with badge
        motherlodes = self.game.increase_tracking('motherlodesCollected')
        # and one to the total motherlodes for good measure - this one is persistent for the game
        self.game.increase_tracking('motherlodesCollectedTotal')
        # check the multiplier value
        myMultiplier = self.game.show_tracking('motherlodeMultiplier')
        # award the points - motherlode value X multiplier
        # save the current value for the display later
        self.displayMotherlodeValue = self.motherlodeValue
        # calc the points to award
        motherLodeScore = self.motherlodeValue * myMultiplier
        # award the points
        self.game.score(motherLodeScore)
        # track highest shot for motherlode champ
        if motherLodeScore > self.game.show_tracking('motherlodeValue'):
            self.game.set_tracking('motherlodeValue', motherLodeScore)
        # and reset the motherlode value and multiplier
        self.set_motherlode_value()
        # reset the motherlode multiplier
        self.game.set_tracking('motherlodeMultiplier',1)

        # if we've collected enough regular motherlodes, or any motherload with a multiplier, then light the badge
        if motherlodes >= self.motherlodesForStar or myMultiplier > 1:
            # set the star flag for motherlode - it's 0
            self.game.badge.update(0)
            # if we met the requirements for the badge, don't offer restart
            self.restarted = True
        # update the lamps
        self.lamp_update()
        # reset a counter
        self.counter = 0
        # play a quote based on the multiplier
        if myMultiplier == 2:
            sound = self.game.assets.quote_doubleMotherlode
        elif myMultiplier == 3:
            sound = self.game.assets.quote_tripleMotherlode
        else:
            sound = self.game.assets.quote_motherlode
        # play the woosh sound followed by the quote
        self.game.sound.play(self.game.assets.sfx_wooshDing)
        self.delay(delay=1.2,handler=self.game.base.priority_quote,param=sound)
        # then move on to the display
        self.wipe_transition(myMultiplier)

    def wipe_transition(self,multiplier):
        # set up the display during multiball
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_multiballFrame.frames[0])
        # title line
        titleString = "GOLD MINE MULTIBALL"
        if self.game.drunk_multiball.running:
            titleString = "DRUNK MINE MULTIBALL"
        titleLine = ep.EP_TextLayer(128/2, -1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(titleString,color=ep.YELLOW)
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = ep.EP_TextLayer(64, 5, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4,color=ep.DARK_BROWN)
        scoreLine.composite_op = "blacksrc"
        # motherlode line
        # if no motherlode is lit
        if self.game.show_tracking('motherlodeLit') and not self.bandits:
            textString = "MOTHERLODE " + ep.format_score(self.motherlodeValue) + " X " + str(self.game.show_tracking('motherlodeMultiplier'))
        # if the bandits showed up
        elif self.bandits:
            textString = "SHOOT THE BANDITS!"
        else:
            textString = "JACKPOTS LIGHT MOTHERLODE"

        motherLine = ep.EP_TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString,color=ep.YELLOW)
        # jackpot value line
        if self.bandits:
            jackString = "TIME REMAINING: " + str(self.banditTimer)
        else:
            if self.game.drunk_multiball.running:
                jackString = "JACKPOTS = " + str(ep.format_score(1000000))
            else:
                jackString = "JACKPOTS = " + str(ep.format_score(500000))
        jackpotLine = ep.EP_TextLayer(128/2,22,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(jackString,color=ep.DARK_BROWN)

        anim = self.game.assets.dmd_explosionWipe1
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        animLayer.composite_op = "blacksrc"
        myWait = len(anim.frames) / 10.0
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,scoreLine,motherLine,jackpotLine,animLayer])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_lockTwoExplosion)
        if self.moo:
            self.moo = False
            self.delay(delay=myWait,handler=self.award_mootherlode,param=multiplier)
        else:
            self.delay(delay=myWait,handler=self.award_motherlode,param=multiplier)

    def award_mootherlode(self,times):
        moo = times + 3
        mooLayer = ep.EP_AnimatedLayer(self.game.assets.dmd_moother)
        mooLayer.frame_time = 4
        mooLayer.opaque = True
        mooLayer.repeat = True
        mooLayer.hold = False
        scoreText = moo * self.displayMotherlodeValue
        self.game.score(scoreText)
        mooText = dmd.TextLayer(70,12,self.game.assets.font_12px_az_outline,"center",opaque=False)
        mooText.composite_op = "blacksrc"
        mooText.set_text(str(ep.format_score(scoreText)),blink_frames=12)
        anim = self.game.assets.dmd_explosionWipe2
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True, opaque = False,repeat = False, frame_time=6)
        animLayer.composite_op = "blacksrc"

        combined = dmd.GroupedLayer(128,32,[mooLayer,mooText,animLayer])
        self.game.sound.play(self.game.assets.sfx_cow3)
        self.layer = combined
        self.delay("Display",delay=3,handler=self.main_display)
        self.game.mountain.kick()
        self.bandits = False

    def award_motherlode(self,times,overlay=None):
        # tick the counter up
        self.counter += 1
        # tick the times down
        times -= 1
        # setup the display
        awardTextTop = ep.EP_TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=True)
        awardTextTop.set_text(str(self.counter) + "X" + " = " + ep.format_score(self.displayMotherlodeValue * self.counter),color=ep.GREEN)
        motherLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_motherlode.frames[0])
        motherLayer.composite_op = "blacksrc"

        # if we're on the first counter, finish the wipe
        if self.counter == 1:
            # set up the second part of the wipe
            anim = self.game.assets.dmd_explosionWipe2
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True, opaque = False,repeat = False, frame_time=6)
            animLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[awardTextTop,motherLayer,animLayer])
        # otherwise just update the view
        else:
            combined = dmd.GroupedLayer(128,32,[awardTextTop, motherLayer])

        self.layer = combined
        # loop through the multiplier again if times is not zero
        if times == 0:
            # then go back to the main display
            self.delay(name="Display",delay=1.5,handler=self.main_display)
            # and kick the ball out
            self.game.mountain.kick()
            # false the bandits flag in case it's on
            self.bandits = False
        else:
            self.delay(delay=1,handler=self.award_motherlode,param=times)


    def restart_option(self):
        # this loops while we wait for a restart, if there is one
        self.restartTimer -= 1
        if self.restartTimer <= 0:
            self.restartFlag = False
            self.end_multiball()
        else:
            if self.restartTimer == 2:
                self.game.sound.play_music(self.game.assets.music_tensePiano2,loops=-1)
            print "RESTART DISPLAY"
            backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mineEntranceBorder.frames[0])
            awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_5px_AZ,justify="center",opaque=False)
            timeText = dmd.TextLayer(64,17,self.game.assets.font_9px_az,justify="center",opaque=False)
            timeText.composite_op = "blacksrc"
            awardTextTop.set_text("SHOOT THE MINE")
            awardTextBottom.set_text("TO RESTART MULTIBALL")
            if self.restartTimer == 1:
                textLine = "1 SECOND"
            else:
                textLine = str(self.restartTimer) + " SECONDS"
            timeText.set_text(textLine,blink_frames=4)
            combined = dmd.GroupedLayer(128,32,[backdrop,awardTextTop,awardTextBottom,timeText])
            self.layer = combined
            self.delay(name="Restart Timer",delay=1.0,handler=self.restart_option)

    def restart_hold_display(self):
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mineEntranceBorder.frames[0])
        awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_5px_AZ,justify="center",opaque=False)
        timeText = dmd.TextLayer(64,17,self.game.assets.font_9px_az,justify="center",opaque=False)
        timeText.composite_op = "blacksrc"
        awardTextTop.set_text("SHOOT THE MINE")
        awardTextBottom.set_text("TO RESTART MULTIBALL")
        textLine = "PAUSED"
        timeText.set_text(textLine,blink_frames=4)
        combined = dmd.GroupedLayer(128,32,[backdrop,awardTextTop,awardTextBottom,timeText])
        self.layer = combined

    def end_multiball(self):
        # remove the doubler if not running via check_doubler
        self.game.check_doubler()
        self.wipe_delays()
        self.running = False
        # clear the layer
        self.layer = None

        self.update_tracking()

        # cancel any mountain movement and flasher
        self.stop_mountain()
        # reset the mountain to the home position
        self.game.mountain.reset_toy()
        print "MULTIBALL ENDED"
        # start the music back up
        # if save polly is running, turn that on instead
        if self.game.trough.num_balls_in_play > 0:
            if self.game.peril:
                self.music_on(self.game.assets.music_pollyPeril)
            else:
                self.music_on(self.game.assets.music_mainTheme,mySlice=5)
        # unset the busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # set the stack flag back off
        self.game.stack_level(4,False)
        #refresh the mine lights
        self.lamp_update()
        # reset some junk
        self.banditTimer = 0
        self.banditsUp = 0
        self.bandits = False
        self.game.bad_guys.drop_targets()
        # remove the switch blocker
        self.game.switch_blocker('remove',self.myID)
        # unload the mode
        self.unload()

    def tilted(self):
        if self.running:
            self.update_tracking()
        self.running = False
        self.unload()

    def update_tracking(self):
        # turn motherlode off
        self.game.set_tracking('motherlodeLit', False)
        # reset the motherlode multiplier just in case
        self.game.set_tracking('motherlodeMultiplier',1)
        # set the status to open
        self.game.set_tracking('mineStatus','OPEN')

    def abort_display(self):
        self.cancel_delayed("Display")
        self.clear_layer()

    def mode_stopped(self):
        if self.game.switches.minePopper.is_active():
            self.game.mountain.eject()

    def set_motherlode_value(self):
        self.motherlodeValue = 0 + (250000 * self.game.show_tracking('rank'))
