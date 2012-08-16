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
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##

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
        self.font_6px_az_inverse = dmd.Font(self.dmd_path + "Font_Custom_6px.dmd")
        self.font_6px_az_inverse.composite_op = "blacksrc"

        self.font_7px_alt_az = dmd.Font(self.dmd_path + "Font_1_CactusCanyon.dmd")
        self.font_7px_az = dmd.Font(self.dmd_path + "Font_2_CactusCanyon.dmd")
        self.font_7px_score = dmd.Font(self.dmd_path + "Font_5_CactusCanyon.dmd")
        self.font_7px_extra_thin_score = dmd.Font(self.dmd_path + "Font_10_CactusCanyon.dmd")
        self.font_7px_thin_score = dmd.Font(self.dmd_path + "Font_4_CactusCanyon.dmd")
        self.font_7px_wide_score = dmd.Font(self.dmd_path + "Font_6_CactusCanyon.dmd")
        self.font_7px_bold_az = dmd.Font(self.dmd_path + "Font_14_CactusCanyon.dmd")

        self.font_9px_az = dmd.Font(self.dmd_path + "Font_15_CactusCanyon.dmd")
        self.font_9px_az_mid = dmd.Font(self.dmd_path + "Font_15_CactusCanyon_2.dmd")
        self.font_9px_az_dim = dmd.Font(self.dmd_path + "Font_15_CactusCanyon_1.dmd")

        self.font_10px_AZ = dmd.Font(self.dmd_path + "Font_Custom_10px_AZ.dmd")
        self.font_12px_az = dmd.Font(self.dmd_path + "Font_16_CactusCanyon.dmd")
        self.font_12px_az_dim = dmd.Font(self.dmd_path + "Font_16_CactusCanyon_dim.dmd")

        self.font_12px_az_outline = dmd.Font(self.dmd_path + "Font_16_mask_CactusCanyon.dmd")
        self.font_12px_az_outline.tracking = -1
        self.font_12px_az_outline.composite_op = "blacksrc"

        self.font_13px_score = dmd.Font(self.dmd_path + "Font_8_CactusCanyon.dmd")
        self.font_13px_extra_thin_score = dmd.Font(self.dmd_path + "Font_11_CactusCanyon.dmd")
        self.font_13px_thin_score = dmd.Font(self.dmd_path + "Font_7_CactusCanyon.dmd")
        self.font_13px_wide_score = dmd.Font(self.dmd_path + "Font_9_CactusCanyon.dmd")

        self.font_15px_az = dmd.Font(self.dmd_path + "Font_17_CactusCanyon.dmd")

        self.font_15px_bionic = dmd.Font(self.dmd_path + "Font_Custom_15px.dmd")

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
        self.sfx_bonusX = 'sfx_bonusX'
        self.game.sound.register_sound(self.sfx_bonusX, self.sfx_path + "036-sfx-bonus-x.wav")
        self.sfx_flourish6 = 'sfx_flourish6'
        self.game.sound.register_sound(self.sfx_flourish6, self.sfx_path + "032-flourish-6.wav")
        self.sfx_flourish7 = 'sfx_flourish7'
        self.game.sound.register_sound(self.sfx_flourish7, self.sfx_path + "034-flourish-7-Horns.wav")
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
        self.sfx_ropeWoosh = 'sfx_ropeWoosh'
        self.game.sound.register_sound(self.sfx_ropeWoosh, self.sfx_path + "00-rope-woosh.wav")
        self.sfx_ropeCreak = 'sfx_ropeCreak'
        self.game.sound.register_sound(self.sfx_ropeCreak, self.sfx_path + "00-rope-creak.wav")

        self.sfx_ricochetSet = 'sfx_ricochetSet'
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "103-sfx-ricochet-1.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "109-sfx-ricochet-2.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "111-sfx-ricochet-3.wav")
        self.game.sound.register_sound(self.sfx_ricochetSet, self.sfx_path + "319-sfx-ricochet-4.wav")

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

        self.sfx_cvaYell = 'sfx_cvaYell'
        self.game.sound.register_sound(self.sfx_cvaYell, self.sfx_path + "bangarang-yell.wav")
        self.sfx_cvaExplosion = 'sfx_cvaExplosion'
        self.game.sound.register_sound(self.sfx_cvaExplosion, self.sfx_path + "208-afm-explosion.wav")
        self.sfx_cvaTeleport = 'sfx_cvaTeleport'
        self.game.sound.register_sound(self.sfx_cvaTeleport, self.sfx_path + "294-afm-teleport.wav")
        self.sfx_cvaWoosh = 'sfx_cvaWoosh'
        self.game.sound.register_sound(self.sfx_cvaWoosh, self.sfx_path + "246-afm-woosh.wav")
        self.sfx_cvaGroan = 'sfx_cvaGroan'
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-1.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-2.wav")
        self.game.sound.register_sound(self.sfx_cvaGroan, self.sfx_path + "cva-groan-3.wav")
        self.sfx_cvaBumper = 'sfx_cvaBumper'
        self.game.sound.register_sound(self.sfx_cvaBumper, self.sfx_path + "bangarang-bwoip-noise.wav")

        # Quotes
        # this bunches the welcome strings together for play_voice()
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
        self.quote_mayhemBank = 'quote_mayhemBank'
        self.game.sound.register_sound(self.quote_mayhemBank, self.quotes_path + "1307-undertaker-oh-good-mayhem-at-the-bank.wav")
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
        self.quote_gunWin = 'quote_gunWin'
        self.game.sound.register_sound(self.quote_gunWin, self.quotes_path + "1117-mayor-say-thats-a-pretty-good-eye-there.wav")
        self.game.sound.register_sound(self.quote_gunWin, self.quotes_path + "1170-mayor-quite-a-knack-with-those-six-shooters-friend.wav")
        self.quote_gunFail = 'quote_gunFail'
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1198-mayor-maybe-you-better-check-the-sights-on-that-weapon.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1199-mayor-are-you-sure-that-thing-is-loaded.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1505-leader-bart-better-luck-next-time.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1564-leader-bart-well-im-still-standin.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1563-leader-bart-aw-you-missed.wav")
        self.quote_superFail = 'quote_superFail'
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1505-leader-bart-better-luck-next-time.wav")
        self.game.sound.register_sound(self.quote_superFail, self.quotes_path + "1563-leader-bart-aw-you-missed.wav")
        self.quote_beerMug = 'quote_beerMug'
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1408-drunk-hey-buddy-you-shot-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1409-drunk-stop-shootin-at-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1414-drunk-i-was-drinking-that-thank-you.wav")
        self.quote_extraBallLit = 'quote_extraBallLit'
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "2013-waitress-that-extra-ball-is-lit-honey.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1258-prospector-extra-ball-is-lit.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1020-mayor-the-extra-ball-is-lit.wav")
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

        self.quote_hurry = 'quote_hurry'
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1175-mayor-i-suggest-you-hurry-friend.wav")
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1173-mayor-time-for-one-more-shot.wav")
        self.game.sound.register_sound(self.quote_hurry, self.quotes_path + "1205-prospector-hurry-youre-runnin-outta-time.wav")

        self.quote_mobStart = 'quote_mobStart'
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1171-mayor-shoot-anything-that-pops-up.wav")
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1259-prospector-shoot-all-the-bad-guys.wav")
        self.game.sound.register_sound(self.quote_mobStart, self.quotes_path + "1152-mayor-ive-had-about-enough-of-those-bart-boys.wav")
        self.quote_mobTaunt = 'quote_mobTaunt'
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "2020-waitress-honey-just-shoot-anything.wav")
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "1165-mayor-aw-just-shoot-em.wav")
        self.game.sound.register_sound(self.quote_mobTaunt, self.quotes_path + "1525-leader-bart-git-that-law-man.wav")
        self.quote_mobEnd = 'quote_mobEnd'
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1303-prospector-look-at-that-bodycount.wav")
        self.game.sound.register_sound(self.quote_mobEnd, self.quotes_path + "1309-undertaker-a-respectable-bodycount-indeed.wav")


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
        self.quote_centerRampSS = 'quote_centerRampSS'
        self.game.sound.register_sound(self.quote_centerRampSS, self.quotes_path + "1167-mayor-head-up-the-center-ramp-sir.wav")
        self.quote_leaderLaugh = 'quote_leaderLaugh'
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.game.sound.register_sound(self.quote_leaderLaugh, self.quotes_path + "1581-leader-bart-laugh-3.wav")
        self.quote_nobodysHome = 'quote_nobodysHome'
        self.game.sound.register_sound(self.quote_nobodysHome, self.quotes_path + "1853-leader-bart-nobodys-home.wav")
        self.quote_catchGuy = 'quote_catchGuy'
        self.game.sound.register_sound(self.quote_catchGuy, self.quotes_path + "00-mayor-dont-let-em-get-away.wav")


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
        #self.music_tensePiano1 = 'music_tensePiano1'
        #self.game.sound.register_music(self.music_tensePiano1, self.music_path + "098-tense-piano-1.wav")
        #self.music_tensePiano2 = 'music_tensePiano2'
        #self.game.sound.register_music(self.music_tensePiano2, self.music_path + "096-tense-piano-2.wav")
        #self.music_tensePiano3 = 'music_tensePiano3'
        #self.game.sound.register_music(self.music_tensePiano3, self.music_path + "095-tense-piano-3.wav")

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

        for lampshow in lampshows:
            self.game.lampctrl.register_show(lampshow,self.lampshows_path + lampshow + ".lampshow")

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

        # Shared Sounds
        self.game.sound.register_sound('service_enter', self.shared_sound_path + "menu_in.wav")
        self.game.sound.register_sound('service_exit', self.shared_sound_path + "menu_out.wav")
        self.game.sound.register_sound('service_next', self.shared_sound_path + "next_item.wav")
        self.game.sound.register_sound('service_previous', self.shared_sound_path + "previous_item.wav")
        self.game.sound.register_sound('service_switch_edge', self.shared_sound_path + "switch_edge.wav")
        self.game.sound.register_sound('service_save', self.shared_sound_path + "save.wav")
        self.game.sound.register_sound('service_cancel', self.shared_sound_path + "cancel.wav")
