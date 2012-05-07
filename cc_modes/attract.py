##
##  This is the Attract mode that runs at start, and ends when a game starts
##  It runs a general display loop and lampshows
##  As well as listening for the start button and flippers
##

from procgame import *
from assets import *
import cc_modes
import ep
import locale

locale.setlocale(locale.LC_ALL, "")

class Attract(game.Mode):
    """Cactus Canyon AttractMode"""
    def __init__(self, game, priority):
        super(Attract, self).__init__(game, priority)

        self.timer = 3
        ## Set up the layers to use
        ballyBanner = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(self.game.assets.dmd_path+'bally-banner.dmd').frames[0])

        presentsText = dmd.TextLayer(128/2, 7, game.assets.font_jazz18, "center", opaque=False).set_text("  PRESENTS")
        gecko = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(game.assets.dmd_path+'gecko-border.dmd').frames[0])
        presents = dmd.GroupedLayer(128, 32, [gecko, presentsText])

        proc_banner = dmd.TextLayer(128/2, 7, game.assets.font_jazz18, "center", opaque=False).set_text("pyprocgame")

        splash = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(game.assets.dmd_path+'cactus-canyon-banner.dmd').frames[0])
        self.myIndex = 0

        # adding a blank layer
        blanker = self.game.score_display.layer

        self.layers = [ {'layer':blanker,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_NORTH},
                        {'layer':ballyBanner,'type':ep.EP_Transition.TYPE_PUSH, 'direction':ep.EP_Transition.PARAM_WEST},
                        {'layer':presents,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_WEST},
                        {'layer':splash,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_WEST},
                        {'layer':proc_banner,'type':ep.EP_Transition.TYPE_CROSSFADE,'direction':False}]

        self.generate_score_frames()


        # run an initial pass on the animation loop
        self.run_animation_loop()
        # then kick off the timer to run it after that
        self.timer_countdown()

    def run_animation_loop(self):
        # grab the current index
        indexA = self.myIndex
        # increment the index for the next round
        if self.myIndex < len(self.layers) - 1:
            self.myIndex += 1
        else:
            self.myIndex = 0
        # and use it to grab the second frame
        indexB = self.myIndex
        frameA = self.layers[indexA]
        frameB = self.layers[indexB]
        # two versions of the transition creation to cover if a direction is needed or not
        if frameB['direction'] != False:
            self.transition = ep.EP_Transition(self,frameA['layer'],frameB['layer'],frameB['type'],frameB['direction'])
        else:
            self.transition = ep.EP_Transition(self,frameA['layer'],frameB['layer'],frameB['type'])

        # reset the timer to 3 for the next go around
        self.timer = 3

    def timer_countdown(self):
        # looping timer to control the animation speed of attract mode
        # can be hurried to the next step by flipper buttons
        self.timer -= 1
        if (self.timer == 0):
            self.run_animation_loop()
            self.delay(name='slideshow_timer', event_type=None, delay=1, handler=self.timer_countdown)
        else:
            self.delay(name='slideshow_timer', event_type=None, delay=1, handler=self.timer_countdown)


    def sw_flipperLwL_active(self,sw):
        self.run_animation_loop()

    def sw_flipperLwR_active(self,sw):
        self.run_animation_loop()

    def mode_topmost(self):
        pass

    def mode_started(self):
        # Blink the start button to notify player about starting a game.
        self.game.lamps.startButton.schedule(schedule=0x00ff00ff, cycle_seconds=0, now=False)
        # Turn on minimal GI lamps
        # Some games don't have controllable GI's (ie Stern games)
        #self.game.lamps.gi01.pulse(0)
        #self.game.lamps.gi02.disable()


    def mode_stopped(self):
        pass

    def mode_tick(self):
        # count down
        pass

    # Enter service mode when the enter button is pushed.
    def sw_enter_active(self, sw):
        for lamp in self.game.lamps:
            lamp.disable()
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_exit_active(self, sw):
        return True

    # Outside of the service mode, up/down control audio volume.
    def sw_down_active(self, sw):
        volume = self.game.sound.volume_down()
        self.game.set_status("Volume Down : " + str(volume))
        return True

    def sw_up_active(self, sw):
        volume = self.game.sound.volume_up()
        self.game.set_status("Volume Up : " + str(volume))
        return True

    # Start button starts a game if the trough is full.  Otherwise it
    # initiates a ball search.
    # This is probably a good place to add logic to detect completely lost balls.
    # Perhaps if the trough isn't full after a few ball search attempts, it logs a ball
    # as lost?

    def sw_startButton_active(self, sw):
        # If the trough is full start a game
        # But we're not runnin the trough yet
        # so I'll just put this stuff here

        self.game.modes.remove(self.game.attract_mode)
        self.game.start_game()
        self.game.add_player()
        self.game.start_ball()
        return True

        #if self.game.trough.is_full:
        # Remove attract mode from mode queue - Necessary?
        #self.game.modes.remove(self)
        # Initialize game
        #self.game.start_game()
        # Add the first player
        #self.game.add_player()
        # Start the ball.  This includes ejecting a ball from the trough.
        #self.game.start_ball()
        #else:

        #self.game.set_status("Ball Search!")
        #self.game.ball_search.perform_search(5)

    def generate_score_frames(self):
        # This big mess generates frames for the attract loop based on high score data.
        # Read the categories
        for category in self.game.highscore_categories:
            for index, score in enumerate(category.scores):
                score_str = locale.format("%d", score.score, True) # Add commas to the score.

                ## Here's where we make some junk
                ## For the standard high scores
                if category.game_data_key == 'ClassicHighScoreData':
                    ## score 1 is the grand champion, gets its own frame
                    if index == 0:
                        title = dmd.TextLayer(128/2, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("GRAND CHAMPION")
                        initLine1 = dmd.TextLayer(5, 13, self.game.assets.font_12px_az, "left", opaque=False).set_text(score.inits)
                        scoreLine1 = dmd.TextLayer(124, 17, self.game.assets.font_7px_bold_az, "right", opaque=False).set_text(score_str)
                        # combine the parts together
                        combined = dmd.GroupedLayer(128, 32, [title, initLine1, scoreLine1])
                        # add it to the stack
                        self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})
                    ## for the second and 4th names set the title and score line 1
                    if index == 1 or index == 3:
                        title = dmd.TextLayer(128/2, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("HIGHEST SCORES")
                        initLine1 = dmd.TextLayer(5, 12, self.game.assets.font_7px_bold_az, "left", opaque=False).set_text(str(index) + ")" + score.inits)
                        scoreLine1 = dmd.TextLayer(124, 12, self.game.assets.font_7px_bold_az, "right", opaque=False).set_text(score_str)
                    ## for the other 2 we ad the second line and make a new layer
                    if index == 2 or index == 4:
                        initLine2 = dmd.TextLayer(5, 21, self.game.assets.font_7px_bold_az, "left", opaque=False).set_text(str(index) + ")" + score.inits)
                        scoreLine2 = dmd.TextLayer(124, 21, self.game.assets.font_7px_bold_az, "right", opaque=False).set_text(score_str)
                        combined = dmd.GroupedLayer(128, 32, [title, initLine1, scoreLine1, initLine2, scoreLine2])
                        # add it to the stack
                        self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_NORTH})

                # generate a screen for the high score champ
                if category.game_data_key == 'QuickDrawChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(self.game.assets.dmd_path+'quick-draw-still.dmd').frames[0])
                    title = dmd.TextLayer(80, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("QUICKDRAW CHAMP")
                    initLine1 = dmd.TextLayer(80, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(80, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " KILLS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})