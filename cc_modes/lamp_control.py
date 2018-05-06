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
## This Class is the mode that runs at all times during active play and acts
## as the central controller for all the main playfield lights
##

#from procgame import *
import ep

class LampControl(ep.EP_Mode):
    """Playfield Lamp Controller"""
    def __init__(self, game,priority):
        super(LampControl, self).__init__(game, priority)
        self.myID = "Lamp Control"

        # lamp groups
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
        # combo lamps
        self.comboLights = [self.game.lamps.rightRampCombo,
                            self.game.lamps.leftRampCombo,
                            self.game.lamps.centerRampCombo,
                            self.game.lamps.leftLoopCombo,
                            self.game.lamps.rightLoopCombo]
        # bad guys
        self.badGuyLamps = [self.game.lamps.badGuyL0,
                      self.game.lamps.badGuyL1,
                      self.game.lamps.badGuyL2,
                      self.game.lamps.badGuyL3]

        self.bigFive = [self.left_loop,self.left_ramp,self.center_ramp,self.right_loop,self.right_ramp]
        self.lights_out = self.game.user_settings['Gameplay (Feature)']['Party Mode'] == 'Lights Out'


    def tilted(self):
        pass

    def disable_lamps(self):
        # disable all playfield lamps
        for lamp in self.game.lamps.items_tagged('Main'):
            lamp.disable()
        self.game.coils.mineFlasher.disable()
        # Note, this doesn't disable the bonus lanes, the bad guys, or the combos

    def disable_all_lamps(self):
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()
        # this gets scheduled in some instances too, so for good measure
        self.game.coils.mineFlasher.disable()

    def update(self):
        # marhsall multiball is a whole separate thing - dont run this when it's running
        if self.game.marshall_multiball.running:
            return

        # this is the big mother.  Called any time playfield lamps should change.
        # first, disable the lamps
        self.disable_lamps()

        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        #   ____        _
        #  / ___|_   __/ \
        # | |   \ \ / / _ \
        # | |___ \ V / ___ \
        #  \____| \_/_/   \_\
        #
        # if CvA is running - Only update the main shots, everything else stays dark
        if self.game.cva.running:
            # update the main 5 shots, and bail
            self.update_bigFive('CvA')
            return

        #  ____  _             _        ____             _
        # | __ )(_) ___  _ __ (_) ___  | __ )  __ _ _ __| |_
        # |  _ \| |/ _ \| '_ \| |/ __| |  _ \ / _` | '__| __|
        # | |_) | | (_) | | | | | (__  | |_) | (_| | |  | |_
        # |____/|_|\___/|_| |_|_|\___| |____/ \__,_|_|   \__|
        #
        bionicStatus = self.game.show_tracking('bionicStatus')
        # If bionic bart is running, run a subset and return
        if bionicStatus == "RUNNING":
            # if loaded, flash the saloon
           if self.game.bionic.loaded:
                self.saloon_flash()
           # Run the big five
           self.update_bigFive('Bionic')
           return

        #  _   _ _       _       _   _
        # | | | (_) __ _| |__   | \ | | ___   ___  _ __
        # | |_| | |/ _` | '_ \  |  \| |/ _ \ / _ \| '_ \
        # |  _  | | (_| | | | | | |\  | (_) | (_) | | | |
        # |_| |_|_|\__, |_| |_| |_| \_|\___/ \___/|_| |_|
        #          |___/
        highNoonStatus = self.game.show_tracking('highNoonStatus')
        if highNoonStatus == "RUNNING":
        # if high noon is running, run a subset
            self.update_bigFive('highNoon')
            self.combos('highNoon')
            self.badge('On')
            self.bad_guys()
            return

        ## Last call
        if self.game.last_call.running:
            self.update_bigFive('lastCall')
            return

        # then - check if lamps are disabled
        status = self.game.show_tracking('lampStatus')
        ## if status is off, we bail here
        if status == "OFF":
            return

        mineStatus = self.game.show_tracking('mineStatus')

        # main shots - basic update
        # if goldmine. stampede, or polly is running, run a non standard update
        if mineStatus == "RUNNING" or self.game.peril or self.game.stampede.running or self.game.drunk_multiball.running:
            # do these in order to the stacking shows the right item in the end
            # if drunk multiball is running, update those
            # if the goldmine is running - update with those
            if mineStatus == "RUNNING":
                self.update_bigFive('Mine')
                self.combos('Mine')
            elif self.game.drunk_multiball.running:
                self.update_bigFive('Drunk')
            # if stampede is running - do that next
            elif self.game.stampede.running:
                self.update_bigFive('Stampede')
                self.combos('Stampede')
            # if polly is running - could be ALSO running - update with that to overwrite jackpot updates
            elif self.game.peril:
                self.update_bigFive('Polly')
            else:
                pass
        # otherwise do the basic update of the big five
        else:
            self.update_bigFive()

        # update the bonus lanes
        self.bonus_lanes(External=False)

        # if goldmine isn't running, update the combos
        if mineStatus != "RUNNING":
            self.combos('Timer')

        # status checks for use later
        bartStatus = self.game.show_tracking('bartStatus')
        drunkStatus =  self.game.show_tracking('drunkMultiballStatus')
        ebPending = self.game.show_tracking('extraBallsPending')

        # Down here is the basic stuff

        #   ____            _
        #  | __ )  __ _  __| | __ _  ___
        #  |  _ \ / _` |/ _` |/ _` |/ _ \
        #  | |_) | (_| | (_| | (_| |  __/
        #  |____/ \__,_|\__,_|\__, |\___|
        #                     |___/
        #
        # If bionic is ready, then the badge lights chase
        if bionicStatus == "READY":
            self.badge('Chase')
        # If high noon is ready, flash the badge
        elif highNoonStatus == "READY":
            self.badge('Flash')
        # otherwise, they just light whichever ones are won
        else:
            self.badge('Level')

        # the rank lamps - enable based on curent rank
        self.rank_level()

        #   ___        _      _       _
        #  / _ \ _   _(_) ___| | ____| |_ __ __ ___      _____
        # | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / / __|
        # | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /\__ \
        #  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/ |___/
        #
        gunsAllowed = self.game.base.guns_allowed()
        left = self.game.show_tracking('quickdrawStatus',0)
        right = self.game.show_tracking('quickdrawStatus',1)
        if gunsAllowed:
            # if a gunfight is lit, that takes precedent
            if self.game.show_tracking('gunfightStatus') == 'READY':
                self.gunfight_flash()
            else:
                if left == 'READY':
                    self.game.lamps.leftReturnQuickdraw.schedule(0x00FF00FF)
                if right == 'READY' and self.game.base.guns_allowed():
                    self.game.lamps.rightReturnQuickdraw.schedule(0x00FF00FF)
                ## on a second pass thorugh the returns - if showdown is ready, flash 'em both
                if self.game.show_tracking('showdownStatus') == "READY" or self.game.show_tracking('ambushStatus') == "READY":
                    self.game.lamps.rightReturnQuickdraw.schedule(0x0F0F0F0F)
                    self.game.lamps.leftReturnQuickdraw.schedule(0xF0F0F0F0)
        # even if guns aren't allowed the quickdraw playfield lights should be on if needed
        if self.game.taf_tribute.running:
            self.game.lamps.leftQuickdraw.schedule(0x0F0F0F0F)
        else:
            if left == 'OPEN':
                self.game.lamps.leftQuickdraw.enable()
            if left == 'TOP' or left == 'BOT':
                self.game.lamps.leftQuickdraw.schedule(0x00FF00FF)
        if right == 'OPEN':
            self.game.lamps.topRightQuickdraw.enable()
            self.game.lamps.bottomRightQuickdraw.enable()
        if right == 'TOP':
            self.game.lamps.bottomRightQuickdraw.enable()
        if right == 'BOT':
            self.game.lamps.topRightQuickdraw.enable()


        #   __  __ _
        #  |  \/  (_)_ __   ___
        #  | |\/| | | '_ \ / _ \
        #  | |  | | | | | |  __/
        #  |_|  |_|_|_| |_|\___|
        #
        # if there's an extra ball pending, flash the light at the mine
        if ebPending > 0:
            self.game.lamps.extraBall.schedule(0x0F0F0F0F)
        # This batch of stuff doesn't happen during certain modes
        if self.game.stampede.running or \
            self.game.ambush.running or \
            self.game.showdown.running or \
            self.game.cva.running or \
            self.game.high_noon.running:
            pass
        else:
            # for the mine arrow , ther'es a bunch of conditionals
            if highNoonStatus == "READY":
                self.game.lamps.mineLock.schedule(0x00FF00FF)
                self.game.coils.mineFlasher.schedule(0x00010001)
            elif mineStatus == "LOCK":
                self.game.lamps.mineLock.enable()
            elif mineStatus == "READY":
                self.game.lamps.mineLock.schedule(0x0F0F0F0F)
            elif self.game.show_tracking('motherlodeLit') or self.game.gm_multiball.restartFlag:
                self.game.coils.mineFlasher.schedule(0x00010001)
                self.game.lamps.mineLock.schedule(0x0F0F0F0F)
            else:
                pass

        #
        #  ____        _
        # / ___|  __ _| | ___   ___  _ __
        # \___ \ / _` | |/ _ \ / _ \| '_ \
        #  ___) | (_| | | (_) | (_) | | | |
        # |____/ \__,_|_|\___/ \___/|_| |_|
        #
        # if bionic is ready, both lights flash fast
        if self.game.doubler.ready:
            self.saloon_flash(1)
        elif bionicStatus == "READY":
            self.saloon_flash(1)
        # if drunk multiball is ready - flash the arrow
        elif drunkStatus == "READY":
            self.game.lamps.bountySaloon.schedule(0xF0F0F0F0)
        # Otherwise, if there's a live bart bro, turn on the saloon arrow
        elif bartStatus == 'RUNNING' or bartStatus == 'LAST':
            if bionicStatus != "READY":
                self.game.lamps.saloonArrow.enable()
        else:
            pass

        #  ____                                ____ _           _
        # | __ )  ___  __ _  ___ ___  _ __    / ___| |_   _ ___| |_ ___ _ __
        # |  _ \ / _ \/ _` |/ __/ _ \| '_ \  | |   | | | | / __| __/ _ \ '__|
        # | |_) |  __/ (_| | (_| (_) | | | | | |___| | |_| \__ \ ||  __/ |
        # |____/ \___|\__,_|\___\___/|_| |_|  \____|_|\__,_|___/\__\___|_|

        beacon = False
        # if a bounty is lit - flash the saloon and turn on the beacon light
        if self.game.show_tracking('isBountyLit'):
            if bionicStatus != "READY" and drunkStatus != "READY":
                self.game.lamps.bountySaloon.schedule(0xFF00FF00)
            self.game.lamps.bountyBeacon.enable()
            beacon = True
        # if there's an extra ball to collect - turn on the beacon light for it
        if ebPending > 0:
            beacon = True
        # if any beacon light is on, enable the shoot to collect above
        if beacon:
            self.game.lamps.shootToCollect.enable()

        #
        #  ____  _                 _        _               _
        # / ___|| |__   ___   ___ | |_     / \   __ _  __ _(_)_ __
        # \___ \| '_ \ / _ \ / _ \| __|   / _ \ / _` |/ _` | | '_ \
        #  ___) | | | | (_) | (_) | |_   / ___ \ (_| | (_| | | | | |
        # |____/|_| |_|\___/ \___/ \__| /_/   \_\__, |\__,_|_|_| |_|
        #                                       |___/
        # if ball saver is on, flash
        if self.game.trough.ball_save_active:
            self.game.lamps.shootAgain.schedule(0x00FF00FF)
        # if not ball saver, but extra ball - turn it on
        elif self.game.current_player().extra_balls > 0:
            self.game.lamps.shootAgain.enable()
        # otherwise, it's off
        else:
            pass

        #   ___        _   _
        #  / _ \ _   _| |_| | __ _ _ __   ___  ___
        # | | | | | | | __| |/ _` | '_ \ / _ \/ __|
        # | |_| | |_| | |_| | (_| | | | |  __/\__ \
        #  \___/ \__,_|\__|_|\__,_|_| |_|\___||___/
        #
        # if the bozo ball is on, flash the outlanes
        if self.game.show_tracking('bozoBall'):
            self.game.lamps.rightOutSpecial.schedule(0x0F0F0F0F)
            self.game.lamps.leftOutGunfight.schedule(0x0F0F0F0F)

        #
        #  ____            _    ____
        # | __ )  __ _  __| |  / ___|_   _ _   _ ___
        # |  _ \ / _` |/ _` | | |  _| | | | | | / __|
        # | |_) | (_| | (_| | | |_| | |_| | |_| \__ \
        # |____/ \__,_|\__,_|  \____|\__,_|\__, |___/
        #                                  |___/
        # if showdown or ambush are running, don't show the dead guy lights - even though they should be off
        if self.game.showdown.running or self.game.ambush.running:
            pass
        else:
            self.bad_guys()

    # This is a combo routine for the 5 main shots
    def update_bigFive(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # polly only updates the main 3 - run the other 2 as base
        if mode == "Polly":
            self.left_ramp('Polly')
            self.center_ramp('Polly')
            self.right_ramp('Polly')
            self.left_loop()
            self.right_loop()
        else:
            for handler in self.bigFive:
                handler(mode)

    #  _          __ _     _
    # | |    ___ / _| |_  | |    ___   ___  _ __
    # | |   / _ \ |_| __| | |   / _ \ / _ \| '_ \
    # | |__|  __/  _| |_  | |__| (_) | (_) | |_) |
    # |_____\___|_|  \__| |_____\___/ \___/| .__/
    #                                      |_|
    def left_loop(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # the left loop collection of lights
        ## high noon
        if mode == "highNoon":
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)

        # bionic bart
        elif mode == "Bionic":
            if 0 in self.game.bionic.activeShots:
                self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
                self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
                self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
                self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)

        # cva
        elif mode == "CvA":
            if self.game.cva.activeShot == 0:
                self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
                self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
                self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
                self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)

        # last call
        elif mode == 'lastCall':
            self.game.lamps.leftLoopBuckNBronco.schedule(0x00FF00FF)
            self.game.lamps.leftLoopWildRide.schedule(0x00FF00FF)
            self.game.lamps.leftLoopRideEm.schedule(0x00FF00FF)
            self.game.lamps.leftLoopJackpot.schedule(0x00FF00FF)

        # drunk multiball
        elif mode == "Drunk":
            if 'leftLoop' in self.game.drunk_multiball.active:
                self.game.lamps.leftLoopJackpot.enable()
                self.game.lamps.leftLoopRideEm.schedule(0xFF00FF00)
                self.game.lamps.leftLoopWildRide.schedule(0xFF00FF00)
                self.game.lamps.leftLoopBuckNBronco.schedule(0xFF00FF00)

        ## goldmine check
        elif mode == "Mine":
            if not self.game.gm_multiball.restartFlag:
                # check if this jackpot shot is active
            # if drunk multiball is running - check those and update
                if self.game.drunk_multiball.running and 'leftLoop' in self.game.drunk_multiball.active:
                    self.game.lamps.leftLoopJackpot.enable()
                    self.game.lamps.leftLoopRideEm.schedule(0xFF00FF00)
                    self.game.lamps.leftLoopWildRide.schedule(0xFF00FF00)
                    self.game.lamps.leftLoopBuckNBronco.schedule(0xFF00FF00)
                else:
                    if self.game.show_tracking('jackpotStatus',0):
                        self.game.lamps.leftLoopJackpot.enable()
                        self.game.lamps.leftLoopRideEm.schedule(0xF0FFF0FF)
                        self.game.lamps.leftLoopWildRide.schedule(0xFF0FFF0F)
                        self.game.lamps.leftLoopBuckNBronco.schedule(0xFFF0FFF0)

        ##  stampede
        elif mode == "Stampede":
            ## left loop is #0 in the stampede jackpot list
            if self.game.stampede.active == 0:
                self.game.lamps.leftLoopJackpot.schedule(0xF000F000)
                self.game.lamps.leftLoopRideEm.schedule(0x0F000F00)
                self.game.lamps.leftLoopWildRide.schedule(0x00F000F0)
                self.game.lamps.leftLoopBuckNBronco.schedule(0x000F000F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.leftLoopJackpot.schedule(0xFF00FF00)

        elif mode == "Disable":
            for lamp in self.game.lamps.items_tagged('leftLoop'):
                lamp.disable()

        ## This is the base mode if all else passes
        else:
            stage = self.game.show_tracking('leftLoopStage')

            if stage == 1:
                # blink the first light
                self.game.lamps.leftLoopBuckNBronco.schedule(0x0F0F0F0F)
            elif stage == 2:
                # first light on
                self.game.lamps.leftLoopBuckNBronco.enable()
                # blink the second
                self.game.lamps.leftLoopWildRide.schedule(0x0F0F0F0F)
            elif stage == 3:
                # first two on
                self.game.lamps.leftLoopBuckNBronco.enable()
                self.game.lamps.leftLoopWildRide.enable()
                # blink the third
                self.game.lamps.leftLoopRideEm.schedule(0x0F0F0F0F)
            # this is completed
            elif stage == 4:
                # all three on
                self.game.lamps.leftLoopBuckNBronco.enable()
                self.game.lamps.leftLoopWildRide.enable()
                self.game.lamps.leftLoopRideEm.enable()
            else:
                pass

    #  _          __ _     ____
    # | |    ___ / _| |_  |  _ \ __ _ _ __ ___  _ __
    # | |   / _ \ |_| __| | |_) / _` | '_ ` _ \| '_ \
    # | |__|  __/  _| |_  |  _ < (_| | | | | | | |_) |
    # |_____\___|_|  \__| |_| \_\__,_|_| |_| |_| .__/
    #                                          |_|
    def left_ramp(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return
        # the left ramp collection of lights
        ## high noon check
        if mode == "highNoon":
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)

        # bionic bart
        elif mode == "Bionic":
            if 1 in self.game.bionic.activeShots:
                self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
                self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
                self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)

        # cva
        elif mode == "CvA":
            if self.game.cva.activeShot == 1:
                self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
                self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
                self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)

        # last call
        elif mode == "lastCall":
            self.game.lamps.leftRampWhiteWater.schedule(0x00FF00FF)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.leftRampJackpot.schedule(0x00FF00FF)

        # drunk multiball
        elif mode == "Drunk":
        ## right ramp is #4 in the stampede jackpot list
            if 'leftRamp' in self.game.drunk_multiball.active:
                self.game.lamps.leftRampJackpot.enable()
                self.game.lamps.leftRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.leftRampWaterfall.schedule(0xFF00FF00)
                self.game.lamps.leftRampWhiteWater.schedule(0xFF00FF00)

        # check for goldmine multiball
        elif mode == "Mine":
            if not self.game.gm_multiball.restartFlag:
            # if drunk multiball is running - check those and update
                if self.game.drunk_multiball.running and 'leftRamp' in self.game.drunk_multiball.active:
                    self.game.lamps.leftRampJackpot.enable()
                    self.game.lamps.leftRampSavePolly.schedule(0xFF00FF00)
                    self.game.lamps.leftRampWaterfall.schedule(0xFF00FF00)
                    self.game.lamps.leftRampWhiteWater.schedule(0xFF00FF00)
                else:
                    if self.game.show_tracking('jackpotStatus',1):
                        self.game.lamps.leftRampJackpot.enable()
                        self.game.lamps.leftRampSavePolly.schedule(0xF0FFF0FF)
                        self.game.lamps.leftRampWaterfall.schedule(0xFF0FFF0F)
                        self.game.lamps.leftRampWhiteWater.schedule(0xFFF0FFF0)

        elif mode == "Stampede":
            if self.game.stampede.active == 1:
                self.game.lamps.leftRampJackpot.schedule(0xF000F000)
                self.game.lamps.leftRampSavePolly.schedule(0x0F000F00)
                self.game.lamps.leftRampWaterfall.schedule(0x00F000F0)
                self.game.lamps.leftRampWhiteWater.schedule(0x000F000F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.leftRampJackpot.schedule(0xFF00FF00)

        # save polly
        elif mode == "Polly":
            # if bank robbery is running - lights are only on if active
            if self.game.bank_robbery.running:
                if not self.game.bank_robbery.isActive[0]:
                    return
            self.game.lamps.leftRampJackpot.enable()
            self.game.lamps.leftRampSavePolly.schedule(0x0FF00FF0)
            self.game.lamps.leftRampWaterfall.schedule(0x00FF00FF)
            self.game.lamps.leftRampWhiteWater.schedule(0xF00FF00F)

        elif mode == "Disable":
            for lamp in self.game.lamps.items_tagged('leftRamp'):
                lamp.disable()

        else:
            stage = self.game.show_tracking('leftRampStage')

            if stage == 1:
                # blink the first light
                self.game.lamps.leftRampWhiteWater.schedule(0x0F0F0F0F)
            elif stage == 2:
                # first light on
                self.game.lamps.leftRampWhiteWater.enable()
                # blink the second
                self.game.lamps.leftRampWaterfall.schedule(0x0F0F0F0F)
            elif stage == 3:
                # first two on
                self.game.lamps.leftRampWhiteWater.enable()
                self.game.lamps.leftRampWaterfall.enable()
                # blink the third
                self.game.lamps.leftRampSavePolly.schedule(0x0F0F0F0F)
            # this is completed - pulse the 3rd light
            elif stage == 5:
                # two on
                self.game.lamps.leftRampWhiteWater.enable()
                self.game.lamps.leftRampWaterfall.enable()
                self.game.lamps.leftRampSavePolly.enable()

    #   ____           _              ____
    #  / ___|___ _ __ | |_ ___ _ __  |  _ \ __ _ _ __ ___  _ __
    # | |   / _ \ '_ \| __/ _ \ '__| | |_) / _` | '_ ` _ \| '_ \
    # | |__|  __/ | | | ||  __/ |    |  _ < (_| | | | | | | |_) |
    #  \____\___|_| |_|\__\___|_|    |_| \_\__,_|_| |_| |_| .__/
    #                                                     |_|
    def center_ramp(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # the center ramp collection of lights
        ## high noon check
        if mode == "highNoon":
            self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
            self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)

        # bionic bart
        elif mode == "Bionic":
            if 2 in self.game.bionic.activeShots:
                self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)

        # cva
        elif mode == "CvA":
            if self.game.cva.activeShot == 2:
                self.game.lamps.centerRampCatchTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.centerRampJackpot.schedule(0x00FF00FF)

        # last call
        elif mode == "lastCall":
            pass

        # drunk multiball
        elif mode == "Drunk":
        ## right ramp is #4 in the stampede jackpot list
            if 'centerRamp' in self.game.drunk_multiball.active:
                self.game.lamps.centerRampJackpot.enable()
                self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.centerRampStopTrain.schedule(0xFF00FF00)
                self.game.lamps.centerRampCatchTrain.schedule(0xFF00FF00)


        # check goldmine active status
        elif mode == "Mine":
            if not self.game.gm_multiball.restartFlag:
            # if drunk multiball is running - check those and update
                if self.game.drunk_multiball.running and 'centerRamp' in self.game.drunk_multiball.active:
                    self.game.lamps.centerRampJackpot.enable()
                    self.game.lamps.centerRampSavePolly.schedule(0xFF00FF00)
                    self.game.lamps.centerRampStopTrain.schedule(0xFF00FF00)
                    self.game.lamps.centerRampCatchTrain.schedule(0xFF00FF00)
                else:
                    if self.game.show_tracking('jackpotStatus',2):
                        self.game.lamps.centerRampJackpot.enable()
                        self.game.lamps.centerRampSavePolly.schedule(0xF0FFF0FF)
                        self.game.lamps.centerRampStopTrain.schedule(0xFF0FFF0F)
                        self.game.lamps.centerRampCatchTrain.schedule(0xFFF0FFF0)

        elif mode == "Stampede":
        ## center ramp is #2 in the stampede jackpot list
            if self.game.stampede.active == 2:
                self.game.lamps.centerRampJackpot.schedule(0xF000F000)
                self.game.lamps.centerRampSavePolly.schedule(0x0F000F00)
                self.game.lamps.centerRampStopTrain.schedule(0x00F000F0)
                self.game.lamps.centerRampCatchTrain.schedule(0x000F000F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.centerRampJackpot.schedule(0xFF00FF00)

        elif mode == "Polly":
            if self.game.river_chase.running:
                self.game.lamps.centerRampJackpot.enable()
                self.game.lamps.centerRampSavePolly.schedule(0x0FF00FF0)
                self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
                self.game.lamps.centerRampCatchTrain.schedule(0xF00FF00F)
            elif self.game.bank_robbery.running:
                if self.game.bank_robbery.isActive[1]:
                    self.game.lamps.centerRampJackpot.enable()
                    self.game.lamps.centerRampSavePolly.schedule(0x0FF00FF0)
                    self.game.lamps.centerRampStopTrain.schedule(0x00FF00FF)
                    self.game.lamps.centerRampCatchTrain.schedule(0xF00FF00F)
            else:
                self.game.lamps.centerRampJackpot.enable()
                self.game.lamps.centerRampSavePolly.schedule(0x00FFFF00)
                self.game.lamps.centerRampStopTrain.schedule(0x0000FFFF)
                self.game.lamps.centerRampCatchTrain.schedule(0xFF0000FF)

        elif mode == "Disable":
            for lamp in self.game.lamps.items_tagged('centerRamp'):
                lamp.disable()

        else:
            stage = self.game.show_tracking('centerRampStage')

            if stage == 1:
                # blink the first light
                self.game.lamps.centerRampCatchTrain.schedule(0x0F0F0F0F)
            elif stage == 2:
                # first light on
                self.game.lamps.centerRampCatchTrain.enable()
                # blink the second
                self.game.lamps.centerRampStopTrain.schedule(0x0F0F0F0F)
            elif stage == 3:
                # first two on
                self.game.lamps.centerRampCatchTrain.enable()
                self.game.lamps.centerRampStopTrain.enable()
                # blink the third
                self.game.lamps.centerRampSavePolly.schedule(0x0F0F0F0F)

            # this is after polly peril - all three on
            elif stage == 5:
            # after polly, before stampede all three stay on
                self.game.lamps.centerRampCatchTrain.enable()
                self.game.lamps.centerRampStopTrain.enable()
                self.game.lamps.centerRampSavePolly.enable()
            else:
                pass

    #  ____  _       _     _     _
    # |  _ \(_) __ _| |__ | |_  | |    ___   ___  _ __
    # | |_) | |/ _` | '_ \| __| | |   / _ \ / _ \| '_ \
    # |  _ <| | (_| | | | | |_  | |__| (_) | (_) | |_) |
    # |_| \_\_|\__, |_| |_|\__| |_____\___/ \___/| .__/
    #          |___/                             |_|
    def right_loop(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return
        # the right loop collection of lights
        ## high noon check
        if mode == "highNoon":
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)

        # bionic bart
        elif mode == "Bionic":
            if 3 in self.game.bionic.activeShots:
                self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
                self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
                self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
                self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)

        # cva
        elif mode == "CvA":
            if self.game.cva.activeShot == 3:
                self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
                self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
                self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
                self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)

        # last call
        elif mode == "lastCall":
            self.game.lamps.rightLoopGoodShot.schedule(0x00FF00FF)
            self.game.lamps.rightLoopGunslinger.schedule(0x00FF00FF)
            self.game.lamps.rightLoopMarksman.schedule(0x00FF00FF)
            self.game.lamps.rightLoopJackpot.schedule(0x00FF00FF)

        # drunk multiball
        elif mode == "Drunk":
            ## right ramp is #4 in the stampede jackpot list
            if 'rightLoop' in self.game.drunk_multiball.active:
                self.game.lamps.rightLoopJackpot.enable()
                self.game.lamps.rightLoopMarksman.schedule(0xFF00FF00)
                self.game.lamps.rightLoopGunslinger.schedule(0xFF00FF00)
                self.game.lamps.rightLoopGoodShot.schedule(0xFF00FF00)

        # goldmine active check
        elif mode == "Mine":
            if not self.game.gm_multiball.restartFlag:
            # if drunk multiball is running - check those and update
                if self.game.drunk_multiball.running and 'rightLoop' in self.game.drunk_multiball.active:
                    self.game.lamps.rightLoopJackpot.enable()
                    self.game.lamps.rightLoopMarksman.schedule(0xFF00FF00)
                    self.game.lamps.rightLoopGunslinger.schedule(0xFF00FF00)
                    self.game.lamps.rightLoopGoodShot.schedule(0xFF00FF00)
                else:
                    if self.game.show_tracking('jackpotStatus',3):
                        self.game.lamps.rightLoopJackpot.enable()
                        self.game.lamps.rightLoopMarksman.schedule(0xF0FFF0FF)
                        self.game.lamps.rightLoopGunslinger.schedule(0xFF0FFF0F)
                        self.game.lamps.rightLoopGoodShot.schedule(0xFFF0FFF0)

        # stampede
        elif mode == "Stampede":
            ## right loop is #3 in the stampede jackpot list
            if self.game.stampede.active == 3:
                self.game.lamps.rightLoopJackpot.schedule(0xF000F000)
                self.game.lamps.rightLoopMarksman.schedule(0x0F000F00)
                self.game.lamps.rightLoopGunslinger.schedule(0x00F000F0)
                self.game.lamps.rightLoopGoodShot.schedule(0x000F000F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.rightLoopJackpot.schedule(0xFF00FF00)

        elif mode == "Disable":
            for lamp in self.game.lamps.items_tagged('rightLoop'):
                lamp.disable()

        else:
            stage = self.game.show_tracking('rightLoopStage')

            if stage == 1:
                # blink the first light
                self.game.lamps.rightLoopGoodShot.schedule(0x0F0F0F0F)
            elif stage == 2:
                # first light on
                self.game.lamps.rightLoopGoodShot.enable()
                # blink the second
                self.game.lamps.rightLoopGunslinger.schedule(0x0F0F0F0F)
            elif stage == 3:
                # first two on
                self.game.lamps.rightLoopGoodShot.enable()
                self.game.lamps.rightLoopGunslinger.enable()
                # blink the third
                self.game.lamps.rightLoopMarksman.schedule(0x0F0F0F0F)
            # this is completed
            elif stage == 4:
                # all three on
                self.game.lamps.rightLoopGoodShot.enable()
                self.game.lamps.rightLoopGunslinger.enable()
                self.game.lamps.rightLoopMarksman.enable()

    #  ____  _       _     _     ____
    # |  _ \(_) __ _| |__ | |_  |  _ \ __ _ _ __ ___  _ __
    # | |_) | |/ _` | '_ \| __| | |_) / _` | '_ ` _ \| '_ \
    # |  _ <| | (_| | | | | |_  |  _ < (_| | | | | | | |_) |
    # |_| \_\_|\__, |_| |_|\__| |_| \_\__,_|_| |_| |_| .__/
    #          |___/                                 |_|
    def right_ramp(self,mode='Base'):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # the right ramp collection of lights
        ## high noon check
        if mode =="highNoon":
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)

        # bionic bart
        elif mode == "Bionic":
            if 4 in self.game.bionic.activeShots:
                self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
                self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
                self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)

        # cva
        elif mode == "CvA":
            if self.game.cva.activeShot == 4:
                self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
                self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
                self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)

        # last call
        elif mode == "lastCall":
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)

        # drunk multiball
        elif mode == "Drunk":
        ## right ramp is #4 in the stampede jackpot list
            if 'rightRamp' in self.game.drunk_multiball.active:
                self.game.lamps.rightRampJackpot.enable()
                self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.rightRampShootOut.schedule(0xFF00FF00)
                self.game.lamps.rightRampSoundAlarm.schedule(0xFF00FF00)

        # goldmine multiball check
        elif mode == "Mine":
            if not self.game.gm_multiball.restartFlag:
            # if drunk multiball is running - check those and update
                if self.game.drunk_multiball.running and 'rightRamp' in self.game.drunk_multiball.active:
                    self.game.lamps.rightRampJackpot.enable()
                    self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
                    self.game.lamps.rightRampShootOut.schedule(0xFF00FF00)
                    self.game.lamps.rightRampSoundAlarm.schedule(0xFF00FF00)
                else:
                    if self.game.show_tracking('jackpotStatus',4):
                        self.game.lamps.rightRampJackpot.enable()
                        self.game.lamps.rightRampSavePolly.schedule(0xF0FFF0FF)
                        self.game.lamps.rightRampShootOut.schedule(0xFF0FFF0F)
                        self.game.lamps.rightRampSoundAlarm.schedule(0xFFF0FFF0)

        elif mode == "Stampede":
        ## right ramp is #4 in the stampede jackpot list
            if self.game.stampede.active == 4:
                self.game.lamps.rightRampJackpot.schedule(0xF000F000)
                self.game.lamps.rightRampSavePolly.schedule(0x0F000F00)
                self.game.lamps.rightRampShootOut.schedule(0x00F000F0)
                self.game.lamps.rightRampSoundAlarm.schedule(0x000F000F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.rightRampJackpot.schedule(0xFF00FF00)

        # save polly
        elif mode == "Polly":
            if self.game.bank_robbery.running:
                if not self.game.bank_robbery.isActive[2]:
                    return
            self.game.lamps.rightRampJackpot.enable()
            self.game.lamps.rightRampSavePolly.schedule(0x0FF00FF0)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)

        elif mode == "Disable":
            for lamp in self.game.lamps.items_tagged('rightRamp'):
                lamp.disable()

        else:
            stage = self.game.show_tracking('rightRampStage')

            if stage == 1:
                # blink the first light
                self.game.lamps.rightRampSoundAlarm.schedule(0x0F0F0F0F)
            elif stage == 2:
                # first light on
                self.game.lamps.rightRampSoundAlarm.enable()
                # blink the second
                self.game.lamps.rightRampShootOut.schedule(0x0F0F0F0F)
            elif stage == 3:
                # first two on
                self.game.lamps.rightRampSoundAlarm.enable()
                self.game.lamps.rightRampShootOut.enable()
                # blink the third
                self.game.lamps.rightRampSavePolly.schedule(0x0F0F0F0F)
            # this is completed - pulse the 3rd light
            elif stage == 5:
                # three on
                self.game.lamps.rightRampSoundAlarm.enable()
                self.game.lamps.rightRampShootOut.enable()
                self.game.lamps.rightRampSavePolly.enable()
            else:
                pass

    #   ____                _
    #  / ___|___  _ __ ___ | |__   ___  ___
    # | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|
    # | |__| (_) | | | | | | |_) | (_) \__ \
    #  \____\___/|_| |_| |_|_.__/ \___/|___/
    #
    def combos(self,mode='Timer'):
        # kill 'em first - they're not in the main shutoff
        for lamp in self.comboLights:
                lamp.disable()
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        if mode == 'Timer':
            # if goldmine is running, don't do this
            if self.game.gm_multiball.running or self.game.gunfight.running or self.game.stampede.running:
                return
            value = self.game.combos.myTimer
            # if timer is greater than 2, slow blink
            if value > 2:
                for myLamp in self.comboLights:
                    myLamp.schedule(0x0000FFFF)
            # if timer is AT 2, speed it up
            elif value == 2:
                for myLamp in self.comboLights:
                    myLamp.schedule(0x00FF00FF)
            # one second left, speed it up even more
            elif value == 1:
                for myLamp in self.comboLights:
                    myLamp.schedule(0x0F0F0F0F)
            else:
                pass

            # high noon check
        elif mode == 'highNoon':
            for i in range(0,5,1):
                self.comboLights[i].schedule(0x00FF00FF)

        # if status is multiball ...
