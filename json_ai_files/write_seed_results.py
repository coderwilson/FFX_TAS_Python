import json
from jsonmerge import merge
import os
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


filepath = os.path.join("json_ai_files", "seed_results.json")

def add_to_seed_results(seed, modifier, avina_heals:str, raw:str, blitz:str, adjusted:str, bcount:str):
    #if seed == 256:
    #    return
    adjusted = adjusted.split(".")[0]
    with open(filepath, "r") as fp:
        results = json.load(fp)

    t = datetime.strptime(adjusted,"%H:%M:%S")
    new_best = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    new_current = adjusted
    try:
        if str(seed) in results.keys():
            t = datetime.strptime(results[str(seed)]["best_adj"],"%H:%M:%S")
            old_best = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            if old_best < new_best:
                new_best = old_best
    except:
        pass
    
    old_current = new_current
    try:
        old_current = results[str(seed)][str(modifier)][str(avina_heals)]["adjusted_time"]
        logger.debug("Previous result identified.")
        if old_current < new_current:
            logger.debug("New time is not better. Ending.")
            return
        logger.debug("New time is better.")
    except:
        logger.debug("No previous results.")

    new_val = {
        str(seed): {
            "best_adj": str(new_best),
            str(modifier): {
                str(avina_heals): {
                    "raw_time": raw,
                    "blitz_time": blitz,
                    "adjusted_time": adjusted,
                    "nea_manip_battle_count": bcount,
                }
            }
        }
    }
    results = merge(results, new_val)
    with open(filepath, "w") as fp:
        json.dump(results, fp, indent=4)

def check_ml_heals(seed_num):
    seed_num = str(seed_num)
    modifier = "standard"
    avina_heals = False

    with open(filepath, "r") as fp:
        results = json.load(fp)
    logger.debug("File opened")
    if str(seed_num) in results.keys():
        logger.debug(f"Seed in file.")
        if not "standard" in results[seed_num].keys():
            logger.debug("No standard runs completed.")
            modifier = "standard"
            avina_heals = False
        
        #  Add other cases before catchall Else statement here, as we add them to the program.
        elif not "flip_lowroad" in results[seed_num].keys():
            logger.debug("First attempt, flipping at Lowroad")
            modifier = "flip_lowroad"
            avina_heals = False

        elif not "flip_bikanel" in results[seed_num].keys():
            logger.debug("Second attempt, flipping in Bikanel.")
            modifier = "flip_bikanel"
            avina_heals = False

        elif not "flip_highroad" in results[seed_num].keys():
            logger.debug("Third attempt, flipping in Highroad.")
            modifier = "flip_highroad"
            avina_heals = False

        elif not "flip_lowroad:flip_bikanel" in results[seed_num].keys():
            logger.debug("Fourth attempt, double flipp (Lowroad & Bikanel).")
            modifier = "flip_lowroad:flip_bikanel"
            avina_heals = False

        elif not "flip_highroad:flip_bikanel" in results[seed_num].keys():
            logger.debug("fifth attempt, double flipp (Highroad & Bikanel).")
            modifier = "flip_highroad:flip_bikanel"
            avina_heals = False

        elif not "flip_lowroad:flip_highroad" in results[seed_num].keys():
            logger.debug("Sixth attempt, double flipp (Highroad & Lowroad).")
            modifier = "flip_lowroad:flip_highroad"
            avina_heals = False

        elif not "flip_lowroad:flip_highroad:flip_bikanel" in results[seed_num].keys():
            logger.debug("Seventh attempt, TRIPLE flip!!!")
            modifier = "flip_lowroad:flip_highroad:flip_bikanel"
            avina_heals = False

        else:
            logger.debug("Catchall settings - determining lowest run time modifier")
            lowest_time = results[seed_num]['best_adj']
            for mod in results[seed_num].keys():
                if mod == "best_adj":
                    continue
                for heal_method in results[seed_num][mod].keys():
                    logger.debug(f"A: {lowest_time}")
                    logger.debug(f"B: {results[seed_num][mod][heal_method]['adjusted_time']}")
                    if lowest_time == results[seed_num][mod][heal_method]['adjusted_time']:
                        logger.debug("test4")
                        modifier=mod
                        #avina_heals = True
        

        '''
        logger.debug("Catchall settings - determining lowest nea_manip_battle_count")
        lowest_modifier = None
        lowest_count = float('inf')
        avina_heals = True  # Default if no valid value found

        for mod in results[seed_num].keys():
            if mod == "best_adj":
                continue
            for heal_method in results[seed_num][mod].keys():
                if "nea_manip_battle_count" in results[seed_num][mod][heal_method]:
                    try:
                        count = int(results[seed_num][mod][heal_method]["nea_manip_battle_count"])
                    except:
                        count = 0
                    if count < lowest_count:
                        lowest_count = count
                        lowest_modifier = mod

        if lowest_modifier:
            modifier = lowest_modifier
        else:
            modifier = "standard"
        '''
    
    return [modifier, avina_heals]
