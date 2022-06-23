# FFX_TAS_Python

Please find more detailed notes here: https://docs.google.com/presentation/d/14NzxMQo_wRyvMf88i0pJpWNiEynn0LAjW3SAcitERuA/edit?usp=sharing

Hello and greetings! I am coderwilson and I wrote the code for this FFX TAS from the ground up. This repository is a large sample of that code that is intended to demonstrate my skills as a programmer and also provide a jumping-off-point if anyone wanted to try to compete with me in programming a TAS for this game (see speed running community for TAS definition. Here are some of the notes pertinent to this sample of code - this will serve as an FAQ

1. Is this code complete? - As of Nov 2021, yes this is the complete project without missing files.
2. Is this code licensed? - Nope. You're free to take this sample and do with it what you will. I ask that you do not sell it in this state, but beyond that it's up to you. - update, I added a general use license to it so it does not overlap with any professional or for-profit efforts.
3. So how do I get it to work? - First of all, good luck to you in picking up the project where I have left it here. Second, I expect you to prove your python skills by installing and running all the core files and extended libraries that are referenced within the project. You will want to go through the main file and other core files and remove (preferably via commenting out) the references to files I have not included in the project.
4. Set-up - Once the code is compile-able and doesn't break on run time, download and install the Steam version of Final Fantasy X. I also recommend the 4gb patch referenced on speedrun.com, but it is not ultimately required. After that, you will need to set up a virtual controller (see the update below). FINALLY, in order for memory to work, sometimes we need to pull or push 1 byte or 2 bytes, where the ReadWriteMemory is set to a static 4-byte push or pull. You will need to add a new function called readBytes and one called writeBytes - see below for specific instructions on this.
5. Can I contact you directly with questions? - Yes, I am active on Discord, username coderwilson#3677. Feel free to message me directly. Or send an email to coderwilson@gmail.com. No solicitations please.


Step 1, get Python installed and set the environment path variables. Once you've done that, run the following commands:
pip install vgamepad
pip install ReadWriteMemory
pip install pyautogui
pip install pyxinput

Step 1.1, install the 4gb patch on speedruncom:
https://www.speedrun.com/ffx/guide/oyi9n

-------------------------------------------------------------------
Virtual Gamepad stuff:
Premise: vgamepad installed from previous steps
We have changed the controller to use a new gamepad, proven to be more stable than the first one. Follow the instructions in this link:
https://github.com/shauleiz/ScpVBus/releases/tag/v1.7.1.2

Other links, don't use these, they are just staying here for legacy reasons.
https://github.com/ViGEm/ViGEmBus (installer to set up the virtual port to plug in to)
https://pypi.org/project/vgamepad/ (new virtual game pad to be plugged in)

-------------------------------------------------------------------
Notes concerning readBytes and writeBytes
Premise: ReadWriteMemory installed from previous steps
The file to fix is located in the python base folder, in this location.
C:\Users\yourUserNameHere\AppData\Local\Programs\Python\Python39\Lib\site-packages\ReadWriteMemory
file name: __init__.py

Copy/paste a duplicate of each of the functions "read" and "write", so that you have two copies of each, then add Bytes to the function name, so "readBytes" and "writeBytes"
Then add a variable for size, so it looks like this:
def readBytes(self, lp_base_address: int, size) -> Any:

Then find the line with ReadProcessMemory and add the size variable where the static 4 is located, so it looks like this:
ReadProcessMemory(self.handle, lp_base_address, lp_buffer,
                                                     size, lp_number_of_bytes_read)
Do this for both readBytes and writeBytes. Save and you're good with this function.

-------------------------------------------------------------------
Now to set up the VI to your computer. Download the repository from Github (here), and unzip.
Open the file FFX_Auto_Main.py in notepad++. Find the line that starts with "FFX_memory.setRngSeed" and add a hashtag at the start of this line.
In addition, make sure the lines for Gamestate = "none" and StepCounter = 1 are not commented (no hashtag).
Save this file, then you can close it if you like.

Similarly, open the FFX_vars.py file. In here, set the following values without changing the whitespace:
self.artificialPauses = True
self.nemesisValue = False
self.savePath = (wherever FFX stores save files on your PC)
Save and close.

-------------------------------------------------------------------
Last set-up step, go into the FFX game and set the controller values:
Confirm button needs to be B
Walk button needs to be A
You may need to plug in a physical controller and then change these settings. If so, restart your computer after.

When you launch the Python program, make sure the game is already running. It needs to connect to the game's memory after launch.
To launch the program, navigate to the folder for the unzipped repository (where you made changes previously), and then enter the command
"py FFX_Auto_Main.py" (no quotes). If everything is set up correctly, it should start running the game for you.
From new game, the VI will automatically detect if you are running a cutscene remover. It is set up for CSR version 1.2.0.

-------------------------------------------------------------------
References:
twitch.tv/coderwilson
youtube.com/coderwilson (now more based on World of Warcraft)
coderwilson@gmail.com - no solicitations please.
