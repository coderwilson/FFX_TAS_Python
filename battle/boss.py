import logging

import battle.main
from battle.main import wrap_up
import battle.utils
import damage
import logs
import manip_planning.rng
import memory.main
import screen
import vars
import xbox
from players import (
    Auron,
    Bahamut,
    CurrentPlayer,
    Kimahri,
    Lulu,
    Rikku,
    Tidus,
    Valefor,
    Wakka,
    Yuna,
)
from battle import avina_memory
from area.gagazet import check_gems
from json_ai_files.write_seed import write_returns

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()
from rng_track import drop_rare, force_equip, force_drop

logger = logging.getLogger(__name__)
import tts # Used to check Kimahri logic.

import rng_track


def ammes_truerng():
    battle_complete = 0
    count_attacks = 0

    while battle_complete != 1:
        if memory.main.turn_ready():
            logger.info("Attacking Sinspawn Ammes")
            if Tidus.is_turn() and Tidus.has_overdrive():
                if memory.main.future_attack_will_crit(
                    character=0, char_luck=18, enemy_luck=10
                ):
                    logger.manip("Overdrive crit")
                    Tidus.overdrive()
                elif memory.main.get_enemy_current_hp()[0] < 700:
                    logger.manip("Boss low, just hit the overdrive.")
                    Tidus.overdrive()
                else:
                    logger.manip("Attack. Maybe a crit later?")
                    CurrentPlayer().attack()
            else:
                CurrentPlayer().attack()
                count_attacks += 1
        if memory.main.user_control():
            battle_complete = 1
            logger.info("Ammes battle complete")


# Spiral Cut turn is relative to the first turn he could use it, i.e. his second turn in the fight is Spiral Cut turn 1
def ammes(spiral_cut_turn: int):
    battle_complete = 0
    count_attacks = 0
    tidus_turn = 0

    while battle_complete != 1:
        if memory.main.turn_ready():
            logger.info("Attacking Sinspawn Ammes")
            if Tidus.is_turn():
                tidus_turn += 1
                if tidus_turn == spiral_cut_turn + 1:
                    Tidus.overdrive()
                    logger.debug(f"Spiral Cut Turn on turn {tidus_turn}")
                else:
                    CurrentPlayer().attack()
                    logger.debug(f"Not Spiral Cut Turn so just Attack on turn {tidus_turn}")
            else:
                CurrentPlayer().attack()
                count_attacks += 1
        if memory.main.user_control():
            battle_complete = 1
            logger.info("Ammes battle complete")


def kimahri_game_over():
    seed = str(game_vars.rng_seed_num())
    logger.error(f"Kimahri game over!!! {seed}")
    avina_memory.add_to_memory(seed=seed, key="kimahri_force_heal", value="True")
    # Report to JSON file for future acknowledgement


@battle.utils.speedup_decorator
def kimahri():
    FFXC.set_neutral()
    # Pull from JSON file to get dynamic value.
    force_heal = False
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        if seed_str in records.keys():
            if records[seed_str]["kimahri_force_heal"] == "True":
                force_heal = True
        else:
            logger.info("I have no memory of this seed.")
    except Exception:
        pass
    logger.debug(f"Forcing heal: {force_heal}")
    if force_heal:
        logger.info("This RNG seed requires a heal on the Kimahri fight.")
    else:
        logger.info("No memory of this seed for Kimahri fight. Treating like normal.")

    while memory.main.battle_active():
        if memory.main.game_over():
            logger.warning("GAME OVER!!!")
            kimahri_game_over()
            return False
        elif memory.main.turn_ready():
            enemy_hp = memory.main.get_enemy_current_hp()
            if force_heal and Tidus.in_danger(300):
                logger.info("Known game-over RNG state, forcing heal on Tidus.")
                battle.main.use_potion_character(Tidus, "l")
                force_heal = False
            elif (
                not game_vars.early_tidus_grid()
                and memory.main.get_turn_by_index(1) != 0
                and memory.main.get_turn_by_index(2) != 0
                and Tidus.in_danger(140)
                and enemy_hp[0] > 119
            ):
                if Tidus.next_crit(12) == 2:
                    CurrentPlayer().attack()
                else:
                    battle.main.use_potion_character(Tidus, "l")
            elif (
                Tidus.in_danger(200)
                and memory.main.get_turn_by_index(1) != 0
                and memory.main.get_turn_by_index(2) != 0
                and enemy_hp[0] > 119
            ):
                if Tidus.next_crit(12) == 2:
                    CurrentPlayer().attack()
                else:
                    battle.main.use_potion_character(Tidus, "l")
            else:
                CurrentPlayer().attack()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    if memory.main.game_over():
        logger.warning("GAME OVER!!!")
        kimahri_game_over()
        return False
    logger.info("Kimahri fight complete.")
    if game_vars.story_mode():
        while not memory.main.battle_wrap_up_active():
            pass
        wrap_up()
    else:
        memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return True


def tidus_wakka_tutorial():
    memory.main.click_to_event()
    FFXC.set_neutral()
    xbox.click_to_battle()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            CurrentPlayer().attack()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()
    wrap_up()


@battle.utils.speedup_decorator
def black_magic_tutorial():
    xbox.click_to_battle()
    CurrentPlayer().attack()
    if game_vars.story_mode():
        memory.main.wait_seconds(26)
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        screen.await_turn()
    else:
        xbox.click_to_battle()
    CurrentPlayer().cast_black_magic_spell(1)
    wrap_up()


@battle.utils.speedup_decorator
def summon_tutorial():
    if game_vars.story_mode():
        memory.main.wait_seconds(20)
        xbox.tap_confirm()
        xbox.tap_confirm()
    else:
        xbox.click_to_battle()
    while not screen.turn_aeon():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                battle.main.aeon_summon(0)
            elif screen.turn_aeon():
                pass
            elif not Yuna.active():
                if game_vars.story_mode():
                    battle.main.buddy_swap(Yuna, quick_return=True)
                    memory.main.wait_seconds(15)
                    xbox.tap_confirm()
                    memory.main.wait_seconds(2)
                    xbox.tap_confirm()
                else:
                    battle.main.buddy_swap(Yuna, quick_return=False)
            else:
                CurrentPlayer().defend()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            CurrentPlayer().cast_black_magic_spell(1)
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def dark_attack_tutorial():
    battle.main.escape_all()
    if game_vars.god_mode():
        rng_track.force_preempt()


def tanker(sinscale_kill: bool):
    logger.info("Fight start: Tanker")
    count_attacks = 0
    tidus_count = 0
    auron_count = 0
    xbox.click_to_battle()

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                tidus_count += 1
                if tidus_count < 4:
                    Tidus.swap_battle_weapon()
                else:
                    Tidus.attack()
                    count_attacks += 1
            elif Auron.is_turn():
                auron_count += 1
                if auron_count < 2:
                    if sinscale_kill:
                        Auron.attack()
                    else:
                        Auron.attack(Auron)
                else:
                    Auron.attack()
                    count_attacks += 1
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
            
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def klikk_truerng():
    logger.info("Fight start: Klikk")
    heal_used = False
    klikk_attacks = 0
    klikk_revives = 0
    steal_count = 0
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Tidus.is_dead():
                battle.main.revive()
                klikk_revives += 1
            elif Tidus.is_turn():
                if (
                    Rikku.is_dead()
                    and memory.main.get_enemy_current_hp()[0] > 125
                    and Tidus.in_danger(120)
                ):
                    battle.main.use_potion_character(Tidus, "l")
                    heal_used = True
                else:
                    CurrentPlayer().attack()
                klikk_attacks += 1
            elif Rikku.is_turn():
                grenade_count = memory.main.get_item_count_slot(
                    memory.main.get_item_slot(35)
                )
                logger.debug("==== Tidus HP check:")
                logger.debug(f"==== In danger (120): {Tidus.in_danger(120)}")
                logger.debug(f"==== Heal Used: {heal_used}")
                logger.debug(f"==== Next Turn: {memory.main.get_next_turn()}")
                logger.debug(f"==== Enemy HP: {memory.main.get_enemy_current_hp()[0]}")

                if (
                    Tidus.in_danger(120)
                    and not heal_used
                    and not (
                        memory.main.get_next_turn() == 0
                        and memory.main.get_enemy_current_hp()[0] <= 181
                    )
                ):
                    battle.main.use_potion_character(Tidus, "l")
                    klikk_revives += 1
                    heal_used = True
                elif memory.main.get_enemy_current_hp()[0] < 58:
                    CurrentPlayer().attack()
                    klikk_attacks += 1
                elif grenade_count < 6 and memory.main.next_steal(
                    steal_count=steal_count
                ):
                    logger.info("Attempting to steal from Klikk")
                    battle.main.steal()
                    steal_count += 1
                else:
                    CurrentPlayer().attack()
                    klikk_attacks += 1
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.info("Klikk fight complete")
    logger.debug(f"map: {memory.main.get_map()}")
    while not (
        memory.main.get_map() == 71
        and memory.main.user_control()
        and memory.main.get_coords()[1] < 15
    ):
        # logger.debug(memory.main.get_map())
        if game_vars.csr():
            FFXC.set_confirm()
        else:
            xbox.tap_b()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.wait_frames(1)
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def klikk(tidus_potion_klikk: bool, tidus_potion_turn: int, rikku_potion_klikk: bool, klikk_steals: int):
    logger.info("Fight start: Klikk")
    tidus_turn = 0
    rikku_turn = 0
    
    xbox.click_to_battle()

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Tidus.is_turn():
                tidus_turn += 1
                if tidus_potion_klikk and tidus_turn == tidus_potion_turn:
                    battle.main.use_potion_character(Tidus, "l")
                else:
                    Tidus.attack()
            elif Rikku.is_turn():
                rikku_turn += 1
                if rikku_turn == 1:
                    grenade_slot = memory.main.get_use_items_slot(35)
                    battle.main.use_item(slot=grenade_slot)
                elif rikku_turn == 2 and rikku_potion_klikk:
                    battle.main.use_potion_character(Tidus, "l")
                elif rikku_turn <= klikk_steals + 1 + (1 if rikku_potion_klikk else 0):
                    battle.main.steal()
                else:
                    Rikku.attack()
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.info("Klikk fight complete")
    logger.debug(f"map: {memory.main.get_map()}")
    wrap_up()
    while not (
        memory.main.get_map() == 71
        and memory.main.user_control()
        and memory.main.get_coords()[1] < 15
    ):
        # logger.debug(memory.main.get_map())
        if game_vars.csr():
            FFXC.set_confirm()
        elif not game_vars.story_mode():
            xbox.tap_b()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.wait_frames(1)


