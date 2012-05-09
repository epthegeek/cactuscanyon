##
## This mode controls the saloon
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes
import ep

class Saloon(game.Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(Saloon, self).__init__(game, priority)
        # setup the difficulty
        difficulty = self.game.user_settings['Gameplay (Feature)']['Bart Brothers Difficulty']
        # Easy version
        print "Difficulty is set to - " + difficulty
        if difficulty == 'Easy':
            self.hitsToDefeatBart = [1,2,3,4,5,6]
        # Hard version
        else:
            self.hitsToDefeatBart = [2,4,6,8,8,8]


    def sw_saloonPopper_closed_for_200ms(self,sw):
        if self.game.show_tracking('isBountyLit'):
            self.collect_bounty()
        print "PULSE THE KICKER FOR THE SALOON"

    def sw_saloonBart_active(self,sw):
        # a direct smack to el barto
        self.hit_bart()

    def sw_saloonGate_active(self,sw):
        # play the sound.
        # add some points
        self.game.score(2530)
        # exciting!

    ###
    ###  ____                    _
    ### | __ )  ___  _   _ _ __ | |_ _   _
    ### |  _ \ / _ \| | | | '_ \| __| | | |
    ### | |_) | (_) | |_| | | | | |_| |_| |
    ### |____/ \___/ \__,_|_| |_|\__|\__, |
    ###                              |___/
    ###

    def light_bounty(self):
        # set the tracking
        self.game.set_tracking('isBountyLit', True)
        # show something on the screen
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'stars-border.dmd').frames[0])
        topText = dmd.TextLayer(128/2, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("COLLECT BOUNTY",blink_frames=10)
        bottomText = dmd.TextLayer(128/2, 16, self.game.assets.font_9px_az, "center", opaque=False).set_text("IS LIT",blink_frames=10)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,topText,bottomText])
        # play a voice clip about the bounty being ready
        self.game.sound.play_voice(self.game.assets.quote_bountyLit)
        # lights and whatnot
        self.delay(delay=1.6,handler=self.clear_layer)

    def collect_bounty(self):
        # TODO award the prize
        # turn off the tracking
        self.game.set_tracking('isBountyLit', False)
        # select an award
        # give the award

    ###
    ###  ____             _     ____            _   _
    ### | __ )  __ _ _ __| |_  | __ ) _ __ ___ | |_| |__   ___ _ __ ___
    ### |  _ \ / _` | '__| __| |  _ \| '__/ _ \| __| '_ \ / _ \ '__/ __|
    ### | |_) | (_| | |  | |_  | |_) | | | (_) | |_| | | |  __/ |  \__\
    ### |____/ \__,_|_|   \__| |____/|_|  \___/ \__|_| |_|\___|_|  |___/
    ###

    def hit_bart(self):
        # lookup the status
        status = self.game.show_tracking('bartStatus')
        # if no bart is currently running, a new challenger appears
        if status == "OPEN":
            self.game.set_tracking('bartStatus',"RUNNING")
            self.activate_bart()
        # else, register the hit
        elif status == "RUNNING":
            self.damage_bart()
        # if there is one active and it's the last hit, defeat
        elif status == "LAST":
            self.defeat_bart()
        # not running? do this
        else:
            # he's dead waiting for a gun fight - TODO have to research what happens
            pass

    def activate_bart(self):
        # set up all the strings & quotes
        self.setup_bart()
        # show the 'challenges you' display
        # play a quote?
        self.game.sound.play_voice(self.tauntQuote)
        # if there's only 1 hit to defeat this bart, set the status to last
        if self.hitsThisBart == 1:
            self.game.set_tracking('bartStatus',"LAST")

    def setup_bart(self):
        # our cast of characters
        names = ('Big','Bandelero','Bubba')
        hits = (self.game.assets.quote_hitBigBart, self.game.assets.quote_hitBandeleroBart,self.game.assets.quote_hitBubbaBart)
        taunts = (self.game.assets.quote_tauntBigBart, self.game.assets.quote_tauntBandeleroBart,self.game.assets.quote_tauntBubbaBart)
        defeats = (self.game.assets.quote_defeatBigBart, self.game.assets.quote_defeatBandeleroBart,self.game.assets.quote_defeatBubbaBart)
        # look up which one is current
        index = self.game.show_tracking('currentBart')
        # setting up all the bits like name for text display
        self.brother = names[index].upper()
        # wanted poster
        self.wantedFrameA = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'wanted-'+ brother +'-a.dmd').frames[0])
        self.wantedFrameB = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'wanted-'+ brother +'-b.dmd').frames[0])
        # hit quotes
        self.hitQuote = hits[index]
        # taunt quotes
        self.tauntQuote = taunts[index]
        # death quote
        self.defeatQuote = defeats[index]
        # setup the points value?
        # TODO points value
        # setup the hits needed to defeat this bart
        self.hitsThisBart = self.hitsToDefeatBart[index]

    def damage_bart(self):
        # play a quote appropriate to the current bart
        self.game.sound.play_voice(self.hitQuote)
        # flash the light and move the dude
        # display the info
        # register the hit
        # increase the hits on bart - and store the new amount
        currentHits = self.game.increase_tracking('bartHits')
        # check to see if we're on the last hit now - meaning, our hit total is one less than defeat
        if currentHits + 1 >= self.hitsThisBart:
            # if it is, set the status to last
            self.game.set_tracking('bartStatus',"LAST")

    def defeat_bart(self):
        # play a defeated quote
        self.game.sound.play_voice(self.defeatQuote)
        # set the status to dead - gunfight has to set it back to open
        self.game.set_tracking('bartStatus',"DEAD")
        # if we're at the end of the line, reset to 0
        if self.game.show_tracking('currentBart') == 2:
            self.game.set_tracking('currentBart',0)
        # if not tick up the current bart for next time
        else:
            self.game.increase_tracking('currentBart')
        # score some points
        # reset the hits on bart
        self.game.set_tracking('bartHits',0)
        # light gunfight?

    def clear_layer(self):
        self.layer = None