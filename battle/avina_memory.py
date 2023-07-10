import json
import os
import logging
logger = logging.getLogger(__name__)

def retrieve_memory():
    logger.debug("Retrieving aVIna memory")
    filepath = os.path.join("json_ai_files", "aVIna_memory.json")
    with open(filepath, "r") as fp:
        rng_values = json.load(fp)
    return rng_values


def save_memory(to_write):
    writing = dict(to_write)
    filepath = os.path.join("json_ai_files", "aVIna_memory.json")
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)


def add_to_memory(seed:int, key:str = "kimahri_force_heal", value:str = "True"):
    filepath = os.path.join("json_ai_files", "aVIna_memory.json")
    records = retrieve_memory()
    new_val = {
        str(seed): {
            key: value
        }
    }
    logger.info("Adding to aVIna memory:")
    logger.info(new_val)
    if str(seed) in records.keys():
        if key in records[str(seed)].keys():
            if records[str(seed)][key] != value:
                records[str(seed)][key] = value
        else:
            records[str(seed)].update(new_val[str(seed)])
    else:
        records.update(new_val)

    save_memory(to_write=records)

def add_battle_to_memory(seed:int, area:str = "mrr_heals", battle_num:int = 0, value:str = "True"):
    filepath = os.path.join("json_ai_files", "aVIna_memory.json")
    records = retrieve_memory()
    new_val = {
        str(seed): {
            area: {
                battle_num: value
            }
        }
    }
    logger.info("Adding to aVIna memory:")
    logger.info(new_val)
    results = merge(records, new_val)
    '''
    if str(seed) in records.keys():
        if area in records[str(seed)].keys():
            if key in records[str(seed)][area].keys():
                if records[str(seed)][area][key] != value:
                    records[str(seed)][area][key] = value
                else:
                    records[str(seed)][area][key].update(new_val[str(seed)])
            else:
                records[str(seed)][area]
    else:
        records.update(new_val)
    '''

    save_memory(to_write=results)

