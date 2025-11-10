from gamestate import game

def write_seed_num(seed: int=999, variant:str=""):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Seed num: {seed} | {variant}\nReturn spheres: none\nBlitz Win: TBD")
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
    f.write(f"TrueRNG run active!\nReturn spheres: none\nBlitz Win: TBD")
    f.close()


def write_state_step(state: str, step: str):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"Mid-run test started\n{state} {step}")
    f.close()


def update_state_step(state: str, step: str):
    f = open("json_ai_files\current_seed.txt")
    new_str = f.read()
    f.close()
    split_str = new_str.split("\n")
    split_str[0] = f"TAS Stage {game.state}, Step {game.step}\n"
    final_str = ""
    for i in range(len(split_str)):
        final_str += split_str[i]

    f = open("json_ai_files\current_seed.txt", "w")
    f.write(final_str)
    f.close()


def write_new_game(seed: int):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(f"New Run! GL\nSeed num: {seed}\nReturn spheres: none\nBlitz Win: TBD")
    f.close()

def write_custom_message(msg:str):
    f = open("json_ai_files\current_seed.txt", "w")
    f.write(msg)
    f.close()


def current_big_text() -> str:
    with open("json_ai_files\\big_text.txt", "r") as f:
        return f.read()


def write_big_text(msg:str):
    f = open("json_ai_files\\big_text.txt", "w")
    f.write(msg)
    f.close()