@battle.utils.speedup_decorator
def tros_truerng():
    logs.open_rng_track()
    logger.info("Fight start: Tros")
    FFXC.set_neutral()
    battle_clock = 0
    Attacks = 0
    Revives = 0
    Grenades = 0
    Steals = 0
    advances = 0
    while not memory.main.turn_ready():
        pass

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            battle_clock += 1
            logger.debug(f"Battle clock: {battle_clock}")
            tros_pos = 2
            logger.debug("Determining Tros position")
            while tros_pos == 2 and memory.main.battle_active():
                # Two for "not yet determined". Maybe can be HP-based instead?
                camera = memory.main.get_camera()
                logger.debug(f"Camera position: {camera[0]}")
                # First, determine position of Tros
                if camera[0] > 2:
                    tros_pos = 1  # One for cannot attack.
                    logger.debug("Tros is long-range. Cannot attack.")
                elif camera[0] < -2:
                    tros_pos = 1  # One for cannot attack.
                    logger.debug("Tros is long-range. Cannot attack.")
                else:
                    tros_pos = 0  # Zero for "Close range, can be attacked.
                    logger.debug("Tros is short-range.")

            # Assuming battle is not complete:
            if memory.main.battle_active():
                # Someone requires reviving.
                if Tidus.is_dead() or Rikku.is_dead():
                    logger.debug("Tros: Someone fainted.")
                    battle.main.revive()
                    Revives += 1
                elif Rikku.is_turn():
                    logger.debug("Rikku turn")
                    grenade_slot = memory.main.get_item_slot(35)
                    grenade_count = memory.main.get_item_count_slot(grenade_slot)
                    logger.debug(f"Current grenade count: {grenade_count}")
                    logger.debug(f"Grenades used: {Grenades}")
                    total_grenades = grenade_count + Grenades
                    if total_grenades < 6:
                        if tros_pos == 1:
                            CurrentPlayer().defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    elif grenade_count == 0:
                        if tros_pos == 1:
                            CurrentPlayer().defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    else:
                        if tros_pos != 1 and advances in [1, 2]:
                            battle.main.steal()
                            Steals += 1
                        else:
                            grenade_slot = memory.main.get_use_items_slot(35)
                            if game_vars.god_mode():
                                memory.main.future_attack_will_crit(
                                    character=6,
                                    char_luck=17,
                                    enemy_luck=15
                                )
                            battle.main.use_item(grenade_slot, "none")
                            Grenades += 1
                elif Tidus.is_turn():
                    logger.debug("Tidus turn")
                    if (
                        tros_pos == 1
                        and Rikku.in_danger(200)
                        and memory.main.get_enemy_current_hp()[0] > 800
                    ):
                        battle.main.use_potion_character(Rikku, "l")
                    elif tros_pos == 1 or memory.main.get_enemy_current_hp()[0] < 300:
                        CurrentPlayer().defend()
                    else:
                        CurrentPlayer().attack()
                        Attacks += 1

    logger.info("Tros battle complete.")
    wrap_up()
    
    #memory.main.click_to_control()
    #if game_vars.god_mode():
    #    rng_track.force_preempt()


def tros(preempt: bool):
    logs.open_rng_track()
    logger.info("Fight start: Tros")
    FFXC.set_neutral()

    rikku_turn = 0
    tidus_turn = 0

    rng26_rolls = 0

    total_damage = 0
    low_roll = False

    done_stealing = False

    rng20_array_tidus = memory.main.rng_array_from_index(index=20, array_len=200)
    rng26_array_rikku = memory.main.rng_array_from_index(index=26, array_len=200)

    for i in range(6):
        base_damage = 350
        var_damage = manip_planning.rng.get_rng_damage(base_damage=base_damage, rng_array=rng26_array_rikku,
                                                       rng_rolls=2 * i, user_luck=18, target_luck=15)
        if i == 0 and not preempt:

            low_roll = var_damage < 350
            logging.debug(f"Normal 1st Attack Low Roll: {low_roll}")

        elif i == 4 and preempt:

            low_roll = var_damage < 350
            logging.debug(f"Pre-empt 5th Attack Low Roll: {low_roll}")

        total_damage += var_damage
        logging.debug(f"Grenade Damage: {var_damage} / Total Damage: {total_damage}")

        if total_damage > (6 * 328):

            grenades_required = i + 1
            logger.debug(f"Grenades Required: {grenades_required}")
            break

    base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15, target_stat=1)
    var_damage = manip_planning.rng.get_rng_damage(base_damage=base_damage, rng_array=rng20_array_tidus,
                                                   rng_rolls=0, user_luck=18, target_luck=15)

    total_damage += var_damage

    if total_damage > 2200:
        tidus_attacks = 1
    else:
        tidus_attacks = 2

    # while not memory.main.turn_ready():
    #     pass

    while memory.main.battle_active():  # AKA end of battle screen

        if memory.main.diag_skip_possible():

            xbox.tap_b()

        elif memory.main.turn_ready():

            if Rikku.is_turn():

                rikku_turn += 1
                grenade_count = memory.main.get_item_count_slot(memory.main.get_item_slot(35))
                logger.debug(f"Grenade Count: {grenade_count} / {grenades_required}")
                if grenade_count < grenades_required and not done_stealing:

                    battle.main.steal()

                elif grenade_count > 0:

                    logger.debug("Done Stealing")
                    done_stealing = True
                    grenade_slot = memory.main.get_use_items_slot(35)
                    battle.main.use_item(slot=grenade_slot)

                else:

                    Rikku.defend()

            elif Tidus.is_turn():

                tidus_turn += 1

                if Rikku.is_dead():
                    battle.main.revive_target(target=6)

                elif tidus_turn == 1 and low_roll and not preempt:

                    Tidus.defend()

                elif rikku_turn == 5 and low_roll and preempt:

                    Tidus.defend()

                elif tros_position() == 1:

                    Tidus.defend()

                elif tidus_attacks > 0:

                    tidus_attacks -= 1
                    Tidus.attack()

                else:

                    Tidus.defend()



    logger.info("Tros battle complete.")
    wrap_up()


def tros_position():
    camera = memory.main.get_camera()
    logger.debug(f"Camera position: {camera[0]}")

    # First, determine position of Tros
    if camera[0] > 2:
        tros_pos = 1  # One for cannot attack.
        logger.debug("Tros is long-range. Cannot attack.")
    elif camera[0] < -2:
        tros_pos = 1  # One for cannot attack.
        logger.debug("Tros is long-range. Cannot attack.")
    else:
        tros_pos = 0  # Zero for "Close range, can be attacked.
        logger.debug("Tros is short-range.")

    return tros_pos


@battle.utils.speedup_decorator
def sin_fin():
    logger.info("Fight start: Sin's Fin")
    screen.await_turn()
    complete = False
    while not complete:
        if memory.main.turn_ready():
            logger.debug("First turns.")
            if Tidus.is_turn():
                CurrentPlayer().defend()
                logger.debug("Tidus defend")
            elif Yuna.is_turn():
                battle.main.buddy_swap(Lulu)  # Yuna out, Lulu in
                CurrentPlayer().cast_black_magic_spell(1, target_id=23, direction="r")
            else:
                battle.main.buddy_swap(Yuna)
                battle.main.aeon_summon(0)
                Valefor.overdrive(overdrive_num=0, sin_fin=True)
                complete = True

    logger.info("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Lulu.is_turn() or Valefor.is_turn():
                CurrentPlayer().cast_black_magic_spell(1, target_id=23, direction="r")
            elif Lulu.is_dead():
                battle.main.revive_target(target=5)
            else:
                CurrentPlayer().defend()

            # Old logic:
            # logger.debug(f"Valefor OD percent: {Valefor.overdrive_percent()}")
            # if Valefor.overdrive_percent(combat=True) == 20:
            #    logger.info("Valefor energy ray")
            #    Valefor.overdrive(overdrive_num=0, sin_fin=True)
            # else:
            #    logger.info("Valefor thunder")
            #    Valefor.cast_black_magic_spell(spell_id=1, target_id=23)
    logger.info("Sin's Fin fight complete")
    xbox.click_to_battle()


@battle.utils.speedup_decorator
def echuilles():
    logger.info("Fight start: Sinspawn Echuilles")
    screen.await_turn()
    logger.info("Sinspawn Echuilles fight start")
    logs.write_rng_track("###########################")
    logs.write_rng_track("Echuilles start")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))

    tidus_counter = 0
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                battle.main.revive()
            elif Tidus.is_turn():
                tidus_counter += 1
                if tidus_counter <= 2:
                    logger.debug("Cheer")
                    Tidus.flee()  # performs cheer command
                elif (
                    memory.main.get_overdrive_battle(0) == 100
                    and memory.main.get_enemy_current_hp()[0] <= 750
                ):
                    logger.debug("Overdrive")
                    Tidus.overdrive()
                else:
                    logger.debug("Tidus attack")
                    CurrentPlayer().attack()
            elif Wakka.is_turn():
                if tidus_counter == 1:  # and memory.main.rng_seed() != 160:
                    logger.debug("Dark Attack")
                    battle.main.use_skill(0)  # Dark Attack
                # elif memory.main.get_enemy_current_hp()[0] <= 558:
                #    logger.debug("Ready for Tidus Overdrive. Wakka defends.")
                #    CurrentPlayer().defend()
                else:
                    logger.debug("Wakka attack")
                    CurrentPlayer().attack()
    logger.info("Battle is complete. Now awaiting control.")
    while not memory.main.user_control():
        if game_vars.story_mode():
            if memory.main.battle_wrap_up_active():
                wrap_up()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
    logs.write_rng_track("###########################")
    logs.write_rng_track("Echuilles end")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def geneaux():
    logger.info("Fight start: Sinspawn Geneaux")
    xbox.click_to_battle()

    if Tidus.is_turn():
        CurrentPlayer().attack()
    elif Yuna.is_turn():
        battle.main.buddy_swap(Kimahri)
        CurrentPlayer().attack()
        while not Tidus.is_turn():
            if memory.main.turn_ready():
                CurrentPlayer().defend()
        while Tidus.is_turn():
            if memory.main.turn_ready():
                CurrentPlayer().defend()
        memory.main.wait_frames(3)
        while not memory.main.turn_ready():
            pass
        battle.main.buddy_swap(Yuna)
    screen.await_turn()
    battle.main.aeon_summon(0)  # Summon Valefor

    first_od_used = False
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            if game_vars.story_mode() and first_od_used:
                logger.info("Valefor fire")
                Valefor.cast_black_magic_spell(spell_id=0)
            elif Valefor.overdrive_percent(combat=True) == 20:
                logger.info("Valefor energy ray")
                Valefor.overdrive(overdrive_num=0, sin_fin=True)
                first_od_used = True
            else:
                logger.info("Valefor fire")
                Valefor.cast_black_magic_spell(spell_id=0)
        else:
            FFXC.set_neutral()
    logger.info("Battle with Sinspawn Geneaux Complete")
    if game_vars.story_mode():
        while not memory.main.battle_wrap_up_active():
            pass
        wrap_up()
    else:
        memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def oblitzerator(early_haste):
    logger.info("Fight start: Oblitzerator")
    xbox.click_to_battle()
    crane = 0
    
    
    if game_vars.god_mode():
        force_equip(equip_type=0, character=0,aeon_kill=False, party_size=3)
        force_drop()

    if early_haste >= 1:
        # First turn is always Tidus. Haste Lulu if we've got the levels.
        battle.main.tidus_haste(direction="left", character=5)

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if crane < 3:
                if Lulu.is_turn():
                    crane += 1
                    CurrentPlayer().cast_black_magic_spell(
                        1, target_id=21, direction="r"
                    )
                else:
                    CurrentPlayer().defend()
            elif crane == 3:
                if Tidus.is_turn():
                    crane += 1
                    while memory.main.main_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    battle.main.tap_targeting()
                elif Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1)
                else:
                    CurrentPlayer().defend()
            else:
                if Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1)
                elif Tidus.is_turn():
                    battle.main.attack_oblitz_end()
                else:
                    CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.info("End of fight, Oblitzerator")
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


