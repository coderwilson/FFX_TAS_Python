import logging

import memory.main
import memory.unlocks
import vars
import rng_track
import battle.main
import screen
from players import CurrentPlayer,Bahamut
from typing import Tuple

logger = logging.getLogger(__name__)


game_vars = vars.vars_handle()


def deep_dive_path(
    epaaj_kills,
    turn_order,
    active_party,
    back_line,
    party_escapes,
    past_actions,
    past_chars,
    rng10_advances,
    targetted_chars
) -> Tuple[list, list, int]:
    # Returns actions (array)
    # Returns characters that take actions (array).
    # Returns weight/score, 1 to 300.
    logger.manip(turn_order)

    encounter_id = memory.main.get_encounter_id()
    epaaj_drop_chances = memory.main.next_chance_rng_10_full()
    for i in range(len(epaaj_drop_chances)):
        epaaj_drop_chances[i] = epaaj_drop_chances[i] - rng10_advances
        # Negative values will be ignored in later calcs, so this is fine.
    mech_drop_chances = memory.main.next_chance_rng_10_full(drop_chance_val=12)
    for i in range(len(mech_drop_chances)):
        # Negative values will be ignored in later calcs, so this is fine.
        mech_drop_chances[i] = mech_drop_chances[i] - rng10_advances
    
    
    # This decision tree will capture if we can summon at this point in the actions.
    # This captures if we hit a game-over state (all characters dead)
    if len(active_party) == 0:
        if len(party_escapes) == 0:
            return past_actions,past_chars,-100
        
        # Score will help us determine alignment for an upcoming battle.
        next_encounter = rng_track.singles_battles(area="calm_lands_(gorge)")[0]
        score = 5
        
        # Assume remaining characters will end up defending/fainting
        for i in range(len(epaaj_drop_chances)):
            epaaj_drop_chances[i] = epaaj_drop_chances[i] - (len(past_chars)*3)
        for i in range(len(mech_drop_chances)):
            mech_drop_chances[i] = mech_drop_chances[i] - (len(past_chars)*3)

        if next_encounter[0] == "Epaaj":
            if 0 in epaaj_drop_chances:
                score += 5
            if 3 in epaaj_drop_chances:
                score += 5
        else:
            if 0 in mech_drop_chances:
                score += 5
            if 3 in epaaj_drop_chances:
                score += 5
            if 6 in mech_drop_chances:
                score += 5
        return past_actions,past_chars,score
    

    # This captures if we have no actions left (expected).
    if len(turn_order) == 0:
        if len(party_escapes) == 0:
            # This almost certainly will end in game-over, if it hasn't already.
            return past_actions,past_chars,-50

        # Score will help us determine alignment for an upcoming battle.
        next_encounter = rng_track.singles_battles(area="calm_lands_(gorge)")[0]
        score = 5
        
        # Assume remaining characters will end up defending/fainting
        for i in range(len(epaaj_drop_chances)):
            epaaj_drop_chances[i] = epaaj_drop_chances[i] - (len(past_chars)*3)
        for i in range(len(mech_drop_chances)):
            mech_drop_chances[i] = mech_drop_chances[i] - (len(past_chars)*3)

        if next_encounter[0] == "Epaaj":
            if 0 in epaaj_drop_chances:
                score += 5
            if 3 in epaaj_drop_chances:
                score += 5
        else:
            if 0 in mech_drop_chances:
                score += 5
            if 3 in epaaj_drop_chances:
                score += 5
            if 6 in mech_drop_chances:
                score += 5
        return past_actions,past_chars,score
    
    current_turn = int(turn_order[0])
    future_turns = turn_order[1:]

    # This captures desirable states to summon.
    if current_turn in range(0,8):
        if(encounter_id == 312):
            # Double Epaaj
            epaaj_hit1 = 0 in epaaj_drop_chances
            epaaj_hit2 = 3 in epaaj_drop_chances
            hits_found = [epaaj_hit1, epaaj_hit2].count(True)
            if hits_found >= 1 and hits_found <= epaaj_kills:
                past_actions.append("SUMMON")
                past_chars.append(current_turn)
                logger.info(f"Found path: {past_actions}")
                return past_actions,past_chars,int(100*hits_found)
        else:
            mech1_hit = 0 in mech_drop_chances
            epaaj_hit = 3 in epaaj_drop_chances
            mech2_hit = 6 in mech_drop_chances
            hits_found = [mech1_hit, epaaj_hit, mech2_hit].count(True)
            # Mech / Epaaj / Mech
            if hits_found >= 1 and hits_found <= epaaj_kills:
                past_actions.append("SUMMON")
                past_chars.append(current_turn)
                logger.info(f"Found path: {past_actions}")
                return past_actions,past_chars,int(100*hits_found)
    
    # Monster turns are pretty easy.
    if current_turn >= 20:
        kill_str = ""
        logger.debug(f"Targetted chars check 1: {active_party}")
        active_party.sort()  # Should sort in order from 0 to 7, to align against enemy_targets
        logger.debug(f"Targetted chars check 1: {active_party}")
        enemy_targets = rng_track.enemy_target_predictions(chars=len(active_party))
        e_advances = len(targetted_chars)
        targetted_chars.append(active_party[enemy_targets[e_advances]])
        logger.debug(f"Targetted chars check 3: {targetted_chars}")
        new_party = active_party[:]
        if active_party[enemy_targets[e_advances]] in [2,3]:
            char_num = active_party[enemy_targets[e_advances]]
            if targetted_chars.count(char_num) >= 2:
                # Auron takes two hits to kill
                logger.warning(f"A/K death check: {active_party[enemy_targets[e_advances]]}")
                new_party.remove(active_party[enemy_targets[e_advances]])  # Character assumed dead
                rng10_advances += 3
                kill_str += ">kill"
                while char_num in future_turns:
                    future_turns.remove(char_num)
        elif active_party[enemy_targets[e_advances]] == 0:
            char_num = active_party[enemy_targets[e_advances]]
            if targetted_chars.count(char_num) >= 3:
                # Tidus generally takes three hits to kill
                logger.warning(f"Tidus death check: {active_party[enemy_targets[e_advances]]}")
                new_party.remove(active_party[enemy_targets[e_advances]])  # Character assumed dead
                rng10_advances += 3
                kill_str += ">kill"
                while char_num in future_turns:
                    future_turns.remove(char_num)
        else:  # Anyone else
            char_num = active_party[enemy_targets[e_advances]]
            logger.warning(f"Other death check: {char_num}")
            new_party.remove(char_num)  # Character assumed dead
            rng10_advances += 3
            kill_str += ">kill"
            while char_num in future_turns:
                future_turns.remove(char_num)
        
        
        past_chars.append(current_turn)
        past_actions.append(f"MONSTER>{active_party[enemy_targets[e_advances]]}{kill_str}")
        return deep_dive_path(
            epaaj_kills=epaaj_kills,
            turn_order=future_turns,
            active_party=new_party,
            back_line=back_line[:],
            party_escapes=party_escapes[:],
            past_actions=past_actions[:],
            past_chars=past_chars[:],
            rng10_advances=rng10_advances,
            targetted_chars=targetted_chars[:]
        )
    # A dead character is also easy.
    elif current_turn not in active_party:
        logger.info(f"Found faint: {past_actions}")
        past_chars.append(current_turn)
        past_actions.append("DEATH_PASS")
        return deep_dive_path(
            epaaj_kills=epaaj_kills,
            turn_order=future_turns,
            active_party=active_party[:],
            back_line=back_line[:],
            party_escapes=party_escapes[:],
            past_actions=past_actions[:],
            past_chars=past_chars[:],
            rng10_advances=rng10_advances,
            targetted_chars=targetted_chars[:]
        )
    
    # Now to continue the search down each tree
    if current_turn in [3,6]:
        actions = ["STEAL","ATTACK","ESCAPE"]
    elif current_turn == 0:
        actions = ["ATTACK","SWAP_3","ESCAPE"]
        if memory.unlocks.has_ability_unlocked(character_index=0,ability_name="Steal"):
            actions = ["STEAL"] + actions
    else:
        actions = ["ATTACK","ESCAPE"]
    
    # We now make a scorecard of the different paths.
    logger.info(f"Building scorecard for {current_turn}")
    scorecard = []
    for action in actions:
        new_chars = past_chars[:]
        new_actions = past_actions[:]
        if action == "ATTACK":
            new_chars.append(current_turn)
            new_actions.append("ATTACK")
            
            scorecard.append(deep_dive_path(
                epaaj_kills=epaaj_kills,
                turn_order=future_turns,
                active_party=active_party[:],
                back_line=back_line[:],
                party_escapes=party_escapes[:],
                past_actions=new_actions[:],
                past_chars=new_chars[:],
                rng10_advances=rng10_advances,
                targetted_chars=targetted_chars[:]
            ))
        elif action == "ESCAPE":
            if rng_track.next_action_escape(character=current_turn):
                new_chars.append(current_turn)
                new_actions.append("ESCAPE")
                new_party = active_party[:]
                new_party.remove(current_turn)
                new_turns = future_turns[:]
                while current_turn in new_turns:
                    new_turns.remove(current_turn)
                new_escapes = party_escapes + [current_turn]
                scorecard.append(deep_dive_path(
                    epaaj_kills=epaaj_kills,
                    turn_order=new_turns,
                    active_party=active_party[:],
                    back_line=back_line[:],
                    party_escapes=new_escapes[:],
                    past_actions=new_actions[:],
                    past_chars=new_chars[:],
                    rng10_advances=rng10_advances,
                    targetted_chars=targetted_chars[:]
                ))
            else:
                found = False
                for i in range(len(back_line)):
                    if back_line[i] != 3:  # Save Kimahri for possible steals.
                        if rng_track.next_action_escape(character=back_line[i]):
                            found = True
                            new_chars.append(current_turn)
                            new_chars.append(back_line[i])
                            new_party = active_party[:]
                            new_party.remove(current_turn)
                            new_party.append(back_line[i])
                            new_back_line = back_line[:]
                            new_back_line.remove(back_line[i])
                            new_back_line.append(current_turn)
                            new_actions.append(f"SWAP_{back_line[i]}")
                            new_actions.append(f"ESCAPE")
                            new_escapes = party_escapes + [current_turn]
                            scorecard.append(deep_dive_path(
                                epaaj_kills=epaaj_kills,
                                turn_order=future_turns,
                                active_party=new_party,
                                back_line=new_back_line,
                                party_escapes=new_escapes[:],
                                past_actions=new_actions[:],
                                past_chars=new_chars[:],
                                rng10_advances=rng10_advances,
                                targetted_chars=targetted_chars[:]
                            ))
                if not found:
                    # Fallback, if we did not find an escape target.
                    new_chars.append(current_turn)
                    new_actions.append("DEFEND")
                    scorecard.append(deep_dive_path(
                        epaaj_kills=epaaj_kills,
                        turn_order=future_turns,
                        active_party=active_party[:],
                        back_line=back_line[:],
                        party_escapes=party_escapes[:],
                        past_actions=new_actions[:],
                        past_chars=new_chars[:],
                        rng10_advances=rng10_advances,
                        targetted_chars=targetted_chars[:]
                    ))
        elif action == "SWAP_3":
            new_chars.append(current_turn)
            new_actions.append("SWAP_3")
            new_party = active_party[:]
            new_party.remove(current_turn)
            new_party.append(3)
            new_back_line = back_line[:]
            new_back_line.remove(3)
            new_back_line.append(current_turn)
            future_turns_2 = [3] + future_turns[:]
            scorecard.append(deep_dive_path(
                epaaj_kills=epaaj_kills,
                turn_order=future_turns_2,
                active_party=new_party,
                back_line=new_back_line,
                party_escapes=party_escapes[:],
                past_actions=new_actions[:],
                past_chars=new_chars[:],
                rng10_advances=rng10_advances,
                targetted_chars=targetted_chars[:]
            ))
        elif action == "STEAL":
            new_chars.append(current_turn)
            new_actions.append("STEAL")
            rng10_advances += 1
            scorecard.append(deep_dive_path(
                epaaj_kills=epaaj_kills,
                turn_order=future_turns,
                active_party=active_party[:],
                back_line=back_line[:],
                party_escapes=party_escapes[:],
                past_actions=new_actions[:],
                past_chars=new_chars[:],
                rng10_advances=rng10_advances,
                targetted_chars=targetted_chars[:]
            ))
        else:
            # We should never reach this, but just in case, default action.
            
            if rng_track.next_action_escape(character=current_turn):
                new_chars.append(current_turn)
                new_actions.append("ESCAPE")
                new_escapes = party_escapes + [current_turn]
                scorecard.append(deep_dive_path(
                    epaaj_kills=epaaj_kills,
                    turn_order=future_turns,
                    active_party=active_party[:],
                    back_line=back_line[:],
                    party_escapes=new_escapes[:],
                    past_actions=new_actions[:],
                    past_chars=new_chars[:],
                    rng10_advances=rng10_advances,
                    targetted_chars=targetted_chars[:]
                ))
            else:
                found = False
                for i in range(len(back_line)):
                    if back_line[i] != 3:  # Save Kimahri for possible steals.
                        if rng_track.next_action_escape(character=back_line[i]):
                            found = True
                            new_chars.append(current_turn)
                            new_chars.append(back_line[i])
                            new_party = active_party[:]
                            new_party.remove(current_turn)
                            new_party.append(back_line[i])
                            new_back_line = back_line[:]
                            new_back_line.remove(back_line[i])
                            new_back_line.append(current_turn)
                            new_actions.append(f"SWAP_{back_line[i]}")
                            new_actions.append(f"ESCAPE")
                            new_escapes = party_escapes[:] + [current_turn]
                            scorecard.append(deep_dive_path(
                                epaaj_kills=epaaj_kills,
                                turn_order=future_turns,
                                active_party=new_party,
                                back_line=new_back_line,
                                party_escapes=new_escapes[:],
                                past_actions=new_actions[:],
                                past_chars=new_chars[:],
                                rng10_advances=rng10_advances,
                                targetted_chars=targetted_chars[:]
                            ))
                if not found:
                    # Fallback, if we did not find an escape target.
                    new_chars.append(current_turn)
                    new_actions.append("ATTACK")
                    scorecard.append(deep_dive_path(
                        epaaj_kills=epaaj_kills,
                        turn_order=future_turns,
                        active_party=active_party[:],
                        back_line=back_line[:],
                        party_escapes=party_escapes[:],
                        past_actions=new_actions[:],
                        past_chars=new_chars[:],
                        rng10_advances=rng10_advances,
                        targetted_chars=targetted_chars[:]
                    ))
    logger.info(f"Eval scorecard for {current_turn}:")
    
    # Now to evaluate paths
    best_actions = []
    best_chars = []
    best_score = -1000
    for scores in scorecard:
        logger.manip(f" - {scores}")
        if scores[2] > best_score:
            best_actions = scores[0]
            best_chars = scores[1]
            best_score = scores[2]
        elif scores[2] == best_score:
            if len(scores[0]) < len(best_actions):
                best_actions = scores[0]
                best_chars = scores[1]
                best_score = scores[2]
    return best_actions,best_chars,best_score


