import memory
memory.start()

print("-----------")
print(memory.rng23())
print(memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
print("-----------")
while memory.nextCrit(character=3, charLuck=18, enemyLuck=15) > 12:
    memory.advanceRNG23()
    print(memory.rng23())
    print(memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
    print("-----------")
