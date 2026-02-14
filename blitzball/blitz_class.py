from typing import List
import memory.main
from memory.main import BlitzActor
import vars
import logging
from math import sqrt
logger = logging.getLogger(__name__)
from json_ai_files.write_seed import write_big_text

class BlitzGameState:
    IDLE                = "IDLE"
    TIDUS_XP            = "TIDUS_NEEDS_XP"
    JASSU_TRAIN         = "JASSU_TRAIN"
    DEFENSIVE_HOLD      = "DEFENSIVE_HOLD"
    JASSU_STAGING       = "JASSU_STAGING"
    BAITING_DEFENDER    = "BAITING_DEFENDER"
    PASSING_TO_TIDUS    = "PASSING_TO_TIDUS"
    RUSH_GOAL           = "RUSH_GOAL"
    SHOOTING_FOR_GOAL   = "SHOOTING_FOR_GOAL"
    DEFEND_HOLD_LEAD    = "DEFEND_HOLD_LEAD"

    def __init__(self):
        self.vars = vars.vars_handle()
        self.player_array: List[BlitzActor] = [BlitzActor(player_num=i) for i in range(12)]
        
        # Snapshot Data
        self.story_progress = 0
        self.game_clock = 0
        self.controlling_player_index = 1
        self.current_stage = self.IDLE
        self.last_stage = 0
        
        # UI/Score Snapshot
        self.menu_num = 0
        self.own_score = 0
        self.opp_score = 0
        self.tidus_xp_gained = False
        self.last_menu = 0
        self.last_dialog = 0
        self.overtime = False

        # Debug mode - none, stage, flags
        self.debug_mode = "flags"

    def update(self, timed:bool=False):
        """The 'Pulse' of the AI. Run this once at the start of every loop."""
        self._refresh_memory_values()
        self.current_stage = self._calculate_current_stage(timed=timed)
        self._calculate_tactical_status()
        self._refresh_player_data()
        if self.last_stage != self.current_stage:
            logger.debug(f"Stage change: {self.current_stage} | {memory.main.get_story_progress()}")
            self.last_stage = self.current_stage
            if self.debug_mode == "stage":
                write_big_text(f"Stage: {self.current_stage}")
        
    def _refresh_player_data(self):
        """Syncs all actors with game memory."""
        self.story_progress = memory.main.get_story_progress()
        self.game_clock = memory.main.blitz_clock()
        
        for player in self.player_array:
            player.update_coords()
            player.update_stats()
    
    def _calculate_tactical_status(self):
        """Logic-heavy pass to determine which players are guarded."""
        for i in range(12):
            actor = self.player_array[i]
            
            # 1. Check proximity to Graav (Opponent Index 8)
            is_near_graav = self.get_distance(i, 8) < 360 if i != 8 else False
            
            # 2. Check general defender proximity (Opponents 6, 7, 9, 10)
            defenders = [6, 7, 9, 10]
            close_defender_count = 0
            if i < 5:
                for d_idx in defenders:
                    if i != d_idx and self.get_distance(i, d_idx) < 360:
                        close_defender_count += 1
            
            # 3. Specific Logic for Jassu/Botta (3, 4)
            special_guard = False
            if i in [3, 4]:
                if self.get_distance(i, 9) < 340 or self.get_distance(i, 10) < 340:
                    special_guard = True

            # Assign the final result to the Actor object
            actor.is_guarded = (
                is_near_graav or 
                close_defender_count >= 2 or 
                special_guard
            )

            actor.is_engaged = False
            
            # If this actor is the current ball carrier, check for hostiles in pursuit
            if i == self.controlling_player_index:
                # Check if any Goer (8-10) is currently 'aggro' (excluding forwards)
                for opp_idx in range(8, 11):
                    if self.player_array[opp_idx].is_aggro:
                        actor.is_engaged = True
                        break

    def get_distance(self, p1_idx: int, p2_idx: int) -> float:
        p1 = self.player_array[p1_idx].position
        if p2_idx == 12:
            p2 = [0,575]
        else:
            p2 = self.player_array[p2_idx].position
        return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    def _refresh_memory_values(self):
        """Captures a snapshot of memory so values don't change mid-calculation."""
        self.story_progress = memory.main.get_story_progress()
        self.game_clock = memory.main.blitz_clock()
        self.menu_num = memory.main.blitz_menu_num()
        self.own_score = memory.main.blitz_own_score()
        self.opp_score = memory.main.blitz_opp_score()
        
        raw_val = memory.main.blitz_current_player() - 2
        self.controlling_player_index = raw_val if raw_val < 200 else 1
    
    def check_receiver_open(self, player_num: int) -> bool:
        """
        Internalized legacy player_guarded logic.
        Uses internal indices for Goers/Aurochs (e.g., 8 is Graav).
        """
        # 1. Graav (index 8) proximity check
        if self.get_distance(player_num, 8) < 360:
            return False

        # 2. Multi-defender check (usually for Tidus/Forward at index 0)
        # Checks defenders: 6, 7, 9, 10
        defenders = [6, 7, 9, 10]
        close_defenders = 0
        for def_idx in defenders:
            if self.get_distance(player_num, def_idx) < 360:
                close_defenders += 1
        
        if close_defenders >= 2:
            return False

        # 3. Specific player logic (Jassu/Botta indices 3, 4)
        if player_num in [3, 4]:
            if self.get_distance(player_num, 9) < 340 or self.get_distance(player_num, 10) < 340:
                return False
                
        return True

    def _calculate_current_stage(self,timed:bool=False) -> str:
        """Determines the current game stage based purely on text names."""
        if memory.main.get_story_progress() < 540:
            if not self.tidus_xp_gained:
                return self.TIDUS_XP
            else:
                return self.JASSU_TRAIN
        elif self.overtime:
            timed=False
        elif memory.main.get_story_progress() < 700:
            timed = True
        
        idx = self.controlling_player_index
        
        tidus_behind_def = self.player_array[0].position[1] > self.player_array[10].position[1]
        tidus_buffer = self.get_distance(0, 10)
        pass_ready = tidus_behind_def and tidus_buffer > 370
        graav_distance = self.get_distance(idx, 8)
        goal_distance = self.get_distance(idx, 11)

        if not timed:
            if idx == 3:
                if pass_ready:
                    return self.PASSING_TO_TIDUS
                elif self.get_distance(3,10) < 350:
                    return self.BAITING_DEFENDER
                elif self.get_distance(3,8) < 350:
                    return self.BAITING_DEFENDER
                elif self.player_array[3].position[1] < -150:
                    return self.JASSU_STAGING
                else:
                    return self.BAITING_DEFENDER
            elif idx == 0:
                return self.RUSH_GOAL
            return self.DEFENSIVE_HOLD

        j_time = self._get_jassu_timing()
        t_time = self._get_tidus_timing()
        
        # logger.debug(f"Jassu: {j_time} | Tidus: {t_time}")

        # Timeline-based Stages
        if self.own_score > self.opp_score and self.story_progress < 700:
            return self.DEFEND_HOLD_LEAD
        elif self.own_score <= self.opp_score - 2 and self.story_progress < 700:
            return self.DEFENSIVE_HOLD
        elif idx == 0:  # Tidus
            if self.game_clock > t_time:
                return self.SHOOTING_FOR_GOAL
            elif graav_distance < 280:
                return self.SHOOTING_FOR_GOAL
            elif goal_distance < 40:
                return self.SHOOTING_FOR_GOAL
            else:
                return self.RUSH_GOAL
        elif idx == 3:  # Jassu
            if self.game_clock > j_time:
                return self.PASSING_TO_TIDUS
            # elif self.game_clock > (j_time - 15) and pass_ready:
            #     return self.PASSING_TO_TIDUS
            elif self.game_clock > (j_time - 12):  # Previously 15
                return self.BAITING_DEFENDER
            elif self.game_clock > (j_time - 35):
                return self.JASSU_STAGING
            else:
                self.DEFENSIVE_HOLD
        elif idx < 5:  # Anyone else
            return self.DEFENSIVE_HOLD

        return self.DEFENSIVE_HOLD
    
    def _get_jassu_timing(self) -> int:
        shot_distance = self.get_distance(0, 12)
        shot_mod = (
            int(shot_distance / 100) + 9
        )  # Distance/time plus animation time. Extra distance for swimming to the goal
        pass_distance = self.get_distance(0, 3)
        pass_mod = int(pass_distance / 100) + 9  # Distance/time plus animation time
        if 540 <= memory.main.get_story_progress() < 570:
            base_timing = int(180 - shot_mod - pass_mod)
        else:
            base_timing = int(
                300 - shot_mod - pass_mod
            )  # Wakka shot is a faster animation.
        return base_timing


    def _get_tidus_timing(self) -> int:
        shot_distance = self.get_distance(0, 12)
        shot_mod = int(shot_distance / 100) + 9
        if 540 <= memory.main.get_story_progress() < 570:
            base_timing = int(180 - shot_mod)
        else:
            base_timing = int(300 - shot_mod)  # Wakka shot is a faster animation.

        count = 0
        for x in [6,8,9,10,7]:
            if self.get_distance(0, x) < 160:
                count += 1
                if x == 7 and count == 1:
                    pass
                else:
                    base_timing = int(base_timing - 4)
        return base_timing

    

def blitz_state_handle():
    return blitz_state_value

blitz_state_value = BlitzGameState()
