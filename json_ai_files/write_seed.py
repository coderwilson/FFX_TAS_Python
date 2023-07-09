

def write_seed_num(seed:int):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Seed num: {seed}")


def write_state_step(state:str, step:str):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Test: {state}={step}")

def write_new_game():
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"New Run! GL")