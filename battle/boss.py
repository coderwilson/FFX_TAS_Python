import battle.main
import logs
import memory.main
import screen
import vars
import xbox
import logging

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()

boss_log = logging.getLogger('battle.boss')

def ammes():
    BattleComplete = 0
    countAttacks = 0
    tidusODflag = False

    while BattleComplete != 1:
        if memory.main.turn_ready():
            if (
                not tidusODflag
                and screen.turn_tidus()
                and memory.main.get_overdrive_battle(0) == 100
            ):
                battle.overdrive.tidus()
                tidusODflag = True
            else:
                boss_log.info("Attacking Sinspawn Ammes")
                battle.main.attack("none")
                countAttacks += 1
        if memory.main.user_control():
            BattleComplete = 1
            boss_log.info("Ammes battle complete")


def tanker():
    boss_log.info("Fight start: Tanker")
    countAttacks = 0
    tidusCount = 0
    auronCount = 0
    xbox.click_to_battle()

    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                tidusCount += 1
                if tidusCount < 4:
                    xbox.weap_swap(0)
                else:
                    battle.main.attack("none")
                    countAttacks += 1
            elif screen.turn_auron():
                auronCount += 1
                if auronCount < 2:
                    battle.main.attack_self_tanker()
                else:
                    battle.main.attack("none")
                    countAttacks += 1
        elif memory.main.diag_skip_possible():
            xbox.tap_b()


def klikk():
    boss_log.info("Fight start: Klikk")
    klikkAttacks = 0
    klikkRevives = 0
    stealCount = 0
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            BattleHP = memory.main.get_battle_hp()
            if BattleHP[0] == 0:
                battle.main.revive()
                klikkRevives += 1
            elif screen.turn_tidus():
                if BattleHP[0] == 0 and memory.main.get_enemy_current_hp()[0] > 125:
                    battle.main.use_potion_character(0, "l")
                else:
                    battle.main.attack("none")
                klikkAttacks += 1
            elif screen.turn_rikku():
                grenadeCount = memory.main.get_item_count_slot(
                    memory.main.get_item_slot(35)
                )
                if (
                    BattleHP[0] < 120
                    and not (
                        memory.main.get_next_turn() == 0
                        and memory.main.get_enemy_current_hp()[0] <= 181
                    )
                    and not memory.main.rng_seed() == 160
                ):
                    battle.main.use_potion_character(0, "l")
                    klikkRevives += 1
                elif memory.main.get_enemy_current_hp()[0] < 58:
                    battle.main.attack("none")
                    klikkAttacks += 1
                elif grenadeCount < 6 and memory.main.next_steal(
                    steal_count=stealCount
                ):
                    boss_log.info("Attempting to steal from Klikk")
                    battle.main.steal()
                    stealCount += 1
                else:
                    battle.main.attack("none")
                    klikkAttacks += 1
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    boss_log.info("Klikk fight complete")
    boss_log.debug(f"map: {memory.main.get_map()}")
    while not (
        memory.main.get_map() == 71
        and memory.main.user_control()
        and memory.main.get_coords()[1] < 15
    ):
        # print(memory.main.getMap())
        if game_vars.csr():
            FFXC.set_value("BtnB", 1)
        else:
            xbox.tap_b()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.wait_frames(1)


def tros():
    logs.open_rng_track()
    boss_log.info("Fight start: Tros")
    FFXC.set_neutral()
    battleClock = 0
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
            battleClock += 1
            boss_log.debug(f"Battle clock: {battleClock}")
            trosPos = 2
            boss_log.debug("Determining Tros position")
            while trosPos == 2 and not memory.main.battle_complete():
                # Two for "not yet determined". Maybe can be HP-based instead?
                camera = memory.main.get_camera()
                # First, determine position of Tros
                if camera[0] > 2:
                    trosPos = 1  # One for cannot attack.
                    boss_log.debug("Tros is long-range. Cannot attack.")
                elif camera[0] < -2:
                    trosPos = 1  # One for cannot attack.
                    boss_log.debug("Tros is long-range. Cannot attack.")
                else:
                    trosPos = 0  # One for "Close range, can be attacked.
                    boss_log.debug("Tros is short-range.")

            # Assuming battle is not complete:
            if memory.main.battle_active():
                partyHP = memory.main.get_battle_hp()
                # Someone requires reviving.
                if partyHP[0] == 0 or partyHP[1] == 0:
                    boss_log.debug("Tros: Someone fainted.")
                    battle.main.revive()
                    Revives += 1
                elif screen.turn_rikku():
                    boss_log.debug("Rikku turn")
                    grenadeSlot = memory.main.get_item_slot(35)
                    grenadeCount = memory.main.get_item_count_slot(grenadeSlot)
                    boss_log.debug("------------------------------")
                    boss_log.debug(f"Current grenade count: {grenadeCount}")
                    boss_log.debug(f"Grenades used: {Grenades}")
                    boss_log.debug("------------------------------")
                    totalNades = grenadeCount + Grenades
                    if totalNades < 6:
                        if trosPos == 1:
                            battle.main.defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    elif grenadeCount == 0:
                        if trosPos == 1:
                            battle.main.defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    else:
                        if trosPos != 1 and advances in [1, 2]:
                            battle.main.steal()
                            Steals += 1
                        else:
                            grenadeSlot = memory.main.get_use_items_slot(35)
                            battle.main.use_item(grenadeSlot, "none")
                            Grenades += 1
                elif screen.turn_tidus():
                    boss_log.debug("Tidus turn")
                    if (
                        trosPos == 1
                        and memory.main.get_battle_hp()[1] < 200
                        and memory.main.get_enemy_current_hp()[0] > 800
                    ):
                        battle.main.use_potion_character(6, "l")
                    elif trosPos == 1 or memory.main.get_enemy_current_hp()[0] < 300:
                        battle.main.defend()
                    else:
                        battle.main.attack("none")
                        Attacks += 1

    boss_log.info("Tros battle complete.")
    memory.main.click_to_control()


