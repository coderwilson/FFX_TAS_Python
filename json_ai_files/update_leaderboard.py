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
        if self.count == 0:
            self.build_results()
        # Check for missing seeds in the range of 0-255
        present_seeds = {tracker.seed_num for tracker in self.trackers}
        missing_seeds = [seed for seed in range(256) if seed not in present_seeds]
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
        self.order_by_timedelta()



resultpath = os.path.join("json_ai_files", "seed_results.json")
seed_results = TrackerManager()

def print_best():
    best_runs = seed_results.get_top_runs()
    for result in best_runs:
        print(result)

def print_missing():
    print(seed_results.find_missing_seeds())

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
    for result in top_runs:
        file_str += f"{i:>4}: {result.seed_num:>3}, {result.delta}\n"
        i += 1
    file_str += f"Seeds completed: {seed_results.get_seed_count()}\n"
    file_str += f"Suggested seeds: {pick_missing_five()}\n"
    return file_str

def new_leaderboard():
    f = open("json_ai_files\leaderboard.txt", "w")
    f.write(build_file_str())
    f.close()