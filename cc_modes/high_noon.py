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
## The High Noon Multiball
##

from procgame import dmd,game
import ep
import random

class HighNoon(ep.EP_Mode):
    """Ooooh no, it's HIIIIIIGH Noon """
    def __init__(self,game,priority):
        super(HighNoon, self).__init__(game,priority)
        self.myID = "High Noon"
        self.gmShots = [self.game.left_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_loop,self.game.right_ramp,self.game.mine]
        # backdrop
        self.backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_highNoonBackdrop.frames[0])

    def mode_started(self):
        self.killed = 0
        self.myTimer = 0
        self.jackpots = 0
        self.grandTotal = 0
        self.hasWon = False
        self.starting = False
        self.timeLeft = 30

    def ball_drained(self):
        if self.running:
        # if a ball drains, we put it back in play as long as the mode is running
            self.empty_trough()
        # if all the balls drain, and we're finishing up, unflag busy
        if self.game.trough.num_balls_in_play <= 0 and self.game.show_tracking('highNoonStatus') == "FINISH":
            self.busy = False

    # jackpot shots
    def sw_leftLoopTop_active(self,sw):
        self.process_shot(0)
        return game.SwitchStop

    def sw_leftRampEnter_active(self, sw):
        self.process_shot(1)
        return game.SwitchStop

    def sw_centerRampMake_active(self, sw):
        self.process_shot(2)
        return game.SwitchStop

    def sw_rightLoopTop_active(self, sw):
        if not self.game.bart.moving:
            self.process_shot(3)
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4)
        return game.SwitchStop

    # timer doesn't start until the ball exits the jets, or the return lane is hit
    def sw_jetBumpersExit_active(self,sw):
        if self.starting:
            self.starting = False
            # delay if starting from the jets to allow the ball to roll down
            self.delay(delay = 1,handler=self.timer,param = self.myTimer)

    def sw_rightReturnLane_active(self,sw):
        if self.starting:
            self.starting = False
            self.timer(self.myTimer)

    def sw_minePopper_active_for_350ms(self,sw):
        if self.running:
            self.game.mountain.kick()
            return game.SwitchStop

    def sw_shooterLane_active_for_1s(self,sw):
        self.game.coils.autoPlunger.pulse(self.game.base.autoplungeStrength)
        return game.SwitchStop

        # jackpot hit
    def process_shot(self,shot):
        # award points
        self.game.score(100000)
        # tick up the counter by one
        self.jackpots += 1
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_jackpot)
        # show an image
        self.cancel_delayed("Display")
        thisOne = random.choice(["A","B","C"])
        if thisOne == "A":
            self.layer = self.game.showcase.punch_out(0.1,isOpaque=True,text="JACKPOT",isTransparent=False,condensed=False,hold=2)
        elif thisOne == "B":
            self.layer = self.game.showcase.blink_fill(2,2,1,3,0.1,isOpaque=True,text="JACKPOT",isTransparent=False,condensed=False)
        else:
            self.layer = self.game.showcase.chase_outline(3,2,1,0.1,isOpaque=True,text="JACKPOT",isTransparent=False,condensed=False,hold=2)
        self.delay("Display",delay=1.5,handler=self.update_display)

    # bad guy targets
    def sw_badGuySW0_active(self,sw):
        # far left bad guy target
        #print "BAD GUY 0 HIT"
        if self.game.show_tracking('badGuyUp',0):
            self.game.bad_guys.target_down(0)
            self.hit_bad_guy(0)
        return game.SwitchStop

    def sw_badGuySW1_active(self,sw):
        # center left badguy target
        #print "BAD GUY 1 HIT"
        if self.game.show_tracking('badGuyUp',1):
            self.game.bad_guys.target_down(1)
            self.hit_bad_guy(1)
        return game.SwitchStop

    def sw_badGuySW2_active(self,sw):
        # center right bad guy target
        #print "BAD GUY 2 HIT"
        if self.game.show_tracking('badGuyUp',2):
            self.game.bad_guys.target_down(2)
            self.hit_bad_guy(2)
        return game.SwitchStop

    def sw_badGuySW3_active(self,sw):
        #print "BAD GUY 3 HIT"
        # far right bad guy target
        if self.game.show_tracking('badGuyUp',3):
            self.game.bad_guys.target_down(3)
            self.hit_bad_guy(3)
        return game.SwitchStop

    # bad guy hit
    def hit_bad_guy(self,target):
        if self.running:
            # tally the hit
            self.killed += 1
            # bad guys currently worth 2.5 mil
            self.game.score(2500000)
            # falsh the flashers
            self.red_flasher_flourish()
            # a sound effect
            self.game.sound.play(self.game.assets.sfx_gunfightShot)
            # a video
            anim = self.game.assets.dmd_dudeShotFullBody
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            # set the position of the dying guy based on target
            if target == 0:
                animLayer.set_target_position(-49,0)
            elif target == 1:
                animLayer.set_target_position(-16,0)
            elif target == 2:
                animLayer.set_target_position(15,0)
            else:
                animLayer.set_target_position(47,0)
            # cancel the current display delay
            self.cancel_delayed("Display")
            self.layer = animLayer
            # then go back to it when the video ends
            self.delay(name="Display",delay=myWait,handler=self.update_display)

            # if that's enough, we're done
            if self.killed >= 20:
                self.won()
            else:
                # pop the target back up
                #print "HIGH NOON: reactivate target " + str(target)
                self.delay(delay=1,handler=self.game.bad_guys.target_up,param=target)

    # todo other switches to trap: mine, saloon, bad guy toy ?

    # timer loop
    def timer(self,seconds):
        # if we're out of time, end
        if seconds <= 0:
            self.timeLeft = seconds
            self.stop_music()
            self.finish_up()
        else:
            seconds -= 1
            self.myTimer = seconds
            self.timeLeft = seconds
            self.delay(name="Timer",delay = 1, handler=self.timer,param=seconds)

    # start high noon
    def start_highNoon(self,step=1):
        if step == 1:
            # audit
            self.game.game_data['Feature']['High Noon Started'] += 1
            # turn off ball search because this takes a while
            self.game.ball_search.disable()
            # kill the music
            self.stop_music()
            # turn off the lights
            self.game.set_tracking('lampStatus', "OFF")
            self.lamp_update()

            self.game.stack_level(6,True)
            self.game.set_tracking('highNoonStatus',"RUNNING")
            self.running = True
            # church bell
            anim = self.game.assets.dmd_bellTower
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            # ding the bell on frame 5
            animLayer.add_frame_listener(5,self.church_bell,param=12)
            self.layer = animLayer
            # loop back to step 2
            self.delay(delay=myWait,handler=self.start_highNoon,param = 2)
        if step == 2:
            # show a 'high noon' banner or animation
            self.banner = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_highNoon.frames[0])
            self.layer = self.banner
            # play the opening quote
            duration = self.game.base.play_quote(self.game.assets.quote_highNoon)
            # after the quote, start the intro
            self.delay(delay=duration,handler=self.intro)


    # intro sequence
    def intro(self,step=1):
        composite = None

        if step == 1 or step == 3 or step == 5 or step == 7 or step == 9:
            # burst wipe the current layer
            anim = self.game.assets.dmd_burstWipe
            myWait = len(anim.frames) / 15.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 4
            animLayer.composite_op = "blacksrc"
            if step == 1:
                duration2 = self.game.sound.play(self.game.assets.music_highNoonLead)
                self.delay(delay=duration2,handler=self.music_on,param=self.game.assets.music_highNoon)

                composite = dmd.GroupedLayer(128,32,[self.banner,animLayer])
            if step == 3:
                composite = dmd.GroupedLayer(128,32,[self.badGuysLayer,animLayer])
            if step == 5:
                composite = dmd.GroupedLayer(128,32,[self.timeLayer,animLayer])
            if step == 7:
                composite = dmd.GroupedLayer(128,32,[self.jackpotLayer,animLayer])
            if step == 9:
                composite = dmd.GroupedLayer(128,32,[self.luckLayer,animLayer])
            self.layer = composite
            self.game.sound.play(self.game.assets.sfx_lightning2)
            # a flourish lampshow
            self.game.lampctrl.play_show(self.game.assets.lamp_highNoonFlash, repeat=False)
            # loop back for step 2
            step += 1
            self.delay(delay=myWait,handler=self.intro,param=step)
        elif step == 2 or step == 4 or step == 6 or step == 8 or step == 10:
            # burst in the next frame
            anim = self.game.assets.dmd_burstWipe2
            myWait = len(anim.frames) / 15.0 + 1.5
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 4
            animLayer.composite_op = "blacksrc"
            if step == 2:
                # set up the badguy layer to expose
                backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_singleCowboySidewaysBorder.frames[0])
                textLayer1 = ep.EP_TextLayer(80, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("SHOOT",color=ep.RED)
                textLayer1.composite_op = "blacksrc"
                textLayer2 = ep.EP_TextLayer(80, 11, self.game.assets.font_9px_az, "center", opaque=False).set_text("20 BAD GUYS",color=ep.RED)
                textLayer3 = ep.EP_TextLayer(80, 21, self.game.assets.font_9px_az, "center", opaque=False).set_text("TO WIN",color=ep.GREEN)
                textLayer3.composite_op = "blacksrc"
                self.badGuysLayer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3])
                # then combine it with the wipe
                composite = dmd.GroupedLayer(128,32,[self.badGuysLayer,animLayer])
            if step == 4:
                # this is the next page to show - time given
                textLayer1 = ep.EP_TextLayer(64, 1, self.game.assets.font_6px_az, "center", opaque=False).set_text("30 SECONDS +",color=ep.YELLOW)
                textLayer2 = ep.EP_TextLayer(64, 8, self.game.assets.font_6px_az, "center", opaque=False)
                kills = self.game.show_tracking('kills')
                textLayer2.set_text(str(kills) + " KILLS =",color=ep.ORANGE)
                # set up the timer while we've got kills hand
                self.myTimer = 30 + kills
                # cap it at 60 seconds
                if self.myTimer > 60:
                    self.myTimer = 60
                textLayer3 = ep.EP_TextLayer(64, 15, self.game.assets.font_12px_az, "center", opaque=False)
                textLayer3.set_text(str(self.myTimer) + " SECONDS",color=ep.GREEN)
                self.timeLayer = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,textLayer3])
                # then combine it with the wipe
                composite = dmd.GroupedLayer(128,32,[self.timeLayer,animLayer])
            if step == 6:
                backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_moneybagBorder.frames[0])
                textLayer1 = ep.EP_TextLayer(80, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("JACKPOTS WORTH",color=ep.ORANGE)
                textLayer2 = ep.EP_TextLayer(80, 13, self.game.assets.font_12px_az, "center", opaque=False).set_text(str(ep.format_score(250000)),color=ep.GREEN)
                self.jackpotLayer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2])
                # combine with burst
                composite = dmd.GroupedLayer(128,32,[self.jackpotLayer,animLayer])
            if step == 8:
                self.luckLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_goodLuck.frames[0])
                composite = dmd.GroupedLayer(128,32,[self.luckLayer,animLayer])
            if step == 10:
                displayLayer = self.display()
                composite = dmd.GroupedLayer(128,32,[displayLayer,animLayer])

            self.layer = composite
            if step <= 9:
                step += 1
                self.delay(delay=myWait,handler=self.intro,param=step)
            elif step == 10:
                #print "SHOULD GET GOING NOW"
                self.delay(delay=myWait,handler=self.get_going)
                # TODO play a quote

    def get_going(self):
        # turn the lights back on
        self.game.set_tracking('lampStatus', "ON")
        # instead of starting the timer, set a flag to start the timer when balls are available
        self.starting = True
        # and the display loop
        self.update_display()
        # kick out the mine ball
        self.game.mountain.kick()
        # put balls in play
        self.empty_trough()
        # flash the bad guy lamps
        for lamp in range(0,4,1):
            self.game.lamp_control.badGuyLamps[lamp].schedule(0x0F0F0F0F)
        # pop up all the bad guys
        self.game.bad_guys.setup_targets()
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_highNoonStart)
        # TODO set all the shots to a status # ?
        # update the lamps
        self.lamp_update()
        # turn the ball search back on
        self.game.ball_search.enable()

    def empty_trough(self):
        # launch more balls
        if self.game.trough.num_balls_in_play != 4:
            thisMany = 4 - self.game.trough.num_balls_in_play
            # launch balls
            self.game.trough.launch_balls(thisMany)

    def update_display(self):
        displayLayer = self.display()
        self.layer = displayLayer
        # loop back every .2 to update the display
        self.delay(name="Display",delay = 0.2, handler = self.update_display)

    def display(self):
        ## this is the main mode display, returns a built layer
        textString1 = str(self.myTimer)
        if self.myTimer > 10:
            timeColor = ep.GREEN
        elif self.myTimer > 5:
            timeColor = ep.YELLOW
        else:
            timeColor = ep.RED
        textLayer1 = ep.EP_TextLayer(105, 4, self.game.assets.font_17px_score, "center", opaque=False).set_text(textString1,color=timeColor)
        remain = 20 - self.killed
        if remain > 10:
            remainColor = ep.RED
        elif remain > 5:
            remainColor = ep.YELLOW
        else:
            remainColor = ep.GREEN
        textString2 = str(remain)
        textLayer2 = ep.EP_TextLayer(24, 4, self.game.assets.font_17px_score, "center", opaque=False).set_text(textString2,color=remainColor)
        display = dmd.GroupedLayer(128,32,[self.backdrop,textLayer1,textLayer2])
        return display

    # won ?
    def won(self):
        # audit
        self.game.game_data['Feature']['High Noon Won'] += 1
        self.hasWon = True
        # cancel the mode timer
        self.cancel_delayed("Timer")
        # set the victory amount
        if self.game.showdown.difficulty == "Hard":
            self.victoryPoints = 20000000
        else:
            self.victoryPoints = 10000000
        self.timeBonus = self.timeLeft * 1000000
        self.game.score(self.timeBonus + self.victoryPoints)
        # cancel the church bell
        self.cancel_delayed("Church Bell")
        # kill the music
        self.stop_music()
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_highNoonWin)
        self.finish_up()

    # finish up
    # collect the balls, display the scores, then end
    def finish_up(self):
        # cancel the main display loop
        self.cancel_delayed("Display")
        # reset the autoplunge, just in case
        self.game.trough.balls_to_autoplunge = 0
        # turn off the local running flag
        self.running = False
        self.game.set_tracking('highNoonStatus',"FINISH")
        # drop the bad guys
        self.game.bad_guys.drop_targets()
        # turn the lights off
        self.game.set_tracking('lampStatus',"OFF")
        self.lamp_update()
        # kill the bad guy lamps?
        for lamp in range(0,4,1):
            self.game.lamp_control.badGuyLamps[lamp].disable()
        # kill the GI
        self.game.gi_control("OFF")
        # lampshow down wipe
        self.game.lampctrl.play_show(self.game.assets.lamp_topToBottom, repeat=False)
        # throw in a 'you won' display
        if self.hasWon:
            # fireworks
            anim = self.game.assets.dmd_fireworks
            myWait = len(anim.frames) / 10.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 6
            # firework sounds keyframed
            animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_fireworks1)
            animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_fireworks2)
            animLayer.add_frame_listener(20,self.game.sound.play,param=self.game.assets.sfx_fireworks3)
            animLayer.composite_op = "blacksrc"
            textLayer1 = ep.EP_TextLayer(64, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("VICTORY",color=ep.GREEN)
            textLayer2 = ep.EP_TextLayer(64, 13, self.game.assets.font_13px_score, "center", opaque=False).set_text(str(ep.format_score(self.victoryPoints + self.timeBonus)),color=ep.ORANGE)
            combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,animLayer])
            self.layer = combined
        else:
            myWait = 3
            textLayer1 = ep.EP_TextLayer(64,4,self.game.assets.font_10px_AZ, "center", opaque=True).set_text("THEY",color=ep.RED)
            textLayer2 = ep.EP_TextLayer(64,18,self.game.assets.font_10px_AZ, "center", opaque=False).set_text("ESCAPED",color=ep.RED)
            combined = dmd.GroupedLayer(128,32,[textLayer1,textLayer2])
            self.layer = combined
        #  turn the flippers off
        self.game.enable_flippers(False)
        # clear the saloon and mine if needed
        if self.game.switches.minePopper.is_active():
            self.game.mountain.kick()
        if self.game.switches.saloonPopper.is_active():
            self.game.saloon.kick()
        # clear the shooter lane if needed
        if self.game.switches.shooterLane.is_active():
            self.game.coils.autoPlunger.pulse(self.game.base.autoplungeStrength)
        if self.hasWon:
            # if we won, the animation is playing, so it may take a while and the balls may drain first
            # so we have to bounce through a helper
            self.delay(delay=myWait+1,handler=self.final_display_pause)
        else:
            # loop through final display which checks for balls on the field
            self.final_display_pause()

    def final_display_pause(self):
        # fakepinproc crutch - I hope
        if self.game.fakePinProc:
            self.game.trough.num_balls_in_play = 0
        # this just calls final display, but checks to see if there are any balls first
        # if there are balls on the field, delay the final display
        if self.game.trough.num_balls_in_play > 0:
            self.busy = True
        self.wait_until_unbusy(self.final_display)

    def final_display(self,step=1):
        # disable ball search
        self.game.ball_search.disable()
        # the tally display after the mode
        #print "HIGH NOON FINAL DISPLAY - STEP " + str(step)
        # jackpots
        if step == 1:
            #print "HIGH NOON JACKPOT TALLY"
            # start the drum roll
            self.music_on(self.game.assets.music_drumRoll)
            myDelay = 0.2
            self.tally(title="JACKPOT",amount=self.jackpots,value=250000,frame_delay=myDelay,callback=self.final_display,step=2)
            musicWait = myDelay * self.jackpots + 1
            # kill the drum roll and play the riff
            self.delay(delay=musicWait,handler=self.game.sound.stop_music)
            self.delay(name="Display",delay=musicWait,handler=self.game.sound.play,param=self.game.assets.sfx_lightning2)
            self.delay(delay=musicWait+0.2,handler=self.game.sound.play,param=self.game.assets.sfx_orchestraBump2)
        # bad guys
        if step == 2:
            #print "HIGH NOON BAD GUY TALLY"
            # start the drum roll
            self.music_on(self.game.assets.music_drumRoll)
            myDelay = 0.2
            self.tally(title="BAD GUY",amount=self.killed,value=500000,frame_delay=myDelay,callback=self.final_display,step=3)
            musicWait = myDelay * self.killed + 1
            # kill the drum roll and play the riff
            self.delay(delay=musicWait,handler=self.game.sound.stop_music)
            self.delay(name="Display",delay=musicWait,handler=self.game.sound.play,param=self.game.assets.sfx_lightning2)
            self.delay(delay=musicWait+0.2,handler=self.game.sound.play,param=self.game.assets.sfx_orchestraSet)

        # total
        if step == 3:
            #print "HIGH NOON TOTAL"
            titleLine = ep.EP_TextLayer(64,3,self.game.assets.font_7px_az, "center", opaque=False).set_text("COMBINED TOTAL:",color=ep.BROWN)
            if self.hasWon:
                self.grandTotal += (self.victoryPoints + self.timeBonus)
            pointsLine = ep.EP_TextLayer(64, 12, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.grandTotal),color=ep.YELLOW)
            combined = dmd.GroupedLayer(128,32,[titleLine,pointsLine])
            # play a sound
            duration = self.game.sound.play(self.game.assets.sfx_orchestraSpike)
            self.delay(delay=duration,handler=self.game.sound.play,param=self.game.assets.sfx_cheers)
            self.layer = combined
            self.delay(name="Display",delay=2,handler=self.end_high_noon)

    def tally(self,title,amount,value,frame_delay,callback,step):
        script = []
        # set the backdrop and offsets
        if title == "JACKPOT":
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_moneybagBorderRight.frames[0])
            x_offset = 50
        elif title == "BAD GUY":
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_singleCowboyBorderRight.frames[0])
            x_offset = 50
        else:
            backdrop = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
            x_offset = 64
        # first just the title
        titleLine = ep.EP_TextLayer(x_offset, 10, self.game.assets.font_12px_az, "center", opaque=False).set_text(title + "S",color=ep.ORANGE)
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine])
        script.append({"layer":combined,"seconds":0.5})
        myWait = 0.5
        # have to define pointsLine and TitleLine just in case it's zero
        titleString = "0 " + title + "S"
        titleLine = ep.EP_TextLayer(x_offset,3,self.game.assets.font_7px_az, "center", opaque=False).set_text(titleString,color=ep.BROWN)
        points = 0
        pointsLine = ep.EP_TextLayer(x_offset, 12, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(points),color=ep.ORANGE)
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,pointsLine])
        script.append({"layer":combined,"seconds":frame_delay})
        # then generate frames for each level of title
        for i in range(1,amount+1,1):
            points = i * value
            if i == 1:
                titleString = "1 " + title
            else:
                titleString = str(i) + " " + title + "S"
            titleLine = ep.EP_TextLayer(x_offset,3,self.game.assets.font_7px_az, "center", opaque=False).set_text(titleString,color=ep.BROWN)
            pointsLine = ep.EP_TextLayer(x_offset, 12, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(points),color=ep.ORANGE)
            combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,pointsLine])
            script.append({"layer":combined,"seconds":frame_delay})
            myWait += frame_delay
            # set a sound for this point at the start of the wipe
        #self.delay(name="Display",delay=myWait,handler=self.game.sound.play,param=self.game.assets.sfx_lightning2)
        # employ the burst wipe
        anim = self.game.assets.dmd_burstWipe
        animWait = len(anim.frames) / 15.0
        myWait += animWait
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 4
        animLayer.composite_op = "blacksrc"
        # add the burst
        burstLayer = dmd.GroupedLayer(128,32,[combined,animLayer])
        script.append({"layer":burstLayer,"seconds":animWait})
        # then a final total with the second half of the wipe
        anim = self.game.assets.dmd_burstWipe2
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 4
        animLayer.composite_op = "blacksrc"
        # set another sound to play after the anim
        myWait += animWait
        #self.delay(name="Display",delay=myWait,handler=self.game.sound.play,param=self.game.assets.sfx_cheers)
        if step == 2:
            preString = "JACKPOTS "
        elif step == 3:
            preString = "BAD GUYS "
        else:
            preString = ""
        titleLine = ep.EP_TextLayer(x_offset,3,self.game.assets.font_7px_az, "center", opaque=False).set_text(preString + "TOTAL:",color=ep.BROWN)
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,pointsLine,animLayer])
        script.append({"layer":combined,"seconds":(animWait + 2)})
        # tack on that extra second
        myWait += 1
        # then set off the layer
        self.layer = dmd.ScriptedLayer(128,32,script)
        # add the points to the grand total
        self.grandTotal += points
        # and delay the comeback for step 2
        #print "TALLY LOOP STEP " + str(step)
        self.delay(name="Display",delay=myWait+1.5,handler=callback,param=step)


    # end high noon
    def end_high_noon(self):
        #print "END HIGH NOON BEGINS"
        # reset the badge
        self.game.badge.reset()
        self.game.lamp_control.badge()
        # clear the stack level
        self.game.stack_level(6,False)
        # turn the flippers back on
        self.game.enable_flippers(True)

        self.update_tracking()

        # turn the lights back on
        self.game.set_tracking('lampStatus',"ON")
        self.lamp_update()
        # launch a ball
        #print "END HIGH NOON BALL LAUNCH"
        self.game.trough.launch_balls(1)
        # load the skillshot
        #print "END HIGH NOON LOAD SKILLSHOT GOES HERE"
        self.game.modes.add(self.game.skill_shot)
        # turn the GI back on
        self.game.gi_control("ON")
        # turn the ball search back on
        self.game.ball_search.enable()
        # unload the mode
        # clear the delays if any
        self.wipe_delays()
        self.unload()

    def update_tracking(self):
        # reset a ton of tracking
        self.game.set_tracking('highNoonStatus',"OPEN")
        # reset all the ramps progress
        self.game.set_tracking('leftRampStatus',1)
        self.game.set_tracking('centerRampStatus',1)
        self.game.set_tracking('rightRampStatus',1)
        self.game.set_tracking('leftLoopStatus',1)
        self.game.set_tracking('rightLoopStatus',1)
        # turn the lights back on
        self.game.set_tracking('lampStatus',"ON")

    def tilted(self):
        if self.running:
            self.update_tracking()
            self.game.badge.reset()
        self.running = False
        self.unload()

    def church_bell(self,rings=12):
        # rin the bell mon
        duration = self.game.sound.play(self.game.assets.sfx_churchBell)
        # flash the red flashers for fabulousness!
        self.game.base.red_flasher_flourish()
        # delay coming back to ring again if there are more left
        rings -= 1
        if rings > 0:
            self.delay("Church Bell",delay=duration,handler=self.church_bell,param=rings)

    def red_flasher_flourish(self,foo='bar'):
        self.game.base.flash(self.game.coils.middleRightFlasher)
        self.delay(delay=0.03,handler=self.game.base.flash,param=self.game.coils.backRightFlasher)
        self.delay(delay=0.06,handler=self.game.base.flash,param=self.game.coils.backLeftFlasher)

