import memory.main

memory.main.start()

print("-----------")
print(memory.main.rng_23())
print(memory.main.next_crit(character=3, char_luck=18, enemy_luck=15))
print("-----------")
while memory.main.next_crit(character=3, char_luck=18, enemy_luck=15) > 12:
    memory.main.advance_rng_23()
    print(memory.main.rng_23())
    print(memory.main.next_crit(character=3, char_luck=18, enemy_luck=15))
    print("-----------")
