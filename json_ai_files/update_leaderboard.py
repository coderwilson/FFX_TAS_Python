import json
from datetime import timedelta
import os
from random import choice

class TimedeltaTracker:
    def __init__(self, seed_num, delta):
        self.seed_num = seed_num
        self.delta = delta
        self.order = None  # Initially blank

    def __repr__(self):
        return f"(Seed: {self.seed_num}, Delta: {self.delta}, Order: {self.order})"


class TrackerManager:
    def __init__(self):
        self.trackers = []
        self.count = 0
        self.identify_all_variants()

    def add_tracker(self, seed_num, delta):
        tracker = TimedeltaTracker(seed_num, delta)
        self.trackers.append(tracker)
        self.count += 1
    
    def get_seed_count(self):
        return self.count

    def order_by_timedelta(self):
        if self.count == 0:
            self.build_results()
        # Sort by timedelta value and assign the order
        self.trackers.sort(key=lambda x: x.delta)
        for idx, tracker in enumerate(self.trackers):
            tracker.order = idx + 1

    def get_top_runs(self):
        if self.count == 0:
            self.build_results()
        # Make sure it's ordered first
        self.order_by_timedelta()
        # Return the top five
        return self.trackers[:10]

    def find_missing_seeds(self):
        with open(resultpath, "r") as fp:
            results = json.load(fp)
        if self.count == 0:
            self.build_results()
        missing_seeds = []
        # Check for missing seeds in the range of 0-255
        for i in range(256):
            if str(i) not in results.keys():
                missing_seeds.append(str(i))
        return missing_seeds
    
    def build_results(self):
        if self.count != 0:
            return
        with open(resultpath, "r") as fp:
            results = json.load(fp)
        
        for key in results.keys():
            if key in ["seed_num", "256"]:
                pass
            else:
                self.add_tracker(key, results[key]["best_adj"])
        try:
            self.order_by_timedelta()
        except:
            pass

    def get_manip_battle_count(self, seed_key) -> str:
        with open(resultpath, "r") as fp:
            results = json.load(fp)

        if seed_key not in results:
            return "N/A"

        best_adj = results[seed_key].get("best_adj")
        for category in results[seed_key].values():
            if isinstance(category, dict):
                for sub_key, sub_value in category.items():
                    if isinstance(sub_value, dict) and sub_value.get("adjusted_time") == best_adj:
                        return str(sub_value.get("nea_manip_battle_count", 99))
        
        return "N/A"  # Return None if no match is found

    def identify_all_variants(self):
        with open(resultpath, "r") as fp:
            results = json.load(fp)

        all_variants = set()

        for seed_key, value in results.items():
            if seed_key.isdigit():  # Only consider numeric seed keys
                for variant in value.keys():
                    if isinstance(value[variant], dict):  # Ensure it's a variant category
                        all_variants.add(variant)

        self.all_variants = sorted(list(all_variants))  # Store globally and sort for consistency
    
    def get_seed_exploration_percentage(self, seed_key):
        with open(resultpath, "r") as fp:
            results = json.load(fp)
        
        if str(seed_key) not in results.keys():
            return 0  # If the seed does not exist, return 0% explored

        explored_variants = 0
        total_variants = len(self.all_variants) # + 1


        for i in range(len(self.all_variants)):
            if self.all_variants[i] in results[str(seed_key)].keys():
                explored_variants += 1  # Each category (e.g., standard, flip_lowroad) is a variant type
                #if "True" in results[str(seed_key)][self.all_variants[i]].keys():
                #    explored_variants += 1  # At least one "True" was attempted

        return explored_variants,total_variants,int(explored_variants/total_variants*100)
    
    def get_variant_exploration_percentage(self,variant):
        with open(resultpath, "r") as fp:
            results = json.load(fp)
        explored_variants = 0
        total_variants = 256.0
        for i in range(256):
            if str(i) in results.keys():
                if variant in results[str(i)].keys():
                    explored_variants = explored_variants + 1
        val_out = explored_variants / total_variants * 100
        val_out = round(val_out,2)
        return val_out

    def get_total_exploration_percentage(self):
        with open(resultpath, "r") as fp:
            results = json.load(fp)
        per_seed_variants = len(self.all_variants) + 1
        explored_variants = 0
        total_variants = 0
        for i in range(256):
            if str(i) in results.keys():
                single_explored, single_total, _ = self.get_seed_exploration_percentage(i)
                explored_variants += single_explored
                total_variants += single_total
            else:
                total_variants += per_seed_variants

        return round((explored_variants / total_variants * 100), 2)
    
    
    def get_best_variant_for_seed(self, seed_num: str):
        with open(resultpath, "r") as fp:
            results = json.load(fp)

        seed_key = seed_num  # Convert to string to match JSON keys
        if seed_key not in results.keys():
            #print(f"Variant not found: {seed_key}")
            return None  # Return None if the seed is not found

        best_variant = None
        best_time = results[seed_key]["best_adj"]

        for variant, data in results[seed_key].items():
            if variant == "best_adj":
                continue
            
            if isinstance(data, dict):
                for sub_key, sub_value in data.items():
                    if isinstance(sub_value, dict) and "adjusted_time" in sub_value:
                        #print(f"{sub_value['adjusted_time']} | {best_time}")
                        adjusted_time = sub_value["adjusted_time"]
                        if adjusted_time == best_time:
                            best_time = adjusted_time
                            best_variant = variant
        #print(f"Variant found: {best_variant}")
        return best_variant


resultpath = os.path.join("json_ai_files", "seed_results.json")
seed_results = TrackerManager()

def print_best():
    best_runs = seed_results.get_top_runs()
    for result in best_runs:
        print(result)

def print_missing():
    print("===================")
    #print(seed_results.find_missing_seeds())
    #print("===================")

def pick_missing_five():
    results = seed_results.find_missing_seeds()
    if len(results) <= 5:
        return results
    ret_array = []
    while len(ret_array) < 5:
        seed = choice(results)
        if not seed in ret_array:
            ret_array.append(seed)
    return ret_array

def build_file_str():
    # seed_results.build_results()

    file_str = "RNG Seed Leaderboard, Real-time minus Blitzball\n"
    top_runs = seed_results.get_top_runs()
    i = 1
    try:
        for result in top_runs:
            file_str += f"{i:>4}: {result.seed_num:>3},  {result.delta} "

            variant = seed_results.get_best_variant_for_seed(str(result.seed_num))
            file_str += f"({variant}) "

            battle_count = seed_results.get_manip_battle_count(str(result.seed_num))
            if battle_count == '0':
                battle_count = "skip"

            _, _, seed_percent = seed_results.get_seed_exploration_percentage(result.seed_num)
            file_str += f"({seed_percent}%)\n"
            
            i += 1
    except:
        pass
    
    try:
        # If you want all exploration, go with this:
        # total_seed_percent = seed_results.get_total_exploration_percentage()
        # file_str += f"Seed completion progress: {total_seed_percent}%\n"

        # If instead you want a specific variant, go with this:
        variant = "standard"
        total_seed_percent = seed_results.get_variant_exploration_percentage(variant)
        file_str += f"{variant} variant completion progress: {total_seed_percent}%\n"
    except:
        pass

    # Continue building the file.
    file_str += f"Suggested seeds: {pick_missing_five()}\n"
    return file_str

def new_leaderboard():
    f = open("json_ai_files\leaderboard.txt", "w")
    f.write(build_file_str())
    f.close()