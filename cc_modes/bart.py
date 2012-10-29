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

###
###  ____             _     ____            _   _
### | __ )  __ _ _ __| |_  | __ ) _ __ ___ | |_| |__   ___ _ __ ___
### |  _ \ / _` | '__| __| |  _ \| '__/ _ \| __| '_ \ / _ \ '__/ __|
### | |_) | (_| | |  | |_  | |_) | | | (_) | |_| | | |  __/ |  \__\
### |____/ \__,_|_|   \__| |____/|_|  \___/ \__|_| |_|\___|_|  |___/
###

from procgame import *
import cc_modes
import ep
import random
import locale

class Bart(ep.EP_Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Bart, self).__init__(game,priority)
        # set up the number of barts required
        self.bartsForStar = self.game.user_settings['Gameplay (Feature)']['Bart Brothers for Star']
        # setup the difficulty
        difficulty = self.game.user_settings['Gameplay (Feature)']['Bart Brothers Difficulty']
        # Easy version
        print "Difficulty is set to - " + difficulty
        if difficulty == 'Easy':
            self.hitsToDefeatBart = [2,4,5,6,7,8]
        # Hard version
        else:
            self.hitsToDefeatBart = [3,5,6,7,8,8]
            # hits banners list
        self.banners = [self.game.assets.dmd_bamBanner,
                        self.game.assets.dmd_biffBanner,
                        self.game.assets.dmd_ouchBanner,
                        self.game.assets.dmd_powBanner,
                        self.game.assets.dmd_whamBanner,
                        self.game.assets.dmd_zoinkBanner]
        # a flag for when bart is in motion
        self.moving = False
        self.bossFight = False
        self.bossWin = False
        self.targetNames = ['Left','Left Center','Right Center','Right']
        self.busy = False

    def mode_started(self):
        # activate the first bart if we're on the first ball
        if self.game.ball == 1:
            self.game.set_tracking('bartStatus',"RUNNING")
            self.setup()

    def ball_drained(self):
        # if boss is running and we lose a ball (or both) boss has to end
        if self.game.trough.num_balls_in_play == 0 and self.bossWin:
            self.busy = False
        elif self.game.trough.num_balls_in_play in (0,1) and self.bossFight:
            self.game.base.busy = True
            self.boss_lose()

    def hit(self,Saloon=False):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()
        # pick a random banner to use
        banner = random.choice(self.banners)
        # set up the banner layer
        self.bannerLayer = dmd.FrameLayer(opaque=False, frame=banner.frames[0])

        # lookup the status
        status = self.game.show_tracking('bartStatus')
        print "BART STATUS: " + status
        print "CURRENT BART: " + str(self.game.show_tracking('currentBart'))
        # if no bart is currently running, a new challenger appears
        bionic = self.game.show_tracking('bionicStatus')
        if bionic == "READY" or bionic == "RUNNING":
            self.game.saloon.busy = False
        if status == "OPEN":
            # if boss is the brother coming up - we don't activate him if other things are running
            if self.game.show_tracking('currentBart') == 3 and True in self.game.show_tracking('stackLevel'):
                self.dead_bart_hit(Saloon)
            else:
                self.game.set_tracking('bartStatus',"RUNNING")
                self.activate()
        # else, register the hit
        elif status == "RUNNING":
            self.damage()
        # if there is one active and it's the last hit, defeat
        elif status == "LAST":
            self.defeat()
        # not running? do this
        else:
            self.dead_bart_hit(Saloon)

    def dead_bart_hit(self,Saloon):
        # intialize this to zero to use later
        duration = 0
        # he's dead waiting for a gun fight
        # no points - play a sound if hit directly
        if not Saloon:
            self.game.sound.play(self.game.assets.sfx_deadBartHit)
        else:
            odds = [False,False,True,False]
            choice = random.choice(odds)
            if choice:
                duration = self.game.base.play_quote(self.game.assets.quote_nobodysHome)
        # if we're waiting for a sound effect delay the busy release
        if duration > 0:
            self.delay(delay=duration,handler=self.game.saloon.unbusy)
        # otherwise do it now
        else:
            self.game.saloon.unbusy()

    def activate(self):
        # set up all the strings & quotes
        self.setup()
        # show the 'challenges you' display
        # clear the banner layer
        textLayer1 = dmd.TextLayer(42,2,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer1.set_text(self.nameLine)
        textLayer2 = dmd.TextLayer(42,16,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer2.set_text("CHALLENGES")
        textLayer3 = dmd.TextLayer(42,24,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer3.set_text("YOU")

        textLayer = dmd.GroupedLayer(128,32,[self.wantedFrameB,textLayer1,textLayer2,textLayer3])
        # play the intro
        self.game.base.play_quote(self.introQuote)
        # show the transition
        transition = ep.EP_Transition(self,self.game.score_display.layer,textLayer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        # divert here if we're on boss bart
        if self.brother == 'BOSS':
            # stop the music
            self.game.sound.stop_music()
            # set the flag
            self.bossFight = True
            # set the stacking level
            self.game.set_tracking('stackLevel',True,5)
            self.delay(delay=1.5,handler=self.activate_boss)
        else:

            # if there's only 1 hit to defeat this bart, set the status to last
            if self.hitsThisBart == 1:
                self.game.set_tracking('bartStatus',"LAST")
            self.delay("Display",delay=1.5,handler=self.clear_layer)

    def activate_boss(self):
        # bump up the points
        self.hitValue *= 2
        self.defeatValue *= 2
        # set some defaults - for target work
        self.bossTargetTimer = [None,None,None,None]
        self.deathTally = 0

        # set the hits to defeat value - 3 for the first, 6 for the second, etc
        self.hitsThisBart = (self.game.show_tracking('bossBartsDefeated') + 1) * 3
        # activate the drop targets
        self.game.bad_guys.setup_targets()
        # add a ball
        self.game.trough.balls_to_autoplunge = 1
        self.game.trough.launch_balls(1)
        # eject the saloon - by clearing the busy flag
        self.game.saloon.unbusy()
        # start some song?
        self.game.base.music_on(self.game.assets.music_steampunk)
        # kill the lights
        self.kill_lights()
        # flash the lights on front of the saloon
        self.game.lamps.saloonArrow.schedule(0xF0F0F0F0)
        self.game.lamps.bountySaloon.schedule(0xF0F0F0F0)

        # go to the boss fight display
        self.boss_display()

    def setup(self):
        # our cast of characters
        names = ('big','bandelero','bubba','boss')
        hits = (self.game.assets.quote_hitBigBart, self.game.assets.quote_hitBandeleroBart,self.game.assets.quote_hitBubbaBart,self.game.assets.quote_hitBossBart)
        taunts = (self.game.assets.quote_tauntBigBart, self.game.assets.quote_tauntBandeleroBart,self.game.assets.quote_tauntBubbaBart,self.game.assets.quote_tauntBossBart)
        defeats = (self.game.assets.quote_defeatBigBart, self.game.assets.quote_defeatBandeleroBart,self.game.assets.quote_defeatBubbaBart,self.game.assets.quote_defeatBossBart)
        intros = (self.game.assets.quote_introBigBart, self.game.assets.quote_introBandeleroBart,self.game.assets.quote_introBubbaBart,self.game.assets.quote_introBossBart)
        posterA = (self.game.assets.dmd_bigPosterA, self.game.assets.dmd_bandeleroPosterA, self.game.assets.dmd_bubbaPosterA,self.game.assets.dmd_bossHit)
        posterB = (self.game.assets.dmd_bigPosterB, self.game.assets.dmd_bandeleroPosterB, self.game.assets.dmd_bubbaPosterB,self.game.assets.dmd_boss)
        # look up which one is current
        index = self.game.show_tracking('currentBart')
        # setting up all the bits like name for text display
        self.brother = names[index].upper()
        # wanted poster
        self.wantedFrameA = dmd.FrameLayer(opaque=False, frame=posterA[index].frames[0])
        self.wantedFrameA.composite_op = "blacksrc"
        self.wantedFrameB = dmd.FrameLayer(opaque=False, frame=posterB[index].frames[0])
        # hit quotes
        self.hitQuote = hits[index]
        # taunt quotes
        self.tauntQuote = taunts[index]
        # death quote
        self.defeatQuote = defeats[index]
        # intro quote
        self.introQuote = intros[index]
        defeated = self.game.show_tracking('bartsDefeatedTotal')
        # setup the points value? 120,000 + 5,000 times the number of defeated barts
        self.hitValue = 120000 + (5000 * defeated)
        self.hitString = locale.format("%d", self.hitValue, True) # Add commas
        # setup the defeat value 150,000 for first + 50,000 times the number of defeated barts
        self.defeatValue = 150000 + (50000 * defeated)
        self.defeatString = locale.format("%d", self.defeatValue, True) # Add commas
        # setup the hits needed to defeat this bart
        # trim back to 5 if over 5 defeated to avoid crash
        if defeated > 5:
            defeated = 5
        self.hitsThisBart = self.hitsToDefeatBart[defeated]
        # set up the name line for the cards
        print self.brother + " IS THE BROTHER"
        if self.brother != "BANDELERO":
            self.nameLine = self.brother.upper() + " BART"
        else:
            self.nameLine = self.brother


    def damage(self,saloonHit=False):
        print "DAMAGE BART"
        # play a quote appropriate to the current bart
        self.game.base.priority_quote(self.hitQuote)
        # move bart
        self.animate(1)

        # score the points
        self.game.score(self.hitValue)
        # flash the light and move the dude
        # a flourish lampshow
        if self.bossFight:
            myCallback = None
        else:
            myCallback = self.game.update_lamps
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=myCallback)
        # display the info
        # register the hit
        # increase the hits on bart - and store the new amount
        currentHits = self.game.increase_tracking('bartHits')
        # check to see if we're on the last hit now - meaning, our hit total is one less than defeat
        # math the remaining hits
        print "HITS FOR THIS BART: " + str(self.hitsThisBart)
        print "CURRENT HITS: " + str(currentHits)
        if currentHits > self.hitsThisBart:
            self.hitsThisBart = currentHits
        hitsLeft = self.hitsThisBart - currentHits
        if hitsLeft <= 1:
            # if it is, set the status to last
            self.game.set_tracking('bartStatus',"LAST")
        theText = str(hitsLeft) + " MORE HITS"
        textLayer1 = dmd.TextLayer(42,1,self.game.assets.font_7px_bold_az,justify="center",opaque=False).set_text(self.nameLine)
        textLayer2 = dmd.TextLayer(42,9,self.game.assets.font_7px_bold_az,justify="center",opaque=False).set_text(str(self.hitString))
        textLayer3 = dmd.TextLayer(42,17,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(theText)
        textLayer4 = dmd.TextLayer(42,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text("TO COLLECT")
        self.textLayer = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,textLayer3,textLayer4])
        self.textLayer.composite_op = "blacksrc"
        # play a fancy lamp show
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, False, self.game.update_lamps)
        # if we're boss fighting, go to that display
        if self.bossFight:
            self.boss_damage_display()
        else:
            self.display_damage_one()

    def defeat(self):
        print "DEFEATING BART"
        # add to the defeated barts - this one doesn't count boss barts
        if not self.bossFight:
            self.game.increase_tracking('bartsDefeated')
        # tick up the global count as well - this one does count boss barts
        globalTotal = self.game.increase_tracking('bartsDefeatedTotal')
        # move bart
        self.animate(1)
        # play a defeated quote
        myWait = self.game.base.play_quote(self.defeatQuote)
        # set the status to dead - gunfight has to set it back to open
        self.game.set_tracking('bartStatus',"DEAD")
        # if we're at the end of the line, reset to 0
        if self.game.show_tracking('currentBart') == 3:
            self.game.set_tracking('currentBart',0)
        # if not tick up the current bart for next time
        else:
            self.game.increase_tracking('currentBart')
            # score some points
        self.game.score(self.defeatValue)
        # reset the hits on bart
        self.game.set_tracking('bartHits',0)
        # play a fancy lampshow
        if self.bossFight:
            myCallback = self.kill_lights
            self.bossWin = True
            self.busy = True
        else:
            myCallback = self.game.update_lamps
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, False, myCallback)

        # divert to boss win here
        if self.bossFight:
            self.boss_damage_display(False)
            self.delay(delay=myWait,handler=self.boss_win)
        else:
            # setup the display
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_weaveBorder.frames[0])
            textLayer1 = dmd.TextLayer(64,2,self.game.assets.font_9px_az,justify="center",opaque=False).set_text("BART DEFEATED")
            textLayer2 = dmd.TextLayer(64,12,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(self.defeatString))
            if globalTotal < self.bartsForStar:
                thetext = str(self.bartsForStar - globalTotal) + " MORE FOR BADGE"
            elif globalTotal == self.bartsForStar:
                thetext = "BADGE COLLECTED!"
                # actually collect the badge - barts defeated is 2
                self.game.badge.update(2)
            else:
                thetext = str(globalTotal) + " DEFEATED!"
            textLayer3 = dmd.TextLayer(64,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(thetext)
            self.layer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3])

            # light gunfight?
            self.delay(delay=myWait,handler=self.game.saloon.light_gunfight)
            # clear the layer
            self.delay("Display",delay=myWait,handler=self.clear_layer,param=True)

    def display_damage_one(self):
        print "MADE IT TO DAMAGE ONE"
        # set up the top layer
        layerOne = dmd.GroupedLayer(128,32,[self.bannerLayer,self.wantedFrameA])
        # activate it
        self.layer = layerOne
        self.delay("Display",delay=0.2,handler=self.display_damage_two,param=layerOne)

    def display_damage_two(self,layerOne):
        # set up the second layer
        layerTwo = dmd.GroupedLayer(128,32,[self.wantedFrameB,self.textLayer])
        transition = ep.EP_Transition(self,layerOne,layerTwo,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        self.delay("Display",delay = 1.5,handler=self.clear_layer)

    ## BOSS FIGHT STUFF

    def boss_target_hit(self,target):
        # desicde if quote or not
        choices = [False,True]
        bartSpeaks = random.choice(choices)
        if bartSpeaks:
            self.game.base.play_quote(self.game.assets.quote_targetBossBart)
            self.animate(2)
        # cancel the main display
        self.cancel_delayed("Boss Display")
        # show a display of dude getting hit
        anim = self.game.assets.dmd_dudeShotShouldersUp
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        animLayer.composite_op = "blacksrc"
        pointsLayer = dmd.TextLayer(64, 6, self.game.assets.font_15px_az, "center", opaque=True).set_text("20,000",blink_frames=4)
        self.layer = dmd.GroupedLayer(128,32,[pointsLayer,animLayer])
        myWait = len(anim.frames) / 10.0 + 1
        # play a shot sound
        self.game.sound.play(self.game.assets.sfx_quickdrawHit)
        # delay restarting of the boss display
        self.delay("Boss Display",delay=myWait,handler=self.boss_display)
        print "TARGET " + str(target) + " HIT"
        # count the dude
        self.deathTally += 1
        # score points - dudes worth 20,000
        self.game.score(20000)
        # increase the shot value and defeat value
        self.hitValue += 10000
        self.defeatValue += 50000
        # start a timer for the target to return
        # start a timer for that target - 15 for the default time for now
        self.bossTargetTimer[target] = 15
        self.boss_target_timer(target)

    def boss_display(self):
        # cancel delay just in case
        self.cancel_delayed("Boss Display")
        self.layer = self.generate_boss_display()
        # delay a loop back to the boss display
        self.delay("Boss Display", delay=1.5, handler=self.boss_display)

    def generate_boss_display(self):
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(40, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4)
        # text line
        hits = self.hitsThisBart - self.game.show_tracking('bartHits')
        textLine = dmd.TextLayer(40,12,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(str(hits) + " HITS TO WIN")
        # hits worth line
        textLine2 = dmd.TextLayer(40,19,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("HITS WORTH:")
        # points line
        valueLine = dmd.TextLayer(40,26,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(str(ep.format_score(self.hitValue)))
        # combined layer
        return dmd.GroupedLayer(128,32,[self.wantedFrameB,scoreLine,textLine,textLine2,valueLine])

    def boss_damage_display(self,loop = True):
        # cancel the delay to be safe
        self.cancel_delayed("Boss Display")
        # make a group layer of the banner and the hit bart face
        self.bannerLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.wantedFrameA,self.bannerLayer])
        self.layer = combined
        # delay a loop back to the boss display
        if loop:
            self.delay("Boss Display", delay=1, handler=self.boss_display)

    def boss_target_timer(self,target):
        # tick one off the timer for that target
        if self.bossTargetTimer[target] > 0:
            self.bossTargetTimer[target] -= 1
        # if the timer has run out, the bad guy comes back
        if self.bossTargetTimer[target] == 0:
            self.game.bad_guys.target_up(target)
            print "RESTARING TARGET " + str(target)
        # if not, loop back again in a bit
        else:
            self.delay(name=self.targetNames[target],delay=1,handler=self.boss_target_timer,param=target)

    def boss_win(self):
        # drop all the targets
        self.game.bad_guys.drop_targets()

        # cancel the main display
        self.cancel_delayed("Boss Display")
        # fireworks
        anim = self.game.assets.dmd_fireworks
        myWait = len(anim.frames) / 10.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 6
        # ding the bell on frame 5
        animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_fireworks1)
        animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_fireworks2)
        animLayer.add_frame_listener(20,self.game.sound.play,param=self.game.assets.sfx_fireworks3)
        animLayer.composite_op = "blacksrc"
        # setup the display
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_weaveBorder.frames[0])
        textLayer1 = dmd.TextLayer(64,2,self.game.assets.font_9px_az,justify="center",opaque=False).set_text("BOSS DEFEATED")
        textLayer2 = dmd.TextLayer(64,12,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(self.defeatString))
        globalTotal = self.game.show_tracking('bartsDefeatedTotal')
        if globalTotal < self.bartsForStar:
            thetext = str(self.bartsForStar - globalTotal) + " MORE FOR BADGE"
        elif globalTotal == self.bartsForStar:
            thetext = "BADGE COLLECTED!"
            # actually collect the badge - barts defeated is 2
            self.game.badge.update(2)
        else:
            thetext = str(globalTotal) + " BROS DEFEATED!"
        textLayer3 = dmd.TextLayer(64,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(thetext)
        combined = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3,animLayer])
        self.layer = combined
        #  turn the flippers off
        self.game.enable_flippers(False)
        # clear the saloon and mine if needed
        if self.game.switches.minePopper.is_active():
            self.game.mountain.kick()
        if self.game.switches.saloonPopper.is_active():
            self.game.saloon.kick()
        # light gunfight after the animation
        self.delay(delay=myWait+1,handler=self.game.saloon.light_gunfight)
        # set the wait for all the balls to drain
        self.final_display_pause()

    def final_display_pause(self):
        # fakepinproc crutch - I hope
        if self.game.fakePinProc:
            self.game.trough.num_balls_in_play = 0
            # this just calls final display, but checks to see if there are any balls first
        # if there are balls on the field, delay the final display
        if self.game.trough.num_balls_in_play > 0:
            self.busy = True
        self.wait_until_unbusy(self.finish_up)

    def finish_up(self):
        # this is for launching a new ball to continue with
        self.game.update_lamps()
        self.game.trough.balls_to_autolaunch = 1
        self.game.trough.launch_balls(1)
        self.game.enable_flippers(True)
        # turn off the win flag
        self.bossWin = False
        self.end_boss()

    def boss_lose(self):
        # drop all the targets
        self.game.bad_guys.drop_targets()

        # play a quote
        self.game.sound.play_quote(self.game.asssets.quote_superFail)
        # housekeeping for the next bart
        # if we're at the end of the line, reset to 0
        if self.game.show_tracking('currentBart') == 3:
            self.game.set_tracking('currentBart',0)
        # if not tick up the current bart for next time
        else:
            self.game.increase_tracking('currentBart')
            # reset the hits on bart
        self.game.set_tracking('bartHits',0)
        # set bart back to open
        self.game.set_tracking('bartStatus',"OPEN")
        # finish up
        self.end_boss()

    def end_boss(self):
        # kill the running flag
        self.bossFight = False
        # set the stack level back down
        self.game.set_tracking('stackLevel',False,5)
        # cancel the display delay if any, and target timers
        self.dispatch_delayed()
        # clear the layer
        self.clear_layer()
        # turn the music back on
        self.game.base.music_on(self.game.assets.music_mainTheme)
        # update the game lamps
        self.game.update_lamps()

    ## OTHER BITS

    def move(self):
        # pulse the bart move coil
        self.game.coils.moveBart.pulse(25)

    def hat(self):
        self.game.coils.moveBartHat.pulse(30)

    def animate(self,version = 1):
        # a collection of coils and whatnot for a standard bart hit
        self.moving = True
        if version == 1:
            self.hat()
            self.game.coils.moveBart.schedule(0x10010001,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000555,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)
        # this one is for just talking - for the taunts
        if version == 2:
            self.game.coils.moveBart.schedule(0x10010001,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000555,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)
        # this one is just the hat and the shaking with no light for bionic bart
        if version == 3:
            self.hat()
            self.game.coils.moveBart.schedule(0x10010001,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)

    def not_moving(self):
        self.moving = False

    def light(self):
        # pulse the flasher light
        self.game.coils.saloonFlasher.pulse(ep.FLASHER_PULSE)

    def clear_layer(self,stayBusy = False):

        self.layer = None
        # bart ties directly to the saloon - when this layer clears it frees up the busy flag on the saloon
        if not stayBusy:
            self.game.saloon.busy = False

    def abort_display(self):
        self.cancel_delayed("Display")

    def kill_lights(self):
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()
