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
## A P-ROC Project by Eric Priepke, Copyright 2012
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The The Addams Family Tribute
##

from procgame import dmd,game
import ep
import random

class TAF_Tribute(ep.EP_Mode):
    """This is Just a Tribute """
    def __init__(self,game,priority):
        super(TAF_Tribute, self).__init__(game,priority)
        self.myID = "TAF Tribute"
        # switch value to raise if it gets hit
        self.bump = 25000
        self.running = False
        # for timer halting in saloon/jets
        self.halted = False

        # set up the pause text layer
        textString = "< COUSIN IT PAUSED >"
        textLayer = ep.EP_TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString,color=ep.GREEN)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"
        self.misses = [self.game.assets.dmd_tafItMiss1,self.game.assets.dmd_tafItMiss2]


    def mode_started(self):
        # switch value to start
        self.value = 100000
        self.total = 500000
        # timer value
        self.modeTimer = 20
        self.running = True
        # set up the default text layers
        self.timerLayer = ep.EP_TextLayer(0,0,self.game.assets.font_9px_az,"left",False)
        self.valueTitleLayer = ep.EP_TextLayer(80,0,self.game.assets.font_5px_AZ,"center",False).set_text("TARGET VALUE")
        self.valueLayer = ep.EP_TextLayer(80,6,self.game.assets.font_7px_az,"center",False).set_text(ep.format_score(self.value))
        self.totalTitleLayer = ep.EP_TextLayer(80,14,self.game.assets.font_7px_az,"center",False).set_text("IT TOTAL")
        self.totalLayer = ep.EP_TextLayer(80,22,self.game.assets.font_9px_az,"center",False).set_text(ep.format_score(self.total))
        self.intro()

    # switches
    # left quickdraws are cousin it
    def sw_leftQuickdrawTop(self,sw):
        self.hit_it()
    def sw_leftQuickdrawBottom(self,sw):
        self.hit_it()

    # switches that register values
    def sw_leftLoopBottom(self,sw):
        self.miss_it()
    def sw_leftRampEnter(self,sw):
        self.miss_it()
    def sw_minePopper_active_for_300ms(self,sw):
        self.miss_it()
    def sw_centerRampEnter(self,sw):
        self.miss_it()
    def sw_saloonGate(self,sw):
        self.miss_it()
    def sw_rightLoopBottom(self,sw):
        self.miss_it()
    def sw_rightRampEnter(self,sw):
        self.miss_it()

    # halt switches
    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_350ms(self,sw):
        print "Cousin It Mine Popper Register"
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_active_for_250ms(self,sw):
        print "Cousin It Saloon Popper Register"
        if not self.halted:
            self.halt_it()
        # if the mode is already halted, cancel any pending resume delay
        else:
            self.cancel_delayed("Resume")

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.delay("Resume",delay=1,handler=self.display_it,param="idle")

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.delay("Resume",delay=1,handler=self.display_it,param="idle")

    def intro(self,step=1):
        if step == 1:
            anim = self.game.dmd.assets.dmd_tafItIntro
            myWait = len(anim.frames) / 10.0
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=6)
            self.layer = animLayer
            self.delay(delay = myWait,handler=self.intro,param=2)
        if step == 2:
            textLayer1 = ep.EP_TextLayer(128,1,self.game.assets.font_9px_az,False).set_text("HIT COUSIN IT")
            textLayer2 = ep.EP_TextLayer(128,10,self.game.assets.font_9px_az,False).set_text("ALL TARGETS=" + str(ep.format_score(self.value)))
            textLayer3 = ep.EP_TextLayer(128,20,self.game.assets.font_9xp_az,False).set_text("'IT' INCREASES VALUE")
            border = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_singlePixelBorder.frames[0])
            combined = dmd.GroupedLayer(128,32,[border,textLayer1,textLayer2,textLayer3])
            transition = ep.EP_Transition(self,self.layer,combined,ep.EP_Transition.TYPE_CROSSFADE)
            self.delay(delay = 2, handler=self.get_going)

    def get_going(self):
        # release the ball
        if self.game.tribute_launcher.shot == 3:
            self.game.mountain.eject()
        else:
            self.game.coils.leftGunfightPost.disable()
        # unload the launcher
        self.game.tribute_launcher.unload()
        # start the music

        # start the display
        self.display_it("idle",startup = True)
        # start the timer
        self.modeTimer += 1
        self.time_it()

    def display_it(self,type=None,startup = False):
        self.cancel_delayed("Display")
        if type == "idle":
            anim = self.game.dmd.assets.dmd_tafItIdle
            myWait = len(anim.frames) / 10.0
            self.cousinLayer = dmd.AnimatedLayer(frames=anim.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        elif type == "miss":
            anim = self.misses[0]
            self.misses.reverse()
            myWait = len(anim.frames) / 10.0
            self.cousinLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        elif type == "hit":
            anim = self.game.dmd.assets.dmd_tafItHit
            myWait = len(anim.frames) / 10.0
            self.cousinLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        else:
            # if we didn't get a cue to change cousin it, we don't mess with him
            myWait = 0
        # build the layer
        combined = dmd.GroupedLayer(128,32,[self.cousinLayer,self.timerLayer,self.valueTitleLayer,self.valueLayer,self.totalTitleLayer,self.totalLayer])
        # turn on the layer - crossfade at startup
        if startup:
            transition = ep.EP_Transition(self,self.layer,combined,ep.EP_Transition.TYPE_CROSSFADE)
        else:
            self.layer = combined
        # set the delay for fixing it after a hit or a miss
        if myWait > 0:
            self.delay("Display",delay=myWait,handler=display_it,param="idle")

    def time_it(self):
        self.modeTimer -= 1
        if self.modeTimer <= 0:
            self.finish_it()
        else:
            self.timerLayer.set_text(str(self.modeTimer))
            self.delay("Mode Timer",handler=self.time_it)

    def hit_it(self):
        # on a hit, increase the value, and add the new value to the total and display the hit
        self.value += self.bump
        self.total += self.value
        self.totalLayer.set_text(ep.format_score(self.total))
        self.valueLayer.set_text(ep.format_score(self.value))
        self.display_it("hit")

    def miss_it(self):
        # on a miss award the current value and display the miss
        self.total += self.value
        self.totalLayer.set_text(ep.format_score(self.total))
        self.display_it("miss")

    def halt_it(self):
        if self.modeTimer <= 0:
            return
        print "HALTING COUSIN IT IN BUMPERS/MINE"
        self.cancel_delayed("Resume")
        # cancel delays
        self.cancel_delayed("Mode Timer")
        # do the halted delay
        self.layer = self.pauseView
        # set the flag
        self.halted = True

    def finish_it(self):
        textLayer1 = ep.EP_TextLayer(128,2,self.game.assets.font_9px_az,"center",opaque=True).set_text("COUSIN IT TOTAL")
        textLayer2 = ep.EP_TextLayer(128,14,self.game.assets.font_12px_az,"center",opaque=False).set_text(str(ep.format_score(self.total)))
        # score the points
        self.game.score(self.total)
        # set the music back to the main loop

        # then unload
        self.unload()