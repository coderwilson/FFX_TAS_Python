import os

import config


class AllVars:
    def __init__(self):
        self.set_start_vars()

    def set_start_vars(self):
        # Open the config file
        config_data = config.open_config()
        # All relevant vars are stored in a dictionary
        config_vars = config_data.get("vars", {})

        # === Important Values ===
        # Set depending on hardware. True = less powerful hardware.
        self.artificial_pauses = config_vars.get("artificial_pauses", False)
        # Set automatically on new game. For testing (loading a save file) set for your environment.
        self.csr_value = config_vars.get("csr_value", True)
        # Set based on if you're doing any% (False) or Nemesis% (True)
        self.nemesis_value = config_vars.get("nemesis_value", False)
        # After game is finished, start again on next seed.
        self.force_loop = config_vars.get("force_loop", False)
        # If you are using Rossy's patch, set to True. Otherwise set to False
        self.set_seed = config_vars.get("set_seed", False)
        # True == Tidus OD on Evrae instead of Seymour. New strat.
        self.kilika_skip = config_vars.get("kilika_skip", True)
        # Before YuYevon, True is slower but more swag.
        self.perfect_aeon_kills = config_vars.get("perfect_aeon_kills", False)
        # Try Djose skip? (not likely to succeed)
        self.attempt_djose = config_vars.get("attempt_djose", False)
        # use the original Soundtrack instead of arranged
        self.legacy_soundtrack = config_vars.get("legacy_soundtrack", True)
        self.do_not_skip_cutscenes = config_vars.get("do_not_skip_cutscenes", False)
        self.battle_speedup = config_vars.get("battle_speedup", False)

        # ----Accessibility for blind
        self.skip_cutscene_flag = config_vars.get("skip_cutscene_flag", True)
        self.skip_diag_flag = config_vars.get("skip_diag_flag", True)
        self.play_TTS_flag = config_vars.get("play_TTS_flag", False)
        self.rails_trials = config_vars.get("rails_trials", True)
        self.rails_egg_hunt = config_vars.get("rails_egg_hunt", True)

        # ----Blitzball
        self.force_blitz_win = config_vars.get("force_blitz_win", False)
        # Loop on the same seed immediately after Blitzball.
        self.blitz_loop = config_vars.get("blitz_loop", False)
        # True = reset after blitz loss
        self.blitz_loss_force_reset = config_vars.get("blitz_loss_force_reset", True)
        # No default value required
        self.blitz_win_value = config_vars.get("blitz_win_value", True)
        # Set to False, no need to change ever.
        self.blitz_overtime = config_vars.get("blitz_overtime", False)
        self.blitz_first_shot_val = config_vars.get("blitz_first_shot_val", False)
        # Used for RNG manip tracking
        self.oblitz_attack_val = config_vars.get("oblitz_attack_val", "255")

        # ----Sphere grid
        self.full_kilik_menu = config_vars.get(
            "full_kilik_menu", False
        )  # Default to False
        self.early_tidus_grid_val = config_vars.get("early_tidus_grid_val", False)
        # Default False
        self.early_haste_val = config_vars.get("early_haste_val", 1)  # Default -1
        # Default False
        self.wakka_late_menu_val = config_vars.get("wakka_late_menu_val", False)
        self.end_game_version_val = config_vars.get(
            "end_game_version_val", 1
        )  # Default 0

        # ----Equipment
        self.zombie_weapon_val = config_vars.get(
            "zombie_weapon_val", 255
        )  # Default 255
        self.l_strike_count = config_vars.get("l_strike_count", 1)  # Default 0

        # ----RNG Manip
        self.yellows = config_vars.get("yellows", 0)  # ?
        self.confirmed_seed_num = config_vars.get("confirmed_seed_num", 999)  # ?
        self.skip_zan_luck = config_vars.get("skip_zan_luck", False)  # ?

        # ----Other
        self.new_game = config_vars.get("new_game", False)  # ?
        self.self_destruct = config_vars.get("self_destruct", False)  # Default False
        self.ytk_farm = config_vars.get("ytk_farm", 0)  # Default to 0
        self.rescue_count = config_vars.get("rescue_count", 0)  # Default to 0
        # Default to False
        self.flux_overkill_var = config_vars.get("flux_overkill_var", False)
        self.try_ne_val = config_vars.get("try_ne_val", True)  # Based on
        self.ne_armor_val = config_vars.get("ne_armor_val", 255)  # Default 255
        self.ne_battles = config_vars.get("ne_battles", 0)  # Default to 0
        # Decides in which zone we charge Rikku OD after reaching Zanarkand.
        self.nea_zone = config_vars.get("nea_zone", 0)

        # ----Nemesis variables, unused in any%
        self.nem_ap_val = config_vars.get("nem_ap_val", 1)  # Default to 1
        self.yojimbo_index = config_vars.get("yojimbo_index", 1)

        # Can't set these particular fields with this syntax in the yaml file
        self.first_hits = [0] * 8
        # Nemesis variables
        self.area_results = [0] * 13
        self.species_results = [0] * 14
        self.original_results = [0] * 7

        # ----Path for save files, used for loading a specific save
        self.savePath = (
            os.environ.get("userprofile")
            + "/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
        )

    def accessibility_vars(self):
        return [
            self.skip_cutscene_flag,
            self.skip_diag_flag,
            self.play_TTS_flag,
            self.rails_trials,
            self.rails_egg_hunt,
        ]

    def use_legacy_soundtrack(self):
        return self.legacy_soundtrack

    def try_djose_skip(self):
        return self.attempt_djose

    def get_force_blitz_win(self):
        return self.force_blitz_win

    def blitz_loss_reset(self):
        return self.blitz_loss_force_reset

    def use_set_seed(self):
        return self.set_seed

    def print_arena_status(self):
        print("###############################")
        print("Area:", self.area_results)
        print("Species:", self.species_results)
        print("Original:", self.original_results)
        print("###############################")

    def arena_success(self, array_num, index):
        print(array_num, "|", index)
        if array_num == 0:
            self.area_results[index] = 1
        elif array_num == 1:
            self.species_results[index] = 1
        elif array_num == 2:
            self.original_results[index] = 1
        self.print_arena_status()

    def yu_yevon_swag(self):
        return self.perfect_aeon_kills

    def skip_kilika_luck(self):
        return self.kilika_skip

    def dont_skip_kilika_luck(self):
        self.kilika_skip = False

    def loop_blitz(self):
        return self.blitz_loop

    def loop_seeds(self):
        return self.force_loop

    def confirmed_seed(self):
        return self.confirmed_seed_num

    def set_confirmed_seed(self, value):
        self.confirmed_seed_num = value

    def set_new_game(self):
        self.new_game = True

    def new_game_check(self):
        return self.new_game

    def set_oblitz_rng(self, value):
        self.oblitz_attack_val = str(value)

    def oblitz_rng_check(self):
        return self.oblitz_attack_val

    def get_yellows(self):
        return self.yellows

    def set_yellows(self, new_vals):
        self.yellows = new_vals

    def yojimbo_get_index(self):
        return self.yojimbo_index

    def yojimbo_increment_index(self):
        self.yojimbo_index += 1

    def nemesis(self):
        return self.nemesis_value

    def get_nea_zone(self):
        return self.nea_zone

    def set_nea_zone(self, value):
        self.nea_zone = value

    def nem_checkpoint_ap(self):
        return self.nem_ap_val

    def set_nem_checkpoint_ap(self, value):
        self.nem_ap_val = value

    def ne_extra_battles(self):
        return self.ne_battles

    def ne_battles_increment(self):
        self.ne_battles += 1

    def ne_armor(self):
        return self.ne_armor_val

    def set_ne_armor(self, value):
        self.ne_armor_val = value

    def try_for_ne(self):
        return self.try_ne_val

    def first_hits_set(self, values):
        for x in range(8):
            self.first_hits[x] = values[x]

    def first_hits_value(self, index):
        return self.first_hits[index]

    def print_first_hits(self):
        print(self.first_hits)

    def game_save_path(self):
        return self.savePath

    def blitz_first_shot(self):
        return self.blitz_first_shot_val

    def blitz_first_shot_taken(self):
        self.blitz_first_shot_val = True

    def blitz_first_shot_reset(self):
        self.blitz_first_shot_val = False

    def flux_overkill(self):
        return self.flux_overkill_var

    def flux_overkill_success(self):
        self.flux_overkill_var = True

    def csr(self):
        return self.csr_value

    def set_csr(self, value):
        print("Setting CSR:", value)
        self.csr_value = value

    def complete_full_kilik_menu(self):
        self.full_kilik_menu = True

    def did_full_kilik_menu(self):
        return self.full_kilik_menu

    def use_pause(self):
        return self.artificial_pauses

    def set_blitz_win(self, value):
        self.blitz_win_value = value

    def get_blitz_win(self):
        return self.blitz_win_value

    def set_blitz_ot(self, value):
        self.blitz_overtime = value

    def get_blitz_ot(self):
        return self.blitz_overtime

    def set_l_strike(self, value):
        self.l_strike_count = value

    def get_l_strike(self):
        return self.l_strike_count

    def zombie_weapon(self):
        return self.zombie_weapon_val

    def set_zombie(self, value):
        self.zombie_weapon_val = value

    def early_tidus_grid_set_true(self):
        self.early_tidus_grid_val = True

    def early_tidus_grid(self):
        return self.early_tidus_grid_val

    def early_haste_set(self, value):
        self.early_haste_val = value

    def early_haste(self):
        return self.early_haste_val

    def wakka_late_menu_set(self, value):
        self.wakka_late_menu_val = value

    def wakka_late_menu(self):
        return self.wakka_late_menu_val

    def end_game_version_set(self, value):
        self.end_game_version_val = value

    def end_game_version(self):
        return self.end_game_version_val

    def self_destruct_learned(self):
        self.self_destruct = True

    def self_destruct_get(self):
        return self.self_destruct

    def add_rescue_count(self):
        self.rescue_count += 1

    def completed_rescue_fights(self):
        print(f"Completed {self.rescue_count} exp kills")
        return self.rescue_count >= 4

    def add_ytk_farm(self):
        self.ytk_farm += 1

    def ytk_farm_count(self):
        return self.ytk_farm

    def completed_ytk_farm(self):
        return self.ytk_farm >= 2

    def set_skip_zan_luck(self, value):
        self.skip_zan_luck = value

    def get_skip_zan_luck(self):
        return self.skip_zan_luck

    def get_battle_speedup(self):
        return self.battle_speedup


def init_vars():
    mainVars = AllVars()


def vars_handle():
    return mainVars


mainVars = AllVars()
