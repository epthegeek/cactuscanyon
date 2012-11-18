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


from procgame import dmd
import ep

class MoveYourTrain(ep.EP_Mode):
    def __init__(self,game,priority):
        super(MoveYourTrain, self).__init__(game,priority)
        # train idle animation
        self.animIdle = self.game.assets.dmd_trainOnTracks
        # train moving right animation
        self.animRight = self.game.assets.dmd_trainMoveRight
        # train moving left animation
        self.animLeft = self.game.assets.dmd_trainMoveLeft
        # set the train animation wait
        self.animWait = len(self.animRight.frames) / 10.0
        # default the train layer
        self.set_train_layer()
        # empty track layer
        self.emptyTrackLayer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_emptyTrack.frames[0])
        self.emptyTrackLayer.composite_op = "blacksrc"
        self.trainOffset = 0
        self.running = False

    def mode_started(self):
        self.postUse = False
        # move the train to the middle of the track
        # set a stop point for the encoder
        self.game.train.stopAt = 100
        print "Stop train at value: " + str(self.game.train.stopAt)
        # move the train forward
        self.game.train.fast_forward()
        # set the horizontal offset to starting point
        self.set_position()
        # set the time for the mode
        self.timeLimit = self.game.user_settings['Gameplay (Feature)']['Move Your Train Timer']
        # set the status to ready
        self.game.set_tracking("mytStatus", "READY")
        self.shots = 0

    def ball_drained(self):
        if self.running:
            if self.game.trough.num_balls_in_play == 0:
                self.end()

    ## Switches
    # left shots

    def sw_leftLoopTop_active(self,sw):
        self.move_train("left")

    def sw_leftRampEnter_active(self,sw):
        self.move_train("left")

    def sw_minePopper_active_for_390ms(self,sw):
        self.move_train("left")

    # right shots
    def sw_rightLoopTop_active(self,sw):
        # this only counts if bart is not moving.  stupid bart.
        if not self.game.bart.moving:
            self.move_train("right")

    def sw_rightRampMake_active(self,sw):
        self.move_train("right")

    def sw_saloonPopper_active_for_290ms(self,sw):
        self.move_train("right")

    # center shot
    def sw_centerRampMake_active(self,sw):
        self.move_train("center")

    def start(self,postTrap = False,side=0):
        if postTrap:
            self.postUse = True
            # raise the right post to hold the ball - to trap the ball after the skillshot win
            self.POSTS[side].patter(on_time=4,off_time=12,original_on_time=30)
        # set the running flag
        self.running = True
        # set the status
        self.game.set_tracking("mytStatus", "RUNNING")
        self.intro_display(1,side)

    def intro_display(self,step = 1,side =0):
        if step == 1:
            moveLayer = self.game.showcase.make_string(1,3,0,text="MOVE")
            self.layer = moveLayer
            self.delay(delay=1,handler=self.intro_display,param=2)
        if step == 2:
            yourLayer = self.game.showcase.make_string(1,3,0,text="YOUR")
            self.layer = yourLayer
            self.delay(delay=1,handler=self.intro_display,param=3)
        if step == 3:
            trainLayer = self.game.showcase.make_string(1,3,0,text="TRAIN")
            self.layer = trainLayer
            self.delay(delay=1,handler=self.get_going,param=side)

    def get_going(self,side):
        # update the display
        self.main_display()
        # drop the post and/or kick the ball
        for post in self.POSTS:
            post.disable()
        if not self.postUse:
            self.game.saloon.kick()
        else:
            self.postUse = False

    def main_display(self):
        # flush any queued display updates
        self.cancel_delayed("Display")
        # the main train on the tracks display - called to refresh any time the train moves
        combined = dmd.GroupedLayer(128,32,[self.emptyTrackLayer,self.trainLayer])
        combined.composite_op = "blacksrc"
        self.layer = combined

    def move_display(self,direction):
        # set the train layer
        if direction == "left":
            self.set_train_layer("left",self.trainOffset)
        elif direction == "right":
            self.set_train_layer("right",self.trainOffset)
        # update the main display
        self.main_display()
        # update the offset position
        if direction == "left":
            self.trainOffset -= 20
        elif direction == "right":
            self.trainOffset += 20
        # play a chugg sound
        self.game.sound.play(self.game.assets.sfx_centerRampEnter,loops=1)
        print "TRAIN OFFSET: " + str(self.trainOffset)
        # four movements in one direction is win
        if self.trainOffset == 80 or self.trainOffset == -80:
            self.delay(delay=self.animWait,handler=self.win)
        else:
            # set a delay to go back to idle for all other cases
            self.delay(name="Display",delay=self.animWait,handler=self.idle_display)

    def move_train(self,direction):
        print "TRAIN STATUS:" + str(self.game.train.inMotion)
        # if we're not currently moving, then we can move again - tweak for running in fakepinproc?
        if not self.game.train.inMotion or self.game.fakePinProc:
            # increase the shots taken
            self.shots += 1
            # if shots divisible by 10, taunt
            if self.shots % 10 == 0:
                self.game.sound.play(self.game.assets.quote_mytTaunt)
            self.game.train.stopAt = 20
            print "Stop train at value: " + str(self.game.train.stopAt)
            if direction == "left":
                self.move_display("left")
                self.game.train.fast_forward()
            if direction == "right":
                self.move_display("right")
                self.game.train.fast_reverse()
            if direction == "center":
                if self.trainOffset > 0:
                    self.move_display("right")
                    self.game.train.fast_reverse()
            elif self.trainOffset < 0:
                    self.move_display("left")
                    self.game.train.fast_forward()
            else:
                self.game.sound.play(self.game.assets.sfx_trainWhistle)


    def idle_display(self):
        # set the train layer to idle
        self.set_train_layer("idle",self.trainOffset)
        # blow the wistle
        self.game.sound.play(self.game.assets.sfx_trainWhistle)
        # update the display
        self.main_display()

    def set_train_layer(self,type="idle",offset = 0):
        # for switching betwen the three train layers
        if type == "idle":
            self.trainLayer = dmd.AnimatedLayer(frames=self.animIdle.frames,hold=False,opaque=False,repeat=True,frame_time=6)
        if type == "left":
            self.trainLayer = dmd.AnimatedLayer(frames=self.animLeft.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        if type == "right":
            self.trainLayer = dmd.AnimatedLayer(frames=self.animRight.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        # move the layer to the appropriate spot
        self.trainLayer.set_target_position(offset,0)
        self.trainLayer.composite_op = "blacksrc"

    def set_position(self,value=0):
        # for setting the offset for the train layers
        self.trainOffset = value

    def win(self):
        duration = self.game.sound.play(self.game.assets.sfx_longTrainWhistle)
        self.delay(delay = duration,handler=self.game.sound.play,param=self.game.assets.sfx_cheers)
        textString = "TRAIN MOVED IN " + str(self.shots) + " SHOTS"
        textLine = dmd.TextLayer(64, 1, self.game.assets.font_5px_AZ, "center", opaque=True).set_text(textString)
        # calculate the score
        # four shots is a perfect score - so we take off 4 shots
        self.shots -= 4
        # a perfect score is 1 million - every additional shot costs 50,000, which makes a 100,000 loss for each due to the 2x nature of it - with a floor of 200,000
        score = 1000000 - (50000 * self.shots)
        if score <= 0:
            score = 200000
        pointsLine = dmd.TextLayer(64, 10, self.game.assets.font_17px_score, "center", opaque=False).set_text(str(ep.format_score(score)),blink_frames = 8)
        self.game.score(score)
        combined = dmd.GroupedLayer(128,32,[textLine,pointsLine])
        self.layer = combined
        # end after 2 seconds
        self.delay(delay=2,handler=self.end)

    def end(self):
        print "Ending Move Your Train"
        self.clear_layer()
        # turn off the running flag
        self.running = False
        # reset the train
        self.game.train.stop_at = 0
        self.game.train.reset_toy(type=2)
        # turn the status to off
        self.game.set_tracking("mytStatus", "OPEN")
        # unload
        self.unload()
