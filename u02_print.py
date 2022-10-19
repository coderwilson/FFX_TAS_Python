import memory.main

memory.main.start()

counter = 0
print("-----------")
print("-----------")
powerArray = memory.main.rng02Array()
for i in range(20):
    print(hex(powerArray[i] & 0x7FFFFFFF))
print("-----------")
for j in range(200000):
    if powerArray[j] == 0x85498AC8:
        print("Value found at position:", j)
print("-----------")
print("-----------")
