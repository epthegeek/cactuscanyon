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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
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
import random

locale.setlocale(locale.LC_ALL, "")

class Attract(ep.EP_Mode):
    """Cactus Canyon AttractMode"""
    def __init__(self, game, priority):
        super(Attract, self).__init__(game, priority)
        self.timer = 3
        self.NOISY_COUNT = self.game.user_settings['Gameplay (Feature)']['Number of attract sounds to play']
        self.NOISY_DELAY = self.game.user_settings['Gameplay (Feature)']['Attract sound delay time']

    def mode_started(self):

        ## Set up the layers to use
        ballyBanner = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_ballyBanner.frames[0])

        textLayer1 = dmd.TextLayer(76, 5, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("ORIGINALLY")
        textLayer1.composite_op = "blacksrc"
        textLayer2 = dmd.TextLayer(76, 18, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("BY")
        textLayer2.composite_op = "blacksrc"
        leftGecko = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_geckoBorderLeft.frames[0])
        original = dmd.GroupedLayer(128, 32, [leftGecko, textLayer1,textLayer2])

        textLayer1 = dmd.TextLayer(58, 5, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("CONTINUED")
        textLayer1.composite_op = "blacksrc"
        textLayer2 = dmd.TextLayer(58, 18, self.game.assets.font_10px_AZ, "center", opaque=False).set_text("WITH")
        textLayer2.composite_op = "blacksrc"
        rightGecko = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_geckoBorderRight.frames[0])
        expanded = dmd.GroupedLayer(128, 32, [rightGecko, textLayer1,textLayer2])

        proc_banner = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_procBanner.frames[0])

        self.splash = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_ccBanner.frames[0])
        continuedBanner = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_cccBanner.frames[0])
        self.myIndex = 0


        # adding a blank layer
        blanker = self.game.score_display.layer


        self.layers = [ {'layer':blanker,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_NORTH},
                        {'layer':self.splash,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_WEST},
                        #{'layer':continuedBanner,'type':ep.EP_Transition.TYPE_WIPE,'direction':ep.EP_Transition.PARAM_EAST},
                        {'layer':continuedBanner,'type':"NONE",'direction':"DERP"},
                        {'layer':original,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_EAST},
                        {'layer':ballyBanner,'type':ep.EP_Transition.TYPE_CROSSFADE, 'direction':False},
                        {'layer':expanded,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_WEST},
                        {'layer':proc_banner,'type':ep.EP_Transition.TYPE_CROSSFADE,'direction':False}]

        self.generate_score_frames()

        # add a game over at the end
        gameOver = ep.EP_Showcase().make_thin_string(3,text="GAME OVER")
        self.layers.append({'layer':gameOver,'type':ep.EP_Transition.TYPE_CROSSFADE,'direction':False})

        # Blink the start button to notify player about starting a game.
        self.game.lamps.startButton.schedule(schedule=0x00ff00ff, cycle_seconds=0, now=False)

        # Turn on the GIs
        self.game.gi_control("ON")

        # flag for if the flippers should make noise or not
        self.noisy = True
        # number of sounds played
        self.soundCount = 0



        ## lampshows for attract mode
        lampshows = [
            self.game.assets.lamp_topToBottom,
            self.game.assets.lamp_bottomToTop,
            self.game.assets.lamp_topToBottom,
            self.game.assets.lamp_bottomToTop,
            self.game.assets.lamp_fanRight,
            self.game.assets.lamp_fanLeft,
            self.game.assets.lamp_fanRight,
            self.game.assets.lamp_fanLeft,
            self.game.assets.lamp_colors,
            self.game.assets.lamp_colors,
            self.game.assets.lamp_rightToLeft,
            self.game.assets.lamp_leftToRight,
            self.game.assets.lamp_rightToLeft,
            self.game.assets.lamp_leftToRight,
            self.game.assets.lamp_starShots,
            self.game.assets.lamp_starShots,
            self.game.assets.lamp_starShots,
        ]
        self.game.schedule_lampshows(lampshows,True)

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

        # new type for the rolling weed animation
        if frameB['type'] == "NONE":
            # tumble weed wipe bits
            anim = self.game.assets.dmd_tumbleweedAttract
            weedFront = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=4)
            weedFront.composite_op = "blacksrc"
            weedBack = self.splash
            tumbleweedWipe = dmd.GroupedLayer(128,32,[weedBack,weedFront])
            weedWait = len(anim.frames) / 15.0
            self.layer = tumbleweedWipe
            self.game.sound.play(self.game.assets.sfx_tumbleWind)
        # two versions of the transition creation to cover if a direction is needed or not
        elif frameB['direction'] != False:
            self.transition = ep.EP_Transition(self,frameA['layer'],frameB['layer'],frameB['type'],frameB['direction'])
        else:
            self.transition = ep.EP_Transition(self,frameA['layer'],frameB['layer'],frameB['type'])

        # reset the timer to 3 for the next go around
        self.timer = 3

    def timer_countdown(self):
        # looping timer to control the animation speed of attract mode
        # can be hurried to the next step by flipper buttons
        self.timer -= 1
        #print "ATTRACT TIMER: " + str(self.timer)
        if (self.timer == 0):
            self.run_animation_loop()
        # come back to the timer - after cancelling any existing delay, just to be sure
        self.cancel_delayed('slideshow_timer')
        self.delay(name='slideshow_timer', event_type=None, delay=1, handler=self.timer_countdown)


    def sw_flipperLwL_active(self,sw):
        # if going left - bump the index down
        self.myIndex -= 2
        self.flipper_action()

    def sw_flipperLwR_active(self,sw):
        self.flipper_action()

    def flipper_action(self):
        # page the attract animation
        self.run_animation_loop()
        # if noisy, play a noise and count it
        if self.noisy:
            # play a sound
            self.play_random()
            # increment the count
            self.soundCount += 1
            print "SOUND COUNT: " + str(self.soundCount) + " OF " + str(self.NOISY_COUNT)
            # check if we're done now
            if self.soundCount >= self.NOISY_COUNT:
                # turn the noisy flag off
                self.noisy = False
                # reset the sound count
                self.soundCount = 0
                # delay a re-enable
                self.delay("Noisy",delay=self.NOISY_DELAY,handler=self.noisy_again)

    def noisy_again(self):
        self.noisy = True

    # random sound routine
    def play_random(self,loops=0, max_time=0, fade_ms=0):
        """ """
        if not self.game.sound.enabled: return
        # pick a random key
        key = random.choice(self.game.sound.sounds.keys())
        if len(self.game.sound.sounds[key]) > 0:
            random.shuffle(self.game.sound.sounds[key])
        self.game.sound.sounds[key][0].play(loops,max_time,fade_ms)
        return self.game.sound.sounds[key][0].get_length()

    def mode_topmost(self):
        pass

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
        return True

    def sw_up_active(self, sw):
        volume = self.game.sound.volume_up()
        return True

    # Start button starts a game if the trough is full.  Otherwise it
    # initiates a ball search.
    # This is probably a good place to add logic to detect completely lost balls.
    # Perhaps if the trough isn't full after a few ball search attempts, it logs a ball
    # as lost?

    def sw_startButton_active(self, sw):
        # If the trough is full start a game - if the end of game delay isn't active
        if not self.game.endBusy:
            if self.game.trough.is_full() or self.game.switches.shooterLane.is_active():
                # kill the lampshow
                self.game.lampctrl.stop_show()
                # kill the music in case the 'end of game' song is playing
                self.game.sound.stop_music()
                # Initialize game
                self.game.start_game()
            else:
                print "BALL SEARCH"
                self.game.ball_search.perform_search(1)

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

                # generate screens for marshall multiball
                if category.game_data_key == 'MarshallHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False,frame=self.game.assets.dmd_marshallHighScoreFrame.frames[0])
                    text = str(index+1) + ") " + score.inits + " " + score_str
                    initsLine = dmd.TextLayer(64,22,self.game.assets.font_7px_az,"center",opaque=False).set_text(text)
                    scoreLine = dmd.TextLayer(64,14,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("OLD TIME PINBALL")
                    combined = dmd.GroupedLayer(128,32,[backdrop,initsLine,scoreLine])
                    # add it to the stack
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_WIPE,'direction':ep.EP_Transition.PARAM_EAST})

                # generate a screen for the quickdraw high score champ
                if category.game_data_key == 'QuickdrawChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_quickdrawStill.frames[0])
                    title = dmd.TextLayer(80, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("QUICKDRAW CHAMP")
                    initLine1 = dmd.TextLayer(80, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(80, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " KILLS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the showdown champ
                if category.game_data_key == 'ShowdownChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShotFullBody.frames[0])
                    backdrop.set_target_position(40,0)
                    title = dmd.TextLayer(44, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("SHOWDOWN CHAMP")
                    initLine1 = dmd.TextLayer(44, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(44, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " KILLS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the ambush champ
                if category.game_data_key == 'AmbushChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dudeShoots.frames[1])
                    backdrop.set_target_position(-49,0)
                    title = dmd.TextLayer(80, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("AMBUSH CHAMP")
                    initLine1 = dmd.TextLayer(80, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(80, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " KILLS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the Tumbleweed Rustler
                if category.game_data_key == 'TumbleweedChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_tumbleweedLeft.frames[7])
                    backdrop.set_target_position(32,0)
                    title = dmd.TextLayer(51, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("TUMBLEWEED RUSTLER")
                    initLine1 = dmd.TextLayer(44, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(44, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " WEEDS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop,title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the Town Drunk
                if category.game_data_key == 'TownDrunkHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dmbIdle.frames[1])
                    title = dmd.TextLayer(80, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("TOWN DRUNK")
                    initLine1 = dmd.TextLayer(80, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(80, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " BEERS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the Town Drunk
                if category.game_data_key == 'UndertakerHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_tombstone.frames[0])
                    title = dmd.TextLayer(44, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("UNDERTAKER")
                    initLine1 = dmd.TextLayer(44, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(44, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " KILLS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the Bounty Hunter
                if category.game_data_key == 'BountyHunterHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_wantedPoster.frames[0])
                    title = dmd.TextLayer(64, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("BOUNTY HUNTER")
                    initLine1 = dmd.TextLayer(44, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(44, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + " BARTS")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the Combo Champ
                if category.game_data_key == 'ComboChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_starsBorder.frames[0])
                    title = dmd.TextLayer(64, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("COMBO CHAMP")
                    initLine1 = dmd.TextLayer(64, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(64, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str + "-WAY COMBO")
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

                # Generate a screen for the motherlode champ
                if category.game_data_key == 'MotherlodeChampHighScoreData':
                    backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_multiballFrame.frames[0])
                    title = dmd.TextLayer(64, 2, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text("MOTHERLODE CHAMP")
                    initLine1 = dmd.TextLayer(64, 7, self.game.assets.font_12px_az, "center", opaque=False).set_text(score.inits)
                    scoreLine1 = dmd.TextLayer(64, 22, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text(score_str)
                    combined = dmd.GroupedLayer(128, 32, [backdrop, title, initLine1, scoreLine1])
                    self.layers.append({'layer':combined,'type':ep.EP_Transition.TYPE_PUSH,'direction':ep.EP_Transition.PARAM_SOUTH})

    def mode_stopped(self):
        print "DELETING ATTRACT DELAYS"
        self.dispatch_delayed()
