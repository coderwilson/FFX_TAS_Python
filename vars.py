import logging
import os

import config

logger = logging.getLogger(__name__)


class AllVars:
    def __init__(self):
        self.set_start_vars()

    def set_start_vars(self):
        # Open the config file
        config_data = config.open_config()
        # All relevant vars are stored in a dictionary
        config_vars = config_data.get("vars", {})

        # === Game mode set ===
        # ----Set defaults, then override for specific run type.
        self.perfect_aeon_kills = False
        self.attempt_djose = False
        self.skip_cutscene_flag = True
        self.force_blitz_win = False
        self.blitz_loop = False
        self.battle_speedup = False
        self.ml_heals_val = False
        self.run_modifier_val = "standard"
        # ----Overrides
        if config_vars.get("game_mode") == "speed":
            self.perfect_aeon_kills = True
            self.force_blitz_win = True
            self.battle_speedup = True
        elif config_vars.get("game_mode") == "story":
            self.skip_cutscene_flag = False
        elif config_vars.get("game_mode") == "swag":
            self.perfect_aeon_kills = True
        elif config_vars.get("game_mode") == "blitz_loop":
            self.blitz_loop = True

        # === RNG settings ===
        self.patched = config_vars.get("game_patched", False)
        self.rng_mode_val = config_vars.get("rng_mode", False)
        self.rng_seed = config_vars.get("rng_seed_num")
        self.rng_preferred_seeds = [31, 139, 160]

        # === Other vars from user ===
        self.nemesis_value = config_vars.get("nemesis_value", False)
        self.platinum_percent_value = False
        self.force_loop = config_vars.get("force_loop", False)
        self.legacy_soundtrack = config_vars.get("original_soundtrack", True)
        self.generate_saves = config_vars.get("generate_saves", False)

        # === Future functions / foundations ===
        self.kilika_skip = True
        self.rails_trials = True
        self.rails_egg_hunt = True
        self.skip_diag_flag = True
        self.play_TTS_flag = False

        # === Vars used by the TAS, no pre-set values ===
        # ----Cutscene remover, TAS will set this value on New Game
        # ----If loading to a save file without CSR, may need to change this.
        self.csr_value = True

        # ----Blitzball
        self.blitz_loss_force_reset = False
        self.blitz_win_value = True
        self.blitz_overtime = False
        self.blitz_first_shot_val = False
        self.oblitz_attack_val = "255"

        # ----Sphere grid
        self.full_kilika_menu = False
        self.early_tidus_grid_val = False
        self.early_haste_val = -1
        self.wakka_late_menu_val = False
        self.end_game_version_val = 0
        self.calm_levels_needed = 4

        # ----Equipment
        self.zombie_weapon_val = 255
        self.l_strike_count = 0
        self.mrr_skip = False

        # ----RNG Manip
        self.yellows = 0  # Not yet implemented. Part of thunderstrike weapon manip.
        self.confirmed_seed_num = 999
        self.skip_zan_luck = False
        self.god_mode_val = config_vars.get("god_mode", False)
        
        # ----NEA Manip
        self.try_ne_val = True  # We can choose False later, no current value here.
        self.ne_armor_val = 255
        self.ne_battles = 0  # Tracks number of forced manip battles outside and inside cave.
        self.nea_zone = 0
        self.nea_force_third_larvae = False
        self.nea_force_def_x_drop = False
        self.nea_after_bny = False
        self.nea_ignore = False

        # ----Other
        self.new_game = False
        self.self_destruct = False
        self.ytk_farm = 0
        self.rescue_count = 0
        self.flux_overkill_var = False
        self.first_hits = [0] * 8
        self.invert_confirm = False
        self.bypass_battle_music = config_vars.get("no_battle_music", False)

        # === Nemesis stuff ===
        # ----Nemesis variables, unused in any%
        # Nemesis route, determines Tidus level-up progress. Starts at 1
        self.nem_ap_val = 1
        self.yojimbo_index = 1  # Used in arena battles to track Zanmato progress.
        self.yojimbo_unlocked_val = False
        self.platinum_percent_value = False

        # ----Nemesis Arena variables, sets to 1 after a boss is killed.
        # ----Note, 0/1 are preferable to True/False for viewing in the console.
        self.area_results = [0] * 13
        self.species_results = [0] * 14
        self.original_results = [0] * 7

        # === Hardware / Other settings ===
        # ----Path for save files, used for loading a specific save
        # ---- The following are valid options, depending on your file path.
        # ---- "C://users//user_name//etc"
        # ---- "" (blank means to use the default path)
        self.save_path = str(config_vars.get("save_path"))
        logger.debug(f"Base save path: |{self.save_path}|")
        if len(self.save_path) == 0:
            logger.debug("Dynamically using userprofile, default")
            self.save_path = (
                os.environ.get("userprofile")
                + "/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"  # noqa: E501
            )
        elif config_vars.get("save_path").find(":"):
            logger.debug("Full save path provided from config")
        else:
            logger.debug("Possibly a bad save path, unknown state.")
        logger.debug(f"Save files, base path: {self.save_path}")
        # If your computer has bad specs, this will input commands to the controller
        # at a lower rate of speed. Very rarely used.
        self.artificial_pauses = config_vars.get("artificial_pauses", False)


    def ml_heals(self):
        return self.ml_heals_val

    def set_invert_confirm(self, value):
        self.invert_confirm = value

    def get_invert_confirm(self):
        return self.invert_confirm
    
    def set_ml_heals(self, value):
        self.ml_heals_val = value
    
    def run_modifier(self):
        return self.run_modifier_val
    
    def set_run_modifier(self, value):
        self.run_modifier_val = value

    def god_mode(self):
        if self.god_mode_val:
            logger.warning("God RNG Mode is active.")
        return self.god_mode_val
    
    def activate_god_rng(self):
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        logger.warning("== God RNG Mode is active. ==")
        self.god_mode_val = True

    def create_saves(self):
        return self.generate_saves

    def accessibility_vars(self):
        return [
            self.skip_cutscene_flag,
            self.skip_diag_flag,
            self.play_TTS_flag,
            self.rails_trials,
            self.rails_egg_hunt,
        ]
    
    def story_mode(self):
        return not self.skip_cutscene_flag

    def activate_story_mode(self):
        self.skip_cutscene_flag = False
        self.generate_saves = True

    def deactivate_story_mode(self):
        self.skip_cutscene_flag = True
        self.generate_saves = False

    def use_legacy_soundtrack(self):
        return self.legacy_soundtrack

    def try_djose_skip(self):
        return self.attempt_djose

    def get_force_blitz_win(self):
        return self.force_blitz_win

    def blitz_loss_reset(self):
        return self.blitz_loss_force_reset

    def game_is_patched(self):
        return self.patched

    def rng_mode(self):
        return self.rng_mode_val

    def rng_seed_num(self):
        return self.rng_seed

    def rng_seed_num_set(self, value):
        self.rng_mode_val = "set"
        self.rng_seed = value

    def rng_preferred_array(self):
        return self.rng_preferred_seeds

    def print_arena_status(self):
        logger.debug(f"Area: {self.area_results}")
        logger.debug(f"Species: {self.species_results}")
        logger.debug(f"Original: {self.original_results}")
    
    def arena_arrays(self):
        return self.area_results, self.species_results, self.original_results

    def arena_success(self, array_num, index):
        logger.debug(f"arena_success(): {array_num} | {index}")
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

    def set_loop_blitz(self, value):
        self.blitz_loop = value

    def loop_seeds(self):
        return self.force_loop

    def confirmed_seed(self):
        return self.confirmed_seed_num

    def set_confirmed_seed(self, value):
        self.confirmed_seed_num = value

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
    
    def yojimbo_unlocked(self):
        return self.yojimbo_unlocked_val
    
    def set_yojimbo_unlocked(self):
        self.yojimbo_unlocked_val = True

    def nemesis(self):
        return self.nemesis_value

    def nemesis_set(self, value):
        self.nemesis_value = value
        #self.generate_saves = True
        
    def platinum(self):
        return self.platinum_percent_value
        
    def platinum_set(self, value):
        self.platinum_percent_value = value

    def get_nea_zone(self):
        return self.nea_zone

    def set_nea_zone(self, value):
        self.nea_zone = value
    
    def get_force_third_larvae(self):
        return self.nea_force_third_larvae

    def set_force_third_larvae(self, value):
        self.nea_force_third_larvae = value

    def get_def_x_drop(self):
        return self.nea_force_def_x_drop

    def set_def_x_drop(self, value):
        self.nea_force_def_x_drop = value

    def get_nea_after_bny(self):
        return self.nea_after_bny

    def set_nea_after_bny(self, value):
        self.nea_after_bny = value

    def get_nea_ignore(self):
        return self.nea_ignore

    def set_nea_ignore(self, value):
        self.nea_ignore = value

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
        logger.debug(f"print_first_hits(): {self.first_hits}")

    def game_save_path(self):
        return self.save_path

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

    def update_calm_levels_needed(self, value):
        self.calm_levels_needed = value

    def get_calm_levels_needed(self):
        return self.calm_levels_needed

    def csr(self):
        if self.story_mode():
            return False
        return self.csr_value

    def set_csr(self, value):
        logger.debug(f"Setting CSR: {value}")
        self.csr_value = value

    def complete_full_kilika_menu(self):
        self.full_kilika_menu = True

    def did_full_kilika_menu(self):
        return self.full_kilika_menu

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

    def mrr_skip_val(self):
        return self.mrr_skip

    def mrr_skip_set(self, value):
        self.mrr_skip = value

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

    def reset_rescue_count(self, value=0):
        self.rescue_count = value

    def remove_rescue_count(self):
        self.rescue_count = 3

    def set_rescue_count(self, value):
        self.rescue_count = value

    def get_rescue_count(self):
        return self.rescue_count

    def completed_rescue_fights(self):
        # logger.debug(f"Completed {self.rescue_count} exp kills")
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
    
    def no_battle_music(self):
        return self.bypass_battle_music


def init_vars():
    AllVars()


def vars_handle():
    return main_vars


main_vars = AllVars()
