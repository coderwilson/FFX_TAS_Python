import memory.main
import pathing
import xbox

FFXC = xbox.controller_handle()


def engage():
    checkpoint = 0
    input("Confirm that CSR is running!!!")
    while not memory.main.battle_active():
        if memory.main.user_control():
            pDownSlot = memory.main.get_item_slot(6)
            if memory.main.get_map() == 58:
                memory.main.full_party_format("tidkimwak")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # elif checkpoint == 2 and memory.main.getItemCountSlot(pDownSlot) >= 10:
            #    checkpoint = 4
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint = 4
            elif pathing.set_movement(pathing.miihen_agency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def battle():
    memory.main.wait_frames(10)
    chocoIndex = memory.main.actor_index(actor_num=4200)
    chocoCoords = memory.main.get_actor_coords(actor_number=chocoIndex)
    input("Ready 1")
    memory.main.choco_eater_fun(actor_index=chocoIndex)
    input("Ready 2")
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    exit()
