print("Trying thing")
# try:
from ffx_rng_tracker.data.monsters import MONSTERS

# print(MONSTERS)

dingoTest = MONSTERS["dingo"].equipment["ability_arrays"]["Tidus"]["Armor"][2]

print(dingoTest)
print("=================")
print("=================")
print("=================")

equip_type = 0
enemy = "chocobo_eater"
if equip_type == 0:
    array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Weapon"]
else:
    array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Armor"]
ret_val = []
print(array)
print("=================")
print("=================")
print("=================")
for i in range(len(array)):
    try:
        auto = array[i]
        print(auto)
        print(auto.tas_id)
        ret_val.append(array[i].tas_id)
    except:
        ret_val.append(255)

print("=================")
print("=================")
print("=================")
print(ret_val)

# except Exception as e:
#    print("Failure:",e)
print("Success")
