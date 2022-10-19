import memory.main

memory.main.start()

print("-----------")
print(memory.main.rng23())
print(memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15))
print("-----------")
while memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15) > 12:
    memory.main.advanceRNG23()
    print(memory.main.rng23())
    print(memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15))
    print("-----------")
