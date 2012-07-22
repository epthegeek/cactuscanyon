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
## The Gold Mine Multiball
##

from procgame import *
import cc_modes
import ep
import random

class GoldMine(ep.EP_Mode):
    """Mining for great justice - For the Gold Mine Multiball, and ... ? """
    def __init__(self,game,priority):
        super(GoldMine, self).__init__(game,priority)
        self.gmShots = [self.game.left_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_loop,self.game.right_ramp,self.game.mine,self.game.combos]

    def mode_started(self):
        self.motherlodeValue = 0
        self.counter = 0
        self.multiplier = False
        # reset the jackpots to false to surpess lights until the mode really starts
        for i in range(0,5,1):
            self.game.set_tracking('jackpotStatus',False,i)

    def ball_drained(self):
    # if we're dropping down to one ball, and goldmine multiball is running - do stuff
        if self.game.trough.num_balls_in_play in (1,0) and self.game.show_tracking('mineStatus') == "RUNNING":
            self.game.base_game_mode.busy = True
            self.end_multiball()

    ### switches
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

    def process_shot(self,shot):
        # we've hit a potential jackpot
        print "JACKPOT STATUS: " + str(self.game.show_tracking('jackpotStatus',shot))
        # check to see if it was an active jackpot
        if self.game.show_tracking('jackpotStatus',shot):
            # if it was, set the flag
            self.game.set_tracking('jackpotStatus',False,shot)
            # and add one to the jackpots collected
            self.game.increase_tracking('jackpotsCollected')
            # and update the lamps for that shot
            self.gmShots[shot].update_lamps()
            # and then award it properly
            self.jackpot_hit()
        # if it wasn't then do something else
        else:
            if shot == 1:
                # left ramp
                self.game.sound.play(self.game.assets.sfx_leftRampEnter)
            elif shot == 2:
                # center ramp
                self.game.sound.play(self.game.assets.sfx_trainWhistle)
            elif shot == 4:
                # right ramp
                self.game.sound.play(self.game.assets.sfx_thrownCoins)
            else:
                pass
            # if a jackpot is already hit, it's just points.
            self.game.score(2530)

    def start_multiball(self):
        # set the stack level flag - since right now only GM Multiball is on stack 2
        self.game.set_tracking('stackLevel',True,2)

        # for now we'll just print a thing
        print "MULTIBALL STARTING"
        # kill the music
        print "start multiball IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # play the multiball intro music
        self.game.base_game_mode.music_on(self.game.assets.music_multiball_intro)
        self.intro_animation()

    def intro_animation(self):
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'multiball-start.dmd')
        # math out how long it is in play time
        myWait = len(anim.frames) / 10.0
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 6
        # TODO add these quotes to assets
        animLayer.add_frame_listener(12,self.game.play_remote_sound,param=self.game.assets.quote_gold)
        animLayer.add_frame_listener(24,self.game.play_remote_sound,param=self.game.assets.quote_mine)
        # turn it on
        self.layer = animLayer
        # when the animation is over go to the next step
        self.delay(delay=myWait,handler=self.intro_banner)

    def intro_banner(self):
        # play the sound
        self.game.sound.play(self.game.assets.quote_multiball)
        # generate a flashing thing
        inverse = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'multiball-banner-inverse.dmd').frames[0])
        normal = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'multiball-banner.dmd').frames[0])
        script = [{'seconds':0.1,'layer':inverse},{'seconds':0.1,'layer':normal}]
        myLayer = dmd.ScriptedLayer(128,32,script)
        self.layer = myLayer

        # show it for a bit - then move on
        self.delay(delay=1.5,handler=self.get_going)

    def get_going(self):
        # kick the ball out of the mine
        self.game.mountain.eject()
        # launch up to 2 more balls
        if self.game.trough.num_balls_in_play < 3:
            total = 3 - self.game.trough.num_balls_in_play
            # turn on the autoplunge
            self.game.autoPlunge = True
            self.game.trough.launch_balls(total)
        # reset the jackpot status to available - just in case
        for i in range(0,5,1):
            self.game.set_tracking('jackpotStatus',True,i)
        # update the lamps
        for shot in self.gmShots:
            shot.update_lamps()
        # kill the intro music and start the multiball music
        self.game.sound.stop_music()
        self.game.base_game_mode.music_on(self.game.assets.music_goldmineMultiball)
        # kick into the MB display
        self.main_display()

    def main_display(self):
        # set up the display during multiball
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'multiball-frame.dmd').frames[0])
        # title line
        titleLine = dmd.TextLayer(128/2, -1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("GOLD MINE MULTIBALL")
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(64, 5, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4)
        scoreLine.composite_op = "blacksrc"
        # motherlode line
        # if no motherlode is lit
        if self.game.show_tracking('motherlodeLit'):
            textString = "MOTHERLODE " + ep.format_score(self.motherlodeValue) + " X " + str(self.game.show_tracking('motherlodeMultiplier'))
        else:
            textString = "JACKPOTS LIGHT MOTHERLODE"

        motherLine = dmd.TextLayer(128/2,16,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString)
        # jackpot value line
        jackString = "JACKPOTS = 500,000"
        jackpotLine = dmd.TextLayer(128/2,22,self.game.assets.font_5px_AZ, "center", opaque=False).set_text(jackString)
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,scoreLine,motherLine,jackpotLine])
        self.layer = combined
        # loop back in .2 to update
        self.delay(name="Display",delay=0.2,handler=self.main_display)

    def jackpot_hit(self,step=1):
        if step == 1:
            # clear the display
            self.abort_display()
            # award the points
            self.game.score(500000)
            # increase the motherlode value
            self.motherlodeValue += 250000
            # see if the multiplier goes up
            self.multiplier = self.check_multiplier()
            # play the animation
            anim = dmd.Animation().load(ep.DMD_PATH+'mine-car-crash.dmd')
            # TODO add the sounds to this and determine if it needs listenrs
            # calcuate the wait time to start the next part of the display
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            self.layer = animLayer
            # play a quote
            self.game.sound.play(self.game.assets.quote_jackpot)
            # loop back to step 2
            self.delay(name="Display",delay=myWait,handler=self.jackpot_hit,param=2)
        if step == 2:
            # grab the last frame of the minecart crash
            backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'mine-car-crash.dmd').frames[9])
            # and setup the text layer to say jackpot
            jackpotLine = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'jackpot.dmd').frames[0])
            # then do the transition
            transition = ep.EP_Transition(self,backdrop,jackpotLine,ep.EP_Transition.TYPE_CROSSFADE)
            # and loop back for step 3
            self.delay(name="Display",delay=.8,handler=self.jackpot_hit,param=3)
        if step == 3:
            # then show 'multiball jackpot' with points
            awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
            awardTextTop.set_text("MULTIBALL JACKPOT")
            awardTextBottom.set_text("500,000",blink_frames=4)
            combined = dmd.GroupedLayer(128,32,[awardTextTop,awardTextBottom])
            self.layer = combined
            # turn on the motherlode if needed
            self.check_motherlode()
            # if multipier went up, we go there, not, it's back to main
            if self.multiplier:
                handler = self.display_multiplier
            else:
                handler = self.main_display
            # go back to the main display
            self.delay(name="Display",delay=1.5,handler=handler)

    def mine_shot(self):
        if self.game.show_tracking('motherlodeLit'):
            # if motherlode is lit, collect it
            self.collect_motherlode()
        else:
            # if no motherlode, score some points and kick the ball out
            self.game.score(2530)
            self.game.mountain.kick()

    def check_motherlode(self):
        # is the motherlode already lit?
        if not self.game.show_tracking('motherlodeLit'):
            # if not, turn some junk on because it should be
            self.game.set_tracking('motherlodeLit',True)
            self.game.mountain.run()
            self.game.mine.update_lamps()
            self.game.sound.play(self.game.assets.quote_motherlodeLit)

    def check_multiplier(self):
        if True not in self.game.show_tracking("jackpotStatus"):
            # if all the jackpots have been hit increase the multiplier
            self.game.increase_tracking('motherlodeMultiplier')
            # and return true to be used to queue the display
            return True
        else:
            return False

    def display_multiplier(self):
            multiplier = self.game.show_tracking('motherlodeMultiplier')
            # and do a display thing
            backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'mine-entrance-border.dmd').frames[0])
            awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
            awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
            awardTextTop.set_text("MOTHERLODE")
            awardTextBottom.set_text(str(multiplier) + "X")
            combined = dmd.GroupedLayer(128,32,[backdrop,awardTextTop,awardTextBottom])
            self.layer = combined
            self.delay(name="Display",delay=1.5,handler=self.main_display)
            # and reset the jackpots
            for i in range(0,5,1):
                self.game.set_tracking('jackpotStatus',True,i)
            # and refresh all the lamps
            for shot in self.gmShots:
                shot.update_lamps()

    def collect_motherlode(self):
        # clear the display
        self.abort_display()
        # turn motherlode off
        self.game.set_tracking('motherlodeLit', False)
        self.game.mountain.stop()
        # add one to the motherlodes collected
        motherlodes = self.game.increase_tracking('motherlodesCollected')
        # and one to the total motherlodes for good measure
        self.game.increase_tracking('motherlodesCollectedTotal')
        myMultiplier = self.game.show_tracking('motherlodeMultiplier')
        # if we've collected 3 regular motherlodes, or any motherload with a multiplier, then light the badge
        if motherlodes >= 3 or myMultiplier > 1:
            # set the star flag for motherlode - it's 0
            self.game.badge.update(0)
        # update the lamps
        self.game.update_lamps()
        # reset a counter
        self.counter = 0
        # play a quote based on the multiplier
        if myMultiplier == 2:
            sound = self.game.assets.quote_doubleMotherlode
        elif myMultiplier == 3:
            sound = self.game.assets.quote_tripleMotherlode
        else:
            sound = self.game.assets.quote_motherlode
        self.game.sound.play(sound)
        # then move on to the display
        self.award_motherlode(myMultiplier)

    def award_motherlode(self,times):
        # tick the counter up
        self.counter += 1
        # tick the times down
        times -= 1
        # setup the display
        awardTextTop = dmd.TextLayer(128/2,5,self.game.assets.font_5px_bold_AZ,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az,justify="center",opaque=False)
        awardTextTop.set_text("MOTHERLODE " + str(self.counter) + "X")
        awardTextBottom.set_text(ep.format_score(self.motherlodeValue * self.counter))
        combined = dmd.GroupedLayer(128,32,[awardTextTop, awardTextBottom])
        self.layer = combined
        # loop through the multiplier again if times is not zero
        if times == 0:
            # award the points
            self.game.score(self.motherlodeValue * self.counter)
            # track highest shot for motherlode champ
            if self.motherlodeValue > self.game.show_tracking('motherlodeValue'):
                self.game.set_tracking('motherlodeValue', self.motherlodeValue)
            # and reset the motherlode value
            self.motherlodeValue = 0
            # then go back to the main display
            self.delay(name="Display",delay=1.5,handler=self.main_display)
            # reset the motherlode multiplier
            self.game.set_tracking('motherlodeMultiplier',1)
            # and kick the ball out
            self.game.mountain.kick()
        else:
            self.delay(delay=1,handler=self.award_motherlode,param=times)

    def end_multiball(self):
        # clear the layer
        self.layer = None
        # kill the motherload just in case
        # turn motherlode off
        self.game.set_tracking('motherlodeLit', False)
        self.game.mountain.stop()
        # reset the motherlode multiplier just in case
        self.game.set_tracking('motherlodeMultiplier',1)
        # set the status to open
        self.game.set_tracking('mineStatus','OPEN')
        print "MULTIBALL ENDED"
        # start the music back up
        if self.game.trough.num_balls_in_play != 0:
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        # unset the busy flag
        self.game.base_game_mode.busy = False
        # set the stack flag back off
        self.game.set_tracking('stackLevel',False,2)
        #refresh the mine lights
        self.game.update_lamps()
        # unload the mode
        self.unload()

    def abort_display(self):
        self.cancel_delayed("Display")
        self.clear_layer()
