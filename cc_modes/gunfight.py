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

class Gunfight(game.Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(Gunfight, self).__init__(game,priority)
        self.posts = [self.game.coils.leftGunFightPost,self.game.coils.rightGunFightPost]

    def ball_drained(self):
        if self.game.num_balls_in_play == 0 and self.game.show_tracking('gunfightStatus') == "RUNNING":
            self.lost()

    def start_gunfight(self,side):
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
        print "GUNFIGHT GOES HERE"
        # pop up the post
        print "RAISE POST ON SIDE: " + str(side)
        self.activeSide = side
        self.posts[self.activeSide].patter(on_time=4,off_time=12,original_on_time=30)
        # set the bad guy pop order accounting for the side it started on
        badGuys = [0,1,2,3]
        # select our eventual target
        # 0 is the left side, it shouldn't use target 1
        if side == 0:
            enemy = random.randrange(1,3,1)
        # 1 is the right side, it shouldn't use target 3
        else:
            enemy = random.randrange(0,2,1)
            # scramble the list
        random.shuffle(badGuys)
        # pull out the enemey
        print "ENEMY: " + str(enemy)
        print badGuys
        badGuys.remove(enemy)
        # and tag them on the end
        badGuys.append(enemy)
        print badGuys
        # stop the music
        print "START GUNFIGHT IS KILLING THE MUSIC"

        self.game.sound.stop_music()
        # play the intro riff
        myWait = self.game.sound.play(self.game.assets.music_gunfightIntro)
        # delayed play the drum roll
        self.delay(delay=myWait,handler=self.game.base_game_mode.music_on,param=self.game.assets.music_drumRoll)
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_gunfightStart)
        # display the clouds with gunfight text
        title = dmd.TextLayer(64, 5, self.game.assets.font_20px_az, "center", opaque=False).set_text("Gunfight")
        title.composite_op = "blacksrc"
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'gunfight-top.dmd').frames[0])
        mask = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'gunfight-mask.dmd').frames[0])
        mask.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128,32,[backdrop,mask,title])
        # after a delay pan down to the dude
        self.delay(name="pan",delay = 1.5,handler=self.gunfight_pan,param=badGuys)

    def won(self):
        print "GUNFIGHT WON IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # cancel the lose delay
        self.cancel_delayed("Gunfight Lost")
        # play a quote
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        self.delay(delay=0.2,handler=self.game.play_remote_sound,param=self.game.assets.sfx_gunfightFlourish)
        self.delay(delay=0.3,handler=self.game.play_remote_sound,param=self.game.assets.quote_gunWin)
        # play the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'dude-gets-shot-shoulders-up.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after the animation, display the win
        self.delay(delay=myWait,handler=self.display_win)

    def display_win(self):
        # set some tracking
        self.game.increase_tracking('gunfightsWon')
        # up the rank if it's not full yet
        if self.game.show_tracking('rank') < 4:
            newrank = self.game.increase_tracking('rank')
        # if it is full, this bit is awkward
        else:
            newrank = 4
        ranks = ["STRANGER", "PARTNER", "DEPUTY", "SHERIFF", "MARSHAL"]
        textString3 = "YOUR RANK: " + ranks[newrank]
        values = ["500,000","750,000","1,000,000","1,500,000","2,000,000"]
        textString4 = "QUICKDRAWS WORTH: " + values[newrank]
        # award some points
        points = 750000
        self.game.score(points)
        # show the win screen
        textLine1 = dmd.TextLayer(64, 0, self.game.assets.font_7px_bold_az, "center", opaque=False).set_text("BAD GUY SHOT!")
        textLine2 = ep.pulse_text(self,64,9,ep.format_score(points))
        textLine3 = dmd.TextLayer(64, 20, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString3)
        textLine4 = dmd.TextLayer(64, 26, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(textString4)
        self.layer = dmd.GroupedLayer(128,32,[textLine1,textLine2,textLine3,textLine4])
        self.delay(delay=2,handler=self.end_gunfight)

    def lost(self):
        # drop the bad guy
        self.target_down(self.enemy)
        print "GUNFIGHT LOST IS KILLING THE MUSIC"
        self.game.sound.stop_music()
        # play a quote
        self.game.sound.play_voice(self.game.assets.quote_gunFail)
        # shut things down
        self.end_gunfight()

    def end_gunfight(self):
        self.layer = None
        self.game.bad_guys.update_lamps()
        # tidy up - set the gunfight status and bart brothers status to open
        self.game.set_tracking('gunfightStatus',"OPEN")
        self.game.set_tracking('bartStatus',"OPEN")
        # turn the main game music back on if a second level mode isn't running
        if not self.game.show_tracking('stackLevel',1):
            self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
            # turn off the level one flag
        self.game.set_tracking('stackLevel',False,0)
        # unload
        self.game.modes.remove(self.game.gunfight)

    def gunfight_pan(self,badGuys):
        # the intro animation
        anim = dmd.Animation().load(ep.DMD_PATH+'gunfight-pan.dmd')
        myWait = len(anim.frames) / 60 + 1.3
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=1)
        self.layer = animLayer
        self.delay(name="eyes",delay=myWait,handler=self.gunfight_intro_eyes,param=badGuys)

    def gunfight_intro_eyes(self,badGuys):
        # pop up the first bad guy and remove it from the array
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        # play the orchestra hit sound
        self.game.sound.play(self.game.assets.sfx_gunfightHit1)
        # show the eyes animation
        anim = dmd.Animation().load(ep.DMD_PATH+'gunfight-eyes.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after a delay pass to the hands with the pop order
        self.delay(name="hands",delay=1.1,handler=self.gunfight_intro_hands,param=badGuys)
        # and drop the current one
        self.delay(delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_hands(self,badGuys):
        # pop the second bad guy and remove it
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        self.game.sound.play(self.game.assets.quote_gunfightReady)
        # play the second orchestra hit
        self.game.sound.play(self.game.assets.sfx_gunfightHit2)
        # show the hands animation
        anim = dmd.Animation().load(ep.DMD_PATH+'gunfight-hands.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # after a delay pass to the feet with the pop order
        self.delay(name="boots",delay=1.1,handler=self.gunfight_intro_boots,param=badGuys)
        self.delay(delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_boots(self,badGuys):
        # pop the third bad guy
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        self.game.bad_guys.target_up(enemy)
        self.game.sound.play(self.game.assets.quote_gunfightSet)
        # play the orchestra hit
        self.game.sound.play(self.game.assets.sfx_gunfightHit3)
        # show the boots
        boots = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'gunfight-boots.dmd').frames[0])
        self.layer = boots
        # after a delay - pass to the final setp
        self.delay(name="draw",delay=1.1,handler=self.gunfight_intro_draw,param=badGuys)
        self.delay(delay=1.1,handler=self.game.bad_guys.target_down,param=enemy)

    def gunfight_intro_draw(self,badGuys):
        # pop the last bad guy
        enemy = badGuys.pop(0)
        print "POP ENEMY: " + str(enemy)
        # need this for the lost
        self.enemy = enemy
        self.game.bad_guys.target_up(enemy)
        # play the 4 bells
        self.game.sound.play(self.game.assets.sfx_gunfightBell)
        self.delay(delay=0.6,handler=self.game.play_remote_sound,param=self.game.assets.sfx_gunCock)
        # run the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'gunfight-boots.dmd')
        myWait = len(anim.frames) / 10.0
        animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
        self.layer = animLayer
        # pass one last time to the release
        self.delay(name="release",delay=myWait,handler=self.gunfight_release)

    def gunfight_release(self):
        # play the draw quote
        self.game.sound.play(self.game.assets.quote_gunfightDraw)
        # relase the post - hm. no way to know which one is up Oops. # todo fix that later
        text = dmd.TextLayer(28,8,self.game.assets.font_12px_az,"center",opaque=False).set_text("DRAW!",blink_frames=2)
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'gunfight-boots.dmd').frames[8])
        self.layer = dmd.GroupedLayer(128,32,[backdrop,text])
        # turn the GI back on
        self.game.set_tracking('lampStatus', "ON")
        self.game.gi_control("ON")
        self.game.update_lamps()
        # and turn on target guy
        #self.lamps[self.enemy].enable()  ## this shouldn't be needed with the lamps in this mode now
        print "DROP THE POST"
        self.posts[self.activeSide].disable()
        # set a named timer for gunfight lost
        self.delay(name="Gunfight Lost",delay=4,handler=self.lost)

