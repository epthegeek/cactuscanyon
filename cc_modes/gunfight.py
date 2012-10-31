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
###
###   ____              __ _       _     _
###  / ___|_   _ _ __  / _(_) __ _| |__ | |_
### | |  _| | | | '_ \| |_| |/ _` | '_ \| __|
### | |_| | |_| | | | |  _| | (_| | | | | |_
###  \____|\__,_|_| |_|_| |_|\__, |_| |_|\__|
###                          |___/
###
from procgame import *
import cc_modes
import ep
import random

class Gunfight(ep.EP_Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Gunfight, self).__init__(game,priority)
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]
        self.rankUps = [self.game.assets.quote_rankUpPartner,
                        self.game.assets.quote_rankUpPartner,
                        self.game.assets.quote_rankUpDeputy,
                        self.game.assets.quote_rankUpSheriff,
                        self.game.assets.quote_rankUpMarshall]
        self.winQuotes = [self.game.assets.quote_gunfightWinPartner,
                          self.game.assets.quote_gunfightWinPartner,
                          self.game.assets.quote_gunfightWinDeputy,
                          self.game.assets.quote_gunfightWinSheriff,
                          self.game.assets.quote_gunfightWinMarshall]
        self.win = False
        self.starting = False

    def ball_drained(self):
        print "GUNFIGHT - BALLS IN PLAY: " + str(self.game.trough.num_balls_in_play)
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('gunfightStatus') == "RUNNING":
            print "GUNFIGHT BALL DRAINED ROUTINE"
            self.lost()

    def mode_started(self):
        self.running = True
        self.win = False

    # kill switches - they check win first, in case the ball glanced off a bad guy and then hit a target
    def sw_leftRampEnter_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - Left ramp enter killed it"
            self.lost()

    def sw_centerRampMake_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - Center ramp make killed it"
            self.lost()

    def sw_rightRampMake_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - right ramp make killed it"
            self.lost()

    def sw_beerMug_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - beer mug killed it"
            self.lost()

    def sw_saloonGate_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - saloon gate killed it"
            self.lost()

    def sw_mineEntrance_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - mine entrance killed it"
            self.lost()

    def sw_leftLoopBottom_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - left loop bottom killed it"
            self.lost()

    def sw_rightLoopBottom_active(self,sw):
        if not self.win and not self.starting:
            print "Gunfight - right loop bottom killed it"
            self.lost()


    def start_gunfight(self,side):
        self.starting = True
        print "GUNFIGHT GOES HERE"
        # pop up the post
        print "RAISE POST ON SIDE: " + str(side)
        self.activeSide = side
        self.posts[self.activeSide].patter(on_time=2,off_time=6,original_on_time=60)
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        # set the level 1 stack flag
        self.game.set_tracking('stackLevel',True,0)
        # turn off the lights
        self.game.set_tracking('lampStatus',"OFF")
        self.game.gi_control("OFF")
        self.game.update_lamps()
        if side == 0:
            self.game.lamps.leftGunfightPin.schedule(0x00FF00FF)
        else:
            self.game.lamps.rightGunfightPin.schedule(0x00FF00FF)
        self.game.increase_tracking('gunfightsStarted')
        # set the bad guy pop order accounting for the side it started on
        badGuys = [0,1,2,3]
        # select our eventual target
        # 0 is the left side, it shouldn't use target 1
        if side == 0:
            enemy = random.randrange(1,4,1)
        # 1 is the right side, it shouldn't use target 3
        else:
            enemy = random.randrange(0,3,1)
            # scramble the list
        random.shuffle(badGuys)
        # pull out the enemey
        print "ENEMY: " + str(enemy)
        # save the final target
        self.enemy = enemy
        print badGuys
        badGuys.remove(enemy)
        # and tag them on the end
        badGuys.append(enemy)
        print badGuys
        # stop the music
        print "START GUNFIGHT IS KILLING THE MUSIC"
        # only kill the music if there's not a higher level running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[1:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        # play the intro riff
        myWait = self.game.sound.play(self.game.assets.music_gunfightIntro)
        # delayed play the drum roll
        self.delay("Operational",delay=myWait,handler=self.game.base.music_on,param=self.game.assets.music_drumRoll)
        # play a quote
        self.game.base.play_quote(self.game.assets.quote_gunfightStart)
        # display the clouds with gunfight text
        title = dmd.TextLayer(64, 5, self.game.assets.font_20px_az, "center", opaque=False).set_text("Gunfight")
        title.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_gunfightTop.frames[0])
        mask = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_gunfightMask.frames[0])
        mask.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[backdrop,mask,title])
        # after a delay pan down to the dude
        self.delay("Operational",name="pan",delay = 1.5,handler=self.gunfight_pan,param=badGuys)

    def won(self):
        self.win = True
        # default the quoteToPlay
        quoteToPlay = self.game.assets.quote_quickdrawWin
        # set some tracking
        self.game.increase_tracking('gunfightsWon')
        # up the rank if it's not full yet
        if self.game.show_tracking('rank') < 4:
            newrank = self.game.increase_tracking('rank')
            self.game.base.update_lamps()
            # pick the sound to play
            quote = random.choice([self.rankUps,self.winQuotes])
            quoteToPlay = quote[newrank]
        # if it is full, this bit is awkward
        else:
            newrank = 4

        print "GUNFIGHT WON IS KILLING THE MUSIC"
        # only kill the music if there's not a higher level running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[1:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        # cancel the lose delay
        self.cancel_delayed("Gunfight Lost")
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        self.delay("Operational",delay=0.2,handler=self.game.sound.play,param=self.game.assets.sfx_gunfightFlourish)
        # this plays the quoteToPlay decided above - separates ranking up from marhsall wins
        self.delay("Operational",delay=0.3,handler=self.game.base.priority_quote,param=quoteToPlay)
        # play the animation
        anim = self.game.assets.dmd_dudeShotShouldersUp
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after the animation, display the win
        self.delay("Operational",delay=myWait,handler=self.display_win,param=newrank)

    def display_win(self,newrank):
        ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHAL"]
        textString3 = "YOUR RANK: " + ranks[newrank]
        values = ["500,000","750,000","1,000,000","1,500,000","2,000,000"]
        textString4 = "QUICKDRAWS WORTH: " + values[newrank]
        # award some points
        points = 750000
        self.game.score(points)
        # show the win screen
        textLine1 = dmd.TextLayer(64, 0, self.game.assets.font_7px_bold_az, "center", opaque=True).set_text("BAD GUY SHOT!")
        textLine2 = ep.pulse_text(self,64,9,ep.format_score(points))
        textLine3 = dmd.TextLayer(64, 20, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString3)
        textLine4 = dmd.TextLayer(64, 26, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString4)
        self.layer = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,textLine4])
        self.delay("Operational",delay=2,handler=self.end_gunfight)

    def lost(self):
        print "Gunfight - Lost routine"
        # cancel the delay, in case a switch sent us here
        self.cancel_delayed("Gunfight Lost")
        # drop the bad guy
        self.game.bad_guys.target_down(self.enemy)
        # only kill the music if there's not a higher level running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[1:] and self.game.trough.num_balls_in_play != 0:
            print "GUNFIGHT LOST IS KILLING THE MUSIC"
            self.game.sound.stop_music()
        # play a quote
        duration = self.game.base.play_quote(self.game.assets.quote_gunFail)
        # shut things down
        self.end_gunfight(duration)

    def end_gunfight(self,waitTime=0):
        self.layer = None
        # tidy up - set the gunfight status and bart brothers status to open
        self.game.set_tracking('gunfightStatus',"OPEN")
        # only change the bart status if he was dead - gunfights from bounty/skill shot shouldn't reset bart
        if self.game.show_tracking('bartStatus') == "DEAD":
            self.game.set_tracking('bartStatus',"OPEN")
        # turn off the level one flag
        self.game.set_tracking('stackLevel',False,0)
        # turn the main game music back on if a second level mode isn't running
        # start up the main theme again if a higher level mode isn't running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[1:] and self.game.trough.num_balls_in_play != 0:
            self.game.base.music_on(self.game.assets.music_mainTheme)
        # if we're at marshall, and it hasn't run yet, do the MM if nothing else is running
        if self.game.show_tracking('rank') == 4 and self.game.show_tracking('marshallMultiballRun') == False:
            if True not in self.game.show_tracking('stackLevel'):
                # disabled marshall multiball for now
                self.delay(delay=waitTime,handler=self.game.base.kickoff_marshall)
            else:
                pass
        self.game.bad_guys.update_lamps()
        self.cancel_delayed("Operational")
        # unload
        self.unload()

    def gunfight_pan(self,badGuys):
        # the intro animation
        anim = self.game.assets.dmd_gunfightPan
        myWait = len(anim.frames) / 60 + 1.3
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=1)
        self.layer = animLayer
        self.delay("Operational",delay=myWait,handler=self.gunfight_intro_eyes,param=badGuys)

    def gunfight_intro_eyes(self,badGuys):
        # pop up the first bad guy and remove it from the array
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        # play the orchestra hit sound
        self.game.sound.play(self.game.assets.sfx_gunfightHit1)
        # show the eyes animation
        anim = self.game.assets.dmd_gunfightEyes
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after a delay pass to the hands with the pop order
        self.delay(name="Operational",delay=1.1,handler=self.gunfight_intro_hands,param=badGuys)
        # and drop the current one
        self.delay(delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_hands(self,badGuys):
        # pop the second bad guy and remove it
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        self.game.base.play_quote(self.game.assets.quote_gunfightReady)
        # play the second orchestra hit
        self.game.sound.play(self.game.assets.sfx_gunfightHit2)
        # show the hands animation
        anim = self.game.assets.dmd_gunfightHands
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after a delay pass to the feet with the pop order
        self.delay("Operational",delay=1.1,handler=self.gunfight_intro_boots,param=badGuys)
        self.delay("Operational",delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_boots(self,badGuys):
        # pop the third bad guy
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        self.game.base.play_quote(self.game.assets.quote_gunfightSet)
        # play the orchestra hit
        self.game.sound.play(self.game.assets.sfx_gunfightHit3)
        # show the boots
        boots = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_gunfightBoots.frames[0])
        self.layer = boots
        # after a delay - pass to the final setp
        self.delay("Operational",delay=1.1,handler=self.gunfight_intro_draw,param=badGuys)
        self.delay("Operational",delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_draw(self,badGuys):
        # pop the last bad guy
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        # need this for the lost
        self.enemy = enemy
        self.game.bad_guys.target_up(enemy)
        # kill the starting flag
        self.starting = False
        # play the 4 bells
        self.game.sound.play(self.game.assets.sfx_gunfightBell)
        self.delay("Operational",delay=0.6,handler=self.game.sound.play,param=self.game.assets.sfx_gunCock)
        # run the animation
        anim = self.game.assets.dmd_gunfightBoots
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # pass one last time to the release
        self.delay("Operational",delay=myWait,handler=self.gunfight_release)

    def gunfight_release(self):
        # play the draw quote
        self.game.base.play_quote(self.game.assets.quote_gunfightDraw)
        text = dmd.TextLayer(28,8,self.game.assets.font_12px_az,"center",opaque=False).set_text("DRAW!",blink_frames=2)
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_gunfightBoots.frames[8])
        self.layer = dmd.GroupedLayer(128,32,[backdrop,text])
        # turn the GI back on
        self.game.set_tracking('lampStatus', "ON")
        self.game.gi_control("ON")
        self.game.update_lamps()
        print "DROP THE POST"
        self.posts[self.activeSide].disable()
        # set a named timer for gunfight lost
        self.delay("Gunfight Lost",delay=4,handler=self.lost)

    def mode_stopped(self):
        self.running = False
        print "GUNFIGHT IS DISPATCHING DELAYS"
        self.dispatch_delayed()
        self.starting = False

