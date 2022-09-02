import FFX_memory
FFX_memory.start()

counter = 0
print("-----------")
print("-----------")
powerArray = FFX_memory.rng02Array()
for i in range(20):
    print(hex(powerArray[i] & 0x7fffffff))
print("-----------")
for j in range(200000):
    if powerArray[j] == 0x85498AC8:
        print("Value found at position:", j)
print("-----------")
print("-----------")