def eval_paths(epaaj_kills) -> Tuple[list,list,int]:
    # Returns the lists of best actions and characters to take those actions.
    if memory.main.get_encounter_id() == 312:
        # Double Epaaj encounter
        eval_length = 5
        battle_characters = [0,2,6,20,21]
    else:
        # Mech / Epaaj / Mech encounter (two possible formations)
        eval_length = 6
        battle_characters = [0,2,6,20,21,22]


    turn_order = []
    ptr = 0
    while len(battle_characters) >= 1:
        next_char = memory.main.get_turn_by_index(turn_index=ptr)
        # logger.warning(f"Turn {ptr}: {next_char}")
        turn_order.append(next_char)
        if next_char in battle_characters:
            battle_characters.remove(next_char)
        ptr += 1
    active_party = memory.main.get_active_battle_formation()
    while 255 in active_party:
        active_party.remove(255)  # This should do nothing, but worth keeping for posterity.
    back_line = memory.main.get_battle_formation()
    for i in range(3):
        back_line.remove(back_line[0])
    while 255 in back_line:
        back_line.remove(255)
    
    logger.info(f"Turn order check: {turn_order}")

    best_actions,best_chars,best_score = deep_dive_path(
        epaaj_kills=epaaj_kills,
        turn_order=turn_order,
        active_party=active_party,
        back_line=back_line,
        party_escapes=[],
        past_actions=[],
        past_chars=[],
        rng10_advances=0,
        targetted_chars=[]
    )
    logger.manip(f"Order Check 1: {turn_order}")
    logger.manip(f"Order Check 2: {best_chars}")
    logger.manip(f"Best Actions path found with score {best_score}: {best_actions}")
    return best_actions, best_chars, best_score