def chocobo_eater():
    logger.info("Fight start: Chocobo Eater")
    screen.await_turn()
    battle.main.tidus_haste(direction="l", character=20)
    while memory.main.battle_active():
        if memory.main.turn_ready():
            # Only if two people are down, very rare but for safety.
            if screen.faint_check() >= 2:
                logger.debug("Attempting revive")
                battle.main.revive()
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.info("Chocobo Eater battle complete.")
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


def chocobo_eater_old():
    logger.info("Fight start: Chocobo Eater")
    rng44Last = memory.main.rng_from_index(44)
    turns = 0
    choco_target = 255
    choco_next = False
    choco_haste = False
    screen.await_turn()
    char_hp_last = memory.main.get_battle_hp()

    # If chocobo doesn't take the second turn, that means it out-sped Tidus.
    if memory.main.get_next_turn() != 20:
        if memory.main.rng_from_index(44) == rng44Last:
            # Eater did not take an attack, but did take first turn.
            # Should register as true.
            choco_next = True
    swapped_yuna = False
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if choco_next:
                choco_next = False
                if memory.main.get_battle_hp() != char_hp_last:  # We took damage
                    pass
                elif memory.main.rng_from_index(44) != rng44Last:
                    # Chocobo eater attacked, covers miss
                    pass
                elif (
                    choco_target == 255
                    and 1 not in memory.main.get_active_battle_formation()
                ):
                    choco_index = memory.main.actor_index(actor_num=4200)
                    logger.debug(f"Chocobo index: {choco_index}")
                    choco_angle = memory.main.get_actor_angle(choco_index)
                    if choco_angle > 0.25:
                        logger.debug(f"Chocobo angle: {choco_angle}")
                        logger.debug("Selecting friendly target 2")
                        choco_target = memory.main.get_active_battle_formation()[0]
                    elif choco_angle < -0.25:
                        logger.debug(f"Chocobo angle: {choco_angle}")
                        logger.debug("Selecting friendly target 0")
                        choco_target = memory.main.get_active_battle_formation()[2]
                    else:
                        logger.debug(f"No Angle, using last hp's: {char_hp_last}")
                        logger.debug("Selecting friendly target 1")
                        choco_target = memory.main.get_active_battle_formation()[1]
            turns += 1
            if choco_target == memory.main.get_battle_char_turn():
                if not Yuna.active():
                    battle.main.buddy_swap(Yuna)
                    Yuna.attack(target_id=Yuna)
                    choco_target = 255
                    swapped_yuna = True
            if memory.main.get_next_turn() == 20:
                choco_next = True
                char_hp_last = memory.main.get_battle_hp()
                rng44Last = memory.main.rng_from_index(44)
            if choco_target != 255:
                logger.debug(f"Target for You're Next attack: {choco_target}")

            # Only if two people are down, very rare but for safety.
            if screen.faint_check() >= 2:
                logger.debug("Attempting revive")
                if Kimahri.is_turn():
                    if not Tidus.active():
                        battle.main.buddy_swap(Tidus)
                    elif not Wakka.active():
                        battle.main.buddy_swap(Wakka)
                    else:
                        battle.main.buddy_swap(Auron)
                battle.main.revive()
            # elif not Tidus.active():
            # Doesn't work - it still hits Tidus if
            # he swapped out and back in (instead of Yuna).
            #    buddy_swap(Tidus)
            elif (
                swapped_yuna
                and not Tidus.active()
                and memory.main.state_dead(1)
                and not choco_haste
            ):
                battle.main.buddy_swap(Tidus)
            elif (
                1 in memory.main.get_active_battle_formation()
                and not choco_haste
                and memory.main.get_battle_char_turn() == 0
            ):
                battle.main.tidus_haste(direction="l", character=20)
                # After Yuna in, haste choco eater.
                choco_haste = True
            else:
                logger.debug("Attempting defend")
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            logger.debug("Skipping dialog")
            xbox.tap_b()
    # logs.write_stats("Chocobo eater turns:")
    # logs.write_stats(str(turns))
    logger.info("Chocobo Eater battle complete.")
    memory.main.click_to_control()
    logger.debug("Back in control.")
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def gui():
    logger.info("Fight start: Sinspawn Gui")
    if game_vars.story_mode:
        screen.await_turn()
    else:
        xbox.click_to_battle()
    logger.info("Engaging Gui")
    logger.debug(
        "Expecting crit: "
        + f"{memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"
    )
    wakka_turn = False
    yuna_turn = False
    auron_turn = False
    tidus_turn = False
    aeon_turn = False
    kimahri_crit = False

    while not aeon_turn:
        if memory.main.turn_ready():
            if Yuna.is_turn():
                if not yuna_turn:
                    battle.main.buddy_swap(Auron)
                    yuna_turn = True
                else:
                    battle.main.aeon_summon(0)
            elif Wakka.is_turn():
                if not wakka_turn:
                    CurrentPlayer().swap_battle_weapon()
                    wakka_turn = True
                else:
                    battle.main.buddy_swap(Kimahri)
                    logger.debug(
                        f"Expecting crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"  # noqa: E501
                    )
            elif Kimahri.is_turn():
                dmg_before = memory.main.get_enemy_current_hp()[0]
                Kimahri.overdrive(2)
                screen.await_turn()
                dmg_after = memory.main.get_enemy_current_hp()[0]
                damage = dmg_before - dmg_after
                logger.debug(f"Kimahri OD damage: {damage}")
                logs.write_stats("gui_crit:")
                if damage > 6000:
                    kimahri_crit = True
                    logs.write_stats("True")
                else:
                    logs.write_stats("False")
            elif Tidus.is_turn():
                if not tidus_turn:
                    CurrentPlayer().defend()
                    tidus_turn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap(Kimahri)
                else:
                    battle.main.buddy_swap(Yuna)
            elif Auron.is_turn():
                if not auron_turn:
                    battle.main.use_skill(0)
                    auron_turn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap(Yuna)
                else:
                    CurrentPlayer().defend()
            elif screen.turn_aeon():
                Valefor.overdrive(overdrive_num=0)
                aeon_turn = True

    screen.await_turn()
    next_hp = memory.main.get_battle_hp()[0]
    last_hp = next_hp
    turn1 = False
    next_turn = 20
    last_turn = 20
    went = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready() and memory.main.get_battle_char_turn() == 8:
            next_hp = memory.main.get_battle_hp()[0]
            last_turn = next_turn
            next_turn = memory.main.get_next_turn()
            if went and kimahri_crit:
                CurrentPlayer().cast_black_magic_spell(1)
            elif memory.main.get_overdrive_battle(8) == 20:
                logger.debug("Overdriving")
                Valefor.overdrive(overdrive_num=0)
                went = True
            elif not turn1:
                turn1 = True
                logger.debug("Recharge unsuccessful. Attempting recovery.")
                CurrentPlayer().shield()
            elif last_turn == 8:  # Valefor takes two turns in a row
                logger.debug("Two turns in a row")
                CurrentPlayer().shield()
            elif next_hp > last_hp - 40 and not next_hp == last_hp:
                # Gravity spell was used
                logger.debug("Gravity was used")
                CurrentPlayer().shield()
            else:
                logger.debug("Attack was just used. Now boost.")
                CurrentPlayer().boost()
            last_hp = next_hp
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 1:
            logger.warning("Yuna turn, something went wrong.")
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 2:
            logger.warning("Auron turn, something went wrong.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        elif screen.turn_seymour():
            break

    # In between battles
    memory.main.wait_frames(12)
    while not memory.main.turn_ready():
        if (
            memory.main.get_story_progress() >= 865
            and memory.main.cutscene_skip_possible()
        ):
            memory.main.wait_frames(10)
            xbox.skip_scene()
            logger.info("Skipping scene")
        elif memory.main.menu_open():
            xbox.tap_confirm()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_confirm()

    # Second Gui battle
    seymour_turn = 0
    if (
        memory.main.get_overdrive_battle(8) == 20
        or memory.main.get_overdrive_battle(1) == 100
    ):
        logger.info("Gui2 - with extra Aeon overdrive")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_seymour() and seymour_turn < 2:
                    battle.main.seymour_spell(target_face=False)
                    seymour_turn += 1
                elif Yuna.is_turn() and seymour_turn >= 2:
                    logger.debug("Laser Time")
                    if memory.main.get_overdrive_battle(1) == 100:
                        while not memory.main.other_battle_menu():
                            xbox.tap_left()
                        while not memory.main.interior_battle_menu():
                            xbox.tap_b()
                        while memory.main.interior_battle_menu():
                            xbox.tap_b()
                    else:
                        battle.main.aeon_summon(0)
                elif screen.turn_aeon():
                    logger.debug("Firing")
                    Valefor.overdrive(overdrive_num=0)
                else:
                    logger.debug("Defend")
                    CurrentPlayer().defend()
    else:
        logger.info("Gui2 - standard")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_seymour():
                    battle.main.seymour_spell(target_face=True)
                else:
                    CurrentPlayer().defend()

    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            logger.debug("Intentional delay to get the cutscene skip to work.")
            memory.main.wait_frames(2)
            xbox.skip_scene_spec()
            memory.main.wait_frames(60)
        elif memory.main.menu_open():
            xbox.tap_confirm()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_confirm()


def extractor_mrr_skip():
    screen.await_turn()
    cheer_count = 0
    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.debug(memory.main.get_actor_coords(3))
            if Tidus.is_turn():
                if memory.main.get_actor_coords(3)[2] < -150:
                    Tidus.attack()
                elif cheer_count < 2:  # Dial in 2-4 cheers later
                    cheer_count += 1
                    battle.main.cheer()
                else:
                    CurrentPlayer().attack()
            else:
                if memory.main.get_actor_coords(3)[2] < -150:
                    if Wakka.has_overdrive():
                        Wakka.overdrive()
                    else:
                        Wakka.attack()
                if Tidus.in_danger(230):
                    battle.main.use_hi_potion_character(Tidus, "l")
                elif Wakka.in_danger(230):
                    battle.main.use_hi_potion_character(Wakka, "l")
                else:
                    CurrentPlayer().attack()
        elif memory.main.special_text_open():
            xbox.tap_b()
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


# @battle.utils.speedup_decorator
def extractor():
    logger.info("Fight start: Extractor")
    FFXC.set_neutral()

    screen.await_turn()
    battle.main.tidus_haste("none")

    screen.await_turn()
    CurrentPlayer().attack()  # Wakka attack

    screen.await_turn()
    battle.main.tidus_haste("l", character=4)
    if game_vars.mrr_skip_val():
        extractor_mrr_skip()
        return

    cheer_count = 0
    while memory.main.battle_active():  # AKA end of battle screen
        # First determine if cheers are needed.
        if game_vars.get_l_strike() % 2 == 0 and cheer_count < 4:
            tidus_cheer = True
        elif game_vars.get_l_strike() % 2 == 1 and cheer_count < 1:
            tidus_cheer = True
        else:
            tidus_cheer = False
        # Then do the battle logic.
        if memory.main.special_text_open():
            xbox.tap_b()
        elif memory.main.turn_ready():
            if (
                screen.faint_check() > 0
                and memory.main.get_enemy_current_hp()[0] > 1100
            ):
                battle.main.revive()
            elif Tidus.is_turn():
                logger.debug(memory.main.get_actor_coords(3))
                if tidus_cheer:
                    cheer_count += 1
                    battle.main.cheer()
                elif (
                    memory.main.get_enemy_current_hp()[0] < 1400
                    and not screen.faint_check()
                    and Wakka.has_overdrive()
                ):
                    CurrentPlayer().defend()
                else:
                    CurrentPlayer().attack()
            else:
                if (
                    memory.main.get_enemy_current_hp()[0] < 1900
                    and Wakka.has_overdrive()
                ):
                    Wakka.overdrive()
                else:
                    CurrentPlayer().attack()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


# Process written by CrimsonInferno
@battle.utils.speedup_decorator
def spherimorph():
    logger.info("Fight start: Spherimorph")
    xbox.click_to_battle()

    FFXC.set_neutral()

    spell_num = 0
    # We know what the weakness is from RNG2 Manip
    if memory.main.get_char_weakness(20) == 1:
        spell_num = 4  # Ice
    elif memory.main.get_char_weakness(20) == 2:
        spell_num = 1  # Fire
    elif memory.main.get_char_weakness(20) == 4:
        spell_num = 3  # Water
    elif memory.main.get_char_weakness(20) == 8:
        spell_num = 2  # Thunder
    tidus_turns = 0
    yuna_turn = False
    kim_turn = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if game_vars.use_pause():
                memory.main.wait_frames(2)
            party_hp = memory.main.get_battle_hp()
            if Tidus.is_turn():
                if tidus_turns == 0:
                    Tidus.swap_battle_armor(ability=[0x8028])
                elif tidus_turns == 1:
                    CurrentPlayer().defend()
                else:
                    battle.main.buddy_swap(Rikku)
                tidus_turns += 1
            elif Yuna.is_turn():
                rikku_slot_num = memory.main.get_battle_char_slot(6)
                if rikku_slot_num < 3 and party_hp[rikku_slot_num] == 0:
                    battle.main.revive()
                    yuna_turn = True
                elif not yuna_turn:
                    CurrentPlayer().defend()
                    yuna_turn = True
                elif not battle.main.spheri_spell_item_ready():
                    if not Lulu.active():
                        battle.main.buddy_swap(Lulu)
                    elif not Rikku.active():
                        battle.main.buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                elif not Rikku.active():
                    battle.main.buddy_swap(Rikku)
                else:
                    CurrentPlayer().defend()
                    yuna_turn = True
            elif Kimahri.is_turn():
                rikku_slot_num = memory.main.get_battle_char_slot(6)
                if rikku_slot_num < 3 and party_hp[rikku_slot_num] == 0:
                    battle.main.revive()
                    kim_turn = True
                elif not kim_turn:
                    # logger.manip(
                    #    "RNG11 before Spherimorph: "
                    #    + f"{memory.main.rng_array_from_index(index=11, array_len=30)}"
                    # )
                    # logs.write_rng_track("RNG11 before Spherimorph")
                    # logs.write_rng_track(
                    #    memory.main.rng_array_from_index(index=11, array_len=30)
                    # )
                    # if memory.main.next_steal_rare(pre_advance=8):
                    # One each for Spherimorph, Negator, Crawler, and guados.
                    # Except we haven't learned Steal yet. That's no good.
                    #    _steal()
                    # else:
                    CurrentPlayer().defend()
                    kim_turn = True
                elif not Rikku.active():
                    battle.main.buddy_swap(Rikku)
                elif not Lulu.active():
                    battle.main.buddy_swap(Lulu)
                else:
                    CurrentPlayer().defend()
            elif Lulu.is_turn():
                if not battle.main.spheri_spell_item_ready():
                    if spell_num == 1:
                        CurrentPlayer().cast_black_magic_spell(3)
                    elif spell_num == 2:
                        CurrentPlayer().cast_black_magic_spell(2)
                    elif spell_num == 3:
                        CurrentPlayer().cast_black_magic_spell(1)
                    else:
                        CurrentPlayer().cast_black_magic_spell(0)
                    screen.await_turn()
                    if memory.main.get_char_weakness(20) == 1:
                        spell_num = 4  # Ice
                    elif memory.main.get_char_weakness(20) == 2:
                        spell_num = 1  # Fire
                    elif memory.main.get_char_weakness(20) == 4:
                        spell_num = 3  # Water
                    elif memory.main.get_char_weakness(20) == 8:
                        spell_num = 2  # Thunder
                elif not Rikku.active():
                    battle.main.buddy_swap(Rikku)
                else:
                    CurrentPlayer().defend()
            elif Rikku.is_turn():
                mix_dmg_rolls = sum(memory.main.rikku_mix_damage())
                logger.manip(f"Mix will do {mix_dmg_rolls} damage.")
                if mix_dmg_rolls < memory.main.get_enemy_current_hp()[0]:
                    logger.debug("Throwing Grenade because of damage rolls")
                    grenade_slot_num = memory.main.get_use_items_slot(35)
                    battle.main.use_item(grenade_slot_num, "none")
                elif not battle.main.spheri_spell_item_ready():
                    if not Lulu.active():
                        battle.main.buddy_swap(Lulu)
                    else:
                        CurrentPlayer().defend()
                elif yuna_turn and kim_turn:
                    logger.info("Starting Rikkus overdrive")
                    logger.manip("Full Damage Values:")
                    logger.manip(memory.main.rikku_mix_damage())
                    if spell_num == 1:
                        logger.debug("Creating Ice")
                        Rikku.overdrive("spherimorph1")
                    elif spell_num == 2:
                        logger.debug("Creating Water")
                        Rikku.overdrive("spherimorph2")
                    elif spell_num == 3:
                        logger.debug("Creating Thunder")
                        Rikku.overdrive("spherimorph3")
                    elif spell_num == 4:
                        logger.debug("Creating Fire")
                        Rikku.overdrive("spherimorph4")
                else:
                    CurrentPlayer().defend()

    if not game_vars.csr():
        xbox.skip_dialog(5)
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def crawler():
    logger.info("Starting battle with Crawler")
    xbox.click_to_battle()

    # if memory.main.next_steal_rare(pre_advance=5):
    #    # One each for two Negators, Crawler, and guados.
    #    battle.main.negator_with_steal()
    # else:
    tidus_turns = 0
    luluturns = 0
    kimahri_turns = 0

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        FFXC.set_neutral()
        if memory.main.turn_ready():
            if Tidus.is_turn():
                if tidus_turns == 0:
                    logger.debug("Swapping Tidus for Rikku")
                    battle.main.buddy_swap(Rikku)
                else:
                    if Rikku.is_dead():
                        battle.main.revive_target(target=6)
                    else:
                        Tidus.defend()

                tidus_turns += 1
            elif Rikku.is_turn():
                if Rikku.overdrive_percent(combat=True) < 100:
                    logger.debug("Using Lightning Marble")
                    lightningmarbleslot = memory.main.get_use_items_slot(30)
                    # if rikku_turns < 1:
                    #    battle.main.use_item(lightningmarbleslot, target=21)
                    # else:
                    battle.main.use_item(lightningmarbleslot, target=21)
                else:
                    logger.debug("Starting Rikkus overdrive")
                    battle.main.rikku_full_od("crawler")
            elif Kimahri.is_turn():
                if kimahri_turns >= 1 and game_vars.story_mode():
                    battle.main.buddy_swap(Lulu)
                    if Rikku.is_dead():
                        battle.main.revive(item_num=6)
                    else:
                        CurrentPlayer().defend()
                else:
                    lightningmarbleslot = memory.main.get_use_items_slot(30)
                    battle.main.use_item(lightningmarbleslot, target=21)
                    kimahri_turns += 1
            elif Lulu.is_turn():
                if luluturns == 0 and not game_vars.story_mode():
                    battle.main.revive_target(target=6)
                    luluturns += 1
                else:
                    battle.main.buddy_swap(Yuna)
                    if Rikku.is_dead():
                        if game_vars.story_mode():
                            battle.main.revive(item_num=6)
                        else:
                            battle.main.revive(item_num=7)
                    else:
                        CurrentPlayer().defend()
            elif Yuna.is_turn():
                battle.main.buddy_swap(Tidus)
                if Rikku.is_dead():
                    battle.main.revive_target(target=6)
                else:
                    Tidus.swap_battle_weapon(named_equip="brotherhood")
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()

    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def wendigo():
    logger.info("Starting battle with Wendigo")

    phase = 0
    yuna_ap = False
    guadosteal = False
    powerbreak = False
    powerbreakused = False
    usepowerbreak = False
    tidushealself = False
    tidus_max_hp = 1520
    tidushaste = False

    screen.await_turn()
    enemy_targets = rng_track.enemy_target_predictions()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            enemy_targets = rng_track.enemy_target_predictions()
            party_hp = memory.main.get_battle_hp()
            tidus_slot = memory.main.get_battle_char_slot(0)

            if party_hp[memory.main.get_battle_char_slot(0)] == 0:
                logger.debug("Tidus is dead")
                tidushaste = False
                powerbreak = True
                usepowerbreak = powerbreak and not powerbreakused

            if Yuna.is_turn():
                logger.debug("Yunas Turn")
                # If Yuna still needs AP:
                if not yuna_ap:
                    logger.debug("Yuna still needs AP")
                    # If both other characters are dead
                    # Mega-Phoenix if available, otherwise PD
                    if (
                        battle.main.wendigo_res_heal(
                            turn_char=Yuna,
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidus_max_hp,
                        )
                        == 0
                    ):
                        CurrentPlayer().swap_battle_weapon()
                    yuna_ap = True
                # If Yuna has had a turn swap for Kimahri, maybe can charge up.
                else:
                    if not Kimahri.active():
                        logger.debug("Swapping to Kimahri")
                        battle.main.buddy_swap(Kimahri)
                    elif not Rikku.active():
                        battle.main.buddy_swap(Rikku)
                    else:
                        CurrentPlayer().swap_battle_weapon()
            elif Tidus.is_turn():
                if not tidushaste:
                    logger.debug("Tidus Haste self")
                    battle.main.tidus_haste("none")
                    tidushaste = True
                elif phase == 0:
                    logger.debug("Switch to Brotherhood")
                    Tidus.swap_battle_weapon(named_equip="brotherhood")
                    phase += 1
                elif phase == 1:
                    logger.debug("Attack top Guado")
                    CurrentPlayer().attack(target_id=22, direction_hint="d")
                    phase += 1
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and screen.faint_check() == 2
                ):
                    logger.debug("2 Characters are dead")
                    tidushealself = True
                    if memory.main.get_throw_items_slot(7) < 255:
                        battle.main.revive_all()
                    elif memory.main.get_throw_items_slot(6) < 255:
                        battle.main.revive()
                # elif (
                #    memory.main.get_enemy_current_hp()[1] < 6000
                #    and memory.main.get_overdrive_battle(0) == 100
                #    and not game_vars.skip_kilika_luck()
                # ):
                #    Tidus.overdrive(direction="left", character=21)
                elif tidushealself:
                    if party_hp[memory.main.get_battle_char_slot(0)] < tidus_max_hp:
                        logger.debug(
                            "Tidus just used Phoenix Down / Mega Phoenix "
                            + "so needs to heal himself"
                        )
                        if battle.main.fullheal(target=0, direction="l") == 0:
                            if screen.faint_check():
                                logger.debug(
                                    "No healing items so revive someone instead"
                                )
                                battle.main.revive()
                            else:
                                logger.debug("No healing items so just go face")
                                CurrentPlayer().attack(target_id=21, direction_hint="l")
                    else:
                        logger.debug("No need to heal. Ver 1")
                        CurrentPlayer().attack(target_id=21, direction_hint="l")
                    tidushealself = False
                else:
                    logger.debug("No need to heal. Ver 2")
                    CurrentPlayer().attack(target_id=21, direction_hint="l")
                memory.main.wait_frames(30 * 0.2)
            elif Rikku.is_turn():
                if phase == 2:
                    phase += 1
                    lightcurtainslot = memory.main.get_use_items_slot(57)
                    if lightcurtainslot < 255:
                        logger.debug("Using Light Curtain on Tidus")
                        battle.main.use_item(lightcurtainslot, target=0)
                    else:
                        logger.debug("No Light Curtain")
                        logger.debug("Swapping to Auron to Power Break")
                        battle.main.buddy_swap(Auron)  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                # elif memory.main.get_enemy_current_hp()[1] < stop_healing:
                #    CurrentPlayer().defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turn_char=Rikku,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidus_max_hp,
                    )
                    == 0
                ):
                    if (
                        not guadosteal
                        and memory.main.get_enemy_current_hp().count(0) != 2
                    ):
                        battle.main.steal()
                        guadosteal = True
                    # elif (
                    #    memory.main.get_enemy_current_hp().count(0) == 2
                    #    and not 5 in memory.main.get_active_battle_formation()
                    # ):
                    #    buddy_swap(Lulu)
                    else:
                        CurrentPlayer().defend()
            elif Auron.is_turn():
                if usepowerbreak:
                    logger.debug("Using Power Break")
                    battle.main.use_skill(position=0, target=21)
                    powerbreakused = True
                    usepowerbreak = False
                # elif (
                #    memory.main.get_enemy_current_hp()[1] < stop_healing
                #    and memory.main.get_battle_hp()[tidus_slot] != 0
                # ):
                #    CurrentPlayer().defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turn_char=Auron,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidus_max_hp,
                    )
                    == 0
                ):
                    if 3 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap(Kimahri)
                    elif 6 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap(Rikku)
                    else:
                        battle.main.buddy_swap(Yuna)

            elif Lulu.is_turn():
                if 3 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap(Kimahri)
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap(Rikku)
                else:
                    battle.main.buddy_swap(Yuna)
                # if (
                #    battle.main.wendigo_res_heal(
                #        turn_char=Lulu,
                #        use_power_break=usepowerbreak,
                #        tidus_max_hp=tidus_max_hp,
                #    )
                #    == 0
                # ):
                #    CurrentPlayer().swap_battle_weapon()
            else:
                if (
                    usepowerbreak
                    and not powerbreakused
                    and 2 not in memory.main.get_active_battle_formation()
                ):
                    logger.debug("Swapping to Auron to Power Break")
                    battle.main.buddy_swap(Auron)
                # if (
                #    memory.main.get_enemy_current_hp()[1] < stop_healing
                #    and memory.main.get_battle_hp()[tidus_slot] != 0
                # ):
                #    logger.debug("End of battle, no need to heal.")
                #    CurrentPlayer().defend()
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and memory.main.get_battle_hp()[tidus_slot] != 0
                ):
                    if (
                        battle.main.wendigo_res_heal(
                            turn_char=memory.main.get_battle_char_turn(),
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidus_max_hp,
                        )
                        == 0
                    ):
                        CurrentPlayer().defend()
                else:
                    CurrentPlayer().defend()

    if memory.main.game_over():
        return False
    if game_vars.god_mode():
        rng_track.force_preempt()
    return True