def sin_fin():
    boss_log.info("Fight start: Sin's Fin")
    screen.await_turn()
    finTurns = 0
    kimTurn = False
    complete = False
    while not complete:
        if memory.main.turn_ready():
            finTurns += 1
            boss_log.debug("Determining first turn.")
            if screen.turn_tidus():
                battle.main.defend()
                boss_log.debug("Tidus defend")
            elif screen.turn_yuna():
                battle.main.buddy_swap_lulu()  # Yuna out, Lulu in
                battle.main.thunder_target(target=23, direction="r")
            elif screen.turn_kimahri():
                battle.main.lancet_target(target=23, direction="r")
                kimTurn = True
            elif screen.turn_lulu():
                battle.main.thunder_target(target=23, direction="r")
            else:
                battle.main.defend()
        if finTurns >= 3 and kimTurn:
            complete = True

    boss_log.info("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    turnCounter = 0
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            turnCounter += 1
            if screen.turn_kimahri():
                screen.await_turn()
                battle.main.lancet_target(23, "r")
            elif screen.turn_lulu():
                battle.main.thunder_target(23, "r")
            elif screen.turn_tidus():
                if turnCounter < 4:
                    battle.main.defend()
                    memory.main.wait_frames(30 * 0.2)
                else:
                    battle.main.buddy_swap_yuna()
                    battle.main.aeon_summon(0)
            elif screen.turn_aeon():
                battle.overdrive.valefor(sin_fin=1)
                boss_log.info("Valefor energy blast")
    boss_log.info("Sin's Fin fight complete")
    xbox.click_to_battle()


def echuilles():
    boss_log.info("Fight start: Sinspawn Echuilles")
    screen.await_turn()
    boss_log.info("Sinspawn Echuilles fight start")
    logs.write_rng_track("######################################")
    logs.write_rng_track("Echuilles start")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))

    tidusCounter = 0
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                battle.main.revive()
            elif screen.turn_tidus():
                tidusCounter += 1
                if tidusCounter <= 2:
                    boss_log.debug("Cheer")
                    battle.main.tidus_flee()  # performs cheer command
                elif (
                    memory.main.get_overdrive_battle(0) == 100
                    and memory.main.get_enemy_current_hp()[0] <= 750
                ):
                    boss_log.debug("Overdrive")
                    battle.overdrive.tidus()
                else:
                    boss_log.debug("Tidus attack")
                    battle.main.attack("none")
            elif screen.turn_wakka():
                if tidusCounter == 1:  # and memory.main.rngSeed() != 160:
                    boss_log.debug("Dark Attack")
                    battle.main.use_skill(0)  # Dark Attack
                # elif memory.main.get_enemy_current_hp()[0] <= 558:
                #    print("Ready for Tidus Overdrive. Wakka defends.")
                #    defend()
                else:
                    boss_log.debug("Wakka attack")
                    battle.main.attack("none")
    boss_log.info("Battle is complete. Now awaiting control.")
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
    logs.write_rng_track("######################################")
    logs.write_rng_track("Echuilles end")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))


def geneaux():
    boss_log.info("Fight start: Sinspawn Geneaux")
    xbox.click_to_battle()

    if screen.turn_tidus():
        battle.main.attack("none")
    elif screen.turn_yuna():
        battle.main.buddy_swap_kimahri()
        battle.main.attack("none")
        while not screen.turn_tidus():
            battle.main.defend()
        while screen.turn_tidus():
            battle.main.defend()
        battle.main.buddy_swap_yuna()
    screen.await_turn()
    battle.main.aeon_summon(0)  # Summon Valefor
    screen.await_turn()
    battle.overdrive.valefor()

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            boss_log.debug("Valefor casting Fire")
            battle.main.aeon_spell(0)
        else:
            FFXC.set_neutral()
    boss_log.info("Battle with Sinspawn Geneaux Complete")
    memory.main.click_to_control()


def oblitzerator(early_haste):
    boss_log.info("Fight start: Oblitzerator")
    xbox.click_to_battle()
    crane = 0

    if early_haste >= 1:
        # First turn is always Tidus. Haste Lulu if we've got the levels.
        battle.main.tidus_haste(direction="left", character=5)

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            if crane < 3:
                if screen.turn_lulu():
                    crane += 1
                    battle.main.thunder_target(target=21, direction="r")
                else:
                    battle.main.defend()
            elif crane == 3:
                if screen.turn_tidus():
                    crane += 1
                    while memory.main.main_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    battle.main.tap_targeting()
                elif screen.turn_lulu():
                    battle.main.thunder("none")
                else:
                    battle.main.defend()
            else:
                if screen.turn_lulu():
                    battle.main.thunder("none")
                elif screen.turn_tidus():
                    battle.main.attack_oblitz_end()
                else:
                    battle.main.defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    boss_log.info("End of fight, Oblitzerator")
    memory.main.click_to_control()
    # logs.writeStats("RNG02 after battle:")
    # logs.writeStats(memory.s32(memory.rng02()))


def chocobo_eater():
    boss_log.info("Fight start: Chocobo Eater")
    rng44Last = memory.main.rng_from_index(44)
    turns = 0
    chocoTarget = 255
    chocoNext = False
    chocoHaste = False
    screen.await_turn()
    charHpLast = memory.main.get_battle_hp()

    # If chocobo doesn't take the second turn, that means it out-sped Tidus.
    if memory.main.get_next_turn() != 20:
        if memory.main.rng_from_index(44) == rng44Last:
            # Eater did not take an attack, but did take first turn. Should register as true.
            chocoNext = True
    swappedYuna = False
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if chocoNext:
                chocoNext = False
                if memory.main.get_battle_hp() != charHpLast:  # We took damage
                    pass
                elif memory.main.rng_from_index(44) != rng44Last:
                    # Chocobo eater attacked, covers miss
                    pass
                elif (
                    chocoTarget == 255
                    and 1 not in memory.main.get_active_battle_formation()
                ):
                    chocoIndex = memory.main.actor_index(actor_num=4200)
                    boss_log.debug(f"#####  Chocobo index: {chocoIndex}")
                    chocoAngle = memory.main.get_actor_angle(chocoIndex)
                    if chocoAngle > 0.25:
                        boss_log.debug(f"#####  Chocobo angle: {chocoAngle}")
                        boss_log.debug("#####  Selecting friendly target 2")
                        chocoTarget = memory.main.get_active_battle_formation()[0]
                    elif chocoAngle < -0.25:
                        boss_log.debug(f"#####  Chocobo angle: {chocoAngle}")
                        boss_log.debug("#####  Selecting friendly target 0")
                        chocoTarget = memory.main.get_active_battle_formation()[2]
                    else:
                        boss_log.debug(f"#####  No Angle, using last hp's: {charHpLast}")
                        boss_log.debug("#####  Selecting friendly target 1")
                        chocoTarget = memory.main.get_active_battle_formation()[1]
            turns += 1
            if chocoTarget == memory.main.get_battle_char_turn():
                if 1 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_yuna()
                    battle.main.attack_by_num(1)
                    chocoTarget = 255
                    swappedYuna = True
            if memory.main.get_next_turn() == 20:
                chocoNext = True
                charHpLast = memory.main.get_battle_hp()
                rng44Last = memory.main.rng_from_index(44)
            if chocoTarget != 255:
                boss_log.debug(f"#####  Target for You're Next attack: {chocoTarget}")

            # Only if two people are down, very rare but for safety.
            if screen.faint_check() >= 2:
                boss_log.debug("Attempting revive")
                if screen.turn_kimahri():
                    if 0 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_tidus()
                    elif 4 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_wakka()
                    else:
                        battle.main.buddy_swap_auron()
                battle.main.revive()
            # elif 0 not in memory.main.getActiveBattleFormation():
            # Doesn't work - it still hits Tidus if he swapped out and back in (instead of Yuna).
            #    buddySwapTidus()
            elif (
                swappedYuna
                and 0 not in memory.main.get_active_battle_formation()
                and memory.main.state_dead(1)
                and not chocoHaste
            ):
                battle.main.buddy_swap_tidus()
            elif (
                1 in memory.main.get_active_battle_formation()
                and not chocoHaste
                and memory.main.get_battle_char_turn() == 0
            ):
                battle.main.tidus_haste(direction="l", character=20)
                # After Yuna in, haste choco eater.
                chocoHaste = True
            else:
                boss_log.debug("Attempting defend")
                battle.main.defend()
        elif memory.main.diag_skip_possible():
            boss_log.debug("Skipping dialog")
            xbox.tap_b()
    # logs.writeStats("Chocobo eater turns:")
    # logs.writeStats(str(turns))
    boss_log.info("Chocobo Eater battle complete.")


