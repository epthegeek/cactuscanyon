###
###   ___        _      _       _
###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      __
### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / /
### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /
###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/
###

from procgame import *
import cc_modes
import ep
import random

class Quickdraw(game.Mode):
    """Quickdraw code """
    def __init__(self,game,priority):
        super(Quickdraw, self).__init__(game,priority)
        # default
        self.side = 0
        self.target = 0
        self.paused = False

    def ball_drained(self):
        # the the ball drains, quickdraw is lost
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('quickdrawStatus',self.side) == "RUNNING":
            self.lost(self.side)

    # switches

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
        self.bumper_hit('bottom')

    # so does the mine
    def sw_minePopper_active_for_400ms(self,sw):
        self.pause()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.paused:
            self.resume()

    def bumper_hit(self,bumper):
        if not self.paused:
            self.pause()

    def start_quickdraw(self,side):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        # set the flag to stop other gun modes
        self.game.set_tracking('stackLevel',True,0)
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
        print "START QUICKDRAW IS KILLING THE MUSIC"

        self.game.sound.stop_music()
        # start the mode music
        self.game.sound.play(self.game.assets.music_quickdrawBumper)
        self.delay(name="quickdraw music",delay=1.3,handler=self.game.base_game_mode.music_on,param=self.game.assets.music_quickdraw)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_quickdrawStart)
        # pop that sucker up
        self.game.bad_guys.target_up(self.target)
        # Set up the display
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-start.dmd')
        self.animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
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
        self.delay(name="Grace",delay=1.5,handler=self.timer,param=self.target)

    def timer(self,target):
        # ok, so this has to control the score and display?
        # for now stepping in 1/5 second
        self.runtime -= 0.2
        if self.runtime <= 0:
            # timer runs out - player lost
            self.lost(target)
        else:
            # every 3 seconds, play a taunt quote
            if int(self.runtime % 3.0) == 0 and self.runtime >= 5:
                self.game.sound.play_voice(self.game.assets.quote_quickdrawTaunt)
            # play a hurry quote if we're at 2 seconds.
            if self.runtime == 2:
                self.game.sound.play(self.game.assets.quote_hurry)
            # take points off the score
            self.points -= self.portion
            # update the score text layer
            scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.points))
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
        textString = "< QUICKDRAW PAUSED >"
        self.layer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)

    def resume(self):
        self.paused = False
        self.timer(self.target)

    def won(self,target):
        # kill the timer
        self.cancel_delayed("Grace")
        self.cancel_delayed("Timer Delay")
        # kill the mode music
        print "QUICKDRAW WON IS KILLING THE MUSIC"
        # add one to the total dead
        self.game.increase_tracking('kills')
        # and tick up the quickdraw wins
        self.game.increase_tracking('quickdrawsWon')

        self.game.sound.stop_music()
        # play the win animation
        anim = dmd.Animation().load(ep.DMD_PATH+'quickdraw-hit.dmd')
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        #  setup the text
        scoreLayer = dmd.TextLayer(84, 4, self.game.assets.font_12px_az, "center", opaque=False).set_text(ep.format_score(self.points))
        # combine and activate
        textLayer = dmd.TextLayer(84,20, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("QUICK DRAW!")
        self.game.sound.play(self.game.assets.sfx_quickdrawHit)
        self.game.sound.play(self.game.assets.sfx_quickdrawFinale)
        self.game.sound.play(self.game.assets.sfx_cheers)
        self.layer = dmd.GroupedLayer(128,32,[animLayer,scoreLayer,textLayer])
        myWait = len(anim.frames) / 10.0 + 2
        # play a quote
        self.delay(delay=0.5,handler=self.game.play_remote_sound,param=self.game.assets.quote_quickdrawWin)
        # stuff specific to winning
        # score the points
        self.game.score(self.points)
        # update the bad guys
        self.game.set_tracking('badGuysDead',"True",target)
        self.game.bad_guys.update_lamps()
        # end the quickdraw after the animation bit - and maybe pad for sound
        self.delay(delay=myWait,handler=self.check_bounty)

    def check_bounty(self):
        # if the bounty isn't lit, light bounty - should these stack?
        # TODO stock game does not stack bounties - might be fun to add that
        if not self.game.show_tracking('isBountyLit'):
            # turn off the current layer
            self.layer = None
            # run the light bounty
            self.game.saloon.light_bounty()
            # shutdown wait to cover the bounty display
            self.delay(delay=1.6,handler=self.end_quickdraw)
        else:
            self.end_quickdraw()

    def lost(self,target):
        # kill the mode music
        print "QUICKDRAW LOST IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # stuff specific to losing
        # drop the coil and kill the lamp
        self.game.bad_guys.target_down(target)
        # else just end the quickdraw
        self.end_quickdraw()

    def end_quickdraw(self):
        # status passes won/lost?
        print "ENDING QUICKDRAW"
        # set the status to OPEN
        self.game.set_tracking('quickdrawStatus',"OPEN",self.side)
        # turn off the layer
        self.layer = None
        # play a parting quote?
        # If all the bad guys are now dead, make showdown ready, or ambush
        if False not in self.game.show_tracking('badGuysDead'):
            if self.game.show_tracking('showdownStatus') != "OVER":
                self.game.set_tracking('showdownStatus',"READY")
                print "SHOWDOWN STATUS IS READY"
            else:
                self.game.set_tracking('ambushStatus',"READY")
        self.game.bad_guys.update_lamps()
        self.game.base_game_mode.update_lamps()
        # turn the main music back on - if a second level mode isn't running
        if not self.game.show_tracking('stackLevel',1):
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
            # turn the level 1 flag off
        self.game.set_tracking('stackLevel',False,0)
        # full lamp update
        self.game.update_lamps()
        # remove the mode
        self.game.modes.remove(self.game.quickdraw)

    def mode_stopped(self):
        self.dispatch_delayed()