def evrae():
    # First to determine Evrae's target attacks, and if we want to steal.
    max_steals = 2
    remaining_steals = 99
    targets = rng_track.evrae_targets()
    if 2 in targets:
        max_steals -= 1
        if targets[0] == 1:
            max_steals -= 1
        elif 0 in targets:
            max_steals += 1
    elif targets[0] == 1:
        max_steals -= 1
    nea_drop_counts = rng_track.guards_to_calm_equip_drop_count(
        guard_battle_num=0,
        pre_Evrae=True
    )
    
    # Now to determine best number of steals
    if (
        nea_drop_counts[2] <= nea_drop_counts[1] and
        nea_drop_counts[2] <= nea_drop_counts[0]
    ):
        remaining_steals = min(2, max_steals)
    elif nea_drop_counts[1] <= nea_drop_counts[0]:
        remaining_steals = min(1, max_steals)
    else:
        remaining_steals = 0
    rng_track.guards_to_calm_equip_drop_count(
        guard_battle_num=0,
        pre_Evrae=True,
        report_num=remaining_steals
    )
    logger.manip(
        "Evrae target order, where 0 is Tidus, 1 is Kimahri, and 2 is Rikku:"
    )
    logger.manip(targets)
    logger.manip(f"Steals - Max:{max_steals} - Best drops: {remaining_steals}")
    logger.manip(f"Drops from here to calm lands (includes Evrae): {nea_drop_counts}")
        
    # With decisions out of the way, time to start the battle.
    logger.info("Starting battle: Evrae")
    tidus_prep = 0
    tidus_attacks = 0
    rikku_turns = 0
    kimahri_turns = 0
    lunar_curtain = False
    FFXC.set_neutral()
    # This gets us past the tutorial and all the dialog.
    if game_vars.story_mode() or not game_vars.csr():
        memory.main.click_to_diag_progress(4)
        memory.main.wait_seconds(13)
        xbox.tap_confirm()
        memory.main.wait_seconds(2)
        xbox.tap_confirm()
        xbox.click_to_battle()
    else:
        xbox.click_to_battle()
    
    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.debug(f"Tidus prep turns: {tidus_prep}")
            logger.manip(memory.main.get_enemy_current_hp())
            if Tidus.is_turn():  # Terra skip strat
                logger.debug("Registering Tidus' turn")
                if tidus_prep == 0:
                    tidus_prep = 1
                    battle.main.tidus_haste("none")
                elif tidus_prep == 1:
                    tidus_prep += 1
                    battle.main.cheer()
                elif tidus_prep == 2 and memory.main.get_next_turn() == 0:
                    Tidus.swap_battle_armor(ability=[0x8028])
                elif tidus_prep == 4:
                    tidus_prep += 1
                    battle.main.cheer()
                elif memory.main.get_enemy_current_hp()[0] <= 9999:
                    tidus_attacks += 1
                    Tidus.overdrive()
                else:
                    tidus_prep += 1
                    tidus_attacks += 1
                    CurrentPlayer().attack()
            elif Rikku.is_turn():
                logger.debug("Registering Rikkus turn")
                if rikku_turns == 0:
                    rikku_turns += 1
                    logger.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Evrae")
                elif not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif (
                    memory.main.get_battle_hp()[memory.main.get_battle_char_slot(0)] < 1520 and 
                    (
                        not game_vars.get_blitz_win() or
                        (
                            targets[1] == 0 and
                            targets[0] == 0 and
                            tidus_attacks < 3
                        )
                    )
                ):
                    logger.debug("Rikku should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                elif remaining_steals != 0:
                    remaining_steals -= 1
                    logger.manip(f"Remaining steals: {remaining_steals}")
                    battle.main.steal()
                else:
                    CurrentPlayer().defend()
                    logger.manip(f"Remaining steals: {remaining_steals}")
            elif Kimahri.is_turn():
                logger.debug("Registering Kimahri's turn")
                if not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif (
                    memory.main.get_battle_hp()[memory.main.get_battle_char_slot(0)] < 1520 and 
                    (
                        not game_vars.get_blitz_win() or
                        (
                            targets[1] == 0 and
                            targets[0] == 0 and
                            tidus_attacks < 3
                        )
                    )
                ):
                    logger.debug("Kimahri should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                elif remaining_steals != 0:
                    remaining_steals -= 1
                    logger.manip(f"Remaining steals: {remaining_steals}")
                    battle.main.steal()
                elif 1 in targets:
                    CurrentPlayer().attack(target_id=3)
                    logger.manip(f"Remaining steals: {remaining_steals}")
                else:
                    CurrentPlayer().defend()
                    logger.manip(f"Remaining steals: {remaining_steals}")
    if memory.main.game_over():
        return False
    else:
        return True

# Process written by CrimsonInferno
@battle.utils.speedup_decorator
def evrae_trueRNG():
    logger.info("Starting battle: Evrae")
    tidus_prep = 0
    tidus_attacks = 0
    rikku_turns = 0
    kimahri_turns = 0
    lunar_curtain = False
    if memory.main.rng_seed() == 31:
        steal_count = 2
    else:
        steal_count = 0
    FFXC.set_neutral()
    # This gets us past the tutorial and all the dialog.
    xbox.click_to_battle()

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            logger.debug(f"Tidus prep turns: {tidus_prep}")
            if Tidus.is_turn():  # Terra skip strat
                logger.debug("Registering Tidus' turn")
                if tidus_prep == 0:
                    tidus_prep = 1
                    battle.main.tidus_haste("none")
                elif tidus_prep == 1:
                    tidus_prep += 1
                    battle.main.cheer()
                elif tidus_prep == 2 and memory.main.get_next_turn() == 0:
                    Tidus.swap_battle_armor(ability=[0x8028])
                elif tidus_prep == 4:
                    tidus_prep += 1
                    battle.main.cheer()
                elif memory.main.get_enemy_current_hp()[0] <= 9999:
                    tidus_attacks += 1
                    Tidus.overdrive()
                else:
                    tidus_prep += 1
                    tidus_attacks += 1
                    CurrentPlayer().attack()
            elif Rikku.is_turn():
                logger.debug("Registering Rikkus turn")
                if rikku_turns == 0:
                    rikku_turns += 1
                    logger.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Evrae")
                elif not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidus_attacks < 3 or not game_vars.get_blitz_win()):
                    logger.debug("Rikku should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                else:
                    battle.main.steal()
                    steal_count += 1
                """
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throw_slot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throw_slot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throw_slot = memory.main.get_use_items_slot(27)
                    else:
                        throw_slot = memory.main.get_use_items_slot(30)
                    if throw_slot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throw_slot)
                """
            elif Kimahri.is_turn():
                logger.debug("Registering Kimahri's turn")
                if not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidus_attacks < 3 or not game_vars.get_blitz_win()):
                    logger.debug("Kimahri should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="u") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                else:
                    battle.main.steal()
                    steal_count += 1
                """
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throw_slot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throw_slot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throw_slot = memory.main.get_use_items_slot(27)
                    else:
                        throw_slot = memory.main.get_use_items_slot(30)
                    if throw_slot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throw_slot)
                """
        elif memory.main.diag_skip_possible():
            xbox.tap_b()

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            if memory.main.menu_open():
                xbox.tap_b()
        xbox.skip_scene_spec()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def isaaru():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() < 258:
        game_vars.add_rescue_count()

    logger.info("Starting battle: Isaaru")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Yuna.is_turn():
                if memory.main.get_encounter_id() in [257, 260]:
                    battle.main.aeon_summon(2)  # Summon Ixion for Bahamut
                else:
                    battle.main.aeon_summon(4)  # Summon Bahamut for other aeons
            elif Auron.is_turn():
                # Can only occur if ambushed on a Larvae fight
                if Yuna.is_dead():
                    if memory.main.get_throw_items_slot(6) < 250:
                        revive_target(item_num=6, target=1)
                    if memory.main.get_throw_items_slot(7) < 250:
                        revive(item_num=7)
                    else:
                        # No good options. Wait for reset.
                        Auron.defend()
                else:
                    Auron.defend()
            else:
                CurrentPlayer().attack()  # Aeon turn
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    
    if memory.main.game_over():
        logger.warning("GAME OVER, FORCE RETURN")
        return False
    while not memory.main.battle_wrap_up_active():
        if memory.main.battle_active():
            return True
    FFXC.set_confirm()
    while memory.main.battle_wrap_up_active():
        if memory.main.battle_active():
            return True
    FFXC.release_confirm()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return True


@battle.utils.speedup_decorator
def evrae_altana():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() != 266:
        logger.info("Not Evrae this time.")
        battle.main.flee_all()
    else:
        logger.info("Evrae Altana fight start")
        # Come back to this. Maybe up NEA manip currently, so needs review.
        #gems = check_gems()
        #if gems != 0:
        #    # One gem is enough to justify stealing in Calm Lands.
        #    logger.manip(f"We have {gems} gems already. No need to steal.")
        #elif not memory.main.next_steal_rare():
        #    logger.manip(f"We have {gems} gems, and the next steal is not rare.")
        #    evrae_altana_steal()
        #else:
        #    logger.debug(f"Next steal will crit, do not steal. {gems}")
        thrown_item = False
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                if memory.main.get_item_slot(18) != 255 and not thrown_item:
                    battle.main._use_healing_item(item_id=18)
                    thrown_item = True
                elif memory.main.get_item_slot(16) != 255 and not thrown_item:
                    battle.main._use_healing_item(item_id=16)
                    thrown_item = True
                elif memory.main.get_item_slot(17) != 255 and not thrown_item:
                    battle.main._use_healing_item(item_id=17)
                    thrown_item = True
                else:
                    battle.main.altana_heal()
    wrap_up()
    if game_vars.god_mode():
        rng_track.force_preempt()


def evrae_altana_steal():
    logger.debug("Steal logic, we will get two gems")
    haste_count = False
    steal_count = False
    while memory.main.get_item_slot(34) == 255:
        if memory.main.turn_ready():
            if Tidus.is_turn() and not haste_count:
                battle.main.tidus_haste(direction="l", character=Rikku)
                haste_count = True
            elif Rikku.is_turn() and not steal_count:
                memory.main.next_steal_rare()
                battle.main._steal()
                steal_count = True
            else:
                CurrentPlayer().defend()
    logger.debug("End of steal logic. Back to regular.")
    if game_vars.god_mode():
        rng_track.force_preempt()


def highbridge_attack():
    if memory.main.get_enemy_current_hp().count(0) == 1:
        return False
    elif memory.main.get_encounter_id() == 271:
        CurrentPlayer().attack(target_id=21, direction_hint="l")
    else:
        CurrentPlayer().attack()
    return True


@battle.utils.speedup_decorator
def seymour_natus(delay_grid:bool):
    while not memory.main.turn_ready():
        pass  # This is so we don't trigger the wrong battle.
    aeon_summoned = False
    if game_vars.story_mode() and memory.main.get_encounter_id() != 272:
        if memory.main.battle_type() == 2:
            # Ambushed
            flee_all()
        else:
            battle.main.calm_impulse()  # Repurposed, does what we want already.
        wrap_up()
    elif memory.main.get_encounter_id() == 272:  # Seymour Natus
        logger.info("Seymour Natus engaged")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    if memory.main.get_lulu_slvl() < 35 or game_vars.nemesis():
                        battle.main.buddy_swap(Lulu)
                        screen.await_turn()
                        CurrentPlayer().swap_battle_weapon()
                    elif aeon_summoned:
                        battle.main.tidus_haste("d", character=1)
                    else:
                        CurrentPlayer().attack()
                elif Lulu.is_turn():
                    battle.main.buddy_swap(Tidus)
                    screen.await_turn()
                    xbox.tap_up()
                    CurrentPlayer().attack()
                elif Yuna.is_turn():
                    if not aeon_summoned:
                        battle.main.aeon_summon(4)
                        aeon_summoned = True
                    else:
                        CurrentPlayer().attack()
                        #battle.main.aeon_summon(2)
                elif screen.turn_aeon():
                    Bahamut.attack()
                    xbox.skip_dialog(3)  # Finishes the fight.
                else:
                    CurrentPlayer().defend()
        logger.warning("Natus complete, returning 1")
        return 1
    elif (
        memory.main.next_chance_rng_10(30) == 0
        and memory.main.next_chance_rng_12() == 1
    ):
        steal_occurred = False
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                battle.main.flee_all()
            elif memory.main.turn_ready():
                if Rikku.is_turn() and not steal_occurred:
                    battle.main.steal()
                    steal_occurred = True
                elif not Rikku.active() and not steal_occurred:
                    battle.main.buddy_swap(Rikku)
                elif Tidus.is_turn() or Yuna.is_turn():
                    if not highbridge_attack():
                        battle.main.flee_all()
                elif not Tidus.active():
                    battle.main.buddy_swap(Tidus)
                elif not Yuna.active():
                    battle.main.buddy_swap(Yuna)
                else:
                    CurrentPlayer().defend()
    elif memory.main.get_encounter_id() == 270:  # YAT-63 x2
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                battle.main.flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        battle.main.flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()
    elif memory.main.get_encounter_id() == 269:  # YAT-63 with two guard guys
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                battle.main.flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        battle.main.flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()
    elif memory.main.get_encounter_id() == 271:  # one YAT-63, two YAT-99
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                battle.main.flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        battle.main.flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()

    if game_vars.god_mode():
        rng_track.force_preempt()
    return 0


@battle.utils.speedup_decorator
def biran_yenke():
    logger.info("Starting battle with Biran & Yenke")
    xbox.click_to_battle()
    battle.main.steal()

    # Nemesis logic
    if game_vars.nemesis():
        screen.await_turn()
        battle.main.steal_right()

    screen.await_turn()
    if game_vars.mrr_skip_val() == False:
        CurrentPlayer().defend()
        screen.await_turn()
    
    if game_vars.god_mode():
        # Leveraging this variable to force preferable results.
        drop1 = drop_rare(drop_num=1)
        drop2 = drop_rare(drop_num=2)
        logger.debug(f"==== B&Y Drops: {drop1} : {drop2}")
        while not (drop1 == True and drop2 == True):
            memory.main.advance_rng_index(11)
            drop1 = drop_rare(drop_num=1)
            drop2 = drop_rare(drop_num=2)
            logger.debug(f"==== B&Y Drops: {drop1} : {drop2}")
    
    gem_slot = memory.main.get_use_items_slot(34)
    if gem_slot == 255:
        gem_slot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gem_slot, "none")
    
    xbox.click_to_battle()
    gem_slot = memory.main.get_use_items_slot(34)
    if gem_slot == 255:
        gem_slot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gem_slot, "none")
    
    while not memory.main.user_control():
        if game_vars.story_mode():
            if memory.main.battle_wrap_up_active():
                FFXC.set_confirm()
            else:
                FFXC.release_confirm()
        else:
            xbox.tap_b()

    ret_slot = memory.main.get_item_slot(96)  # Return sphere
    friend_slot = memory.main.get_item_slot(97)  # Friend sphere

    if friend_slot == 255:  # Four return sphere method.
        logger.debug("Double return sphere drops.")
        write_returns(4)
        end_game_version = 4
    elif ret_slot == 255:
        logger.warning("Double friend sphere, effective game over. :( ")
        write_returns(0)
        end_game_version = 3
    else:
        logger.debug("Split items between friend and return spheres.")
        write_returns(2)
        end_game_version = 1

    game_vars.end_game_version_set(end_game_version)
    if game_vars.god_mode():
        rng_track.force_preempt()


