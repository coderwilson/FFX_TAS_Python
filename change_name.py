import json

def update_name(index:str, new_name:str):
    f = open("json_ai_files/battle_id_to_formation.json")
    all_names = json.load(f)
    f.close()
    if not index in all_names.keys():
        return False

    all_names[index] = new_name
    writing = dict(all_names)
    filepath = "character_names.json"
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)

# Test mode
#update_name("Anima","Johnny")