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
#
# This mode is just a display layer for the beans and franks
#
# Franks and Beans is a "Scoring Mode" like 2x playfield or others in the past.
# It has no goal. It should have no goal.  There is no "Frank" -- franks is
# another word for hot dogs.  This little goofy thing is a tribute to the movie
# Blazing Saddles.
#
from procgame import game, dmd
import ep

class FranksDisplay(ep.EP_Mode):
    """Game mode for controlling the skill shot"""
    def __init__(self, game,priority):
        super(FranksDisplay, self).__init__(game, priority)
        self.myID = "Beans And Franks Switches"
        self.running = False

    def ball_drained(self):
        if self.game.trough.num_balls_in_play == 0 and self.running:
            self.end()

    def mode_started(self):
        self.game.sound.play(self.game.assets.sfx_dinnerBell)
        self.game.modes.add(self.game.franks_switches)
        self.game.set_tracking('farted',True)
        self.running = True
        self.time = self.game.user_settings['Gameplay (Feature)']['Franks N Beans Time'] + 1
        # build the display
        background = dmd.FrameLayer(opaque=True,frame=self.game.assets.dmd_franksBackdrop.frames[0])
        self.scoreLine = ep.EP_TextLayer(48,1,self.game.assets.font_7px_az, "center", opaque= False)
        titleLine = ep.EP_TextLayer(48,12,self.game.assets.font_9px_az, "center", opaque=False).set_text("FRANKS N BEANS",color=ep.ORANGE)
        infoLine = ep.EP_TextLayer(48,24,self.game.assets.font_5px_AZ, "center", opaque=False).set_text("SWITCHES + " + ep.format_score(20000), color=ep.RED)
        self.timeLine = ep.EP_TextLayer(126,1,self.game.assets.font_5px_AZ, "right", opaque=False)
        self.timer_loop()
        self.update_display()
        combined = dmd.GroupedLayer(128,32,[background,titleLine,infoLine,self.scoreLine,self.timeLine])
        self.layer = combined

    def update_display(self):
        if self.time < 5:
            color = ep.RED
        elif self.time < 15:
            color = ep.ORANGE
        else:
            color = ep.YELLOW

        self.timeLine.set_text("TIME: " + str(self.time),color)
        p = self.game.current_player()
        scoreString = ep.format_score(p.score)
        self.scoreLine.set_text(scoreString,color=ep.BROWN)

    def timer_loop(self):
        self.time -= 1
        if self.time <= 0:
            self.end()
        else:
            self.update_display()
            self.delay("Timer",delay=1, handler=self.timer_loop)

    def end(self):
        self.running = False
        self.wipe_delays()
        self.game.franks_switches.end()
        self.unload()