def gorge_manip_engage(epaaj_kills):
    screen.await_turn()
    chosen_path,chars,score = eval_paths(epaaj_kills=epaaj_kills)

    if score <= -1:
        logger.warning(f"Best path is highly undesirable (likely game over). Fleeing.")
        battle.main.flee_all()
        return

    for i in range(len(chosen_path)):
        screen.await_turn()
        if memory.main.game_over():
            return False
        if not memory.main.battle_active():
            battle.main.wrap_up()
            return False
        if chosen_path[i] == "SUMMON":
            backline = memory.main.get_battle_formation()
            for i in range(3):
                backline.remove(backline[i])
            if 1 in backline:
                battle.main.buddy_swap_char(1)
            if memory.main.get_current_turn() == 1:
                battle.main.aeon_summon(4)
                Bahamut.unique()
            else:
                CurrentPlayer().defend()
        elif int(chars[i]) >= 20:
            pass
        elif int(chars[i]) != memory.main.get_current_turn():
            logger.warning(f"WRONG TURN ORDER: {chars[i]} > {memory.main.get_current_turn()}")
            battle.main.escape_one()
        elif chosen_path[i] == "STEAL":
            battle.main.steal_target(21)
        elif chosen_path[i] == "DEFEND":
            CurrentPlayer().defend()
        elif chosen_path[i] == "ATTACK":
            CurrentPlayer().attack(target_id=21)
        elif chosen_path[i] == "ESCAPE":
            battle.main.escape_one()
        elif "SWAP" in chosen_path[i]:
            swap_to = chosen_path[i].split("_")[1]
            battle.main.buddy_swap_char(int(swap_to))
        else:
            # Default, in case something goes wrong
            CurrentPlayer().defend()
    
    logger.info("End of predicted battle. Defend until the battle ends.")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            CurrentPlayer().defend()
    battle.main.wrap_up()