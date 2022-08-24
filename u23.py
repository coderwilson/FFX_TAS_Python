import FFX_memory
FFX_memory.start()

print("-----------")
print(FFX_memory.rng23())
print(FFX_memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
print("-----------")
while FFX_memory.nextCrit(character=3, charLuck=18, enemyLuck=15) > 12:
    FFX_memory.advanceRNG23()
    print(FFX_memory.rng23())
    print(FFX_memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
    print("-----------")
