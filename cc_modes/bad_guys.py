#   ____           _                ____
#   ____           _                ____
#  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
# | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
# | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
#  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
#                                                   |___/
#           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
#          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
#         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
#          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
#
# A P-ROC Project by Eric Priepke, Copyright 2012-2013
# Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
# Original Cactus Canyon software by Matt Coriale
#
#
#  ____            _    ____
# | __ )  __ _  __| |  / ___|_   _ _   _ ___
# |  _ \ / _` |/ _` | | |  _| | | | | | / __|
# | |_) | (_| | (_| | | |_| | |_| | |_| \__\
# |____/ \__,_|\__,_|  \____|\__,_|\__, |___/
#                                  |___/
# Bad guy Targets and their lamps
#
#  Drop Target info:
#  Left to right - 0,1,2,3
#  Switches = badGuySW#
#     Lamps = badGuyL#
#     Coils = badGuyC#

import ep


class BadGuys(ep.EP_Mode):
    """BadGuys for great justice - covers Quickdraw, Showdown, and ... ? """
    def __init__(self,game,priority):
        super(BadGuys, self).__init__(game, priority)
        self.myID = "Bad Guys"
        self.coils = [self.game.coils.badGuyC0,
                      self.game.coils.badGuyC1,
                      self.game.coils.badGuyC2,
                      self.game.coils.badGuyC3]
        self.knockdown_coils = [self.game.coils.badGuyDown0,
                                self.game.coils.badGuyDown1,
                                self.game.coils.badGuyDown2,
                                self.game.coils.badGuyDown3]
        self.switches = [self.game.switches.badGuySW0,
                         self.game.switches.badGuySW1,
                         self.game.switches.badGuySW2,
                         self.game.switches.badGuySW3]
        self.lamps = [self.game.lamps.badGuyL0,
                      self.game.lamps.badGuyL1,
                      self.game.lamps.badGuyL2,
                      self.game.lamps.badGuyL3]

        self.posts = [self.game.coils.leftGunFightPost,
                      self.game.coils.rightGunFightPost]
        self.shows = [self.game.assets.lamp_target0,
                      self.game.assets.lamp_target1,
                      self.game.assets.lamp_target2,
                      self.game.assets.lamp_target3]
        self.pending = [False, False, False, False]
        self.pending_delay = [None, None, None, None]
        self.on_time = self.game.user_settings['Machine (Standard)']['Drop Target Boost']
        self.smart_drops = self.game.user_settings['Machine (Standard)']['Drop Target Type'] == 'Smart'

    def tilted(self):
        pass

    def ball_drained(self):
        # just in case, drop all the coils when ball ends
        if self.game.trough.num_balls_in_play == 0:
            self.kill_power()

    def mode_stopped(self):
        self.kill_power()

    def sw_badGuySW0_active(self, sw):
        # far left bad guy target
        if self.game.show_tracking('badGuyUp', 0):
            #print "BAD GUY 0 HIT"
            self.hit_bad_guy(0)

    def sw_badGuySW0_inactive_for_200ms(self, sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc and self.pending[0]:
            self.pending[0] = False
            self.target_activate(0)

    def sw_badGuySW1_active(self, sw):
        # center left badguy target
        if self.game.show_tracking('badGuyUp', 1):
            #print "BAD GUY 1 HIT"
            self.hit_bad_guy(1)

    def sw_badGuySW1_inactive_for_200ms(self, sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc and self.pending[1]:
            self.pending[1] = False
            self.target_activate(1)

    def sw_badGuySW2_active(self, sw):
        # center right bad guy target
        if self.game.show_tracking('badGuyUp', 2):
            #print "BAD GUY 2 HIT"
            self.hit_bad_guy(2)

    def sw_badGuySW2_inactive_for_200ms(self, sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc and self.pending[2]:
            self.pending[2] = False
            self.target_activate(2)

    def sw_badGuySW3_active(self, sw):
        # far right bad guy target
        if self.game.show_tracking('badGuyUp',3):
            #print "BAD GUY 3 HIT"
            self.hit_bad_guy(3)

    def sw_badGuySW3_inactive_for_200ms(self, sw):
        # allowance for running in fakepinproc
        if not self.game.fakePinProc and self.pending[3]:
            self.pending[3] = False
            self.target_activate(3)

    def hit_bad_guy(self, target):
        # ding the ball search timer
        self.game.ball_search.reset('None')
        # stop the timer
        # play the target lampshow
        if not self.game.marshall_multiball.running and not self.game.high_noon.running:
            self.game.lampctrl.play_show(self.shows[target], repeat=False, callback=self.lamp_update)
        # kill the coil to the drop target based on position
        self.target_down(target)
        # call back to base to turn on the light for this bad guy?
        self.game.logger.debug("QD STATUS CHECK: " + str(self.game.show_tracking('quickdrawStatus')))
        # If there's a mb tribute running
        if self.game.mb_tribute.running:
            self.game.mb_tribute.hit_drac()
        elif self.game.mm_tribute.running:
            self.game.mm_tribute.hit_troll(target)
        # If there's a quickdraw running
        elif "RUNNING" in self.game.show_tracking('quickdrawStatus'):
            # It's been won
            self.game.quickdraw.won(target)
        # we might be fighting with boss bart
        elif self.game.bart.bossFight:
            #print "FIGHTING BOSS BART - TARGET DIVERTS"
            self.game.bart.boss_target_hit(target)
        # bandits in goldmine
        elif self.game.show_tracking('mineStatus') == "RUNNING":
            self.game.gm_multiball.hit_bandit(target)
        # Otherwise, if all badguys are dead, we're in a showdown
        elif self.game.show_tracking('showdownStatus') == "RUNNING":
            #print "SHOWDOWN RUNNING OMG"
            self.game.showdown.hit(target)
            # showdown stuff would go here
        elif self.game.show_tracking('ambushStatus') == "RUNNING":
            self.game.ambush.hit(target)
        # cva
        elif self.game.show_tracking('cvaStatus') == "RUNNING":
            self.game.cva.hit_alien(target)
        # marshall multiball
        elif self.game.marshall_multiball.running:
            self.game.marshall_multiball.hit_bad_guy(target)
        # option 3 is a gunfight
        else:
            # if the gunfight is still starting up, do nothing
            if self.game.gunfight.starting:
                pass
            else:
                self.game.gunfight.won()

    def target_up(self, target, lamp=True):
        # ignore the light if high noon is running
        if self.game.high_noon.running:
            lamp = False
        self.game.logger.debug("TARGET RAISE ATTEMPT " + str(target))
        self.game.logger.debug(self.game.show_tracking('badGuyUp'))
        
        # Smart drop targets
        if self.smart_drops:
            # do smart drop stuff
            self.coils[target].pulse(25)
        # regular drop targets
        else:
            # Disable the target first
            self.coils[target].disable()
            # new coil raise based on research with on o-scope by jim (jvspin)
            self.game.logger.debug("Target Start " + str(target) + " on time " + str(self.on_time))
            self.coils[target].patter(on_time=2, off_time=2, original_on_time=self.on_time)
        
        if lamp and not self.game.lamp_control.lights_out:
            if self.smart_drops:
                self.lamps[target].enable()
            else:
                self.lamps[target].schedule(0x00FF00FF)
            # set a pending flag for this target
        self.pending[target] = True
        # attempt a re-raise in one second
        self.pending_delay[target] = self.delay(delay=1, handler=self.check_pending, param=target)
        # If fakepinproc is true, activate the target right away
        if self.game.fakePinProc:
            self.target_activate(target)

    def check_pending(self, target):
        # if this target is still pending and the switch is on so the target is down
        if self.pending[target] and self.switches[target].is_active():
            self.game.logger.debug("PENDING CHECK RETRYING TARGET " + str(target))
            self.target_up(target)
        else:
            self.game.logger.debug("TARGET " + str(target) + " PENDING CHECK PASSED")
            pass

    def target_down(self, target, lamp=True):
        if self.game.high_noon.running:
            lamp = False
        # remove the delay
        self.cancel_delayed(self.pending_delay[target])
        self.game.set_tracking('badGuyUp', False, target)
        self.game.logger.debug("DEACTIVATING TARGET " + str(target))
        # new optional smart drop down
        if self.smart_drops:
            # fire the drop coil - if the target is up
            if self.switches[target].is_inactive():
                self.knockdown_coils[target].pulse(25)
        # Original drop code
        else:
            self.coils[target].disable()
        # schedule a check if it went down
        self.cancel_delayed("Target Down")
        self.delay("Target Down", delay=0.2, handler=self.check_target_down, param=target)
        if lamp:
            self.lamps[target].disable()

    def check_target_down(self, target):
        if self.switches[target].is_active():
            # target is down
            self.game.set_tracking('badGuyUp', False, target)
        else:
            # if not, try again
            self.target_down(target)
        
    def target_activate(self, target):
        if not self.game.show_tracking('badGuyUp', target):
            self.game.logger.debug("ACTIVATING TARGET " + str(target))
            # cancel the pending delay
            self.cancel_delayed(self.pending_delay[target])

            # this bit is for orignal drop targets
            if not self.smart_drops:
                # TRYING THIS IN A NEW METHOD
                self.coils[target].patter(on_time=2, off_time=10)

            self.game.set_tracking('badGuyUp', True, target)
            self.game.logger.debug(self.game.show_tracking('badGuyUp'))
        else:
            self.game.logger.debug("SYSTEM THINKS TARGET " + str(target) + " IS ALREADY UP")

    def setup_targets(self):
        # pop up the targets
        delay_time = 0
        for i in range(0, 4, 1):
            self.delay(delay=delay_time, handler=self.target_up, param=i)
            delay_time += 0.25

    def drop_targets(self):
        # drop all teh targets
        for i in range(0, 4, 1):
            # for smart drops only fire knockdown if target is up
            if self.smart_drops:
                if self.switches[i].is_inactive():
                    self.target_down(i)
            else:
                self.target_down(i)

    def kill_power(self):
        # drop all the targets
        self.drop_targets()
        self.wipe_delays()
        for coil in self.posts:
            coil.disable()

    def slay(self):
        # just turn the targets off - for service mode
        for coil in self.coils:
            coil.disable()

    def count_active(self):
        # return the amount of bad guy targets active
        count = 0
        for target in self.game.show_tracking('badGuyUp'):
            if target:
                count += 1
        return count
