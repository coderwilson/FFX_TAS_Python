from twitchio.ext import commands
import subprocess
import random
import os
import json
import time

import yaml
import logging
import pyautogui
from timer_saver_logic.timer_reset import clickHeader
from typing import Dict

logger = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Define the path to the Python script to run
SCRIPT_PATH = "main.py"
CHOCO_PATH = "z_choco_races_test.py"
BLITZ_PATH = "x_blitz_only.py"
CSR_PATH = ""
GAME_PATH = ""
CONFIG_FILE_PATH = "bot-config.yaml"
MARBLES_PATH = "C:\\Users\\coder\\Desktop\\Python_projects\\marbles_on_stream"

import psutil

def terminate_marbles_processes():
    """Identify and terminate processes with 'marbles' in their names (case-insensitive)."""
    terminated = []
    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"]
            if "marbles" in process_name.lower():
                process.terminate()  # Request termination
                terminated.append(process.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Process might have ended or can't be accessed
    
    if terminated:
        print(f"Terminated processes: {terminated}")
    else:
        print("No processes with 'marbles' in their names found.")

def oblitz_history():
    filepath = os.path.join("json_ai_files", "oblitz_results.json")
    with open(filepath, "r") as fp:
        rng_values = json.load(fp)
    return rng_values


def update_timer_category(category:str="csr_speedrun"):
    prefix = '   <SplitsFile gameName="Final Fantasy X" categoryName="REPLACE" lastTimingMethod="GameTime" lastHotkeyProfile="Default">'
    base_path = TIMER_PATH
    postfix = '</SplitsFile>\n '

    with open(base_path + 'LiveSplit_1.8.29\\settings.cfg','r') as f:
        contents=f.read()

    opentag='<RecentSplits>\n'
    closetag=' </RecentSplits>'
    oldtext=contents[contents.find(opentag)+16:contents.find(closetag)]

    if category=="nemesis":
        file_name='Final Fantasy X - PC - Nemesis.lss'
        category_name = 'PC Nemesis%'
    elif category=="non_csr_speedrun":
        file_name='Final Fantasy X - PC - Non-CSR.lss'
        category_name = 'PC'
    elif category=="csr_speedrun":
        file_name='Final Fantasy X - PC - CSR.lss'
        category_name = 'Cutscene Remover'
    elif category=="story":
        file_name='Final Fantasy X - PC - Story.lss'
        category_name = 'Story%'
    
    prefix = prefix.replace('REPLACE',category_name)
    cat_str = prefix + base_path + file_name + postfix

    contents=contents.replace(oldtext,cat_str)
    
    with open(base_path + 'LiveSplit_1.8.29\\settings.cfg','w') as f:
        f.write(contents)


class BotConfig:
    def __init__(self, config_path: str):
        self.data = {}
        # Open the config file and parse the yaml contents
        try:
            with open(config_path) as config_file:
                try:
                    self.data = yaml.load(config_file, Loader=Loader)
                except Exception as E:
                    logger.error(f"Error: Failed to parse config file {config_path}")
                    logger.exception(E)
        except Exception:
            logger.info(f"Didn't find config file {config_path}, using default values.")


# Define the bot
class Bot(commands.Bot):
    def __init__(self, config: Dict):
        token: str = config.get("token", "YOUR_TOKEN_HERE")
        channels: str = config.get("channels", ["YOUR_CHANNEL_NAME"])
        # Define the users who are allowed to send commands
        self.allowed_users = config.get("allowed_users", ["YOUR_CHANNEL_NAME"])
        super().__init__(token=token, prefix="!", initial_channels=channels)
        self.process = None
        self.csr = None
        self.game = None
        self.timer = None
        self.marbles = None
    
    def is_valid_user(self, ctx: commands.Context):
        if self.game_ended_check():
            print("Game has ended. Adjusting.")
            self.kill(ctx)
            time.sleep(5)
        if ctx.author.is_mod or ctx.author.name in self.allowed_users:
            print("Identified mod or elevated user. Valid User function returning True.")
            return True
        elif self.process == None and self.marbles == None:
            print("No processes running. Valid User function returning True.")
            return True
        else:
            print("Regular user. Valid User function returning False.")
            ctx.send(
                f"Sorry {ctx.author.name}, you don't have permissions to execute this. Please wait for the run to finish or ask for mod status."
            )
            return False

    async def event_ready(self):
        # Notify when we are logged in and ready to use commands
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")
        print("Ready for commands")
        
    # Timer, cancel last split
    @commands.command(aliases=("undo","timer_undo"))
    async def undo_split(self, ctx: commands.Context):
        if self.is_valid_user(ctx):
            await ctx.send("Undo command on last split.")
            pyautogui.press("num8")
        else:
            await ctx.send("Permissions error - must be a mod.")
            pass

    # Timer, cancel last split
    @commands.command(aliases=("skip","timer_skip"))
    async def skip_split(self, ctx: commands.Context):
        if self.is_valid_user(ctx):
            await ctx.send("Advancing one split with no recorded time.")
            pyautogui.press("num2")
        else:
            await ctx.send("Permissions error - must be a mod.")
            pass

    # Define the start command
    @commands.command(aliases=("begin", "launch"))
    async def start(self, ctx: commands.Context):
        arg_array = []
        print(ctx.message.content)
        args = ctx.message.content.split()
        print(args)
        seed_set = False
        records = oblitz_history()
        seed_num = str(random.choice(range(256)))
        reroll = 0
        print(records.keys())
        while seed_num in records.keys() and reroll < 1000:
            seed_num = str(random.choice(range(256)))
            reroll += 1
        for i in range(len(args)):
            try:
                if args[i].lower() == "seed":
                    arg_array.append("-seed")
                    seed_num = str(args[i + 1])
                    print(f"Specified Seed: {seed_num}")
                    seed_set = True
                    arg_array.append(seed_num)
                if args[i].lower() in ["state","stage"]:
                    arg_array.append("-state")
                    arg_array.append(args[i + 1])
                if args[i].lower() == "step":
                    arg_array.append("-step")
                    arg_array.append(args[i + 1])
                if args[i].lower() == "blitz":
                    arg_array.append("-train_blitz")
                    arg_array.append("True")
                #if args[i].lower() == "godrng":
                #    arg_array.append("-godrng")
                #    arg_array.append("True")
                if "classic" in args:
                    arg_array.append("-classic")
                    arg_array.append("True")
                elif "story" in args:
                    arg_array.append("-story")
                    arg_array.append("True")
                else:
                    arg_array.append("-story")
                    arg_array.append("False")
                if "nem" in args or "nemesis" in args:
                    arg_array.append("-nemesis")
                    arg_array.append("True")
            except Exception:
                await ctx.send(
                    f"There was an error with your command: {ctx.message.content}"
                )

        if not seed_set:
            arg_array.append("-seed")
            arg_array.append(seed_num)

        if self.process is None and self.marbles is None:
            print(["python", SCRIPT_PATH] + arg_array)
            self.process = subprocess.Popen(["python", SCRIPT_PATH] + arg_array)
            #await ctx.send("FFX TAS started.")
            print("aVIna FFX TAS started.")
        else:
            #await ctx.send("FFX TAS is already running.")
            print("aVIna FFX TAS is already running.")
        return self.process

    # Define the start command
    @commands.command()
    async def blitz(self, ctx: commands.Context):
        if self.process is None and self.marbles is None:
            print(["python", BLITZ_PATH])
            self.process = subprocess.Popen(["python", BLITZ_PATH])
            #await ctx.send("FFX TAS started.")
            print("aVIna FFX TAS started.")
        else:
            #await ctx.send("FFX TAS is already running.")
            print("aVIna FFX TAS is already running.")
        return self.process

    # Alternate start command, Chocobo races
    @commands.command(aliases=("choco", "race", "races", "showcase"))
    async def chocobo(self, ctx: commands.Context):
        if self.process is None and self.marbles is None:
            print(["python", CHOCO_PATH])
            await self.start_csr(ctx)
            await self.start_game(ctx)
            time.sleep(3)
            self.process = subprocess.Popen(["python", CHOCO_PATH])
            await ctx.send("FFX Showcase started.")
            print("Showcase started.")
        else:
            #await ctx.send("FFX TAS is already running.")
            print("TAS is already running.")
        return self.process

    # Define the exit command
    @commands.command(aliases=("stop", "quit", "terminate"))
    async def exit(self, ctx: commands.Context):
        #if self.is_valid_user(ctx):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            #await ctx.send("FFX TAS stopped.")
            print("aVIna FFX TAS stopped.")
        else:
            #await ctx.send("FFX TAS is not running.")
            print("aVIna FFX TAS is not running.")

    # Define the start-CSR command
    @commands.command(aliases=("csr_start", "csr_launch"))
    async def start_csr(self, ctx: commands.Context):
        if "story" in ctx.message.content:
            logger.info("CSR undesirable for story mode.")
            return
        if "classic" in ctx.message.content:
            logger.info("CSR undesirable for classic mode.")
            return
        arg_array = []
        #if self.is_valid_user(ctx):
        if self.csr is None and self.marbles is None:
            print(CSR_PATH)
            arg_array.append("--csr=true")
            arg_array.append("--truerng=false")
            self.csr = subprocess.Popen([CSR_PATH] + arg_array)
            #await ctx.send("CSR started.")
            print("CSR started.")
        #else:
        #    await ctx.send("CSR is already running.")
                
    # Define the stop-CSR command
    @commands.command(aliases=("csr_stop", "csr_halt"))
    async def stop_csr(self, ctx: commands.Context):
        #if self.is_valid_user(ctx):
        if self.csr is not None:
            self.csr.terminate()
            self.csr.wait()
            self.csr = None
            #await ctx.send("CSR stopped.")
            print("CSR stopped.")
        #else:
        #    await ctx.send("CSR is not running.")

    # Launch FFX
    @commands.command(aliases=("game_start", "launch_game"))
    async def start_game(self, ctx: commands.Context):
        #if self.is_valid_user(ctx):
        if self.game is None and self.marbles is None:
            cwd = os.getcwd()
            print(cwd)
            os.chdir(GAME_PATH)
            print(os.getcwd())
            launch_path = GAME_PATH + "\FFX.exe"
            print(launch_path)
            self.game = subprocess.Popen([launch_path])
            os.chdir(cwd)
            #await ctx.send("FFX started.")
            print("FFX started.")
        else:
            #await ctx.send("FFX is already running.")
            print("FFX is already running.")

    # Kill FFX
    @commands.command(aliases=("game_stop", "halt_game"))
    async def stop_game(self, ctx: commands.Context):
        #if self.is_valid_user(ctx):
        if self.game is not None:
            self.game.terminate()
            self.game.wait()
            self.game = None
            #await ctx.send("FFX stopped.")
            print("FFX stopped.")
        else:
            #await ctx.send("FFX is not running.")
            print("FFX is not running.")

    # Launch timer
    @commands.command(aliases=("timer_start", "launch_timer"))
    async def start_timer(self, ctx: commands.Context):
        #await ctx.send("Timer is disabled while we rebuild save files.")
        #return
    
        '''
        if "story" in ctx.message.content:
            #await ctx.send("Timer undesirable for story mode.")
            return
        '''
        if "state" in ctx.message.content:
            #await ctx.send("Timer undesirable for starting mid run")
            return
        if "stage" in ctx.message.content:
            #await ctx.send("Timer undesirable for starting mid run")
            return
        print(f"Timer args check: {ctx.message.content}")
        args = ctx.message.content.split()

        if self.csr is None:
            csr_val = False
        else:
            csr_val = True
        #if self.is_valid_user(ctx):
        if self.timer is None and self.marbles is None:
            if "nem" in ctx.message.content.lower():
                cat = "nemesis"
            elif "story" in ctx.message.content.lower():
                cat = "story"
            elif csr_val == False:
                cat = "non_csr_speedrun"
            else:
                cat = "csr_speedrun"
            await ctx.send(f"Initiating timer: {cat}")
            update_timer_category(category=cat)
            # Updated, no longer necessary.
            #if csr_val == "False":
            #    TIMER_PATH = TIMER_PATH_NORM
            #else:
            #    TIMER_PATH = TIMER_PATH_CSR
            cwd = os.getcwd()
            print(cwd)
            os.chdir(TIMER_PATH)  # Confirms path
            print(os.getcwd())
            launch_path = TIMER_PATH + "\LiveSplit_1.8.29\LiveSplit.exe"
            print(launch_path)
            self.timer = subprocess.Popen([launch_path])
            os.chdir(cwd)
            print("Timer started.")
        else:
            #await ctx.send("Timer is already running.")
            print("Timer is already running.")

    # Kill timer
    @commands.command(aliases=("timer_stop", "halt_timer"))
    async def stop_timer(self, ctx: commands.Context):
        '''
        if ctx.author.name not in self.allowed_users:
            await ctx.send(
                f"Sorry {ctx.author.name}, you don't have permissions to execute this."
            )
        '''
        clickHeader()
        print("Save successful.")
        time.sleep(0.5)
        print("Killing process.")

        #if self.is_valid_user(ctx):
        if self.timer is not None:
            self.timer.terminate()
            self.timer.wait()
            self.timer = None
            #await ctx.send("Timer stopped.")
            print("Timer stopped.")
        else:
            #await ctx.send("Timer is not running.")
            print("Timer is not running.")

    # Define the help command
    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(
            "Primary commands: !all, !halt_all, !stuck, !skip_split, !undo_split | "
            + "There are four categories which can be started with the following commands. "
            + "CSR speedrun: '!all', Classic speedrun: '!all classic', "
            + "Story mode: '!all story', Nemesis run: '!all nem'"
        )
    
    # Start All
    @commands.command(aliases=("begin_all", "all"))
    async def start_all(self, ctx: commands.Context):
        await self.marbles_end(ctx)
        #if self.is_valid_user(ctx):
        await ctx.send("Launching all elements!")
        await self.start_game(ctx)
        time.sleep(3)
        await self.start_csr(ctx)
        time.sleep(1)
        if "state" in ctx.message.content.lower():
            #await ctx.send("Timer undesirable when loading a save.")
            pass
        else:
            await self.start_timer(ctx)
        time.sleep(3)
        await self.start(ctx)
    
    # Kill All
    @commands.command(aliases=("kill_all","halt_all","stop_all"))
    async def kill(self, ctx: commands.Context):
        if self.is_valid_user(ctx):
            await self.exit(ctx)
            await self.stop_csr(ctx)
            await self.stop_game(ctx)
            await self.stop_timer(ctx)
            await ctx.send("All processes halted.")
            
    @commands.command(aliases=("NEA", "Nea"))
    async def nea(self, ctx: commands.Context):
        await ctx.send(
            "NEA, or No-Encounters Armor, is one of the most important time-saving "
            + "parts of the Final Fantasy speedrun. By doing a number of steals and/or allowing "
            + "party characters to die, we manipulate randomness in a way that will line up "
            + "a certain drop at a certain time, right at the start of Calm Lands, to result "
            + "in this NEA equipment to drop for us. Overall time saved is around 12 minutes "
            + "even with the cutscenes removed."
        )
    
    @commands.command(aliases=("play_marbles"))
    async def play(self, ctx: commands.Context):
        # This is so we don't have to catch someone joining a game of marbles.
        pass
        

    # End Marbles
    @commands.command(aliases=("marbles_stop"))
    async def marbles_end(self, ctx: commands.Context):
        print("Marbles End command received")
        try:
            if self.marbles is not None: # and self.marbles.poll() != None:
                self.marbles.terminate()
                self.marbles.wait()
                self.marbles = None
                print("Reset handle, python process is no longer running.")
                terminate_marbles_processes()
                #self.game.terminate()
                #self.game.wait()
                #self.game = None
                print("Reset handle, marbles executable is no longer running.")
            else:
                print("Marbles was not launched or has completed.")
        except:
            print("Process was never launched, this is normal.")
        print (f"Reset logic complete - {self.marbles}")
    
    # Launch Marbles
    @commands.command(aliases=("marbles_start"))
    async def marbles(self, ctx: commands.Context):
        #await ctx.send("Sorry, Marbles is currently broken.")
        
        await self.marbles_end(ctx)
        if self.marbles is None and self.game is None:
            '''
            # First need to launch the game.
            cwd = os.getcwd()
            print(cwd)
            os.chdir(GAME_PATH)
            print(os.getcwd())
            launch_path = MARBLES_EXE + "\Marbles on Stream"
            print(launch_path)
            self.game = subprocess.Popen([launch_path])
            os.chdir(cwd)
            await ctx.send("FFX started.")
            print("FFX started.")
            time.sleep(10)
            print("Sleep check")
            '''

            # Now for the python code
            print("Attempting process start.")
            await ctx.send("Launching marbles. Credit for background music: Rozen - Battle for Spira (feat. Julie Elven) https://youtu.be/TpXtRt6hM4Q?si=xkdA83vHXMZZ1J1E")
            cwd = os.getcwd()
            print(cwd)
            os.chdir(MARBLES_PATH)
            print(os.getcwd())
            launch_path = MARBLES_PATH
            print(launch_path)
            self.marbles = subprocess.Popen(["python", "marblesMain.py"])
            os.chdir(cwd)
            print("Marbles started.")
        else:
            print("===  MARBLES ALREADY RUNNING  ===")
        
    
    def game_ended_check(self):
        try:
            game_running = self.process.poll()
            if game_running == None:
                # Game is still running.
                return False
            else:
                # Game has been ended properly.
                self.process = None
                return True
        except:
            # Game has not been started.
            return False

    # Stuck command
    @commands.command(aliases=("stuck_all"))
    async def stuck(self, ctx: commands.Context):
        #await ctx.send("Attempting to un-stuck the system. Stand by.")
        if self.is_valid_user(ctx):
            await self.kill(ctx)
            await self.marbles_end(ctx)
            await ctx.send("Everything should now be unstuck.")

# Main entry point of script
if __name__ == "__main__":
    conf = BotConfig(CONFIG_FILE_PATH)
    print("================================")
    print("================================")
    print(conf.data["csr_path"])
    CSR_PATH = conf.data["csr_path"]
    print(conf.data["game_path"])
    GAME_PATH = conf.data["game_path"]
    TIMER_PATH = conf.data["timer_path"]
    print("================================")
    print("================================")

    bot = Bot(conf.data)
    bot.run()
