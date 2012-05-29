##
## The Gold Mine Multiball
##

from procgame import *
import cc_modes
import ep
import random

class GoldMine(game.Mode):
    """Mining for great justice - For the Gold Mine Multiball, and ... ? """
    def __init__(self,game,priority):
        super(GoldMine, self).__init__(game,priority)


    def start_multiball(self):
        # for now we'll just print a thing
        print "MULTIBALL STARTING"
        # and then end
        # kill the music
        print "start multiball IS KILLING THE MUSIC"
        self.game.sound.stop_music()
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

        ## TEMPORARY - kick the ball out
        self.game.mine_toy.eject()
        # show it for a bit
        self.delay(delay=1.5,handler=self.end_multiball)


    def end_multiball(self):
        # clear the layer
        self.layer = None
        # set the status to open
        self.game.set_tracking('mineStatus','OPEN')
        print "MULTIBALL ENDED"
        # start the music back up
        self.game.base_game_mode.music_on(self.game.assets.music_mainTheme)
        # unload the mode
        self.game.modes.remove(self.game.gm_multiball)