def gui():
    boss_log.info("Fight start: Sinspawn Gui")
    xbox.click_to_battle()
    boss_log.info("Engaging Gui")
    boss_log.debug(f"##### Expecting crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}")
    wakkaTurn = False
    yunaTurn = False
    auronTurn = False
    tidusTurn = False
    aeonTurn = False
    kimahriCrit = False

    while not aeonTurn:
        if memory.main.turn_ready():
            if screen.turn_yuna():
                if not yunaTurn:
                    battle.main.buddy_swap_auron()
                    yunaTurn = True
                else:
                    battle.main.aeon_summon(0)
            elif screen.turn_wakka():
                if not wakkaTurn:
                    xbox.weap_swap(0)
                    wakkaTurn = True
                else:
                    battle.main.buddy_swap_kimahri()
                    boss_log.debug(f"##### Expecting crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}")
            elif screen.turn_kimahri():
                dmgBefore = memory.main.get_enemy_current_hp()[0]
                battle.overdrive.kimahri(2)
                screen.await_turn()
                dmgAfter = memory.main.get_enemy_current_hp()[0]
                damage = dmgBefore - dmgAfter
                boss_log.debug(f"Kimahri OD damage: {damage}")
                logs.write_stats("guiCrit:")
                if damage > 6000:
                    kimahriCrit = True
                    logs.write_stats("True")
                else:
                    logs.write_stats("False")
            elif screen.turn_tidus():
                if not tidusTurn:
                    battle.main.defend()
                    tidusTurn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap_kimahri()
                else:
                    battle.main.buddy_swap_yuna()
            elif screen.turn_auron():
                if not auronTurn:
                    battle.main.use_skill(0)
                    auronTurn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap_yuna()
                else:
                    battle.main.defend()
            elif screen.turn_aeon():
                battle.overdrive.valefor()
                aeonTurn = True

    screen.await_turn()
    nextHP = memory.main.get_battle_hp()[0]
    lastHP = nextHP
    turn1 = False
    nextTurn = 20
    lastTurn = 20
    went = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready() and memory.main.get_battle_char_turn() == 8:
            nextHP = memory.main.get_battle_hp()[0]
            lastTurn = nextTurn
            nextTurn = memory.main.get_next_turn()
            if went and kimahriCrit:
                battle.main.aeon_spell(1)
            elif memory.main.get_overdrive_battle(8) == 20:
                boss_log.debug("------Overdriving")
                battle.overdrive.valefor()
                went = True
            elif not turn1:
                turn1 = True
                boss_log.debug("------Recharge unsuccessful. Attempting recovery.")
                battle.main.aeon_shield()
            elif lastTurn == 8:  # Valefor takes two turns in a row
                boss_log.debug("------Two turns in a row")
                battle.main.aeon_shield()
            elif nextHP > lastHP - 40 and not nextHP == lastHP:
                # Gravity spell was used
                boss_log.debug("------Gravity was used")
                battle.main.aeon_shield()
            else:
                boss_log.debug("------Attack was just used. Now boost.")
                battle.main.aeon_boost()
            lastHP = nextHP
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 1:
            boss_log.warning("Yuna turn, something went wrong.")
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 2:
            boss_log.warning("Auron turn, something went wrong.")
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
            boss_log.info("Skipping scene")
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()

    # Second Gui battle
    seymourTurn = 0
    if (
        memory.main.get_overdrive_battle(8) == 20
        or memory.main.get_overdrive_battle(1) == 100
    ):
        boss_log.info("Gui2 - with extra Aeon overdrive")
        while memory.main.battle_active():
            if screen.turn_seymour() and seymourTurn < 2:
                battle.main.seymour_spell(target_face=False)
                seymourTurn += 1
            elif screen.turn_yuna() and seymourTurn >= 2:
                boss_log.debug("Laser Time")
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
                boss_log.debug("Firing")
                battle.overdrive.valefor()
            else:
                boss_log.debug("Defend")
                battle.main.defend()
    else:
        boss_log.info("Gui2 - standard")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_seymour():
                    battle.main.seymour_spell(target_face=True)
                else:
                    battle.main.defend()

    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            boss_log.debug("Intentional delay to get the cutscene skip to work.")
            memory.main.wait_frames(2)
            xbox.skip_scene_spec()
            memory.main.wait_frames(60)
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()


