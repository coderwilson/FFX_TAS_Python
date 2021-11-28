# FFX_TAS_Python

Please find more detailed notes here: https://docs.google.com/presentation/d/14NzxMQo_wRyvMf88i0pJpWNiEynn0LAjW3SAcitERuA/edit?usp=sharing

Hello and greetings! I am coderwilson and I wrote the code for this FFX TAS from the ground up. This repository is a large sample of that code that is intended to demonstrate my skills as a programmer and also provide a jumping-off-point if anyone wanted to try to compete with me in programming a TAS for this game (see speed running community for TAS definition. Here are some of the notes pertinent to this sample of code - this will serve as an FAQ

1. Is this code complete? - As of Nov 2021, yes this is the complete project without missing files.
2. Is this code licensed? - Nope. You're free to take this sample and do with it what you will. I ask that you do not sell it in this state, but beyond that it's up to you.
3. So how do I get it to work? - First of all, good luck to you in picking up the project where I have left it here. Second, I expect you to prove your python skills by installing and running all the core files and extended libraries that are referenced within the project. You will want to go through the main file and other core files and remove (preferably via commenting out) the references to files I have not included in the project.
4. Set-up - Once the code is compile-able and doesn't break on run time, download and install the Steam version of Final Fantasy X. I also recommend the 4gb patch referenced on speedrun.com, but it is not ultimately required. Once game is installed, change your monitor to 1600x900 resolution and set the game to run in borderless mode (better than fullscreen for controller stability) and low video quality mode. The current iteration of the project reads pixel colors off of the screen for various reasons, so the screen size and quality are important (something I'd like to ultimately remove later). After that, you will need to set up a virtual controller (see the update below). FINALLY, in order for memory to work, sometimes we need to pull or push 1 byte or 2 bytes, where the ReadWriteMemory is set to a static 4-byte push or pull. You will need to add a new function called readBytes and one called writeBytes (copy/paste the read and write functions respectively) where you have one additional variable for byte size, replacing the static 4-byte size in the original function. It's pretty complicated so GOOD LUCK!!!
5. Can I contact you directly with questions? - Yes, I am active on Discord, username coderwilson#3677. Feel free to message me directly. Or send an email to coderwilson@gmail.com. No solicitations please.

Update as of 11/18/2021:
We have changed the controller to use a new gamepad, proven to be more stable than the first one. See these links for more details.
https://github.com/ViGEm/ViGEmBus (installer to set up the virtual port to plug in to)
https://pypi.org/project/vgamepad/ (new virtual game pad to be plugged in)

References:
twitch.tv/coderwilson
youtube.com/coderwilson (I don't use this too much any more, but it has some old stuff that's kinda fun)
coderwilson@gmail.com - no solicitations please.
