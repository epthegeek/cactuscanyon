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
## This is a heavily modified copy of the trough code from pyprocgame - I added a bunch of "print"s to
## Help me understand what it was doing, and re-worked a bunch of it to make it make more sense
## to me - mostly in the 'checking swtiches' section.  And made changes to deal with balls
## bouncing back in to the trough after launch

#from procgame.game import Mode
import ep

class Trough(ep.EP_Mode):
    """Manages trough by providing the following functionality:

         - Keeps track of the number of balls in play
         - Keeps track of the number of balls in the trough
         - Launches one or more balls on request and calls a launch_callback when complete, if one exists.
         - Auto-launches balls while ball save is active (if linked to a ball save object
         - Identifies when balls drain and calls a registered drain_callback, if one exists.
         - Maintains a count of balls locked in playfield lock features (if externally incremented) and adjusts the count of number of balls in play appropriately.  This will help the drain_callback distinguish between a ball ending or simply a multiball ball draining.

     Parameters:

         'game': Parent game object.
         'position_switchnames': List of switchnames for each ball position in the trough.
         'eject_switchname': Name of switch in the ball position the feeds the shooter lane.
         'eject_coilname': Name of coil used to put a ball into the shooter lane.
         'early_save_switchnames': List of switches that will initiate a ball save before the draining ball reaches the trough (ie. Outlanes).
         'shooter_lane_switchname': Name of the switch in the shooter lane.  This is checked before a new ball is ejected.
         'drain_callback': Optional - Name of method to be called when a ball drains (and isn't saved).
     """
    def __init__(self, game, position_switchnames, eject_switchname, eject_coilname,
                 early_save_switchnames, shooter_lane_switchname, drain_callback=None):
        super(Trough, self).__init__(game, 90)
        self.position_switchnames = position_switchnames
        self.eject_switchname = eject_switchname
        self.eject_coilname = eject_coilname
        self.shooter_lane_switchname = shooter_lane_switchname
        self.drain_callback = drain_callback

        # Install switch handlers.
        # Use a delay of 750ms which should ensure balls are settled.
        for switch in position_switchnames:
            self.add_switch_handler(name=switch, event_type='active', delay=None, handler=self.position_switch_handler)

        for switch in position_switchnames:
            self.add_switch_handler(name=switch, event_type='inactive', delay=None, handler=self.position_switch_handler)

        # Install early ball_save switch handlers.
        for switch in early_save_switchnames:
            self.add_switch_handler(name=switch, event_type='active', delay=None, handler=self.early_save_switch_handler)

        # Reset variables
        self.num_balls_in_play = 0
        self.num_balls_locked = 0
        self.num_balls_to_launch = 0
        self.num_balls_to_stealth_launch = 0
        self.launch_in_progress = False

        self.ball_save_active = False

        #""" Callback called when a ball is saved.  Used optionally only when ball save is enabled (by a call to :meth:`Trough.enable_ball_save`).  Set externally if a callback should be used. """
        self.ball_save_callback = None

        #""" Method to get the number of balls to save.  Set externally when using ball save logic."""
        self.num_balls_to_save = None

        self.launch_callback = None

        self.balls_to_autoplunge = 0

        # set the current total number of balls at start
        self.last_ball_count = self.game.num_balls_total

    #self.debug()

    def debug(self):
        self.game.set_status(str(self.num_balls_in_play) + "," + str(self.num_balls_locked))
        self.delay(name='launch', event_type=None, delay=1.0,handler=self.debug)

    def enable_ball_save(self, enable=True):
        """Used to enable/disable ball save logic."""
        print "SETTING ball_save_active to " + str(enable)
        self.ball_save_active = enable

    def early_save_switch_handler(self, sw):
        if self.ball_save_active:
            # Only do an early ball save if a ball is ready to be launched.
            # Otherwise, let the trough switches take care of it.
            if self.game.switches[self.eject_switchname].is_active():
                self.balls_to_autoplunge += 1
                self.launch_balls(1, self.ball_save_callback,stealth=True)

    def mode_stopped(self):
        self.cancel_delayed('check_switches')

    # Switches will change states a lot as balls roll down the trough.
    # So don't go through all of the logic every time.  Keep resetting a
    # delay function when switches change state.  When they're all settled,
    # the delay will call the real handler (check_switches).
    def position_switch_handler(self, sw):
        self.cancel_delayed('check_switches')
        self.delay(name='check_switches', event_type=None, delay=0.50, handler=self.check_switches)

    def check_switches(self):
        print "CHECKING SWITCHES - Balls in play: " + str(self.num_balls_in_play)
        if self.num_balls_in_play > 0:
            print "THERE'S A BALL IN PLAY"
            # how many balls should the machine have
            num_current_machine_balls = self.game.num_balls_total
            # how many balls in in the trough now
            temp_num_balls = self.num_balls()
            if self.launch_in_progress:
                print "And we're trying to launch another one."
                # check if we had a drain RIGHT while trying to launch
                if temp_num_balls + self.num_balls_in_play == num_current_machine_balls + 1:
                    print "whoa, we're out of whack here"
                    # set the balls in play to zero
                    self.num_balls_in_play = 0
                    # add a ball to launch
                    self.num_balls_to_launch += 1
                    # kill the bounce delay
                    self.cancel_delayed("Bounce Delay")
                    # and launch again
                    self.common_launch_code()
                    return
                # and check for a bounceback
                elif temp_num_balls + self.num_balls_in_play == num_current_machine_balls:
                    print "multiball launch fell back in?"
                    self.cancel_delayed("Bounce Delay")
                    self.common_launch_code()
                    return
            #  Ball saver on situations
            if self.ball_save_active:
                print "BALL SAVE IS ACTIVE"
                if self.num_balls_to_save:
                    num_balls_to_save = self.num_balls_to_save()
                else:
                    num_balls_to_save = 0
                print "TROUGH SAVING " + str(num_balls_to_save) + " BALLS"
                # Calculate how many balls shouldn't be in the
                # trough assuming one just drained
                num_balls_out = num_balls_to_save - 1
                # Translate that to how many balls should be in
                # the trough if one is being saved.
                balls_in_trough = num_current_machine_balls - num_balls_out

                if (temp_num_balls - self.num_balls_to_launch) >= balls_in_trough:
                    print "CHECK SWITCHES THINKS THE BALL WAS SAVED"
                    # tick up the autoplunge
                    self.balls_to_autoplunge += 1
                    self.launch_balls(1, self.ball_save_callback,stealth=True)
                else:
                    # If there are too few balls in the trough.
                    # Ignore this one in an attempt to correct
                    # the tracking.
                    return 'ignore'
            else:
                print "BALL SAVE IS NOT ACTIVE"
                # Calculate how many balls should be in the trough
                # for various conditions.
                # ball ends when all balls are in the trough CC has no playfield locks, so those don't factor in
                num_trough_balls_if_ball_ending = num_current_machine_balls
                # If total number minus one are in the trough - that means the multiball should end, if we're off track, catch that by force
                num_trough_balls_if_multiball_ending = num_trough_balls_if_ball_ending - 1
                # I'm not sure what purpose this one serves, really - from the original trough code
                num_trough_balls_if_multiball_drain = num_trough_balls_if_ball_ending -  (self.num_balls_in_play - 1)

                # The ball should end if all of the balls are in the trough.
                if temp_num_balls == num_current_machine_balls:
                    self.num_balls_in_play = 0
                    if self.drain_callback:
                        print "THE TROUGH IS FULL, BALL SAVE IN ACTIVE, ENDING BALL"
                        self.drain_callback()
                # otherwise there's thinking to do
                else:
                    print "END OF THE TROUGH LINE - ALL OTHER CONDITIONS PASSED"
                    # if the ball count went up ...
                    if self.count_is == "HIGHER":
                        print "THERE ARE MORE BALLS IN THE TROUGH - CALL A DRAIN"
                        if self.drain_callback:
                            # tick the count down one
                            self.num_balls_in_play -= 1
                            # sanity check
                            if self.num_balls_in_play + temp_num_balls > num_current_machine_balls:
                                print "Crap, too many balls accounted for. In play now: " + str(self.num_balls_in_play) + " -- correcting"
                                self.num_balls_in_play = num_current_machine_balls - temp_num_balls
                                print "Balls in play is now: " + str(self.num_balls_in_play)
                            # call a drain
                            self.drain_callback()
                            print "BALLS NOW IN PLAY: " + str(self.num_balls_in_play)
                    # if the ball count hasn't changed ...
                    elif self.count_is == "SAME":
                        print "Trough count stayed the same"
                        print "Counted in trough: " + str(temp_num_balls)
                        print "Balls in play: " + str(self.num_balls_in_play)
                        counted_balls_in_play = num_current_machine_balls - temp_num_balls
                        print "Balls in play should be: " + str(counted_balls_in_play)
                        difference = self.num_balls_in_play - counted_balls_in_play
                        # in this case, we may have caught a launch too close to a drain
                        # if we subtract the number in play, from the number in the trough
                        # and get a number more than 0 there's a correction to do
                        if difference == 0:
                            print "EVERYTHING ADDS UP, GOOD TO GO"
                        elif difference > 0:
                            print "There are more balls in play counted"
                            print "Resetting to counted number"
                            self.launch_balls(difference,stealth=True)
                        elif difference < 0:
                            print "Ball count shows BIP should be higher than it is"
                            self.num_balls_in_play = counted_balls_in_play
                    # if the ball count went down just do a sanity check
                    elif self.count_is == "LOWER":
                        print "THE BALL COUNT IS LOWER"
                        if temp_num_balls + self.num_balls_in_play == num_current_machine_balls:
                            print "EVERYTHING ADDS UP - IGNORING"
                        else:
                            print "Counted in trough: " + str(temp_num_balls)
                            print "Balls in play: " + str(self.num_balls_in_play)
                            counted_balls_in_play = num_current_machine_balls - temp_num_balls
                            print "Balls in play should be: " + str(counted_balls_in_play)
                            difference = self.num_balls_in_play - counted_balls_in_play
                            # in this case, we may have caught a launch too close to a drain
                            # if we subtract the number in play, from the number in the trough
                            # and get a number more than 0 there's a correction to do
                            if difference == 0:
                                print "EVERYTHING ADDS UP, GOOD TO GO"
                            elif difference > 0:
                                print "There are more balls in play counted"
                                print "Resetting to counted number"
                                self.launch_balls(difference,stealth=True)
                            elif difference < 0:
                                print "Ball count shows BIP should be higher than it is"
                                self.num_balls_in_play = counted_balls_in_play
        # if there aren't any balls in play
        else:
            if self.launch_in_progress:
                print "WHAT THE - NO BALLS IN PLAY, and we're launching - try again?"
                # experiental condition for lanny's case where I don't think the balls settled
                if self.num_balls() == 4 or self.game.switches.troughEject.is_active():
                    print "It fell back in, try again"
                    self.cancel_delayed("Bounce Delay")
                    self.common_launch_code()

    # Count the number of balls in the trough by counting active trough switches.
    def num_balls(self):
        """Returns the number of balls in the trough."""
        ball_count = 0
        for switch in self.position_switchnames:
            if self.game.switches[switch].is_active():
                ball_count += 1
                print "Active trough switch: " + str(switch)
        print "balls counted: " + str(ball_count)
        # check if the ball count went up or down
        if ball_count < self.last_ball_count:
            self.count_is = "LOWER"
            print "THE BALL COUNT WENT DOWN"
        elif ball_count == self.last_ball_count:
            self.count_is = "SAME"
            print "THE BALL COUNT STAYED THE SAME"
        else:
            self.count_is = "HIGHER"
            print "THE BALL COUNT WENT UP"
        self.last_ball_count = ball_count
        if self.game.switches.troughEject.is_active():
            print "There's a ball stacked up in the way of the eject opto"
        return ball_count

    def is_full(self):
        print "Checking if trough is full"
        return self.num_balls() == self.game.num_balls_total

    # Either initiate a new launch or add another ball to the count of balls
    # being launched.  Make sure to keep a separate count for stealth launches
    # that should not increase num_balls_in_play.
    def launch_balls(self, num, callback=None, stealth=False):
        """Launches balls into play.

              'num': Number of balls to be launched.
              If ball launches are still pending from a previous request,
              this number will be added to the previously requested number.

              'callback': If specified, the callback will be called once
              all of the requested balls have been launched.

              'stealth': Set to true if the balls being launched should NOT
              be added to the number of balls in play.  For instance, if
              a ball is being locked on the playfield, and a new ball is
              being launched to keep only 1 active ball in play,
              stealth should be used.
          """
        print "I SHOULD LAUNCH A BALL NOW"
        self.num_balls_to_launch += num
        if stealth:
            self.num_balls_to_stealth_launch += num
        if not self.launch_in_progress:
            self.launch_in_progress = True
            if callback:
                self.launch_callback = callback
            self.common_launch_code()

    # This is the part of the ball launch code that repeats for multiple launches.
    def common_launch_code(self):
        # Only kick out another ball if the last ball is gone from the
        # shooter lane.
        if self.game.switches[self.shooter_lane_switchname].is_inactive():
            self.game.coils[self.eject_coilname].pulse(30)
            # go to a hold pattern to wait for the shooter lane
            # if after 2 seconds the shooter lane hasn't been hit we should try again
            if not self.game.fakePinProc:
                self.delay("Bounce Delay",delay=1.5,handler=self.finish_launch)
            # if we are under fakepinproc, proceed immediately to ball in play
            else:
                self.finish_launch()

        # Otherwise, wait 1 second before trying again.
        else:
            self.delay(name='launch', event_type=None, delay=1.0,
                handler=self.common_launch_code)

    def finish_launch(self):
        self.launch_in_progress = False
        # tick down the balls to launch
        self.num_balls_to_launch -= 1
        print "BALL LAUNCHED - left to launch: " +str(self.num_balls_to_launch)
        # Only increment num_balls_in_play if there are no more
        # stealth launches to complete.
        if self.num_balls_to_stealth_launch > 0:
            self.num_balls_to_stealth_launch -= 1
        else:
            self.num_balls_in_play += 1
        print "IN PLAY: " + str(self.num_balls_in_play)
        # If more balls need to be launched, delay 1 second
        if self.num_balls_to_launch > 0:
            print "More balls to launch: " + str(self.num_balls_to_launch) + " - adding delay"
            self.delay(name='launch', event_type=None, delay=2.0,
                handler=self.common_launch_code)
        else:
            if self.launch_callback:
                self.launch_callback()

    def sw_shooterLane_active_for_80ms(self,sw):
        print "SOLID LAUNCH, GOOD TO GO"
        # if we're ejecting - process the launch
        if self.launch_in_progress:
            # kill the fallback loop
            self.cancel_delayed("Bounce Delay")
            self.finish_launch()

