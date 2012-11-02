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
# for controlling the status of the badge

from procgame import *
import cc_modes
import ep
import random

class Badge(ep.EP_Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Badge, self).__init__(game,priority)
        self.starLamps = [self.game.lamps.starMotherlode,
                          self.game.lamps.starCombo,
                          self.game.lamps.starBartBrothers,
                          self.game.lamps.starShowdown,
                          self.game.lamps.starStampede]
        # rank - set up the bulb list
        self.rankLamps = [self.game.lamps.rankStranger,
                          self.game.lamps.rankPartner,
                          self.game.lamps.rankDeputy,
                          self.game.lamps.rankSheriff,
                          self.game.lamps.rankMarshall]
        marshallRequirement = self.game.user_settings['Gameplay (Feature)']['Marshall Required for Bionic']
        if marshallRequirement == "Yes":
            self.marshallRequired = True
        else:
            self.marshallRequired = False
        self.rankSounds = [self.game.assets.quote_rankUpPartner,
                           self.game.assets.quote_rankUpPartner,
                           self.game.assets.quote_rankUpDeputy,
                           self.game.assets.quote_rankUpSheriff,
                           self.game.assets.quote_rankUpMarshall]
        self.winQuotes = [self.game.assets.quote_gunfightWinPartner,
                          self.game.assets.quote_gunfightWinPartner,
                          self.game.assets.quote_gunfightWinDeputy,
                          self.game.assets.quote_gunfightWinSheriff,
                          self.game.assets.quote_gunfightWinMarshall]

    def update_lamps(self):
        # reset first
        self.disable_lamps()
        status = self.game.show_tracking('lampStatus')
        ## if status is off, we bail here
        if status == "OFF" or self.game.show_tracking('cvaStatus') == "RUNNING":
            return

        # star lamps for high noon
        for lamp in range(0,5,1):
            if self.game.show_tracking('starStatus',lamp) == True:
                #print "STAR LAMP " + str(lamp) + "IS" + str(self.game.show_tracking('starStatus',lamp))
                self.starLamps[lamp].enable()
        # bionic bart ready chases the lights
        status = self.game.show_tracking('bionicStatus')
        if status == "READY" or status == "RUNNING":
            self.game.lamps.starMotherlode.schedule(0xFFE0FFE0)
            self.game.lamps.starCombo.schedule(0xFF07FF07)
            self.game.lamps.starBartBrothers.schedule(0xF83FF83F)
            self.game.lamps.starShowdown.schedule(0x81FF81FF)
            self.game.lamps.starStampede.schedule(0x0FFE0FFE)
        # center of high noon
        if self.game.show_tracking('highNoonStatus') == "READY":
            self.game.lamps.starHighNoon.schedule(0x00FF00FF)
            for lamp in range(0,5,1):
                if self.game.show_tracking('starStatus',lamp) == True:
                    #print "STAR LAMP " + str(lamp) + "IS" + str(self.game.show_tracking('starStatus',lamp))
                    self.starLamps[lamp].schedule(0xFF00FF00)
        # the rank lights
        rank = self.game.show_tracking('rank')
        # loop through 0 through current rank and turn the lamps on
        for lamp in range(0,(rank +1),1):
            self.rankLamps[lamp].enable()


    def disable_lamps(self):
        for lamp in self.starLamps:
            lamp.disable()
        for lamp in self.rankLamps:
            lamp.disable()
        self.game.lamps.starHighNoon.disable()

    def reset(self):
        # reset the badge progress
        # set all 5 points to false
        print "RESETTING BADGE STATUS"
        for i in range(0,5,1):
            self.game.set_tracking('starStatus',"False",i)
        # reset the combos
        self.game.set_tracking('combos',0)
        # reset the barts defeated
        self.game.set_tracking('bartsDefeated',0)
        # reset the motherlodes count
        self.game.set_tracking('motherlodesCollected',0)
        self.update_lamps()

    def update(self,point):
        # update for the new award
        self.game.set_tracking('starStatus',True,point)
        # check if bionic is ready
        self.check_bionic()
        # update the lamps no matter what
        self.update_lamps()

    def check_bionic(self):
        print "Checking if bionic bart is ready"
        # if all the lights are on, it's bionic bart tiome
        if False not in self.game.show_tracking('starStatus'):
            # is marshall rank required?
            if marshallRequired:
                # if it is, are we there yet?
                if rank < 4:
                    # if not, bail
                    return
            # if we didn't bail, then it's safe to ready bionic bart
            self.game.set_tracking('bionicStatus',"READY")
            # if bart goes ready, update the saloon lights to flash the arrow
            self.game.saloon.update_lamps()

    def light_high_noon(self):
        self.game.set_tracking('highNoonStatus', "READY")
        # update the mine lamps to flash the lock arrow
        self.game.mine.update_lamps()
        # then update local lamps
        self.update_lamps()

    def increase_rank(self,gunfight=False):
        # for updating the rank lights
        rank = self.game.show_tracking('rank')
        # if we're at less than 4, increase
        if rank < 4:
            newRank = self.game.increase_tracking('rank')
        else:
            newRank = 999
        ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHAL"]
        rankTitle = ranks[newRank]
        # play the appropriate rank quote
        if gunfight:
            # if we didn't increase rank, just use the quickdraw win quotes
            if newRank == 999:
                quote = self.game.assets.quote_quickdrawWin
            else:
                type = random.choice([self.rankSounds,self.winQuotes])
                quote = type[newRank]
        # anything tha tisn't a gunfight uses the rank specific congrats all the time
        else:
            quote = self.rankSounds[newRank]

        duration = self.game.base.priority_quote(quote)
        # if we're now at rank 4, then start marshall multiball
        if newRank == 4:
            self.delay(delay=duration+0.2,handler=self.game.base.kickoff_marshall)
        # update the lamps
        self.update_lamps()
        # return the new rank and duration
        return rankTitle,duration