def seymour_flux_battle_site_version():
    aeon_order = [4,0,1,3,2]
    aeon_summoned = 0
    stage = 1
    yuna_haste = False


    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                logger.debug(f"Yunas turn. Stage: {stage}")
                if stage == 1:
                    Yuna.attack()
                    stage += 1
                elif stage == 2:
                    if memory.main.who_goes_first_after_current_turn([1,20]) == 1:
                        Yuna.attack()
                    else:
                        battle.main.aeon_summon(aeon_order[aeon_summoned])
                        aeon_summoned += 1
                        if aeon_summoned == len(aeon_order):
                            stage += 1
                else:
                    Yuna.attack()
            elif Tidus.is_turn():
                if not yuna_haste:
                    battle.main.tidus_haste("down", character=1)
                    yuna_haste = True
                else:
                    CurrentPlayer().attack()
            elif screen.turn_aeon():
                #if aeon_order[aeon_summoned] == 2:
                #    Bahamut.unique()  # This might not work. Supposed to dispell
                #else:
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
    wrap_up()



@battle.utils.speedup_decorator
def seymour_flux():
    if game_vars.mrr_skip_val() == False:
        seymour_flux_battle_site_version()
        return
    stage = 1
    logger.info("Start: Seymour Flux battle")
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    logger.debug(f"Next Aeon Crit: {bahamut_crit}")
    yuna_xp = memory.main.get_slvl_yuna()
    
    xbox.click_to_battle()
    if game_vars.end_game_version() == 3:
        bahamut_summoned = False
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    battle.main.buddy_swap(Yuna)
                elif Yuna.is_turn():
                    if not bahamut_summoned:
                        battle.main.aeon_summon(4)
                        bahamut_summoned = True
                    else:
                        CurrentPlayer().attack()
                elif screen.turn_aeon():
                    CurrentPlayer().attack()
                elif screen.faint_check() >= 1:
                    battle.main.revive()
                else:
                    CurrentPlayer().defend()
    elif bahamut_crit == 2:
        bahamut_summoned = False
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_aeon():
                    CurrentPlayer().attack()
                elif bahamut_summoned:
                    if Yuna.is_turn() or Tidus.is_turn():
                        CurrentPlayer().attack()
                    else:
                        CurrentPlayer().defend()
                else:
                    if Yuna.is_turn():
                        battle.main.aeon_summon(4)
                        bahamut_summoned = True
                    elif Tidus.is_turn():
                        CurrentPlayer().attack()
                    else:
                        CurrentPlayer().defend()
    elif game_vars.end_game_version() in [1,2]:
        bahamut_summoned = False
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                if Yuna.is_turn():
                    logger.debug(f"Yunas turn. Stage: {stage}")
                    if stage == 1:
                        CurrentPlayer().attack()
                        stage += 1
                    elif stage == 2:
                        battle.main.aeon_summon(4)
                        stage += 1
                    else:
                        CurrentPlayer().attack()
                elif Tidus.is_turn():
                    if stage <= 2:
                        battle.main.tidus_haste("down", character=1)
                    else:
                        CurrentPlayer().attack()
                elif screen.turn_aeon():
                    Bahamut.unique()
                else:
                    CurrentPlayer().defend()
    else:
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                last_hp = memory.main.get_enemy_current_hp()[0]
                logger.debug("Last HP")
                if Yuna.is_turn():
                    logger.debug(f"Yunas turn. Stage: {stage}")
                    if stage == 1:
                        CurrentPlayer().attack()
                        stage += 1
                    elif stage == 2:
                        battle.main.aeon_summon(4)
                        CurrentPlayer().attack()
                        stage += 1
                    else:
                        CurrentPlayer().attack()
                elif Tidus.is_turn():
                    logger.debug(f"Tidus' turn. Stage: {stage}")
                    if stage < 3:
                        battle.main.tidus_haste("down", character=1)
                    elif last_hp > 3500:
                        CurrentPlayer().attack()
                    else:
                        CurrentPlayer().defend()
                elif Auron.is_turn():
                    logger.debug("Auron's turn. Swap for Rikku and overdrive.")
                    battle.main.buddy_swap(Rikku)
                    if memory.main.get_overdrive_battle(6) == 100:
                        logger.debug("Rikku overdrive")
                        battle.main.rikku_full_od("Flux")
                else:
                    logger.debug("Non-critical turn. Defending.")
                    CurrentPlayer().defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.click_to_control()
    if memory.main.get_slvl_yuna() - yuna_xp == 15000:
        game_vars.flux_overkill_success()
    logger.info("-----------------------------")
    logger.info(f"Flux Overkill: {game_vars.flux_overkill()}")
    logger.info("Seymour Flux battle complete.")
    logger.info("-----------------------------")
    if game_vars.god_mode():
        rng_track.force_preempt()


