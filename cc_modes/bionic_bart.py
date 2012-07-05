from procgame import *
import cc_modes
import ep
import random

class BionicBart(game.Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(BionicBart, self).__init__(game,priority)
        self.hitsToDefeat = self.game.user_settings['Gameplay (Feature)']['Shots to defeat Bionic Bart']
        self.shotModes = [self.game.left_loop,self.game.right_loop,self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]

    # TODO - need a taunt timer, display updater, switch handling, yadda yadda

    def ball_drained(self):
        # if we lose all the balls the battle is lost
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('bionicStatus') == "RUNNING":
            self.bionic_failed()

    def mode_started(self):
        # set the stack level
        self.game.set_tracking('stackLevel',True,3)
        # set up the standard display stuff
        self.idleLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'bionic-combo.dmd').frames[0])
        script = []
        talkLayer1 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'bionic-combo.dmd').frames[1])
        script.append({'layer':talkLayer1,'seconds':0.3})
        talkLayer2 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'bionic-combo.dmd').frames[2])
        script.append({'layer':talkLayer2,'seconds':0.3})
        self.talkingLayer = dmd.ScriptedLayer(128,32,script)
        script = []
        hurtLayer1 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'bionic-combo.dmd').frames[3])
        script.append({'layer':hurtLayer1,'seconds':0.3})
        hurtLayer2 = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'bionic-combo.dmd').frames[4])
        script.append({'layer':hurtLayer2,'seconds':0.3})
        self.whineLayer = dmd.ScriptedLayer(128,32,script)
        self.title = dmd.TextLayer(46, 3, self.game.assets.font_15px_bionic, "center", opaque=False).set_text("BIONIC BART")
        self.title2 = dmd.TextLayer(46,20, self.game.assets.font_6px_az, "center", opaque=False).set_text("CHALLENGES YOU!")
        self.title2.composite_op = "blacksrc"

        # intialize some layers
        self.set_bart_layer(self.idleLayer)
        self.set_action_line()
        self.set_status_line()

        self.loaded = False
        self.shots = 0
        self.shotsToLoad = 1
        self.hits = 0

    # switches
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

    def process_shot(self,shot):
        if self.loaded == False:
            self.shots += 1
            # if we're up to the required shots, load the weapon
            if self.shots >= self.shotsToLoad:
                self.load_weapon()
            # otherwise tick up the shots and update the status
            else:
                amount = self.shotsToLoad - self.shots
                self.set_status_line(amount,"LOAD")
        # if we're already loaded, then what?
        else:
            # todo something needs to go here
            pass

    def start_bionic(self):
        # kill the music
        self.game.sound.stop_music()
        # kick off the intro
        self.intro(1)

    def intro(self,step):
        # initial display/sound
        # step 1
        if step == 1:
            # play the 'deal with this' quote
            duration = self.game.sound.play(self.game.assets.quote_bionicIntroQuote)
            self.delay(delay=duration,handler=self.intro,param=2)
        if step == 2:
        # load up the lightning
            anim = dmd.Animation().load(ep.DMD_PATH+'cloud-lightning.dmd')
            # math out the wait
            myWait = len(anim.frames) / 10.0
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 6
            # keyframe sounds
            animLayer.add_frame_listener(2,self.game.play_remote_sound,param=self.game.assets.sfx_lightning1)
            animLayer.add_frame_listener(2,self.game.lightning,param="top")
            animLayer.add_frame_listener(3,self.game.lightning,param="left")
            animLayer.add_frame_listener(6,self.game.play_remote_sound,param=self.game.assets.sfx_lightning2)
            animLayer.add_frame_listener(6,self.game.lightning,param="top")
            animLayer.add_frame_listener(7,self.game.lightning,param="left")
            animLayer.add_frame_listener(10,self.game.play_remote_sound,param=self.game.assets.sfx_lightningRumble)
            animLayer.add_frame_listener(10,self.game.lightning,param="top")
            animLayer.add_frame_listener(11,self.game.lightning,param="right")
            # turn it on
            self.layer = animLayer
            self.delay(delay=myWait,handler=self.intro,param=3)
        if step == 3:
            combined = dmd.GroupedLayer(128,32,[self.idleLayer,self.title,self.title2])
            self.layer = combined
            self.delay(delay=1,handler=self.intro,param=4)
        if step == 4:
            # play the intro quote
            duration = self.game.sound.play(self.game.assets.quote_introBionicBart)
            # show the talking layer
            combined = dmd.GroupedLayer(128,32,[self.talkingLayer,self.title,self.title2])
            self.layer = combined
            # loop back for step 3
            self.delay(delay=duration,handler=self.intro,param=5)
        if step == 5:
            combined = dmd.GroupedLayer(128,32,[self.idleLayer,self.title,self.title2])
            self.layer = combined
            duration = self.game.sound.play(self.game.assets.music_bionicBartIntro)
            # loop back to start the music
            self.delay(delay = duration, handler=self.intro,param=6)
        if step == 6:
            # start the music
            self.game.base_game_mode.music_on(self.game.assets.music_bionicBart)
            self.update_display()

    def update_display(self):
        # set up the display during multiball
        # whateve the current bart layer is, default is idle
        backdrop = self.bartLayer
        # title line
        titleLine = dmd.TextLayer(46, -1, self.game.assets.font_5px_AZ, "center", opaque=False).set_text("BIONIC BART")
        # score line
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        scoreLine = dmd.TextLayer(46, 5, self.game.assets.font_9px_az, "center", opaque=False).set_text(scoreString,blink_frames=4)
        scoreLine.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[backdrop,titleLine,scoreLine,self.actionLine,self.statusLine])
        self.layer = combined
        # loop back in .2 to update
        self.delay(name="Display",delay=0.2,handler=self.update_display)

    def set_bart_layer(self,layer):
        self.bartLayer = layer

    def set_action_line(self,string="LOAD THE WEAPON"):
        self.actionLine = dmd.TextLayer(46, 16, self.game.assets.font_7px_az, "center", opaque=False).set_text(string)
        self.actionLine.composite_op = "blacksrc"

    def set_status_line(self,amount=1,style="LOAD"):
        if amount > 1:
            shotWord = "SHOTS"
            hitWord = "HITS"
        else:
            shotWord = "SHOT"
            hitWord = "HIT"
        if style == "LOAD":
            theWord = shotWord
            theEnd = "LOAD"
        else:
            theWord = hitWord
            theEnd = "DEFEAT"
        string = str(amount) + " " + theWord + " TO " + theEnd
        self.statusLine = dmd.TextLayer(46, 24, self.game.assets.font_5px_AZ, "center", opaque=False).set_text(string)

    def load_weapon(self):
        amount = self.hitsToDefeat - self.hits
        self.set_status_line(amount, "HIT")
        self.set_action_line("HIT BIONIC BART")
        # set the flag
        self.loaded = True
        # update lamps
        self.game.saloon.update_lamps()
        for shot in self.shotModes:
            shot.update_lamps()
        # next round takes more hits
        self.shotsToLoad += 1

    def bionic_defeated(self):
        # VICTOLY!
        # set bart flag to dead
        self.game.set_tracking('bionicStatus', "DEAD")
        # light high noon
        self.game.badge.light_high_noon()

        # TODO - lots. points? final display? WAT?

        self.finish_up()

    def bionic_failed(self):
        # Lose the balls during a bionic fight and you lose
        # reset all the star status
        self.game.badge.reset()
        # set bionic
        self.game.set_tracking('bionicStatus',"OPEN")

        self.finish_up()

    def finish_up(self):
        # as is tradition
        # clear the stack level
        self.game.set_tracking('stackLevel',False,3)
        # turn the main music back on
        self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        # unload the mode
        self.game.modes.remove(self.game.bionic)

    def clear_layer(self):
        self.layer = None