#        elif mode == 'Mine':
#            # loop through and turn on the appropriate lights
#            for i in range(0,5,1):
#                if self.game.show_tracking('jackpotStatus',i):
#                    self.comboLights[i].schedule(0x000F000F)
            ## if status is anything other than ON bail here

        if mode == 'Stampede':
            # loop through and turn on the appropriate light
            for i in range(0,5,1):
                if self.game.stampede.active == i:
                    self.comboLights[i].schedule(0x000F000F)

        else:
            pass

    def disable_combos(self):
        for myLamp in self.comboLights:
            myLamp.disable()


    #  ____            _
    # | __ )  __ _  __| | __ _  ___
    # |  _ \ / _` |/ _` |/ _` |/ _ \
    # | |_) | (_| | (_| | (_| |  __/
    # |____/ \__,_|\__,_|\__, |\___|
    #                    |___/
    def badge(self,mode='Level'):
        self.disable_badge()
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        if mode == 'Level':
            # turn on all the badge lights that have been earned
            for lamp in range(0,5,1):
                if self.game.show_tracking('starStatus',lamp) == True:
                    self.starLamps[lamp].enable()
            if self.game.stampede.running:
                self.starLamps[4].enable()

        elif mode == 'Chase':
            # chase the badge points
            self.game.lamps.starMotherlode.schedule(0xFFE0FFE0)
            self.game.lamps.starCombo.schedule(0xFF07FF07)
            self.game.lamps.starBartBrothers.schedule(0xF83FF83F)
            self.game.lamps.starShowdown.schedule(0x81FF81FF)
            self.game.lamps.starStampede.schedule(0x0FFE0FFE)

        elif mode == 'Flash':
            # flash the full badge
            self.game.lamps.starHighNoon.schedule(0x00FF00FF)
            for lamp in range(0,5,1):
                if self.game.show_tracking('starStatus',lamp) == True:
                    self.starLamps[lamp].schedule(0xFF00FF00)

        elif mode == 'On':
            # turn all the bade lights on
            self.game.lamps.starHighNoon.enable()
            for lamp in range(0,5,1):
                self.starLamps[lamp].enable()
        else:
            pass

    def disable_badge(self):
        for lamp in self.game.lamps.items_tagged('Badge'):
            lamp.disable()


    #  ____             _
    # |  _ \ __ _ _ __ | | __
    # | |_) / _` | '_ \| |/ /
    # |  _ < (_| | | | |   <
    # |_| \_\__,_|_| |_|_|\_\
    #
    def rank_level(self):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        rank = self.game.show_tracking('rank')
        # loop through 0 through current rank and turn the lamps on
        for lamp in range(0,(rank +1),1):
            self.rankLamps[lamp].enable()


    def saloon_flash(self,speed=0):
        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        if speed == 0:
            self.game.lamps.saloonArrow.schedule(0x00FF00FF)
            self.game.lamps.bountySaloon.schedule(0x00FF00FF)
        elif speed == 1:
            self.game.lamps.saloonArrow.schedule(0xF0F0F0F0)
            self.game.lamps.bountySaloon.schedule(0xF0F0F0F0)

    def gunfight_flash(self):
        self.game.lamps.rightGunfightPin.schedule(0x00FF00FF)
        self.game.lamps.leftGunfightPin.schedule(0x00FF00FF)

    #  ____            _    ____
    # | __ )  __ _  __| |  / ___|_   _ _   _ ___
    # |  _ \ / _` |/ _` | | |  _| | | | | | / __|
    # | |_) | (_| | (_| | | |_| | |_| | |_| \__ \
    # |____/ \__,_|\__,_|  \____|\__,_|\__, |___/
    #                                  |___/
    def bad_guys(self):
        # if high noon is running ignore the bad guys
        if self.game.high_noon.running:
            return
        # first disable, they're not in the common wipe
        self.disable_bad_guys()

        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # Then, turn on lights accordingly
        for lamp in range(0,4,1):
            status = self.game.show_tracking('badGuysDead',lamp)
            active = self.game.show_tracking('badGuyUp',lamp)
            # if the guy is dead, his light is on solid - if we're not in high noon or stampede
            if status:
                self.badGuyLamps[lamp].enable()
            # if the guy is active (which he might be also, even if dead, based on mode) flash it
            if active:
                self.badGuyLamps[lamp].schedule(0x00FF00FF)

    def disable_bad_guys(self):
        for lamp in self.badGuyLamps:
            lamp.disable()


    #   ____                          _
    #  | __ )  ___  _ __  _   _ ___  | |    __ _ _ __   ___  ___
    #  |  _ \ / _ \| '_ \| | | / __| | |   / _` | '_ \ / _ \/ __|
    #  | |_) | (_) | | | | |_| \__ \ | |__| (_| | | | |  __/\__ \
    #  |____/ \___/|_| |_|\__,_|___/ |_____\__,_|_| |_|\___||___/
    #
    def bonus_lanes(self,External=True):
        # reset first
        self.disable_bonus_lanes()

        # if lights out party mode is on - bail
        if self.lights_out == True:
            return

        # if it was an external call just to the bonus lanes, make sure they should be on
        if External:
            # skip entirely if MBB is running or cva is running
            if self.game.marshall_multiball.running or self.game.cva.running:
                return
            status = self.game.show_tracking('lampStatus')
            ## if status is off, we bail here
            if status != "ON":
                return

        # bonus lanes
        if self.game.show_tracking('bonusLaneStatus',0) == 'ON':
            self.game.lamps.leftBonusLane.enable()
        if self.game.show_tracking('bonusLaneStatus',1) == 'ON':
            self.game.lamps.rightBonusLane.enable()

    def disable_bonus_lanes(self):
        self.game.lamps.leftBonusLane.disable()
        self.game.lamps.rightBonusLane.disable()


    #
    #  Extra crap
    #

    def feature_lamps_on(self):
        for lamp in self.game.lamps:
            lamp.enable()

    def feature_lamps_off(self):
        for lamp in self.game.lamps:
            if lamp.name == 'startButton':
                pass
            else:
                lamp.disable()


