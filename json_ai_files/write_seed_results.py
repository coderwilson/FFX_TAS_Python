import json
from jsonmerge import merge
import os
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


filepath = os.path.join("json_ai_files", "seed_results.json")

def add_to_seed_results(seed, modifier, avina_heals:str, raw:str, blitz:str, adjusted:str):
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
        elif not "False" in results[seed_num]["standard"]:  # True/False if using ML heal method.
            logger.debug("No standard runs completed - with all heal method.")
            modifier = "standard"
            avina_heals = False
        elif not "True" in results[seed_num]["standard"]:  # True/False if using ML heal method.
            logger.debug("No standard runs completed - with ML heal method.")
            modifier = "standard"
            avina_heals = True
        
        #  Add other cases before catchall Else statement here, as we add them to the program.
        elif not "flip_lowroad" in results[seed_num].keys():
            logger.debug("First attempt, flipping at Lowroad")
            modifier = "flip_lowroad"
            avina_heals = False
        elif not "True" in results[seed_num]["flip_lowroad"]:
            logger.debug("Flip lowroad and aVIna heals")
            modifier = "flip_lowroad"
            avina_heals = True

        else:
            logger.debug("Catchall settings.")
            modifier = "standard"
            avina_heals = True
    
    return [modifier, avina_heals]