def extractor():
    boss_log.info("Fight start: Extractor")
    FFXC.set_neutral()

    screen.await_turn()
    battle.main.tidus_haste("none")

    screen.await_turn()
    battle.main.attack("none")  # Wakka attack

    screen.await_turn()
    battle.main.tidus_haste("l", character=4)

    cheerCount = 0
    while not memory.main.battle_complete():  # AKA end of battle screen
        # First determine if cheers are needed.
        if game_vars.get_l_strike() % 2 == 0 and cheerCount < 4:
            tidusCheer = True
        elif game_vars.get_l_strike() % 2 == 1 and cheerCount < 1:
            tidusCheer = True
        else:
            tidusCheer = False
        # Then do the battle logic.
        if memory.main.special_text_open():
            xbox.tap_b()
        elif memory.main.turn_ready():
            if (
                screen.faint_check() > 0
                and memory.main.get_enemy_current_hp()[0] > 1100
            ):
                battle.main.revive()
            elif screen.turn_tidus():
                print(memory.main.get_actor_coords(3))
                if tidusCheer:
                    cheerCount += 1
                    battle.main.cheer()
                elif (
                    memory.main.get_enemy_current_hp()[0] < 1400
                    and not screen.faint_check()
                    and memory.main.get_overdrive_battle(4) == 100
                ):
                    battle.main.defend()
                else:
                    battle.main.attack("none")
            else:
                if (
                    memory.main.get_enemy_current_hp()[0] < 1900
                    and memory.main.get_overdrive_battle(4) == 100
                ):
                    battle.overdrive.wakka()
                else:
                    battle.main.attack("none")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    memory.main.click_to_control()


# Process written by CrimsonInferno
def spherimorph():
    boss_log.info("Fight start: Spherimorph")
    xbox.click_to_battle()

    FFXC.set_neutral()

    spellNum = 0
    tidusturns = 0
    rikkuturns = 0
    yunaTurn = False
    kimTurn = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if game_vars.use_pause():
                memory.main.wait_frames(2)
            turnchar = memory.main.get_battle_char_turn()
            partyHP = memory.main.get_battle_hp()
            if turnchar == 0:
                if tidusturns == 0:
                    battle.main.equip_in_battle(equip_type="armor", ability_num=0x8028)
                elif tidusturns == 1:
                    battle.main.defend()
                else:
                    battle.main.buddy_swap_rikku()
                tidusturns += 1
            elif turnchar == 1:
                rikkuslotnum = memory.main.get_battle_char_slot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    battle.main.revive()
                    yunaTurn = True
                elif not yunaTurn:
                    battle.main.defend()
                    yunaTurn = True
                elif not battle.main.spheri_spell_item_ready():
                    if 5 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_lulu()
                    elif 6 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_rikku()
                    else:
                        battle.main.defend()
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                else:
                    battle.main.defend()
                    yunaTurn = True
            elif turnchar == 3:
                rikkuslotnum = memory.main.get_battle_char_slot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    battle.main.revive()
                    kimTurn = True
                elif not kimTurn:
                    boss_log.debug(f"RNG11 before Spherimorph: {memory.main.rng_array_from_index(index=11, array_len=30)}")
                    logs.write_rng_track("RNG11 before Spherimorph")
                    logs.write_rng_track(
                        memory.main.rng_array_from_index(index=11, array_len=30)
                    )
                    # if memory.main.nextStealRare(preAdvance=6):
                    # One each for Spherimorph, Negator, Crawler, and guados.
                    # Except we haven't learned Steal yet. That's no good.
                    #    _steal()
                    # else:
                    battle.main.defend()
                    kimTurn = True
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                elif 5 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_lulu()
                else:
                    battle.main.defend()
            elif turnchar == 5:
                if not battle.main.spheri_spell_item_ready():
                    if spellNum == 1:
                        battle.main.ice()
                    elif spellNum == 2:
                        battle.main.water()
                    elif spellNum == 3:
                        battle.main.thunder()
                    else:
                        battle.main.fire()
                    screen.await_turn()
                    if memory.main.get_char_weakness(20) == 1:
                        spellNum = 4  # Ice
                    elif memory.main.get_char_weakness(20) == 2:
                        spellNum = 1  # Fire
                    elif memory.main.get_char_weakness(20) == 4:
                        spellNum = 3  # Water
                    elif memory.main.get_char_weakness(20) == 8:
                        spellNum = 2  # Thunder
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                else:
                    battle.main.defend()
            elif turnchar == 6:
                if rikkuturns == 0:
                    boss_log.debug("Throwing Grenade to check element")
                    grenadeslotnum = memory.main.get_use_items_slot(35)
                    battle.main.use_item(grenadeslotnum, "none")
                    if memory.main.get_char_weakness(20) == 1:
                        spellNum = 4  # Ice
                    elif memory.main.get_char_weakness(20) == 2:
                        spellNum = 1  # Fire
                    elif memory.main.get_char_weakness(20) == 4:
                        spellNum = 3  # Water
                    elif memory.main.get_char_weakness(20) == 8:
                        spellNum = 2  # Thunder

                    # spellNum = screen.spherimorphSpell()
                elif not battle.main.spheri_spell_item_ready():
                    if 5 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_lulu()
                    else:
                        battle.main.defend()
                else:
                    boss_log.debug("Starting Rikkus overdrive")
                    # logs.writeStats("Spherimorph spell used:")
                    if spellNum == 1:
                        # ogs.writeStats("Fire")
                        boss_log.debug("Creating Ice")
                        battle.main.rikku_full_od("spherimorph1")
                    elif spellNum == 2:
                        # logs.writeStats("Water")
                        boss_log.debug("Creating Water")
                        battle.main.rikku_full_od("spherimorph2")
                    elif spellNum == 3:
                        # logs.writeStats("Thunder")
                        boss_log.debug("Creating Thunder")
                        battle.main.rikku_full_od("spherimorph3")
                    elif spellNum == 4:
                        # logs.writeStats("Ice")
                        boss_log.debug("Creating Fire")
                        battle.main.rikku_full_od("spherimorph4")

                rikkuturns += 1

    if not game_vars.csr():
        xbox.skip_dialog(5)


