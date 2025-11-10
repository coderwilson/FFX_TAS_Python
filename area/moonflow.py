import logging

import battle.boss
import battle.main
import memory.main
from memory.main import get_item_slot, get_item_count_slot
import menu
import pathing
import screen
import vars
import xbox
from battle import avina_memory
from paths import Moonflow1, MoonflowBankNorth, MoonflowBankSouth
from players import Auron, Tidus, Wakka

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    # aVIna has perfect memory. Right? Right?!
    heal_array = []
    ml_heals = False
    section = "moonflow_heals"
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        logger.manip(f"Seed: {seed_str}")
        if seed_str in records.keys():
            if section in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str][section]:
                        if records[seed_str][section][i] == "True":
                            heal_array.append(i)
            else:
                logger.info("I have no memory of this seed. (A)")
            if "ml_heals" in records[seed_str].keys():
                if records[seed_str]["ml_heals"] == "True":
                    ml_heals = True
        else:
            logger.info("I have no memory of this seed. (B)")
    except Exception:
        logger.info("I have no memory of this seed. (C)")

    logger.info("Starting Moonflow section")
    keys = 0
    key_slot = get_item_slot(81)
    keys_start = get_item_count_slot(key_slot)
    battle_count = 0

    checkpoint = 0
    while memory.main.get_map() != 235:
        if memory.main.user_control():
            # logger.debug(keys)
            # Chests
            if checkpoint == 2:  # Gil outside Djose temple
                logger.info("Djose gil chest")
                FFXC.set_movement(-1, 1)
                xbox.skip_dialog(1)
                FFXC.set_movement(1, -1)
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 15 and keys == 0:
                key_slot = get_item_slot(81)
                keys = get_item_count_slot(key_slot)
                if keys == keys_start:
                    checkpoint = 70
                logger.debug(f"Key sphere checkpoint: {checkpoint}")
            elif checkpoint == 38:
                checkpoint = 45
                logger.info(
                    f"No longer get mdef sphere. Updated checkpoint: {checkpoint}"
                )
            elif checkpoint == 43:  # Moonflow chest
                if memory.main.get_item_slot(90) < 200:
                    checkpoint += 1
                else:
                    pathing.set_movement([-1796, -480])
                    xbox.tap_b()
            elif checkpoint == 75:
                key_slot = get_item_slot(81)
                keys = get_item_count_slot(key_slot)
                if keys == keys_start:
                    FFXC.set_movement(0, 1)
                    xbox.tap_b()
                else:
                    checkpoint += 1
                    logger.debug(f"Chest gotten. {checkpoint}")
            elif checkpoint == 77:
                checkpoint = 17

            # Map changes
            elif checkpoint < 6 and memory.main.get_map() == 76:
                checkpoint = 6
            elif checkpoint < 11 and memory.main.get_map() == 93:
                checkpoint = 11
            elif checkpoint < 14 and memory.main.get_map() == 75:
                checkpoint = 14
            elif checkpoint < 49 and memory.main.get_map() == 105:
                checkpoint = 49
            elif checkpoint < 54 and memory.main.get_story_progress() == 1045:
                checkpoint = 54
                logger.debug(f"Updating checkpoint based on progress: {checkpoint}")
            elif checkpoint == 54 and memory.main.get_map() == 188:
                checkpoint = 55
                logger.debug(f"Updating checkpoint based on progress: {checkpoint}")

            # General pathing
            elif pathing.set_movement(Moonflow1.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_count += 1
                battle.main.flee_all()
                if memory.main.game_over():
                    seed_str = str(memory.main.rng_seed())
                    avina_memory.add_battle_to_memory(
                        seed=seed_str,
                        area="moonflow_heals",
                        battle_num=battle_count - 1,
                    )
                    return [False, 0, False, False]
                battle.main.wrap_up()
                logger.debug(f"ML heals value: {ml_heals}")
                if ml_heals:
                    logger.warning("aVIna deciding if we need to heal.")
                    if battle_count in heal_array:
                        battle.main.heal_up()
                    else:
                        logger.debug("No need to heal up. Moving onward.")
                else:
                    battle.main.heal_up()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif checkpoint in [75,76] and memory.main.diag_skip_possible():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    logger.info("End of approach section, should now be talking to Lucille/Elma/etc.")


def south_bank(checkpoint: int = 0):
    # Arrive at the south bank of the moonflow.
    logger.info("South bank, Save sphere screen")

    memory.main.click_to_control()  # "Where there's a will, there's a way."
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_neutral()

    memory.main.click_to_control()
    party_hp = memory.main.get_hp()
    if memory.main.equipped_weapon_has_ability(char_num=0, ability_num=0x8026):
        if memory.main.check_ability(ability=0x804B):
            menu.equip_weapon(character=0, ability=0x804B, full_menu_close=False)
    if party_hp[4] < 800:
        battle.main.heal_up(2)
    elif party_hp[0] < 700:
        battle.main.heal_up(1)
    memory.main.close_menu()

    while not memory.main.battle_active():
        if memory.main.user_control():
            if checkpoint == 4:
                FFXC.set_neutral()
                memory.main.click_to_event()
                memory.main.wait_frames(18)
                xbox.menu_b()  # Ride ze Shoopuff?
                memory.main.wait_frames(10)
                xbox.menu_down()
                xbox.menu_b()  # All aboardz!
                xbox.skip_dialog(3)  # Just to clear some dialog

            elif pathing.set_movement(MoonflowBankSouth.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()

    battle.boss.extractor()


def north_bank():
    memory.main.click_to_control_3()
    FFXC.set_movement(-1, 0)
    memory.main.await_event()
    memory.main.wait_frames(30 * 1)
    memory.main.await_control()
    if game_vars.platinum():
        while not pathing.set_movement([43,-66]):
            pass
        pathing.primer()
        while not pathing.set_movement([43,-66]):
            pass
        while not pathing.set_movement([14,-143]):
            pass
    elif game_vars.csr():
        memory.main.wait_frames(10)
        FFXC.set_movement(-1, -0.7)
        memory.main.wait_frames(6)
        FFXC.set_movement(-1, 0)
        memory.main.await_event()
    else:
        memory.main.wait_frames(45)
        memory.main.click_to_event()  # Talk to Auron
        FFXC.set_neutral()
        memory.main.wait_frames(9)
        memory.main.click_to_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(15)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_frames(15)
    if game_vars.get_l_strike() % 2 == 1:
        menu.equip_weapon(character=0, special="brotherhoodearly")

    checkpoint = 0
    logger.info("Miihen North Bank pattern. Starts after talking to Auron.")
    while memory.main.get_map() != 135:
        if memory.main.user_control():
            if checkpoint == 7:  # Rikku steal/mix tutorial
                FFXC.set_movement(1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.main.mix_tutorial()
                memory.main.update_formation(Tidus, Wakka, Auron)
                memory.main.close_menu()
                checkpoint += 1
            elif memory.main.get_story_progress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                logger.debug(f"Rikku scene, updating Checkpoint {checkpoint}")

            # Map changes
            elif checkpoint < 2 and memory.main.get_map() == 109:
                checkpoint = 2
            elif checkpoint < 12 and memory.main.get_map() == 97:
                checkpoint = 12

            # General pathing
            elif pathing.set_movement(MoonflowBankNorth.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
    logger.info("Moonflow End")
