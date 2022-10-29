import os

# pyyaml for loading a configuration file
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# TODO: Make this be set by an argument instead
CONFIG_FILE_PATH = "config.yaml"

class AllVars:
    def __init__(self):
        self.set_start_vars()

    def set_start_vars(self):
        # Open the config file
        try:
            with open(CONFIG_FILE_PATH) as config_file:
                try:
                    config_data = yaml.load(config_file, Loader=Loader)
                    # All relevant vars are stored in a dictionary
                    config_vars = config_data['vars']

                    # === Important Values ===
                    # Set depending on hardware. True = less powerful hardware.
                    self.artificialPauses   = config_vars['artificialPauses']
                    # Set automatically on new game. For testing (loading a save file) set for your environment.
                    self.csrValue           = config_vars['csrValue']
                    # Set based on if you're doing any% (False) or Nemesis% (True)
                    self.nemesisValue       = config_vars['nemesisValue']
                    # After game is finished, start again on next seed.
                    self.forceLoop          = config_vars['forceLoop']
                    # Loop on the same seed immediately after Blitzball.
                    self.blitzLoop          = config_vars['blitzLoop']
                    # True = reset after blitz loss
                    self.blitzLossForceReset = config_vars['blitzLossForceReset']
                    # If you are using Rossy's patch, set to True. Otherwise set to False
                    self.setSeed            = config_vars['setSeed']
                    # True == Tidus OD on Evrae instead of Seymour. New strat.
                    self.kilikaSkip         = config_vars['kilikaSkip']
                    # Before YuYevon, True is slower but more swag.
                    self.perfectAeonKills   = config_vars['perfectAeonKills']
                    # Try Djose skip? (not likely to succeed)
                    self.attemptDjose       = config_vars['attemptDjose']
                    # use the original Soundtrack instead of arranged
                    self.legacySoundtrack   = config_vars['legacySoundtrack']
                    self.doNotSkipCutscenes = config_vars['doNotSkipCutscenes']

                    # ----Accessibility for blind
                    self.skip_cutscene_flag = config_vars['skip_cutscene_flag']
                    self.skip_diag_flag     = config_vars['skip_diag_flag']
                    self.play_TTS_flag      = config_vars['play_TTS_flag']
                    self.rails_trials       = config_vars['rails_trials']
                    self.rails_egg_hunt     = config_vars['rails_egg_hunt']

                    # ----Blitzball
                    self.blitzWinValue      = config_vars['blitzWinValue']  # No default value required
                    self.blitzOvertime      = config_vars['blitzOvertime']  # Set to False, no need to change ever.
                    self.blitzFirstShotVal  = config_vars['blitzFirstShotVal']
                    self.oblitzAttackVal    = config_vars['oblitzAttackVal']  # Used for RNG manip tracking

                    # ----Sphere grid
                    self.fullKilikMenu      = config_vars['fullKilikMenu']  # Default to False
                    self.earlyTidusGridVal  = config_vars['earlyTidusGridVal']  # Default False
                    self.earlyHasteVal      = config_vars['earlyHasteVal']  # Default -1
                    self.wakkaLateMenuVal   = config_vars['wakkaLateMenuVal']  # Default False
                    self.endGameVersionVal  = config_vars['endGameVersionVal']  # Default 0

                    # ----Equipment
                    self.zombieWeaponVal    = config_vars['zombieWeaponVal']  # Default 255
                    self.lStrikeCount       = config_vars['lStrikeCount']  # Default 0

                    # ----RNG Manip
                    self.yellows            = config_vars['yellows']  # ?
                    self.confirmedSeedNum   = config_vars['confirmedSeedNum']  # ?
                    self.skipZanLuck        = config_vars['skipZanLuck']  # ?

                    # ----Other
                    self.newGame            = config_vars['newGame']  # ?
                    self.selfDestruct       = config_vars['selfDestruct']  # Default False
                    self.YTKFarm            = config_vars['YTKFarm']  # Default to 0
                    self.rescueCount        = config_vars['rescueCount']  # Default to 0
                    self.fluxOverkillVar    = config_vars['fluxOverkillVar']  # Default to False
                    self.tryNEVal           = config_vars['tryNEVal']  # Based on
                    self.neArmorVal         = config_vars['neArmorVal']  # Default 255
                    self.neBattles          = config_vars['neBattles']  # Default to 0
                    # Decides in which zone we charge Rikku OD after reaching Zanarkand.
                    self.neaZone            = config_vars['neaZone']

                    # ----Nemesis variables, unused in any%
                    self.nemAPVal           = config_vars['nemAPVal']  # Default to 1
                    self.yojimboIndex       = config_vars['yojimboIndex']

                    print("Loaded config file: ", CONFIG_FILE_PATH)
                except Exception as E:
                    print("Failed to parse config file: ", E)
        except:
            print("Unable to load config file: ", CONFIG_FILE_PATH)

        # Can't set these particular fields with this syntax in the yaml file
        self.firstHits = [0] * 8
        # Nemesis variables
        self.areaResults = [0] * 13
        self.speciesResults = [0] * 14
        self.originalResults = [0] * 7

        # ----Path for save files, used for loading a specific save
        self.savePath = (
            os.environ.get("userprofile")
            + "/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
        )

    def accessibilityVars(self):
        return [
            self.skip_cutscene_flag,
            self.skip_diag_flag,
            self.play_TTS_flag,
            self.rails_trials,
            self.rails_egg_hunt
        ]

    def useLegacySoundtrack(self):
        return self.legacySoundtrack

    def try_djose_skip(self):
        return self.attemptDjose

    def blitz_loss_reset(self):
        return self.blitzLossForceReset

    def use_set_seed(self):
        return self.setSeed

    def print_arena_status(self):
        print("###############################")
        print("Area:", self.areaResults)
        print("Species:", self.speciesResults)
        print("Original:", self.originalResults)
        print("###############################")

    def arena_success(self, array_num, index):
        print(array_num, "|", index)
        if array_num == 0:
            self.areaResults[index] = 1
        elif array_num == 1:
            self.speciesResults[index] = 1
        elif array_num == 2:
            self.originalResults[index] = 1
        self.print_arena_status()

    def yu_yevon_swag(self):
        return self.perfectAeonKills

    def skip_kilika_luck(self):
        return self.kilikaSkip

    def dont_skip_kilika_luck(self):
        self.kilikaSkip = False

    def loop_blitz(self):
        return self.blitzLoop

    def loop_seeds(self):
        return self.forceLoop

    def confirmed_seed(self):
        return self.confirmedSeedNum

    def set_confirmed_seed(self, value):
        self.confirmedSeedNum = value

    def set_new_game(self):
        self.newGame = True

    def new_game_check(self):
        return self.newGame

    def set_oblitz_rng(self, value):
        self.oblitzAttackVal = str(value)

    def oblitz_rng_check(self):
        return self.oblitzAttackVal

    def get_yellows(self):
        return self.yellows

    def set_yellows(self, new_vals):
        self.yellows = new_vals

    def yojimbo_get_index(self):
        return self.yojimboIndex

    def yojimbo_increment_index(self):
        self.yojimboIndex += 1

    def nemesis(self):
        return self.nemesisValue

    def get_nea_zone(self):
        return self.neaZone

    def set_nea_zone(self, value):
        self.neaZone = value

    def nem_checkpoint_ap(self):
        return self.nemAPVal

    def set_nem_checkpoint_ap(self, value):
        self.nemAPVal = value

    def ne_extra_battles(self):
        return self.neBattles

    def ne_battles_increment(self):
        self.neBattles += 1

    def ne_armor(self):
        return self.neArmorVal

    def set_ne_armor(self, value):
        self.neArmorVal = value

    def try_for_ne(self):
        return self.tryNEVal

    def first_hits_set(self, values):
        for x in range(8):
            self.firstHits[x] = values[x]

    def first_hits_value(self, index):
        return self.firstHits[index]

    def print_first_hits(self):
        print(self.firstHits)

    def game_save_path(self):
        return self.savePath

    def blitz_first_shot(self):
        return self.blitzFirstShotVal

    def blitz_first_shot_taken(self):
        self.blitzFirstShotVal = True

    def blitz_first_shot_reset(self):
        self.blitzFirstShotVal = False

    def flux_overkill(self):
        return self.fluxOverkillVar

    def flux_overkill_success(self):
        self.fluxOverkillVar = True

    def csr(self):
        return self.csrValue

    def set_csr(self, value):
        print("Setting CSR:", value)
        self.csrValue = value

    def complete_full_kilik_menu(self):
        self.fullKilikMenu = True

    def did_full_kilik_menu(self):
        return self.fullKilikMenu

    def use_pause(self):
        return self.artificialPauses

    def set_blitz_win(self, value):
        self.blitzWinValue = value

    def get_blitz_win(self):
        return self.blitzWinValue

    def set_blitz_ot(self, value):
        self.blitzOvertime = value

    def get_blitz_ot(self):
        return self.blitzOvertime

    def set_l_strike(self, value):
        self.lStrikeCount = value

    def get_l_strike(self):
        return self.lStrikeCount

    def zombie_weapon(self):
        return self.zombieWeaponVal

    def set_zombie(self, value):
        self.zombieWeaponVal = value

    def early_tidus_grid_set_true(self):
        self.earlyTidusGridVal = True

    def early_tidus_grid(self):
        return self.earlyTidusGridVal

    def early_haste_set(self, value):
        self.earlyHasteVal = value

    def early_haste(self):
        return self.earlyHasteVal

    def wakka_late_menu_set(self, value):
        self.wakkaLateMenuVal = value

    def wakka_late_menu(self):
        return self.wakkaLateMenuVal

    def end_game_version_set(self, value):
        self.endGameVersionVal = value

    def end_game_version(self):
        return self.endGameVersionVal

    def self_destruct_learned(self):
        self.selfDestruct = True

    def self_destruct_get(self):
        return self.selfDestruct

    def add_rescue_count(self):
        self.rescueCount += 1

    def completed_rescue_fights(self):
        print(f"Completed {self.rescueCount} exp kills")
        return self.rescueCount >= 4

    def add_ytk_farm(self):
        self.YTKFarm += 1

    def ytk_farm_count(self):
        return self.YTKFarm

    def completed_ytk_farm(self):
        return self.YTKFarm >= 2

    def set_skip_zan_luck(self, value):
        self.skipZanLuck = value

    def get_skip_zan_luck(self):
        return self.skipZanLuck


def init_vars():
    mainVars = AllVars()


def vars_handle():
    return mainVars


mainVars = AllVars()