def crawler():
    boss_log.info("Starting battle with Crawler")
    xbox.click_to_battle()

    if memory.main.next_steal_rare(pre_advance=5):
        # One each for two Negators, Crawler, and guados.
        battle.main.negator_with_steal()
    else:
        tidusturns = 0
        rikkuturns = 0
        kimahriturns = 0
        luluturns = 0
        yunaturns = 0

        while not memory.main.turn_ready():
            pass
        while memory.main.battle_active():  # AKA end of battle screen
            FFXC.set_neutral()
            if memory.main.turn_ready():
                turnchar = memory.main.get_battle_char_turn()
                if turnchar == 0:
                    if tidusturns == 0:
                        boss_log.debug("Swapping Tidus for Rikku")
                        battle.main.buddy_swap_rikku()
                    else:
                        battle.main.defend()
                    tidusturns += 1
                elif turnchar == 6:
                    if luluturns < 2:
                        boss_log.debug("Using Lightning Marble")
                        lightningmarbleslot = memory.main.get_use_items_slot(30)
                        if rikkuturns < 1:
                            battle.main.use_item(lightningmarbleslot, target=21)
                        else:
                            battle.main.use_item(lightningmarbleslot, target=21)
                    else:
                        boss_log.debug("Starting Rikkus overdrive")
                        battle.main.rikku_full_od("crawler")
                    rikkuturns += 1
                elif turnchar == 3:
                    if kimahriturns == 0:
                        lightningmarbleslot = memory.main.get_use_items_slot(30)
                        battle.main.use_item(lightningmarbleslot, target=21)
                    else:
                        battle.main.buddy_swap_yuna()
                    kimahriturns += 1
                elif turnchar == 5:
                    battle.main.revive()
                    luluturns += 1
                elif turnchar == 1:
                    if yunaturns == 0:
                        battle.main.defend()
                    else:
                        battle.main.buddy_swap_tidus()
                    yunaturns += 1
                else:
                    battle.main.defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    memory.main.click_to_control()


def wendigo():
    boss_log.info("Starting battle with Wendigo")

    phase = 0
    YunaAP = False
    guadosteal = False
    powerbreak = False
    powerbreakused = False
    usepowerbreak = False
    tidushealself = False
    tidusmaxHP = 1520
    tidushaste = False

    screen.await_turn()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            partyHP = memory.main.get_battle_hp()
            turnchar = memory.main.get_battle_char_turn()
            tidusSlot = memory.main.get_battle_char_slot(0)

            if partyHP[memory.main.get_battle_char_slot(0)] == 0:
                boss_log.debug("Tidus is dead")
                tidushaste = False
                powerbreak = True
                usepowerbreak = powerbreak and not powerbreakused

            if turnchar == 1:
                boss_log.debug("Yunas Turn")
                # If Yuna still needs AP:
                if not YunaAP:
                    boss_log.debug("Yuna still needs AP")
                    # If both other characters are dead Mega-Phoenix if available, otherwise PD
                    if (
                        battle.main.wendigo_res_heal(
                            turnchar=turnchar,
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidusmaxHP,
                        )
                        == 0
                    ):
                        xbox.weap_swap(0)
                    YunaAP = True
                # If Yuna has had a turn swap for Lulu
                else:
                    if 5 not in memory.main.get_active_battle_formation():
                        boss_log.debug("Swapping to Lulu")
                        battle.main.buddy_swap_lulu()
                    elif 6 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_rikku()
                    else:
                        xbox.weap_swap(0)
            elif turnchar == 0:
                if not tidushaste:
                    boss_log.debug("Tidus Haste self")
                    battle.main.tidus_haste("none")
                    tidushaste = True
                elif phase == 0:
                    boss_log.debug("Switch to Brotherhood")
                    battle.main.equip_in_battle(special="brotherhood")
                    phase += 1
                elif phase == 1:
                    boss_log.debug("Attack top Guado")
                    battle.main.attack_by_num(22, "d")
                    phase += 1
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and screen.faint_check() == 2
                ):
                    boss_log.debug("2 Characters are dead")
                    tidushealself = True
                    if memory.main.get_throw_items_slot(7) < 255:
                        battle.main.revive_all()
                    elif memory.main.get_throw_items_slot(6) < 255:
                        battle.main.revive()
                elif (
                    memory.main.get_enemy_current_hp()[1] < 6000
                    and memory.main.get_overdrive_battle(0) == 100
                    and not game_vars.skip_kilika_luck()
                ):
                    battle.overdrive.tidus("left", character=21)
                elif tidushealself:
                    if partyHP[memory.main.get_battle_char_slot(0)] < tidusmaxHP:
                        boss_log.debug(
                            "Tidus just used Phoenix Down / Mega Phoenix so needs to heal himself"
                        )
                        if battle.main.fullheal(target=0, direction="l") == 0:
                            if screen.faint_check():
                                boss_log.debug("No healing items so revive someone instead")
                                battle.main.revive()
                            else:
                                boss_log.debug("No healing items so just go face")
                                battle.main.attack_by_num(21, "l")
                    else:
                        boss_log.debug("No need to heal. Ver 1")
                        battle.main.attack_by_num(21, "l")
                    tidushealself = False
                else:
                    boss_log.debug("No need to heal. Ver 2")
                    battle.main.attack_by_num(21, "l")
                memory.main.wait_frames(30 * 0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = memory.main.get_use_items_slot(57)
                    if lightcurtainslot < 255:
                        boss_log.debug("Using Light Curtain on Tidus")
                        battle.main.use_item(lightcurtainslot, target=0)
                    else:
                        boss_log.debug("No Light Curtain")
                        boss_log.debug("Swapping to Auron to Power Break")
                        battle.main.buddy_swap_auron()  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                # elif memory.main.get_enemy_current_hp()[1] < stopHealing:
                #    defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidusmaxHP,
                    )
                    == 0
                ):
                    if (
                        not guadosteal
                        and memory.main.get_enemy_current_hp().count(0) != 2
                    ):
                        battle.main.steal()
                        guadosteal = True
                    # elif memory.main.get_enemy_current_hp().count(0) == 2 and not 5 in memory.main.getActiveBattleFormation():
                    #    buddySwapLulu()
                    else:
                        battle.main.defend()
            elif turnchar == 2:
                if usepowerbreak:
                    boss_log.debug("Using Power Break")
                    battle.main.use_skill(position=0, target=21)
                    powerbreakused = True
                    usepowerbreak = False
                # elif memory.main.get_enemy_current_hp()[1] < stopHealing and memory.main.getBattleHP()[tidusSlot] != 0:
                #    defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidusmaxHP,
                    )
                    == 0
                ):
                    battle.main.buddy_swap_kimahri()
            elif turnchar == 5:
                if (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidusmaxHP,
                    )
                    == 0
                ):
                    xbox.weap_swap(0)
            else:
                if (
                    usepowerbreak
                    and not powerbreakused
                    and 2 not in memory.main.get_active_battle_formation()
                ):
                    boss_log.debug("Swapping to Auron to Power Break")
                    battle.main.buddy_swap_auron()
                # if memory.main.get_enemy_current_hp()[1] < stopHealing and memory.main.getBattleHP()[tidusSlot] != 0:
                #    boss_log.debug("End of battle, no need to heal.")
                #    defend()
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and memory.main.get_battle_hp()[tidusSlot] != 0
                ):
                    if (
                        battle.main.wendigo_res_heal(
                            turnchar=turnchar,
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidusmaxHP,
                        )
                        == 0
                    ):
                        battle.main.defend()
                else:
                    battle.main.defend()


