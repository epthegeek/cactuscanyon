
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

class Bart(game.Mode):
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
        self.banners = ['bam','biff','ouch','pow','wham','zoink']
        # a flag for when bart is in motion
        self.moving = False

    def mode_started(self):
        # activate the first bart if we're on the first ball
        if self.game.ball == 1:
            self.game.set_tracking('bartStatus',"RUNNING")
            self.setup()

    def hit(self):
        # pick a random banner to use
        banner = random.choice(self.banners)
        # set up the banner layer
        self.bannerLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+banner+'-banner.dmd').frames[0])

        # lookup the status
        status = self.game.show_tracking('bartStatus')
        print "BART STATUS: " + status
        print "CURRENT BART: " + str(self.game.show_tracking('currentBart'))
        # if no bart is currently running, a new challenger appears
        bionic = self.game.show_tracking('bionicStatus')
        if bionic == "READY" or bionic == "RUNNING":
            self.game.saloon.busy = False
        if status == "OPEN":
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
            # he's dead waiting for a gun fight
            # no points - play a sound?
            self.game.saloon.busy = False

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
        self.game.sound.play(self.introQuote)
        # show the transition
        transition = ep.EP_Transition(self,self.game.score_display.layer,textLayer,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)

        # if there's only 1 hit to defeat this bart, set the status to last
        if self.hitsThisBart == 1:
            self.game.set_tracking('bartStatus',"LAST")
        self.delay(delay=1.5,handler=self.clear_layer)

    def setup(self):
        # our cast of characters
        names = ('big','bandelero','bubba')
        hits = (self.game.assets.quote_hitBigBart, self.game.assets.quote_hitBandeleroBart,self.game.assets.quote_hitBubbaBart)
        taunts = (self.game.assets.quote_tauntBigBart, self.game.assets.quote_tauntBandeleroBart,self.game.assets.quote_tauntBubbaBart)
        defeats = (self.game.assets.quote_defeatBigBart, self.game.assets.quote_defeatBandeleroBart,self.game.assets.quote_defeatBubbaBart)
        intros = (self.game.assets.quote_introBigBart, self.game.assets.quote_introBandeleroBart,self.game.assets.quote_introBubbaBart)
        # look up which one is current
        index = self.game.show_tracking('currentBart')
        # setting up all the bits like name for text display
        self.brother = names[index].upper()
        # wanted poster
        self.wantedFrameA = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'wanted-'+ self.brother +'-A.dmd').frames[0])
        self.wantedFrameA.composite_op = "blacksrc"
        self.wantedFrameB = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'wanted-'+ self.brother +'-B.dmd').frames[0])
        # hit quotes
        self.hitQuote = hits[index]
        # taunt quotes
        self.tauntQuote = taunts[index]
        # death quote
        self.defeatQuote = defeats[index]
        # intro quote
        self.introQuote = intros[index]
        defeated = self.game.show_tracking('bartsDefeated')
        # setup the points value? 120,000 + 5,000 times the number of defeated barts
        self.hitValue = 120000 + (5000 * defeated)
        self.hitString = locale.format("%d", self.hitValue, True) # Add commas
        # setup the defeat value 150,000 for first + 50,000 times the number of defeated barts
        self.defeatValue = 150000 + (50000 * defeated)
        self.defeatString = locale.format("%d", self.defeatValue, True) # Add commas
        # setup the hits needed to defeat this bart
        self.hitsThisBart = self.hitsToDefeatBart[index]
        # set up the name line for the cards
        print self.brother + " IS THE BROTHER"
        if self.brother != "BANDELERO":
            self.nameLine = self.brother.upper() + " BART"
        else:
            self.nameLine = self.brother


    def damage(self,saloonHit=False):
        print "DAMAGE BART"
        # play a quote appropriate to the current bart
        self.game.sound.play_voice(self.hitQuote)
        # move bart
        self.animate(1)

        # score the points
        self.game.score(self.hitValue)
        # flash the light and move the dude
        # a flourish lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, repeat=False,callback=self.game.update_lamps)
        # display the info
        # register the hit
        # increase the hits on bart - and store the new amount
        currentHits = self.game.increase_tracking('bartHits')
        # check to see if we're on the last hit now - meaning, our hit total is one less than defeat
        # math the remaining hits
        print "HITS FOR THIS BART: " + str(self.hitsThisBart)
        print "CURRENT HITS: " + str(currentHits)
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
        self.display_damage_one()

    def defeat(self):
        print "DEFEATING BART"
        # add to the defeated barts
        currentTotal = self.game.increase_tracking('bartsDefeated')
        # tick up the global count as well
        self.game.increase_tracking('bartsDefeatedTotal')
        # move bart
        self.animate(1)

        # play a defeated quote
        myWait = self.game.sound.play_voice(self.defeatQuote)
        # set the status to dead - gunfight has to set it back to open
        self.game.set_tracking('bartStatus',"DEAD")
        # if we're at the end of the line, reset to 0
        if self.game.show_tracking('currentBart') == 2:
            self.game.set_tracking('currentBart',0)
        # if not tick up the current bart for next time
        else:
            self.game.increase_tracking('currentBart')
            # score some points
        self.game.score(self.defeatValue)
        # reset the hits on bart
        self.game.set_tracking('bartHits',0)
        # play a fancy lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_sparkle, False, self.game.update_lamps)
        # setup the display
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'weave-border.dmd').frames[0])
        textLayer1 = dmd.TextLayer(64,2,self.game.assets.font_9px_az,justify="center",opaque=False).set_text("BART DEFEATED")
        textLayer2 = dmd.TextLayer(64,12,self.game.assets.font_9px_az,justify="center",opaque=False).set_text(str(self.defeatString))
        if currentTotal < self.bartsForStar:
            thetext = str(self.bartsForStar - currentTotal) + " MORE FOR BADGE"
        elif currentTotal == self.bartsForStar:
            thetext = "BADGE COLLECTED!"
            # actually collect the badge - barts defeated is 2
            self.game.badge.check_bionic_bart(2)
        else:
            thetext = str(currentTotal) + " DEFEATED!"
        textLayer3 = dmd.TextLayer(64,24,self.game.assets.font_6px_az,justify="center",opaque=False).set_text(thetext)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3])

        # light gunfight?
        self.delay(delay=myWait,handler=self.game.saloon.light_gunfight)

    def display_damage_one(self):
        print "MADE IT TO DAMAGE ONE"
        # set up the top layer
        layerOne = dmd.GroupedLayer(128,32,[self.bannerLayer,self.wantedFrameA])
        # activate it
        self.layer = layerOne
        self.delay(delay=0.2,handler=self.display_damage_two,param=layerOne)

    def display_damage_two(self,layerOne):
        # set up the second layer
        layerTwo = dmd.GroupedLayer(128,32,[self.wantedFrameB,self.textLayer])
        transition = ep.EP_Transition(self,layerOne,layerTwo,ep.EP_Transition.TYPE_PUSH,ep.EP_Transition.PARAM_NORTH)
        self.delay(delay = 1.5,handler=self.clear_layer)

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
            self.game.coils.moveBart.schedule(0x0000000A,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000555,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)
        # this one is for just talking - for the taunts
        if version == 2:
            self.game.coils.moveBart.schedule(0x0000000A,cycle_seconds=1)
            self.game.coils.saloonFlasher.schedule(0x00000555,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)
        # this one is just the hat and the shaking with no light for bionic bart
        if version == 3:
            self.hat()
            self.game.coils.moveBart.schedule(0x0000000A,cycle_seconds=1)
            self.delay(delay=0.15,handler=self.not_moving)

    def not_moving(self):
        self.moving = False

    def light(self):
        # pulse the flasher light
        self.game.coils.saloonFlasher.pulse(ep.FLASHER_PULSE)

    def clear_layer(self):
        self.layer = None
        # bart ties directly to the saloon - when this layer clears it frees up the busy flag on the saloon
        self.game.saloon.busy = False
