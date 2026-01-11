import logging

import battle.main
import screen
import logs
import memory.get
import memory.main
from memory.main import equipped_weapon_has_ability
from memory.unlocks import has_ability_unlocked, od_mode_unlocks, od_mode_current
from menu import open_grid, equip_armor
import memory.sphere_grid
import menu
import pathing
import save_sphere
import vars
import xbox
import blitz
from players import (
    Auron, 
    CurrentPlayer, 
    Rikku, 
    Tidus, 
    Yuna, 
    Wakka,
    Kimahri,
    Lulu
)
import area.boats
import reset
import area.dream_zan
from area.dream_zan import split_timer
import load_game
import area.chocobos
from json_ai_files.write_seed import write_big_text, write_custom_message
from nemesis.arena_battles import (
    yojimbo_battle,
    recharge_overdrives_overworld,
    juggernaut_farm,
    vidatu_farm,
    restock_downs,
    item_dump,
    basic_quick_attacks,
    zan_ready,
    recharge_overdrives
)
from nemesis.arena_select import (
    arena_return,
    arena_npc,
    navigate_to_airship_destination,
    add_airship_unlocked_location,
    remove_airship_unlocked_location,
    air_ship_destination,
    return_to_airship,
    od_change,
    arena_menu_select,
    start_fight,
    rin_equip_dump,
    od_check_2,
    distill_spheres
)
import random
from save_sphere import touch_and_go
from sphere_grid.completion_functions import (
    max_level_ups,
    stock_all_locks,
    get_grid,
    nearest_interesting_node,
    stock_return_sphere,
    restock_mp,
    count_still_locked,
    update_completion_report
)
from gamestate import game
from paths.nem import YojimboFarm, OmegaFarm
from paths.gagazet import GagazetCave

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def lv1_locks():
    stock_all_locks(limit=1)
    # stock_all_locks(limit=2)