def s_keeper_bahamut_crit() -> int:
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    logger.debug(f"Next Aeon Crit: {bahamut_crit}")
    return bahamut_crit


@battle.utils.speedup_decorator
def s_keeper():
    xbox.click_to_battle()
    logger.info("Start of Sanctuary Keeper fight")
    s_keeper_bahamut_crit()
    xbox.click_to_battle()
    bahamut_crit = s_keeper_bahamut_crit()
    if bahamut_crit == 2 or bahamut_crit == 7:
        while memory.main.battle_active():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_aeon():
                    CurrentPlayer().attack()
                elif Yuna.is_turn():
                    battle.main.aeon_summon(4)
                else:
                    CurrentPlayer().defend()
    elif game_vars.end_game_version() == 3 and game_vars.get_blitz_win():
        while memory.main.battle_active():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if Yuna.is_turn():
                    battle.main.aeon_summon(4)
                elif screen.turn_aeon():
                    CurrentPlayer().attack()
                else:
                    CurrentPlayer().defend()
    else:
        armor_break = False
        while memory.main.battle_active():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if Tidus.is_turn():
                    battle.main.use_skill(0)
                    armor_break = True
                elif Yuna.is_turn():
                    if armor_break:
                        battle.main.aeon_summon(4)
                    else:
                        CurrentPlayer().defend()
                elif screen.turn_aeon():
                    CurrentPlayer().attack()
                else:
                    CurrentPlayer().defend()
    if memory.main.game_over():
        return False
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return True


