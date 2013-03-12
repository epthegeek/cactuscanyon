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
# for controlling the status of the badge

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
        marshallRequirement = self.game.user_settings['Gameplay (Feature)']['Marshall Req for Bionic']
        self.marshallValue = self.game.user_settings['Gameplay (Feature)']['Marshall Multiball']

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

    def reset(self):
        # reset the badge progress
        # set all 5 points to false
        print "RESETTING BADGE STATUS"
        for i in range(0,5,1):
            self.game.set_tracking('starStatus',False,i)
        print self.game.show_tracking('starStatus')
        # reset the combos
        self.game.set_tracking('combos',0)
        # reset the barts defeated
        self.game.set_tracking('bartsDefeated',0)
        # reset the motherlodes count
        self.game.set_tracking('motherlodesCollected',0)
        self.game.lamp_control.badge()

    def update(self,point):
        # update for the new award
        self.game.set_tracking('starStatus',True,point)
        print "BADGE STATUS: "
        print self.game.show_tracking('starStatus')
        # log some audits
        if point == 1:
        # log the hit in audits
            self.game.game_data['Feature']['Combos Complete'] += 1
        elif point == 2:
            self.game.game_data['Feature']['Bart Bros Complete'] += 1
        # check if bionic is ready
        self.check_bionic()
        # update the badge lamps no matter what
        self.game.lamp_control.badge()

    def check_bionic(self):
        print "Checking if bionic bart is ready"
        # if all the lights are on, it's bionic bart time
        if False not in self.game.show_tracking('starStatus'):
            print "Don't see a False - setting BB to ready"
            # is marshall rank required?
            if self.marshallRequired:
                # if it is, are we there yet?
                if self.game.show_tracking('rank') < 4:
                    # if not, bail
                    return
            # if we didn't bail, then it's safe to ready bionic bart
            self.game.set_tracking('bionicStatus',"READY")
            # if bart goes ready, update the saloon lights to flash the arrow
            self.lamp_update()
        else:
            print "Bart is not ready yet - Badge incomplete"

    def light_high_noon(self):
        self.game.set_tracking('highNoonStatus', "READY")
        # call the full lamp update
        self.lamp_update()

    def increase_rank(self,gunfight=False):
        # for updating the rank lights
        rank = self.game.show_tracking('rank')
        ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHALL"]
        # if we're at less than 4, increase
        if rank < 4:
            newRank = self.game.increase_tracking('rank')
            rankTitle = ranks[newRank]
        # if we're not, set this arbitrary number
        else:
            newRank = 999
            rankTitle = ranks[4]
        # play the appropriate rank quote
        if gunfight:
            # if we didn't increase rank, just use the quickdraw win quotes
            if newRank == 999:
                quote = self.game.assets.quote_quickdrawWin
            # if we did increase rank, the sound matches the rank
            else:
                type = random.choice([self.rankSounds,self.winQuotes])
                quote = type[newRank]
        # anything that isn't a gunfight uses the rank specific congrats all the time
        else:
            quote = self.rankSounds[newRank]

        duration = self.game.base.priority_quote(quote)
        # if we're now at rank 4, then start marshall multiball - if it's turned on
        if newRank == 4 and self.marshallValue == 'Enabled':
                self.delay(delay=duration+0.2,handler=self.game.base.kickoff_marshall)
        # update the rank lamps
        self.game.lamp_control.rank_level()
        # return the new rank and duration
        return rankTitle,duration
