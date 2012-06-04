##
## The Gold Mine Multiball
##

from procgame import *
import cc_modes
import ep
import random

class HighNoon(game.Mode):
    """Ooooh no, it's HIIIIIIGH Noon """
    def __init__(self,game,priority):
        super(HighNoon, self).__init__(game,priority)
        self.gmShots = [self.game.left_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_loop,self.game.right_ramp,self.game.mine]
        self.killed = 0
        self.myTimer = 0
        self.jackpots = 0

    def ball_drained(self):
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
        # if a ball drains, we put it back in play as long as the mode is running
            self.empty_trough()
        # if the last ball drains and we're finishing up - show the final display
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('highNoonStatus') == "FINISH":
            self.final_display()

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
        self.process_shot(3)
        return game.SwitchStop

    def sw_rightRampMake_active(self, sw):
        self.process_shot(4)
        return game.SwitchStop

    # jackpot hit
    def process_shot(self,shot):
        # award points
        self.game.score(100000)
        # tick up the counter by one
        self.jackpots += 1

    # bad guy targets
    def sw_badGuySW0_active(self,sw):
        # far left bad guy target
        print "BAD GUY 1 HIT"
        if self.game.show_tracking('badGuyUp',0):
            self.game.bad_guys.target_down(0)
            self.hit_bad_guy(0)
        return game.SwitchStop

    def sw_badGuySW1_active(self,sw):
        # center left badguy target
        print "BAD GUY 2 HIT"
        if self.game.show_tracking('badGuyUp',1):
            self.game.bad_guys.target_down(1)
            self.hit_bad_guy(1)
        return game.SwitchStop

    def sw_badGuySW2_active(self,sw):
        # center right bad guy target
        print "BAD GUY 3 HIT"
        if self.game.show_tracking('badGuyUp',2):
            self.game.bad_guys.target_down(2)
            self.hit_bad_guy(2)
        return game.SwitchStop

    def sw_badGuySW3_active(self,sw):
        print "BAD GUY 4 HIT"
        # far right bad guy target
        if self.game.show_tracking('badGuyUp',3):
            self.game.bad_guys.target_down(3)
            self.hit_bad_guy(3)
        return game.SwitchStop

    # bad guy hit
    def hit_bad_guy(self,target):
        # tally the hit
        self.killed += 1
        # TODO award some points ?
        # if that's enough, we're done
        if self.killed >= 20:
            self.won()
        else:
            # pop the target back up
            self.game.bad_guys.target_up(target)

    # other switches to trap: mine, saloon, bad guy toy ?

    # timer loop
    def timer(self,seconds):
        # if we're out of time, end
        if seconds == 0:
            self.finish_up()
        else:
            seconds -= 1
            self.myTimer = seconds
            self.delay(name="Timer",delay = 1, handler=self.timer,param=seconds)

    # start high noon
    def start_highNoon(self):
        # kill the music
        self.game.sound.stop_music()
        # turn off the lights
        self.game.set_tracking('lampStatus', "OFF")
        self.game.update_lamps()

        self.game.set_tracking('stackLevel',True,3)
        self.game.set_tracking('highNoonStatus',"RUNNING")
        # show a 'high noon' banner or animation
        self.banner = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'high-noon.dmd').frames[0])
        self.layer = self.banner
        # play the opening quote
        duration = self.game.sound.play(self.game.assets.quote_highNoon)
        # after the quote, start the intro
        self.delay(delay=duration,handler=self.intro)


    # intro sequence
    def intro(self,step=1):
        if step == 1 or step == 3 or step == 5 or step == 7 or step == 9:
            # burst wipe the current layer
            anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe.dmd')
            myWait = len(anim.frames) / 12.0
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 5
            animLayer.composite_op = "blacksrc"
            if step == 1:
                duration2 = self.game.sound.play(self.game.assets.music_highNoonLead)
                self.delay(delay=duration2,handler=self.game.base_game_mode.music_on,param=self.game.assets.music_highNoon)

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
            # TODO play a lampshow here
            # loop back for step 2
            step += 1
            self.delay(delay=myWait,handler=self.intro,param=step)
        elif step == 2 or step == 4 or step == 6 or step == 8 or step == 10:
            # burst in the next frame
            anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe-2.dmd')
            myWait = len(anim.frames) / 12.0 + 1.5
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 5
            animLayer.composite_op = "blacksrc"
            if step == 2:
                # set up the badguy layer to expose
                backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'single-cowboy-sideways-border.dmd').frames[0])
                textLayer1 = dmd.TextLayer(80, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("SHOOT")
                textLayer1.composite_op = "blacksrc"
                textLayer2 = dmd.TextLayer(80, 11, self.game.assets.font_9px_az, "center", opaque=False).set_text("20 BAD GUYS")
                textLayer3 = dmd.TextLayer(80, 21, self.game.assets.font_9px_az, "center", opaque=False).set_text("TO WIN")
                textLayer3.composite_op = "blacksrc"
                self.badGuysLayer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2,textLayer3])
                # then combine it with the wipe
                composite = dmd.GroupedLayer(128,32,[self.badGuysLayer,animLayer])
            if step == 4:
                # this is the next page to show - time given
                textLayer1 = dmd.TextLayer(64, 1, self.game.assets.font_6px_az, "center", opaque=False).set_text("30 SECONDS +")
                textLayer2 = dmd.TextLayer(64, 8, self.game.assets.font_6px_az, "center", opaque=False)
                kills = self.game.show_tracking('kills')
                textLayer2.set_text(str(kills) + " BAD GUYS =")
                # set up the timer while we've got kills hand
                self.myTimer = 30 + kills
                textLayer3 = dmd.TextLayer(64, 15, self.game.assets.font_12px_az, "center", opaque=False)
                textLayer3.set_text(str(self.myTimer) + " SECONDS")
                self.timeLayer = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,textLayer3])
                # then combine it with the wipe
                composite = dmd.GroupedLayer(128,32,[self.timeLayer,animLayer])
            if step == 6:
                backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'moneybag-border.dmd').frames[0])
                textLayer1 = dmd.TextLayer(80, 3, self.game.assets.font_9px_az, "center", opaque=False).set_text("JACKPOTS WORTH")
                textLayer2 = dmd.TextLayer(80, 13, self.game.assets.font_12px_az, "center", opaque=False).set_text("100,000")
                self.jackpotLayer = dmd.GroupedLayer(128,32,[backdrop,textLayer1,textLayer2])
                # combine with burst
                composite = dmd.GroupedLayer(128,32,[self.jackpotLayer,animLayer])
            if step == 8:
                self.luckLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'good-luck.dmd').frames[0])
                composite = dmd.GroupedLayer(128,32,[self.luckLayer,animLayer])
            if step == 10:
                displayLayer = self.display()
                composite = dmd.GroupedLayer(128,32,[displayLayer,animLayer])

            self.layer = composite
            if step <= 9:
                step += 1
                self.delay(delay=myWait,handler=self.intro,param=step)
            elif step == 10:
                print "SHOULD GET GOING NOW"
                self.delay(delay=myWait,handler=self.get_going)
                # TODO play a quote

    def get_going(self):
        # turn the lights back on
        self.game.set_tracking('lampStatus', "ON")
        # start the timer
        self.timer(self.myTimer)
        # and the display loop
        self.update_display()
        # kick out the mine ball
        self.game.mountain.kick()
        # put balls in play
        self.empty_trough()
        # pop up all the bad guys
        self.game.bad_guys.setup_targets()
        # TODO set all the shots to a status # ?
        # update the lamps
        self.game.update_lamps()

    def empty_trough(self):
        # launch more balls
        if self.game.trough.num_balls_in_play != 4:
            thisMany = 4 - self.game.trough.num_balls_in_play
            # turn on autoplunge and launch balls
            self.game.autoPlunge = True
            self.game.trough.launch_balls(thisMany)

    def update_display(self):
        displayLayer = self.display()
        self.layer = displayLayer
        # loop back every .2 to update the display
        self.delay(name="Display",delay = 0.2, handler = self.update_display)

    def display(self):
        ## this is the main mode display, returns a built layer
        textLayer1 = dmd.TextLayer(64, 1, self.game.assets.font_7px_az, "center", opaque=False).set_text("HIGH NOON")
        textLayer2 = dmd.TextLayer(64, 9, self.game.assets.font_7px_az, "center", opaque=False)
        textString = str(self.myTimer) + " SECONDS"
        textLayer2.set_text(textString)
        remain = 20 - self.killed
        textString = str(remain) + " BAD GUYS LEFT"
        textLayer3 = dmd.TextLayer(64, 20, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString)
        display = dmd.GroupedLayer(128,32,[textLayer1,textLayer2,textLayer3])
        return display

    # won ?
    def won(self):
        self.game.score(20000000)
        self.finish_up()

    # lost ?

    # finish up
    # collect the balls, display the scores, then end
    def finish_up(self):
        self.game.set_tracking('highNoonStatus',"FINISH")
        # drop the bad guys
        self.game.bad_guys.drop_targets()
        # turn the lights off
        self.game.set_tracking('lampStatus',"OFF")
        self.game.update_lamps()
        # TODO turn the flippers off

    def final_display(self,step=1):
        # the tally display after the mode
        # TODO all the stuff that goes here
        self.end_highNoon()

    # end high noon
    def end_highNoon(self):
        # reset a ton of tracking
        self.game.set_tracking('highNoonStatus',"OPEN")
        self.game.set_tracking('stackLevel',False,3)
        # TODO turn the flippers back on
        # turn the lights back on
        self.game.set_tracking('lampStatus',"ON")
        self.game.update_lamps()
        # launch a ball
        self.game.trough.launch_balls(1)
        # load the skillshot
        self.game.modes.add(self.skill_shot)
        # unload the mode
        self.modes.remove(self.game.high_noon)

    def clear_layer(self):
        self.layer = None