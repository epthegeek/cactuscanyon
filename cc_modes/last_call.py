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
##
## The Last Call Multiball
##

## This multiball is a match award only
## Happens after regular gameplay
## Ends when you get down to one ball.

from procgame import dmd,game
import ep
import random

class LastCall(ep.EP_Mode):
    """Last Call multiball mode ... """
    def __init__(self,game,priority):
        super(LastCall, self).__init__(game,priority)
        self.starting = False
        self.ending = False
        self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_simpleBorder.frames[0])
        self.startValue = 200000

    def mode_started(self):
        # reload the basemodes for switch help
        self.game.base.load_modes()
        self.shotValue = self.startValue
        self.running = True
        # set up the info layer
        infoLine1 = dmd.TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("BEER MUG RAISES JACKPOTS")
        infoLine2 = dmd.TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SALOON RESETS JACKPOTS")
        self.infoLayer = dmd.ScriptedLayer(128,32,[{'seconds':3,'layer':infoLine1},{'seconds':3,'layer':infoLine2}])
        self.infoLayer.composite_op = "blacksrc"



    def ball_drained(self):
        # if we get down to one ball or less
        if self.game.trough.num_balls_in_play <= 1:
            # and we're not already in ending mode
            if not self.ending:
                print "Ending Last call"
                # then turn on ending mode
                self.ending = True
                # and call the end of round
                self.end_round()

    # Switches
    def sw_beerMug_active(self,sw):
        if not self.ending:
            # track it, because why not
            self.game.increase_tracking('beerMugHitsTotal')
            # bump up the shotvalue
            self.shotValue += 100000
            # score some points
            self.score(2530)
            # play a sound effect
            self.game.sound.play(self.game.assets.sfx_ricochetSet)
            # play a quote on a random 1/3 choice
            weDo = random.choice([False,True,False])
            if weDo:
                self.game.base.play_quote(self.game.assets.quote_beerMug)
        return game.SwitchStop

    def sw_topLeftStandUp_active(self, sw):
        self.default_hit()
        return game.SwitchStop

    def sw_bottomLeftStandUp_active(self,sw):
        self.default_hit()
        return game.SwitchStop

    def sw_topRightStandUp_active(self, sw):
        self.default_hit()
        return game.SwitchStop

    def sw_bottomRightStandUp_active(self,sw):
        self.default_hit()
        return game.SwitchStop

    def default_hit(self):
        if not self.ending:
            # play a noise
            self.game.sound.play(self.game.assets.sfx_ricochetSet)
            # score points
            self.score(2530)

    def saloon_hit(self):
        print "Saloon hit"
        if not self.ending:
            print "not ending"
            # cancel the display loop
            self.cancel_delayed("Display")
            # display a thing about jackpots resetting
            anim = self.game.assets.dmd_beerFill
            beerLayer = ep.EP_AnimatedLayer(anim)
            beerLayer.hold = True
            beerLayer.repeat = False
            beerLayer.frame_time = 8
            beerLayer.opaque = True
            textLayer1 = dmd.TextLayer(51, 2, self.game.assets.font_9px_az, "center", opaque=False).set_text("ANOTHER")
            textLayer2 = dmd.TextLayer(51, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("ROUND")
            textLayer3 = dmd.TextLayer(51, 24, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOTS RESET",blink_frames=8)
            combined = dmd.GroupedLayer(128,32,[beerLayer,textLayer1,textLayer2,textLayer3])
            self.layer = combined

            self.game.sound.play(self.game.assets.sfx_pour)

            # reset the value
            self.shotValue = self.startValue
            # kick the ball
            self.game.saloon.kick()
            # back to the main display in 2 seconds
            self.delay("Display",delay=2, handler=self.main_display)

    def sw_leftBonusLane_active(self,sw):
        self.bonus_hit()

    def sw_rightBonusLane_active(self,sw):
        self.bonus_hit()

    def bonus_hit(self):
        self.score(2530)

    def bart_toy_hit(self):
        # just the score & sound default hit
        self.default_hit()

    def sw_jetBumpersExit_active(self,sw):
        self.score(2530)
        return game.SwitchStop

    def sw_leftRampEnter_active(self,sw):
        self.jackpot_shot()
        return game.SwitchStop

    def sw_leftLoopTop_active(self,sw):
        self.jackpot_shot()
        return game.SwitchStop

    def sw_rightLoopTop_active(self,sw):
        self.jackpot_shot()
        return game.SwitchStop

    def sw_rightRampMake_active(self,sw):
        self.jackpot_shot()
        return game.SwitchStop

    def jackpot_shot(self,double = False):
        # score points
        if double:
            points = self.shotValue * 2
        else:
            points = self.shotValue

        self.score(points)

        # play a quote
        self.game.base.priority_quote(self.game.assets.quote_jackpot)
        # do a display
        # load up the animation
        anim = self.game.assets.dmd_beerSlide
        # setup the animated layer
        beerLayer = ep.EP_AnimatedLayer(anim)
        beerLayer.hold=True
        beerLayer.frame_time = 3
        beerLayer.composite_op = "blacksrc"

        anim = self.game.assets.dmd_dmbJackpot
        # setup the animated layer
        wordsLayer = ep.EP_AnimatedLayer(anim)
        wordsLayer.hold=True
        wordsLayer.frame_time = 3
        wordsLayer.composite_op = "blacksrc"

        if self.layer == None:
            self.layer = self.no_layer()

        combined = dmd.GroupedLayer(128,32,[self.layer,wordsLayer,beerLayer])
        self.cancel_delayed("Display")
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_slide)
        self.delay(name="Display",delay=1.5,handler=self.jackpot_score,param=points)
        # enable the double jackpot shot
        self.enable_double()

    def jackpot_score(self,points=0):
        self.game.sound.play(self.game.assets.sfx_orchestraSpike)
        scoreString = str(ep.format_score(points))
        scoreLine = dmd.TextLayer(64, 8, self.game.assets.font_15px_az_outline, "center", opaque=False).set_text(scoreString)
        scoreLine.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dmbJackpot.frames[17])
        combined = dmd.GroupedLayer(128,32,[backdrop,scoreLine])
        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.update_display)

    def sw_centerRampMake_active(self,sw):
        if self.double:
            # it's a double jackpot
            self.jackpot_shot(double=True)
            self.disable_double()
        return game.SwitchStop

    ## actual mode stuff

    def set_players(self,players):
        self.playerList = players
        self.game.current_player_index = self.playerList[0]
        print "Last call - player index: " + str(self.game.current_player_index)

    def intro(self):
        # set a stack level, mostly to kill the inlanes
        self.game.stack_level(6,True)
        # play the startup animation
        anim = self.game.assets.dmd_lastCall
        introLayer = ep.EP_AnimatedLayer(anim)
        introLayer.hold = True
        introLayer.frame_time = 6
        introLayer.opaque = False
        introLayer.repeat = False
        introLayer.composite_op = "blacksrc"
        introLayer.add_frame_listener(5, self.game.sound.play,param=self.game.assets.quote_whatThe)
        introLayer.add_frame_listener(14, self.game.sound.play,param=self.game.assets.sfx_glassSmash)
        introLayer.add_frame_listener(19, self.game.sound.play,param=self.game.assets.sfx_pianoRiff)
        textLayer = dmd.TextLayer(64, 8, self.game.assets.font_12px_az, "center", opaque=False).set_text("LAST CALL")
        myWait = (len(anim.frames) / 10.0) + 2
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLayer,introLayer])
        self.layer = combined
        # kick off the music
        self.delay("Operational",delay=myWait,handler=self.game.base.music_on,param=self.game.assets.music_lastCall)
        # kick off the player start
        self.delay("Operational",delay=myWait,handler=self.start)

    def start(self):
        # set the starting flag for the double flipper start
        self.starting = True
        # start the actual player
        playerNum = self.playerList[0] + 1
        textLayer1 = dmd.TextLayer(64, 3, self.game.assets.font_9px_az, "center", opaque=False)
        textLayer1.set_text("PLAYER " + str(playerNum),blink_frames=10)
        textLayer2 = dmd.TextLayer(64, 15, self.game.assets.font_5px_bold_AZ, "center", opaque=False)
        textLayer2.set_text("PRESS BOTH FLIPPERS")
        textLayer3 = dmd.TextLayer(64, 22, self.game.assets.font_5px_bold_AZ, "center", opaque=False)
        textLayer3.set_text("TO START")
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLayer1,textLayer2,textLayer3])
        self.layer = combined
        # set a timer to end if nobody hits the flippers
        self.delay("Start Delay",delay=20,handler=self.end)

    def get_going(self):
        # turn off the starting flag, just in case
        self.starting = False
        # update the lamps
        self.lamp_update()
        # cancel the start delay
        self.cancel_delayed("Start Delay")
        # launch some balls
        self.game.trough.launch_balls(3)
        # turn on the main display loop
        self.main_display()

    def main_display(self):
        # cancel any display loop - if there is one
        self.cancel_delayed("Display")
        # set up the display during multiball
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(64, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4)
        scoreLine.composite_op = "blacksrc"

        textString = "BEER MUG RAISES JACKPOTS"
        if self.ending:
            textString = "ENDING LAST CALL"
            infoLine = dmd.TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString)
        else:
            infoLine = self.infoLayer

        # jackpot value line
        jackString = "JACKPOTS = " + str(ep.format_score(self.shotValue))
        if self.ending:
            jackString = "COLLECTING BALLS"
        jackpotLine = dmd.TextLayer(128/2,22,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(jackString)

        combined = dmd.GroupedLayer(128,32,[self.backdrop,scoreLine,infoLine,jackpotLine])
        self.layer = combined
        # loop back in .2 to update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    def end_round(self):
        # turn off the flippers
        self.game.enable_flippers(False)
        # show the final score display
        textLine1 = dmd.TextLayer(64, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("LAST CALL TOTAL:")
        totalscore = self.game.show_tracking('lastCallTotal')
        textLine2 = dmd.TextLayer(64, 15, self.game.assets.font_9px_az, "center", opaque=False).set_text(str(ep.format_score(totalscore)),blink_frames=8)
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,textLine2])
        self.layer = combined
        # wait until all the balls are back in the trough
        self.delay("Operational",delay=3,handler=self.ball_collection)

    def ball_collection(self):
        # holding pattern until the balls are all back
        if self.game.trough.is_full():
            self.end()
        else:
            self.delay("Operational",delay=2,handler=self.ball_collection)

    def final_display(self):
        # show the final player score
        pass

    def end(self):
        # turn off the ending flag
        self.ending = False
        # if there are more than one player, que up the next one
        if len(self.playerList) > 1:
            # re-run set players with any players left after the first one
            self.set_players(self.playerList[1:])
            # then call start for the next player
            self.start()
        # if not finish up
        else:
            self.finish_up()

    def finish_up(self):
        self.running = False
        self.game.stack_level(6,False)
        # stop the music
        self.game.sound.stop_music()
        textLine1 = dmd.TextLayer(64, 9, self.game.assets.font_9px_az, "center", opaque=False).set_text("FINAL TOTAL")
        self.layer = dmd.GroupedLayer(128,32,[self.backdrop,textLine1])
        self.delay("Operational",delay=2,handler=self.show_scores)

    def show_scores(self):
        self.layer = None
        self.delay("Operational",delay=3,handler=self.shutdown)

    def shutdown(self):
        # kick off the high score entry
        self.game.run_highscore()
        # then unload
        self.unload()

    def score(self,points):
        # score the points regular style
        self.game.score(points)
        # and then add them to the last call total for high score action
        self.game.increase_tracking('lastCallTotal',points)

    def enable_double(self):
        self.cancel_delayed("Double")
        # turn on theflag
        self.double = True
        # flash thelights
        self.game.lamps.centerRampCatchTrain.schedule(0xF0F0F0F0)
        self.game.lamps.centerRampStopTrain.schedule(0xF0F0F0F0)
        self.game.lamps.centerRampSavePolly.schedule(0xF0F0F0F0)
        self.game.lamps.centerRampJackpot.schedule(0xF0F0F0F0)
        # que the shut off
        self.delay("Double", delay=3,handler=self.disable_double)

    def disable_double(self):
        # turn off the flag
        self.double = False
        # kill the lights
        self.game.lamps.centerRampCatchTrain.disable()
        self.game.lamps.centerRampStopTrain.disable()
        self.game.lamps.centerRampSavePolly.disable()
        self.game.lamps.centerRampJackpot.disable()