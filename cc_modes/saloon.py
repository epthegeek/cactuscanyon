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
## This mode controls the saloon
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import dmd
import ep
import random

class Saloon(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(Saloon, self).__init__(game, priority)
        self.myID = "Saloon"
        self.smacked = False
        self.mytValue = self.game.user_settings['Gameplay (Feature)']['Move Your Train Mode']
        self.saloonPulse = self.game.user_settings['Machine (Standard)']['Saloon Eject Strength']
        self.keys_index = {'gunfight':list(range(len(self.game.sound.sounds[self.game.assets.quote_gunfightLit]))),
                           'lit_bounty':list(range(len(self.game.sound.sounds[self.game.assets.quote_bountyLit])))}
        self.counts_index = {'gunfight':0,
                             'lit_bounty':0}
        random.shuffle(self.keys_index['gunfight'])
        random.shuffle(self.keys_index['lit_bounty'])


    def tilted(self):
        if self.game.switches.saloonPopper.is_active():
            self.game.coils.saloonPopper.pulse(self.game.saloon.saloonPulse)
        self.unload()

    def mode_started(self):
        self.unbusy()

    def start_cva(self):
        self.game.modes.add(self.game.cva)
        self.game.cva.intro(entry = "saloon")

    def sw_saloonPopper_active_for_300ms(self,sw):
        #print "Saloon popper mode - active for 300 ms"
        self.saloon_shot()

    def saloon_shot(self):
        #print "saloon shot"
        stackLevel = self.game.show_tracking('stackLevel')
        # if MMB, moonlight or high noon is running, just kick out
        if self.game.marshall_multiball.running or self.game.moonlight.running or self.game.high_noon.running:
            self.kick()
            return

        # Divert here for bionic bart if ready - unless something above guns is running
        if self.game.show_tracking('bionicStatus') == "READY" and True not in stackLevel[1:]:
            # if any of the polly modes is running, bail
            self.game.modes.add(self.game.bionic)
            self.game.bionic.start_bionic()
            # then break out of the rest of this action
            return

        # if cva is ready, we do that - if guns or less is running
        if self.game.show_tracking('cvaStatus') == "READY" and True not in stackLevel[1:] and not self.game.bart.bossFight:
            self.wait_until_unbusy(self.start_cva)
            return

        # if bionic bart is running don't do anything
        if self.game.show_tracking('bionicStatus') == "RUNNING" or \
            self.game.show_tracking('cvaStatus') == "RUNNING":
            #print "cva bionic bail"
            return

        # if drunk multiball is ready, start that, maybe
        if self.game.show_tracking('drunkMultiballStatus') == "READY":
            ## If anything other than a gun mode is running, dmb does not start
            if True in stackLevel[1:]:
                pass
            else:
                self.game.modes.add(self.game.drunk_multiball)
                if self.game.drunk_multiball.enabled:
                    self.wait_until_unbusy(self.game.drunk_multiball.start_drunk)
                return

        # if last call is running - call that hit and bail
        if self.game.last_call.running:
            #print "saloon passing to last call"
            self.game.last_call.saloon_hit()
            return

        # if there's a mode running (other than polly peril and quickdraw), just kick the ball back out
        if not self.game.peril and "RUNNING" not in self.game.show_tracking('quickdrawStatus'):
            if True in stackLevel:
                #print "Saloon Stack bail"
                self.kick()
                return
            else:
                pass

        ## if it it counts as a hit so we have to do that first
        if ep.last_switch != "saloonBart" and ep.last_switch != "rightLoopTop" and not self.smacked:
            # set the busy flag
            self.is_busy()
            # then hit bart
            self.game.bart.hit(True)

        # now we check the bounty after an appropriate delay.
        self.wait_until_unbusy(self.check_bounty)
        ## -- set the last switch hit --
        ep.last_switch = "saloonPopper"

    def unsmack(self):
        self.smacked = False

    def sw_saloonBart_active(self,sw):
        # if last call is running - crank dat
        if self.game.last_call.running:
            self.game.last_call.bart_toy_hit()
            return
        # set a timer flag about the hit
        self.smacked = True
        self.delay("Smack Delay",delay=2,handler=self.unsmack)
        bionic = self.game.show_tracking('bionicStatus')
        if bionic == "READY":
            # play a laugh sound and flash the light and return
            self.game.base.play_quote(self.game.assets.quote_leaderLaugh)
            self.game.coils.saloonFlasher.pulse(30)
            return
        elif bionic == "RUNNING":
            # play a ricochet and flash the light and return
            self.game.sound.play(self.game.assets.sfx_ricochetSet)
            self.game.coils.saloonFlasher.pulse(30)
            return
        # set the busy flag
        self.is_busy()
        # a direct smack to el barto
        self.game.bart.hit()
        ## -- set the last switch hit --
        ep.last_switch = "saloonBart"

    def sw_saloonGate_active(self,sw):
        # play the sound.
        # add some points
        self.game.score(2530,bonus=True)
        # exciting!
        ## -- set the last switch hit --
        ep.last_switch = "saloonGate"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_jetBumpersExit_active(self,sw):
        # if there's an active bart, play a quote
        if self.game.show_tracking('bartStatus') == "RUNNING" or self.game.show_tracking('bartStatus') == "LAST":
            #self.game.base.play_quote(self.game.bart.tauntQuote)
            self.game.bart.play_ordered_quote(self.game.bart.tauntQuote,'taunt',squelch=True)
            # and move the bart
            self.game.bart.animate(2)
        # score some points
        self.game.score(2530,bonus=True)
        # reset the jetcount
        self.game.base.jetCount = 0
        # if the bottom jet was killed
        if self.game.base.jetKilled == True:
            # turn the bumper back on
            self.game.enable_bottom_bumper(True)
            # and reset the flag
            self.game.base.jetKilled = False
        ## -- set the last switch hit --
        ep.last_switch = "jetBumpersExit"

    def kick(self):
        #print "SALOON EJECTING"
        # kick the ball out
        if self.game.switches.saloonPopper.is_active():
            self.game.coils.saloonPopper.pulse(self.saloonPulse)

    def wait_until_unbusy(self,myHandler):
        if not self.busy:
            myHandler()
        else:
            self.delay(delay=0.1,handler=self.wait_until_unbusy,param=myHandler)

    def clear_layer(self):
        self.layer = None
        self.unbusy()

    ###
    ###  ____                    _
    ### | __ )  ___  _   _ _ __ | |_ _   _
    ### |  _ \ / _ \| | | | '_ \| __| | | |
    ### | |_) | (_) | |_| | | | | |_| |_| |
    ### |____/ \___/ \__,_|_| |_|\__|\__, |
    ###                              |___/
    ###
    # TODO move bounty to a higher priority so it can interrupt things?
    def check_bounty(self):
        #print "CHECKING BOUNTY"
        # check the bounty lit status, and collect if needed
        if self.game.show_tracking('isBountyLit'):
            self.collect_bounty()
        # otherwise clear the layer, as we may be coming from a saloon hit and have junk on the screen
        else:
            self.clear_layer()
            self.kick()

    def light_bounty(self,callback=None):
        # set the tracking
        self.game.set_tracking('isBountyLit', True)
        # show something on the screen
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_starsBorder.frames[0])
        topText = ep.pulse_text(self,64,4,"COLLECT BOUNTY")
        bottomText = ep.pulse_text(self,64,16,"IS LIT",color=ep.GREEN)
        self.repeat_ding(4)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,topText,bottomText])
        # play a voice clip about the bounty being ready
        self.play_ordered_quote(self.game.assets.quote_bountyLit,'lit_bounty')
        # lights and whatnot
        self.lamp_update()
        self.delay("Display",delay=1.6,handler=self.clear_layer)
        # if we got a callback - do that - its for skillshot ending
        if callback:
            self.delay(delay=1.6,handler=callback)


    def collect_bounty(self):
        # audit
        self.game.game_data['Feature']['Bounty Awards'] += 1
        # shutup the music
        self.game.squelch_music()
        # turn off the tracking
        self.game.set_tracking('isBountyLit', False)
        # select an award
        prizes = []
        # if we're not running in tournament mode, choices are as normal
        if not self.game.tournament:
            # - Choices:
            #   1 - Light Extra Ball - include as long as we're not at maximum
            if not self.game.max_extra_balls_reached():
                prizes.append('extraBall')
            #   2 - Light Gun Fight - include if not currently lit via dead bart
            if self.game.show_tracking('bartStatus') != "DEAD":
                prizes.append('lightGunFight')
            #   3 - Light Quick Draw
            if "OPEN" in self.game.show_tracking('quickdrawStatus'):
                prizes.append('lightQuickdraw')
            #   4 - Light Lock / Lock ball - included if lock is ready or lit
            if self.game.show_tracking('mineStatus') == "OPEN" or self.game.show_tracking('mineStatus') == "LOCK":
                prizes.append('awardLock')
            #   5 - Bonus multiplier + 5
            if self.game.show_tracking('bonusX') < 6:
                # we're probably going to add this item
                additem = True
                # but if bonus x limits are on
                if self.game.bonus_lanes.limited:
                    # If adding 5 would go over max, don't do that
                    if (self.game.show_tracking('bonusX') + 5) > self.game.bonus_lanes.max:
                        additem = False

                if additem:
                    prizes.append('bonusX')
            #   6 - Increase your rank
            if self.game.show_tracking('rank') < 4 and not self.game.bart.bossFight:
                prizes.append('rank')
            #   7 - Points 250,000
            prizes.append('points250k')
            #   8 - Points 500,000
            prizes.append('points500k')
            #   9 - + 1 Million Bonus
            prizes.append('points1Mil')
            # 10 - Move your train - only add if polly isn't running
            if not self.game.peril and self.game.move_your_train not in self.game.modes and self.mytValue == 'Enabled' and not self.game.train.mytFail:
                prizes.append('moveYourTrain')
            # 11 - 30 second ball save
            if not self.game.trough.ball_save_active:
                prizes.append('ballSave')
            # 12 - franks n beans
            if self.game.user_settings['Gameplay (Feature)']['Franks N Beans'] == True and not self.game.show_tracking('farted'):
                prizes.append('franksNBeans')
            # so as of this point we have a prizes list to use
            # and pick one of those at random
            self.bountyPrize = random.choice(prizes)
        # this section is for when tournament mode IS active
        else:
            # only do franks and beans once
            if self.game.user_settings['Gameplay (Feature)']['Franks N Beans'] == True and not self.game.show_tracking('farted'):
                franksOption = 'franksNBeans'
            else:
                franksOption = 'points250k'
            if self.game.show_tracking('rank') < 4:
                rankOption = 'rank'
            else:
                rankOption = 'points250k'
            prizes = ['points500k','bonusX','points1Mil',rankOption,'ballSave',franksOption]
            # get the current player bounty index position
            index = self.game.show_tracking('bountyIndex')
            # set the bounty based on index
            self.bountyPrize = prizes[index]
            # increase the index
            index += 1
            # cap at 5
            if index > 5:
                index = 0
            # set the new index
            self.game.set_tracking('bountyIndex',index)
        #print "SELECTED BOUNTY: " + self.bountyPrize
        # play some sounds/music
        self.game.sound.play(self.game.assets.sfx_bountyCollected)

        # give the award
        mayorfeet = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_mayorFeet.frames[0])
        self.layer = mayorfeet
        # pause a bit and then pan up the mayor
        self.delay(delay=.3,handler=self.mayor_pan)

    def mayor_pan(self):
        anim = self.game.assets.dmd_mayorPan
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False)
        self.layer = animLayer
        myWait = len(anim.frames) / 60.0
        # when the pan finishes play the animation to reveal the award
        self.delay(delay = myWait,handler=self.award_bounty)

    def award_bounty(self):
        # setup the award
        # make this false unless set otherwise
        self.prizeVal = False
        prizeText2 = None
        # set a prizeHandler and prizeParam based on bounty for use later
        if self.bountyPrize == 'extraBall':
            # audit
            self.game.game_data['Feature']['EB Lit Bounty'] += 1
            prizeText = "EXTRA BALL"
            prizeText2 = "IS LIT"
            self.prizeHandler = self.game.mine.light_extra_ball
            self.prizeParam = False
        elif self.bountyPrize == 'lightGunFight':
            prizeText = "GUNFIGHT"
            prizeText2 = "IS LIT"
            self.prizeHandler = self.light_gunfight
            self.prizeParam = False
        elif self.bountyPrize == 'lightQuickdraw':
            prizeText = "QUICKDRAW"
            prizeText2 = "IS LIT"
            self.prizeHandler = self.game.base.light_quickdraw
            # have to figure out which quickdraw to light
            if self.game.show_tracking('quickdrawStatus',0) != "READY":
                self.prizeParam = 0
            else:
                self.prizeParam = 1
        elif self.bountyPrize == 'awardLock':
            prizeText = "ADVANCE MINE"
            if self.game.show_tracking('mineStatus') == "OPEN":
                self.prizeHandler = self.game.mine.light_lock
            else:
                self.prizeHandler = self.game.mine.lock_ball
            self.prizeParam = False
        elif self.bountyPrize == 'bonusX':
            prizeText = "+5 BONUS X"
            self.prizeHandler = self.game.increase_tracking
            self.prizeParam = 'bonusX'
            self.prizeVal = 5
        elif self.bountyPrize == 'rank':
            prizeText = "RANK"
            prizeText2 = "INCREASED"
            self.prizeHandler = self.game.badge.increase_rank
            self.prizeParam = False
        elif self.bountyPrize == 'points250k':
            prizeText = str(ep.format_score(250000))
            self.prizeHandler = self.game.score
            self.prizeParam = 250000
        elif self.bountyPrize == 'points500k':
            prizeText = str(ep.format_score(500000))
            self.prizeHandler = self.game.score
            self.prizeParam = 500000
        elif self.bountyPrize == 'points1Mil':
            prizeText = str(ep.format_score(1000000))
            self.prizeHandler = self.game.score
            self.prizeParam = 1000000
        elif self.bountyPrize == 'moveYourTrain':
            prizeText = "MOVE"
            prizeText2 = "YOUR TRAIN"
            # load the MYT mode to move the train and set up
            self.game.modes.add(self.game.move_your_train)
            # set the handler to the start of MYT
            self.prizeHandler = self.game.move_your_train.start
            # null the param flag
            self.prizeParam = False
        elif self.bountyPrize == 'ballSave':
            prizeText = "30 SEC"
            prizeText2 = "BALL SAVER"
            self.game.trough.start_ball_save(num_balls_to_save=1, time=30, now=True, allow_multiple_saves=False)
            self.prizeParam = 10000
            self.prizeHandler = self.game.score
        elif self.bountyPrize == 'franksNBeans':
            prizeText = "FRANKS N"
            prizeText2 = "BEANS"
            self.delay(delay=3,handler=self.game.base.start_franks)
            self.prizeParam = 10000
            self.prizeHandler = self.game.score
        else:
            prizeText = "WTF"
            #print "WTF BOUNTY: " + self.bountyPrize

        # load the animation
        # set up the layer
        animLayer = ep.EP_AnimatedLayer(self.game.assets.dmd_bountyCollected)
        animLayer.composite_op = "blacksrc"
        animLayer.frame_time = 6
        animLayer.hold = True
        # calculate a wait time with some buffer after to leave the text
        myWait = (len(self.game.assets.dmd_bountyCollected.frames) /10 ) + 2
        # set the backdrop for the revealed award
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_moneybagBorder.frames[0])
        # set the text for the award
        awardTextTop = dmd.TextLayer(76,3,self.game.assets.font_9px_az,justify="center",opaque=False)
        awardTextTop.set_text("YOUR BOUNTY:")
        awardTextTop.composite_op = "blacksrc"
        if prizeText2 != None:
            awardTextMiddle = ep.EP_TextLayer(76,15,self.game.assets.font_6px_az,justify="center",opaque=False)
            awardTextBottom = ep.EP_TextLayer(76,24,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextMiddle.set_text(prizeText,color=ep.GREEN)
            awardTextMiddle.composite_op = "blacksrc"
            awardTextBottom.set_text(prizeText2,color=ep.GREEN)
            self.layer= dmd.GroupedLayer(128,32,[backdrop,awardTextBottom,awardTextMiddle,awardTextTop,animLayer])
        else:
            awardTextMiddle = ep.EP_TextLayer(76,17,self.game.assets.font_9px_az,justify="center",opaque=False)
            awardTextMiddle.set_text(prizeText,color=ep.GREEN)
            self.layer= dmd.GroupedLayer(128,32,[backdrop,awardTextMiddle,awardTextTop,animLayer])
        # play a lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_topToBottom, repeat=False,callback=self.lamp_update)
        # play the quote
        self.game.base.priority_quote(self.game.assets.quote_bountyCollected)
        # then clear the layer and kick the ball out
        self.delay(delay = myWait,handler=self.finish_up)

    def finish_up(self):
        self.clear_layer()
        # this should hopefully do the actual awarding
        if self.prizeVal:
            self.prizeHandler(self.prizeParam,self.prizeVal)
        elif self.prizeParam != False:
            self.prizeHandler(self.prizeParam)
        else:
            self.prizeHandler()
        # update lamps
        self.lamp_update()

        # for anything other than move your train, kick the ball out
        if self.bountyPrize != "moveYourTrain":
            self.kick()
        self.game.restore_music()

    def repeat_ding(self,times):
        self.game.sound.play(self.game.assets.sfx_bountyBell)
        self.game.coils.beaconFlasher.pulse(ep.FLASHER_PULSE)
        times -= 1
        if times > 0:
            self.delay(delay=0.4,handler=self.repeat_ding,param=times)

    ## Gunfight

    def light_gunfight(self,callback=None):
        #print "GUNFIGHT IS LIT"
        # turn on the lights
        # show the display
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_singleCowboyBorder.frames[0])
        textString1 = "GUNFIGHT"
        textLayer1 = ep.pulse_text(self,77,2,textString1,size="12px")
        textString2 = "IS LIT"
        textLayer2 = ep.pulse_text(self,77,15,textString2,size="12px",color=ep.GREEN)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2])
        # play a quote
        self.game.sound.play(self.game.assets.sfx_flourish6)
        self.play_ordered_quote(self.game.assets.quote_gunfightLit,'gunfight',priority=True)
        # set the tracking
        self.game.set_tracking('gunfightStatus',"READY")
        self.lamp_update()
        self.game.coils.leftGunFlasher.schedule(0x11111111,cycle_seconds=1)
        self.game.coils.rightGunFlasher.schedule(0x11111111,cycle_seconds=1)

        if callback != None:
            #print "I GOT A GUNFIGHT CALLBACK"
            self.delay("Callback",delay=2,handler=callback)
        self.delay(delay=2,handler=self.clear_layer)
        if self.busy:
            #print "Light Gunfight - Delay timer for unbusy"
            self.delay(delay=2,handler=self.unbusy)