@battle.utils.speedup_decorator
def yunalesca():
    xbox.click_to_battle()
    battle.main.aeon_summon(4)  # Summon Bahamut and attack.
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not Bahamut.is_turn():
                logger.error("Bahamut is down! This is a fail state!")
                seed = str(game_vars.rng_seed_num())
                avina_memory.add_to_memory(seed=seed, key="zan_luck", value="False")
                return False
            else:
                CurrentPlayer().attack()
    wrap_up()
    return True


@battle.utils.speedup_decorator
def omnis():
    logger.info("Fight start: Seymour Omnis")
    xbox.click_to_battle()
    CurrentPlayer().defend()  # Yuna defends
    rikku_in = False
    backup_cure = False
    summoned = False

    while memory.main.get_enemy_max_hp()[0] == memory.main.get_enemy_current_hp()[0]:
        if memory.main.turn_ready():
            if Tidus.is_turn():
                battle.main.use_skill(0)
            elif Auron.is_turn():
                battle.main.buddy_swap(Rikku)
                battle.main.rikku_full_od(battle="omnis")
                rikku_in = True
            elif Yuna.is_turn() and rikku_in:
                if not backup_cure:
                    battle.main.yuna_cure_omnis()
                    backup_cure = True
                else:
                    Yuna.swap_battle_weapon(ability=[0x8001])
            else:
                CurrentPlayer().defend()

    logger.debug("Ready for aeon.")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            logger.debug(f"Character turn: {memory.main.get_battle_char_turn()}")
            if Yuna.is_turn():
                if not summoned:
                    battle.main.aeon_summon(4)
                    summoned = True
                else:
                    battle.main.attack()
            elif screen.turn_aeon():
                CurrentPlayer().attack()
            elif Tidus.is_turn():
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            logger.debug("Skipping dialog maybe?")
            xbox.tap_b()
    if memory.main.game_over():
        return False
    else:
        logger.debug("Should be done now.")
        memory.main.click_to_control()
        if game_vars.god_mode():
            rng_track.force_preempt()
        return True


