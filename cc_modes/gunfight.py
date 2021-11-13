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
###
###   ____              __ _       _     _
###  / ___|_   _ _ __  / _(_) __ _| |__ | |_
### | |  _| | | | '_ \| |_| |/ _` | '_ \| __|
### | |_| | |_| | | | |  _| | (_| | | | | |_
###  \____|\__,_|_| |_|_| |_|\__, |_| |_|\__|
###                          |___/
###
from procgame import dmd
import ep
import random

class Gunfight(ep.EP_Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Gunfight, self).__init__(game,priority)
        self.myID = "Gunfight"
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
        self.shooting = False
        self.keys_index = {'start':list(range(len(self.game.sound.sounds[self.game.assets.quote_gunfightStart]))),
                           'fail':list(range(len(self.game.sound.sounds[self.game.assets.quote_gunFail])))}
        self.counts_index = {'start':0,
                             'fail':0}
        random.shuffle(self.keys_index['start'])
        random.shuffle(self.keys_index['fail'])
        self.hard = 'Hard' ==  self.game.user_settings['Gameplay (Feature)']['Gunfight Difficulty']

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('gunfightStatus') == "RUNNING":
            #print "GUNFIGHT BALL DRAINED ROUTINE"
            self.lost()

    def mode_started(self):
        self.running = True
        self.win = False
        self.wipe_delays()
        # check the balls save timer
        if self.game.trough.ball_save_timer > 0:
            self.save_timer = self.game.trough.ball_save_timer
        else:
            self.save_timer = 0

    # kill switches - they check win first, in case the ball glanced off a bad guy and then hit a target
    def sw_leftRampEnter_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - Left ramp enter killed it"
            self.lost()

    def sw_centerRampMake_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - Center ramp make killed it"
            self.lost()

    def sw_rightRampMake_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - right ramp make killed it"
            self.lost()

    def sw_beerMug_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - beer mug killed it"
            self.lost()

    def sw_saloonGate_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - saloon gate killed it"
            self.lost()

    def sw_mineEntrance_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - mine entrance killed it"
            self.lost()

    def sw_leftLoopBottom_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - left loop bottom killed it"
            self.lost()

    def sw_rightLoopBottom_active(self,sw):
        if not self.win and not self.starting:
            #print "Gunfight - right loop bottom killed it"
            self.lost()

    def sw_flipperLwL_active(self,sw):
        if self.shooting and self.activeSide == 0:
            self.game.sound.play(self.game.assets.sfx_explosion11)
            self.game.coils.leftGunFlasher.schedule(0x0000025F,cycle_seconds=1)

    def sw_flipperLwR_active(self,sw):
        if self.shooting and self.activeSide == 1:
            self.game.sound.play(self.game.assets.sfx_explosion11)
            self.game.coils.rightGunFlasher.schedule(0x0000025F,cycle_seconds=1)

    def start_gunfight(self,side):
        # audit
        self.game.game_data['Feature']['Gunfights Started'] += 1
        self.starting = True
        #print "GUNFIGHT GOES HERE"
        # pop up the post
        #print "RAISE POST ON SIDE: " + str(side)
        self.activeSide = side
        self.posts[self.activeSide].patter(on_time=2,off_time=6,original_on_time=60)
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        # set the level 1 stack flag
        self.game.stack_level(0,True)
        # turn off the lights
        self.game.set_tracking('lampStatus',"OFF")
        self.game.gi_control("OFF")
        self.game.lamp_control.disable_bad_guys()
        self.game.lamp_control.disable_bonus_lanes()
        self.lamp_update()
        if side == 0 and not self.game.lamp_control.lights_out:
            self.game.lamps.leftGunfightPin.schedule(0x00FF00FF)
        else:
            if not self.game.lamp_control.lights_out:
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
        #print "ENEMY: " + str(enemy)
        # save the final target
        self.enemy = enemy
        #print badGuys
        badGuys.remove(enemy)
        # and tag them on the end
        badGuys.append(enemy)
        #print badGuys
        # stop the music
        # only kill the music if there's not a higher level running
        self.stop_music(slice=1)
        # play the intro riff
        myWait = self.game.sound.play(self.game.assets.music_gunfightIntro)
        # delayed play the drum roll
        self.delay("Operational",delay=myWait,handler=self.music_on,param=self.game.assets.music_drumRoll)
        # play a quote
        self.play_ordered_quote(self.game.assets.quote_gunfightStart,'start')
        # display the clouds with gunfight text
        if self.game.user_settings['Gameplay (Feature)']['Gunfight Mountain'] == 'Green':
            thecolor = ep.ORANGE
        else:
            thecolor = ep.RED
        title = ep.EP_TextLayer(64, 5, self.game.assets.font_20px_az, "center", opaque=False).set_text("Gunfight",color=thecolor)
        title.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_gunfightPan.frames[0])
        mask = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_gunfightMask.frames[0])
        mask.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[backdrop,mask,title])
        # after a delay pan down to the dude
        self.delay("Operational",delay = 1.5,handler=self.gunfight_pan,param=badGuys)

    def won(self):
        # audit
        self.game.game_data['Feature']['Gunfights Won'] += 1
        self.win = True
        self.shooting = False
        # set some tracking
        self.game.increase_tracking('gunfightsWon')
        # only kill the music if there's not a higher level running
        self.stop_music(slice=1)
        # cancel the lose delay
        self.cancel_delayed("Gunfight Lost")
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        # call increase rank with the True flag to trigger the gunfight quote option
        rankTitle,duration = self.game.badge.increase_rank(True)
        # the melodic flourish noise
        self.delay("Operational",delay=0.2,handler=self.game.sound.play,param=self.game.assets.sfx_gunfightFlourish)
        # flash the guns
        self.game.base.guns_flash(1)
        # play the animation
        anim = self.game.assets.dmd_dudeShotShouldersUp
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after the animation, display the win
        self.delay("Operational",delay=myWait,handler=self.display_win,param=rankTitle)

    def display_win(self,rankTitle):
        textString3 = "YOUR RANK: " + rankTitle
        newrank = self.game.show_tracking('rank')
        values = [str(ep.format_score(500000)),str(ep.format_score(750000)),str(ep.format_score(1000000)),str(ep.format_score(1500000)),str(ep.format_score(2000000))]
        textString4 = "QUICKDRAWS WORTH: " + values[newrank]
        # award some points
        points = 750000
        self.game.score(points)
        self.game.add_bonus(100000)
        # show the win screen
        textLine1 = ep.EP_TextLayer(64, 0, self.game.assets.font_7px_bold_az, "center", opaque=True).set_text("BAD GUY SHOT!",color=ep.YELLOW)
        textLine2 = ep.pulse_text(self,64,9,ep.format_score(points),color=ep.GREEN)
        textLine3 = ep.EP_TextLayer(64, 20, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString3,color=ep.BROWN)
        textLine4 = ep.EP_TextLayer(64, 26, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString4,color=ep.BROWN)
        self.layer = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,textLine4])
        self.delay("Operational",delay=2,handler=self.end_gunfight)

    def lost(self):
        self.shooting = False
        #print "Gunfight - Lost routine"
        # cancel the delay, in case a switch sent us here
        self.cancel_delayed("Gunfight Lost")
        # drop the bad guy
        self.game.bad_guys.target_down(self.enemy)
        # only kill the music if there's not a higher level running
        self.stop_music(slice=1)
        # play a quote
        duration = self.play_ordered_quote(self.game.assets.quote_gunFail,'fail')
        # shut things down
        self.end_gunfight(duration)

    def end_gunfight(self,waitTime=0):
        self.layer = None

        self.update_tracking()

        # turn off the level one flag
        self.game.stack_level(0,False)
        # turn the main game music back on if a second level mode isn't running
        # start up the main theme again if a higher level mode isn't running
        if self.game.trough.num_balls_in_play > 0:
            self.music_on(self.game.assets.music_mainTheme,mySlice=1)

        self.lamp_update()
        self.cancel_delayed("Operational")
        # unload
        self.unload()

    def tilted(self):
        if self.running:
            self.update_tracking()
        self.running = False
        self.unload()

    def update_tracking(self):
        # tidy up - set the gunfight status and bart brothers status to open
        self.game.set_tracking('gunfightStatus',"OPEN")
        # only change the bart status if he was dead - gunfights from bounty/skill shot shouldn't reset bart
        if self.game.show_tracking('bartStatus') == "DEAD":
            self.game.set_tracking('bartStatus',"OPEN")


    def gunfight_pan(self,badGuys):
        # the intro animation
        anim = self.game.assets.dmd_gunfightPan
        myWait = len(anim.frames) / 30 + 1.2
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
        self.layer = animLayer
        # Split here for optional HARD setting
        if self.hard:
            handler = self.gunfight_intro_hard
        else:
            handler = self.gunfight_intro_eyes
        self.delay("Operational",delay=myWait,handler=handler,param=badGuys)

    def gunfight_intro_hard(self,badGuys):
        # put the last bad guy in the zero spot
        badGuys[0] = badGuys[3]
        #print "Hard mode: Active Target is now: " +str(badGuys[0])
        # set the display to the eyes
        anim = self.game.assets.dmd_gunfightEyes
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # pick a random wait time between 1 and 4 seconds
        myWait = random.randrange(1,4,1)
        #print "Hard Mode: wait time is " + str(myWait)
        # go to the draw after the delay
        self.delay("Operational",delay=myWait,handler=self.gunfight_intro_draw,param=badGuys)

    def gunfight_intro_eyes(self,badGuys):
        # pop up the first bad guy and remove it from the array
        enemy = badGuys.pop(0)
        #print "POP ENEMY: " + str(enemy)
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
        #print "POP ENEMY: " + str(enemy)
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
        #print "POP ENEMY: " + str(enemy)
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
        #print "POP ENEMY: " + str(enemy)
        # need this for the lost
        self.enemy = enemy
        self.game.bad_guys.target_up(enemy)
        # play the 4 bells
        if not self.hard:
            self.game.sound.play(self.game.assets.sfx_gunfightBell)
            # flash the gun flashers
            self.game.coils.leftGunFlasher.schedule(0x00020821,cycle_seconds=1)
            self.game.coils.rightGunFlasher.schedule(0x00020821,cycle_seconds=1)
            self.delay("Operational",delay=0.6,handler=self.game.sound.play,param=self.game.assets.sfx_gunCock)
            # run the animation
            anim = self.game.assets.dmd_gunfightBoots
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            self.layer = animLayer
        else:
            myWait = 0.2
            # flash the gun flashers
            self.game.coils.leftGunFlasher.schedule(0x00000021,cycle_seconds=1)
            self.game.coils.rightGunFlasher.schedule(0x00000021,cycle_seconds=1)
        # pass one last time to the release
        self.delay("Operational",delay=myWait,handler=self.gunfight_release)

    def gunfight_release(self):
        # play the draw quote
        self.game.base.play_quote(self.game.assets.quote_gunfightDraw)
        text = ep.EP_TextLayer(28,8,self.game.assets.font_12px_az,"center",opaque=False).set_text("DRAW!",blink_frames=2,color=ep.RED)
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_gunfightBoots.frames[8])
        self.layer = dmd.GroupedLayer(128,32,[backdrop,text])
        # turn the GI back on
        self.game.set_tracking('lampStatus', "ON")
        self.game.gi_control("ON")
        self.lamp_update()
        # kill the starting flag
        self.starting = False
        #print "DROP THE POST"
        self.posts[self.activeSide].disable()
        # if there was ball save time left, put that back
        if self.save_timer > 0:
            self.game.trough.start_ball_save(self.save_timer,1)
        # set the shooting flag
        self.shooting = True
        # set a named timer for gunfight lost
        self.delay("Gunfight Lost",delay=4,handler=self.lost)

    def mode_stopped(self):
        self.running = False
        self.shooting = False
        self.wipe_delays()
        self.starting = False

