##
## This mode controls the saloon
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes
import ep
import random
import locale

class Saloon(game.Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(Saloon, self).__init__(game, priority)
        self.busy = False

    def sw_saloonPopper_active_for_300ms(self,sw):
        # if there's a mode running, just kick the ball back out
        if True in self.game.show_tracking('stackLevel'):
            self.kick()
        # Divert here for bionic bart if ready
        elif self.game.show_tracking('bionicStatus') == "READY":
            self.game.modes.add(self.game.bionic)
            self.game.bionic.start_bionic()
            # then break out of the rest of this action
            return

        else:
            ## if we went through the gate, and missed bart or snuck in the back way
            ## it counts as a hit so we have to do that first
            if ep.last_switch != "saloonBart" and ep.last_switch != "rightLoopTop":
                # set the busy flag
                self.busy = True
                # if drunk multiball is ready, start that, maybe
                if self.game.show_tracking('drunkMultiballStatus') == "READY":
                ## If any level below is running, avoid multiball start
                    stackLevel = self.game.show_tracking('stackLevel')
                    if True in stackLevel[:2]:
                        self.game.bart.hit()
                    else:
                        self.game.modes.add(self.game.drunk_multiball)
                        self.game.drunk_multiball.start_drunk()
                else:
                    # then hit bart
                    self.game.bart.hit()
            # now we check the bounty after an appropriate delay.
            self.wait_until_unbusy(self.check_bounty)
            ## -- set the last switch hit --
            ep.last_switch = "saloonPopper"

    def sw_saloonBart_active(self,sw):
        # set the busy flag
        self.busy = True
        # a direct smack to el barto
        self.game.bart.hit()
        ## -- set the last switch hit --
        ep.last_switch = "saloonBart"

    def sw_saloonGate_active(self,sw):
        # play the sound.
        # add some points
        self.game.score_with_bonus(2530)
        # exciting!
        ## -- set the last switch hit --
        ep.last_switch = "saloonGate"


    def sw_jetBumpersExit_active(self,sw):
        # if there's an active bart, play a quote
        if self.game.show_tracking('bartStatus') == "RUNNING":
            self.game.sound.play_voice(self.game.bart.tauntQuote)
            # and move the bart
            self.game.bart.move()
            self.delay(delay=0.03,handler=self.game.bart.light)
            self.delay(delay=0.07,handler=self.game.bart.move)
        # score some points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "jetBumpersExit"

    def kick(self):
        # kick the ball out
        if self.game.switches.saloonPopper.is_active():
            self.game.coils.saloonPopper.pulse(30)

    def wait_until_unbusy(self,myHandler):
        if not self.busy:
            myHandler()
        else:
            self.delay(delay=0.1,handler=self.wait_until_unbusy,param=myHandler)

    def update_lamps(self):
        self.disable_lamps()
        ## if status is off, we bail here
        if self.game.show_tracking('lampStatus') == "OFF":
            return

        # flash the saloon arrow if bionic bart is ready
        bionicStatus = self.game.show_tracking('bionicStatus')
        if bionicStatus == "READY":
            self.game.lamps.saloonArrow.schedule(0xF0F0F0F0)
            self.game.lamps.bountySaloon.schedule(0xF0F0F0F0)
        # flash bount and arrow if running and loaded
        elif bionicStatus == "RUNNING":
            if self.game.bionic.loaded:
                self.game.lamps.saloonArrow.schedule(0x00FF00FF)
                self.game.lamps.bountySaloon.schedule(0x00FF00FF)
            return

        beacon = False
        if self.game.show_tracking('bartStatus') == 'RUNNING' or self.game.show_tracking('bartStatus') == 'LAST':
            if bionicStatus != "READY" and bionicStatus != "RUNNING":
                self.game.lamps.saloonArrow.enable()
        if self.game.show_tracking('isBountyLit'):
            self.game.lamps.bountySaloon.schedule(0xFF00FF00)
            self.game.lamps.bountyBeacon.enable()
            beacon = True
        if self.game.show_tracking('extraBallsPending') > 0:
            beacon = True
        ## todo jackpot isn't set up
        if beacon:
            self.game.lamps.shootToCollect.enable()
        if self.game.show_tracking('gunfightStatus') == 'READY':
            self.game.lamps.rightGunfightPin.enable()
            self.game.lamps.leftGunfightPin.enable()
        if self.game.show_tracking('drunkMultiballStatus') == "READY":
            self.game.lamps.bountySaloon.disable()
            self.game.lamps.bountySaloon.schedule(0xF0F0F0F0)

    def disable_lamps(self):
        self.game.lamps.saloonArrow.disable()
        self.game.lamps.bountySaloon.disable()
        self.game.lamps.shootToCollect.disable()
        self.game.lamps.bountyBeacon.disable()
        self.game.lamps.jackpotBeacon.disable()
        self.game.lamps.rightGunfightPin.disable()
        self.game.lamps.leftGunfightPin.disable()

    def clear_layer(self):
        self.layer = None
        self.busy = False

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
        print "CHECKING BOUNTY"
        # check the bounty lit status, and collect if needed
        if self.game.show_tracking('isBountyLit'):
            self.collect_bounty()
        # otherwise clear the layer, as we may be coming from a saloon hit and have junk on the screen
        else:
            self.clear_layer()
            # TODO kick the ball out here
            self.kick()

    def light_bounty(self):
        # set the tracking
        self.game.set_tracking('isBountyLit', True)
        # show something on the screen
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'stars-border.dmd').frames[0])
        topText = ep.pulse_text(self,64,4,"COLLECT BOUNTY")
        bottomText = ep.pulse_text(self,64,16,"IS LIT")
        self.repeat_ding(4)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,topText,bottomText])
        # play a voice clip about the bounty being ready
        self.game.sound.play(self.game.assets.quote_bountyLit)
        # lights and whatnot
        self.update_lamps()
        self.delay(delay=1.6,handler=self.clear_layer)


    def collect_bounty(self):
        # shutup the music
        print "collect_bounty IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # TODO award the prize
        # turn off the tracking
        self.game.set_tracking('isBountyLit', False)
        # select an award
        prizes = []
        # - Choices:
        #   1 - Light Extra Ball - include as long as we're not at maximum
        if self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
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
            prizes.append('bonusX')
        #   6 - Increase your rank
        if self.game.show_tracking('rank') < 4:
            prizes.append('rank')
        #   7 - Points 250,000
        prizes.append('points250k')
        #   8 - Points 500,000
        prizes.append('points500k')
        #   9 - + 1 Million Bonus
        prizes.append('points1Mil')
        # so as of this point we have a prizes list to use
        # and pick one of those at random
        self.bountyPrize = random.choice(prizes)
        print "SELECTED BOUNTY: " + self.bountyPrize
        # play some sounds/music
        self.game.sound.play(self.game.assets.sfx_bountyCollected)

        # give the award
        mayorfeet = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'mayor-feet.dmd').frames[0])
        self.layer = mayorfeet
        # pause a bit and then pan up the mayor
        self.delay(delay=.3,handler=self.mayor_pan)

    def mayor_pan(self):
        anim = dmd.Animation().load(ep.DMD_PATH+'mayor-pan.dmd')
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False)
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
            prizeText = "EXTRA BALL"
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
            self.prizeHandler = self.game.base_game_mode.light_quickdraw
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
            self.prizeHandler = self.game.increase_tracking
            self.prizeParam = 'rank'
            self.game.base_game_mode.update_lamps()
        elif self.bountyPrize == 'points250k':
            prizeText = "250,000"
            self.prizeHandler = self.game.score
            self.prizeParam = 250000
        elif self.bountyPrize == 'points500k':
            prizeText = "500,000"
            self.prizeHandler = self.game.score
            self.prizeParam = 500000
        elif self.bountyPrize == 'points1Mil':
            prizeText = "1,000,000"
            self.prizeHandler = self.game.score
            self.prizeParam = 1000000
        else:
            prizeText = "WTF"
            print "WTF BOUNTY: " + self.bountyPrize

        # load the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'bounty-collected.dmd')
        # set up the layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.composite_op = "blacksrc"
        animLayer.frame_time = 6
        animLayer.hold = True
        # calculate a wait time with some buffer after to leave the text
        myWait = (len(anim.frames) /10 ) + 2
        # set the backdrop for the revealed award
        backdrop = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(ep.DMD_PATH+'moneybag-border.dmd').frames[0])
        # set the text for the award
        awardTextTop = dmd.TextLayer(76,4,self.game.assets.font_9px_az,justify="center",opaque=False)
        awardTextTop.set_text("YOUR BOUNTY:")
        awardTextTop.composite_op = "blacksrc"
        if prizeText2 != None:
            awardTextMiddle = dmd.TextLayer(76,15,self.game.assets.font_6px_az,justify="center",opaque=False)
            awardTextBottom = dmd.TextLayer(76,24,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextMiddle.set_text(prizeText)
            awardTextMiddle.composite_op = "blacksrc"
            awardTextBottom.set_text(prizeText2)
            self.layer= dmd.GroupedLayer(128,32,[backdrop,awardTextBottom,awardTextMiddle,awardTextTop,animLayer])
        else:
            awardTextMiddle = dmd.TextLayer(76,17,self.game.assets.font_9px_az,justify="center",opaque=False)
            awardTextMiddle.set_text(prizeText)
            self.layer= dmd.GroupedLayer(128,32,[backdrop,awardTextMiddle,awardTextTop,animLayer])
        # play a lampshow
        self.game.lampctrl.play_show(self.game.assets.lamp_topToBottom, repeat=False,callback=self.game.update_lamps)
        # play the quote
        self.game.sound.play_voice(self.game.assets.quote_bountyCollected)
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
        # then kick out
        self.update_lamps()
        self.kick()
        self.game.base_game_mode.music_on()

    def repeat_ding(self,times):
        self.game.sound.play(self.game.assets.sfx_bountyBell)
        self.game.coils.beaconFlasher.pulse(ep.FLASHER_PULSE)
        times -= 1
        if times > 0:
            self.delay(delay=0.4,handler=self.repeat_ding,param=times)

    ## Gunfight

    def light_gunfight(self,callback=None):
        print "GUNFIGHT IS LIT"
        # turn on the lights
        # show the display
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'single-cowboy-border.dmd').frames[0])
        textString1 = "GUNFIGHT"
        textLayer1 = ep.pulse_text(self,77,2,textString1,size="12px")
        textString2 = "IS LIT"
        textLayer2 = ep.pulse_text(self,77,15,textString2,size="12px")
        self.layer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2])
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_gunfightLit)
        # set the tracking
        self.game.set_tracking('gunfightStatus',"READY")
        self.update_lamps()
        if callback != None:
            print "I GOT A GUNFIGHT CALLBACK"
            self.delay(delay=2,handler=callback)
        self.delay(delay=2,handler=self.clear_layer)