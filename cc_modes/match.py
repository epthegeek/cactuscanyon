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
## The match animation routine
## Crutched on myPinball's IJ match routine heavily.
##

from procgame import dmd
import random
import ep

class Match(ep.EP_Mode):
    """Cactus Canyon AttractMode"""
    def __init__(self, game, priority):
        super(Match, self).__init__(game, priority)
        self.myID = "Match"
        self.digitLayer = ep.EP_TextLayer(76,13, self.game.assets.font_13px_thin_score, "center")
        self.zeroLayer = ep.EP_TextLayer(88,13, self.game.assets.font_13px_thin_score, "center").set_text("0")
        self.p1Layer = ep.EP_TextLayer(13, 0, self.game.assets.font_7px_az, "right", opaque=False)
        self.p2Layer = ep.EP_TextLayer(13, 8, self.game.assets.font_7px_az, "right", opaque=False)
        self.p3Layer = ep.EP_TextLayer(13, 16, self.game.assets.font_7px_az, "right", opaque=False)
        self.p4Layer = ep.EP_TextLayer(13, 24, self.game.assets.font_7px_az, "right", opaque=False)
        self.playerLayers=[self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer]
        self.match_percent = self.game.user_settings['Machine (Standard)']['Match Percentage']

    # TODO maybe set this up so it shows full scores, then they scroll off to the left for more pizazz

    def tilted(self):
        pass

    def mode_started(self):
        self.playerDigits = [0,0,0,0]
        self.winners = 0
        self.zeroLayer.set_text("0",blink_frames=0,color=ep.RED)
        self.p1Layer.set_text("",blink_frames=0,color=ep.RED)
        self.p2Layer.set_text("",blink_frames=0,color=ep.RED)
        self.p3Layer.set_text("",blink_frames=0,color=ep.RED)
        self.p4Layer.set_text("",blink_frames=0,color=ep.RED)
        self.lastCall = []

    def run_match(self):
        self.game.sound.play(self.game.assets.sfx_ragtimePiano)
        possible = ["0","1","2","3","4","5","6","7","8","9"]

        # New match determination based on code from Brian Madden!
        # generate the player digits and check for replay winners
        self.generate_digits()
        # generate the probability line
        match_target = len(set(self.playerDigits)) * self.match_percent
        print "Len Set = " + str(set(self.playerDigits))
        print "Match break point " + str(match_target)
        # generate a random number for comparison
        match_value = random.randint(1,100)
        print "Match value chosen " + str(match_value)

        # check if we have a winner
        if match_value <= match_target:
            print "Match winner via value selection!"
            # here's our winning number - comes from all choices, including replay winners, so non replay winners may get shafted.
            self.selection = str(random.choice(self.playerDigits))
        # If not, the selection comes from unused digits
        else:
            # take out the player digits
            for n in self.playerDigits:
                print "Attempting to remove " + str(n)
                if n in possible:
                    print "Found it"
                    possible.remove(n)
                else:
                    print "Already removed"
            # pick from what's left
            self.selection = str(random.choice(possible))
        # if we get here

        self.digitLayer.set_text(self.selection,color=ep.RED)

        # put up the end of the scores
        # put up the bottles
        bottlesLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_match.frames[0])
        # put up the match number
        # text
        textLayer1 = ep.EP_TextLayer(30, 1, self.game.assets.font_7px_az, "center", opaque=False).set_text("MATCH",blink_frames=12,color=ep.YELLOW)
        textLayer2 = ep.EP_TextLayer(30, 9, self.game.assets.font_7px_az, "center", opaque=False).set_text("TO",blink_frames=12,color=ep.YELLOW)
        textLayer3 = ep.EP_TextLayer(30, 17, self.game.assets.font_7px_az, "center", opaque=False).set_text("WIN",blink_frames=12,color=ep.GREEN)

        combined = dmd.GroupedLayer(128,32,[bottlesLayer,self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,textLayer1,textLayer2,textLayer3])

        # this is the first display with the bottles and score endings
        self.layer = combined
        # hold for 2 seconds, then animate
        self.delay(delay=2,handler=self.run_animation)

    def generate_digits(self):
        #extract and display the last 2 score digits for each player

        for i in range(len(self.game.players)):
            score = self.game.players[i].score
            digit = str(score)[-2:-1]
            # if replays are on, they may already be a winner
            if self.game.replays and self.game.players[i].player_stats['replay_earned'] and self.game.user_settings['Machine (Standard)']['Replay Award'] == 'Last Call':
                print "Player " + str(i) + "earned last call in replay"
                self.playerLayers[i].set_text("**",color=ep.GREEN)
                self.lastCall.append(i)
                self.winners += 1
            else:
                print "PLAYER SCORE - " + str(score)
                print "MATCH DIGITS - " + str(digit)
                digitString = str(digit) + "0"
                self.playerLayers[i].set_text(digitString,color=ep.RED)

            # add digit only if it's not in the list of already picked digits
            if digit not in self.playerDigits:
                print "Adding digit " + str(digit)
                self.playerDigits[i] = str(digit)

    def run_animation(self):
        # run the animation with sound
        # load up the animation
        anim = self.game.assets.dmd_match
        # start the full on animation
        myWait = len(anim.frames) / 7.5 + 0.5
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 8
        animLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.digitLayer,self.zeroLayer,self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,animLayer])
        # fire it up
        self.layer = combined
        self.fire("LEFT")
        self.delay(delay=0.125,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=0.5,handler=self.fire,param="RIGHT")
        self.delay(delay=0.625,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1,handler=self.fire,param="LEFT")
        self.delay(delay=1.125,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.125,handler=self.fire,param="RIGHT")
        self.delay(delay=1.250,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.625,handler=self.fire,param="LEFT")
        self.delay(delay=1.75,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.75,handler=self.fire,param="RIGHT")
        self.delay(delay=1.875,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)


        # after the animation ends, see if anybody won and run that action
        self.delay(delay = myWait,handler=self.award_match)

    def award_match(self):
        # check the scores to see if anybody won
        for i in range(len(self.game.players)):
            if str(self.playerDigits[i]) == self.selection:
                # set the text on that layer to blink
                self.playerLayers[i].set_text(str(self.playerDigits[i]) + "0",blink_frames=8,color=ep.GREEN)
                # and tick the winner count to true
                self.winners += 1
                # store a list of winning players
                print ("Player " + str(i) + " gets last call")
                # check to make sure they're not in last call already
                if i not in self.lastCall:
                    self.lastCall.append(i)

        # if we had any winners there's stuff to do
        if self.winners > 0:
            self.digitLayer.set_text(self.selection,blink_frames=8,color=ep.GREEN)
            self.zeroLayer.set_text("0",blink_frames=8,color=ep.GREEN)
            bottlesLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_match.frames[20])
            bottlesLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[self.digitLayer,self.zeroLayer,self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,bottlesLayer])
            self.layer = combined
            self.game.interrupter.knock(self.winners)
            self.game.sound.play(self.game.assets.sfx_matchRiff)

        # Then delay for 2 seconds and shut 'er down
        self.delay(delay=2,handler=self.finish_up)

    def fire(self,side):
        self.game.sound.play(self.game.assets.sfx_explosion11)
        if side == "LEFT":
            self.game.coils.leftGunFlasher.pulse(30)
        if side == "RIGHT":
            self.game.coils.rightGunFlasher.pulse(30)

    def finish_up(self):
        # if somebody won - we're going to run last call, with the list of players
        if self.winners > 0:
            self.game.modes.add(self.game.last_call)
            self.game.last_call.set_players(self.lastCall)
            self.game.last_call.intro()
        else:
            # run the high score routine after the match
            self.game.run_highscore()
        # and remove thyself.
        self.unload()