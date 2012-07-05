from procgame import *
import cc_modes
import ep
import random

class BionicBart(game.Mode):
    """Gunfight code """
    def __init__(self,game,priority):
        super(BionicBart, self).__init__(game,priority)


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

    # switches
     # ramps
     # loops
    # process - bart hits here? seems like a lot of redundant

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
