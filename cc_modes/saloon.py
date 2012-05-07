##
## This mode controls the saloon
## for now it's just popping the ball back out of the mine if it gets in there
##

from procgame import *
import cc_modes
import ep

class Saloon(game.Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(Saloon, self).__init__(game, priority)
        # setup the difficulty
        difficulty = self.game.user_settings['Gameplay (Feature)']['Bart Brothers Difficulty']
        # Easy version
        print "Difficulty is set to - " + difficulty
        if difficulty == 'Easy':
            self.hitsToDefeatBart = [1,2,3,4,5,6]
        # Hard version
        else:
            self.hitsToDefeatBart = [2,4,6,8,8,8]


    def sw_saloonPopper_closed_for_200ms(self,sw):
        print "PULSE THE KICKER FOR THE SALOON"

    def sw_saloonBart_active(self,sw):
        # a direct smack to el barto
        self.hit_bart()

    def sw_saloonGate_active(self,sw):
        # play the sound.
        # add some points
        self.game.score(2530)
        # exciting!


    def light_bounty(self):
        # set the tracking
        self.game.set_tracking('isBountyLit', True)
        # show something on the screen
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'stars-border.dmd').frames[0])
        topText = dmd.TextLayer(128/2, 4, self.game.assets.font_9px_az, "center", opaque=False).set_text("COLLECT BOUNTY",blink_frames=10)
        bottomText = dmd.TextLayer(128/2, 16, self.game.assets.font_9px_az, "center", opaque=False).set_text("IS LIT",blink_frames=10)
        self.layer = dmd.GroupedLayer(128,32,[backdrop,topText,bottomText])
        # play a voice clip about the bounty being ready
        self.game.sound.play_voice(self.game.assets.quote_bountyLit)
        # lights and whatnot
        self.delay(delay=1.6,handler=self.clear_layer)

    def collect_bounty(self):
        # TODO award the prize
        # turn off the tracking
        self.game.set_tracking('isBountyLit', False)


    def hit_bart(self):
        # play the sound
        # play a quote appropriate to the current bart
        # flash the light and move the dudes
        # register the
        # is he defeated? need to light gunfight?
        pass

    def clear_layer(self):
        self.layer = None