def jecht_shot():
    return_to_airship()
    # air_ship_destination(1)
    navigate_to_airship_destination("Besaid")
    memory.main.await_control()

    # First to Besaid for a Jecht sphere
    while not pathing.set_movement([-246,-360]):
        pass
    while not pathing.set_movement([95,-63]):
        pass
    while not pathing.set_movement([340,-56]):
        pass
    while not pathing.set_movement([353,19]):
        pass
    FFXC.set_movement(1,1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.click_to_control()

    # Now on the SS Liki (first boat)
    memory.main.await_control()
    while not pathing.set_movement([-19,-46]):
        pass
    FFXC.set_movement(0,1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([8,-17]):
        pass
    pathing.approach_coords([10,-10])  # Touch the Jecht Sphere
    FFXC.set_neutral()
    memory.main.click_to_control()
    FFXC.set_movement(0,-1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([1,-50]):
        pass
    FFXC.set_movement(0,1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_seconds(2)
    xbox.tap_confirm()
    memory.main.wait_seconds(1)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.await_control()

    # Arrived at Kilika
    #while not pathing.set_movement([-291,-257]):
    #    pass
    while not pathing.set_movement([-348,-251]):
        pass

    # Boarding boat to Luca
    FFXC.set_movement(-1,0)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_seconds(3)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.await_control()

    # Learn shot
    while not pathing.set_movement([-41,-1]):
        pass
    while not pathing.set_movement([-28,92]):
        pass
    pathing.approach_coords([0, 115], click_through=False)
    #memory.main.wait_seconds(3)
    #xbox.tap_confirm()
    area.boats.jecht_shot(learn_shot=True)
    memory.main.await_control()
    
    # Sleep on boat
    while not pathing.set_movement([-28,92]):
        pass
    while not pathing.set_movement([-41,-1]):
        pass
    while not pathing.set_movement([-32,-47]):
        pass
    while not pathing.set_movement([6,-48]):
        pass
    FFXC.set_movement(1,1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(1)
    xbox.tap_down()
    xbox.tap_confirm()

    # Luca, to stadium front
    memory.main.await_control()
    while not pathing.set_movement([94,374]):
        pass
    while not pathing.set_movement([29,331]):
        pass
    FFXC.set_movement(0,-1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([-275,112]):
        pass
    FFXC.set_movement(0,-1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([-301,-38]):
        pass
    logger.debug("End of Platinum section, jecht_shot.")
    # return_to_airship()


def blitzball_recruit_tour(extras:bool = True):
    if memory.main.get_map() == 374:
        # air_ship_destination(3)
        navigate_to_airship_destination("Luca")
    # write_big_text("Recruiting Wedge, Forward 2")
    # while not pathing.set_movement([-301,-56]):
    #     pass
    # while not pathing.set_movement([-207,-59]):
    #     pass

    # pathing.blitz_recruit(8360) # Wedge, #2 defender.
    
    # while not pathing.set_movement([-207,-59]):
    #     pass
    # while not pathing.set_movement([-301,-56]):
    #     pass
    while not pathing.set_movement([-439,-1]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    write_big_text("Recruiting Zalitz, Defender 2")
    while not pathing.set_movement([-20,19]):
        pass
    logger.debug("Mark 1")
    while not pathing.set_movement([-7,70]):
        pass
    logger.debug("Mark 2")
    while not pathing.set_movement([-6,133]):
        pass
    logger.debug("Mark 3")
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,1)
    logger.debug("Mark 4")
    FFXC.set_neutral()
    memory.main.await_event()
    while not pathing.set_movement([-371,-396]):
        pass
    logger.debug("Mark 5")
    
    pathing.blitz_recruit(8538) # Zalitz, Defender 2
    
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
        
    while not pathing.set_movement([-7,70]):
        pass
    while not pathing.set_movement([-13,19]):
        pass
    while not pathing.set_movement([-248,9]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,0)
    while not pathing.set_movement([-288,-45]):
        pass
    return_to_airship()
    write_big_text("Recruiting Ropp, Defender 1")
    
    # air_ship_destination(4)
    navigate_to_airship_destination("Mi'ihen Highroad")
    
    while not pathing.set_movement([30,-26]):
        pass
    while not pathing.set_movement([21,-18]):
        pass

    pathing.blitz_recruit(8277) # Ropp, #1 defender!
    
    while not pathing.set_movement([30,-26]):
        pass
    return_to_airship()
    
    write_big_text("Recruiting Miyu, Goalkeeper")
    # air_ship_destination(6)
    navigate_to_airship_destination("Moonflow")
    # First, another Jecht sphere
    if extras:
        while not pathing.set_movement([262,47]):
            pass
        pathing.approach_coords([185,12])


    while not pathing.set_movement([145,110]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,0)
    while not pathing.set_movement([-112,109]):
        pass
    while not pathing.set_movement([-107,93]):
        pass
    pathing.approach_coords([-65,40], click_through=False)
    FFXC.set_neutral()  # Ride ze shoopuff?
    memory.main.wait_seconds(4)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.await_control()
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,0)
    while not pathing.set_movement([27,-184]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,0)
    while not pathing.set_movement([-270,191]):
        pass
    pathing.blitz_recruit(8329) # Miyu, scaling goalie.
    while not pathing.set_movement([-270,191]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,0)
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([76,-137]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,0)
    while not pathing.set_movement([166,83]):
        pass
    return_to_airship()


def blitz_game(first_game:bool=False, tourney:bool=False, jecht_shot:bool=False):
    if memory.main.game_over():
        return False
    if memory.main.get_map() == 374:
        while not pathing.set_movement([-266,360]):
            pass
    save_sphere.approach_save_sphere()
    if memory.main.get_map() == 374:
        while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
            xbox.menu_down()
    else:
        while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
            xbox.menu_down()
    xbox.menu_b()

    if tourney:
        from memory.main import save_popup_cursor
        last_value = save_popup_cursor()
        while save_popup_cursor() != 1:
            if last_value < 1:
                xbox.menu_down()
            else:
                xbox.menu_up()
            memory.main.wait_frames(2)
            if last_value == 0 and save_popup_cursor() == 2:
                xbox.tap_back()
                xbox.tap_confirm()
                return False
    else:
        xbox.tap_confirm()
    memory.main.wait_seconds(2)

    
    while not memory.main.diag_progress_flag() in [113,40]:
        if memory.main.diag_progress_flag() == 41:
            # Select team/formation
            if first_game:
                logger.warning("first_game true, setting team.")
                # xbox.tap_confirm()
                # memory.main.wait_seconds(1)
                # xbox.tap_confirm()
                # memory.main.wait_seconds(1)
                xbox.tap_confirm()  # Tidus
                memory.main.wait_seconds(1)
                xbox.tap_confirm()  # Datto
                memory.main.wait_seconds(1)
                xbox.tap_confirm()  # Letty
                memory.main.wait_seconds(1)
                xbox.tap_up()
                xbox.tap_confirm()  # Ropp
                memory.main.wait_seconds(1)
                xbox.tap_up()
                xbox.tap_confirm()  # Zalitz
                memory.main.wait_seconds(1)
                xbox.tap_up()
                xbox.tap_confirm()  # Miyu
                memory.main.wait_seconds(1)
                xbox.tap_confirm()
            else:
                while memory.main.diag_progress_flag() == 41:
                    xbox.tap_confirm()
                    memory.main.wait_seconds(1)
            memory.main.wait_seconds(1)
        elif memory.main.diag_progress_flag() in [20]:
            logger.warning("Skill setting screen, no XP gained.")
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
        elif memory.main.diag_progress_flag() == 27:
            logger.warning("Skill setting screen")
            # Set jecht shot
            if jecht_shot:
                xbox.tap_confirm()
                memory.main.wait_seconds(1)
                xbox.tap_confirm()
                memory.main.wait_seconds(1)
                xbox.tap_confirm()
                memory.main.wait_seconds(2)
                xbox.tap_back()
                memory.main.wait_seconds(2)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
        elif memory.main.diag_progress_flag() == 22:
            logger.warning("Skill setting screen (2)")
            xbox.tap_back()
            memory.main.wait_seconds(2)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
        elif memory.main.diag_progress_flag() == 33:
            logger.warning("Skill setting screen (3)")
            xbox.tap_back()
            memory.main.wait_seconds(2)
            xbox.tap_back()
            memory.main.wait_seconds(2)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
        elif memory.main.diag_progress_flag() in [102,103,134,41]:
            if memory.main.diag_skip_possible():
                xbox.tap_back()
                memory.main.wait_seconds(1)
                xbox.tap_back()
                memory.main.wait_frames(9)
                xbox.menu_b()
        elif memory.main.diag_progress_flag() == 40:
            logger.info("Attempting to proceed.")
            if memory.main.blitz_proceed_cursor() != 0:
                xbox.menu_up()
            else:
                xbox.menu_b()
        else:
            logger.debug(f"Screen: {memory.main.diag_progress_flag()}")
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
    # if memory.main.diag_progress_flag() == 134:
    #     logger.warning(memory.main.wakka_od_learned())
    #     while memory.main.blitz_proceed_cursor() == 1:
    #         while memory.main.blitz_proceed_cursor() == 1:
    #             xbox.tap_up()
    #         memory.main.wait_frames(1)
    if memory.main.diag_progress_flag() == 40:
        logger.info("Attempting to proceed.")
        if memory.main.blitz_proceed_cursor() != 0:
            xbox.menu_up()
        else:
            xbox.menu_b()
    blitz.blitz_main(False)
    logger.warning(memory.main.wakka_od_learned())

def blitz_force_reward(reward_num:int = 99):
    if memory.main.game_over():
        return False
    save_sphere.touch_and_save(save_num=199)

    complete = False
    while not complete:
        write_big_text("Manipulating Blitz rewards (force)")
        if memory.main.get_map() == 374:
            while not pathing.set_movement([-266,360]):
                pass
        save_sphere.approach_save_sphere()
        if memory.main.get_map() == 374:
            while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
                xbox.menu_down()
        else:
            while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
                xbox.menu_down()
        xbox.menu_b()
        memory.main.wait_seconds(5)
        xbox.tap_down()
        memory.main.wait_seconds(5)
        xbox.tap_up()

        if reward_num in [0x011F, 0x0121]:
            if memory.main.blitz_tournament_prizes()[0] == reward_num:
                if memory.main.blitz_tournament_active():
                    complete = True
        elif reward_num in [0x0120, 0x0018]:
            if memory.main.blitz_league_prizes()[0] == reward_num:
                complete = True
        
        if not complete:
            if memory.main.blitz_tournament_prizes()[0] != reward_num:
                write_big_text("Resetting")
                logger.debug("Mark 1")
                xbox.tap_back()
                xbox.tap_back()
                xbox.tap_confirm()
                logger.debug("Mark 2")
                memory.main.await_control()
                logger.debug("Mark 3")
                memory.main.wait_frames(9)
                reset.reset_to_main_menu()
                logger.debug("Mark 4")
                area.dream_zan.new_game(gamestate="reload_autosave")
                logger.debug("Mark 5")
                load_game.load_save_num(0)
            logger.debug("Ready")
            memory.main.await_control()
        else:
            write_big_text("Manipulation done")


    xbox.tap_back()
    memory.main.wait_frames(2)
    xbox.tap_confirm()

def blitz_remake_tourney(reward_num):
    if memory.main.game_over():
        return False
    write_big_text("Manipulating Blitz rewards (remake)")
    while True:
        # if memory.main.get_map() == 374:
        #     while not pathing.set_movement([-266,360]):
        #         pass
        # save_sphere.touch_and_save(save_num=199)
        save_sphere.approach_save_sphere()
        if memory.main.get_map() == 374:
            while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
                xbox.menu_down()
        else:
            while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
                xbox.menu_down()
        xbox.menu_b()
        memory.main.wait_seconds(5)

        if memory.main.blitz_tournament_active():
            if memory.main.blitz_tournament_prizes()[0] == reward_num:
                logger.info("Tournament is now set up.")
                write_big_text("Tournament Ready")
                xbox.tap_back()
                xbox.tap_confirm()
                memory.main.await_control()
                return True
            else:
                logger.info("Tournament is incorrect. Resetting.")
                write_big_text("Tournament incorrect")
                reset.reset_to_main_menu()
                area.dream_zan.new_game(gamestate="reload_autosave")
                load_game.load_save_num(199)
                memory.main.await_control()
        else:
            logger.info("Tournament is not active.")
            write_big_text("Tournament offline")
            xbox.tap_back()
            xbox.tap_confirm()
            memory.main.await_control()


def blitz_remove_tourney():
    write_big_text("Manipulating Blitz rewards (remove)")
    while memory.main.blitz_tournament_active():
        if memory.main.get_map() == 374:
            while not pathing.set_movement([-266,360]):
                pass
        save_sphere.approach_save_sphere()
        if memory.main.get_map() == 374:
            while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
                xbox.menu_down()
        else:
            while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
                xbox.menu_down()
        xbox.menu_b()
        memory.main.wait_seconds(5)

        xbox.tap_back()
        xbox.tap_confirm()
        memory.main.await_control()
    
    for i in range(4):
        # This should end just before a new tournament is created.
        if memory.main.get_map() == 374:
            while not pathing.set_movement([-266,360]):
                pass
        save_sphere.approach_save_sphere()
        if memory.main.get_map() == 374:
            while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
                xbox.menu_down()
        else:
            while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
                xbox.menu_down()
        xbox.menu_b()
        memory.main.wait_seconds(5)

        xbox.tap_back()
        xbox.tap_confirm()
        memory.main.await_control()
        logger.warning(f"Map: {memory.main.get_map()}")
        # if memory.main.get_map() == 374:
        while not pathing.set_movement([-266,360]):
            pass
        save_sphere.touch_and_save(save_num=199)

def blitz_force_season_reward(reward_num:int = 99):
    write_big_text("Manipulating Blitz Season rewards")

    if memory.main.get_map() == 374:
        while not pathing.set_movement([-266,360]):
            pass
    save_sphere.approach_save_sphere()
    if memory.main.get_map() == 374:
        while memory.main.save_menu_cursor() != 1 and memory.main.save_menu_cursor_2() != 1:
            xbox.menu_down()
    else:
        while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
            xbox.menu_down()
    xbox.menu_b()
    memory.main.wait_seconds(5)
    
    complete = False
    while not complete:
        
        xbox.tap_up()
        xbox.tap_b()
        memory.main.wait_seconds(2)
        xbox.tap_b()
        memory.main.wait_seconds(2)
        xbox.tap_up()
        xbox.tap_b()
        memory.main.wait_seconds(4)

        if memory.main.blitz_league_prizes()[0] == reward_num:
            complete = True

    xbox.tap_back()
    memory.main.wait_frames(2)
    xbox.tap_confirm()
    memory.main.wait_seconds(4)

    blitzball_recruit_tour(extras=False)


def status_reels_start():
    write_big_text("Manipulating Blitz rewards (Status Reels)")
    blitz_force_season_reward(0x0120)

    write_big_text(f"Learning Status Reels\nGame {1} of 10")
    blitz_game(first_game=True)

    write_big_text(f"Learning Status Reels\nGame {2} of 10")
    blitz_game(jecht_shot=True)
    

    for i in range(8):
        write_big_text(f"Learning Status Reels\nGame {i+3} of 10")
        blitz_game()
    return

def aurochs_reels_start():
    blitz_remove_tourney()
    blitz_force_reward(0x0121)

    write_big_text(f"Learning Auroch Reels\nGame {1} of 3")
    blitz_game(tourney=True)
    for i in range(2):
        write_big_text(f"Learning Auroch Reels\nGame {i+2} of 3")
        blitz_game(tourney=True)
    #for i in range(10):
    #    write_big_text(f"Advancing for Jupiter Sigil\nGame {i+1} of 10")
    #    # This is to reset for the Jupiter Sigil without losing XP.
    #    # We could reset game data in a later iteration.
    #    blitz_game()

def jupiter_sigil_start():
    write_big_text("Manipulating Blitz rewards (Jupiter)")
    blitz_force_season_reward(0x0018)

    write_big_text(f"Jupiter Sigil League\nGame {1} of 10")
    blitz_game(first_game=True, jecht_shot=False)

    write_big_text(f"Jupiter Sigil League\nGame {2} of 10")
    blitz_game(jecht_shot=True)

    for i in range(8):
        write_big_text(f"Jupiter Sigil League\nGame {i+3} of 10")
        blitz_game()
    split_timer()
    save_sphere.touch_and_save(save_num=199)

def next_blitzball():
    battles = memory.main.wakka_total_battles()
    drives = memory.main.wakka_od_learned()
    if (
        battles > 250 and 
        drives[1] and not 
        drives[2]
    ):
        status_reels_start()
        # split_timer()
    elif battles > 450:
        if not drives[3]:
            aurochs_reels_start()
            # split_timer()

def blitz_rewards_in_luca():
    write_big_text("Collecting Wakka's Celestial")
    # air_ship_destination(3)
    navigate_to_airship_destination("Luca")
    
    while not pathing.set_movement([-296,-52]):
        pass
    while not pathing.set_movement([-174,-66]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    memory.main.await_control()
    
    while not pathing.set_movement([12,9]):
        pass
    pathing.approach_coords([12,25])
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([-11,-2]):
        pass
    while memory.main.get_coords()[0] > -30:
        pathing.set_movement([-25,-1])
    
    # Inside the locker room
    while not pathing.set_movement([-70,22]):
        pass
    while not pathing.set_movement([-118,24]):
        pass
    while memory.main.user_control():
        variance = random.choice(range(-6,6))
        x = -118 + variance
        pathing.set_movement([x,27])  # Get Jupiter Crest
        xbox.tap_confirm()
        memory.main.wait_frames(6)
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([-70,22]):
        pass
    while memory.main.get_coords()[0] < -30:
        pathing.set_movement([-30,-1])
    while not pathing.set_movement([1,-48]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Front of stadium
    while not pathing.set_movement([-296,-52]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Reverse T section
    while not pathing.set_movement([5,-35]):
        pass
    while not pathing.set_movement([173,-15]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Fountain
    while not pathing.set_movement([29,-87]):
        pass
    while not pathing.set_movement([61,-32]):
        pass
    while not pathing.set_movement([59,38]):
        pass
    while not pathing.set_movement([1,117]):
        pass
    while not pathing.set_movement([1,156]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Cantina
    while not pathing.set_movement([8,-45]):
        pass
    pathing.approach_coords([4,-45])
    FFXC.set_neutral()
    xbox.tap_confirm()
    xbox.tap_confirm()
    xbox.tap_confirm()
    memory.main.click_to_control()
    while not pathing.set_movement([-1,-74]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Fountain again
    while not pathing.set_movement([23,90]):
        pass
    while not pathing.set_movement([58,68]):
        pass
    while not pathing.set_movement([63,-35]):
        pass
    while not pathing.set_movement([23,-84]):
        pass
    while not pathing.set_movement([2,-182]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Towards theater
    while not pathing.set_movement([43,25]):
        pass
    while not pathing.set_movement([6,63]):
        pass
    while not pathing.set_movement([1,130]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Past Zalitz
    while not pathing.set_movement([-362,-328]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Theater Entrance
    while not pathing.set_movement([-15,-20]):
        pass
    while not pathing.set_movement([22,-5]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Theater purchase, movie spheres
    while not pathing.set_movement([8,-134]):
        pass
    pathing.approach_actor_by_id(actor_id=8403)
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(5)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    while not memory.main.user_control():
        xbox.tap_back()
        xbox.tap_confirm()
        memory.main.wait_seconds(3)
    
    # Theater purchase, music spheres
    while not pathing.set_movement([-6,-121]):
        pass
    pathing.approach_actor_by_id(actor_id=8252)
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    while not memory.main.user_control():
        xbox.tap_back()
        xbox.tap_confirm()
        memory.main.wait_seconds(3)
    
    # Now special music spheres.
    pathing.approach_actor_by_id(actor_id=8252)
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    memory.main.wait_seconds(5)
    xbox.tap_confirm()
    memory.main.wait_seconds(3)
    xbox.tap_confirm()
    while not memory.main.user_control():
        xbox.tap_back()
        xbox.tap_confirm()
        memory.main.wait_seconds(3)

    # Leaving the movie theater
    while not pathing.set_movement([-7,-151]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Leaving the movie theater entrance (with musicians)
    while not pathing.set_movement([-17,15]):
        pass
    while not pathing.set_movement([-83,18]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Past Zalitz
    while not pathing.set_movement([-382,-402]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    memory.main.await_control()

    # Reverse T
    while not pathing.set_movement([-10,56]):
        pass
    while not pathing.set_movement([-54,22]):
        pass
    while not pathing.set_movement([-231,2]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(-1,0)
    FFXC.set_neutral()
    memory.main.await_control()
    logger.debug("Blitzball Front Desk map")
    
    while not pathing.set_movement([-308,-35]):
        pass
    return_to_airship()

def showcase_1():
    area.chocobos.all_races()
    area.chocobos.to_remiem(get_primer=True)
    area.chocobos.remiem_races()
    area.chocobos.leave_temple()
    area.chocobos.butterflies()
    area.chocobos.upgrade_mirror()
    area.chocobos.spirit_lance(skip_dodges=True)
    
    area.chocobos.sun_sigil(godhand=0, baaj=0)
    area.chocobos.cactuars(godhand=0, baaj=0)
    area.chocobos.cactuars_finish(godhand=0, baaj=0)
    area.chocobos.upgrade_celestials(godhand=0, baaj=0, Tidus_only=True)

def farming_power_spheres():
    # This must come after showcase_1 or we will soft lock fighting Juggernaut.
    rin_equip_dump()
    write_big_text(f"Stock all locks up to level 3!")
    arena_return()
    stock_all_locks()
    menu.equip_weapon(character=0, ability=32772,full_menu_close=True)  # Evade & Counter (Caldabolg)
    menu.remove_all_nea()
    write_big_text(f"Power farm STR and MP spheres.")
    juggernaut_farm(include_yojimbo=False)
    vidatu_farm()
    menu.equip_weapon(character=0, ability=32781,full_menu_close=True)  # One-MP
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    return_to_airship()

def showcase_2(jump_in_from_save:bool=False):
    godhand = 0
    baaj=0
    if not jump_in_from_save:
        blitz_rewards_in_luca()
        primer_cleanup_1()  # Now performed prior to level grind.
        # primer_cleanup_2()  # Now performed during the Nova section.
        split_timer()
        if not zan_ready():
            recharge_overdrives(align_zan=True)
        area.chocobos.sun_crest(godhand=godhand, baaj=baaj, face_bahamut=True, get_crest=False)
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    area.chocobos.besaid_destro(godhand=godhand, baaj=baaj, jecht_sphere=True, checkpoint=12)
    # area.chocobos.kilika_destro(godhand=godhand, baaj=baaj)
    # area.chocobos.djose_destro(godhand=godhand, baaj=baaj)
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    area.chocobos.ice_destro(godhand=godhand, baaj=baaj)

    area.chocobos.rusty_sword(godhand=godhand, baaj=baaj)
    # area.chocobos.saturn_crest(godhand=godhand, baaj=baaj)
    area.chocobos.masamune(godhand=godhand, baaj=baaj)

    baaj = area.chocobos.onion_knight(godhand=godhand, baaj=baaj)
    area.chocobos.belgemine(godhand=godhand, baaj=baaj)
    area.chocobos.venus_crest(godhand=godhand, baaj=baaj)
    godhand = area.chocobos.godhand(baaj=baaj)
    add_airship_unlocked_location("Mushroom Rock")
    write_big_text("")

    area.chocobos.upgrade_celestials(godhand=godhand, baaj=baaj, Yuna=True, Wakka=True)
    
    menu.equip_weapon(character=4, ability=32772,full_menu_close=False)  # Evade & Counter
    menu.equip_weapon(character=6, ability=32794,full_menu_close=True)  # Gillionaire
    split_timer()

def showcase_3():
    # This is just to realign to the regular Nemesis run.
    arena_return(godhand=1, baaj=1)


def buy_clear_sheres():
    grid_instance = get_grid() # Get the grid instance
    luck_count = 0
    for i in range(4):
        node_type = f"Luck ({i+1} pt)"
        luck_count_local = grid_instance.count_nodes_of_type(node_type)
        logger.debug(f"There are {luck_count_local} nodes for {node_type}")
        luck_count += luck_count_local
    # memory.main.wait_frames(300)
    clears = memory.main.get_item_count_slot(memory.main.get_item_slot(95))
    luck_count -= clears
    if luck_count >= 1:
        arena_npc()
        arena_menu_select(3)
        memory.main.wait_seconds(3)
        xbox.menu_b()
        memory.main.wait_seconds(3)
        for i in range(30):
            xbox.menu_down()
        xbox.menu_b()
        memory.main.wait_seconds(3)
        for i in range(luck_count-1):
            xbox.menu_right()
        xbox.menu_b()
        memory.main.wait_seconds(1)
        xbox.menu_a()
        memory.main.wait_seconds(1)
        xbox.menu_a()
        memory.main.wait_seconds(1)
        xbox.menu_a()
        xbox.menu_b()
        memory.main.wait_seconds(3)


def steal_lv_4_keys():
    stock_all_locks(limit=4)


def cactuar_levels_battle():
    write_big_text("Farming XP via Cactuars")
    update_completion_report()
    haste = False
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not haste:
                if has_ability_unlocked(
                    character_index=CurrentPlayer().raw_id(),
                    ability_name="Haste"
                ):
                    CurrentPlayer().cast_white_magic_spell_by_name("Haste", target_id=20)
                    haste = True
                else:
                    CurrentPlayer().defend()
            elif memory.main.get_item_count_slot(memory.main.get_item_slot(6)) < 2:
                battle.main.flee_all()
            else:
                CurrentPlayer().defend()

    logger.debug("Battle is complete.")
    battle.main.wrap_up()
    logger.debug("Now back in control.")


def tonberry_levels_battle():
    write_big_text("Farming XP via Tonberries")
    # write_custom_message(f"Nemesis stage 4.5\nOD > AP on Stoic\nfor massive AP\n{game.state} {game.step}")
    screen.await_turn()
    tidus_turns = 0
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                tidus_turns += 1
                if tidus_turns == 8:
                    Tidus.flee()
                elif memory.main.get_overdrive_battle(character=0) == 100:
                    Tidus.overdrive()
                else:
                    battle.main.attack()
            else:
                CurrentPlayer().defend()

    logger.debug("Battle is complete.")
    battle.main.wrap_up()
    logger.debug("Now back in control.")


def get_weapon_value(char:int):
    try:
        if not equipped_weapon_has_ability(
            char_num=char, ability_num=0x8011
        ):
            # No OD > AP, no value.
            return 0

        value = 1
        if equipped_weapon_has_ability(
            char_num=char, ability_num=0x8013
        ):
            # Triple_AP
            value += 3
        elif equipped_weapon_has_ability(
            char_num=char, ability_num=0x8012
        ):
            # Double_AP
            value += 2
        if equipped_weapon_has_ability(
            char_num=char, ability_num=0x800F
        ):
            # Triple_OD
            value += 3
        elif equipped_weapon_has_ability(
            char_num=char, ability_num=0x800E
        ):
            # Double_OD
            value += 2
        return value
    except:
        return 0


def power_farm():
    if memory.main.get_map() == 374:
        arena_return(godhand=1, baaj=1)
    remaining_array = [0]*7
    for i in range(7):
        remaining_array[i] = count_still_locked(actor_id=i)
    if memory.main.equipped_armor_has_ability(
        char_num=game_vars.ne_armor(), ability_num=0x801D
    ) and game_vars.ne_armor() != 2:
        # Auron does not get auto-phoenix.
        # Everyone else should be sure to equip auto-phoenix again.
        try:
            menu.equip_armor(character=game_vars.ne_armor(), ability=0x800A)
        except:
            # This char has no Auto-Phoenix. Only occurs for Auron.
            pass
    
    while any(remaining_array):
        
        if memory.main.get_gil_value() < 10000 or len(memory.main.all_equipment()) > 150:
            menu.auto_sort_equipment()
            arena_npc()
            arena_menu_select(2)
            item_dump()
            arena_menu_select(4)
            menu.auto_sort_equipment()
        # od_check_2()
        power_formation = []
        for weap_value in range(8,-1,-1):
            for character in range(1,7): #  Tidus should always be the last.
                if (
                    remaining_array[character] != 0 and
                    get_weapon_value(character) == weap_value and
                    not character in power_formation and
                    len(power_formation) < 3
                ):
                    power_formation.append(character)
        if len(power_formation) < 3:
            for character in range(0,7):
                if (
                    not character in power_formation and
                    len(power_formation) < 3
                ):
                    power_formation.append(character)
        
        for i in range(3):
            # Find and equip the best weapon.
            logger.warning(f"Selected formation: {power_formation}")
            best_weap = memory.main.check_any_odap(power_formation[i], prio_odap=True)
            logger.warning(f"Best weap for {power_formation[i]}: {best_weap}")
            equip_handles = memory.main.weapon_array_character(power_formation[i])
            for current_handle in equip_handles:
                equip_weapon=True
                for j in range(len(best_weap)):
                    if not current_handle.has_ability(best_weap[j]):
                        equip_weapon=False
                if current_handle.is_equipped():
                    equip_weapon=False
                    logger.warning(f"Curr weap for {power_formation[i]}: {current_handle.abilities()}")
                if equip_weapon: 
                    menu.equip_weapon(
                        character=power_formation[i], 
                        ability_list=best_weap,
                        full_menu_close=False
                    )
            # memory.main.wait_frames(300)
                
            # Now set the most preferable overdrive mode.
            logger.debug(f"Unlocks for {power_formation[i]}: {od_mode_unlocks(power_formation[i])}")
            logger.debug(f"Current - {od_mode_current(power_formation[i])}")
            if (
                od_mode_unlocks(power_formation[i])[2] == 1 and
                od_mode_current(power_formation[i]) != 2 and
                power_formation[i] != 0
            ):
                od_change(character=power_formation[i], set_od_mode=2, full_menu_close=False)
            elif (
                od_mode_current(power_formation[i]) != 0 and
                (
                    od_mode_unlocks(power_formation[i])[2] == 0 or
                    power_formation[i] == 0
                )
            ):
                od_change(character=power_formation[i], set_od_mode=0, full_menu_close=False)
        memory.main.update_formation(
            power_formation[0],
            power_formation[1],
            power_formation[2]
        )
        
        arena_npc()
        arena_menu_select(1)
        if all(element == 0 for element in remaining_array[1:]):
            start_fight(area_index=13, monster_index=9)
            tonberry_levels_battle()
        else:
            start_fight(area_index=13, monster_index=5)
            cactuar_levels_battle()
        update_completion_report()
        arena_menu_select(4)
        restock_downs()
        response = grid_check()
        if response == "low_spheres":
            logger.debug("Low Spheres")
            distill_spheres()
        elif response == "low_filler_spheres":
            logger.debug("Low MP fillers")
            restock_mp()
            
        for i in range(7):
            remaining_array[i] = count_still_locked(actor_id=i)
    
    # All done farming, let's re-equip celestials.
    menu.auto_sort_equipment()
    for i in range(7):
        menu.equip_celestial(i)
    # memory.main.update_formation(Tidus, Wakka, Rikku)

def overdrive_buff(drops_for:int):
    if memory.main.get_item_count_slot(memory.main.get_item_slot(111)) >= 30:
        menu.add_ability(
            owner=drops_for,
            equipment_type=0,
            ability_array=[32787, 0x8011, 255, 255],
            ability_index=0x800F,
            slot_count=3,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=True,
        )
    elif memory.main.get_item_count_slot(memory.main.get_item_slot(110)) >= 30:
        menu.add_ability(
            owner=drops_for,
            equipment_type=0,
            ability_array=[32787, 0x8011, 255, 255],
            ability_index=0x800E,
            slot_count=3,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=True,
        )

def buff_equipped_weapon(char_id:int):
    ability_array = memory.main.equipped_weapon_current_abilities(char_id)
    logger.info(f"Customizing weapon for {char_id}")
    logger.info(f"Current abilities: {ability_array}")
    used_slots = 0
    for i in range(4):
        if ability_array[i] != 255:
            used_slots += 1
    total_slots = memory.main.equipped_weapon_slot_count(char_id)

    # memory.main.wait_frames(90)
    while total_slots > used_slots:
        action_taken = False
        if not 0x8011 in ability_array:
            menu.add_ability(
                owner=char_id,
                equipment_type=0,
                ability_array=ability_array,
                ability_index=0x8011,
                slot_count=total_slots,
                navigate_to_equip_menu=True,
                exit_out_of_current_weapon=True,
                close_menu=True,
                full_menu_close=True,
            )
            used_slots += 1
            action_taken = True
        
        elif not (equipped_weapon_has_ability(0x800E) or equipped_weapon_has_ability(0x800F)):
            if memory.main.get_item_count_slot(memory.main.get_item_slot(111)) >= 30:
                menu.add_ability(
                    owner=char_id,
                    equipment_type=0,
                    ability_array=ability_array,
                    ability_index=0x800F,
                    slot_count=total_slots,
                    navigate_to_equip_menu=True,
                    exit_out_of_current_weapon=True,
                    close_menu=True,
                    full_menu_close=True,
                )
                used_slots += 1
                action_taken = True
        
            elif memory.main.get_item_count_slot(memory.main.get_item_slot(110)) >= 30:
                menu.add_ability(
                    owner=char_id,
                    equipment_type=0,
                    ability_array=ability_array,
                    ability_index=0x800E,
                    slot_count=total_slots,
                    navigate_to_equip_menu=True,
                    exit_out_of_current_weapon=True,
                    close_menu=True,
                    full_menu_close=True,
                )
                used_slots += 1
                action_taken = True
        
        elif not (equipped_weapon_has_ability(0x8013) or equipped_weapon_has_ability(0x8012)):
            if memory.main.get_item_count_slot(memory.main.get_item_slot(108)) >= 50:
                menu.add_ability(
                    owner=char_id,
                    equipment_type=0,
                    ability_array=ability_array,
                    ability_index=0x8013,
                    slot_count=total_slots,
                    navigate_to_equip_menu=True,
                    exit_out_of_current_weapon=True,
                    close_menu=True,
                    full_menu_close=True,
                )
                used_slots += 1
                action_taken = True
        
            elif memory.main.get_item_count_slot(memory.main.get_item_slot(9)) >= 20:
                menu.add_ability(
                    owner=char_id,
                    equipment_type=0,
                    ability_array=ability_array,
                    ability_index=0x8012,
                    slot_count=total_slots,
                    navigate_to_equip_menu=True,
                    exit_out_of_current_weapon=True,
                    close_menu=True,
                    full_menu_close=True,
                )
                used_slots += 1
                action_taken = True
        # memory.main.wait_frames(90)
        if not action_taken:
            return
        ability_array = memory.main.equipped_weapon_current_abilities(char_id)
        logger.info(f"Customizing weapon for {char_id}")
        logger.info(f"Current abilities: {ability_array}")

def best_odap_weapons():
    for i in [5,2,1,3,4,6,0]:
        if game_vars.plat_triple_ap_check()[i]:
            # ability_array = memory.main.equipped_weapon_current_abilities(i)
            # if ability_array == [0x8013,0x8011,255,255]:
            #     overdrive_buff(i)
            if not equipped_weapon_has_ability(char_num=i, ability_num=0x8013):
                menu.equip_weapon(character=i, ability=0x8013)
            buff_equipped_weapon(i)
        else:
            chosen_abilities = memory.main.check_any_odap(i)
            logger.warning(f"Char {i} can equip ability {chosen_abilities}")
            # memory.main.wait_frames(180)
            if len(chosen_abilities) != 0:
                menu.equip_weapon(character=i, ability_list=chosen_abilities)
                game_vars.plat_triple_ap_check()[i] = 1
                buff_equipped_weapon(i)

def prep_back_line():
    write_big_text(f"Now, bribe extra Mega-Phoenix's.")
    arena_npc()
    arena_menu_select(1)
    start_fight(area_index=9, monster_index=7)
    battle.main.bribe_battle(spare_change_value=250000)
    arena_menu_select(4)
    write_big_text(f"Let's prep some B-squad equipment.")
    
    return_to_airship()
    rin_equip_dump(cap=True, b_squad=True)

    write_big_text(f"Now to Kilika")
    # air_ship_destination(3)
    navigate_to_airship_destination("Kilika")
    while not pathing.set_movement([-25, -246]):
        pass
    while not pathing.set_movement([-47, -209]):
        pass
    while not pathing.set_movement([-91, -199]):
        pass
    while not pathing.set_movement([-108, -169]):
        pass

    if (
        game_vars.plat_triple_ap_check()[5] and
        game_vars.plat_triple_ap_check()[1] and
        game_vars.plat_triple_ap_check()[2] and
        game_vars.plat_triple_ap_check()[3]
    ):
        logger.info("Everyone has a triple AP weap already.")
        logger.info("There is no need to buy new weapons, only armor.")
        pathing.approach_actor_by_id(8231)
        FFXC.set_neutral()
        memory.main.wait_frames(60)
        xbox.tap_b()  # Talking to the old lady
        memory.main.wait_frames(60)
        while not memory.main.equipment_buy_ready():
            xbox.menu_b()  # Buy equipment
        memory.main.wait_frames(6)
    else:
        first=255
        if not game_vars.plat_triple_ap_check()[5]:
            logger.info(f"Lulu weapon (1)")
            if memory.main.get_item_count_slot(memory.main.get_item_slot(107)) >= 10:
                menu.add_ability(
                    owner=5,
                    equipment_type=0,
                    ability_array=[0x8068, 255, 255, 255],
                    ability_index=0x8011,
                    slot_count=4,
                    navigate_to_equip_menu=True,
                    full_menu_close=False,
                )
            # memory.main.wait_frames(90)
            logger.info(f"Lulu weapon (2)")
            if memory.main.get_item_count_slot(memory.main.get_item_slot(108)) >= 50:
                menu.add_ability(
                    owner=5,
                    equipment_type=0,
                    ability_array=[0x8068, 0x8011, 255, 255],
                    ability_index=8013,
                    slot_count=4,
                    navigate_to_equip_menu=True,
                    full_menu_close=False,
                )
                first=0x8013
            elif memory.main.get_item_count_slot(memory.main.get_item_slot(9)) >= 20:
                menu.add_ability(
                    owner=5,
                    equipment_type=0,
                    ability_array=[0x8068, 0x8011, 255, 255],
                    ability_index=0x8012,
                    slot_count=4,
                    navigate_to_equip_menu=True,
                    full_menu_close=False,
                )
                first=0x8012
            # memory.main.wait_frames(90)
            logger.info(f"Lulu weapon (3)")
            if memory.main.get_item_count_slot(memory.main.get_item_slot(111)) >= 30:
                menu.add_ability(
                    owner=5,
                    equipment_type=0,
                    ability_array=[0x8068, 0x8011, first, 255],
                    ability_index=0x800F,
                    slot_count=4,
                    navigate_to_equip_menu=True,
                    full_menu_close=True,
                )
            elif memory.main.get_item_count_slot(memory.main.get_item_slot(110)) >= 30:
                menu.add_ability(
                    owner=5,
                    equipment_type=0,
                    ability_array=[0x8068, 0x8011, first, 255],
                    ability_index=0x800E,
                    slot_count=4,
                    navigate_to_equip_menu=True,
                    full_menu_close=True,
                )
            else:
                memory.main.close_menu()
        # memory.main.wait_frames(180)
        pathing.approach_actor_by_id(8231)
        FFXC.set_neutral()
        memory.main.wait_frames(60)
        xbox.tap_b()  # Talking to the old lady
        memory.main.wait_frames(60)
        while not memory.main.equipment_buy_ready():
            xbox.menu_b()  # Buy equipment
        memory.main.wait_frames(6)

        # Yuna weapon
        if not game_vars.plat_triple_ap_check()[1]:
            while memory.main.equip_buy_row() != 1:
                while memory.main.equip_buy_row() != 1:
                    if memory.main.equip_buy_row() > 1:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
        
        # Kimahri weapon
        if not game_vars.plat_triple_ap_check()[3]:
            while memory.main.equip_buy_row() != 4:
                while memory.main.equip_buy_row() != 4:
                    if memory.main.equip_buy_row() > 4:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
        
        # Auron weapon
        if not game_vars.plat_triple_ap_check()[2]:
            while memory.main.equip_buy_row() != 5:
                while memory.main.equip_buy_row() != 5:
                    if memory.main.equip_buy_row() > 5:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()

    # Lulu armor
    while memory.main.equip_buy_row() != 10:
        while memory.main.equip_buy_row() != 10:
            if memory.main.equip_buy_row() > 10:
                xbox.tap_up()
            else:
                xbox.tap_down()
        memory.main.wait_frames(6)
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    xbox.menu_up()
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    xbox.menu_up()
    memory.main.wait_frames(60)
    xbox.menu_b()

    # Kimahri armor
    while memory.main.equip_buy_row() != 11:
        while memory.main.equip_buy_row() != 11:
            if memory.main.equip_buy_row() > 11:
                xbox.tap_up()
            else:
                xbox.tap_down()
        memory.main.wait_frames(6)
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    xbox.menu_up()
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    xbox.menu_up()
    memory.main.wait_frames(60)
    xbox.menu_b()


    memory.main.close_menu()
    memory.main.click_to_control()
    if not game_vars.plat_triple_ap_check()[1]:
        logger.info(f"Yuna weapon (1)")
        menu.add_ability(
            owner=1,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 255, 255],
            ability_index=0x8011,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=False,
            full_menu_close=False,
        )
        logger.info(f"Yuna weapon (2)")
        menu.add_ability(
            owner=1,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 0x8011, 255],
            ability_index=0x801A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=False,
        )
    if not game_vars.plat_triple_ap_check()[2]:
        logger.info(f"Auron weapon (1)")
        menu.add_ability(
            owner=2,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 255, 255],
            ability_index=0x8011,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=False,
            full_menu_close=False,
        )
        logger.info(f"Auron weapon (2)")
        menu.add_ability(
            owner=2,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 0x8011, 255],
            ability_index=0x800F,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=False,
        )
    if not game_vars.plat_triple_ap_check()[3]:
        logger.info(f"Kimahri weapon (1)")
        menu.add_ability(
            owner=3,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 255, 255],
            ability_index=0x8011,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=False,
            full_menu_close=False,
        )
        logger.info(f"Kimahri weapon (2)")
        menu.add_ability(
            owner=3,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 0x8011, 255],
            ability_index=0x800F,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=False,
        )
    if memory.main.get_item_count_slot(memory.main.get_item_slot(7)) >= 20:
        logger.info(f"Kimahri armor (1)")
        menu.add_ability(
            owner=3,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=True,
        )
    logger.warning("Test - Lulu armor check")
    logger.warning(memory.main.get_item_count_slot(memory.main.get_item_slot(7)))
    # memory.main.wait_frames(900)
    if memory.main.get_item_count_slot(memory.main.get_item_slot(7)) >= 20:
        logger.info(f"Lulu armor (1)")
        menu.add_ability(
            owner=5,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=True,
        )
    else:
        logger.info(f"Not enough Mega.P.downs")
    if memory.main.get_item_count_slot(memory.main.get_item_slot(7)) >= 20:
        logger.info(f"Kimahri armor (1)")
        menu.add_ability(
            owner=3,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            full_menu_close=True,
        )
    memory.main.close_menu()
    memory.main.await_control()
    
    while not pathing.set_movement([-90, -203]):
        pass
    while not pathing.set_movement([-45, -212]):
        pass
    while not pathing.set_movement([20, -253]):
        pass
    return_to_airship()
    arena_return(godhand=1, baaj=1)

def equip_all_odap():
    for i in range(6):
        menu.equip_weapon(character=i, ability=0x8011,full_menu_close=False)
    menu.equip_weapon(character=6, ability=0x8011,full_menu_close=True)

def plat_finish_1():
    write_big_text("Best weapons")
    best_odap_weapons()
    write_big_text("Clear spheres")
    buy_clear_sheres()
    write_big_text("Lv.4 Key Spheres")
    steal_lv_4_keys()
    equip_all_odap()
    write_big_text("Prep the B-squad")
    prep_back_line()
    # primer_cleanup_1()

def plat_finish_2():
    write_big_text("Power farm all characters")
    power_farm()
    split_timer()

    write_big_text("Dark Yojimbo")
    dark_yojimbo()
    write_big_text("Dark Sisters")
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    primer_cleanup_1(sisters_return=True)
    dark_sisters()
    write_big_text("Dark Ixion")
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    dark_ixion(baaj=1, godhand=1)
    write_big_text("Dark Ifrit")
    dark_ifrit()
    write_big_text("Dark Anima")
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    dark_anima()
    add_airship_unlocked_location("Penance")

def plat_finish_3():
    write_big_text("Last Boss: Penance!!!")
    if not zan_ready():
        recharge_overdrives(align_zan=True)
    penance()
    split_timer()
    # write_big_text("Now to get Nova, the last Blue Magic we should need.")
    # nova()
    # split_timer()
    write_big_text("What else are we missing?\nWe should put more here.")
    FFXC.set_neutral()
    memory.main.wait_frames(30)
    navigate_to_airship_destination("Sin")

def dark_ixion(baaj:int=1, godhand:int=1):
    if memory.main.get_map() == 307:
        return_to_airship()
    navigate_to_airship_destination(destination_name="Thunder Plains")
    od_change(character=4, set_od_mode=0)
    extra_turns = [False]*5
    while not pathing.set_movement([-3,-46]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    while not pathing.set_movement([-61,-4]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
        
    while not pathing.set_movement([67,995]):
        pass
    while not pathing.set_movement([110,704]):
        pass
    while not pathing.set_movement([77,493]):
        pass
    while not pathing.set_movement([73,419]):
        pass
    pathing.approach_coords([60,400])  # Last Jecht Sphere
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([77,493]):
        pass
    while not pathing.set_movement([110,704]):
        pass
    while not pathing.set_movement([115,1072]):
        pass
    FFXC.set_neutral()
    memory.main.update_formation(Tidus, Wakka, Rikku)
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)

    # Now for Dark Ixion:
    while not pathing.set_movement([27,-951]):
        pass
    while not pathing.set_movement([11,-873]):
        pass
    while not pathing.set_movement([-15,-632]):
        pass
    while not memory.main.battle_active():
        if memory.main.user_control():
            pathing.approach_coords([-21,-531], quick_return=True)
    FFXC.set_neutral()
    while not Yuna.has_overdrive():
        if memory.main.turn_ready():
            if not Yuna.active():
                battle.main.buddy_swap(Yuna)
            elif Yuna.is_turn():
                Yuna.attack()
                extra_turns[0] = True
            elif not Tidus.active():
                battle.main.buddy_swap(Tidus)
            elif not Wakka.active():
                battle.main.buddy_swap(Wakka)
            elif Tidus.is_turn():
                if memory.main.get_overdrive_battle(character=0) == 100:
                    Tidus.overdrive()
                else:
                    Tidus.attack()
            elif Wakka.is_turn():
                if memory.main.get_overdrive_battle(character=4) == 100:
                    Wakka.overdrive(reels="attack")
                else:
                    CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                if memory.main.get_overdrive_battle(character=0) == 100:
                    Tidus.overdrive(version=0)
                else:
                    Tidus.attack()
            elif Wakka.is_turn():
                if memory.main.get_overdrive_battle(character=4) == 100:
                    Wakka.overdrive(reels="attack")
                else:
                    CurrentPlayer().attack()
            elif not Tidus.active():
                battle.main.buddy_swap(Tidus)
            elif not Wakka.active():
                battle.main.buddy_swap(Wakka)
            elif not extra_turns[0] and not Yuna.active():
                battle.main.buddy_swap(Yuna)
                Yuna.defend()
                extra_turns[0] = True
                extra_turns[3] = True
            elif not extra_turns[4] and not Rikku.active():
                battle.main.buddy_swap(Rikku)
                Rikku.defend()
                extra_turns[4] = True
            elif not extra_turns[2] and not Kimahri.active():
                battle.main.buddy_swap(Kimahri)
                Kimahri.defend()
                extra_turns[2] = True
            elif not extra_turns[1] and not Auron.active():
                battle.main.buddy_swap(Auron)
                Auron.defend()
                extra_turns[1] = True
            elif not extra_turns[3] and not Lulu.active():
                battle.main.buddy_swap(Lulu)
                Lulu.defend()
            else:
                CurrentPlayer().defend()
    battle.main.wrap_up()
    memory.main.click_to_control()
    # if od_ready:
    #     logger.info("Yuna has overdrive.")
    #     success = yojimbo_battle(flee_available=True,arena=False)
    # else:
    #     logger.info("Yuna does not have overdrive.")
    #     recharge_overdrives_overworld()
    #     battle.main.wrap_up()
    memory.main.update_formation(Tidus, Wakka, Rikku)
            
        # if not success:
        #     while not memory.main.battle_active():
        #         if memory.main.user_control():
        #             pathing.approach_coords([45,-90], quick_return=True)

        # if not success:
        #     logger.debug("Starting reset process.")
        #     reset.reset_to_main_menu()
        #     logger.debug("Intro screen - load game")
        #     new_game(gamestate="reload_autosave")
        #     logger.debug("Selecting save number.")
        #     load_game.load_save_num(0)
    memory.main.click_to_control()
    while not pathing.set_movement([79,-135]):
        pass
    logger.info("In position to start waiting.")
    
    FFXC.set_neutral()
    # 8300, 8364, 4432 are the three??? actors.
    success=False
    while not success:
        od_ready = Yuna.has_overdrive()
        while not memory.main.battle_active():
            actor_id = 8300
            index = memory.main.actor_index(actor_id)
            if memory.main.user_control():
                if pathing.distance(index) > 80:
                    FFXC.set_neutral()
                else:
                    logger.warning("Moving!!!")
                    memory.main.wait_seconds(2)
                    horse_coords = memory.main.get_actor_coords(index)
                    while memory.main.user_control():
                        pathing.set_movement([horse_coords[0],horse_coords[1]])
            else:
                FFXC.set_neutral()
        split_timer()
        FFXC.set_neutral()
        if od_ready:
            success = yojimbo_battle(flee_available=True,arena=False, anima=1)
        else:
            recharge_overdrives_overworld()

        if not success:
            battle.main.wrap_up()
            memory.main.update_formation(Tidus, Wakka, Rikku)
            while pathing.distance(index) < 80:
                if od_ready:
                    pathing.set_movement([131,-168])
                else:
                    pathing.set_movement([79,-135])
            if od_ready:
                touch_and_go()
                while not pathing.set_movement([79,-135]):
                    pass
            FFXC.set_neutral()
            memory.main.wait_seconds(2)
            actor_id = 8300
            index = memory.main.actor_index(actor_id)
            logger.debug("Waiting for horse to move/despawn")
            while pathing.distance(index) < 80:
                pass
            logger.debug("Wait complete")
            success=False

    while not pathing.set_movement([131,-168]):
        pass
    return_to_airship()

def dark_ifrit():
    if memory.main.get_map() == 307:
        return_to_airship()
    navigate_to_airship_destination(destination_name="Bikanel")
    area.chocobos.desert_path()
    FFXC.set_neutral()
    memory.main.update_formation(Lulu, Wakka, Yuna)
    while not pathing.set_movement([-228,726]):
        pass
    pathing.approach_coords([-240,765])
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([-341,998]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    while not memory.main.battle_active():
        pass
    battle.main.dark_aeon()
    split_timer()
    memory.main.await_control()
    area.chocobos.desert_path(start=55,end=1)

    return_to_airship()

def dark_sisters(baaj:int=1, godhand:int=1):
    # air_ship_destination(8+baaj+godhand)
    # navigate_to_airship_destination("Djose")
    memory.main.update_formation(Tidus, Wakka, Rikku)
    
    success=False
    while not success:
        while not pathing.set_movement([-18,-670]):
            pass
        while memory.main.user_control():
            FFXC.set_movement(0,-1)
        FFXC.set_neutral()
        while not memory.main.turn_ready():
            pass
        
        success = yojimbo_battle(flee_available=True, arena=False, anima=1)
        if not success:
            logger.debug("Starting reset process.")
            reset.reset_to_main_menu()
            logger.debug("Intro screen - load game")
            area.dream_zan.new_game(gamestate="reload_autosave")
            logger.debug("Selecting save number.")
            load_game.load_save_num(0)
    split_timer()

    while not pathing.set_movement([-91,-485]):
        pass
    while not pathing.set_movement([-195,-430]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,1)
    FFXC.set_neutral()
    memory.main.await_control()
    return_to_airship()

def dark_yojimbo():
    if memory.main.get_map() == 307:
        return_to_airship()
    menu.auto_sort_equipment()
    menu.add_ability(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 255, 255],
        ability_index=0x8038,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=False,
        full_menu_close=False
    )
    menu.add_ability(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 0x8038, 255],
        ability_index=0x805B,
        slot_count=4,
        navigate_to_equip_menu=True,
        close_menu=False,
        full_menu_close=False
    )
    menu.add_ability(
        owner=4,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 255, 255],
        ability_index=0x8038,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=False,
        full_menu_close=False
    )
    menu.add_ability(
        owner=4,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 0x8038, 255],
        ability_index=0x805B,
        slot_count=4,
        navigate_to_equip_menu=True,
        close_menu=False,
        full_menu_close=False
    )
    menu.add_ability(
        owner=5,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 255, 255],
        ability_index=0x8038,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=False,
        full_menu_close=False
    )
    menu.add_ability(
        owner=5,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 0x8038, 255],
        ability_index=0x805B,
        slot_count=4,
        navigate_to_equip_menu=True,
        full_menu_close=False
    )
    memory.main.update_formation(Lulu, Wakka, Yuna, full_menu_close=False)
    navigate_to_airship_destination("Gagazet")

    # Fist, have to get to the cave.
    last_map = memory.main.get_map()
    checkpoint = 0
    while checkpoint < 23:
        if memory.main.get_map() != last_map:
            checkpoint += 2
            FFXC.set_neutral()
            logger.debug(f"Checkpoint update: {checkpoint}")
            last_map = memory.main.get_map()
        elif pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
            checkpoint += 1
            logger.debug(f"Checkpoint update: {checkpoint}")
    while not pathing.set_movement([-17,266]):
        pass
    FFXC.set_neutral()
    xbox.menu_b()
        
    # For the detour, we need the following:
    third_battle_complete = False
    detour = [
        [455,927],
        [627,928],
        [711,928]
    ]
    detour_cp = 0
    detour_dir = "forward"

    # Now tele to the back and start walking through Yojimbo battles.
    checkpoint = 49
    direction = 'exit'
    backup_aeon = 0
    while memory.main.get_map() != 266:
        if memory.main.user_control():
            if checkpoint == 48 and direction == 'save':
                # save_sphere.touch_and_go()
                direction = 'exit'
                checkpoint -= 1
            elif checkpoint == 38 and not third_battle_complete:
                logger.debug(f"{checkpoint} - Moving to {detour[detour_cp]}")
                if pathing.set_movement(detour[detour_cp]):
                    if detour_dir == "forward":
                        detour_cp += 1
                    else:
                        detour_cp -= 1
                if detour_cp == 3:  # Out of bounds
                    detour_cp = 2
                if detour_cp == -1:  # Out of bounds
                    third_battle_complete = True
                    # direction = 'save'
            elif pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                if direction == 'exit':
                    # if checkpoint == 48:
                    #     save_sphere.touch_and_go()
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint update: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                backup_aeon=battle.main.dark_aeon(backup_aeon=backup_aeon)
                
                if memory.main.game_over():
                    reset.reset_to_main_menu()
                    area.dream_zan.new_game(gamestate="reload_autosave")
                    logger.debug("Selecting save number.")
                    load_game.load_save_num(0)
                    while not pathing.set_movement([-17,266]):
                        pass
                    FFXC.set_neutral()
                    xbox.menu_b()
                    checkpoint = 49
                elif checkpoint == 38 and not third_battle_complete:
                    detour_dir = "back"
                    # direction = 'save'
                elif checkpoint < 47:
                    # direction = 'save'
                    pass
    
    split_timer()
    logger.warning(f"Escaped the cave.")
    # while not pathing.set_movement([-330,-159]):
    #     pass
    return_to_airship()

def dark_anima():
    if memory.main.get_map() == 307:
        return_to_airship()
    navigate_to_airship_destination("Gagazet")

    #Teleporter pad.
    while not pathing.set_movement([54,107]):
        pass
    FFXC.set_neutral()
    pathing.approach_coords([70,120], click_through=False)
    FFXC.set_neutral()
    memory.main.wait_frames(90)
    xbox.menu_down()
    xbox.tap_confirm()
    memory.main.click_to_control()
    equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    
    # Now tele to the back and start walking through Yojimbo battles.
    checkpoint = 2
    direction = 'f'
    while memory.main.get_map() != 259:
        if memory.main.user_control():
            if checkpoint == 12:
                # Trial
                while memory.main.user_control():
                    FFXC.set_movement(0,1)
                FFXC.set_neutral()
                logger.debug("Trial start")
                
                while not memory.main.user_control():
                    if memory.main.battle_active():
                        basic_quick_attacks(quick_return=True)
                    else:
                        logger.debug(f"{round(memory.main.gt_outer_ring(),2)} | {round(memory.main.gt_inner_ring(),2)}")
                        if (
                            memory.main.gt_outer_ring() > 3.1
                            # or memory.main.gt_outer_ring() < -3.0
                        ):
                            if (
                                memory.main.gt_inner_ring() < 2.9
                                and memory.main.gt_inner_ring() > 1.3
                            ):
                                logger.debug(f"Mark 1")
                                xbox.tap_confirm()
                            elif (
                                memory.main.gt_inner_ring() < 0.1
                                and memory.main.gt_inner_ring() > -1.6
                            ):
                                logger.debug(f"Mark 2")
                                xbox.tap_confirm()
                        # elif (
                        #     memory.main.gt_outer_ring() < -0.7
                        #     and memory.main.gt_outer_ring() > -1.1
                        # ):
                        #     if (
                        #         memory.main.gt_inner_ring() < 2.9
                        #         and memory.main.gt_inner_ring() > 1.3
                        #     ):
                        #         logger.debug(f"Mark 3")
                        #         xbox.tap_confirm()
                        #     elif (
                        #         memory.main.gt_inner_ring() < 0.1
                        #         and memory.main.gt_inner_ring() > -1.6
                        #     ):
                        #         logger.debug(f"Mark 4")
                        #         xbox.tap_confirm()

                checkpoint = 10
                direction = 'b'
                logger.debug(f"Checkpoint update: {checkpoint}")
            elif checkpoint == 7:
                if direction == 'f':
                    if memory.main.get_map() == 272:
                        FFXC.set_movement(0,1)
                    else:
                        checkpoint += 1
                else:
                    if memory.main.get_map() == 310:
                        FFXC.set_movement(0,-1)
                    else:
                        checkpoint -= 1
            elif checkpoint == 1:
                pathing.set_movement([111,-1040])
            elif pathing.set_movement(GagazetCave.execute(checkpoint)) is True:
                if direction == 'f':
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint update: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                basic_quick_attacks(quick_return=True)
            elif checkpoint == 1 and memory.main.diag_progress_flag() == 31:
                xbox.tap_confirm()
    
    logger.warning(f"Back to Gagazet Front")
    success = False
    while not success:
        memory.main.update_formation(Lulu, Wakka, Yuna)
        while not pathing.set_movement([60,40]):
            pass
        while memory.main.user_control():
            FFXC.set_movement(1,0)
        FFXC.set_neutral()
        memory.main.wait_frames(60)
        success = yojimbo_battle(flee_available=True, arena=False, anima=1)
        if not success:
            reset.reset_to_main_menu()
            area.dream_zan.new_game(gamestate="reload_autosave")
            logger.debug("Selecting save number.")
            load_game.load_save_num(0)
    split_timer()
    return_to_airship()

def penance():
    if memory.main.get_map() == 307:
        return_to_airship()
    memory.main.update_formation(Tidus, Wakka, Rikku)
    navigate_to_airship_destination("Penance")
    success = False
    while not success:
        success = yojimbo_battle(flee_available=True, arena=False, anima=1)
        if not success:
            reset.reset_to_main_menu()
            area.dream_zan.new_game(gamestate="reload_autosave")
            logger.debug("Selecting save number.")
            load_game.load_save_num(0)
    remove_airship_unlocked_location("Penance")

def primer_cleanup_1(sisters_return:bool=False, baaj:int=1):
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    
    if memory.main.get_map() == 307:
        return_to_airship()
    if sisters_return:
        write_big_text("Pathing to Dark Sisters")
    else:
        write_big_text("Primer & Jecht Sphere clean-up")
    if memory.main.get_map() == 374:
        # air_ship_destination(5+baaj)
        navigate_to_airship_destination("Djose")

        # Aftermath
        while not pathing.set_movement([301,-423]):
            pass
        while not pathing.set_movement([265,-416]):
            pass
        while not pathing.set_movement([253,-449]):
            pass
        last_map = memory.main.get_map()
        while last_map == memory.main.get_map():
            FFXC.set_movement(0,-1)

        # Behind Clasko
        while not pathing.set_movement([297,521]):
            pass
        while not pathing.set_movement([252,326]):
            pass
        while not pathing.set_movement([133,140]):
            pass
        while not pathing.set_movement([60,-11]):
            pass
        while not pathing.set_movement([-20,-355]):
            pass

    if sisters_return:
        return

    # Past dark sisters
    while not pathing.set_movement([-9,-603]):
        pass
    while not pathing.set_movement([-62,-675]):
        pass
    while not pathing.set_movement([-44,-704]):
        pass
    while not pathing.set_movement([-42,-828]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    
    # End of Highroad
    while not pathing.set_movement([-53,254]):
        pass
    while not pathing.set_movement([-66,-74]):
        pass
    while not pathing.set_movement([-142,-267]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    
    # Highroad section
    while not pathing.set_movement([608,382]):
        pass
    while not pathing.set_movement([582,320]):
        pass
    while not pathing.set_movement([322,216]):
        pass
    #while not pathing.set_movement([274,227]):
    #    pass
    pathing.approach_coords([255,225], use_raw_coords=True)
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([322,216]):
        pass
    while not pathing.set_movement([582,320]):
        pass
    while not pathing.set_movement([608,382]):
        pass
    while not pathing.set_movement([593,552]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    
    # Upper to lower
    while not pathing.set_movement([-68,-53]):
        pass
    while not pathing.set_movement([12,-61]):
        pass
    while not pathing.set_movement([140,-189]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,-1)

    # Lowroad 1
    path = [
        [699,330],
        [626,241],
        [532,178],
        [355,116],
        [217,134],
        [0,0],
        [4,-48],
        [8,-203],
        [114,-310],
        [199,-385],
        [181,-547],
        [25,-863],
        [23,-1075],
        [131,-1286],
        [104,-1527]
    ]
    for i in range(len(path)):
        if path[i] == [0,0]:
            last_map = memory.main.get_map()
            while last_map == memory.main.get_map():
                FFXC.set_movement(0,-1)
        else:
            while not pathing.set_movement(path[i]):
                pass
    
    pathing.approach_coords([115,-1565], use_raw_coords=True)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    pathing.approach_coords([90,-1570], use_raw_coords=True)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    for i in range(len(path)-1, -1, -1):
        if path[i] == [0,0]:
            last_map = memory.main.get_map()
            while last_map == memory.main.get_map():
                FFXC.set_movement(1,1)
        else:
            while not pathing.set_movement(path[i]):
                pass
            
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)

        
    # End of Highroad
    while not pathing.set_movement([167,-220]):
        pass
    while not pathing.set_movement([-5,-60]):
        pass
    while not pathing.set_movement([-52,213]):
        pass
    while not pathing.set_movement([-46,316]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(0,1)

    # Past dark sisters
    while not pathing.set_movement([-42,-828]):
        pass
    while not pathing.set_movement([-44,-704]):
        pass
    while not pathing.set_movement([-62,-675]):
        pass
    while not pathing.set_movement([-9,-603]):
        pass
    while not pathing.set_movement([-33,-504]):
        pass
    while not pathing.set_movement([-115,-477]):
        pass
    while not pathing.set_movement([-214,-410]):
        pass
    last_map = memory.main.get_map()
    while last_map == memory.main.get_map():
        FFXC.set_movement(1,1)
    
    # MRR path
    while not pathing.set_movement([-32,-700]):
        pass
    while not pathing.set_movement([-37,-602]):
        pass
    FFXC.set_neutral()
    while memory.main.user_control():
        xbox.tap_confirm()
    memory.main.await_control()
    while not pathing.set_movement([-48,-551]):
        pass
    while not pathing.set_movement([-116,-439]):
        pass
    while not pathing.set_movement([-85,-396]):
        pass
    while not pathing.set_movement([-89,-354]):
        pass
    while not pathing.set_movement([-9,-356]):
        pass
    while not pathing.set_movement([39,-426]):
        pass
    while not pathing.set_movement([116,-337]):
        pass
    while not pathing.set_movement([125,-165]):
        pass
    while not pathing.set_movement([85,-171]):
        pass
    while not pathing.set_movement([12,-221]):
        pass
    while not pathing.set_movement([-67,-191]):
        pass
    while not pathing.set_movement([-90,-143]):
        pass
    while not pathing.set_movement([-116,99]):
        pass
    while not pathing.set_movement([56,131]):
        pass
    while not pathing.set_movement([27,230]):
        pass
    while not pathing.set_movement([-98,330]):
        pass
    while not pathing.set_movement([-49,429]):
        pass
    while not pathing.set_movement([33,435]):
        pass
    while not pathing.set_movement([101,528]):
        pass
    while not pathing.set_movement([44,541]):
        pass
    while not pathing.set_movement([-66,573]):
        pass
    while not pathing.set_movement([-135,676]):
        pass
    while not pathing.set_movement([-69,746]):
        pass
    while not pathing.set_movement([-49,840]):
        pass
    while not pathing.set_movement([42,807]):
        pass
    while not pathing.set_movement([62,843]):
        pass
    while not pathing.set_movement([59,901]):
        pass
    FFXC.set_neutral()
    while memory.main.user_control():
        xbox.tap_confirm()

    # Upper area
    while not pathing.set_movement([-4,-201]):
        pass
    while not pathing.set_movement([96,-81]):
        pass
    while not pathing.set_movement([130,28]):
        pass
    while not pathing.set_movement([109,122]):
        pass

    # First, to get the primer.
    while not pathing.set_movement([26,132]):
        pass
    while not pathing.set_movement([-34,54]):
        pass
    while not pathing.set_movement([-67,58]):
        pass
    while not pathing.set_movement([-121,114]):
        pass
    while not pathing.set_movement([-102,157]):
        pass
    pathing.primer()
    while not pathing.set_movement([-102,157]):
        pass
    while not pathing.set_movement([-121,114]):
        pass
    while not pathing.set_movement([-67,58]):
        pass
    while not pathing.set_movement([-34,54]):
        pass
    while not pathing.set_movement([26,132]):
        pass

    #Lift
    while not pathing.set_movement([29,229]):
        pass
    FFXC.set_neutral()
    while memory.main.user_control():
        xbox.tap_confirm()
    while not pathing.set_movement([62,249]):
        pass
    while not pathing.set_movement([186,260]):
        pass
    while not pathing.set_movement([222,210]):
        pass
    while not pathing.set_movement([210,94]):
        pass
    while not pathing.set_movement([161,47]):
        pass
    pathing.approach_coords([142,44], use_raw_coords=True)
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([161,47]):
        pass
    while not pathing.set_movement([210,94]):
        pass
    
    return_to_airship()


def primer_cleanup_2():
    # air_ship_destination(13)  # Omega ruins
    navigate_to_airship_destination("Omega")

    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)

    path = [
        [-82,-985],
        [-85,-810],
        [-169,-754],
        [-345,-680],
        [-430,-566],
        [-433,-538],
        [-385,-468],
        [-313,-344],
        [-299,-236],
        [-276,-115],
        [-286,-8],
        [-176,69],
        [-74,109],
        [-25,118],
        [9,185],
        [42,285],
        [32,376],
        [31,517]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    pathing.approach_coords([8,576])
    FFXC.set_neutral()
    memory.main.click_to_control()

    
    for i in range(len(path)-1,-1,-1):
        while not pathing.set_movement(path[i]):
            pass
    
    return_to_airship()

def force_yojimbo_unlock():
    
    navigate_to_airship_destination("Gagazet")
    memory.main.update_formation(Tidus, Yuna, Wakka)
    checkpoint = 0
    while memory.main.get_map() not in [194, 374]:
        if memory.main.user_control():
            if checkpoint in [5, 14, 59]:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 19 and memory.main.get_map() == 56:
                checkpoint = 21
            elif checkpoint in [52, 53]:  # Glyph and Yojimbo
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                xbox.tap_b()
                memory.main.wait_frames(5)
                logger.warning("Yojimbo (3)")
                yojimbo_dialog()
                checkpoint = 54
                logger.warning(f"Yojimbo update (C): {checkpoint}")
            elif checkpoint == 55:  # Back to entrance
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                xbox.tap_b()
                memory.main.wait_frames(5)
                checkpoint += 1
            elif checkpoint == 62:
                return_to_airship()
            elif pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
    

def yojimbo_dialog():
    logger.debug("New Yojimbo Unlock function. (plat)")
    success = False
    while not memory.main.user_control():
        if memory.main.diag_progress_flag() == 0:
            logger.debug("Dialog box online.")
            memory.main.wait_frames(60)
            xbox.tap_up()
            xbox.tap_b()
        elif memory.main.diag_progress_flag() == 5:
            logger.debug("Gil amount is now online.")
            memory.main.wait_frames(12)
            xbox.tap_left()
            xbox.tap_up()
            xbox.tap_up()
            xbox.tap_up()
            xbox.tap_up()
            xbox.tap_up()
            xbox.tap_left()
            xbox.tap_up()
            xbox.tap_up()
            xbox.tap_b() 
            FFXC.set_neutral()  # just in case
        elif memory.main.name_aeon_ready() and not game_vars.yojimbo_unlocked():
            logger.debug("Naming aeon.")
            memory.main.wait_frames(12)
            xbox.name_aeon("Yojimbo")
            memory.main.wait_frames(12)
            game_vars.set_yojimbo_unlocked()
            success = True
        elif memory.main.diag_progress_flag() == 10 and not game_vars.yojimbo_unlocked():
            logger.debug("Wrong dialog. We already unlocked?!")
            game_vars.set_yojimbo_unlocked()
            success = False
        else:
            FFXC.set_neutral()
            xbox.tap_b()
    return success


def nova(checkpoint:int=0):
    if checkpoint == 0:
        rin_equip_dump()
        if not zan_ready():
            recharge_overdrives(align_zan=True)
        # air_ship_destination(13)  # Omega ruins
        navigate_to_airship_destination("Omega")

        memory.main.check_nea_armor()
        if not memory.main.equipped_armor_has_ability(
            char_num=game_vars.ne_armor(), ability_num=0x801D
        ):
            menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
        menu.equip_weapon(character=0, ability=32772,full_menu_close=True)  # Evade & Counter (Caldabolg)
        
        if not game_vars.yojimbo_unlocked():
            game_vars.set_yojimbo_unlocked()
        memory.main.update_formation(Tidus, Wakka, Rikku)
    
    armor_swap_tidus = memory.main.equipped_armor_has_ability(char_num=0)
    armor_swap_wakka = memory.main.equipped_armor_has_ability(char_num=4)
    next_aeon = 4
    get_primer = game_vars.platinum()

    last_map = memory.main.get_map()
    while memory.main.get_encounter_id() != 449:
        if memory.main.user_control():
            if checkpoint >= 28 and armor_swap_tidus:
                FFXC.set_neutral()
                menu.equip_armor(character=0, ability=0x800A)
                armor_swap_tidus = False
            if checkpoint >= 28 and armor_swap_wakka:
                FFXC.set_neutral()
                menu.equip_armor(character=4, ability=0x800A)
                armor_swap_wakka = False
            if last_map != memory.main.get_map():
                logger.debug(f"Map change: {memory.main.get_map()}")
                checkpoint += 2
                last_map = memory.main.get_map()
            elif checkpoint == 17 and get_primer:
                pathing.primer()
                get_primer = False
                checkpoint += 1
            else:
                # logger.debug(f"Moving towards: {path[checkpoint]}")
                if pathing.set_movement(OmegaFarm.execute(checkpoint)):
                    logger.debug(f"Checkpoint reached: {checkpoint}")
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.turn_ready():
                logger.warning(memory.main.get_encounter_id())
                if memory.main.get_encounter_id() in [440,442,445]:
                    battle.main.flee_all()
                else:
                    while memory.main.battle_active():
                        if memory.main.turn_ready():
                            if screen.turn_aeon():
                                CurrentPlayer().attack()
                            elif (
                                memory.main.get_encounter_id() == 439 and
                                memory.main.get_next_turn() == 20 and
                                not Yuna.active()
                            ):
                                battle.main.buddy_swap(Yuna)
                                battle.main.aeon_summon(next_aeon)
                                next_aeon -= 1
                            elif not Tidus.active():
                                battle.main.buddy_swap(Tidus)
                            elif Tidus.is_turn():
                                Tidus.quick_hit()
                            elif not Wakka.active():
                                battle.main.buddy_swap(Wakka)
                            elif Wakka.is_turn():
                                Wakka.defend()
                            elif not Rikku.active():
                                battle.main.buddy_swap(Rikku)
                            else:
                                CurrentPlayer().defend()
                    if memory.main.game_over():
                        last_map = memory.main.get_map()
                        while last_map == memory.main.get_map():
                            xbox.menu_b()
                        return False
                    battle.main.wrap_up()
                    memory.main.update_formation(Tidus, Wakka, Rikku)
                logger.warning(memory.main.get_encounter_id())
                if memory.main.game_over():
                    last_map = memory.main.get_map()
                    while last_map == memory.main.get_map():
                        xbox.menu_b()
                    return False
        
    # Now in battle with Omega.
    battle.main.lancet_omega()
    return_to_airship()
    return True


def grid_check():
    # After restocking, perform grid on any ready characters.
    ret_val = None
    remaining_array = [0] * 7
    for i in range(7):
        remaining_array[i] = count_still_locked(actor_id=i)
    for x in range(6,-1,-1):
        if remaining_array[x] != 0:
            levels = memory.sphere_grid.char_sphere_levels(x)
            if levels > 10:
                # if nearest_interesting_node(
                #     x,
                #     include_empty=fill_empty,
                #     locks=locks,
                #     target_node_id=destination
                # ) < levels:
                ret_val = max_level_ups(
                    x, 
                    include_empty=True, 
                    locks=4,
                    clear_luck=True
                )
                update_completion_report()
                logger.info(f"Level ups returned value: {ret_val}")
                if ret_val == "dest_reached":
                    return grid_check()
                elif ret_val == "low_spheres":
                    return ret_val
                elif ret_val == "low_filler_spheres":
                    return ret_val
        
        remaining_array[x] = count_still_locked(actor_id=x)
                
    if ret_val is None:
        ret_val = "normal_return"
    return ret_val
            

def grid_check_early(force=False):
    # logger.warning(memory.main.get_item_slot(86))
    # memory.main.wait_seconds(5)
    slot = memory.main.get_item_slot(86)
    if slot == 255:
        logger.debug("No MP spheres, we haven't reached that point yet. (C)")
        return
    count = memory.main.get_item_count_slot(slot)
    if count < 4:
        logger.debug("No MP spheres, we haven't reached that point yet. (D)")
        return

    grid_instance = get_grid() # Get the grid instance
    logger.debug(f"State: {game.state} | Step {game.step}")
    if game.state == 'Nem_Farm' and game.step >= 6:
        fill_empty = True
    elif game.state == 'Platinum' and game.step > 3:
        fill_empty = True
    else:
        fill_empty = False
    
    base_locks = 0
    if force:
        actor_array = [6]
    elif game.state == "Nem_Farm" and game.step >= 6:
        actor_array = [0,6,4]
        base_locks = 3
    else:
        actor_array = [5,1,6,4]
        base_locks = 0
    
    # Perform grid on any ready characters.
    for x in actor_array:  # We only really need these ones.
    # for x in range(6,0,-1):
        perform=True
        levels = memory.sphere_grid.char_sphere_levels(x)
        logger.warning(f"Checking grid for character {x}, Slvls: {levels}")
        for i in range(3):
            sphere_index = memory.main.get_item_slot(70+i)
            if sphere_index == 255:
                sphere_count = 0
            else:
                sphere_count = memory.main.get_item_count_slot(sphere_index)
            # logger.debug(f"Sphere {70+i}, slot {sphere_index}, count {sphere_count}")
            if sphere_count > 90:
                # logger.warning(f"Overflow, spheres type {70+i}.")
                force=True
            if sphere_count < 20:
                logger.warning(f"Not enough spheres of type {70+i}.")
                perform=False
        # logger.warning(f"Perform: {perform} | Force: {force}")
        # memory.main.wait_frames(120)
        if force or perform:
            perform=True
            # memory.main.wait_frames(120)
            if levels > 10:
                # open_grid(x)
                destination = None
                locks = base_locks
                if x == 6:
                    # Rikku has a specific path to follow.
                    if grid_instance.get_node(407).current_content_id == 0x28:
                        locks=4
                        destination=450
                    elif game.state == 'Nem_Farm' and game.step >= 8:
                        if not grid_instance.get_node(7).unlocked_by_characters['Rikku']:
                            logger.warning(f"Check 4: {grid_instance.get_node(7).unlocked_by_characters['Rikku']}")
                            destination=7
                            locks=3
                        elif not grid_instance.get_node(21).unlocked_by_characters['Rikku']:
                            logger.warning(f"Check 5: {grid_instance.get_node(21).unlocked_by_characters['Rikku']}")
                            destination=21
                        elif not grid_instance.get_node(405).unlocked_by_characters['Rikku']:
                            logger.warning(f"Check 2: {grid_instance.get_node(405).unlocked_by_characters['Rikku']}")
                            destination=406
                        elif grid_instance.get_node(1).current_content_id == 0x27:
                            logger.warning(f"Check 3: {grid_instance.get_node(1).current_content_id}")
                            if not grid_instance.get_node(679).unlocked_by_characters['Rikku']:
                                logger.warning(f"Subcheck 3-1")
                                destination=677
                            else:
                                logger.warning(f"Subcheck 3-2")
                                destination=680
                                locks=4
                        elif not grid_instance.get_node(705).unlocked_by_characters['Rikku']:
                            if not (game.state == 'Nem_Farm' and game.step <= 12):
                                logger.warning(f"Check 6: {grid_instance.get_node(705).unlocked_by_characters['Rikku']}")
                                destination=706
                    else:
                        perform=False
                if x == 1:
                    # Yuna needs Use and Steal. Mostly just Use, but whatever.
                    if not grid_instance.get_node(449).unlocked_by_characters['Yuna']:
                        destination=449
                    elif not grid_instance.get_node(450).unlocked_by_characters['Yuna']:
                        destination=449
                    else:
                        perform=False
                if x == 4:
                    # Let's get Wakka moving towards strength and hp.
                    if not grid_instance.get_node(742).unlocked_by_characters['Wakka']:
                        destination=743
                    elif not grid_instance.get_node(741).unlocked_by_characters['Wakka']:
                        destination=205
                    elif not grid_instance.get_node(580).unlocked_by_characters['Wakka']:
                        destination=581
                    elif not grid_instance.get_node(609).unlocked_by_characters['Wakka']:
                        destination=608
                    elif not grid_instance.get_node(705).unlocked_by_characters['Wakka']:
                        if not (game.state == 'Nem_Farm' and game.step <= 12):
                            destination=706
                
                # # In case we don't have a pre-planned path, path towards dead ends.
                # if destination == None:
                #     pref_path = grid_instance.find_path_to_nearest_dead_end(start_node=?, x)
                #     if pref_path is not None:
                #         destination = pref_path

                if perform:
                    ret_val = max_level_ups(
                        x, 
                        include_empty=fill_empty, 
                        locks=locks, 
                        dest_index=destination
                    )
                    logger.info(f"Level ups returned value: {ret_val}")
                    if ret_val == "dest_reached":
                        return grid_check_early()

def rikku_provoke():
    grid_instance = get_grid() # Get the grid instance
    while not grid_instance.get_node(21).unlocked_by_characters['Rikku']:
        logger.debug("Attempting to teach Rikku Provoke")
        grid_check_early(force=True)
