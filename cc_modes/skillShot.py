##
## The Skill Shot mode for working the lasso ramp awards
##

from procgame import *
import cc_modes
import random


class SkillShot(game.Mode):
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

    def mode_started(self):
        # call the welcome quote - and start the theme song after on the first ball
        self.game.sound.play(self.game.assets.music_drumRiff)
        if self.game.ball == 1:
            # play a random voice call from a pre-set collection
            self.delay(delay=0.3,handler=self.game.play_remote_sound,param=self.game.assets.quote_welcomes)
        # fire up the shooter lane groove - maybe should tie this to a ball on the shooter lane. meh.
        self.delay(delay=0.2,handler=self.music_on)

        # set up a blank list for prizes
        prizes = []
        # completed items are not added to the random list
        # and maybe putting specific weight on certain items to make them more rare
        # but for now, randomly select 5 items to build the prize list

        # right ramp complete (bank)
        if self.game.show_tracking('rightRampStage') < 4:
            prizes.append("C")

        # light lock (padlock)
        # if multiball is ready, then don't include light lock
        if self.game.show_tracking('mineStatus') != "READY":
            prizes.append("D")

        # light bounty? (money bag) don't add if bounty is already lit
        if not self.game.show_tracking('isBountyLit'):
            prizes.append("E")

        # left ramp complete (boat)
        if self.game.show_tracking('leftRampStage') < 4:
            prizes.append("F")

        # right loop complete (gun)
        if self.game.show_tracking('rightLoopStage') < 4:
            prizes.append("G")

        # light quick draw (gun w/ quick draw)
        if self.game.show_tracking('quickDrawStatus',key=1) != "READY":
            prizes.append("H")

        # left loop complete (horse)
        if self.game.show_tracking('leftLoopStage') < 4:
            prizes.append("I")

        # extra ball (ball) don't include on ball 1
        if self.game.ball != 1:
            prizes.append("J")

        # increae rank (star) don't include if already at max rank
        if self.game.show_tracking('rank') < 5:
            prizes.append("K")

        # bonus X don't include if bonus already 6x or more
        if self.game.show_tracking('bonusX') < 6:
            prizes.append("L")

        # center ramp complete (train)
        if self.game.show_tracking('centerRampStage') < 4:
            prizes.append("M")

        # 1 million points (1M) is always available
        prizes.append("N")

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

        self.update_layer()

    def update_layer(self):
        # set up the text layer of prizes
        prizeList = dmd.TextLayer(self.x, 1, self.game.assets.font_skillshot, "right", opaque=True).set_text(self.selectedPrizes)
        self.layer = dmd.GroupedLayer(128, 32, [prizeList,self.mask, self.lasso])


    # if the ramp switch gets hit - shift the prizes over
    # take the last prize off the string and stick it back on the front
    def sw_skillBowl_active(self, sw):
        ##
        self.game.score(7250)
        ## TODO add bonus points to all kinds of junk
        self.game.add_bonus(130)
        # slide the prize list over
        self.game.sound.play(self.game.assets.sfx_skillShotWoosh)
        self.shift_right()
        # have to figure out some way to make this animate smoothly or something - this works for now
        # catches the first five in one variable and then the next in another and drops the far right
        # then builds a new target string with the new far right symbol at both ends, for shifting
        prizeTemp1 = self.selectedPrizes[0:4]
        prizeTemp2 = self.selectedPrizes[4:5]
        self.selectedPrizes = prizeTemp2 + prizeTemp1 + prizeTemp2


    # if the ramp bottom switch gets hit - award the prize and unload the mode
    def sw_rightRampBottom_active(self, sw):
        # kill the music
        self.game.sound.stop_music()
        # play the sound
        ## TODO might need to move this to specific awards
        self.game.sound.play(self.game.assets.sfx_flourish7)

        # award the prize - TODO these will change to real awards later
        if self.selectedPrizes[5:] == "C":
            self.game.score(10)
            awardStringTop = "BANK ROBBERY"
            awardStringBottom = "FOILED"
            # set the bank ramp to completed
            self.game.set_tracking('rightRampStage',4)
            self.game.score(250000)

        elif self.selectedPrizes[5:] == "D":
            self.game.score(20)
            # this one is the lock - going to be complicated
            # if no balls have been locked yet, this awards a free lock straight up
            # or if lock is lit, it locks the ball as well
            if self.game.show_tracking('ballsLockedTotal') == 0 or self.game.show_tracking('mineStatus') == "LOCK":
                # turn off the skillshot layer
                self.layer = None
                # run the lock ball routine
                self.game.mine.lock_ball()
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
            self.game.saloon.light_bounty()
            return

        elif self.selectedPrizes[5:] == "F":
            awardStringTop = "RIVER RESCUE"
            awardStringBottom = "COMPLETE"
            self.game.set_tracking('leftRampStage',4)
            self.game.score(250000)

        elif self.selectedPrizes[5:] == "G":
            # This one is the right loop
            awardStringTop = "TRICK SHOTS"
            awardStringBottom = "COMPLETE"
            self.game.set_tracking('rightLoopStage',4)
            self.game.score(250000)

        elif self.selectedPrizes[5:] == "H":
            # This one is the quickdraw
            awardStringTop = "QUICK DRAW"
            awardStringBottom ="IS LIT"
            self.game.score(10000)
            # turn on the right quickdraw
            self.game.light_quickdraw(1)

        elif self.selectedPrizes[5:] == "I":
            # this one is the left loop
            awardStringTop = "BUCK N BRONCO"
            awardStringBottom ="COMPLETE"
            self.game.set_tracking('leftLoopStage',4)
            self.game.score(250000)

        elif self.selectedPrizes[5:] == "J":
            awardStringTop = "EXTRA BALL"
            awardStringBottom ="IS LIT"

        elif self.selectedPrizes[5:] == "K":
            # this one is the rank
            awardStringTop = "RANK INCREASED"
            self.game.increase_tracking('rank')
            ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHAL"]
            awardStringBottom = "TO " + ranks[self.game.show_tracking('rank')]

        elif self.selectedPrizes[5:] == "L":
            self.game.score(100)
            awardStringTop = "BONUS X"
            awardStringBottom = "INCREASED +3"
            self.game.increase_tracking('bonusX',3)

        elif self.selectedPrizes[5:] == "M":
            awardStringTop = "TRAIN RESCUE"
            awardStringBottom = "COMPLETE"
            self.game.set_tracking('centerRampStage',4)
            self.game.score(250000)

        elif self.selectedPrizes[5:] == "N":
            self.game.score(1000000)
            # setup the wipe animation and the text layer
            topText= dmd.TextLayer(128/2,2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("ONE", blink_frames=5)
            million = dmd.TextLayer(128/2,9, self.game.assets.font_20px_az, "center", opaque=False).set_text("MILLION",blink_frames=5)
            anim = dmd.Animation().load(self.game.assets.anim_cashWipe)
            wipeLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
            wipeLayer.composite_op = "blacksrc"
            self.layer = dmd.GroupedLayer(128,32,[topText,million,wipeLayer])
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            self.game.sound.play(self.game.assets.sfx_yeeHoo)
            self.delay(delay=1.6,handler=self.clear_layer)
            return

        # the award icon
        prizeList = dmd.TextLayer(126, 1, self.game.assets.font_skillshot, "right", opaque=False).set_text(self.selectedPrizes[5:])
        # the award text
        awardTextTop = dmd.TextLayer(6,10,self.game.assets.font_5px_bold_AZ,justify="left",opaque=False).set_text(awardStringTop,blink_frames=10)
        awardTextBottom = dmd.TextLayer(6,18,self.game.assets.font_5px_bold_AZ,justify="left",opaque=True).set_text(awardStringBottom,blink_frames=10)
        self.layer = dmd.GroupedLayer(128, 32, [awardTextBottom, awardTextTop, prizeList,self.mask, self.lasso])

        # remove after 2 seconds
        self.delay(delay=2,handler=self.clear_layer)

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


    def sw_rightReturnLane_active(self,sw):
        # this is how the actual CC tracks the end of
        # the skillshot and I'm not going to argue
        # start the main game music
        self.game.base_game_mode.music_on()
        # unload in 2 seconds - to give
        # the award junk time to finish
        self.delay(delay=2,handler=self.shutdown)

    def music_on(self):
        self.game.sound.play_music(self.game.assets.music_shooterLaneGroove, loops=-1)

    def shutdown(self):
        # unload the skill shot since it's not needed
        # once the game is in play
        self.game.modes.remove(self.game.skill_shot)

    def clear_layer(self):
        self.layer = None