def bfa():
    if memory.main.get_gil_value() < 150000:
        swag_mode = True
    else:
        swag_mode = game_vars.yu_yevon_swag()
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()

    if game_vars.story_mode():
        while not memory.main.turn_ready():
            pass
    else:
        xbox.click_to_battle()
    battle.main.buddy_swap(Rikku)
    if memory.main.overdrive_state()[6] == 100:
        battle.main.rikku_full_od("bfa")
    else:
        battle.main.use_skill(0)

    screen.await_turn()
    while memory.main.main_battle_menu():
        xbox.tap_left()
    while memory.main.battle_cursor_2() != 1:
        xbox.tap_down()
    while memory.main.other_battle_menu():
        xbox.tap_b()
    battle.main.tap_targeting()
    battle.main.buddy_swap(Yuna)
    battle.main.aeon_summon(4)

    # Bahamut finishes the battle.
    while memory.main.battle_active():
        if memory.main.turn_ready():
            CurrentPlayer().attack()
        else:
            xbox.tap_confirm()
    if memory.main.game_over():
        logger.error("Failure on BFA!")
        seed = game_vars.rng_seed_num()
        avina_memory.add_to_memory(seed=seed, key="zan_luck", value="False")

    # Skip the cutscene
    logger.info("BFA down. Ready for Aeons")
    while not memory.main.get_map() == 326:
        if game_vars.story_mode():
            pass
        else:
            xbox.tap_confirm()

    while memory.main.get_story_progress() < 3380:
        if memory.main.battle_active():
            if memory.main.turn_ready():
                if Yuna.is_turn():
                    while memory.main.battle_menu_cursor() != 20:
                        if memory.main.battle_menu_cursor() in [22, 1]:
                            xbox.tap_up()
                        else:
                            xbox.tap_down()
                    while memory.main.main_battle_menu():
                        xbox.menu_b()
                    while memory.main.other_battle_menu():
                        xbox.menu_b()
                    logger.info(f"Enemy max hp: {memory.main.get_enemy_max_hp()}")
                    aeon_hp = memory.main.get_enemy_max_hp()[0]
                    if swag_mode or aeon_hp % 1000 == 0:
                        use_gil = aeon_hp * 10
                    else:
                        use_gil = (int(aeon_hp / 1000) + 1) * 10000
                    logger.info(f"#### USING GIL #### {use_gil}")
                    battle.main.calculate_spare_change_movement(use_gil)
                    while memory.main.spare_change_open():
                        xbox.menu_b()
                    xbox.tap_b()
                    xbox.tap_b()
                    xbox.tap_b()
                    xbox.tap_b()
                elif memory.main.turn_ready():
                    CurrentPlayer().defend()
            else:
                FFXC.set_neutral()
        else:
            FFXC.set_neutral()
            if memory.main.cutscene_skip_possible():
                xbox.skip_scene()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.diag_progress_flag() == 10 and memory.main.diag_skip_possible():
                xbox.tap_confirm()
    
    '''
    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            if not game_vars.story_mode():
                xbox.tap_b()
        xbox.skip_scene()

    while memory.main.get_story_progress() < 3380:
        if memory.main.turn_ready():
            encounter_id = memory.main.get_encounter_id()
            logger.info(f"Battle engaged. Encounter id: {encounter_id}")
            if Yuna.is_turn():
                while memory.main.battle_menu_cursor() != 20:
                    if memory.main.battle_menu_cursor() in [22, 1]:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                while memory.main.main_battle_menu():
                    xbox.tap_b()
                while memory.main.other_battle_menu():
                    xbox.tap_b()
                logger.info(f"Enemy max hp: {memory.main.get_enemy_max_hp()}")
                aeon_hp = memory.main.get_enemy_max_hp()[0]
                if swag_mode or aeon_hp % 1000 == 0:
                    use_gil = aeon_hp * 10
                else:
                    use_gil = (int(aeon_hp / 1000) + 1) * 10000
                logger.info(f"#### USING GIL #### {use_gil}")
                battle.main.calculate_spare_change_movement(use_gil)
                while memory.main.spare_change_open():
                    xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
            else:
                CurrentPlayer().defend()
        elif not memory.main.battle_active():
            xbox.tap_b()
    '''
    logger.debug("End of aeons")
    return True


def yu_yevon():
    logger.info("Ready for Yu Yevon.")
    screen.await_turn()  # No need for skipping dialog
    logger.info("Awww such a sad final boss!")
    zombie_attack = False
    za_char = game_vars.zombie_weapon()
    weap_swap = False
    while memory.main.get_story_progress() < 3400:
        if memory.main.turn_ready():
            logger.debug(f"za_char: {za_char}")
            logger.debug(f"zombie_attack: {zombie_attack}")
            logger.debug(f"weap_swap: {weap_swap}")
            if zombie_attack is True:  # Throw P.down to end game
                item_num = battle.main.yu_yevon_item()
                if item_num == 99:
                    logger.warning("No phoenix downs!!! Panic!!!")
                    if memory.main.get_enemy_current_hp()[0] < 9999 and Yuna.is_turn():
                        Yuna.attack()
                    elif memory.main.get_enemy_current_hp()[0] < 6000 and Tidus.is_turn() and Tidus.has_overdrive():
                        Tidus.overdrive()
                    else:
                        CurrentPlayer().defend()
                elif CurrentPlayer().raw_id() == za_char:
                    CurrentPlayer().attack()
                else:
                    while memory.main.battle_menu_cursor() != 1:
                        xbox.tap_down()
                    while memory.main.main_battle_menu():
                        xbox.tap_b()
                    item_pos = memory.main.get_throw_items_slot(item_num)
                    battle.main._navigate_to_position(item_pos)
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    while not memory.main.enemy_targetted():
                        xbox.tap_up()
                    battle.main.tap_targeting()
                logger.info("Phoenix Down on Yu Yevon. Good game.")
            elif za_char == 1:  # Yuna zombie weapon
                if Yuna.is_turn():
                    if not weap_swap:
                        CurrentPlayer().swap_battle_weapon(ability=[0x8032])
                        weap_swap = True
                    else:
                        CurrentPlayer().attack()
                        zombie_attack = True
                elif weap_swap and Tidus.is_turn():
                    CurrentPlayer().swap_battle_weapon()
                else:
                    CurrentPlayer().defend()
            elif za_char == 0:  # Tidus zombie weapon
                if Tidus.is_turn():
                    if not weap_swap:
                        CurrentPlayer().swap_battle_weapon(ability=[0x8032])
                        weap_swap = True
                    else:
                        CurrentPlayer().attack()
                        zombie_attack = True
                else:
                    CurrentPlayer().defend()
            elif za_char == 2:  # Auron logic:
                if Yuna.is_turn():
                    battle.main.buddy_swap(Auron)
                elif Auron.is_turn():
                    if not weap_swap:
                        CurrentPlayer().swap_battle_weapon(ability=[0x8032])
                        weap_swap = True
                    else:
                        CurrentPlayer().attack()
                        zombie_attack = True
                else:
                    CurrentPlayer().defend()
            elif za_char == 6:  # Rikku logic:
                if Yuna.is_turn() and not weap_swap:
                    # Piggy back off the weap_swap function
                    CurrentPlayer().defend()
                    weap_swap = True  # Just to piggy back for turn manip.
                elif Yuna.is_turn():
                    CurrentPlayer().swap_battle_weapon()
                elif Tidus.is_turn():
                    battle.main.tidus_haste("r", character=6)
                elif Rikku.is_turn():
                    CurrentPlayer().attack()
                    zombie_attack = True
                else:
                    CurrentPlayer().defend()
            elif za_char == 255:
                if Tidus.is_turn():
                    # Tidus to use Zombie Strike ability
                    if memory.main.get_tidus_mp() > 10:
                        battle.main.use_skill(0)
                    else:
                        CurrentPlayer().attack()
                    zombie_attack = True
                else:
                    # Non-Tidus char to defend so Tidus can use Zombie Strike ability
                    CurrentPlayer().defend()
            else:
                if memory.main.get_battle_char_turn() == za_char:
                    CurrentPlayer().attack()
                    zombie_attack = True
                elif memory.main.get_battle_char_slot(za_char) >= 3:
                    battle.main.buddy_swap_char(za_char)
                elif Tidus.is_turn():
                    battle.main.tidus_haste("l", character=za_char)
                else:
                    CurrentPlayer().defend()
        elif not memory.main.battle_active():
            xbox.tap_b()
