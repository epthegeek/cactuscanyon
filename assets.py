from procgame import *


class Assets():

    def __init__(self, game):

        self.game = game

        # Paths
        self.lampshows_path = "lampshows/"
        self.sounds_path = "sounds/"
        self.sfx_path = "sounds/sfx/"
        self.music_path = "sounds/music/"
        self.quotes_path = "sounds/quotes/"
        self.dmd_path = "dmd/"

        # CC Fonts
        # _az = All numerals, letters, and lower case
        # _AZ = All numerals and upper case letters
        # _score = Numerals only
        self.font_5px_AZ = dmd.Font(self.dmd_path + "Font_3_CactusCanyon.dmd")
        self.font_5px_bold_AZ = dmd.Font(self.dmd_path + "Font_21_CactusCanyon.dmd")

        self.font_5px_bold_AZ_outline = dmd.Font(self.dmd_path + "Font_21_mask_CactusCanyon.dmd")
        self.font_5px_bold_AZ_outline.tracking = -1
        self.font_5px_bold_AZ_outline.composite_op = "blacksrc"

        self.font_6px_az = dmd.Font(self.dmd_path + "Font_19_CactusCanyon.dmd")

        self.font_7px_alt_az = dmd.Font(self.dmd_path + "Font_1_CactusCanyon.dmd")
        self.font_7px_az = dmd.Font(self.dmd_path + "Font_2_CactusCanyon.dmd")
        self.font_7px_score = dmd.Font(self.dmd_path + "Font_5_CactusCanyon.dmd")
        self.font_7px_extra_thin_score = dmd.Font(self.dmd_path + "Font_10_CactusCanyon.dmd")
        self.font_7px_thin_score = dmd.Font(self.dmd_path + "Font_4_CactusCanyon.dmd")
        self.font_7px_wide_score = dmd.Font(self.dmd_path + "Font_6_CactusCanyon.dmd")
        self.font_7px_bold_az = dmd.Font(self.dmd_path + "Font_14_CactusCanyon.dmd")

        self.font_9px_az = dmd.Font(self.dmd_path + "Font_15_CactusCanyon.dmd")

        self.font_12px_az = dmd.Font(self.dmd_path + "Font_16_CactusCanyon.dmd")

        self.font_13px_score = dmd.Font(self.dmd_path + "Font_8_CactusCanyon.dmd")
        self.font_13px_extra_thin_score = dmd.Font(self.dmd_path + "Font_11_CactusCanyon.dmd")
        self.font_13px_thin_score = dmd.Font(self.dmd_path + "Font_7_CactusCanyon.dmd")
        self.font_13px_wide_score = dmd.Font(self.dmd_path + "Font_9_CactusCanyon.dmd")

        self.font_15px_az = dmd.Font(self.dmd_path + "Font_17_CactusCanyon.dmd")

        self.font_15px_az_outline = dmd.Font(self.dmd_path + "Font_17_mask_CactusCanyon.dmd")
        self.font_15px_az_outline.tracking = -1
        self.font_15px_az_outline.composite_op = "blacksrc"

        self.font_17px_score = dmd.Font(self.dmd_path + "Font_12_CactusCanyon.dmd")

        #self.font_score_x12 = dmd.Font(self.dmd_path + "Font_Score_12_CactusCanyon.dmd")
        self.font_score_x12 = dmd.Font(self.dmd_path + "Font_12b_CactusCanyon.dmd")
        self.font_score_x11 = dmd.Font(self.dmd_path + "Font_12c_CactusCanyon.dmd")
        self.font_score_x10 = dmd.Font(self.dmd_path + "Font_12d_CactusCanyon.dmd")

        self.font_20px_az = dmd.Font(self.dmd_path + "Font_18_CactusCanyon.dmd")

        self.font_skillshot = dmd.Font(self.dmd_path + "Font_20_CactusCanyon.dmd")


        # CC Sounds
        # Sound Effects
        self.sfx_banjoTrillUp = 'sfx_banjoTrillUp' ; self.game.sound.register_sound(self.sfx_banjoTrillUp, self.sfx_path + "622-banjo-trill-up.wav")
        self.sfx_banjoTrillDown = 'sfx_banjoTrillDown' ; self.game.sound.register_sound(self.sfx_banjoTrillDown, self.sfx_path + "623-banjo-trill-down.wav")
        self.sfx_banjoTaDa = 'sfx_banjoTaDa' ; self.game.sound.register_sound(self.sfx_banjoTaDa, self.sfx_path + "624-banjo-ta-da.wav")
        self.sfx_blow = 'sfx_blow' ; self.game.sound.register_sound(self.sfx_blow, self.sfx_path + "169-sfx-blow-on-gun.wav")
        self.sfx_cactusMash = 'sfx_cactusMash' ; self.game.sound.register_sound(self.sfx_cactusMash, self.sfx_path + "235-bonus-cactus-mash.wav")
        self.sfx_explosion1 = 'sfx_explosion1' ; self.game.sound.register_sound(self.sfx_explosion1, self.sfx_path + "105-sfx-explosion-1.wav")
        self.sfx_explosion11 = 'sfx_explosion2' ; self.game.sound.register_sound(self.sfx_explosion11, self.sfx_path + "257-sfx-explosion-11.wav")
        self.sfx_explosion17 = 'sfx_explosion17' ; self.game.sound.register_sound(self.sfx_explosion17, self.sfx_path + "341-sfx-explosion-17.wav")
        self.sfx_fallAndCrash1 = 'sfx_fallAndCrash1' ; self.game.sound.register_sound(self.sfx_fallAndCrash1, self.sfx_path + "101-sfx-fall-and-crash-1.wav")
        self.sfx_flourish6 = 'sfx_flourish6' ; self.game.sound.register_sound(self.sfx_flourish6, self.sfx_path + "032-flourish-6.wav")
        self.sfx_flourish7 = 'sfx_flourish7' ; self.game.sound.register_sound(self.sfx_flourish7, self.sfx_path + "034-flourish-7-Horns.wav")
        self.sfx_grinDing = 'sfx_grinDing' ; self.game.sound.register_sound(self.sfx_grinDing, self.sfx_path + "117-sfx-grin-ding.wav")
        self.sfx_horseYell = 'sfx_horseYell' ; self.game.sound.register_sound(self.sfx_horseYell, self.sfx_path + "115-sfx-horse-running-with-yell.wav")
        self.sfx_rightRampEnter = 'sfx_rightRampEnter' ; self.game.sound.register_sound(self.sfx_rightRampEnter, self.sfx_path + "129-sfx-right-ramp-enter.wav")
        self.sfx_leftRampEnter = 'sfx_leftRampEnter' ; self.game.sound.register_sound(self.sfx_leftRampEnter, self.sfx_path + "407-sfx-river-ramp-splash.wav")
        self.sfx_leftLoopEnter = 'sfx_leftLoopEnter' ; self.game.sound.register_sound(self.sfx_leftLoopEnter, self.sfx_path + "179-woosh-with-horse-running.wav")
        self.sfx_rattlesnake = 'sfx_rattlesnake' ; self.game.sound.register_sound(self.sfx_rattlesnake, self.sfx_path + "221-rattlesnake.wav")
        self.sfx_skillShotWoosh = 'sfx_skillShotWoosh' ; self.game.sound.register_sound(self.sfx_skillShotWoosh, self.sfx_path + "393-skillshot-woosh.wav")
        self.sfx_thrownCoins = 'sfx_thrownCoins' ; self.game.sound.register_sound(self.sfx_thrownCoins, self.sfx_path + "137-sfx-thrown-coins.wav")
        # Quotes
        self.quote_pollyOhHowBrave = 'quote_pollyOhHowBrave' ; self.game.sound.register_sound(self.quote_pollyOhHowBrave, self.quotes_path + "850-polly-ooh-how-brave.wav")
        self.quote_pollyThankYou = 'quote_pollyThankYou' ; self.game.sound.register_sound(self.quote_pollyThankYou,self.quotes_path + "835-polly-thank-you.wav")
        self.quote_pollyHeadedForFalls = 'quote_pollyHeadedForFalls' ; self.game.sound.register_sound(self.quote_pollyHeadedForFalls, self.quotes_path + "829-polly-were-headed-for-the-falls.wav")
        self.quote_pollyGoinOver = 'quote_pollyGoinOver' ; self.game.sound.register_sound(self.quote_pollyGoinOver, self.quotes_path + "830-polly-were-going-over-the-falls.wav")
        self.quote_welcomes = 'quote_welcomes'
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1202-prospector-welcome-to-cactus-canyon.wav")
        #self.quote_mayorWelcome = 'quote_mayorWelcome';
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1101-mayor-dewey-cheetum-at-your-service.wav")
        #self.quote_undertakerWelcome = 'quote_undertakerWelcome' ;
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1324-undertaker-welcome-to-cactus-canyon.wav")
        self.quote_leaderBartLaugh2 = 'quote_leaderBartLaugh2' ; self.game.sound.register_sound(self.quote_leaderBartLaugh2, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.quote_playerTwo = 'quote_playerTwo' ; self.game.sound.register_sound(self.quote_playerTwo, self.quotes_path + "856-polly-player-two.wav")
        self.quote_playerThree = 'quote_playerThree' ; self.game.sound.register_sound(self.quote_playerThree, self.quotes_path + "857-polly-player-three.wav")
        self.quote_playerFour = 'quote_playerFour' ; self.game.sound.register_sound(self.quote_playerFour, self.quotes_path + "858-polly-player-four.wav")
        self.quote_mayorMyMoneysInThere = 'quote_mayorMyMoneysInThere' ; self.game.sound.register_sound(self.quote_mayorMyMoneysInThere, self.quotes_path + "1134-mayor-well-do-somethin-my-moneys-in-there.wav")
        self.quote_mayorFineRideSir = 'quote_mayorFineRideSir' ; self.game.sound.register_sound(self.quote_mayorFineRideSir, self.quotes_path + "1187-mayor-a-fine-ride-sir.wav")
        self.quote_prospectorGottaHurt = 'quote_prospectorGottaHurt' ; self.game.sound.register_sound(self.quote_prospectorGottaHurt, self.quotes_path + "1254-prospector-oh-boy-thats-gotta-hurt.wav")
        # Music
        self.music_shooterLaneGroove = 'music_shooterLaneGroove' ; self.game.sound.register_music(self.music_shooterLaneGroove, self.music_path + "005-shooter-lane-groove.wav")
        self.music_mainTheme = 'music_mainTheme' ; self.game.sound.register_music(self.music_mainTheme, self.music_path + "002-song-starting-gameplay.wav")

        # Lampshows

        # DMD Animations
        self.anim_bankRampOne = self.dmd_path + "bank-explodes.dmd"
        self.anim_bankRampTwo = self.dmd_path + "bank-sherrif-arrives.dmd"
        self.anim_bankRampFour = self.dmd_path + "bank-victory-animation.dmd"
        self.anim_sheriffPan = self.dmd_path + "sheriff-pan.dmd"
        self.anim_increaseBonusX = self.dmd_path + "bonus-cactus-mash.dmd"
        self.anim_horseChase = self.dmd_path + "horse-chase.dmd"
        self.anim_horseDrag = self.dmd_path + "horse-drag.dmd"
        self.anim_goodShot = self.dmd_path + "shot-bottles-animation.dmd"
        self.anim_gunslinger = self.dmd_path + "shot-candles-animation.dmd"
        self.anim_marksman1 = self.dmd_path + "shot-card-animation.dmd"
        self.anim_marksman2 = self.dmd_path + "smoking-card-loop.dmd"
        self.anim_riverChase = self.dmd_path + "river-chase.dmd"

        self.anim_ballOneLocked = self.dmd_path + "ball-one-locked.dmd"

        # Shared Paths
        self.shared_sound_path = "shared/sound/"
        self.shared_dmd_path = "shared/dmd/"

        # Shared Fonts
        self.font_tiny7 = dmd.Font(self.shared_dmd_path + "04B-03-7px.dmd")
        self.font_jazz18 = dmd.Font(self.shared_dmd_path + "Jazz18-18px.dmd")
        self.font_18x12 = dmd.Font(self.shared_dmd_path + "Font18x12.dmd")
        self.font_18x11 = dmd.Font(self.shared_dmd_path + "Font18x11.dmd")
        self.font_14x10 = dmd.Font(self.shared_dmd_path + "Font14x10.dmd")
        self.font_14x9 = dmd.Font(self.shared_dmd_path + "Font14x9.dmd")
        self.font_14x8 = dmd.Font(self.shared_dmd_path + "Font14x8.dmd")
        self.font_09Bx7 = dmd.Font(self.shared_dmd_path + "Font09Bx7.dmd")
        self.font_09x7 = dmd.Font(self.shared_dmd_path + "Font09x7.dmd")
        self.font_09x6 = dmd.Font(self.shared_dmd_path + "Font09x6.dmd")
        self.font_09x5 = dmd.Font(self.shared_dmd_path + "Font09x5.dmd")
        self.font_07x4 = dmd.Font(self.shared_dmd_path + "Font07x4.dmd")
        self.font_07x5 = dmd.Font(self.shared_dmd_path + "Font07x5.dmd")

        # Shared Animations
        self.anim_proclogo = dmd.Animation().load(self.shared_dmd_path + "Splash.dmd")

        # Shared Sounds
        #self.game.sound.register_sound('service_enter', self.shared_sound_path + "menu_in.wav")
        #self.game.sound.register_sound('service_exit', self.shared_sound_path + "menu_out.wav")
        #self.game.sound.register_sound('service_next', self.shared_sound_path + "next_item.wav")
        #self.game.sound.register_sound('service_previous', self.shared_sound_path + "previous_item.wav")
        #self.game.sound.register_sound('service_switch_edge', self.shared_sound_path + "switch_edge.wav")
        #self.game.sound.register_sound('service_save', self.shared_sound_path + "save.wav")
        #self.game.sound.register_sound('service_cancel', self.shared_sound_path + "cancel.wav")