# Process written by CrimsonInferno
def evrae():
    boss_log.info("Starting battle: Evrae")
    tidusPrep = 0
    tidusAttacks = 0
    rikkuTurns = 0
    kimahriTurns = 0
    lunarCurtain = False
    if memory.main.rng_seed() == 31:
        stealCount = 2
    else:
        stealCount = 0
    FFXC.set_neutral()
    # This gets us past the tutorial and all the dialog.
    xbox.click_to_battle()

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            turnchar = memory.main.get_battle_char_turn()
            boss_log.debug(f"Tidus prep turns: {tidusPrep}")
            if turnchar == 0:
                boss_log.debug("Registering Tidus' turn")
                if game_vars.skip_kilika_luck():
                    if tidusPrep == 0:
                        tidusPrep = 1
                        battle.main.tidus_haste("none")
                    elif tidusPrep in [1, 2]:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif (
                        tidusAttacks == 4
                        or memory.main.get_enemy_current_hp()[0] <= 9999
                    ):
                        tidusAttacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
                elif game_vars.get_blitz_win():  # Blitz win logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        battle.main.tidus_haste("none")
                    elif tidusPrep == 1:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif tidusPrep == 2 and rikkuTurns == 0:
                        tidusPrep += 1
                        battle.main.equip_in_battle(
                            equip_type="armor", ability_num=0x8028
                        )
                    elif tidusPrep == 2 and tidusAttacks == 2:
                        tidusPrep += 1
                        battle.main.cheer()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
                else:  # Blitz loss logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        battle.main.tidus_haste("none")
                    elif tidusPrep <= 2:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif tidusPrep == 3:
                        boss_log.debug("Equip Baroque Sword.")
                        battle.main.equip_in_battle(special="baroque")
                        tidusPrep += 1
                    elif tidusAttacks == 4 and game_vars.skip_kilika_luck():
                        tidusAttacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
            elif turnchar == 6:
                boss_log.debug("Registering Rikkus turn")
                if rikkuTurns == 0:
                    rikkuTurns += 1
                    boss_log.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Evrae")
                elif not game_vars.get_blitz_win() and not lunarCurtain:
                    boss_log.debug("Use Lunar Curtain")
                    lunarSlot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunarSlot, direction="l", target=0)
                    lunarCurtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidusAttacks < 3 or not game_vars.get_blitz_win()):
                    boss_log.debug("Rikku should attempt to heal a character.")
                    kimahriTurns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        boss_log.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        boss_log.debug("Heal should be successful.")
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throwSlot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throwSlot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throwSlot = memory.main.get_use_items_slot(27)
                    else:
                        throwSlot = memory.main.get_use_items_slot(30)
                    if throwSlot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throwSlot)
                else:
                    battle.main.steal()
                    stealCount += 1
            elif turnchar == 3:
                boss_log.debug("Registering Kimahri's turn")
                if not game_vars.get_blitz_win() and not lunarCurtain:
                    boss_log.debug("Use Lunar Curtain")
                    lunarSlot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunarSlot, direction="l", target=0)
                    lunarCurtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidusAttacks < 3 or not game_vars.get_blitz_win()):
                    boss_log.debug("Kimahri should attempt to heal a character.")
                    kimahriTurns += 1
                    if battle.main.fullheal(target=0, direction="u") == 0:
                        boss_log.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        boss_log.debug("Heal should be successful.")
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throwSlot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throwSlot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throwSlot = memory.main.get_use_items_slot(27)
                    else:
                        throwSlot = memory.main.get_use_items_slot(30)
                    if throwSlot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throwSlot)
                else:
                    battle.main.steal()
                    stealCount += 1
        elif memory.main.diag_skip_possible():
            xbox.tap_b()

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            if memory.main.menu_open():
                xbox.tap_b()
        xbox.skip_scene_spec()


def isaaru():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() < 258:
        game_vars.add_rescue_count()

    boss_log.info("Starting battle: Isaaru")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.turn_yuna():
                if memory.main.get_encounter_id() in [257, 260]:
                    battle.main.aeon_summon(2)  # Summon Ixion for Bahamut
                else:
                    battle.main.aeon_summon(4)  # Summon Bahamut for other aeons
            else:
                battle.main.attack("none")  # Aeon turn
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    FFXC.set_value("BtnB", 1)
    memory.main.wait_frames(30 * 2.8)
    FFXC.set_value("BtnB", 0)


def evrae_altana():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() != 266:
        boss_log.info("Not Evrae this time.")
        battle.main.flee_all()
    else:
        boss_log.info("Evrae Altana fight start")
        if memory.main.next_steal_rare():
            battle.main.evrae_altana_steal()
        else:
            boss_log.debug("===================================")
            boss_log.debug("Next steal will crit, do not steal.")
            boss_log.debug("===================================")
        thrownItem = False
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                if memory.main.get_item_slot(18) != 255 and not thrownItem:
                    battle.main._use_healing_item(item_id=18)
                    thrownItem = True
                elif memory.main.get_item_slot(16) != 255 and not thrownItem:
                    battle.main._use_healing_item(item_id=16)
                    thrownItem = True
                else:
                    battle.main.altana_heal()

    memory.main.click_to_control()


