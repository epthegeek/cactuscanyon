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

## This assets file is used to pre-load all the sound and dots when the program launches
## That way, everything is in ram and readily accessible with no overhead when you need to use it

from procgame import *
import os
import ep

curr_file_path = os.path.dirname(os.path.abspath( __file__ ))

class Assets():

    def __init__(self, game):

        self.game = game
        color_desktop = self.game.color_desktop
        print "Color Desktop Assets: " + str(color_desktop)

        # Paths
        self.lampshows_path = curr_file_path + "/lampshows/"
        self.sounds_path = curr_file_path + "/sounds/"
        self.sfx_path = curr_file_path + "/sounds/sfx/"
        self.music_path = curr_file_path + "/sounds/music/"
        self.quotes_path = curr_file_path + "/sounds/quotes/"
        self.dmd_path = curr_file_path + "/dmd/"

        # CC Fonts
        # _az = All numerals, letters, and lower case
        # _AZ = All numerals and upper case letters
        # _score = Numerals only
        self.font_5px_AZ = ep.ColorFont(self.dmd_path + "Font_3_CactusCanyon.dmd")
        self.font_5px_AZ.make_colors([ep.GREY,ep.GREEN,ep.DARK_GREEN,ep.ORANGE,ep.YELLOW,ep.BROWN,ep.DARK_BROWN,ep.MAGENTA,ep.DARK_RED,ep.PURPLE,ep.RED])
        self.font_5px_AZ_inverted = dmd.Font(self.dmd_path + "Font_3_CactusCanyon_inverted.dmd")
        self.font_5px_bold_AZ = ep.ColorFont(self.dmd_path + "Font_21_CactusCanyon.dmd")
        self.font_5px_bold_AZ.make_colors([ep.BLUE,ep.YELLOW,ep.MAGENTA,ep.CYAN,ep.GREEN,ep.DARK_GREEN,ep.ORANGE,ep.RED,ep.BROWN,ep.DARK_BROWN])

        self.font_5px_bold_AZ_outline = ep.ColorFont(self.dmd_path + "Font_21_mask_CactusCanyon.dmd")
        self.font_5px_bold_AZ_outline.make_colors([ep.DARK_GREEN])
        self.font_5px_bold_AZ_outline.tracking = -1
        self.font_5px_bold_AZ_outline.composite_op = "blacksrc"

        self.font_6px_az = ep.ColorFont(self.dmd_path + "Font_19_CactusCanyon.dmd")
        self.font_6px_az.make_colors([ep.GREEN,ep.YELLOW,ep.RED,ep.DARK_RED,ep.MAGENTA])
        self.font_6px_az_inverse = ep.ColorFont(self.dmd_path + "Font_Custom_6px.dmd")
        self.font_6px_az_inverse.make_colors([ep.GREEN,ep.BROWN,ep.MAGENTA,ep.BLUE,ep.YELLOW,ep.RED])
        self.font_6px_az_inverse.composite_op = "blacksrc"

        self.font_7px_alt_az = dmd.Font(self.dmd_path + "Font_1_CactusCanyon.dmd")
        self.font_7px_az = ep.ColorFont(self.dmd_path + "Font_2_CactusCanyon.dmd")
        self.font_7px_az.make_colors([ep.GREEN,ep.MAGENTA,ep.YELLOW,ep.ORANGE,ep.RED])
    #    self.font_7px_score = dmd.Font(self.dmd_path + "Font_5_CactusCanyon.dmd")
    #    self.font_7px_extra_thin_score = dmd.Font(self.dmd_path + "Font_10_CactusCanyon.dmd")
    #    self.font_7px_thin_score = dmd.Font(self.dmd_path + "Font_4_CactusCanyon.dmd")
    #    self.font_7px_wide_score = dmd.Font(self.dmd_path + "Font_6_CactusCanyon.dmd")
        self.font_7px_bold_az = ep.ColorFont(self.dmd_path + "Font_14_CactusCanyon.dmd")
        self.font_7px_bold_az.make_colors([ep.BROWN,ep.BLUE,ep.YELLOW,ep.MAGENTA,ep.CYAN,ep.GREEN,ep.ORANGE,ep.RED])

        self.font_9px_az = ep.ColorFont(self.dmd_path + "Font_15_CactusCanyon.dmd")
        self.font_9px_az.make_colors([ep.BLUE,ep.YELLOW,ep.MAGENTA,ep.CYAN,ep.GREEN,ep.ORANGE,ep.RED,ep.DARK_GREEN,ep.BROWN,ep.DARK_BROWN])
        self.font_9px_az_mid = dmd.Font(self.dmd_path + "Font_15_CactusCanyon_2.dmd")
        self.font_9px_az_dim = ep.ColorFont(self.dmd_path + "Font_15_CactusCanyon_1.dmd")
        self.font_9px_az_dim.make_colors([ep.RED,ep.ORANGE,ep.GREEN])

        self.font_10px_AZ = ep.ColorFont(self.dmd_path + "Font_Custom_10px_AZ.dmd")
        self.font_10px_AZ.make_colors([ep.BLUE,ep.YELLOW,ep.MAGENTA,ep.CYAN,ep.GREEN,ep.ORANGE,ep.RED])

        self.font_12px_az = ep.ColorFont(self.dmd_path + "Font_16_CactusCanyon.dmd")
        self.font_12px_az.make_colors([ep.BLUE,ep.YELLOW,ep.MAGENTA,ep.CYAN,ep.GREEN,ep.ORANGE,ep.RED,ep.DARK_RED])
        self.font_12px_az_dim = ep.ColorFont(self.dmd_path + "Font_16_CactusCanyon_dim.dmd")
        self.font_12px_az_dim.make_colors([ep.RED,ep.GREEN])

        self.font_12px_az_outline = ep.ColorFont(self.dmd_path + "Font_16_mask_CactusCanyon.dmd")
        self.font_12px_az_outline.make_colors([ep.GREEN])
        self.font_12px_az_outline.tracking = -1
        self.font_12px_az_outline.composite_op = "blacksrc"

        self.font_dangerFont = ep.ColorFont(self.dmd_path + "Font_16_mask_CactusCanyon.dmd")
        self.font_dangerFont.make_colors([ep.RED])
        self.font_dangerFont.composite_op = "blacksrc"

        self.font_13px_score = dmd.Font(self.dmd_path + "Font_8_CactusCanyon.dmd")
    #    self.font_13px_extra_thin_score = dmd.Font(self.dmd_path + "Font_11_CactusCanyon.dmd")
        self.font_13px_thin_score = ep.ColorFont(self.dmd_path + "Font_7_CactusCanyon.dmd")
        self.font_13px_thin_score.make_colors([ep.RED,ep.GREEN])
    #    self.font_13px_wide_score = dmd.Font(self.dmd_path + "Font_9_CactusCanyon.dmd")

        self.font_15px_az = ep.ColorFont(self.dmd_path + "Font_17_CactusCanyon.dmd")
        self.font_15px_az.make_colors([ep.ORANGE,ep.BROWN,ep.CYAN,ep.GREEN,ep.RED])

        self.font_15px_bionic = dmd.Font(self.dmd_path + "Font_Custom_15px.dmd")

        self.font_15px_az_outline = ep.ColorFont(self.dmd_path + "Font_17_mask_CactusCanyon.dmd")
        self.font_15px_az_outline.make_colors([ep.GREEN,ep.YELLOW])
        self.font_15px_az_outline.tracking = -1
        self.font_15px_az_outline.composite_op = "blacksrc"

        self.font_17px_score = dmd.Font(self.dmd_path + "Font_12_CactusCanyon.dmd")

        #self.font_score_x12 = dmd.Font(self.dmd_path + "Font_Score_12_CactusCanyon.dmd")
        self.font_score_x12 = dmd.Font(self.dmd_path + "Font_12b_CactusCanyon.dmd")
        self.font_score_x11 = dmd.Font(self.dmd_path + "Font_12c_CactusCanyon.dmd")
        self.font_score_x10 = dmd.Font(self.dmd_path + "Font_12d_CactusCanyon.dmd")

        self.font_20px_az = ep.ColorFont(self.dmd_path + "Font_18_CactusCanyon.dmd")
        self.font_20px_az.make_colors([ep.RED,ep.ORANGE])

        self.font_skillshot = dmd.Font(self.dmd_path + "Font_20_CactusCanyon.dmd")

        self.font_marshallScore = dmd.Font(self.dmd_path + "Font_Reel.dmd")

        # showcase fonts
        self.font_showcase_ll_0 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_LL_0.dmd")
        self.font_showcase_ll_1 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_LL_1.dmd")
        self.font_showcase_ll_2 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_LL_2.dmd")
        self.font_showcase_ll_3 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_LL_3.dmd")

        self.font_showcase_ur_0 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_UR_0.dmd")
        self.font_showcase_ur_1 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_UR_1.dmd")
        self.font_showcase_ur_2 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_UR_2.dmd")
        self.font_showcase_ur_3 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Outline_UR_3.dmd")

        self.font_showcase_fill_0 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Fill_0.dmd")
        self.font_showcase_fill_1 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Fill_1.dmd")
        self.font_showcase_fill_2 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Fill_2.dmd")
        self.font_showcase_fill_3 = dmd.Font(self.dmd_path + "Font_Custom_Showcase_Fill_3.dmd")

        # switch matrix font
        self.font_matrix = dmd.Font(self.dmd_path + "switch_matrix_font.dmd")

