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
import ep

class BallSearch(ep.EP_Mode):
    """Ball Search mode."""
    def __init__(self, game, priority, countdown_time, coils=[], reset_switches=[], stop_switches=[], enable_switch_names=[], special_handler_modes=[]):
        super(BallSearch, self).__init__(game,priority)
        self.myID = "Ball Search"
        self.stop_switches = stop_switches
        self.countdown_time = countdown_time
        self.coils = coils
        self.special_handler_modes = special_handler_modes
        self.enable_switch_names = enable_switch_names
        self.enabled = 0
        self.badGuyCoils = [self.game.coils.badGuyC0,
                      self.game.coils.badGuyC1,
                      self.game.coils.badGuyC2,
                      self.game.coils.badGuyC3]

        #Mode.__init__(self, game, 8)
        for switch in reset_switches:
            self.add_switch_handler(name=str(switch), event_type=str(reset_switches[switch]), delay=None, handler=self.reset)
        # The disable_switch_names identify the switches that, when closed,
        # keep the ball search from occuring.  This is typically done,
        # for instance, when a ball is in the shooter lane or held on a flipper.
        for switch in stop_switches:
            self.add_switch_handler(name=str(switch), event_type=str(stop_switches[switch]), delay=None, handler=self.stop)

    #def sw_trough1_open_for_200ms(self, sw):
    #	if self.game.is_trough_full():
    #		for special_handler_mode in self.special_handler_modes:
    #			special_handler_mode.mode_stopped()
    #		self.stop(0)

    def tilted(self):
        pass

    def enable(self):
        self.enabled = 1
        print "--> BALL SEARCH ENABLED <--"
        self.reset('None')

    def disable(self):
        self.stop(None)
        print "-->> BALL SEARCH DISABLED <<--"
        self.enabled = 0

    def reset(self,sw):
        self.cancel_delayed("stoppedReset")
        if self.enabled:
            # Stop delayed coil activations in case a ball search has
            # already started.
            self.cancel_delayed('search_coils')
            self.cancel_delayed('start_special_handler_modes')
            schedule_search = 1
            for switch in self.stop_switches:

                # Don't restart the search countdown if a ball
                # is resting on a stop_switch.  First,
                # build the appropriate function call into
                # the switch, and then call it using getattr()
                sw = self.game.switches[str(switch)]
                state_str = str(self.stop_switches[switch])
                m = getattr(sw, 'is_%s' % (state_str))
                if m():
                    #print "BALL SEARCH NULL - BALL ON STOP SWITCH"
                    schedule_search = 0
                    #print "Rescheduling a check in 2 seconds"
                    self.delay("stoppedReset",delay=2,handler=self.reset,param="Ding")

            if schedule_search:
                self.cancel_delayed(name='ball_search_countdown')
                #print "BALL SEARCH: Scheduling new countdown"
                self.delay(name='ball_search_countdown', event_type=None, delay=self.countdown_time, handler=self.perform_search, param=0)

    def stop(self,sw):
        #print "Ball Search - Stop Switch"
        self.cancel_delayed(name='ball_search_countdown')
        # delay a reset call - so it will restart after a stop switch
        self.delay("stoppedReset",delay=2,handler=self.reset,param="Ding")

    def perform_search(self, completion_wait_time, completion_handler = None):
        print "DO A BARREL ROLL! - er, BALL SEARCH!"
        # log the search in audits
        self.game.game_data['Feature']['Ball Searches'] += 1

        if (completion_wait_time != 0):
            self.game.set_status("Balls Missing") # Replace with permanent message
        delay = .150
        for coil in self.coils:
            self.delay(name='search_coils', event_type=None, delay=delay, handler=self.pop_coil, param=str(coil))
            delay += .150
        # cycle everything twice
        for coil in self.coils:
            self.delay(name='search_coils', event_type=None, delay=delay, handler=self.pop_coil, param=str(coil))
            delay += .150

        self.delay(name='start_special_handler_modes', event_type=None, delay=delay, handler=self.start_special_handler_modes)

        # shake bart around
        self.game.bart.hardMove()

        # home the mountain
        self.game.mountain.reset_toy(True)

        # move the train
        self.game.train.reset_toy()

        # drop the gunfight posts and pulse
        self.game.coils.leftGunFightPost.disable()
        self.game.coils.leftGunFightPost.pulse()
        self.game.coils.rightGunFightPost.disable()
        self.game.coils.rightGunFightPost.pulse()

        # kill the drop targets - if the game is running and pulse
        for coil in self.badGuyCoils:
            coil.disable()
        delay = .2
        for coil in self.badGuyCoils:
            self.delay(name='search targets',delay=delay,handler=coil.pulse,param=12)
            delay += .2

        if completion_wait_time != 0:
            pass
        else:
            self.cancel_delayed(name='ball_search_countdown')
            self.delay(name='ball_search_countdown', event_type=None, delay=self.countdown_time, handler=self.perform_search, param=0)

    def pop_coil(self,coil):
        self.game.coils[coil].pulse()

    def start_special_handler_modes(self):
        for special_handler_mode in self.special_handler_modes:
            self.game.modes.add(special_handler_mode)
            self.delay(name='remove_special_handler_mode', event_type=None, delay=7, handler=self.remove_special_handler_mode, param=special_handler_mode)

    def remove_special_handler_mode(self,special_handler_mode):
        self.game.modes.remove(special_handler_mode)
