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
## This is a slightly modified version of the base PyProcgame score display
##
import ep
import locale
from procgame import dmd

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

class ScoreLayer(dmd.GroupedLayer):
    def __init__(self, width, height, mode):
        super(ScoreLayer, self).__init__(width, height, mode)
        self.myID = "Score Display"
        self.mode = mode
    def next_frame(self):
        """docstring for next_frame"""
        # Setup for the frame.
        self.mode.update_layer()
        return super(ScoreLayer, self).next_frame()


class ScoreDisplay(ep.EP_Mode):
    """:class:`ScoreDisplay` is a mode that provides a DMD layer containing a generic 1-to-4 player score display.
    To use :class:`ScoreDisplay` simply instantiate it and add it to the mode queue.  A low priority is recommended.

    When the layer is asked for its :meth:`~procgame.dmd.Layer.next_frame` the DMD frame is built based on
    the player score and ball information contained in the :class:`~procgame.game.GameController`.

    :class:`ScoreDisplay` uses a number of fonts, the defaults of which are included in the shared DMD resources folder.
    If a font cannot be found then the score may not display properly
    in some states.  Fonts are loaded using :func:`procgame.dmd.font_named`; see its documentation for dealing with
    fonts that cannot be found.

    You can substitute your own fonts (of the appropriate size) by assigning the font attributes after initializing
    :class:`ScoreDisplay`.
    """

    font_common = None
    """Font used for the bottom status line text: ``'BALL 1  FREE PLAY'``.  Defaults to Font07x5.dmd."""

    credit_string_callback = None
    """If non-``None``, :meth:`update_layer` will call it with no parameters to get the credit string (usually FREE PLAY or CREDITS 1 or similar).
    If this method returns the empty string no text will be shown (and any ball count will be centered).  If ``None``, FREE PLAY will be shown."""

    def __init__(self, game, priority, left_players_justify="right"):
        super(ScoreDisplay, self).__init__(game, priority)
        self.layer = ScoreLayer(128, 32, self)
        self.font_common = self.game.assets.font_07x5
        self.set_left_players_justify(left_players_justify)
        anim = self.game.assets.dmd_1pBurnCycle
        self.burnLayer1p = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=3)
        self.burnLayer1p.composite_op = "blacksrc"

    def tilted(self):
        pass

    def set_left_players_justify(self, left_players_justify):
        """Call to set the justification of the left-hand players' scores in a multiplayer game.
        Valid values for ``left_players_justify`` are ``'left'`` and ``'right'``."""
        if left_players_justify == "left":
            self.score_posns = { True: [(0, 0), (128, 0), (0, 11), (128, 11)], False: [(0, -1), (128, -1), (0, 16), (128, 16)] }
        elif left_players_justify == "right":
            self.score_posns = { True: [(75, 0), (128, 0), (75, 11), (128, 11)], False: [(52, -1), (128, -1), (52, 16), (128, 16)] }
        else:
            raise ValueError, "Justify must be right or left."
        self.score_justs = [left_players_justify, 'right', left_players_justify, 'right']

    def format_score(self, score):
        """Returns a string representation of the given score value.
        Override to customize the display of numeric score values."""
        if score == 0:
            return '00'
        else:
            return locale.format("%d", score, True)

    def font_for_score_single(self, score):
        """Returns the font to be used for displaying the given numeric score value in a single-player game."""
        if score <   1e10:
            return self.game.assets.font_score_x12
        elif score < 1e11:
            return self.game.assets.font_score_x11
        else:
            return self.game.assets.font_score_x10

    def font_for_score(self, score, is_active_player):
        """Returns the font to be used for displaying the given numeric score value in a 2, 3, or 4-player game."""
        if is_active_player:
            if score < 1e7:
                return self.game.assets.font_14x10,ep.YELLOW
            if score < 1e8:
                return self.game.assets.font_14x9,ep.YELLOW
            else:
                return self.game.assets.font_14x8,ep.YELLOW
        else:
            if score < 1e7:
                return self.game.assets.font_09x7,ep.DARK_BROWN
            if score < 1e8:
                return self.game.assets.font_09x6,ep.DARK_BROWN
            else:
                return self.game.assets.font_09x5,ep.DARK_BROWN

    def pos_for_player(self, player_index, is_active_player):
        return self.score_posns[is_active_player][player_index]

    def justify_for_player(self, player_index):
        return self.score_justs[player_index]

    def update_layer(self):
        """Called by the layer to update the score layer for the present game state."""
        self.layer.layers = []
        if len(self.game.players) <= 1:
            self.update_layer_1p()
        else:
            self.update_layer_4p()
        # Common: Add the "BALL X ... FREE PLAY" footer.
        common = dmd.TextLayer(128/2, 32-6, self.font_common, "center")

        if self.game.tournament:
            credit_str = 'TOURNAMENT'
        elif self.game.party_setting != 'Disabled':
            credit_str = 'PARTY MODE'
        else:
            credit_str = 'FREE PLAY'

        if self.credit_string_callback:
            credit_str = self.credit_string_callback()
        if self.game.ball == 0:
            common.set_text(credit_str)
        elif len(credit_str) > 0:
            common.set_text("BALL %d      %s" % (self.game.ball, credit_str))
        else:
            common.set_text("BALL %d" % (self.game.ball))
        self.layer.layers += [common]

    def update_layer_1p(self):
        if self.game.current_player() == None:
            score = 0 # Small hack to make *something* show up on startup.
        else:
            score = self.game.current_player().score
        layer = dmd.TextLayer(128/2, 5, self.font_for_score_single(score), "center")
        layer.set_text(self.format_score(score))
        self.layer.layers += [layer]
        ## add the burn layer
        self.layer.layers += [self.burnLayer1p]

    def update_layer_4p(self):
        for i in range(len(self.game.players[:4])): # Limit to first 4 players for now.
            score = self.game.players[i].score
            is_active_player = (self.game.ball > 0) and (i == self.game.current_player_index)
            font,myColor = self.font_for_score(score=score, is_active_player=is_active_player)
            pos = self.pos_for_player(player_index=i, is_active_player=is_active_player)
            justify = self.justify_for_player(player_index=i)
            layer = ep.EP_TextLayer(pos[0], pos[1], font, justify)
            layer.set_text(self.format_score(score),color=myColor)
            self.layer.layers += [layer]
        pass

    def mode_started(self):
        pass

    def mode_stopped(self):
        pass

    # Throwing the slam tilt in here so it's always watching
    ## SLAM TILT
    def sw_tilt_active(self,sw):
        # slam tilt switch
        self.game.interrupter.tilt_display(slam=True)

    # this is to try to catch if a ball should have launched when the door was open
    def sw_coinDoorClosed_active(self,sw):
        #print ("Checking ball count on door close")
        if self.game.trough.num_balls_in_play != 0:
            ball_count = self.game.trough.num_balls()
            if ball_count == 4:
                #print ("The trough is full, but there should be a ball in play. Stealth Launch")
                self.game.trough.launch_balls(1,stealth=True)
            # clear the saloon and mine too
            if self.game.switches.minePopper.is_active():
                self.game.mountain.eject()
            if self.game.switches.saloonPopper.is_active():
                self.game.saloon.kick()
