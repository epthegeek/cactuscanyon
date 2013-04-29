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
## A P-ROC Project by Eric Priepke, Copyright 2012
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

from procgame import dmd
import ep
import random
import locale

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

class Bart(ep.EP_Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Bart, self).__init__(game,priority)
        self.myID = "Bart"
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
        self.activeBossPosse = []


    def mode_started(self):
        # activate the first bart if we're on the first ball
        if self.game.ball == 1:
            self.game.set_tracking('bartStatus',"RUNNING")
            self.setup()

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0 and self.bossFight:
            self.drop_posse()

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
        textLayer1 = ep.EP_TextLayer(42,2,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer1.set_text(self.nameLine,color=ep.BROWN)
        textLayer2 = ep.EP_TextLayer(42,16,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer2.set_text("CHALLENGES",color=ep.RED)
        textLayer3 = ep.EP_TextLayer(42,24,self.game.assets.font_7px_bold_az,justify="center",opaque=False)
        textLayer3.set_text("YOU",color=ep.RED)

        textLayer = dmd.GroupedLayer(128,32,[self.wantedFrameB,textLayer1,textLayer2,textLayer3])

        # play the intro
        duration = self.game.base.play_quote(self.introQuote,squelch=True)

        # show the transition
        transition = ep.EP_Transition(self,self.game.score_display.layer,textLayer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        # divert here if we're on boss bart
        if self.brother == 'BOSS':
            self.bossFight = True
            # bump up the points
            self.hitValue *= 2
            self.defeatValue *= 2
            self.deathTally = 0
            # activate the drop targets
            self.delay(delay=duration,handler=self.game.bad_guys.setup_targets)
            # set them all to true
            self.activeBossPosse = [0,1,2,3]
        else:

            # if there's only 1 hit to defeat this bart, set the status to last
            if self.hitsThisBart == 1:
                self.game.set_tracking('bartStatus',"LAST")
        self.delay("Display",delay=duration,handler=self.clear_layer)
        self.delay(delay=duration,handler=self.game.saloon.unbusy)


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
        # log the hit in audits
        self.game.game_data['Feature']['Bart Hits'] += 1
        # play a quote appropriate to the current bart
        self.game.base.priority_quote(self.hitQuote,squelch=True)

        # move bart
        self.animate(1)

        # score the points
        self.game.score(self.hitValue)
        # add some bonus
        self.game.add_bonus(25000)
        # flash the light and move the dude
        # a flourish lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.lamp_update)
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
        if self.brother == "BOSS":
            offset = 40
        else:
            offset = 42
        textLayer1 = ep.EP_TextLayer(offset,1,self.game.assets.font_7px_bold_az,justify="center",opaque=False).set_text(self.nameLine,color=ep.BROWN)
        textLayer2 = ep.EP_TextLayer(offset,9,self.game.assets.font_7px_bold_az,justify="center",opaque=False).set_text(str(self.hitString))
        textLayer3 = ep.EP_TextLayer(offset,17,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(theText,color=ep.YELLOW)
        textLayer4 = ep.EP_TextLayer(offset,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text("TO COLLECT",color=ep.YELLOW)
        self.textLayer = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,textLayer3,textLayer4])
        self.textLayer.composite_op = "blacksrc"
        # play a fancy lamp show
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, False, self.lamp_update)
        # if we're boss fighting, go to that display
        if self.brother == "BOSS":
            self.boss_damage_display()
        else:
            self.display_damage_one()

    def defeat(self):
        print "DEFEATING BART"
        # log the hit in audits
        self.game.game_data['Feature']['Barts Defeated'] += 1
        # count barts to the reset
        total = self.game.increase_tracking('bartsDefeated')
        # tick up the global count as well
        globalTotal = self.game.increase_tracking('bartsDefeatedTotal')
        # this bart total counts just regualr barts
        if self.brother != "BOSS":
            self.game.increase_tracking('regularBartsDefeated')
        # move bart
        self.animate(1)

        # play a defeated quote
        myWait = self.game.base.play_quote(self.defeatQuote,squelch=True)

        # set the status to dead - gunfight has to set it back to open
        self.game.set_tracking('bartStatus',"DEAD")
        # if we're one away from the badge, switch to boss
        if self.bartsForStar - total == 1:
            # by jumping ahead to the 4th spot
            self.game.set_tracking('currentBart',3)
        # if we just did boss bart, figure out where we were in the rotation
        elif self.game.show_tracking('currentBart') == 3:
            nextBart = self.game.show_tracking('regularBartsDefeated') % 3
            self.game.set_tracking('currentBart',nextBart)
        # if we're at the end of the line, reset to 0
        elif self.game.show_tracking('currentBart') == 2:
            self.game.set_tracking('currentBart',0)
        # if not tick up the current bart for next time
        else:
            self.game.increase_tracking('currentBart')
            # score some points
        self.game.score(self.defeatValue)
        # add some bonus
        self.game.add_bonus(150000)
        # reset the hits on bart
        self.game.set_tracking('bartHits',0)
        # play a fancy lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, False, self.lamp_update)
        # kill the bossfight flag just to cover if it's on
        if self.bossFight == True:
            self.bossFight = False
            # drop all the targets that are still up
            self.drop_posse()
        # setup the display
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_weaveBorder.frames[0])
        textLayer1 = ep.EP_TextLayer(64,1,self.game.assets.font_9px_az,justify="center",opaque=False).set_text("BART DEFEATED",color=ep.BROWN)
        textLayer2 = ep.EP_TextLayer(64,12,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(self.defeatString),color=ep.GREEN)
        if total < self.bartsForStar:
            theText = str(self.bartsForStar - total) + " MORE FOR BADGE"
        elif total == self.bartsForStar:
            theText = "BADGE COLLECTED!"
            # actually collect the badge - barts defeated is 2
            self.game.badge.update(2)
        else:
            theText = str(globalTotal) + " DEFEATED!"
        textLayer3 = ep.EP_TextLayer(64,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(theText, color=ep.DARK_RED)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3])
         # light gunfight?
        self.delay(delay=myWait,handler=self.game.saloon.light_gunfight)
        # clear the layer
        self.delay("Display",delay=myWait,handler=self.clear_layer)

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
        self.delay(delay=1.5,handler=self.game.saloon.unbusy)

    ## BOSS FIGHT STUFF

    def boss_target_hit(self,target):
        # remove this dude from the posse
        self.activeBossPosse.remove(target)
        self.game.base.play_quote(self.game.assets.quote_targetBossBart)
        self.animate(2)
        # cancel the main display
        self.cancel_delayed("Boss Display")
        # show a display of dude getting hit
        anim = self.game.assets.dmd_dudeShotShouldersUp
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        animLayer.composite_op = "blacksrc"
        textString = str(ep.format_score(25000))
        pointsLayer = dmd.TextLayer(64, 1, self.game.assets.font_15px_az, "center", opaque=True).set_text(textString,blink_frames=4)
        textLine = dmd.TextLayer(64,18,self.game.assets.font_5px_AZ, "center",opaque = False).set_text("BOSS SHOTS")
        textLine2 = dmd.TextLayer(64,24,self.game.assets.font_5px_AZ,"center",opaque = False).set_text("VALUE INCREASED")
        self.layer = dmd.GroupedLayer(128,32,[pointsLayer,textLine,textLine2,animLayer])
        myWait = len(anim.frames) / 10.0 + 1
        # play a shot sound
        self.game.sound.play(self.game.assets.sfx_quickdrawHit)
        # flash the guns
        self.game.base.guns_flash(1)
        # delay clearing display
        self.delay("Display",delay=myWait,handler=self.clear_layer)
        # count the dude
        self.deathTally += 1
        # if death tally makes it to 4, kill the bossfight flag
        if self.deathTally >= 4:
            self.bossFight = False
        # score points - dudes worth 20,000
        self.game.score(25000)
        # increase the shot value and defeat value
        self.hitValue += 50000
        self.defeatValue += 100000

    def boss_damage_display(self,loop = True):
        # cancel the delay to be safe
        self.cancel_delayed("Boss Display")
        # make a group layer of the banner and the hit bart face
        self.bannerLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.wantedFrameA,self.bannerLayer])
        self.layer = combined
        self.delay("Display",delay=0.7,handler=self.boss_display_two)

    def boss_display_two(self):
        self.layer = dmd.GroupedLayer(128,32,[self.wantedFrameB,self.textLayer])
        # delay a loop back to the boss display
        self.delay("Display",delay = 2,handler=self.clear_layer)
        self.delay(delay=2,handler=self.game.saloon.unbusy)

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
            self.game.coils.moveBart.schedule(0x00001001,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000333,cycle_seconds=1)
            self.delay(delay=0.75,handler=self.not_moving)
        # this one is for just talking - for the taunts
        if version == 2:
            self.game.coils.moveBart.schedule(0x00001001,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000555,cycle_seconds=1)
            self.delay(delay=0.75,handler=self.not_moving)
        # this one is just the hat and the shaking with no light for bionic bart
        if version == 3:
            self.hat()
            self.game.coils.moveBart.schedule(0x00001001,cycle_seconds=1)
            self.delay(delay=0.75,handler=self.not_moving)

    def not_moving(self):
        self.moving = False

    def light(self):
        # pulse the flasher light
        self.game.coils.saloonFlasher.pulse(ep.FLASHER_PULSE)

    def clear_layer(self):
        self.layer = None

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")


    def drop_posse(self):
        for dude in self.activeBossPosse:
            self.game.bad_guys.target_down(dude)
        self.activeBossPosse = []
        # kill the bossfight so gun modes are available again
        self.bossFight = False