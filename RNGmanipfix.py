import sys
import shutil

test = input("Drag and drop your FFX.exe file into this window: ").strip(
    '\"').strip('&').strip(' ').strip("\'")
copiedfile = test[:-4] + "RNGMOD.exe"
shutil.copyfile(test, copiedfile)

seed = int(
    input("FFXRNGMOD.exe created. Which seed would you like to use? 0-255: "))

seed = seed.to_bytes(1, byteorder="big")

with open(copiedfile, "r+b") as f:
    byts = f.read()
    print("Writing chosen seed value")
    f.seek(0x397CA4)
    f.write(b"\xb8")
    f.seek(0x397CA5)
    f.write(seed)
    print("Disabling the splash screen pop-up after closing FFX")
    f.seek(0x22585f)
    f.write(b"\x90\x90\x90\x90\x90\x90")
