def write_seed_num(seed: int):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Seed num: {seed}\nBlitz Win: TBD\nReturn spheres: none")
    f.close()


def write_blitz_results(results:str):
    f = open("json_ai_files\current_seed.txt")
    new_str = f.read().replace("TBD", results)
    f.close()
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(new_str)
    f.close()

def write_returns(results:int):
    f = open("json_ai_files\current_seed.txt")
    new_str = f.read().replace("none", str(results))
    f.close()
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(new_str)
    f.close()


def write_seed_err():
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"TrueRNG run active!\nBlitz Win: TBD\nReturn spheres: none")
    f.close()


def write_state_step(state: str, step: str):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Test: {state}={step}")
    f.close()


def write_new_game():
    f = open("json_ai_files\current_seed.txt", "w")
    f.write("New Run! GL\nBlitz Win: TBD")
    f.close()

def write_custom_message(msg:str):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(msg)
    f.close()