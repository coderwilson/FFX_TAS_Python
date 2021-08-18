# FFX_TAS_Python

Please find more detailed notes here: https://docs.google.com/presentation/d/14NzxMQo_wRyvMf88i0pJpWNiEynn0LAjW3SAcitERuA/edit?usp=sharing

Hello and greetings! I am coderwilson and I wrote the code for this FFX TAS from the ground up. This repository is a large sample of that code that is intended to demonstrate my skills as a programmer and also provide a jumping-off-point if anyone wanted to try to compete with me in programming a TAS for this game (see speed running community for TAS definition. Here are some of the notes pertinent to this sample of code - this will serve as an FAQ

1. Is this code complete? - No! I am intentionally omitting a major part of the code. I feel the best way to retain ownership of the code is to only give out part of it, and keep a large part of it for myself so that I can continue to shoot for the best time possible with my own code. The project as a whole has been going on for two years, so I feel like it would be a slap in the face for someone to pick it up and submit runs as their own work. That being said, if someone wanted to take this sample and build out the rest of it yourself, you are free to do so.
2. So where is the rest of it? - I continue to retain and improve on the entire project outside of Github. Sorry.
3. Is this code licensed? - Nope. You're free to take this sample and do with it what you will. I ask that you do not sell it in this state, but beyond that it's up to you.
4. So how do I get it to work? - First of all, good luck to you in picking up the project where I have left it here. Second, I expect you to prove your python skills by installing and running all the core files and extended libraries that are referenced within the project. You will want to go through the main file and other core files and remove (preferably via commenting out) the references to files I have not included in the project.
5. Set-up - Once the code is compile-able and doesn't break on run time, download and install the Steam version of Final Fantasy X. I also recommend the 4gb patch referenced on speedrun.com, but it is not ultimately required. Once game is installed, change the settings to run in full screen mode, 1600x900 resolution, and low video quality mode. The current iteration of the project reads pixel colors off of the screen for various reasons, so the screen size and quality are important. (something I'd like to ultimately remove later). After that, you will need to set up a virtual controller, look for ScpVBus online and see if you can get that rolling (it's a bit challenging). FINALLY, in order for memory to work, sometimes we need to pull or push 1 byte or 2 bytes, where the ReadWriteMemory is set to a static 4-byte push or pull. You will need to add a new function called readBytes and one called writeBytes where you have one additional variable for byte size, replacing the static 4-byte size in the original function. It's pretty complicated so GOOD LUCK!!!
6. Can I contact you directly with questions? - Yes, I am active on Discord, username coderwilson. Feel free to message me directly. Or send an email to coderwilson@gmail.com. No solicitations please.

References:
twitch.tv/coderwilson
youtube.com/coderwilson (I don't use this any more, but it has some old stuff that's kinda fun)
coderwilson@gmail.com - no solicitations please.
