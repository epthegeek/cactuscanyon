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
###
###   ___        _      _       _
###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      __
### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / /
### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /
###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/
###

from procgame import dmd
import ep
import random

class Quickdraw(ep.EP_Mode):
    """Quickdraw code """
    def __init__(self,game,priority):
        super(Quickdraw, self).__init__(game,priority)
        self.myID = "QuickDraw"
        # default
        self.side = 0
        self.target = 0
        # build the pause view
        script = []
        # set up the text layer
        textString = "< QUICKDRAW PAUSED >"
        textLayer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"

    def mode_started(self):
        self.paused = False
        self.running = True

    def ball_drained(self):
        # the the ball drains, quickdraw is lost
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('quickdrawStatus',self.side) == "RUNNING":
            self.lost(self.target)

    # switches

    def sw_leftBonusLane_active(self,sw):
        if not self.paused:
            self.pause()

    def sw_rightBonusLane_active(self,sw):
        if not self.paused:
            self.pause()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
        self.bumper_hit('bottom')

    # so does the mine
    def sw_minePopper_active_for_390ms(self,sw):
        self.pause()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.paused:
            self.resume()

    # saloon pauses the quickdraw
    def sw_saloonPopper_active_for_290ms(self,sw):
        self.pause()

    # resume when inactive
    def sw_saloonPopper_inactive(self,sw):
        if self.paused:
            self.resume()

    def bumper_hit(self,bumper):
        if not self.paused:
            self.pause()

    def start_quickdraw(self,side):
        # audit
        self.game.game_data['Feature']['Quickdraws Started'] += 1
        # set the stack flag
        self.game.stack_level(0,True)

        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        self.side = side
        # tick up the started stat
        self.game.increase_tracking('quickdrawsStarted')

        print "STARTING QUICKDRAW ON SIDE:" + str(side)
        # set the status of this side to running
        self.game.set_tracking('quickdrawStatus',"RUNNING",side)
        # figure out the available bad guys
        choices = []
        count = 0
        for x in self.game.show_tracking('badGuysDead'):
            if not x:
                choices.append(count)
            count += 1

        print "AVAILABLE BAD GUYS"
        print choices
        # pick one of them at random
        self.target = random.choice(choices)
        print "BAD GUY ACTIVE IS: " + str(self.target)
        # kill the game music
        self.stop_music()
        # start the mode music
        self.game.sound.play(self.game.assets.music_quickdrawBumper)
        self.delay("Operational",delay=1.3,handler=self.music_on,param=self.game.assets.music_quickdraw)
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_quickdrawStart)
        # pop that sucker up
        self.game.bad_guys.target_up(self.target)
        # Set up the display
        anim = self.game.assets.dmd_quickdrawStart
        self.animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        # set the end time based on the config setting
        # set up the point value
        value = [500000,750000,1000000,1500000,2000000]
        # based on rank
        rank = self.game.show_tracking('rank')
        self.points = value[rank]
        scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.points))
        # combine the score and animation and turn it on
        self.layer = dmd.GroupedLayer(128,32,[self.animLayer,scoreLayer])
        # read the run time from the settings
        self.runtime = self.game.user_settings['Gameplay (Feature)']['Quickdraw Timer']
        # set the amount to subtract per 5th of a second
        # I hope this is right - divide the points by 10, divide by 5 times the amount of seconds, times 10 again to get an even number
        # then take off 370 to get a more interesting countdown
        self.portion = ((self.points / 10) / int(self.runtime * 5) * 10) - 370
        # queue up a delay for when the timer should run out if the mode hasn't been won
        # then start the timer after a 1 second grace period
        self.delay("Grace",delay=1.5,handler=self.timer,param=self.target)

    def timer(self,target):
        # ok, so this has to control the score and display?
        # for now stepping in 1/5 second
        self.runtime -= 0.2
        if self.runtime <= 0:
            # timer runs out - player lost
            self.lost(target)
        else:
            # every 3 seconds, play a taunt quote
            if int(self.runtime % 5.0) == 0 and self.runtime >= 6:
                self.game.base.play_quote(self.game.assets.quote_quickdrawTaunt)
            # play a hurry quote if we're at 2 seconds.
            if self.runtime == 2:
                self.game.base.play_quote(self.game.assets.quote_hurry)
            # take points off the score
            self.points -= self.portion
            # update the score text layer
            scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.points))
            if self.layer == None:
                self.layer = self.no_layer()

            self.layer = dmd.GroupedLayer(128,32,[self.layer,scoreLayer])
            # update the group layer
            # make it active
            self.layer = dmd.GroupedLayer(128,32,[self.animLayer,scoreLayer])
            # delay the next iteration
            self.delay("Timer Delay", delay = 0.2, handler = self.timer, param=target)

    def pause(self):
        self.paused = True
        # clear the layer
        self.layer = None
        self.cancel_delayed("Timer Delay")
        #textString = "< QUICKDRAW PAUSED >"
        #self.layer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)
        self.layer = self.pauseView

    def resume(self):
        self.paused = False
        self.timer(self.target)

    def won(self,target):
        # audit
        self.game.game_data['Feature']['Quickdraws Won'] += 1
        # kill the timer
        self.cancel_delayed("Grace")
        self.cancel_delayed("Timer Delay")
        # kill the mode music
        print "QUICKDRAW WON IS KILLING THE MUSIC"
        # add one to the total dead
        self.game.increase_tracking('kills')
        # and tick up the quickdraw wins
        dudesDead = self.game.increase_tracking('quickdrawsWon')
        # only kill the music if there's not a higher level running
        self.stop_music(slice=1)
        # play the win animation
        anim = self.game.assets.dmd_quickdrawHit
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        #  setup the text
        scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.points))
        # combine and activate
        textLayer = dmd.TextLayer(84,20, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("QUICK DRAW!")
        self.game.sound.play(self.game.assets.sfx_quickdrawHit)
        self.game.sound.play(self.game.assets.sfx_quickdrawFinale)
        self.game.sound.play(self.game.assets.sfx_cheers)
        stackLevel = self.game.show_tracking('stackLevel')
        winLayer = dmd.GroupedLayer(128,32,[animLayer,scoreLayer,textLayer])
        # flash the guns
        self.game.base.guns_flash(1)
        # if something higher is running, throw the win display in a cut in
        if True in stackLevel[1:]:
            self.game.interrupter.cut_in(winLayer,1)
        else:
            self.layer = winLayer
        myWait = len(anim.frames) / 10.0 + 2
        # stuff specific to winning
        # score the points
        self.game.score(self.points)
        # add some bonus
        self.game.add_bonus(50000)
        # update the bad guys
        self.game.set_tracking('badGuysDead',"True",target)
        self.lamp_update()
        # stall a bit, then do the rest of the winning
        self.delay("Operational",delay=0.5,handler=self.finish_win,param=dudesDead)

    def finish_win(self,dudesDead):
        # play a quote
        duration = self.game.base.priority_quote(self.game.assets.quote_quickdrawWin)
        # if this is the 4th one , and we're not at the EB max, then light extra ball
        if dudesDead == 4 and self.game.show_tracking('extraBallsTotal') < self.game.user_settings['Machine (Standard)']['Maximum Extra Balls']:
            # call the extra ball lit with a callback to the check bounty routine after
            # audit
            self.game.game_data['Feature']['EB Lit Quickdraws'] += 1
            self.delay("Operational",delay=duration,handler=self.game.mine.light_extra_ball,param=self.game.quickdraw.check_bounty)
        # any other case, just go to check bounty
        else:
            self.delay("Operational",delay=duration,handler=self.check_bounty)

    def check_bounty(self):
        # if the bounty isn't lit, light bounty - should these stack?
        # TODO stock game does not stack bounties - might be fun to add that
        if not self.game.show_tracking('isBountyLit'):
            # turn off the current layer
            self.layer = None
            # run the light bounty
            self.game.saloon.light_bounty()
            # shutdown wait to cover the bounty display
            self.delay("Operational",delay=1.6,handler=self.end_quickdraw)
        else:
            self.end_quickdraw()

    def lost(self,target):
        # kill the mode music
        # start up the main theme again if a higher level mode isn't running
        self.stop_music(slice=1)
        # stuff specific to losing
        # drop the coil and kill the lamp
        self.game.bad_guys.target_down(target)
        # else just end the quickdraw
        self.end_quickdraw()

    def end_quickdraw(self):
        # status passes won/lost?
        print "ENDING QUICKDRAW"
        # turn off the layer
        self.layer = None

        self.update_tracking()

        self.lamp_update()
        # turn the main music back on - if a second level mode isn't running
        print "QUICKDRAW MUSIC BACK ON CHECK - BALLS IN PLAY: " + str(self.game.trough.num_balls_in_play)
            # turn the level 1 flag off
        self.game.stack_level(0,False)
        if True not in self.game.show_tracking('stackLevel') and self.game.trough.num_balls_in_play != 0:
            self.music_on(self.game.assets.music_mainTheme)
            # full lamp update
        self.lamp_update()
        # remove the mode
        self.unload()

    def tilted(self):
        if self.running:
            self.update_tracking()
        self.running = False
        self.unload()

    def update_tracking(self):
        # set the status to OPEN
        self.game.set_tracking('quickdrawStatus',"OPEN",self.side)
        # If all the bad guys are now dead, make showdown ready, or ambush
        if False not in self.game.show_tracking('badGuysDead'):
            if self.game.show_tracking('showdownStatus') != "OVER":
                self.game.set_tracking('showdownStatus',"READY")
                print "SHOWDOWN STATUS IS READY"
            else:
                self.game.set_tracking('ambushStatus',"READY")


    def mode_stopped(self):
        self.running = False
        print "QUICKDRAW IS DISPATCHING DELAYS"
        self.wipe_delays()