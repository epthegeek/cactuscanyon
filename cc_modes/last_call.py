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
        self.myID = "Last Call"
        self.backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_simpleBorder.frames[0])
        self.starting = False
        self.ending = False
        self.running = False

    def mode_started(self):
        self.starting = False
        self.ending = False
        self.startValue = 200000
        self.showDub = False
        # reload the basemodes for switch help
        self.game.base.load_modes()
        # kill any extra balls
        self.game.set_tracking('extraBallsPending',0)
        # kill the bozo ball if it was on
        self.game.set_tracking('bozoBall', False)
        self.running = True
        # set up the info layer
        infoLine1 = ep.EP_TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("BEER MUG RAISES JACKPOTS",color=ep.YELLOW)
        infoLine2 = ep.EP_TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SALOON RESETS JACKPOTS",color=ep.ORANGE)
        infoLine3 = ep.EP_TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("CENTER RAMP 2X WHEN LIT",color=ep.MAGENTA)
        self.infoLayer = dmd.ScriptedLayer(128,32,[{'seconds':2,'layer':infoLine1},{'seconds':2,'layer':infoLine2},{'seconds':2,'layer':infoLine3}])
        self.infoLayer.composite_op = "blacksrc"
        self.double = False
        # turn on the GI in case of a 3rd ball tilt
        self.game.gi_control("ON")

    def ball_drained(self):
        # if we get down to one ball or less
        if self.game.trough.num_balls_in_play <= 1:
            # and we're not already in ending mode
            if not self.ending:
                #print "Ending Last call"
                # then turn on ending mode
                self.ending = True
                # cancel the main display updates
                self.cancel_delayed("Display")
                # and call the end of round
                self.end_round()

    # Switches
    def sw_beerMug_active(self,sw):
        if not self.ending:
            # track it, because why not
            self.game.increase_tracking('beerMugHitsTotal')
            # bump up the shotvalue
            self.shotValue += 50000
            # score some points
            self.score(2530)
            # play a sound effect
            self.game.sound.play(self.game.assets.sfx_ricochetSet)
            # play a quote on a random 1/3 choice
            weDo = random.choice([False,True,False])
            if weDo:
                self.game.base.play_quote(self.game.assets.quote_beerMug)
            jackString = "JACKPOTS = " + str(ep.format_score(self.shotValue))
            self.jackpotLine.set_text(jackString)
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
        #print "Saloon hit"
        if not self.ending:
            #print "not ending"
            # cancel the display loop
            self.cancel_delayed("Display")
            # display a thing about jackpots resetting
            anim = self.game.assets.dmd_beerFill
            beerLayer = ep.EP_AnimatedLayer(anim)
            beerLayer.hold = True
            beerLayer.repeat = False
            beerLayer.frame_time = 8
            beerLayer.opaque = True
            textLayer1 = ep.EP_TextLayer(51, 2, self.game.assets.font_9px_az, "center", opaque=False).set_text("ANOTHER",color=ep.RED)
            textLayer2 = ep.EP_TextLayer(51, 12, self.game.assets.font_9px_az, "center", opaque=False).set_text("ROUND",color=ep.RED)
            textLayer3 = ep.EP_TextLayer(51, 24, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("JACKPOTS RESET",blink_frames=8,color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[beerLayer,textLayer1,textLayer2,textLayer3])
            self.layer = combined

            self.game.sound.play(self.game.assets.sfx_pour)

            # reset the value
            self.shotValue = self.startValue
            # kick the ball
            self.game.saloon.kick()
            # back to the main display in 2 seconds
            self.delay("Display",delay=2, handler=self.main_display)
        if self.ending:
            self.game.saloon.kick()

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
            self.showDub = True
        else:
            points = self.shotValue
            self.showDub = False

        self.score(points)

        # play a quote
        self.game.base.priority_quote(self.game.assets.quote_jackpot)
        # flash some lights
        self.game.base.red_flasher_flourish()
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
        if self.showDub:
            double = True
            self.showDub = False
        else:
            double = False
        self.game.sound.play(self.game.assets.sfx_orchestraSpike)
        scoreString = str(ep.format_score(points))
        #print "Score string: " + scoreString
        backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_dmbJackpot.frames[17])
        if double:
            scoreLine1 = ep.EP_TextLayer(64,2, self.game.assets.font_12px_az_outline, "center", opaque=False)
            scoreLine1.composite_op = "blacksrc"
            scoreLine1.set_text("DOUBLE",color=ep.GREEN)
            scoreLine2 = ep.EP_TextLayer(64,15, self.game.assets.font_12px_az_outline, "center",opaque=False)
            scoreLine2.composite_op = "blacksrc"
            scoreLine2.set_text(scoreString,color=ep.GREEN)
            combined = dmd.GroupedLayer(128,32,[backdrop,scoreLine1,scoreLine2])
        else:
            scoreLine = ep.EP_TextLayer(64, 8, self.game.assets.font_15px_az_outline, "center", opaque=False)
            scoreLine.composite_op = "blacksrc"
            scoreLine.set_text(scoreString,color=ep.GREEN)
            combined = dmd.GroupedLayer(128,32,[backdrop,scoreLine])

        self.layer = combined
        self.delay(name="Display",delay=1,handler=self.main_display)

    def sw_centerRampMake_active(self,sw):
        if self.double:
            # it's a double jackpot
            self.jackpot_shot(double=True)
            self.disable_double()
        return game.SwitchStop


    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit()
        return game.SwitchStop

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit()
        return game.SwitchStop

    def sw_bottomJetBumper_active(self,sw):
        self.bumper_hit()
        return game.SwitchStop

    def bumper_hit(self):
        self.score(2530)
        self.game.sound.play(self.game.assets.sfx_punch)

    ## actual mode stuff

    def set_players(self,players):
        self.playerList = players
        self.game.current_player_index = self.playerList[0]
        #print "Last call - player index: " + str(self.game.current_player_index)

    def intro(self):
        # audit
        self.game.game_data['Feature']['Last Call Started'] += 1
        # set a stack level, mostly to kill the inlanes
        self.game.stack_level(6,value=True,lamps=False)
        # play the startup animation
        anim = self.game.assets.dmd_lastCall
        introLayer = ep.EP_AnimatedLayer(anim)
        introLayer.hold = True
        introLayer.frame_time = 8
        introLayer.opaque = False
        introLayer.repeat = False
        introLayer.composite_op = "blacksrc"
        introLayer.add_frame_listener(6, self.game.sound.play,param=self.game.assets.quote_whatThe)
        introLayer.add_frame_listener(14, self.game.sound.play,param=self.game.assets.sfx_glassSmash)
        introLayer.add_frame_listener(19, self.game.sound.play,param=self.game.assets.sfx_pianoRiff)
        textLayer = ep.EP_TextLayer(64, 8, self.game.assets.font_12px_az, "center", opaque=False).set_text("LAST CALL",color=ep.CYAN)
        myWait = (len(anim.frames) / 7.5) + 2
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLayer,introLayer])
        self.layer = combined
        # kick off the music
        self.delay("Operational", delay=myWait, handler=self.start_music)
        # kick off the player start
        self.delay("Operational",delay=myWait,handler=self.start)

    def start_music(self):
        # play the intro
        duration = self.game.sound.play(self.game.assets.music_lastCallIntro)
        # delay the loop start
        self.delay("Operational", delay=duration, handler=self.music_on, param=self.game.assets.music_lastCall)

    def start(self):
        # set the starting flag for the double flipper start
        self.starting = True
        self.shotValue = self.startValue
        # start the actual player
        playerNum = self.playerList[0] + 1
        textLayer1 = ep.EP_TextLayer(64, 3, self.game.assets.font_9px_az, "center", opaque=False)
        textLayer1.set_text("PLAYER " + str(playerNum),blink_frames=10,color=ep.CYAN)
        textLayer2 = ep.EP_TextLayer(64, 15, self.game.assets.font_5px_bold_AZ, "center", opaque=False)
        textLayer2.set_text("PRESS BOTH FLIPPERS",color=ep.GREEN)
        textLayer3 = ep.EP_TextLayer(64, 22, self.game.assets.font_5px_bold_AZ, "center", opaque=False)
        textLayer3.set_text("TO START",color=ep.GREEN)
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLayer1,textLayer2,textLayer3])
        self.layer = combined
        # set a timer to end if nobody hits the flippers
        self.delay("Start Delay",delay=20,handler=self.end)

    def get_going(self):
        # turn off the starting flag, just in case
        self.starting = False
        # Turn on the flippers
        self.game.enable_flippers(enable=True)
        # update the lamps
        self.lamp_update()
        # cancel the start delay
        self.cancel_delayed("Start Delay")
        # launch some balls
        self.game.trough.balls_to_autoplunge = 3
        self.game.trough.launch_balls(3)
        # turn on the main display loop
        self.main_display()

    def main_display(self,loop = True):
        # cancel any display loop - if there is one
        self.cancel_delayed("Display")
        # set up the display during multiball
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = ep.EP_TextLayer(64, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4,color=ep.CYAN)
        scoreLine.composite_op = "blacksrc"

        if self.ending:
            textString = "ENDING LAST CALL"
            infoLine = dmd.TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString)
        else:
            infoLine = self.infoLayer

        # jackpot value line
        jackString = "JACKPOTS = " + str(ep.format_score(self.shotValue))
        if self.ending:
            jackString = "COLLECTING BALLS"
        self.jackpotLine = dmd.TextLayer(128/2,22,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(jackString)

        combined = dmd.GroupedLayer(128,32,[self.backdrop,scoreLine,infoLine,self.jackpotLine])
        self.layer = combined
        # loop back in .2 to update
        if not loop:
            self.delay(name="Display",delay=0.2,handler=self.main_display)

    def end_round(self):
        # turn off the flippers
        self.game.enable_flippers(enable=False)
        # play a cheer
        self.game.sound.play(self.game.assets.sfx_cheers)
        # stop the music - ifwe're out of players
        #self.game.sound.play_music(self.game.assets.music_lastCallEnd,loops=1)
        if not len(self.playerList) > 1:
            self.game.sound.fadeout_music(4000)
        # new line to reset the volume after fade
        self.delay("Fade",delay=6,handler=self.game.interrupter.reset_volume)

        # show the final score display
        textLine1 = ep.EP_TextLayer(64, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("LAST CALL TOTAL:",color=ep.CYAN)
        totalscore = self.game.show_tracking('lastCallTotal')
        textLine2 = ep.EP_TextLayer(64, 15, self.game.assets.font_9px_az, "center", opaque=False).set_text(str(ep.format_score(totalscore)),blink_frames=8,color=ep.GREEN)
        combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,textLine2])
        self.layer = combined
        # turn off the playfield lights
        for lamp in self.game.lamps.items_tagged('Playfield'):
            lamp.disable()

        # wait until all the balls are back in the trough
        self.delay("Operational",delay=3,handler=self.ball_collection)

    def ball_collection(self,tilted=False):
        # set a 20 second ball search delay just in case
        self.delay("Search",delay=20,handler=self.game.ball_search.perform_search)
        # holding pattern until the balls are all back
        if self.game.trough.is_full() or self.game.fakePinProc:
            self.cancel_delayed("Search")
            self.end(tilted)
        else:
            self.delay("Operational",delay=2,handler=self.ball_collection)

    def tilted(self):
        if self.running:
            self.ball_collection(True)

    def end(self,tilted=False):
        if tilted:
            # clear the interrupter layer in case of a tilt
            self.game.interrupter.clear_layer()
            # turn on the GI
            self.game.gi_control("ON")

        # turn off the ending flag
        self.ending = False
        # if there are more than one player, que up the next one
        if len(self.playerList) > 1:
            # if we tilted some things have to get fixed
            if tilted:
                # update the lamps
                self.lamp_update()

            # re-run set players with any players left after the first one
            self.set_players(self.playerList[1:])
            # then call start for the next player
            self.start()
        # if not finish up
        else:
            self.finish_up()

    def finish_up(self):
        self.running = False
        self.game.stack_level(6,value=False,lamps=False)
        textLine1 = ep.EP_TextLayer(64, 4, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("FINAL TOTALS:",color=ep.RED)
        playerCount = len(self.game.players)
        if playerCount == 1:
            playerLine1 = ep.EP_TextLayer(64, 15, self.game.assets.font_7px_az, "center", opaque=False).set_text(str(ep.format_score(self.game.players[0].score)),color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,playerLine1])
        elif playerCount == 2:
            playerLine1 = ep.EP_TextLayer(64, 12, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("1) " + str(ep.format_score(self.game.players[0].score)),color=ep.YELLOW)
            playerLine2 = ep.EP_TextLayer(64, 20, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("2) " + str(ep.format_score(self.game.players[1].score)),color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,playerLine1,playerLine2])
        elif playerCount == 3:
            playerLine1 = ep.EP_TextLayer(4, 12, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("1) " + str(ep.format_score(self.game.players[0].score)),color=ep.YELLOW)
            playerLine2 = ep.EP_TextLayer(4, 20, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("2) " + str(ep.format_score(self.game.players[1].score)),color=ep.YELLOW)
            playerLine3 = ep.EP_TextLayer(68, 12, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("3) " + str(ep.format_score(self.game.players[2].score)),color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,playerLine1,playerLine2,playerLine3])
        else:
            playerLine1 = ep.EP_TextLayer(4, 12, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("1) " + str(ep.format_score(self.game.players[0].score)),color=ep.YELLOW)
            playerLine2 = ep.EP_TextLayer(4, 20, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("2) " + str(ep.format_score(self.game.players[1].score)),color=ep.YELLOW)
            playerLine3 = ep.EP_TextLayer(68, 12, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("3) " + str(ep.format_score(self.game.players[2].score)),color=ep.YELLOW)
            playerLine4 = ep.EP_TextLayer(68, 20, self.game.assets.font_5px_AZ, "left", opaque=False).set_text("4) " + str(ep.format_score(self.game.players[3].score)),color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[self.backdrop,textLine1,playerLine1,playerLine2,playerLine3,playerLine4])


        self.layer = combined
        self.delay("Operational",delay=3,handler=self.shutdown)

    def shutdown(self):
        # kick off the high score entry
        self.game.run_highscore()
        # then unload
        self.unload()

    def mode_stopped(self):
        # clear any remaining delays
        self.wipe_delays()

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
        if not self.game.lamp_control.lights_out:
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