def seymour_natus():
    aeonSummoned = False
    while not memory.main.user_control():
        if memory.main.get_encounter_id() == 272:  # Seymour Natus
            boss_log.info("Seymour Natus engaged")
            while not memory.main.battle_complete():
                if memory.main.turn_ready():
                    if screen.turn_tidus():
                        if memory.main.get_lulu_slvl() < 35 or game_vars.nemesis():
                            battle.main.buddy_swap_lulu()
                            screen.await_turn()
                            xbox.weap_swap(0)
                        elif aeonSummoned:
                            battle.main.tidus_haste("d", character=1)
                        else:
                            battle.main.attack("none")
                    elif screen.turn_lulu():
                        battle.main.buddy_swap_tidus()
                        screen.await_turn()
                        xbox.tap_up()
                        battle.main.attack("none")
                    elif screen.turn_yuna():
                        if not aeonSummoned:
                            battle.main.aeon_summon(4)
                            aeonSummoned = True
                        else:
                            battle.main.aeon_summon(2)
                    elif screen.turn_aeon():
                        xbox.skip_dialog(3)  # Finishes the fight.
                    else:
                        battle.main.defend()
            return 1
        elif memory.main.get_encounter_id() == 270:  # YAT-63 x2
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack_by_num(22, "r")
                    else:
                        battle.main.defend()
        elif memory.main.get_encounter_id() == 269:  # YAT-63 with two guard guys
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack("none")
                    else:
                        battle.main.defend()
        elif memory.main.get_encounter_id() == 271:  # one YAT-63, two YAT-99
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack_by_num(21, "l")
                    else:
                        battle.main.defend()
        if memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
    return 0


def biran_yenke():
    boss_log.info("Starting battle with Biran & Yenke")
    xbox.click_to_battle()
    battle.main.steal()

    # Nemesis logic
    if game_vars.nemesis():
        screen.await_turn()
        battle.main.steal_right()

    screen.await_turn()
    gemSlot = memory.main.get_use_items_slot(34)
    if gemSlot == 255:
        gemSlot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gemSlot, "none")

    xbox.click_to_battle()
    gemSlot = memory.main.get_use_items_slot(34)
    if gemSlot == 255:
        gemSlot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gemSlot, "none")

    while not memory.main.user_control():
        xbox.tap_b()

    retSlot = memory.main.get_item_slot(96)  # Return sphere
    friendSlot = memory.main.get_item_slot(97)  # Friend sphere

    if friendSlot == 255:  # Four return sphere method.
        boss_log.debug("Double return sphere drops.")
        endGameVersion = 4
    elif retSlot == 255:
        boss_log.warning("Double friend sphere, effective game over. :( ")
        endGameVersion = 3
    else:
        boss_log.debug("Split items between friend and return spheres.")
        endGameVersion = 1

    game_vars.end_game_version_set(endGameVersion)


def seymour_flux():
    stage = 1
    boss_log.info("Start: Seymour Flux battle")
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    boss_log.debug(f"Next Aeon Crit: {bahamut_crit}")
    yunaXP = memory.main.get_slvl_yuna()
    xbox.click_to_battle()
    if bahamut_crit == 2:
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                if screen.turn_aeon():
                    battle.main.attack("none")
                elif screen.turn_yuna():
                    battle.main.aeon_summon(4)
                else:
                    battle.main.defend()
    elif game_vars.end_game_version() == 3:
        bahamutSummoned = False
        while not memory.main.battle_complete():  # AKA end of battle screen
            if memory.main.turn_ready():
                if screen.turn_tidus():
                    battle.main.buddy_swap_yuna()
                elif screen.turn_yuna():
                    if not bahamutSummoned:
                        battle.main.aeon_summon(4)
                        bahamutSummoned = True
                    else:
                        battle.main.attack("none")
                elif screen.turn_aeon():
                    if game_vars.get_blitz_win():
                        battle.main.attack("none")
                    else:
                        battle.main.impulse()
                elif screen.faint_check() >= 1:
                    battle.main.revive()
                else:
                    battle.main.defend()
    else:
        while not memory.main.battle_complete():  # AKA end of battle screen
            if memory.main.turn_ready():
                lastHP = memory.main.get_enemy_current_hp()[0]
                boss_log.debug("Last HP")
                if screen.turn_yuna():
                    boss_log.debug(f"Yunas turn. Stage: {stage}")
                    if stage == 1:
                        battle.main.attack("none")
                        stage += 1
                    elif stage == 2:
                        battle.main.aeon_summon(4)
                        battle.main.attack("none")
                        stage += 1
                    else:
                        battle.main.attack("none")
                elif screen.turn_tidus():
                    boss_log.debug(f"Tidus' turn. Stage: {stage}")
                    if stage < 3:
                        battle.main.tidus_haste("down", character=1)
                    elif lastHP > 3500:
                        battle.main.attack("none")
                    else:
                        battle.main.defend()
                elif screen.turn_auron():
                    boss_log.debug("Auron's turn. Swap for Rikku and overdrive.")
                    battle.main.buddy_swap_rikku()
                    boss_log.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Flux")
                else:
                    boss_log.debug("Non-critical turn. Defending.")
                    battle.main.defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.click_to_control()
    if memory.main.get_slvl_yuna() - yunaXP == 15000:
        game_vars.flux_overkill_success()
    boss_log.info("-----------------------------")
    boss_log.info(f"Flux Overkill: {game_vars.flux_overkill()}")
    boss_log.info("Seymour Flux battle complete.")
    boss_log.info("-----------------------------")
    # time.sleep(60) #Testing only

def s_keeper_bahamut_crit() -> int:
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    boss_log.debug(f"Next Aeon Crit: {bahamut_crit}")
    return bahamut_crit


def s_keeper():
    xbox.click_to_battle()
    boss_log.info("Start of Sanctuary Keeper fight")
    s_keeper_bahamut_crit()
    xbox.click_to_battle()
    bahamut_crit = s_keeper_bahamut_crit()
    if bahamut_crit == 2 or bahamut_crit == 7:
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_aeon():
                    battle.main.attack("none")
                elif screen.turn_yuna():
                    battle.main.aeon_summon(4)
                else:
                    battle.main.defend()
    elif game_vars.end_game_version() == 3 and game_vars.get_blitz_win():
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_yuna():
                    battle.main.aeon_summon(4)
                elif screen.turn_aeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    else:
        armorBreak = False
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_tidus():
                    battle.main.use_skill(0)
                    armorBreak = True
                elif screen.turn_yuna():
                    if armorBreak:
                        battle.main.aeon_summon(4)
                    else:
                        battle.main.defend()
                elif screen.turn_aeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    memory.main.click_to_control()