# CC Sounds
        # Sound Effects
        self.sfx_ballEnd = 'sfx_ballEnd'
        self.game.sound.register_sound(self.sfx_ballEnd,self.sfx_path + "006-sfx-ball-end.wav")
        self.sfx_ballOneLock = 'sfx_ballOneLock'
        self.game.sound.register_sound(self.sfx_ballOneLock, self.sfx_path + "241-sfx-ball-one-lock.wav")
        self.sfx_banjoTrillUp = 'sfx_banjoTrillUp'
        self.game.sound.register_sound(self.sfx_banjoTrillUp, self.sfx_path + "622-banjo-trill-up.wav")
        self.sfx_banjoTrillDown = 'sfx_banjoTrillDown'
        self.game.sound.register_sound(self.sfx_banjoTrillDown, self.sfx_path + "623-banjo-trill-down.wav")
        self.sfx_banjoTaDa = 'sfx_banjoTaDa'
        self.game.sound.register_sound(self.sfx_banjoTaDa, self.sfx_path + "624-banjo-ta-da.wav")
        self.sfx_blow = 'sfx_blow'
        self.game.sound.register_sound(self.sfx_blow, self.sfx_path + "169-sfx-blow-on-gun.wav")
        self.sfx_breakingGlass1 = 'sfx_breakingGlass1'
        self.game.sound.register_sound(self.sfx_breakingGlass1, self.sfx_path + "119-sfx-breaking-glass-1.wav")
        self.sfx_breakingGlass2 = 'sfx_breakingGlass2'
        self.game.sound.register_sound(self.sfx_breakingGlass2, self.sfx_path + "135-sfx-breaking-glass-2.wav")
        self.sfx_cactusMash = 'sfx_cactusMash'
        self.game.sound.register_sound(self.sfx_cactusMash, self.sfx_path + "235-bonus-cactus-mash.wav")
        self.sfx_explosion1 = 'sfx_explosion1'
        self.game.sound.register_sound(self.sfx_explosion1, self.sfx_path + "105-sfx-explosion-1.wav")
        self.sfx_explosion11 = 'sfx_explosion2'
        self.game.sound.register_sound(self.sfx_explosion11, self.sfx_path + "257-sfx-explosion-11.wav")
        self.sfx_explosion17 = 'sfx_explosion17'
        self.game.sound.register_sound(self.sfx_explosion17, self.sfx_path + "341-sfx-explosion-17.wav")
        self.sfx_fallAndCrash1 = 'sfx_fallAndCrash1'
        self.game.sound.register_sound(self.sfx_fallAndCrash1, self.sfx_path + "101-sfx-fall-and-crash-1.wav")
        self.sfx_smashingWood = 'sfx_smashingWood'
        self.game.sound.register_sound(self.sfx_smashingWood, self.sfx_path + "133-sfx-smashing-wood.wav")
        self.sfx_bonusX = 'sfx_bonusX'
        self.game.sound.register_sound(self.sfx_bonusX, self.sfx_path + "036-sfx-bonus-x.wav")
        self.sfx_flourish6 = 'sfx_flourish6'
        self.game.sound.register_sound(self.sfx_flourish6, self.sfx_path + "032-flourish-6.wav")
        self.sfx_flourish7 = 'sfx_flourish7'
        self.game.sound.register_sound(self.sfx_flourish7, self.sfx_path + "034-flourish-7-horns.wav")
        self.sfx_grinDing = 'sfx_grinDing'
        self.game.sound.register_sound(self.sfx_grinDing, self.sfx_path + "117-sfx-grin-ding.wav")
        self.sfx_rightRampEnter = 'sfx_rightRampEnter'
        self.game.sound.register_sound(self.sfx_rightRampEnter, self.sfx_path + "129-sfx-right-ramp-enter.wav")
        self.sfx_leftRampEnter = 'sfx_leftRampEnter'
        self.game.sound.register_sound(self.sfx_leftRampEnter, self.sfx_path + "407-sfx-river-ramp-splash.wav")
        self.sfx_leftLoopEnter = 'sfx_leftLoopEnter'
        self.game.sound.register_sound(self.sfx_leftLoopEnter, self.sfx_path + "179-woosh-with-horse-running.wav")
        self.sfx_horse = 'sfx_horse'
        self.game.sound.register_sound(self.sfx_horse,self.sfx_path + "179b-horse-running.wav")
        self.sfx_orchestraRiff = 'sfx_orchestraRiff'
        self.game.sound.register_sound(self.sfx_orchestraRiff, self.sfx_path + "041-orchestra-riff.wav")
        self.sfx_orchestraFlourish = 'sfx_orchestraFlourish'
        self.game.sound.register_sound(self.sfx_orchestraFlourish, self.sfx_path + "066-orchestra-flourish.wav")
        self.sfx_quickdrawOff = 'sfx_quickdrawOff'
        self.game.sound.register_sound(self.sfx_quickdrawOff, self.sfx_path + "287-quickdraw-hit-light.wav")
        self.sfx_quickdrawOn = 'sfx_quickdrawOn'
        self.game.sound.register_sound(self.sfx_quickdrawOn, self.sfx_path + "289-quickdraw-hit-already-lit.wav")
        self.sfx_rattlesnake = 'sfx_rattlesnake'
        self.game.sound.register_sound(self.sfx_rattlesnake, self.sfx_path + "221-rattlesnake.wav")
        self.sfx_rightLoopEnter = 'sfx_rightLoopEnter'
        self.game.sound.register_sound(self.sfx_rightLoopEnter, self.sfx_path + "155-sfx-ricochet-triple.wav")
        self.sfx_skillShotWoosh = 'sfx_skillShotWoosh'
        self.game.sound.register_sound(self.sfx_skillShotWoosh, self.sfx_path + "393-skillshot-woosh.wav")
        self.sfx_thrownCoins = 'sfx_thrownCoins'
        self.game.sound.register_sound(self.sfx_thrownCoins, self.sfx_path + "137-sfx-thrown-coins.wav")
        self.sfx_yeeHoo = 'sfx_yeeHoo'
        self.game.sound.register_sound(self.sfx_yeeHoo, self.sfx_path + "1963-yee-hoo.wav")
        self.sfx_gunfightHit1 = 'sfx_gunfightHit1'
        self.game.sound.register_sound(self.sfx_gunfightHit1, self.sfx_path + "011-gunfight-hit-1.wav")
        self.sfx_gunfightHit2 = 'sfx_gunfightHit2'
        self.game.sound.register_sound(self.sfx_gunfightHit2, self.sfx_path + "013-gunfight-hit-2.wav")
        self.sfx_gunfightHit3 = 'sfx_gunfightHit3'
        self.game.sound.register_sound(self.sfx_gunfightHit3, self.sfx_path + "015-gunfight-hit-3.wav")
        self.sfx_gunfightBell = 'sfx_gunfightBell'
        self.game.sound.register_sound(self.sfx_gunfightBell, self.sfx_path + "123-gunfight-four-bells.wav")
        self.sfx_centerRampEnter = 'sfx_cetnerRampEnter'
        self.game.sound.register_sound(self.sfx_centerRampEnter, self.sfx_path + "201-train-center-ramp-enter-chugging.wav")
        self.sfx_quickdrawHit = 'sfx_quickdrawHit'
        self.game.sound.register_sound(self.sfx_quickdrawHit, self.sfx_path + "309-sfx-quickdraw-hit.wav")
        self.sfx_bountyBell = 'sfx_bountyBell'
        self.game.sound.register_sound(self.sfx_bountyBell, self.sfx_path + "113-sfx-other-bell.wav")
        self.sfx_bountyCollected = 'sfx_bountyCollected'
        self.game.sound.register_sound(self.sfx_bountyCollected, self.sfx_path + "045-sfx-bounty-collected.wav")
        self.sfx_gunCock = 'sfx_gunCock'
        self.game.sound.register_sound(self.sfx_gunCock, self.sfx_path + "391-sfx-gun-cock.wav")
        self.sfx_gunShot = 'sfx_gunShot'
        self.game.sound.register_sound(self.sfx_gunShot, self.sfx_path + "183-sfx-clear-gunshot.wav")
        self.sfx_gunfightShot = 'sfx_gunfightShot'
        self.game.sound.register_sound(self.sfx_gunfightShot, self.sfx_path + "339-sfx-gunfight-hit.wav")
        self.sfx_gunfightFlourish = 'sfx_gunfightFlourish'
        self.game.sound.register_sound(self.sfx_gunfightFlourish, self.sfx_path + "068-sfx-gunfight-flourish.wav")
        self.sfx_shooterLaunch = 'sfx_shooterLaunch'
        self.game.sound.register_sound(self.sfx_shooterLaunch, self.sfx_path + "273-sfx-shooter-lane-launch.wav")
        self.sfx_outlane = 'sfx_outlane'
        self.game.sound.register_sound(self.sfx_outlane, self.sfx_path + "283-sfx-outlane.wav")
        self.sfx_mineKicker = 'sfx_mineKicker'
        self.game.sound.register_sound(self.sfx_mineKicker, self.sfx_path + "255-sfx-mine-kicker-hit.wav")
        self.sfx_mineEntrance = 'sfx_mineEntrance'
        self.game.sound.register_sound(self.sfx_mineEntrance, self.sfx_path + "121-sfx-mine-entrance.wav")
        self.sfx_trainWhistle = 'sfx_trainWhistle'
        self.game.sound.register_sound(self.sfx_trainWhistle, self.sfx_path + "271-sfx-train-whistle.wav")
        self.sfx_longTrainWhistle = 'sfx_longTrainWhistle'
        self.game.sound.register_sound(self.sfx_longTrainWhistle, self.sfx_path + "00-sfx-long-train-whistle.wav")
        self.sfx_trainChugShort = 'sfx_trainChugShort'
        self.game.sound.register_sound(self.sfx_trainChugShort, self.sfx_path + "203-sfx-train-chug-short.wav")
        self.sfx_ebMusic = 'sfx_ebMusic'
        self.game.sound.register_sound(self.sfx_ebMusic, self.sfx_path + "029-sfx-extra-ball-intro.wav")
        self.sfx_ebDrink = 'sfx_ebDrink'
        self.game.sound.register_sound(self.sfx_ebDrink, self.sfx_path + "173-sfx-eb-drink.wav")
        self.sfx_ebGunfire = 'sfx_ebGunfire'
        self.game.sound.register_sound(self.sfx_ebGunfire, self.sfx_path + "181-sfx-eb-gunfire.wav")
        self.sfx_ebLookRight = 'sfx_ebLookRight'
        self.game.sound.register_sound(self.sfx_ebLookRight, self.sfx_path + "058-sfx-eb-look-right.wav")
        self.sfx_ebLookLeft = 'sfx_eblookLeft'
        self.game.sound.register_sound(self.sfx_ebLookLeft, self.sfx_path + "060-sfx-eb-look-left.wav")
        self.sfx_ebFallAndCrash = 'sfx_ebFallAndCrash'
        self.game.sound.register_sound(self.sfx_ebFallAndCrash, self.sfx_path + "149-sfx-eb-fall-and-crash.wav")
        self.sfx_ebFlourish = 'sfx_ebFlourish'
        self.game.sound.register_sound(self.sfx_ebFlourish, self.sfx_path + "074-sfx-eb-flourish.wav")
        self.sfx_tiltDanger = 'sfx_tiltDanger'
        self.game.sound.register_sound(self.sfx_tiltDanger, self.sfx_path + "143-sfx-tilt-danger.wav")
        self.sfx_cow1 = 'sfx_cow1'
        self.game.sound.register_sound(self.sfx_cow1, self.sfx_path + "321-sfx-cow-1.wav")
        self.sfx_cow2 = 'sfx_cow2'
        self.game.sound.register_sound(self.sfx_cow2, self.sfx_path + "323-sfx-cow-2.wav")
        self.sfx_cow3 = 'sfx_cow3'
        self.game.sound.register_sound(self.sfx_cow3, self.sfx_path + "00-sfx-cow-3.wav")
        self.sfx_lockTwoMinecart = 'sfx_lockTwoMinecart'
        self.game.sound.register_sound(self.sfx_lockTwoMinecart, self.sfx_path + "243-sfx-lock-2-minecart.wav")
        self.sfx_lockTwoFlourish = 'sfx_lockTwoFlourish'
        self.game.sound.register_sound(self.sfx_lockTwoFlourish, self.sfx_path + "048-sfx-lock-two-orchestra-hit.wav")
        self.sfx_lockTwoExplosion = 'sfx_lockTwoExplosion'
        self.game.sound.register_sound(self.sfx_lockTwoExplosion, self.sfx_path + "213-sfx-mine-lock-2-explosion.wav")
        self.sfx_trainStop = 'sfx_trainStop'
        self.game.sound.register_sound(self.sfx_trainStop, self.sfx_path + "199-sfx-train-stops.wav")
        self.sfx_trainStopWithBrake = 'sfx_trainStopWithBrake'
        self.game.sound.register_sound(self.sfx_trainStopWithBrake, self.sfx_path + "205-sfx-train-stops-with-brake-pull.wav")
        self.sfx_lightning1 = 'sfx_lightning1'
        self.game.sound.register_sound(self.sfx_lightning1, self.sfx_path + "249-sfx-lightning-1.wav")
        self.sfx_lightning2 = 'sfx_lightning2'
        self.game.sound.register_sound(self.sfx_lightning2, self.sfx_path + "251-sfx-lightning-2.wav")
        self.sfx_lightningRumble = 'sfx_lightningRumble'
        self.game.sound.register_sound(self.sfx_lightningRumble, self.sfx_path + "295-sfx-lightning-with-rumble.wav")
        self.sfx_flyByNoise = 'sfx_flyByNoise'
        self.game.sound.register_sound(self.sfx_flyByNoise, self.sfx_path + "285-sfx-fly-by-noise.wav")
        self.sfx_quickdrawFinale = 'sfx_quickdrawFinale'
        self.game.sound.register_sound(self.sfx_quickdrawFinale, self.sfx_path + "020-sfx-quickdraw-finale-riff.wav")
        self.sfx_revRicochet = 'sfx_revRicochet'
        self.game.sound.register_sound(self.sfx_revRicochet, self.sfx_path + "147-sfx-rev-up-ricochet.wav")
        self.sfx_punch = 'sfx_punch'
        self.game.sound.register_sound(self.sfx_punch, self.sfx_path + "349-sfx-punch.wav")
        self.sfx_futuristicRicochet = 'sfx_futuristicRicochet'
        self.game.sound.register_sound(self.sfx_futuristicRicochet, self.sfx_path + "217-sfx-futuristic-ricochet.wav")
        self.sfx_smallExplosion = 'sfx_smallExplosion'
        self.game.sound.register_sound(self.sfx_smallExplosion, self.sfx_path + "263-sfx-explosion.wav")
        self.sfx_woosh = 'sfx_woosh'
        self.game.sound.register_sound(self.sfx_woosh, self.sfx_path + "229-sfx-plain-woosh.wav")
        self.sfx_wooshDing = 'sfx_wooshDing'
        self.game.sound.register_sound(self.sfx_wooshDing, self.sfx_path + "277-sfx-woosh-ding.wav")
        self.sfx_ropeWoosh = 'sfx_ropeWoosh'
        self.game.sound.register_sound(self.sfx_ropeWoosh, self.sfx_path + "00-rope-woosh.wav")
        self.sfx_ropeCreak = 'sfx_ropeCreak'
        self.game.sound.register_sound(self.sfx_ropeCreak, self.sfx_path + "00-rope-creak.wav")

        self.sfx_ricochetSet = 'sfx_ricochetSet'
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "103-sfx-ricochet-1.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "109-sfx-ricochet-2.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "111-sfx-ricochet-3.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "319-sfx-ricochet-4.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "159-sfx-new-ricochet-set.wav")

        self.sfx_cheers = 'sfx_cheers'
        self.game.sound.register_sound(self.sfx_cheers, self.sfx_path + "167-sfx-crowd-cheer-3.wav")
        self.game.sound.register_sound(self.sfx_cheers, self.sfx_path + "163-sfx-crowd-cheer-2.wav")
        self.game.sound.register_sound(self.sfx_cheers, self.sfx_path + "161-sfx-crowd-cheer-1.wav")
        self.game.sound.register_sound(self.sfx_cheers, self.sfx_path + "165-sfx-crowd-cheer-3.wav")

        self.sfx_pour = 'sfx_pour'
        self.game.sound.register_sound(self.sfx_pour, self.sfx_path + "00-sfx-pouring-beer.wav")
        self.sfx_slide = 'sfx_slide'
        self.game.sound.register_sound(self.sfx_slide, self.sfx_path + "00-sfx-mug-slide.wav")
        self.sfx_orchestraBump1 = 'sfx_orchestraBump1'
        self.game.sound.register_sound(self.sfx_orchestraBump1, self.sfx_path + "050-sfx-orchestra-hit-bump1.wav")
        self.sfx_orchestraBump2 = 'sfx_orchestraBump2'
        self.game.sound.register_sound(self.sfx_orchestraBump2, self.sfx_path + "052-sfx-orchestra-hit-bump2.wav")
        self.sfx_orchestraSet = 'sfx_orchestraSet'
        self.game.sound.register_sound(self.sfx_orchestraSet, self.sfx_path + "054-sfx-orchestra-hit-set.wav")
        self.sfx_orchestraSpike = 'sfx_orchestraSpike'
        self.game.sound.register_sound(self.sfx_orchestraSpike, self.sfx_path + "056-sfx-orchestra-hit-spike.wav")
        self.sfx_lowBoom = 'sfx_lowBoom'
        self.game.sound.register_sound(self.sfx_lowBoom, self.sfx_path + "209-sfx-low-boom.wav")
        self.sfx_incoming = 'sfx_incoming'
        self.game.sound.register_sound(self.sfx_incoming, self.sfx_path + "00-sfx-incoming.wav")
        self.sfx_tumbleWind = 'sfx_tumbleWind'
        self.game.sound.register_sound(self.sfx_tumbleWind, self.sfx_path + "00-sfx-wind-blows.wav")

        self.sfx_deadBartHit = 'sfx_deadBartHit'
        self.game.sound.register_sound(self.sfx_deadBartHit, self.sfx_path + "297-sfx-dead-bart-1.wav")
        self.game.sound.register_sound(self.sfx_deadBartHit, self.sfx_path + "299-sfx-dead-bart-2.wav")
        self.game.sound.register_sound(self.sfx_deadBartHit, self.sfx_path + "301-sfx-dead-bart-3.wav")
        self.sfx_hitBionicBart = 'sfx_hitBionicBart'
        self.game.sound.register_sound(self.sfx_hitBionicBart, self.sfx_path + "310-sfx-hit-bionic-bart.wav")
        self.sfx_dieBionicBart = 'sfx_dieBionicBart'
        self.game.sound.register_sound(self.sfx_dieBionicBart, self.sfx_path + "125-sfx-bionic-critical-hit.wav")
        self.sfx_heavyExplosion = 'sfx_heavyExplosion'
        self.game.sound.register_sound(self.sfx_heavyExplosion, self.sfx_path + "247-sfx-heavy-explosion.wav")
        self.sfx_ragtimePiano = 'sfx_ragtimePiano'
        self.game.sound.register_sound(self.sfx_ragtimePiano, self.sfx_path + "00-sfx-ragtime-piano.wav")
        self.sfx_churchBell = 'sfx_churchBell'
        self.game.sound.register_sound(self.sfx_churchBell, self.sfx_path + "00-sfx-church-bell.wav")

        self.sfx_fireworks1 = 'sfx_fireworks1'
        self.game.sound.register_sound(self.sfx_fireworks1, self.sfx_path + "317-sfx-fireworks-1.wav")
        self.sfx_fireworks2 = 'sfx_fireworks2'
        self.game.sound.register_sound(self.sfx_fireworks2, self.sfx_path + "315-sfx-fireworks-2.wav")
        self.sfx_fireworks3 = 'sfx_fireworks3'
        self.game.sound.register_sound(self.sfx_fireworks3, self.sfx_path + "311-sfx-fireworks-3.wav")

        self.sfx_cvaInlane = 'sfx_cvaInlane'
        self.game.sound.register_sound(self.sfx_cvaInlane, self.sfx_path + "828-afm-beam-noise.wav")
        self.sfx_cvaDrain = 'sfx_cvaDrain'
        self.game.sound.register_sound(self.sfx_cvaDrain,self.sfx_path + "340-afm-drain-noise.wav")
        self.sfx_cvaExplosion = 'sfx_cvaExplosion'
        self.game.sound.register_sound(self.sfx_cvaExplosion, self.sfx_path + "208-afm-explosion.wav")
        self.sfx_cvaFinalRiff = 'sfx_cvaFinalRiff'
        self.game.sound.register_sound(self.sfx_cvaFinalRiff, self.sfx_path + "328-afm-celebratory-riff.wav")
        self.sfx_cvaTeleport = 'sfx_cvaTeleport'
        self.game.sound.register_sound(self.sfx_cvaTeleport, self.sfx_path + "294-afm-teleport.wav")
        self.sfx_cvaWoosh = 'sfx_cvaWoosh'
        self.game.sound.register_sound(self.sfx_cvaWoosh, self.sfx_path + "246-afm-woosh.wav")
        self.sfx_cvaGroan = 'sfx_cvaGroan'
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-1.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-2.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-3.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-4.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-5.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-6.wav")
        self.sfx_cvaAlienHit = 'sfx_cvaAlienHit'
        self.game.sound.register_sound(self.sfx_cvaAlienHit, self.sfx_path + "322-afm-alien-hit.wav")
        self.sfx_cvaBumper = 'sfx_cvaBumper'
        self.game.sound.register_sound(self.sfx_cvaBumper, self.sfx_path + "bangarang-bwoip-noise.wav")
        self.sfx_cvaSiren = 'sfx_cvaSiren'
        self.game.sound.register_sound(self.sfx_cvaSiren, self.sfx_path + "bangarang-siren.wav")
        self.sfx_spinDown = 'sfx_spinDown'
        self.game.sound.register_sound(self.sfx_spinDown, self.sfx_path + "145-sfx-spin-down.wav")

        self.sfx_glumRiff = 'sfx_glumRiff'
        self.game.sound.register_sound(self.sfx_glumRiff, self.sfx_path + "021-glum-riff.wav")
        self.sfx_glumRiffShort = 'sfx_glumRiffShort'
        self.game.sound.register_sound(self.sfx_glumRiffShort, self.sfx_path + "021-glum-riff-short.wav")
        self.snd_attractCollection = 'snd_attractCollection'
        self.game.sound.register_sound(self.snd_attractCollection, self.quotes_path + "1132-mayor-vote-cheetum.wav")

        self.sfx_chime10 = 'sfx_chime10'
        self.game.sound.register_sound(self.sfx_chime10, self.sfx_path + "BELL10.wav")
        self.sfx_chime20 = 'sfx_chime20'
        self.game.sound.register_sound(self.sfx_chime20, self.sfx_path + "BELL20.wav")
        self.sfx_chime30 = 'sfx_chime30'
        self.game.sound.register_sound(self.sfx_chime30, self.sfx_path + "BELL30.wav")
        self.sfx_chime50 = 'sfx_chime50'
        self.game.sound.register_sound(self.sfx_chime30, self.sfx_path + "BELL50.wav")

        self.sfx_chime100 = 'sfx_chime100'
        self.game.sound.register_sound(self.sfx_chime100, self.sfx_path + "BELL100.wav")
        self.sfx_chime200 = 'sfx_chime200'
        self.game.sound.register_sound(self.sfx_chime200, self.sfx_path + "BELL200.wav")
        self.sfx_chime300 = 'sfx_chime300'
        self.game.sound.register_sound(self.sfx_chime300, self.sfx_path + "BELL300.wav")
        self.sfx_chime500 = 'sfx_chime500'
        self.game.sound.register_sound(self.sfx_chime300, self.sfx_path + "BELL500.wav")

        self.sfx_chime1000 = 'sfx_chime1000'
        self.game.sound.register_sound(self.sfx_chime1000, self.sfx_path + "BELL1000.wav")
        self.sfx_chime2000 = 'sfx_chime2000'
        self.game.sound.register_sound(self.sfx_chime2000, self.sfx_path + "BELL2000.wav")
        self.sfx_chime3000 = 'sfx_chime3000'
        self.game.sound.register_sound(self.sfx_chime3000, self.sfx_path + "BELL3000.wav")
        self.sfx_chime5000 = 'sfx_chime5000'
        self.game.sound.register_sound(self.sfx_chime5000, self.sfx_path + "BELL5000.wav")

        self.sfx_chime1500 = 'sfx_chime1500'
        self.game.sound.register_sound(self.sfx_chime1500, self.sfx_path + "BELL1500.wav")
        self.sfx_chime2500 = 'sfx_chime2500'
        self.game.sound.register_sound(self.sfx_chime2500, self.sfx_path + "BELL2500.wav")
        self.sfx_chime3500 = 'sfx_chime3500'
        self.game.sound.register_sound(self.sfx_chime3500, self.sfx_path + "BELL3500.wav")
        self.sfx_chime4500 = 'sfx_chime4500'
        self.game.sound.register_sound(self.sfx_chime4500, self.sfx_path + "BELL4500.wav")

        self.sfx_chimeOut = 'sfx_chimeOut'
        self.game.sound.register_sound(self.sfx_chimeOut, self.sfx_path + "Bell-100-10-1000.wav")

        self.sfx_serviceStart = 'sfx_serviceStart'
        self.game.sound.register_sound(self.sfx_serviceStart, self.sfx_path + "989-sfx-service-startup.wav")
        self.sfx_menuUp = 'sfx_menuUp'
        self.game.sound.register_sound(self.sfx_menuUp, self.sfx_path + "985-sfx-menu-up.wav")
        self.sfx_menuDown = 'sfx_menuDown'
        self.game.sound.register_sound(self.sfx_menuDown, self.sfx_path + "986-sfx-menu-down.wav")
        self.sfx_menuEnter = 'sfx_menuEnter'
        self.game.sound.register_sound(self.sfx_menuEnter, self.sfx_path + "987-sfx-menu-enter.wav")
        self.sfx_menuExit = 'sfx_menuExit'
        self.game.sound.register_sound(self.sfx_menuExit, self.sfx_path + "988-sfx-menu-exit.wav")
        self.sfx_menuReject = 'sfx_menuReject'
        self.game.sound.register_sound(self.sfx_menuReject, self.sfx_path + "982-sfx-menu-reject.wav")
        self.sfx_menuCancel = 'sfx_menuCancel'
        self.game.sound.register_sound(self.sfx_menuCancel, self.sfx_path + "983-sfx-menu-cancel.wav")
        self.sfx_menuSwitchEdge = 'sfx_menuSwitchEdge'
        self.game.sound.register_sound(self.sfx_menuSwitchEdge, self.sfx_path + "980-sfx-menu-switch-edge.wav")
        self.sfx_menuSave = 'sfx_menuSave'
        self.game.sound.register_sound(self.sfx_menuSave, self.sfx_path + "984-sfx-menu-save.wav")

        self.sfx_knocker = 'sfx_knocker'
        self.game.sound.register_sound(self.sfx_knocker, self.sfx_path + "knocker.wav")

        self.sfx_glassSmash = 'sfx_glassSmash'
        self.game.sound.register_sound(self.sfx_glassSmash,self.sfx_path + "267-sfx-glass-smash.wav")
        self.sfx_pianoRiff = 'sfx_pianoRiff'
        self.game.sound.register_sound(self.sfx_pianoRiff, self.sfx_path + "043-sfx-piano-cymbal.wav")
        self.sfx_matchRiff = 'sfx_matchRiff'
        self.game.sound.register_sound(self.sfx_matchRiff, self.sfx_path + "038-sfx-match-riff.wav")

        self.sfx_ballSaved = 'sfx_ballSaved'
        self.game.sound.register_sound(self.sfx_ballSaved, self.sfx_path + "00-ball_saved.wav")

        self.sfx_tafMissIt = 'sfx_tafMissIt'
        self.game.sound.register_sound(self.sfx_tafMissIt, self.sfx_path + "taf-ball-whiff.wav")
        self.sfx_tafHitIt = 'sfx_tafHitIt'
        self.game.sound.register_sound(self.sfx_tafHitIt, self.sfx_path + "taf-it-hit.wav")
        self.sfx_tafIt1 = 'sfx_tafIt1'
        self.game.sound.register_sound(self.sfx_tafIt1, self.sfx_path + "taf-it1.wav")
        self.sfx_tafIt2 = 'sfx_tafIt2'
        self.game.sound.register_sound(self.sfx_tafIt2, self.sfx_path + "taf-it2.wav")
        self.sfx_tafIt3 = 'sfx_tafIt3'
        self.game.sound.register_sound(self.sfx_tafIt3, self.sfx_path + "taf-it3.wav")
        self.sfx_tafIt4 = 'sfx_tafIt4'
        self.game.sound.register_sound(self.sfx_tafIt4, self.sfx_path + "taf-it4.wav")
        self.sfx_tafDitty = 'sfx_tafDitty'
        self.game.sound.register_sound(self.sfx_tafDitty, self.sfx_path + "taf-mansion-ditty.wav")
        self.quote_itsCousinIt = 'quote_itsCousinIt'
        self.game.sound.register_sound(self.quote_itsCousinIt, self.sfx_path + "taf-its-cousin-it.wav")

        self.sfx_mbDracIntro = 'sfx_mbDracIntro'
        self.game.sound.register_sound(self.sfx_mbDracIntro, self.sfx_path + "mb_drac_intro.wav")
        self.sfx_mbCoffinCreak = 'sfx_mbCoffinCreak'
        self.game.sound.register_sound(self.sfx_mbCoffinCreak, self.sfx_path + "mb_coffin_creak.wav")
        self.sfx_mbBangCrash = 'sfx_mbBangCrash'
        self.game.sound.register_sound(self.sfx_mbBangCrash, self.sfx_path + "mb_bang-crash.wav")
        self.sfx_mbBats = 'sfx_mbBats'
        self.game.sound.register_sound(self.sfx_mbBats, self.sfx_path + "mb_screeching-bats.wav")
        self.sfx_mbSmack = 'sfx_mbSmack'
        self.game.sound.register_sound(self.sfx_mbSmack, self.sfx_path + "mb_drac_smack.wav")
        self.sfx_mbHowl = 'sfx_mbHowl'
        self.game.sound.register_sound(self.sfx_mbHowl, self.sfx_path + "mb-howl.wav")

        self.sfx_mmTrollSmack = 'sfx_mmTrollSmack'
        self.game.sound.register_sound(self.sfx_mmTrollSmack, self.sfx_path + "mm_troll-smack.wav")
        self.sfx_mmIntro = 'sfx_mmIntro'
        self.game.sound.register_sound(self.sfx_mmIntro, self.music_path + "mm_trolls_intro.wav")

        # Quotes

        self.quote_mmTrolls = 'quote_mmTrolls'
        self.game.sound.register_sound(self.quote_mmTrolls, self.quotes_path + "mm_trolls_crowd.wav")
        self.quote_mmLeftPain = 'quote_mmLeftPain'
        self.game.sound.register_sound(self.quote_mmLeftPain, self.quotes_path + "mm_left-troll-pain-1.wav")
        self.game.sound.register_sound(self.quote_mmLeftPain, self.quotes_path + "mm_left-troll-pain-2.wav")
        self.game.sound.register_sound(self.quote_mmLeftPain, self.quotes_path + "mm_left-troll-pain-3.wav")
        self.quote_mmRightPain = 'quote_mmRightPain'
        self.game.sound.register_sound(self.quote_mmRightPain, self.quotes_path + "mm_right-troll-pain-1.wav")
        self.game.sound.register_sound(self.quote_mmRightPain, self.quotes_path + "mm_right-troll-pain-2.wav")
        self.game.sound.register_sound(self.quote_mmRightPain, self.quotes_path + "mm_right-troll-pain-3.wav")
        self.quote_mmLeftDeath = 'quote_mmLeftDeath'
        self.game.sound.register_sound(self.quote_mmLeftDeath, self.quotes_path + "mm_left-troll-death-1.wav")
        self.game.sound.register_sound(self.quote_mmLeftDeath, self.quotes_path + "mm_left-troll-death-2.wav")
        self.quote_mmRightDeath = 'quote_mmRightDeath'
        self.game.sound.register_sound(self.quote_mmRightDeath, self.quotes_path + "mm_right-troll-death-1.wav")
        self.game.sound.register_sound(self.quote_mmRightDeath, self.quotes_path + "mm_right-troll-death-2.wav")
        self.quote_mmRightAlone = 'quote_mmRightAlone'
        self.game.sound.register_sound(self.quote_mmRightAlone, self.quotes_path + "mm_right-troll-alone-1.wav")
        self.game.sound.register_sound(self.quote_mmRightAlone, self.quotes_path + "mm_right-troll-alone-2.wav")
        self.game.sound.register_sound(self.quote_mmRightAlone, self.quotes_path + "mm_right-troll-alone-3.wav")
        self.quote_mmLeftAlone = 'quote_mmLeftAlone'
        self.game.sound.register_sound(self.quote_mmLeftAlone, self.quotes_path + "mm_left-troll-alone-1.wav")
        self.game.sound.register_sound(self.quote_mmLeftAlone, self.quotes_path + "mm_left-troll-alone-2.wav")
        self.game.sound.register_sound(self.quote_mmLeftAlone, self.quotes_path + "mm_left-troll-alone-3.wav")
        self.quote_mmLT1 = 'quote_mmLT1'
        self.game.sound.register_sound(self.quote_mmLT1, self.quotes_path + "mm_left-team-taunt-1.wav")
        self.quote_mmLT2 = 'quote_mmLT2'
        self.game.sound.register_sound(self.quote_mmLT2, self.quotes_path + "mm_left-team-taunt-2.wav")
        self.quote_mmLT3 = 'quote_mmLT3'
        self.game.sound.register_sound(self.quote_mmLT3, self.quotes_path + "mm_left-team-taunt-3.wav")
        self.quote_mmLT4 = 'quote_mmLT4'
        self.game.sound.register_sound(self.quote_mmLT4, self.quotes_path + "mm_left-team-taunt-4.wav")
        self.quote_mmLT5 = 'quote_mmLT5'
        self.game.sound.register_sound(self.quote_mmLT5, self.quotes_path + "mm_left-team-taunt-5.wav")
        self.quote_mmLT6 = 'quote_mmLT6'
        self.game.sound.register_sound(self.quote_mmLT6, self.quotes_path + "mm_left-team-taunt-6.wav")
        self.quote_mmRT1 = 'quote_mmRT1'
        self.game.sound.register_sound(self.quote_mmRT1, self.quotes_path + "mm_right-team-taunt-1.wav")
        self.quote_mmRT2 = 'quote_mmRT2'
        self.game.sound.register_sound(self.quote_mmRT2, self.quotes_path + "mm_right-team-taunt-2.wav")
        self.quote_mmRT3 = 'quote_mmRT3'
        self.game.sound.register_sound(self.quote_mmRT3, self.quotes_path + "mm_right-team-taunt-3.wav")
        self.quote_mmRT4 = 'quote_mmRT4'
        self.game.sound.register_sound(self.quote_mmRT4, self.quotes_path + "mm_right-team-taunt-4.wav")
        self.quote_mmRT5 = 'quote_mmRT5'
        self.game.sound.register_sound(self.quote_mmRT5, self.quotes_path + "mm_right-team-taunt-5.wav")
        self.quote_mmRT6 = 'quote_mmRT6'
        self.game.sound.register_sound(self.quote_mmRT6, self.quotes_path + "mm_right-team-taunt-6.wav")
        self.quote_mmLTS1 = 'quote_mmLTS1'
        self.game.sound.register_sound(self.quote_mmLTS1, self.quotes_path + "mm_left-taunt-1.wav")
        self.quote_mmLTS2 = 'quote_mmLTS2'
        self.game.sound.register_sound(self.quote_mmLTS2, self.quotes_path + "mm_left-taunt-2.wav")
        self.quote_mmLTS3 = 'quote_mmLTS3'
        self.game.sound.register_sound(self.quote_mmLTS3, self.quotes_path + "mm_left-taunt-3.wav")
        self.quote_mmLTS4 = 'quote_mmLTS4'
        self.game.sound.register_sound(self.quote_mmLTS4, self.quotes_path + "mm_left-taunt-4.wav")
        self.quote_mmLTS5 = 'quote_mmLTS5'
        self.game.sound.register_sound(self.quote_mmLTS5, self.quotes_path + "mm_left-taunt-5.wav")
        self.quote_mmLTS6 = 'quote_mmLTS6'
        self.game.sound.register_sound(self.quote_mmLTS6, self.quotes_path + "mm_left-taunt-6.wav")
        self.quote_mmRTS1 = 'quote_mmRTS1'
        self.game.sound.register_sound(self.quote_mmRTS1, self.quotes_path + "mm_right-taunt-1.wav")
        self.quote_mmRTS2 = 'quote_mmRTS2'
        self.game.sound.register_sound(self.quote_mmRTS2, self.quotes_path + "mm_right-taunt-2.wav")
        self.quote_mmRTS3 = 'quote_mmRTS3'
        self.game.sound.register_sound(self.quote_mmRTS3, self.quotes_path + "mm_right-taunt-3.wav")
        self.quote_mmRTS4 = 'quote_mmRTS4'
        self.game.sound.register_sound(self.quote_mmRTS4, self.quotes_path + "mm_right-taunt-4.wav")
        self.quote_mmRTS5 = 'quote_mmRTS5'
        self.game.sound.register_sound(self.quote_mmRTS5, self.quotes_path + "mm_right-taunt-5.wav")
        self.quote_mmRTS6 = 'quote_mmRTS6'
        self.game.sound.register_sound(self.quote_mmRTS6, self.quotes_path + "mm_right-taunt-6.wav")
        self.quote_mmFatality = 'quote_mmFatality'
        self.game.sound.register_sound(self.quote_mmFatality, self.quotes_path + "mm_fatality.wav")
        self.quote_mmYouSuck = 'quote_mmYouSuck'
        self.game.sound.register_sound(self.quote_mmYouSuck, self.quotes_path + "mm_you-suck.wav")

        self.quote_mbDracBleh = 'quote_mbDracBleh'
        self.game.sound.register_sound(self.quote_mbDracBleh, self.quotes_path + "mb_drac-blah.wav")
        self.quote_mbDracStart = 'quote_mbDracStart'
        self.game.sound.register_sound(self.quote_mbDracStart, self.quotes_path + "mb_drac-can-you-hit-dis-bat.wav")
        self.game.sound.register_sound(self.quote_mbDracStart, self.quotes_path + "mb_drac-who-dare-disturb-my-slumber.wav")
        self.game.sound.register_sound(self.quote_mbDracStart, self.quotes_path + "mb_drac-i-am-count-dracula-and-youre-not.wav")
        self.quote_mbDracMove = 'quote_mbDracMove'
        self.game.sound.register_sound(self.quote_mbDracMove, self.quotes_path + "mb_drac-look-out-now.wav")
        self.game.sound.register_sound(self.quote_mbDracMove, self.quotes_path + "mb_drac-over-here-garlic-breath.wav")
        self.game.sound.register_sound(self.quote_mbDracMove, self.quotes_path + "mb_drac-over-here-sphere-boy.wav")
        self.game.sound.register_sound(self.quote_mbDracMove, self.quotes_path + "mb_drac-watch-me-now.wav")
        self.quote_mbDracSmack = 'quote_mbDracSmack'
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-hey.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-ow.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-thats-my-feet.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-ooch.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-how-dare-you-strike-the-great-impaler.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-ouch.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-those-are-my-bruno-males.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-watch-the-family-jewels.wav")
        self.game.sound.register_sound(self.quote_mbDracSmack, self.quotes_path + "mb_drac-not-below-the-belt.wav")
        self.quote_mbDracWin = 'quote_mbDracWin'
        self.game.sound.register_sound(self.quote_mbDracWin, self.quotes_path + "mb_drac-can-i-get-some-fries-with-that-stake.wav")
        self.quote_mbDracLose = 'quote_mbDracLose'
        self.game.sound.register_sound(self.quote_mbDracLose, self.quotes_path + "mb_drac-blah-blah-blah.wav")
        self.quote_mbDracBad = 'quote_mbDracBad'
        self.game.sound.register_sound(self.quote_mbDracBad, self.quotes_path + "mb_drac-thats-lower-than-franks-iq.wav")

        self.quote_cvaTaunt = 'quote_cvaTaunt'
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "592-alien-you-dont-stand-a-chance.wav")
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "546-alien-nothing-can-defeat-us.wav")
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "544-alien-laugh-2.wav")
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "569-alien-taunt.wav")
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "543-alien-we-are-invincible.wav")
        self.game.sound.register_sound(self.quote_cvaTaunt, self.quotes_path + "538-alien-earth-will-be-ours.wav")

        self.quote_cvaTeleported = 'quote_cvaTeleported'
        self.game.sound.register_sound(self.quote_cvaTeleported, self.quotes_path + "532-alien-attack.wav")
        self.game.sound.register_sound(self.quote_cvaTeleported, self.quotes_path + "579-alien-martians-superior.wav")

        self.quote_welcomes = 'quote_welcomes'
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1202-prospector-welcome-to-cactus-canyon.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1101-mayor-dewey-cheetum-at-your-service.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1324-undertaker-welcome-to-cactus-canyon.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "2002-waitress-come-in-and-take-a-load-off-stranger.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1100-mayor-welcome-to-cactus-canyon-stranger.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "803-polly-welcome-to-town-stranger.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1851-leader-bart-well-lookie-here-sheriff-of-the-week.wav")
        self.quote_bountyLit = 'quote_bountyLit'
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1012-mayor-theres-a-bounty-just-waitin-for-ya.wav")
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1013-mayor-bounty-is-lit.wav")
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1043-mayor-collect-your-bounty-son.wav")
        self.quote_bountyCollected = 'quote_bountyCollected'
        self.game.sound.register_sound(self.quote_bountyCollected, self.quotes_path + "1014-mayor-your-bounty-friend.wav")
        self.game.sound.register_sound(self.quote_bountyCollected, self.quotes_path + "1042-mayor-bounty-collected.wav")
        self.quote_quickdrawLit = 'quote_quickdrawLit'
        self.game.sound.register_sound(self.quote_quickdrawLit, self.quotes_path + "509-townie-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickdrawLit, self.quotes_path + "1304-undertaker-oh-goodie-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickdrawLit, self.quotes_path + "1305-undertaker-quickdraws-are-good-for-business.wav")
        self.game.sound.register_sound(self.quote_quickdrawLit, self.quotes_path + "2040-waitress-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickdrawLit, self.quotes_path + "1037-mayor-quickdraw-is-lit.wav")
        self.quote_quickdrawStart = 'quote_quickdrawStart'
        self.game.sound.register_sound(self.quote_quickdrawStart, self.quotes_path + "1241-prospector-get-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawStart, self.quotes_path + "1274-prospector-nail-that-bad-guy-lawman.wav")
        self.game.sound.register_sound(self.quote_quickdrawStart, self.quotes_path + "1150-mayor-theres-a-bad-guy-out-there.wav")
        self.quote_quickdrawTaunt = 'quote_quickdrawTaunt'
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1151-mayor-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1554-leader-bart-go-on-take-your-best-shot.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1550-leader-bart-you-cant-shoot.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1552-leader-bart-come-on-tough-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1156-mayor-mertilate-that-villan.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1155-mayor-shoot-that-scurvy-scoundrel.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1277-prospector-the-bad-guy-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "2042-waitress-hit-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1520-leader-bart-go-get-im.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "1416-drunk-shoot-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "511-prospector-you-cant-shoot-nothin.wav")
        self.game.sound.register_sound(self.quote_quickdrawTaunt, self.quotes_path + "847-polly-blow-his-little-old-head-off.wav")
        self.quote_quickdrawWin = 'quote_quickdrawWin'
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "852-polly-nice-shootin.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1315-undertaker-my-theyre-dropping-like-flies.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "2003-waitress-i-didnt-like-that-deadbeat-anyway.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1318-undertaker-a-dead-ringer.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1111-mayor-that-was-a-bit-too-close-for-comfort.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "839-polly-youre-quite-a-man.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "840-polly-congratulations.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "2008-waitress-amazing.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "2005-waitress-ooh-what-are-you-packin.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1316-undertaker-so-many-bodies.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1117-mayor-say-thats-a-pretty-good-eye-there.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1170-mayor-quite-a-knack-with-those-six-shooters-friend.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "2015-waitress-i-like-that-colt-45.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1406-drunk-thats-a-good-one-buddy.wav")
        self.game.sound.register_sound(self.quote_quickdrawWin, self.quotes_path + "1538-leader-bart-aw-I-never-liked-him-anyway.wav")
        self.quote_bionicUrge = 'quote_bionicUrge'
        self.game.sound.register_sound(self.quote_bionicUrge, self.quotes_path + "1151-mayor-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_bionicUrge, self.quotes_path + "1277-prospector-the-bad-guy-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_bionicUrge, self.quotes_path + "2042-waitress-hit-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_bionicUrge, self.quotes_path + "1416-drunk-shoot-that-bad-guy.wav")

        self.quote_lockLit = 'quote_lockLit'
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1186-mayor-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "859-polly-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1431-drunk-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1432-drunk-lock-is-lit-and-so-am-i.wav")
        self.quote_leftRamp1 = 'quote_leftRamp1'
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "831-polly-im-gettin-all-wet.wav")
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "829-polly-were-headed-for-the-falls.wav")
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.quote_leftRamp2 = 'quote_leftRamp2'
        self.game.sound.register_sound(self.quote_leftRamp2, self.quotes_path + "830-polly-were-going-over-the-falls.wav")
        self.game.sound.register_sound(self.quote_leftRamp2, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.quote_rightRamp1 = 'quote_rightRamp1'
        self.game.sound.register_sound(self.quote_rightRamp1, self.quotes_path + "1134-mayor-well-do-somethin-my-moneys-in-there.wav")
        self.game.sound.register_sound(self.quote_rightRamp1, self.quotes_path + "1189-mayor-those-bart-boys-are-robbin-the-bank.wav")
        self.quote_rightRamp2 = 'quote_rightRamp2'
        self.game.sound.register_sound(self.quote_rightRamp2, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.game.sound.register_sound(self.quote_rightRamp2, self.quotes_path + "850-polly-ooh-how-brave.wav")
        self.quote_centerRamp1 = 'quote_centerRamp1'
        self.game.sound.register_sound(self.quote_centerRamp1, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.game.sound.register_sound(self.quote_centerRamp1, self.quotes_path + "1576-leader-bart-you-cant-stop-this-train.wav")
        self.game.sound.register_sound(self.quote_centerRamp1, self.quotes_path + "1552-leader-bart-come-on-tough-guy.wav")
        self.quote_centerRamp2 = 'quote_centerRamp2'
        self.game.sound.register_sound(self.quote_centerRamp2, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.game.sound.register_sound(self.quote_centerRamp2, self.quotes_path + "1504-leader-bart-looks-like-we-got-us-some-company-boys.wav")
        self.game.sound.register_sound(self.quote_centerRamp2, self.quotes_path + "1577-leader-bart-youll-never-catch-us.wav")
        self.game.sound.register_sound(self.quote_centerRamp2, self.quotes_path + "1553-leader-bart-im-over-here.wav")
        self.quote_leftLoop1 = 'quote_leftLoop1'
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1255-prospector-guess-that-horse-is-breaking-you-in.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1200-prospector-woo-cough.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.sfx_path + "115-sfx-horse-running-with-yell.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1254-prospector-oh-boy-thats-gotta-hurt.wav")
        self.quote_leftLoop2 = 'quote_leftLoop2'
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "2007-waitress-i-like-how-you-ride-that-horse.wav")
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "1187-mayor-a-fine-ride-sir.wav")
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "1256-prospector-ride-em-cowboy-hey-hey.wav")
        self.quote_victory = 'quote_victory'
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "836-polly-youre-the-greatest.wav")
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "837-polly-youre-my-hero.wav")
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "838-polly-my-hero.wav")
        self.quote_gunfightLit = 'quote_gunfightLit'
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1038-mayor-gunfight-is-lit.wav")
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1237-prospector-gunfight-is-lit.wav")
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1306-undertaker-theres-going-to-be-a-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1867-leader-bart-time-for-a-gunfight-lawman.wav")
        self.quote_gunfightStart = 'quote_gunfightStart'
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1004-mayor-ok-son-lets-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1029-mayor-dont-move-its-a-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "2041-waitress-looks-like-a-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1233-prospector-ooh-i-smell-a-gunfight-brewin.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1871-leader-bart-lets-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1544-leader-bart-this-is-my-town-lawman.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1573-leader-bart-lawman-its-you-and-me.wav")
        self.quote_gunfightWinMarshall = 'quote_gunfightWinMarshall'
        self.game.sound.register_sound(self.quote_gunfightWinMarshall, self.quotes_path + "2027-waitress-nice-shootin-marshall.wav")
        self.quote_rankUpMarshall = 'quote_rankUpMarshall'
        self.game.sound.register_sound(self.quote_rankUpMarshall, self.quotes_path + "1147-mayor-congratulations-marshall.wav")
        self.game.sound.register_sound(self.quote_rankUpMarshall, self.quotes_path + "1129-mayor-fair-townsfolk-the-new-marshall.wav")
        self.quote_gunfightWinSheriff = 'quote_gunfightWinSheriff'
        self.game.sound.register_sound(self.quote_gunfightWinSheriff, self.quotes_path + "2026-waitress-nice-shootin-sheriff.wav")
        self.quote_rankUpSheriff = 'quote_rankUpSheriff'
        self.game.sound.register_sound(self.quote_rankUpSheriff, self.quotes_path + "1146-mayor-congratulations-sheriff.wav")
        self.game.sound.register_sound(self.quote_rankUpSheriff, self.quotes_path + "863-polly-congratulations-sheriff.wav")
        self.game.sound.register_sound(self.quote_rankUpSheriff, self.quotes_path + "1128-mayor-citizens-our-new-sheriff.wav")
        self.quote_gunfightWinDeputy = 'quote_gunfightWinDeputy'
        self.game.sound.register_sound(self.quote_gunfightWinDeputy, self.quotes_path + "2025-waitress-nice-shootin-deputy.wav")
        self.quote_rankUpDeputy = 'quote_rankUpDeputy'
        self.game.sound.register_sound(self.quote_rankUpDeputy, self.quotes_path + "1145-mayor-contratulations-deputy.wav")
        self.game.sound.register_sound(self.quote_rankUpDeputy, self.quotes_path + "862-polly-congratulations-deputy.wav")
        self.quote_gunfightWinPartner = 'quote_gunfightWinPartner'
        self.game.sound.register_sound(self.quote_gunfightWinPartner, self.quotes_path + "2024-waitress-nice-shootin-partner.wav")
        self.quote_rankUpPartner = 'quote_rankUpPartner'
        self.game.sound.register_sound(self.quote_rankUpPartner, self.quotes_path + "1144-mayor-congratulations-partner.wav")
        self.game.sound.register_sound(self.quote_rankUpPartner, self.quotes_path + "861-polly-congratulations-partner.wav")
        self.quote_gunFail = 'quote_gunFail'
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1198-mayor-maybe-you-better-check-the-sights-on-that-weapon.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1199-mayor-are-you-sure-that-thing-is-loaded.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1505-leader-bart-better-luck-next-time.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1564-leader-bart-well-im-still-standin.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1563-leader-bart-aw-you-missed.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1321-undertaker-your-shooting-is-killing-me.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1244-prospector-say-is-that-thing-loaded.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1280-prospector-check-the-sights.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1565-leader-bart-you-missed.wav")
        self.quote_superFail = 'quote_superFail'
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1505-leader-bart-better-luck-next-time.wav")
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1563-leader-bart-aw-you-missed.wav")
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1565-leader-bart-you-missed.wav")
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.quote_beerMug = 'quote_beerMug'
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1408-drunk-hey-buddy-you-shot-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1409-drunk-stop-shootin-at-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1414-drunk-i-was-drinking-that-thank-you.wav")
        self.quote_extraBallLit = 'quote_extraBallLit'
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "2013-waitress-that-extra-ball-is-lit-honey.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1258-prospector-extra-ball-is-lit.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1020-mayor-the-extra-ball-is-lit.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1036-mayor-shoot-the-mine-to-collect.wav")
        self.quote_extraBallSet = 'quote_extraBallSet'
        self.game.sound.register_sound(self.quote_extraBallSet, self.quotes_path + "2018-waitress-extra-ball.wav")
        self.quote_goodbye = 'quote_goodbye'
        self.game.sound.register_sound(self.quote_goodbye, self.quotes_path + "1317-undertaker-hope-to-see-you-soon.wav")
        self.game.sound.register_sound(self.quote_goodbye, self.quotes_path + "1421-drunk-its-all-over-citizens.wav")
        self.game.sound.register_sound(self.quote_goodbye, self.quotes_path + "876-polly-come-back-soon.wav")
        self.game.sound.register_sound(self.quote_goodbye, self.quotes_path + "1010-mayor-thank-you-for-cleaning-up-cactus-canyon.wav")
        self.game.sound.register_sound(self.quote_goodbye, self.quotes_path + "1557-leader-bart-on-to-the-next-town-boys.wav")
        self.quote_stampedeStart = 'quote_stampedeStart'
        self.game.sound.register_sound(self.quote_stampedeStart, self.quotes_path + "1260-prospector-its-a-stampede.wav")
        self.game.sound.register_sound(self.quote_stampedeStart, self.quotes_path + "531-prospector-stampede-multiball.wav")
        self.quote_jackpot = 'quote_jackpot'
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "530-prospector-jackpot.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "529-prospector-jackpot-hey-hey.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "2017-waitress-jackpot.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "1430-drunk-jackpot-whoopie.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "1433-drunk-jackpot-ill-drink-to-that.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "1039-mayor-jackpot.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "851-polly-jackpot.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "1218-prospector-jackpot.wav")
        self.game.sound.register_sound(self.quote_jackpot, self.quotes_path + "532-prospector-jackpot-yee-ha.wav")
        self.quote_stampedeWiff = 'quote_stampedeWiff'
        self.game.sound.register_sound(self.quote_stampedeWiff, self.quotes_path + "1243-prospector-woo-hoo.wav")
        self.game.sound.register_sound(self.quote_stampedeWiff, self.quotes_path + "1200-prospector-woo-cough.wav")
        self.quote_motherlode = 'quote_motherlode'
        self.game.sound.register_sound(self.quote_motherlode, self.quotes_path + "1185-mayor-motherlode.wav")
        self.game.sound.register_sound(self.quote_motherlode, self.quotes_path + "528-prospector-motherlode-yee-hoo.wav")
        self.game.sound.register_sound(self.quote_motherlode, self.quotes_path + "533-prospector-motherlode-yee-hoo.wav")
        self.quote_doubleMotherlode = 'quote_doubleMotherlode'
        self.game.sound.register_sound(self.quote_doubleMotherlode, self.quotes_path + "542-prospector-double-motherlode.wav")
        self.quote_tripleMotherlode = 'quote_tripleMotherlode'
        self.game.sound.register_sound(self.quote_tripleMotherlode, self.quotes_path + "543-prospector-triple-motherlode.wav")
        self.quote_motherlodeLit = 'quote_motherlodeLit'
        self.game.sound.register_sound(self.quote_motherlodeLit, self.quotes_path + "1227-prospector-motherlode-is-lit.wav")
        self.game.sound.register_sound(self.quote_motherlodeLit, self.quotes_path + "1249-prospector-shoot-the-mine.wav")
        self.quote_highNoon = 'quote_highNoon'
        self.game.sound.register_sound(self.quote_highNoon, self.quotes_path + "1006-mayor-oh-no-its-high-noon.wav")
        self.quote_highNoonStart = 'quote_highNoonStart'
        self.game.sound.register_sound(self.quote_highNoonStart, self.quotes_path + "1271-prospector-wanna-win-shoot-the-bad-guys.wav")
        self.game.sound.register_sound(self.quote_highNoonStart, self.quotes_path + "1003-mayor-shoot-everything.wav")
        self.quote_highNoonWin = 'quotehighNoonWin'
        self.game.sound.register_sound(self.quote_highNoonWin, self.quotes_path + "1135-mayor-a-job-well-done.wav")
        self.game.sound.register_sound(self.quote_highNoonWin, self.quotes_path + "1308-undertaker-oh-goody-you-shot-them-all.wav")
        self.game.sound.register_sound(self.quote_highNoonWin, self.quotes_path + "1562-leader-bart-aw-you-shot-everybody.wav")
        self.quote_shootAgain = 'quote_shootAgain'
        self.game.sound.register_sound(self.quote_shootAgain, self.quotes_path + "810-polly-im-so-glad-youre-back.wav")
        self.game.sound.register_sound(self.quote_shootAgain, self.quotes_path + "2021-waitress-shoot-again.wav")
        self.game.sound.register_sound(self.quote_shootAgain, self.quotes_path + "854-polly-shoot-again.wav")
        self.game.sound.register_sound(self.quote_shootAgain, self.quotes_path + "875-polly-try-again-big-fella.wav")
        self.game.sound.register_sound(self.quote_shootAgain, self.quotes_path + "1133-mayor-welcome-back.wav")

        self.quote_hurry = 'quote_hurry'
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1175-mayor-i-suggest-you-hurry-friend.wav")
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1173-mayor-time-for-one-more-shot.wav")
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1205-prospector-hurry-youre-runnin-outta-time.wav")

        self.quote_pollyHurry = 'quote_pollyHurry'
        self.game.sound.register_sound(self.quote_pollyHurry, self.quotes_path + "815-polly-hurry-hurry.wav")
        self.game.sound.register_sound(self.quote_pollyHurry, self.quotes_path + "816-polly-hurry.wav")
        self.game.sound.register_sound(self.quote_pollyHurry, self.quotes_path + "mayor-save-miss-polly.wav")

        self.quote_pollyPlead = 'quote_pollyPlead'
        self.game.sound.register_sound(self.quote_pollyPlead, self.quotes_path + "814-polly-be-a-gentlemen-and-save-me.wav")
        self.game.sound.register_sound(self.quote_pollyPlead, self.quotes_path + "818-polly-help.wav")
        self.game.sound.register_sound(self.quote_pollyPlead, self.quotes_path + "811-polly-save-little-old-me.wav")
        self.game.sound.register_sound(self.quote_pollyPlead, self.quotes_path + "mayor-miss-polly-needs-your-help.wav")
        self.game.sound.register_sound(self.quote_pollyPlead, self.quotes_path + "1266-prospector-miss-polly-is-in-trouble.wav")

        self.quote_pollyStop = 'quote_pollyStop'
        self.game.sound.register_sound(self.quote_pollyStop, self.quotes_path + "823-polly-stop-the-train.wav")

        self.quote_ttttIntro = 'quote_ttttIntro'
        self.game.sound.register_sound(self.quote_ttttIntro, self.quotes_path + "1193-mayor-miss-polly-tracks-2.wav")
        self.game.sound.register_sound(self.quote_ttttIntro, self.quotes_path + "1193-mayor-miss-polly-tracks.wav")
        self.game.sound.register_sound(self.quote_ttttIntro, self.quotes_path + "mayor-bart-boys-tied-miss-polly-to-the-tracks.wav")
        self.game.sound.register_sound(self.quote_ttttIntro, self.quotes_path + "822-polly-im-tied-to-the-track.wav")
        self.game.sound.register_sound(self.quote_ttttIntro, self.quotes_path + "849-polly-why-do-they-always-tie-me-to-the-tracks.wav")

        self.quote_rotrIntro = 'quote_rotrIntro'
        self.game.sound.register_sound(self.quote_rotrIntro, self.quotes_path + "mayor-they-went-down-to-the-river.wav")
        self.game.sound.register_sound(self.quote_rotrIntro, self.quotes_path + "mayor-hurry-sheriff-catch-that-boat.wav")
        self.game.sound.register_sound(self.quote_rotrIntro, self.quotes_path + "00-mayor-dont-let-em-get-away.wav")


        self.quote_hatbIntro = 'quote_hatbIntro'
        self.game.sound.register_sound(self.quote_hatbIntro, self.quotes_path + "mayor-hostage-in-the-bank.wav")
        self.game.sound.register_sound(self.quote_hatbIntro, self.quotes_path + "mayor-miss-pollys-in-there-sheriff.wav")
        self.game.sound.register_sound(self.quote_hatbIntro, self.quotes_path + "1307-undertaker-oh-good-mayhem-at-the-bank.wav")


        self.quote_mobStart = 'quote_mobStart'
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1171-mayor-shoot-anything-that-pops-up.wav")
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1259-prospector-shoot-all-the-bad-guys.wav")
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1152-mayor-ive-had-about-enough-of-those-bart-boys.wav")
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1401-drunk-lookout.wav")
        self.quote_mobTaunt = 'quote_mobTaunt'
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "2020-waitress-honey-just-shoot-anything.wav")
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "1165-mayor-aw-just-shoot-em.wav")
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "1525-leader-bart-git-that-law-man.wav")
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "1157-mayor-those-nefarious-nogoodnicks.wav")
        self.quote_mobEnd = 'quote_mobEnd'
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1303-prospector-look-at-that-bodycount.wav")
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1169-mayor-nice-shootin-sir.wav")
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1309-undertaker-a-respectable-bodycount-indeed.wav")
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1209-prospector-well-that-was-some-nice-shootin.wav")

        self.quote_cvaIntro = 'quote_cvaIntro'
        self.game.sound.register_sound(self.quote_cvaIntro, self.quotes_path + "mayor-something-strange-is-going-on-here.wav")
        self.game.sound.register_sound(self.quote_cvaIntro, self.quotes_path + "mayor-this-can-not-be-a-good-thing.wav")
        self.game.sound.register_sound(self.quote_cvaIntro, self.quotes_path + "mayor-whats-that-strange-light-in-the-sky.wav")

        self.quote_cvaEnd = 'quote_cvaEnd'
        self.game.sound.register_sound(self.quote_cvaEnd, self.quotes_path + "mayor-boy-im-glad-thats-over.wav")
        self.game.sound.register_sound(self.quote_cvaEnd, self.quotes_path + "mayor-strange-geckos.wav")
        self.game.sound.register_sound(self.quote_cvaEnd, self.quotes_path + "mayor-those-things-were-ugly.wav")

        self.quote_mytTaunt = 'quote_mytTaunt'
        self.game.sound.register_sound(self.quote_mytTaunt, self.quotes_path + "mayor-need-to-move-that-train.wav")

        self.quote_introBigBart = 'quote_introBigBart'
        self.game.sound.register_sound(self.quote_introBigBart, self.quotes_path + "1466-big-name-is-big-bart-tough-guy.wav")
        self.quote_hitBigBart = 'quote_hitBigBart'
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1451-big-hit-that-hurt-a-little.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1452-big-hit-nothin-but-a-little-hole.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1456-big-hit-ow-i-said.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1460-big-hit-ow.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1462-big-hit-well-that-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1464-big-hit-ow-dangit.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1465-big-hit-well-i-can-tell-ya-that-hurt.wav")
        self.quote_tauntBigBart = 'quote_tauntBigBart'
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1450-big-taunt-mess-with-me-will-ya.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1454-big-taunt-youre-messin-with-the-wrong-hombre-hombre.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1457-big-taunt-im-gonna-shoot-my-initials-in-ya-lawman.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1467-big-taunt-what-do-you-think-youre-doin-pilgrim.wav")
        self.quote_defeatBigBart = 'quote_defeatBigBart'
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1468-big-defeat-well-im-done-for.wav")
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1469-big-defeat-well-thats-all-folks.wav")
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1470-big-defeat-i-guess-ill-just-fall-down-now.wav")

        self.quote_introBandeleroBart = 'quote_introBandeleroBart'
        self.game.sound.register_sound(self.quote_introBandeleroBart, self.quotes_path + "1805-bandelero-youre-messing-with-bandelero.wav")
        self.quote_hitBandeleroBart = 'quote_hitBandeleroBart'
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1803-bandelero-hit-oh-i-think-ive-been-hit.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1804-bandelero-hit-that-one-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1806-bandelero-hit-ooh-ive-been-air-conditioned.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1809-bandelero-hit-look-at-all-this-blood-my-wife-is-going-to-kill-me.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1810-bandelero-hit-holy-camochie-ive-been-shot.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1823-bandelero-hit-ooh.wav")
        self.quote_tauntBandeleroBart = 'quote_tauntBandeleroBart'
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1801-bandelero-taunt-you-dont-think-i-see-you-but-i-do.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1807-bandelero-taunt-you-couldnt-hit-the-broad-side-of-a-burrito.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1808-bandelero-taunt-my-burro-can-shoot-better-than-that.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1821-bandelero-taunt-come-on-lone-ranger.wav")
        self.quote_defeatBandeleroBart = 'quote_defeatBandeleroBart'
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1813-bandelero-defeat-adios-amigo-time-for-a-siesta.wav")
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1814-bandelero-defeat-say-youre-pretty-good.wav")
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1824-bandelero-defeat-you-got-me.wav")

        self.quote_introBubbaBart = 'quote_introBubbaBart'
        self.game.sound.register_sound(self.quote_introBubbaBart, self.quotes_path + "1915-bubba-taunt-me-bubba-you-dead.wav")
        self.quote_hitBubbaBart = 'quote_hitBubbaBart'
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1900-bubba-hit-bubba-hit.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1901-bubba-hit-bubba-mad-now.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1906-bubba-hit-shiny-ball-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1909-bubba-hit-uh.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1910-bubba-hit-groan.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1912-bubba-hit-oh.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1914-bubba-hit-groan2.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1918-bubba-hit-groan3.wav")
        self.quote_tauntBubbaBart = 'quote_tauntBubbaBart'
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1902-bubba-taunt-you-mess-wif-bubba-bubba-mess-wif-you.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1903-bubba-taunt-bubba-mess-pants.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1905-bubba-taunt-bubba-like-shiny-silver-ball.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1917-bubba-taunt-bubba-gonna-mess-you-up.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1919-bubba-taunt-youre-dead.wav")
        self.quote_defeatBubbaBart = 'quote_defeatBubbaBart'
        self.game.sound.register_sound(self.quote_defeatBubbaBart, self.quotes_path + "1904-bubba-defeat-bubba-take-dirt-nap.wav")
        self.game.sound.register_sound(self.quote_defeatBubbaBart, self.quotes_path + "1916-bubba-defeat-nite-nite-bubba-go-to-sleep-now.wav")

        self.quote_introBossBart = 'quote_introBossBart'
        self.game.sound.register_sound(self.quote_introBossBart, self.quotes_path + "1850-leader-bart-intro-were-the-bart-boys-and-im-the-boss.wav")

        self.quote_hitBossBart = 'quote_hitBossBart'
        self.game.sound.register_sound(self.quote_hitBossBart, self.quotes_path + "1555-leader-bart-hit-oh-hot-lead.wav")
        self.game.sound.register_sound(self.quote_hitBossBart, self.quotes_path + "1551-leader-bart-hit-nothin-but-a-scratch.wav")
        self.game.sound.register_sound(self.quote_hitBossBart, self.quotes_path + "1859-leader-bart-hit-i-never-use-that-finger-anyway.wav")
        self.game.sound.register_sound(self.quote_hitBossBart, self.quotes_path + "1856-leader-bart-hit-oh-im-hit.wav")
        self.game.sound.register_sound(self.quote_hitBossBart, self.quotes_path + "1857-leader-bart-hit-just-a-flesh-wound.wav")

        self.quote_defeatBossBart = 'quote_defeatBossBart'
        self.game.sound.register_sound(self.quote_defeatBossBart, self.quotes_path+ "1862-leader-bart-defeat-nice-knowin-ya-boys.wav")
        self.game.sound.register_sound(self.quote_defeatBossBart, self.quotes_path+ "1860-leader-bart-defeat-i-think-ill-just-rest.wav")
        self.game.sound.register_sound(self.quote_defeatBossBart, self.quotes_path+ "1866-leader-bart-defeat-seeya-six-feet-under.wav")
        self.game.sound.register_sound(self.quote_defeatBossBart, self.quotes_path+ "1864-leader-bart-defeat-hes-better-than-he-looks.wav")
        self.game.sound.register_sound(self.quote_defeatBossBart, self.quotes_path+ "1861-leader-bart-defeat-well-boys-im-a-goner.wav")

        self.quote_tauntBossBart = 'quote_tauntBossBart'
        self.game.sound.register_sound(self.quote_tauntBossBart, self.quotes_path + "1582-leader-bart-taunt-youre-askin-for-it.wav")
        self.game.sound.register_sound(self.quote_tauntBossBart, self.quotes_path + "1852-leader-bart-taunt-i-love-the-smell-of-lead.wav")
        self.game.sound.register_sound(self.quote_tauntBossBart, self.quotes_path + "1549-leader-bart-taunt-show-me-yer-stuff.wav")
        self.game.sound.register_sound(self.quote_tauntBossBart, self.quotes_path + "1501-leader-bart-taunt-you-got-a-hankerin.wav")

        self.quote_targetBossBart = 'quote_targetBossBart'
        self.game.sound.register_sound(self.quote_targetBossBart, self.quotes_path+ "1870-leader-bart-target-you-hurt-my-brother.wav")
        self.game.sound.register_sound(self.quote_targetBossBart, self.quotes_path+ "1869-leader-bart-target-that-was-my-brother.wav")
        self.game.sound.register_sound(self.quote_targetBossBart, self.quotes_path+ "1868-leader-bart-target-you-shot-my-brother.wav")
        self.game.sound.register_sound(self.quote_targetBossBart, self.quotes_path+ "1535-leader-bart-target-you-shot-my-brother.wav")

        self.quote_bionicIntroQuote = 'quote_bionicIntroQuote'
        self.game.sound.register_sound(self.quote_bionicIntroQuote, self.quotes_path + "1569-leader-bart-alright-tough-guy-deal-with-this.wav")
        self.game.sound.register_sound(self.quote_bionicIntroQuote, self.quotes_path + "1568-leader-bart-my-secret-weapon.wav")
        self.game.sound.register_sound(self.quote_bionicIntroQuote, self.quotes_path + "1583-leader-bart-prepare-for-pain-lawman.wav")
        self.game.sound.register_sound(self.quote_bionicIntroQuote, self.quotes_path + "1586-leader-bart-alright-ive-had-it.wav")

        self.quote_introBionicBart = 'quote_introBionicBart'
        self.game.sound.register_sound(self.quote_introBionicBart, self.quotes_path + "2100-bionic-bart-i-am-a-bionic-bart-unit.wav")

        self.quote_tauntBionicBart = 'quote_tauntBionicBart'
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2122-bionic-bart-eat-my-tire-treads-cowpoke.wav")
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2120-bionic-bart-puny-carbon-unit.wav")
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2119-bionic-bart-steel-balls-do-not-phase-me.wav")
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2118-bionic-bart-i-am-the-new-sheriff-in-town.wav")
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2102-bionic-bart-prepare-for-anhiliation-cowboy.wav")
        self.game.sound.register_sound(self.quote_tauntBionicBart, self.quotes_path + "2103-bionic-bart-time-for-payback-lawman.wav")

        self.quote_failBionicBart = 'quote_failBionicBart'
        self.game.sound.register_sound(self.quote_failBionicBart, self.quotes_path + "2115-bionic-bart-i-am-not-through-with-you-yet.wav")

        self.quote_defeatBionicBart = 'quote_defeatBionicBart'
        self.game.sound.register_sound(self.quote_defeatBionicBart, self.quotes_path + "2124-bionic-bart-game-over.wav")
        self.game.sound.register_sound(self.quote_defeatBionicBart, self.quotes_path + "2116-bionic-bart-please-send-me-to.wav")
        self.game.sound.register_sound(self.quote_defeatBionicBart, self.quotes_path + "2105-bionic-bart-my-systems-are-shutting-down.wav")
        self.game.sound.register_sound(self.quote_defeatBionicBart, self.quotes_path + "2101-bionic-bart-hasta-la-vista.wav")

        self.quote_hitBionicBart = 'quote_hitBionicBart'
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2109-bionic-bart-ow.wav")
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2110-bionic-bart-ouch-that-one-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2108-bionic-bart-you-put-a-hole-in-my-machinery.wav")
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2107-bionic-bart-that-does-not-feel-good.wav")
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2106-bionic-bart-you-are-scrambling-my-memory-banks.wav")
        self.game.sound.register_sound(self.quote_hitBionicBart, self.quotes_path + "2104-bionic-bart-you-have-dented-my-armor.wav")

        self.quote_leaderFailBionic = 'quote_leaderFailBionic'
        self.game.sound.register_sound(self.quote_leaderFailBionic, self.quotes_path + "1505-leader-bart-better-luck-next-time.wav")
        self.game.sound.register_sound(self.quote_leaderFailBionic, self.quotes_path + "1506-leader-bart-well-be-back-lawman.wav")
        self.game.sound.register_sound(self.quote_leaderFailBionic, self.quotes_path + "1579-leader-bart-laugh-2.wav")

        self.quote_leaderWinBionic = 'quote_leaderWinBionic'
        self.game.sound.register_sound(self.quote_leaderWinBionic, self.quotes_path + "1533-leader-bart-you-broke-my-favorite-toy.wav")
        self.game.sound.register_sound(self.quote_leaderWinBionic, self.quotes_path + "1570-leader-bart-oh-i-just-bought-that-thing.wav")
        self.game.sound.register_sound(self.quote_leaderWinBionic, self.quotes_path + "1571-leader-bart-you-broke-my-toy.wav")
        self.game.sound.register_sound(self.quote_leaderWinBionic, self.quotes_path + "1572-leader-bart-boy-they-dont-make-em.wav")
        self.game.sound.register_sound(self.quote_leaderWinBionic, self.quotes_path + "1585-leader-bart-im-gonna-get-my-money-back.wav")


        self.quote_pollyHelp = 'quote_pollyHelp'
        self.game.sound.register_sound(self.quote_pollyHelp, self.quotes_path + "802-polly-help.wav")
        self.quote_pollyThankYou = 'quote_pollyThankYou'
        self.game.sound.register_sound(self.quote_pollyThankYou,self.quotes_path + "835-polly-thank-you.wav")
        self.quote_playerOne = 'quote_playerOne'
        self.game.sound.register_sound(self.quote_playerOne, self.quotes_path + "855-polly-player-one.wav")
        self.quote_playerTwo = 'quote_playerTwo'
        self.game.sound.register_sound(self.quote_playerTwo, self.quotes_path + "856-polly-player-two.wav")
        self.quote_playerThree = 'quote_playerThree'
        self.game.sound.register_sound(self.quote_playerThree, self.quotes_path + "857-polly-player-three.wav")
        self.quote_playerFour = 'quote_playerFour'
        self.game.sound.register_sound(self.quote_playerFour, self.quotes_path + "858-polly-player-four.wav")
        self.quote_mayorMyMoneysInThere = 'quote_mayorMyMoneysInThere'
        self.game.sound.register_sound(self.quote_mayorMyMoneysInThere, self.quotes_path + "1134-mayor-well-do-somethin-my-moneys-in-there.wav")
        self.quote_gunfightReady = 'quote_gunfightReady'
        self.game.sound.register_sound(self.quote_gunfightReady, self.quotes_path + "1546-leader-bart-ready.wav")
        self.quote_gunfightSet = 'quote_gunfight_Set'
        self.game.sound.register_sound(self.quote_gunfightSet, self.quotes_path + "1547-leader-bart-set.wav")
        self.quote_gunfightDraw = 'quote_gunfightDraw'
        self.game.sound.register_sound(self.quote_gunfightDraw, self.quotes_path + "1507-leader-bart-draw.wav")
        self.quote_gold = 'quote_gold'
        self.game.sound.register_sound(self.quote_gold, self.quotes_path + "539-prospector-gold.wav")
        self.quote_mine = 'quote_mine'
        self.game.sound.register_sound(self.quote_mine, self.quotes_path + "540-prospector-mine.wav")
        self.quote_multiball = 'quote_multiball'
        self.game.sound.register_sound(self.quote_multiball, self.quotes_path + "536-prospector-multiball.wav")
        self.quote_extraBallGuy = 'quote_extraBallGuy'
        self.game.sound.register_sound(self.quote_extraBallGuy, self.quotes_path + "538-guy-extra-ball.wav")
        self.quote_thirsty = 'quote_thirsty'
        self.game.sound.register_sound(self.quote_thirsty, self.quotes_path + "1427-drunk-boy-im-thirsty.wav")
        self.quote_whatThe = 'quote_whatThe'
        self.game.sound.register_sound(self.quote_whatThe, self.quotes_path + "1423-drunk-what-the.wav")
        self.quote_dontMove = 'quote_dontMove'
        self.game.sound.register_sound(self.quote_dontMove, self.quotes_path + "1265-prospector-dont-move.wav")
        self.quote_dontJustStandThere = 'quote_dontJustStandThere'
        self.game.sound.register_sound(self.quote_dontJustStandThere, self.quotes_path + "1196-mayor-dont-just-stand-there-do-somethin.wav")
        self.quote_gasp = 'quote_gasp'
        self.game.sound.register_sound(self.quote_gasp, self.quotes_path + "878-polly-gasp.wav")
        self.quote_showdown = 'quote_showdown'
        self.game.sound.register_sound(self.quote_showdown, self.quotes_path + "1005-mayor-oh-my-a-showdown.wav")
        self.game.sound.register_sound(self.quote_showdown, self.quotes_path + "541-prospector-showdown.wav")
        self.quote_ambush = 'quote_ambush'
        self.game.sound.register_sound(self.quote_ambush, self.quotes_path + "00-mayor-look-out-sheriff-its-an-ambush.wav")
        self.game.sound.register_sound(self.quote_ambush, self.quotes_path + "00-mayor-oh-no-its-an-ambush.wav")
        self.quote_ambushUrge = 'quote_ambushUrge'
        self.game.sound.register_sound(self.quote_ambushUrge, self.quotes_path + "00-mayor-dont-let-em-get-away.wav")
        self.game.sound.register_sound(self.quote_ambushUrge, self.quotes_path + "00-mayor-shoot-the-bad-guys-before-they-get-away.wav")
        self.quote_drunkMultiballLit = 'quote_drunkMultiballLit'
        self.game.sound.register_sound(self.quote_drunkMultiballLit, self.quotes_path + "1116-mayor-this-calls-for-a-drink.wav")
        self.quote_drunkNeverSeen = 'quote_drunkNeverSeen'
        self.game.sound.register_sound(self.quote_drunkNeverSeen, self.quotes_path + "1418-drunk-ooh-i-never-seen-nothin-like-that.wav")
        self.quote_drunkDrinkToThat = 'quote_drunkDrinkToThat'
        self.game.sound.register_sound(self.quote_drunkDrinkToThat, self.quotes_path + "1433-drunk-ill-drink-to-that.wav")
        self.quote_drunkJackpot = 'quote_drunkJackpot'
        self.game.sound.register_sound(self.quote_drunkJackpot, self.quotes_path + "1430-drunk-jackpot-whoopie.wav")
        self.quote_deepLaugh = 'quote_deepLaugh'
        self.game.sound.register_sound(self.quote_deepLaugh, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.quote_superSkillShot = 'quote_SuperSKillShot'
        self.game.sound.register_sound(self.quote_superSkillShot, self.quotes_path + "00-Mayor-SuperSkillShot.wav")
        self.quote_leftLoopSS = 'quote_leftLoopSS'
        self.game.sound.register_sound(self.quote_leftLoopSS, self.quotes_path + "00-Mayor-LeftLoop.wav")
        self.quote_leftRampSS = 'quote_leftRampSS'
        self.game.sound.register_sound(self.quote_leftRampSS, self.quotes_path + "1118-mayor-that-left-ramp-is-wiiide-open.wav")
        self.game.sound.register_sound(self.quote_leftRampSS, self.quotes_path + "1267-prospector-head-up-the-left-ramp.wav")
        self.quote_centerRampSS = 'quote_centerRampSS'
        self.game.sound.register_sound(self.quote_centerRampSS, self.quotes_path + "1167-mayor-head-up-the-center-ramp-sir.wav")
        self.game.sound.register_sound(self.quote_centerRampSS, self.quotes_path + "1268-prospector-shoot-the-center-ramp.wav")
        self.quote_mineSS = 'quote_mineSS'
        self.game.sound.register_sound(self.quote_mineSS, self.quotes_path + "1036-mayor-shoot-the-mine.wav")
        self.game.sound.register_sound(self.quote_mineSS, self.quotes_path + "1249-prospector-shoot-the-mine2.wav")
        self.quote_leaderLaugh = 'quote_leaderLaugh'
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1581-leader-bart-laugh-3.wav")
        self.quote_nobodysHome = 'quote_nobodysHome'
        self.game.sound.register_sound(self.quote_nobodysHome, self.quotes_path + "1853-leader-bart-nobodys-home.wav")
        self.quote_marshallMultiball = 'quote_marshallMultiball'
        self.game.sound.register_sound(self.quote_marshallMultiball, self.quotes_path + "544-marshall-multiball.wav")

        self.quote_yippie = 'quote_yippie'
        self.game.sound.register_sound(self.quote_yippie, self.quotes_path + "1959-yip-yip-yippie.wav")
        self.game.sound.register_sound(self.quote_yippie, self.quotes_path + "1957-woohoo-yippie.wav")

        self.quote_mineOpen = 'quote_mineOpen'
        self.game.sound.register_sound(self.quote_mineOpen, self.quotes_path + "1183-quote-mayor-mine-is-wide-open.wav")
        self.quote_niceLoopin = 'quote_niceLoopin'
        self.game.sound.register_sound(self.quote_niceLoopin, self.quotes_path + "1120-quote-mayor-nice-loopin-sir.wav")
        self.quote_shootSaloon = 'quote_shootSaloon'
        self.game.sound.register_sound(self.quote_shootSaloon, self.quotes_path + "1025-mayor-shoot-the-saloon.wav")

        self.quote_4lights = 'quote_4lights'
        self.game.sound.register_sound(self.quote_4lights, self.quotes_path + "1031-mayor-only-4-lights.wav")
        self.quote_3lights = 'quote_3lights'
        self.game.sound.register_sound(self.quote_3lights, self.quotes_path + "1032-mayor-only-3-lights.wav")
        self.quote_2lights = 'quote_2lights'
        self.game.sound.register_sound(self.quote_2lights, self.quotes_path + "1033-mayor-only-2-lights.wav")
        self.quote_1light = 'quote_1light'
        self.game.sound.register_sound(self.quote_1light, self.quotes_path + "1034-mayor-only-1-light.wav")

        self.quote_toasty = 'quote_toasty'
        self.game.sound.register_sound(self.quote_toasty, self.quotes_path + "mm-570-toasty.wav")

        # Music
        self.music_drumRiff = 'music_drumRiff'
        self.game.sound.register_sound(self.music_drumRiff, self.music_path + "001-drum-lead-in.wav")
        self.music_shooterLaneGroove = 'music_shooterLaneGroove'
        self.game.sound.register_music(self.music_shooterLaneGroove, self.music_path + "001-shooter-lane-groove.wav")
        self.music_mainTheme = 'music_mainTheme'
        self.game.sound.register_music(self.music_mainTheme, self.music_path + "002-song-starting-gameplay.wav")
        self.music_quickdrawBumper = 'music_quickdrawBumper'
        self.game.sound.register_sound(self.music_quickdrawBumper, self.music_path + "017-quickdraw-bumper.wav")
        self.music_quickdraw = 'music_quickdraw'
        self.game.sound.register_music(self.music_quickdraw, self.music_path + "025-quickdraw.wav")
        self.music_gunfightIntro = 'music_gunfightIntro'
        self.game.sound.register_sound(self.music_gunfightIntro, self.music_path + "009-gunfight-intro.wav")
        self.music_drumRoll = 'music_drumRoll'
        self.game.sound.register_music(self.music_drumRoll, self.music_path + "009-gunfight-drumroll.wav")
        self.music_multiball_intro = 'music_multiball_intro'
        self.game.sound.register_music(self.music_multiball_intro, self.music_path + "026-multiball-intro-music.wav")
        self.music_pollyPeril = 'music_pollyPeril'
        self.game.sound.register_music(self.music_pollyPeril, self.music_path + "031-polly-peril.wav")
        self.music_altPeril = 'music_altPeril'
        self.game.sound.register_music(self.music_altPeril, self.music_path + "cowboy.wav")
        self.music_highScoreLead = 'music_highScoreLead'
        self.game.sound.register_sound(self.music_highScoreLead, self.music_path + "044-high-score-entry-lead.wav")
        self.music_goldmineMultiball = 'music_goldmineMultiball'
        self.game.sound.register_music(self.music_goldmineMultiball, self.music_path + "008-goldmine-multiball.wav")
        self.music_showdown = 'music_showdown'
        self.game.sound.register_music(self.music_showdown, self.music_path + "022-showdown.wav")
        self.music_stampede = 'music_stampede'
        self.game.sound.register_music(self.music_stampede, self.music_path + "003-stampede.wav")
        self.music_highNoonLead = 'music_highNoonLead'
        self.game.sound.register_sound(self.music_highNoonLead, self.music_path + "099-music-high-noon-lead-in.wav")
        self.music_highNoon = 'music_highNoon'
        self.game.sound.register_music(self.music_highNoon, self.music_path + "099-music-high-noon.wav")
        self.music_drunkMultiball = 'music_drunkMultiball'
        self.game.sound.register_music(self.music_drunkMultiball, self.music_path + "005-not-shooter-lane-groove.wav")
        self.music_bionicBartIntro = 'music_bionicBartIntro'
        self.game.sound.register_sound(self.music_bionicBartIntro, self.music_path + "042-intro-bionic-bart.wav")
        self.music_bionicBart = 'music_bionicBart'
        self.game.sound.register_music(self.music_bionicBart, self.music_path + "042-bionic-bart.wav")
        self.music_cvaIntro = 'music_cvaIntro'
        self.game.sound.register_sound(self.music_cvaIntro, self.music_path + "bangarang-intro.wav")
        self.music_cvaLoop = 'music_cvaLoop'
        self.game.sound.register_music(self.music_cvaLoop, self.music_path + "bangarang-loop.wav")
        self.sfx_cvaLoop = 'sfx_cvaLoop'
        self.game.sound.register_sound(self.sfx_cvaLoop, self.music_path + "bangarang-loop.wav")

        self.music_lastCallIntro = 'music_lastCallIntro'
        self.game.sound.register_sound(self.music_lastCallIntro, self.music_path + "last_call_lead_in.wav")
        self.music_lastCall = 'music_lastCall'
        self.game.sound.register_music(self.music_lastCall, self.music_path + "last_call_loop.wav")
        self.music_tensePiano1 = 'music_tensePiano1'
        self.game.sound.register_music(self.music_tensePiano1, self.music_path + "098-tense-piano-1.wav")
        self.music_tensePiano2 = 'music_tensePiano2'
        self.game.sound.register_music(self.music_tensePiano2, self.music_path + "096-tense-piano-2.wav")
        #self.music_tensePiano3 = 'music_tensePiano3'
        #self.game.sound.register_music(self.music_tensePiano3, self.music_path + "095-tense-piano-3.wav")

        self.music_mmOpeningLoop = 'music_mmOpeningLoop'
        self.game.sound.register_music(self.music_mmOpeningLoop, self.music_path + "opening_loop.wav")
        self.music_mmMainLoopOne = 'music_mmMainLoopOne'
        self.game.sound.register_music(self.music_mmMainLoopOne, self.music_path + "main_loop.wav")
        self.music_mmMainLoopTwo = 'music_mmMainLoopTwo'
        self.game.sound.register_music(self.music_mmMainLoopTwo, self.music_path + "main_loop_2.wav")
        self.music_mmClosing = 'music_mmClosing'
        self.game.sound.register_music(self.music_mmClosing, self.music_path + "Closing_Riff.wav")

        self.music_cousinIt = 'music_cousinIt'
        self.game.sound.register_music(self.music_cousinIt, self.music_path + "taf-cousin-it-music.wav")

        self.music_dracAttack = 'music_dracAttack'
        self.game.sound.register_music(self.music_dracAttack, self.music_path + "mb_drac_song.wav")

        self.music_trolls = 'music_trolls'
        self.game.sound.register_music(self.music_trolls, self.music_path + "mm_trolls_music.wav")

        self.music_tribute = 'music_tribute'
        self.game.sound.register_music(self.music_tribute, self.music_path + "tribute-intro.wav")
        self.music_mb = 'music_mb'
        self.game.sound.register_music(self.music_mb, self.music_path + "mb_theme.wav")
        self.music_mm = 'music_mm'
        self.game.sound.register_music(self.music_mm, self.music_path + "mm_theme.wav")
        self.music_taf = 'music_taf'
        self.game.sound.register_music(self.music_taf, self.music_path + "taf_theme.wav")

        # lampshows
        lampshows = list()

        self.lamp_giTest = 'gi-test'; lampshows.append(self.lamp_giTest)
        self.lamp_colors = 'colors'; lampshows.append(self.lamp_colors)
        self.lamp_topToBottom = "top-to-bottom"; lampshows.append(self.lamp_topToBottom)
        self.lamp_bottomToTop = "bottom-to-top"; lampshows.append(self.lamp_bottomToTop)
        self.lamp_rightToLeft = "right-to-left"; lampshows.append(self.lamp_rightToLeft)
        self.lamp_leftToRight = "left-to-right"; lampshows.append(self.lamp_leftToRight)
        self.lamp_starShots = "star-shots"; lampshows.append(self.lamp_starShots)
        self.lamp_sparkle = "sparkle"; lampshows.append(self.lamp_sparkle)
        self.lamp_pollyPeril = "polly-peril"; lampshows.append(self.lamp_pollyPeril)
        self.lamp_highNoonFlash = "high-noon-flash"; lampshows.append(self.lamp_highNoonFlash)
        self.lamp_fanRight = "fan-pan-right"; lampshows.append(self.lamp_fanRight)
        self.lamp_fanLeft = "fan-pan-left"; lampshows.append(self.lamp_fanLeft)
        self.lamp_slowSparkle = "slow_sparkle"; lampshows.append(self.lamp_slowSparkle)
        self.lamp_slowSparkle2 = "slow_sparkle_attract"; lampshows.append(self.lamp_slowSparkle2)
        self.lamp_gmStart = "gm_start"; lampshows.append(self.lamp_gmStart)
        self.lamp_flashers = "flasher-show"; lampshows.append(self.lamp_flashers)
        self.lamp_target0 = "target0"; lampshows.append(self.lamp_target0)
        self.lamp_target1 = "target1"; lampshows.append(self.lamp_target1)
        self.lamp_target2 = "target2"; lampshows.append(self.lamp_target2)
        self.lamp_target3 = "target3"; lampshows.append(self.lamp_target3)

        for lampshow in lampshows:
            self.game.lampctrl.register_show(lampshow,self.lampshows_path + lampshow + ".lampshow")

        self.lamp_cva = "cva"
        self.game.GI_lampctrl.register_show("cva",self.lampshows_path + "cva.lampshow")
        self.lamp_flashers = "flasher-show"
        self.game.GI_lampctrl.register_show("flasher-show",self.lampshows_path + "flasher-show.lampshow")

        # DMD pre-loading
        self.dmd_blank = dmd.Animation().load(self.dmd_path +'blank.dmd')
        self.dmd_ballyBanner = dmd.Animation().load(self.dmd_path +'bally-banner.dmd')
        self.dmd_geckoBorderLeft = dmd.Animation().load(self.dmd_path +'gecko-border.dmd')
        self.dmd_geckoBorderRight = dmd.Animation().load(self.dmd_path +'right-gecko-border.dmd')
        self.dmd_procBanner = dmd.Animation().load(self.dmd_path +'splash.dmd')
        if color_desktop:
            self.dmd_cccBanner = dmd.Animation().load(self.dmd_path +'ccc-banner-color.dmd')
            self.dmd_ccBanner = dmd.Animation().load(self.dmd_path+'cactus-canyon-banner-color.dmd')
        else:
            self.dmd_cccBanner = dmd.Animation().load(self.dmd_path +'ccc-banner.dmd')
            self.dmd_ccBanner = dmd.Animation().load(self.dmd_path+'cactus-canyon-banner.dmd')

        self.dmd_quickdrawStill = dmd.Animation().load(self.dmd_path+'quick-draw-still.dmd')

        self.dmd_mayorFeet = dmd.Animation().load(self.dmd_path +'mayor-feet.dmd')
        self.dmd_mayorPan = dmd.Animation().load(self.dmd_path +'mayor-pan.dmd')
        self.dmd_bountyCollected = dmd.Animation().load(self.dmd_path +'bounty-collected.dmd')
        self.dmd_moneybagBorder = dmd.Animation().load(self.dmd_path +'moneybag-border.dmd')
        self.dmd_moneybagBorderRight = dmd.Animation().load(self.dmd_path+'moneybag-right.dmd')
        self.dmd_starsBorder = dmd.Animation().load(self.dmd_path +'stars-border.dmd')
        self.dmd_tracksBorder = dmd.Animation().load(self.dmd_path +'tracks-border.dmd')
        self.dmd_gunsBorder = dmd.Animation().load(self.dmd_path +'guns-border.dmd')
        self.dmd_woodcutBorder = dmd.Animation().load(self.dmd_path +'woodcut-border.dmd')
        self.dmd_cactusBorder = dmd.Animation().load(self.dmd_path +'cactus-border.dmd')
        self.dmd_singleCactusBorder = dmd.Animation().load(self.dmd_path + 'single-cactus-border.dmd')
        self.dmd_weaveBorder = dmd.Animation().load(self.dmd_path +'weave-border.dmd')
        self.dmd_skullsBorder = dmd.Animation().load(self.dmd_path+'skulls-border.dmd')
        self.dmd_singleCowboyBorder = dmd.Animation().load(self.dmd_path +'single-cowboy-border.dmd')
        self.dmd_singleCowboyBorderRight = dmd.Animation().load(self.dmd_path+'cowboy-border-right.dmd')
        self.dmd_singleCowboySidewaysBorder = dmd.Animation().load(self.dmd_path+'single-cowboy-sideways-border.dmd')
        self.dmd_mineEntranceBorder = dmd.Animation().load(self.dmd_path +'mine-entrance-border.dmd')
        self.dmd_simpleBorder = dmd.Animation().load(self.dmd_path + 'simple_border.dmd')
        self.dmd_singlePixelBorder = dmd.Animation().load(self.dmd_path + 'single_pixel_border.dmd')
        self.dmd_ropeBorder = dmd.Animation().load(self.dmd_path + 'rope-border.dmd')
        self.dmd_skyline = dmd.Animation().load(self.dmd_path+'skyline.dmd')
        self.dmd_bartender = dmd.Animation().load(self.dmd_path + 'bartender.dmd')
        self.dmd_escaped = dmd.Animation().load(self.dmd_path +'escaped.dmd')
        self.dmd_stringBorder = dmd.Animation().load(self.dmd_path+'string-border.dmd')

        self.dmd_tombstone = dmd.Animation().load(self.dmd_path+'tombstone.dmd')
        self.dmd_beerMug = dmd.Animation().load(self.dmd_path +'beer-mug-1.dmd')

        self.dmd_cashWipe = dmd.Animation().load(self.dmd_path +'cash-wipe.dmd')
        self.dmd_burstWipe = dmd.Animation().load(self.dmd_path +'burst-wipe.dmd')
        self.dmd_burstWipe2 = dmd.Animation().load(self.dmd_path +'burst-wipe-2.dmd')
        self.dmd_horseWipeRight = dmd.Animation().load(self.dmd_path+'horse-wipe-right.dmd')

        self.dmd_blankRiver = dmd.Animation().load(self.dmd_path +'blank-river.dmd')
        self.dmd_blankRiverLoop = dmd.Animation().load(self.dmd_path + 'blank-river-loop.dmd')
        self.dmd_rowboat = dmd.Animation().load(self.dmd_path +'rowboat.dmd')
        self.dmd_rowboatLoop = dmd.Animation().load(self.dmd_path + 'rowboat-cycle.dmd')
        self.dmd_horseLoop = dmd.Animation().load(self.dmd_path + 'horse-loop.dmd')
        self.dmd_riverChase = dmd.Animation().load(self.dmd_path +'river-chase.dmd')

        self.dmd_bankExplodes = dmd.Animation().load(self.dmd_path +'bank-explodes.dmd')
        self.dmd_bankSheriff = dmd.Animation().load(self.dmd_path +'bank-sherrif-arrives.dmd')
        self.dmd_bankDude = dmd.Animation().load(self.dmd_path + 'dude-shoots-bank.dmd')
        self.dmd_bankInterior = dmd.Animation().load(self.dmd_path + 'bank-interior.dmd')
        self.dmd_hatbTitle = dmd.Animation().load(self.dmd_path +'polly-peril-hatb.dmd')

        self.dmd_trainHeadOn = dmd.Animation().load(self.dmd_path+'train-head-on.dmd')
        self.dmd_cowOnTracks = dmd.Animation().load(self.dmd_path+'cow-on-tracks.dmd')
        self.dmd_ttttBanner = dmd.Animation().load(self.dmd_path+'polly-peril-tttt.dmd')
        self.dmd_pollyOnTracks = dmd.Animation().load(self.dmd_path +'train-polly-on-tracks.dmd')

        self.dmd_pollyMurder = dmd.Animation().load(self.dmd_path + 'train-murder.dmd')
        self.dmd_poutySheriff = dmd.Animation().load(self.dmd_path + 'pouty-sheriff.dmd')

        self.dmd_dudeShotFullBody = dmd.Animation().load(self.dmd_path+'dude-gets-shot-full-body.dmd')
        self.dmd_dudeShotShouldersUp = dmd.Animation().load(self.dmd_path+'dude-gets-shot-shoulders-up.dmd')
        self.dmd_dudeShoots = dmd.Animation().load(self.dmd_path+'dude-shoots.dmd')

        self.dmd_trainBoarding = dmd.Animation().load(self.dmd_path +'train-boarding.dmd')
        self.dmd_trainRunning = dmd.Animation().load(self.dmd_path +'train-running-on-top.dmd')
        self.dmd_trainBrakes = dmd.Animation().load(self.dmd_path +'train-brake-pull.dmd')

        self.dmd_pollyIntro = dmd.Animation().load(self.dmd_path +'polly-peril.dmd')
        self.dmd_pollyVictory = dmd.Animation().load(self.dmd_path +'bank-victory-animation.dmd')
        self.dmd_ourHero = dmd.Animation().load(self.dmd_path+'our-hero.dmd')
        self.dmd_rotrTitle = dmd.Animation().load(self.dmd_path +'polly-peril-rotr.dmd')

        self.dmd_horseRunLeft = dmd.Animation().load(self.dmd_path + 'horse-run-left.dmd')
        self.dmd_horseRunRight = dmd.Animation().load(self.dmd_path + 'horse-run-right.dmd')
        self.dmd_horseDrag = dmd.Animation().load(self.dmd_path + 'horse-drag.dmd')
        self.dmd_horseChase = dmd.Animation().load(self.dmd_path + 'horse-chase.dmd')

        self.dmd_shotBottles = dmd.Animation().load(self.dmd_path +'shot-bottles-animation.dmd')
        self.dmd_shotCandles = dmd.Animation().load(self.dmd_path +'shot-candles-animation.dmd')
        self.dmd_shotCard = dmd.Animation().load(self.dmd_path +'shot-card-animation.dmd')
        self.dmd_smokingCard = dmd.Animation().load(self.dmd_path +'smoking-card-loop.dmd')

        self.dmd_tumbleweedBanner = dmd.Animation().load(self.dmd_path +'tumbleweed-banner.dmd')
        self.dmd_tumbleweedRight = dmd.Animation().load(self.dmd_path +'tumbleweed-right.dmd')
        self.dmd_tumbleweedLeft = dmd.Animation().load(self.dmd_path +'tumbleweed.dmd')
        self.dmd_tumbleweedAttract = dmd.Animation().load(self.dmd_path +'tumbleweed-attract.dmd')

        self.dmd_superBlink = dmd.Animation().load(self.dmd_path +'super-blink.dmd')
        self.dmd_superSkillShot = dmd.Animation().load(self.dmd_path +'super-skill-shot.dmd')

        self.dmd_quickdrawStart = dmd.Animation().load(self.dmd_path +'quickdraw-start.dmd')
        self.dmd_quickdrawHit = dmd.Animation().load(self.dmd_path +'quickdraw-hit.dmd')

        #self.dmd_gunfightTop = dmd.Animation().load(self.dmd_path+'gunfight-top.dmd')
        self.dmd_gunfightMask = dmd.Animation().load(self.dmd_path +'gunfight-mask.dmd')
        self.dmd_gunfightPan = dmd.Animation().load(self.dmd_path+'gunfight-pan.dmd')
        self.dmd_gunfightEyes = dmd.Animation().load(self.dmd_path+'gunfight-eyes.dmd')
        self.dmd_gunfightHands = dmd.Animation().load(self.dmd_path+'gunfight-hands.dmd')
        self.dmd_gunfightBoots = dmd.Animation().load(self.dmd_path+'gunfight-boots.dmd')

        self.dmd_ambush = dmd.Animation().load(self.dmd_path +'ambush.dmd')
        self.dmd_showdown = dmd.Animation().load(self.dmd_path +'showdown.dmd')
        self.dmd_cloudLightning = dmd.Animation().load(self.dmd_path +'cloud-lightning.dmd')
        self.dmd_townPan = dmd.Animation().load(self.dmd_path +'town-pan.dmd')

        self.dmd_stampede = dmd.Animation().load(self.dmd_path + 'stampede-animation.dmd')
        self.dmd_cowsParading = dmd.Animation().load(self.dmd_path +'cows-parading.dmd')
        self.dmd_stampedeJackpot = dmd.Animation().load(self.dmd_path +'stampede-jackpot.dmd')
        self.dmd_cowsLeft = dmd.Animation().load(self.dmd_path + 'cows-left.dmd')
        self.dmd_cowsRight = dmd.Animation().load(self.dmd_path + 'cows-right.dmd')
        self.dmd_stampedeBannerLeft = dmd.Animation().load(self.dmd_path +'stampede-banner-left.dmd')
        self.dmd_stampedeBannerRight = dmd.Animation().load(self.dmd_path + 'stampede-banner-right.dmd')

        self.dmd_shootAgain = dmd.Animation().load(self.dmd_path+'shoot-again.dmd')
        self.dmd_ball = dmd.Animation().load(self.dmd_path +'ball.dmd')
        self.dmd_extraBall = dmd.Animation().load(self.dmd_path +'extra-ball.dmd')
        self.dmd_bonusCactus = dmd.Animation().load(self.dmd_path+'bonus-cactus-mash.dmd')

        self.dmd_lockOne = dmd.Animation().load(self.dmd_path +'ball-one-locked.dmd')
        self.dmd_lockTwo = dmd.Animation().load(self.dmd_path +'ball-two-locked.dmd')
        self.dmd_multiballStart = dmd.Animation().load(self.dmd_path+'multiball-start.dmd')
        self.dmd_multiballBannerInverse = dmd.Animation().load(self.dmd_path +'multiball-banner-inverse.dmd')
        self.dmd_multiballBanner = dmd.Animation().load(self.dmd_path +'multiball-banner.dmd')
        self.dmd_multiballFrame = dmd.Animation().load(self.dmd_path +'multiball-frame.dmd')
        self.dmd_mineCarCrash = dmd.Animation().load(self.dmd_path +'mine-car-crash.dmd')
        self.dmd_goldmineJackpot = dmd.Animation().load(self.dmd_path +'jackpot.dmd')

        self.dmd_bamBanner = dmd.Animation().load(self.dmd_path + 'bam-banner.dmd')
        self.dmd_biffBanner = dmd.Animation().load(self.dmd_path + 'biff-banner.dmd')
        self.dmd_ouchBanner = dmd.Animation().load(self.dmd_path + 'ouch-banner.dmd')
        self.dmd_powBanner = dmd.Animation().load(self.dmd_path + 'pow-banner.dmd')
        self.dmd_whamBanner = dmd.Animation().load(self.dmd_path + 'wham-banner.dmd')
        self.dmd_zoinkBanner = dmd.Animation().load(self.dmd_path + 'zoink-banner.dmd')

        self.dmd_bigPosterA = dmd.Animation().load(self.dmd_path +'wanted-BIG-A.dmd')
        self.dmd_bandeleroPosterA = dmd.Animation().load(self.dmd_path + 'wanted-BANDELERO-A.dmd')
        self.dmd_bubbaPosterA = dmd.Animation().load(self.dmd_path + 'wanted-BUBBA-A.dmd')
        self.dmd_bigPosterB = dmd.Animation().load(self.dmd_path +'wanted-BIG-B.dmd')
        self.dmd_bandeleroPosterB = dmd.Animation().load(self.dmd_path + 'wanted-BANDELERO-B.dmd')
        self.dmd_bubbaPosterB = dmd.Animation().load(self.dmd_path + 'wanted-BUBBA-B.dmd')

        self.dmd_trainOnTracks = dmd.Animation().load(self.dmd_path+'train-on-tracks.dmd')
        self.dmd_trainMoveRight = dmd.Animation().load(self.dmd_path+'train-on-tracks-move-right.dmd')
        self.dmd_trainMoveLeft = dmd.Animation().load(self.dmd_path+'train-on-tracks-move-left.dmd')
        self.dmd_emptyTrack = dmd.Animation().load(self.dmd_path+'empty-track.dmd')

        self.dmd_dmbIdle = dmd.Animation().load(self.dmd_path+'dmb-idle.dmd')
        self.dmd_reverse = dmd.Animation().load(self.dmd_path+'reverse.dmd')
        self.dmd_pourMask = dmd.Animation().load(self.dmd_path+'pour-mask.dmd')
        self.dmd_beerMug1 = dmd.Animation().load(self.dmd_path+'beer-mug-1.dmd')
        self.dmd_drunkMultiball = dmd.Animation().load(self.dmd_path+'drunk-multiball.dmd')
        self.dmd_flippers1 = dmd.Animation().load(self.dmd_path+'flippers1.dmd')
        self.dmd_flippers2 = dmd.Animation().load(self.dmd_path+'flippers2.dmd')
        self.dmd_flippers3 = dmd.Animation().load(self.dmd_path+'flippers3.dmd')
        self.dmd_rightArrow1 = dmd.Animation().load(self.dmd_path+'right-arrow-1.dmd')
        self.dmd_rightArrow2 = dmd.Animation().load(self.dmd_path+'right-arrow-2.dmd')
        self.dmd_rightArrow3 = dmd.Animation().load(self.dmd_path+'right-arrow-3.dmd')
        self.dmd_leftArrow1 = dmd.Animation().load(self.dmd_path+'left-arrow-1.dmd')
        self.dmd_leftArrow2 = dmd.Animation().load(self.dmd_path+'left-arrow-2.dmd')
        self.dmd_leftArrow3 = dmd.Animation().load(self.dmd_path+'left-arrow-3.dmd')
        self.dmd_dmb = dmd.Animation().load(self.dmd_path+'dmb.dmd')
        self.dmd_dmbJackpotAdded = dmd.Animation().load(self.dmd_path+'jackpot-added.dmd')
        self.dmd_beerSlide = dmd.Animation().load(self.dmd_path+'beer-slide.dmd')
        self.dmd_dmbJackpot = dmd.Animation().load(self.dmd_path+'dmb-jackpot.dmd')
        
        self.dmd_match = dmd.Animation().load(self.dmd_path+'match.dmd')
        
        self.dmd_bionicCombo = dmd.Animation().load(self.dmd_path +'bionic-combo.dmd')
        self.dmd_bionicHit = dmd.Animation().load(self.dmd_path+'bionic-hit.dmd')
        self.dmd_bionicGunClose = dmd.Animation().load(self.dmd_path+'gun-close.dmd')
        self.dmd_bionicGunLoad = dmd.Animation().load(self.dmd_path+'gun-load.dmd')
        self.dmd_bionicGunUnload = dmd.Animation().load(self.dmd_path+'gun-unload.dmd')
        self.dmd_bionicGunOpen = dmd.Animation().load(self.dmd_path+'gun-open.dmd')
        self.dmd_bionicDeath = dmd.Animation().load(self.dmd_path+'bionic-death.dmd')
        self.dmd_bionicDeathTalking = dmd.Animation().load(self.dmd_path+'bionic-death-talking.dmd')
        self.dmd_bionicExplode = dmd.Animation().load(self.dmd_path+'bionic-explode.dmd')
        
        self.dmd_cvaStandingAlien0 = dmd.Animation().load(self.dmd_path+'cva_standing_alien0.dmd')
        self.dmd_cvaStandingAlien1 = dmd.Animation().load(self.dmd_path+'cva_standing_alien1.dmd')
        self.dmd_cvaStandingAlien2 = dmd.Animation().load(self.dmd_path+'cva_standing_alien2.dmd')
        self.dmd_cvaStandingAlien3 = dmd.Animation().load(self.dmd_path+'cva_standing_alien3.dmd')
        self.dmd_cvaSmallShip = dmd.Animation().load(self.dmd_path+'cva_small_ship.dmd')
        self.dmd_cvaLargeShip = dmd.Animation().load(self.dmd_path+'cva_large_ship.dmd')
        self.dmd_cvaLargeShipExplodes = dmd.Animation().load(self.dmd_path+'cva_large_ship_explodes.dmd')
        self.dmd_cvaShipBehindStatic = dmd.Animation().load(self.dmd_path+'cva_ship_behind_static.dmd')
        self.dmd_cvaStatic = dmd.Animation().load(self.dmd_path+'cva_static.dmd')
        self.dmd_cvaTeleport = dmd.Animation().load(self.dmd_path+'cva_teleport.dmd')
        self.dmd_cvaShot = dmd.Animation().load(self.dmd_path+'cva_shot.dmd')
        self.dmd_cvaIntro = dmd.Animation().load(self.dmd_path+'cva_intro.dmd')
        self.dmd_cvaBlastWipe = dmd.Animation().load(self.dmd_path+'cva_blast_wipe.dmd')
        self.dmd_cvaDesert = dmd.Animation().load(self.dmd_path+'cva_desert_empty.dmd')
        self.dmd_cvaShipsBorder = dmd.Animation().load(self.dmd_path+'cva_ships_border.dmd')
        self.dmd_cvaAliensBorder = dmd.Animation().load(self.dmd_path+'cva_aliens_border.dmd')
        
        self.dmd_highNoonBackdrop = dmd.Animation().load(self.dmd_path+'high-noon-backdrop.dmd')
        self.dmd_bellTower = dmd.Animation().load(self.dmd_path+'bell-ring.dmd')
        self.dmd_highNoon = dmd.Animation().load(self.dmd_path+'high-noon.dmd')
        self.dmd_goodLuck = dmd.Animation().load(self.dmd_path+'good-luck.dmd')
        self.dmd_fireworks = dmd.Animation().load(self.dmd_path+'fireworks.dmd')

        self.dmd_marshallBorder = dmd.Animation().load(self.dmd_path+'marshall-border.dmd')
        self.dmd_marshallHighScoreFrame = dmd.Animation().load(self.dmd_path+'marshall-highscore-frame.dmd')

        self.dmd_boss = dmd.Animation().load(self.dmd_path+'boss.dmd')
        self.dmd_bossHit = dmd.Animation().load(self.dmd_path+'boss-hit.dmd')

        self.dmd_lastCall = dmd.Animation().load(self.dmd_path+'last_call.dmd')
        self.dmd_beerFill = dmd.Animation().load(self.dmd_path+'beer-fill.dmd')

        self.dmd_cows = dmd.Animation().load(self.dmd_path+'crazy_cows.dmd')
        self.dmd_moother = dmd.Animation().load(self.dmd_path+'moother.dmd')

        self.dmd_1pBurnCycle = dmd.Animation().load(self.dmd_path+'1p_burn_cycle.dmd')

        self.dmd_mmJacob = dmd.Animation().load(self.dmd_path+'mm_jacob.dmd')
        self.dmd_mmZap = dmd.Animation().load(self.dmd_path+'mm_zap.dmd')
        self.dmd_mmPowie = dmd.Animation().load(self.dmd_path+'mm_powie.dmd')
        self.dmd_mmDOHO = dmd.Animation().load(self.dmd_path+'mm_doho.dmd')
        self.dmd_mmCrash = dmd.Animation().load(self.dmd_path+'mm_crash.dmd')
        self.dmd_mmBoom = dmd.Animation().load(self.dmd_path+'mm_boom.dmd')
        self.dmd_mmBang = dmd.Animation().load(self.dmd_path+'mm_bang.dmd')
        self.dmd_moonIntro = dmd.Animation().load(self.dmd_path+'moon-intro.dmd')

        self.dmd_ballSaved = dmd.Animation().load(self.dmd_path+'ball_saved.dmd')

        self.dmd_switchMatrix = dmd.Animation().load(self.dmd_path+'matrix_backdrop.dmd')
        self.dmd_testBackdrop = dmd.Animation().load(self.dmd_path+'test_backdrop.dmd')

        # Tribute bits
        if color_desktop:
            self.dmd_mbLogo = dmd.Animation().load(self.dmd_path+'mb-logo-color.dmd')
        else:
            self.dmd_mbLogo = dmd.Animation().load(self.dmd_path+'mb-logo.dmd')
        self.dmd_mbDracIntro1 = dmd.Animation().load(self.dmd_path+'mb-drac-intro-part1.dmd')
        self.dmd_mbDracIntro2 = dmd.Animation().load(self.dmd_path+'mb-drac-intro-part2.dmd')
        self.dmd_mbDracIdle = dmd.Animation().load(self.dmd_path+'mb-drac-idle.dmd')
        self.dmd_mbDracSmack = dmd.Animation().load(self.dmd_path+'mb-drac-smack.dmd')
        self.dmd_mbStakeBorder = dmd.Animation().load(self.dmd_path+'mb-stake-border.dmd')

        if color_desktop:
            self.dmd_mmLogo = dmd.Animation().load(self.dmd_path+'mm-logo-color.dmd')
        else:
            self.dmd_mmLogo = dmd.Animation().load(self.dmd_path+'mm-logo.dmd')
        self.dmd_mmTrollsIntro = dmd.Animation().load(self.dmd_path+'mm_trolls_intro_anim.dmd')
        self.dmd_mmTrollDeadLeft = dmd.Animation().load(self.dmd_path+'mm_left_troll_dead.dmd')
        self.dmd_mmTrollHitLeft = dmd.Animation().load(self.dmd_path+'mm_left_troll_hit.dmd')
        self.dmd_mmTrollIdleLeft = dmd.Animation().load(self.dmd_path+'mm_left_troll_idle.dmd')
        self.dmd_mmTrollDeadRight = dmd.Animation().load(self.dmd_path+'mm_right_troll_dead.dmd')
        self.dmd_mmTrollHitRight = dmd.Animation().load(self.dmd_path+'mm_right_troll_hit.dmd')
        self.dmd_mmTrollIdleRight = dmd.Animation().load(self.dmd_path+'mm_right_troll_idle.dmd')
        self.dmd_mmTrollFinalFrame = dmd.Animation().load(self.dmd_path+'mm_trolls_final_border.dmd')

        self.dmd_tafLogo = dmd.Animation().load(self.dmd_path+'taf-logo.dmd')
        self.dmd_tafItIntro = dmd.Animation().load(self.dmd_path+'taf-it-intro.dmd')
        self.dmd_tafItIdle = dmd.Animation().load(self.dmd_path+'taf-it-idle.dmd')
        self.dmd_tafItMiss1 = dmd.Animation().load(self.dmd_path+'taf-it-miss-1.dmd')
        self.dmd_tafItMiss2 = dmd.Animation().load(self.dmd_path+'taf-it-miss-2.dmd')
        self.dmd_tafItHit = dmd.Animation().load(self.dmd_path+'taf-it-hit.dmd')

        # Shared Paths
        self.shared_dmd_path = curr_file_path + "/shared/dmd/"

        # Shared Fonts
        self.font_tiny7 = dmd.Font(self.shared_dmd_path + "04B-03-7px.dmd")
        self.font_jazz18 = dmd.Font(self.shared_dmd_path + "Jazz18-18px.dmd")
        self.font_18x12 = dmd.Font(self.shared_dmd_path + "Font18x12.dmd")
        self.font_18x11 = dmd.Font(self.shared_dmd_path + "Font18x11.dmd")
        self.font_14x10 = ep.ColorFont(self.shared_dmd_path + "Font14x10.dmd")
        self.font_14x10.make_colors([ep.YELLOW])
        self.font_14x9 = ep.ColorFont(self.shared_dmd_path + "Font14x9.dmd")
        self.font_14x9.make_colors([ep.YELLOW])
        self.font_14x8 = ep.ColorFont(self.shared_dmd_path + "Font14x8.dmd")
        self.font_14x8.make_colors([ep.YELLOW])
        self.font_09Bx7 = ep.ColorFont(self.shared_dmd_path + "Font09Bx7.dmd")
        self.font_09Bx7.make_colors([ep.GREEN])
        self.font_09x7 = ep.ColorFont(self.shared_dmd_path + "Font09x7.dmd")
        self.font_09x7.make_colors([ep.DARK_BROWN])
        self.font_09x6 = ep.ColorFont(self.shared_dmd_path + "Font09x6.dmd")
        self.font_09x6.make_colors([ep.DARK_BROWN])
        self.font_09x5 = ep.ColorFont(self.shared_dmd_path + "Font09x5.dmd")
        self.font_09x5.make_colors([ep.DARK_BROWN])
        self.font_07x4 = dmd.Font(self.shared_dmd_path + "Font07x4.dmd")
        self.font_07x5 = ep.ColorFont(self.shared_dmd_path + "Font07x5.dmd")
        self.font_07x5.make_colors([ep.CYAN,ep.YELLOW,ep.ORANGE])

        
