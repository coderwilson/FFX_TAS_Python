# FFX_TAS_Python

Please find more detailed notes here: https://docs.google.com/presentation/d/14NzxMQo_wRyvMf88i0pJpWNiEynn0LAjW3SAcitERuA/edit?usp=sharing

Hello and greetings! I am coderwilson and I wrote the code for this FFX VI-TAS from the ground up. This repository makes up the code that is intended to demonstrate my skills as a programmer and also provide a jumping-off-point if anyone wanted to the programming for this project. Here are some of the notes pertinent to this sample of code - this will serve as an FAQ.

1. Is this code complete? - As of Nov 2021, yes this is the complete project without missing files.
2. Is this code licensed? - The code falls under the "GNU General Public License v3.0". It is not intended for commercial use.
3. So how do I get it to work? - The short version is that you will want to get the latest version of Python installed onto your machine, and then use the appropriate Python commands to run the FFX_auto_main.py file. There are other run-able files for various purposes, but the main file is the one you want to go with. As I will note later, you will also need to install the Steam version of FFX, the 4gb patch (available at speedrun.com), and the virtual controller.
4. Set-up - Once the code is compile-able and doesn't break on run time, download and install the Steam version of Final Fantasy X. I also recommend the 4gb patch referenced on speedrun.com, but it is not ultimately required. After that, you will need to set up a virtual controller (see the update below).
5. readBytes and writeBytes - FINALLY, in order for memory to work, sometimes we need to pull or push 1 byte or 2 bytes, where the ReadWriteMemory is set to a static 4-byte push or pull. You will need to add a new function called readBytes and one called writeBytes (copy/paste the read and write functions respectively) where you have one additional variable for byte size, replacing the static 4-byte size in the original function. It's pretty complicated so feel free to touch base with me and ask questions if you're having trouble with this.
6. Can I contact you directly with questions? - Yes, I am active on Discord, username coderwilson#3677. Feel free to message me directly. Or send an email to coderwilson@gmail.com. No solicitations please.

Update as of 11/18/2021:
We have changed the controller to use a new gamepad, proven to be more stable than the first one. See these links for more details.
https://github.com/ViGEm/ViGEmBus (installer to set up the virtual port to plug in to)
https://pypi.org/project/vgamepad/ (new virtual game pad to be plugged in)

References:
twitch.tv/coderwilson
youtube.com/coderwilson (I don't use this too much any more, but it has some old stuff that's kinda fun)
coderwilson@gmail.com - no solicitations please.

-------------------------------------------------------------------
Also, this may be helpful:
https://github.com/shauleiz/ScpVBus/releases/tag/v1.7.1.2

-------------------------------------------------------------------
Notes concerning readBytes and writeBytes
Make sure to instal (via pip) the library ReadWriteMemory.
The file to fix is located in the python base folder, in this location.
C:\Users\yourUserNameHere\AppData\Local\Programs\Python\Python39\Lib\site-packages\ReadWriteMemory
file name: __init__.py

Copy/paste a duplicate of each of the functions "read" and "write", so that you have two copies of each, then add Bytes to the function name, so "readBytes" and "writeBytes"
Then add a variable for size, so it looks like this:
---  def readBytes(self, lp_base_address: int, size) -> Any:

Then find the line with ReadProcessMemory and add the size variable where the static 4 is located, so it looks like this:
---  ReadProcessMemory(self.handle, lp_base_address, lp_buffer,
                                                     size, lp_number_of_bytes_read)
Do this for both readBytes and writeBytes. Save and you're good to go.
