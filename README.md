# FFX TAS Python

This Project aims to speedrun the Steam version of Final Fantasy X using tools such as python, virtual controllers and memory reading.

This is achieved by reading memory values and sending controller inputs that fit the situation.

We strive to only include code that is not seed-specific which causes the codebase to be quite large so we can cover as many edge cases as possible.

## Best Times

- Cutscene Remover Any% in `3:04:14`
  <https://www.youtube.com/watch?v=P0wDLfiLtOs>
- Any% in `8:45:14`
  <https://www.youtube.com/watch?v=xc-ixb5rCFU>
- Nemesis% _-Work in Progress-_

## Showcases

This project has been showcased on:

- Q4G HH2 - Nov 2021
<https://www.twitch.tv/videos/1205160940>

- TASgiving - Nov 2021
<https://www.youtube.com/watch?v=Gvz-XdiNuKI>

- RPG Limit Break 2022 - October 17th 2022
<https://www.youtube.com/watch?v=C598HEcfdgE>

## Setup/Getting started

For troubleshooting please refer to our Discord: <https://discord.gg/2Xh3SFmrVN>

Currently, only the Windows version of the game is supported (due to the Cutscene Remover only being supported on this platform).

## Installation

* Install the Steam version of Final Fantasy X (in other words, the Final Fantasy X/X-2 HD Remaster).
* Install Virtual gamepad port: <https://github.com/ViGEm/ViGEmBus/releases/tag/v1.21.442.0>
* Install Python version 3.10 or later (through Windows store or from <https://www.python.org/downloads/>). Ensure that python is added to the `PATH` variable during installation. If you run into problems on version 3.11 or later, try installing 3.10.
* Download the repository to your computer: <https://github.com/coderwilson/FFX_TAS_Python>
* Install the python requirements using pip (comes with your python installation):
  - Run `CMD` or `PowerShell` as administrator.
  - Navigate to the `FFX_TAS_Python` directory.
  - Run `pip install -r requirements.txt`

## Speedrunner tools to install

* The 4gb memory patch (improves game stability), follow installation instructions here: <https://www.speedrun.com/ffx/guide/oyi9n>
* [Optional] Set up LiveSplit timer:
  - Install LiveSplit: <https://livesplit.org/downloads/>
  - Set up timer/splits for FFX in LiveSplit: <https://www.speedrun.com/ffx/guide/vnxps>
  - There are some autosplits that doesn't work with the Cutscene Remover, and should be disabled: MushroomRockRoad, Seymour, BevelleGuards, SanctuaryKeeper.
* The latest release of the Final Fantasy X Cutscene Remover: <https://github.com/erickt420/FFXCutsceneRemover/releases>

## Before starting a run

* Make sure the correct game settings are used:
  - Open the game launcher and set language, change resolution and set to windowed or borderless mode.
  - Launch the base game (`FFX.exe`). Press `Escape` and go into `System Settings > Key Bindings > Controller` and set the `Talk/Examine/Confirm` option to `A`.
* Make sure that there are no physical XBox/Playstation controllers connected. This is because the virtual gamepad needs to be controller 1 for the TAS to work.
* Make sure the correct settings for the run are set in `vars.py`:
  - Change `self.setSeed = True` to `self.setSeed = False`
* Make sure the correct GameState for your run is set in `main.py`. For a new game, use `GameState = "none"` and `step_counter = 1`. Comment out any other assignment at the top of `main.py`.

In order for other starting GameStates to work, the saves in `TAS Saves` must be installed correctly. Please ask in the Discord how to do this, as it requires a few steps beyond just copying the files.

## Starting a run

* [Optional] Start LiveSplit
* Start the patched `FFX.exe`
* [Optional] Start the Cutscene remover
* In `CMD` or `PowerShell` as administrator, run `py main.py` in the `FFX_TAS_Python` directory.

The TAS should now be running!