def omnis():
    boss_log.info("Fight start: Seymour Omnis")
    xbox.click_to_battle()
    battle.main.defend()  # Yuna defends
    rikkuIn = False
    backupCure = False

    while memory.main.get_enemy_max_hp()[0] == memory.main.get_enemy_current_hp()[0]:
        if memory.main.turn_ready():
            if screen.turn_tidus():
                battle.main.use_skill(0)
            elif screen.turn_auron():
                battle.main.buddy_swap_rikku()
                battle.main.rikku_full_od(battle="omnis")
                rikkuIn = True
            elif screen.turn_yuna() and rikkuIn:
                if not backupCure:
                    battle.main.yuna_cure_omnis()
                    backupCure = True
                else:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8001, character=1
                    )
            else:
                battle.main.defend()

    boss_log.debug("Ready for aeon.")
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            boss_log.debug(f"Character turn: {memory.main.get_battle_char_turn()}")
            if screen.turn_yuna():
                battle.main.aeon_summon(4)
            elif screen.turn_aeon():
                battle.main.attack("none")
            elif screen.turn_tidus():
                battle.main.attack("none")
            else:
                battle.main.defend()
        elif memory.main.diag_skip_possible():
            boss_log.debug("Skipping dialog maybe?")
            xbox.tap_b()
    boss_log.debug("Should be done now.")
    memory.main.click_to_control()


def bfa():
    if memory.main.get_gil_value() < 150000:
        swagMode = True
    else:
        swagMode = game_vars.yu_yevon_swag()
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()

    xbox.click_to_battle()
    battle.main.buddy_swap_rikku()
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
    battle.main.buddy_swap_yuna()
    battle.main.aeon_summon(4)

    # Bahamut finishes the battle.
    while memory.main.battle_active():
        xbox.tap_b()

    # Skip the cutscene
    boss_log.info("BFA down. Ready for Aeons")

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_scene()

    while memory.main.get_story_progress() < 3380:
        if memory.main.turn_ready():
            encounterID = memory.main.get_encounter_id()
            boss_log.info(f"Battle engaged. Battle number: {encounterID}")
            if screen.turn_yuna():
                if memory.main.battle_menu_cursor() != 20:
                    while memory.main.battle_menu_cursor() != 20:
                        if memory.main.battle_menu_cursor() in [22, 1]:
                            xbox.tap_up()
                        else:
                            xbox.tap_down()
                while memory.main.main_battle_menu():
                    xbox.tap_b()
                while memory.main.other_battle_menu():
                    xbox.tap_b()
                boss_log.log(f"Enemy max hp: {memory.main.get_enemy_max_hp()}")
                aeon_hp = memory.main.get_enemy_max_hp()[0]
                if swagMode or aeon_hp % 1000 == 0:
                    useGil = aeon_hp * 10
                else:
                    useGil = (int(aeon_hp / 1000) + 1) * 10000
                boss_log.info(f"#### USING GIL #### {useGil}")
                battle.main.calculate_spare_change_movement(useGil)
                while memory.main.spare_change_open():
                    xbox.tap_b()
                while not memory.main.main_battle_menu():
                    xbox.tap_b()
            else:
                battle.main.defend()
        elif not memory.main.battle_active():
            xbox.tap_b()


def yu_yevon():
    boss_log.info("Ready for Yu Yevon.")
    screen.await_turn()  # No need for skipping dialog
    boss_log.info("Awww such a sad final boss!")
    zombieAttack = False
    zaChar = game_vars.zombie_weapon()
    weapSwap = False
    while memory.main.get_story_progress() < 3400:
        if memory.main.turn_ready():
            boss_log.debug("-----------------------")
            boss_log.debug("-----------------------")
            boss_log.debug(f"zaChar: {zaChar}")
            boss_log.debug(f"zombieAttack: {zombieAttack}")
            boss_log.debug(f"weapSwap: {weapSwap}")
            boss_log.debug("-----------------------")
            boss_log.debug("-----------------------")
            if zaChar == 1 and not zombieAttack:  # Yuna logic
                if not weapSwap and screen.turn_yuna():
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=1
                    )
                    weapSwap = True
                elif screen.turn_yuna():
                    battle.main.attack("none")
                    zombieAttack = True
                elif weapSwap and not zombieAttack and screen.turn_tidus():
                    xbox.weap_swap(0)
                else:
                    battle.main.defend()
            elif zaChar == 0 and not zombieAttack:  # Tidus logic:
                if screen.turn_yuna():
                    battle.main.defend()
                elif screen.turn_tidus() and not weapSwap:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=0
                    )
                    weapSwap = True
                elif screen.turn_tidus():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zaChar == 2 and not zombieAttack:  # Auron logic:
                if screen.turn_yuna():
                    battle.main.buddy_swap_auron()
                elif screen.turn_auron() and not weapSwap:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=2
                    )
                    weapSwap = True
                elif screen.turn_auron():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zaChar == 6 and not zombieAttack:  # Rikku logic:
                if screen.turn_yuna() and not weapSwap:
                    # Piggy back off the weapSwap function
                    battle.main.defend()
                    weapSwap = True
                elif screen.turn_yuna():
                    xbox.weap_swap(0)
                elif screen.turn_tidus():
                    battle.main.tidus_haste("r", character=6)
                elif screen.turn_rikku():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zombieAttack:  # Throw P.down to end game
                itemNum = battle.main.yu_yevon_item()
                if itemNum == 99:
                    battle.main.attack("none")
                else:
                    while memory.main.battle_menu_cursor() != 1:
                        xbox.tap_down()
                    while memory.main.main_battle_menu():
                        xbox.tap_b()
                    itemPos = memory.main.get_throw_items_slot(itemNum)
                    battle.main._navigate_to_position(itemPos)
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    while not memory.main.enemy_targetted():
                        xbox.tap_up()
                    battle.main.tap_targeting()
                boss_log.info("Phoenix Down on Yu Yevon. Good game.")
            elif screen.turn_tidus() and zaChar == 255:
                # Tidus to use Zombie Strike ability
                battle.main.use_skill(0)
                zombieAttack = True
            elif zaChar == 255 and not screen.turn_tidus():
                # Non-Tidus char to defend so Tidus can use Zombie Strike ability
                battle.main.defend()
            else:
                if memory.main.get_battle_char_turn() == zaChar:
                    battle.main.attack("none")
                    zombieAttack = True
                elif memory.main.get_battle_char_slot(zaChar) >= 3:
                    battle.main.buddy_swap_char(zaChar)
                elif screen.turn_tidus():
                    battle.main.tidus_haste("l", character=zaChar)
                else:
                    battle.main.defend()
        elif not memory.main.battle_active():
            xbox.tap_b()
