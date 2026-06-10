from twitchio.ext import commands
import subprocess
import random
from json_ai_files.update_leaderboard import TrackerManager
from datetime import datetime
import sys
import os
import asyncio
import json
import time

import yaml
import logging
import pyautogui
from timer_saver_logic.timer_reset import clickHeader
from typing import Dict
import psutil
import pygetwindow as gw
import ctypes
from json_ai_files.write_seed import write_big_text
from json_ai_files.write_seed_results import check_ml_heals
from types import SimpleNamespace
from obswebsocket import obsws, requests

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
LANGUAGE_FILE = "C:\\Users\\coder\\Documents\\SQUARE ENIX\\FINAL FANTASY X&X-2 HD Remaster"
CHOSEN_SEED_NUM = 999

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

def terminate_ff_processes():
    """Identify and terminate processes with 'marbles' in their names (case-insensitive)."""
    terminated = []
    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"]
            if "ffx" in process_name.lower():
                process.terminate()  # Request termination
                terminated.append(process.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Process might have ended or can't be accessed
    
    if terminated:
        print(f"Terminated processes: {terminated}")
    else:
        print("No processes with 'marbles' in their names found.")

def focus_obs():
    # --- 1. Debug: List all open windows to find the correct title ---
    print("\n--- Diagnostic: Active Window Titles ---")
    all_windows = gw.getAllTitles()
    clean_titles = [t for t in all_windows if t.strip()]
    for title in clean_titles:
        print(f"Active Window: {title}")
    print("----------------------------------------\n")

    # --- NEW: Minimize Visual Studio Code ---
    print("Searching for Visual Studio Code to minimize...")
    vscode_windows = [
        win for win in gw.getWindowsWithTitle('') 
        if "visual studio code" in win.title.lower()
    ]
    
    for vscode_win in vscode_windows:
        try:
            # SW_MINIMIZE = 6
            ctypes.windll.user32.ShowWindow(vscode_win._hWnd, 6)
            print(f"Minimized: '{vscode_win.title}'")
        except Exception as e:
            print(f"Failed to minimize VS Code: {e}")
    
    if vscode_windows:
        time.sleep(0.3) # Brief pause for the minimize animation

    # --- 2. Focus PowerShell and press Backspace ---
    print("Searching for PowerShell window...")
    
    # We look for common PowerShell window title patterns
    # (Windows PowerShell, PowerShell Core, or Windows Terminal)
    pwsh_keywords = ["PowerShell", "pwsh", "Windows Terminal", "Administrator: PowerShell"]
    pwsh_windows = [
        win for win in gw.getWindowsWithTitle('') 
        if any(key.lower() in win.title.lower() for key in pwsh_keywords)
    ]

    if pwsh_windows:
        # Sort by visibility or just grab the first match
        pwsh_win = pwsh_windows[0]
        print(f"Found PowerShell match: '{pwsh_win.title}'")
        
        try:
            # Using the Minimize/Restore trick here too, as it's more reliable than SetForegroundWindow alone
            ctypes.windll.user32.ShowWindow(pwsh_win._hWnd, 6)  # SW_MINIMIZE
            time.sleep(0.1)
            ctypes.windll.user32.ShowWindow(pwsh_win._hWnd, 9)  # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(pwsh_win._hWnd)
            
            time.sleep(0.3) # Wait for focus to settle
            pyautogui.press('backspace')
            print("Pressed Backspace in PowerShell.")
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed to focus PowerShell window: {e}")
    else:
        print("PowerShell window not found by title search.")

    # --- 3. Focus OBS (Original Logic) ---
    print("Searching for 'obs64.exe' process...")
    obs_processes = [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] and "obs64.exe" in p.info['name'].lower()]
    
    if not obs_processes:
        print("OBS process (obs64.exe) not found.")
        return False

    obs_windows = [win for win in gw.getWindowsWithTitle('') if "OBS" in win.title]

    if not obs_windows:
        print("OBS window not found.")
        return False

    obs_window = obs_windows[0]
    print(f"Attempting to focus OBS window: '{obs_window.title}'")

    # Minimize and restore to force foreground focus
    ctypes.windll.user32.ShowWindow(obs_window._hWnd, 6)  # SW_MINIMIZE
    time.sleep(0.2)
    ctypes.windll.user32.ShowWindow(obs_window._hWnd, 9)  # SW_RESTORE
    time.sleep(0.1)
    ctypes.windll.user32.SetForegroundWindow(obs_window._hWnd)

    print(f"Successfully brought OBS window '{obs_window.title}' to focus.")
    

    # --- 4. Focus LiveSplit (Final active window) ---
    print("Searching for LiveSplit window...")
    
    # Common variations for LiveSplit window titles
    livesplit_keywords = ["LiveSplit", "LiveSplit.exe"]
    ls_windows = [
        win for win in gw.getWindowsWithTitle('') 
        if any(key.lower() in win.title.lower() for key in livesplit_keywords)
    ]

    if ls_windows:
        # Pick the first match (usually the main timer window)
        ls_win = ls_windows[0]
        print(f"Found LiveSplit match: '{ls_win.title}'")
        
        try:
            # Minimize and Restore to force focus over other windows
            ctypes.windll.user32.ShowWindow(ls_win._hWnd, 6)  # SW_MINIMIZE
            time.sleep(0.1)
            ctypes.windll.user32.ShowWindow(ls_win._hWnd, 9)  # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(ls_win._hWnd)
            
            print(f"LiveSplit '{ls_win.title}' is now the active window.")
        except Exception as e:
            print(f"Failed to focus LiveSplit: {e}")
    else:
        print("LiveSplit window not found.")
    return True

def decide_seed(ctx):
    global CHOSEN_SEED_NUM
    args = ctx.message.content.lower().split()
    
    print("\n=== Deciding Seed ===")
    
    # 1. Priority: Manual Seed Override
    for i in range(len(args)):
        try:
            if args[i] == "seed":
                CHOSEN_SEED_NUM = str(args[i + 1])
                print(f"=== Manual Seed Passed: {CHOSEN_SEED_NUM} ===")
                return
        except (IndexError, ValueError):
            pass

    # 2. Check for specialty runs that don't use the "Missing Seed" logic
    run_types = ["classic", "story", "nem", "plat", "godrng"]
    is_specialty = any(x in args for x in run_types)

    # 3. If it's a regular run (or we want to force a missing seed)
    if not is_specialty:
        tm = TrackerManager()
        missing = tm.find_missing_seeds()
        if missing:
            CHOSEN_SEED_NUM = random.choice(missing)
            print(f"=== Missing Seed Selected: {CHOSEN_SEED_NUM} ===")
            return

    # 4. Fallback: Standard Random
    CHOSEN_SEED_NUM = str(random.choice(range(256)))
    print(f"=== Fallback Random Seed: {CHOSEN_SEED_NUM} ===")

def set_language(force:str='none'):
    global CHOSEN_SEED_NUM
    print(f"Checking ML heals for seed {CHOSEN_SEED_NUM}")
    modifier, avina_heals = check_ml_heals(seed_num=CHOSEN_SEED_NUM)
    print(f"Running ")

    if force.lower() == 'english':
        desired_str = "Language=en"
        search_str = "Language=ch"
    elif force.lower() == 'chinese':
        desired_str = "Language=ch"
        search_str = "Language=en"
    else:
        desired_str = "Language=ch"
        search_str = "Language=en"
    print(f"Running {desired_str} Mark 1")
    orig_dir = os.getcwd()
    print(os.getcwd())
    os.chdir(LANGUAGE_FILE)
    print(os.getcwd())
    print(f"Running {desired_str} Mark 2")
    with open("GameSetting.ini",'r') as f:
        contents=f.read()

    contents=contents.replace(search_str,desired_str)
    
    with open("GameSetting.ini",'w') as f:
        f.write(contents)
    os.chdir(orig_dir)
    print(os.getcwd())
    print("=== Language has been set ====")
    time.sleep(1)


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

    if category=="platinum":
        file_name='Final Fantasy X - PC - Platinum.lss'
        category_name = 'PC Platinum%'
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
        
        self.obs_pwd = config.get("obs_key", "YOUR_OBS_KEY")
        
        # Start connection monitor
        self.connection_check_task = None

    async def event_disconnect(self):
        """Called when the bot loses connection to Twitch chat."""
        print("[WARN] Lost connection to Twitch chat.")
        print("[INFO] Attempting to reconnect in 30 seconds...")

        # Wait 30 seconds before trying to reconnect
        await asyncio.sleep(30)

        # Try reconnecting safely
        try:
            await self.connect()
            print("[INFO] Reconnected to Twitch chat successfully.")
        except Exception as e:
            print(f"[ERROR] Reconnection failed: {e}")
            # Optional: schedule another retry after a delay
            asyncio.create_task(self._delayed_reconnect())
    
    async def _delayed_reconnect(self):
        """Retry reconnecting if the first attempt failed."""
        await asyncio.sleep(60)
        try:
            await self.connect()
            print("[INFO] Reconnected after retry.")
        except Exception as e:
            print(f"[ERROR] Second reconnection attempt failed: {e}")

    async def shutdown_obs(self):
        """Gracefully stop OBS system."""
        try:
            ws = obsws("localhost", 4455, "G7v9Xp2rLwB4qZ8M")
            ws.connect()
            print("Connected to OBS via WebSocket.")

            # Stop streaming if active
            try:
                ws.call(requests.StopStream())
                print("Stopped streaming.")
            except Exception:
                print("Streaming was not active or already stopped.")

            # Give OBS a moment to wrap up
            await asyncio.sleep(6)

            # Tell OBS to quit gracefully, once every 20 seconds, until closed.
            counter = 0
            while any(p.name() == "obs64.exe" for p in psutil.process_iter()):
                await asyncio.sleep(1)
                if counter % 20 == 0:
                    print("Mark 1")
                    stream_status = ws.call(requests.GetStreamStatus())
                    print(stream_status.getOutputActive())
                    print("Mark 2")
                    if stream_status.getOutputActive():
                        print("Mark 3")
                        print("OBS is streaming, stopping now...")
                        ws.call(requests.StopStream())
                    elif counter < 600:
                        print("Mark 4")
                        # print(stream_status)
                        # print(f"{stream_status.getStreaming()} | {record_status.getIsRecording()}")
                        print("Sending quit command.")
                        try:
                            from pywinauto import Application
                            app = Application(backend="uia").connect(path="obs64.exe")
                            window = app.top_window()
                            window.close()  # Sends WM_CLOSE
                            print("Sent close window command to OBS.")
                        except Exception as e:
                            print(f"Could not send close command: {e}")


                        # ws.call(requests.Quit(force=False))
                        # ws.call(requests.TriggerHotkeyByName("Quit OBS"))
                        # try:
                        #     for p in psutil.process_iter():
                        #         if p.name() == "obs64.exe":
                        #             print("Terminating OBS process...")
                        #             p.terminate()  # sends graceful SIGTERM
                        #             try:
                        #                 p.wait(timeout=30)  # wait up to 30 seconds for it to close
                        #                 print("Terminated gracefully.")
                        #             except:
                        #                 print("Terminate command completed WITH ERRORS")
                        # except:
                        #     pass

                        time.sleep(3)
                    else:
                        print("Mark 5")
                        # print("OBS did not terminate after 200 seconds. Force killing...")
                        # for p in psutil.process_iter():
                        #     if p.name() == "obs64.exe":
                        #         p.terminate()
                        pass
                counter += 1
                print(f"OBS Close counter: {counter}")
            print("OBS closed.")
            await asyncio.sleep(3)

            ws.disconnect()

        except Exception as e:
            print(f"Error shutting down OBS: {e}")
            
    @commands.command(name="obs_test")
    async def obs_test(self, ctx: commands.Context):
        await self.shutdown_obs()
    
    def is_valid_user(self, ctx: commands.Context):
        # 1. Check if the internal python process is running
        process_active = False
        if self.process is not None:
            # Check if the subprocess is still running
            if self.process.poll() is None:
                process_active = True
            else:
                # Clean up if it finished
                self.process = None

        # 2. Check if the game (ffx.exe) is running
        game_active = any(p.info['name'] == "ffx.exe" for p in psutil.process_iter(['name']))

        # Logic: If nothing is running, anyone can use the bot. 
        # If something IS running, we check for Mod/Allowed status.
        if not process_active and not game_active:
            print("System idle (Process/Game not running). Granting access to regular user.")
            return True

        # 3. Standard permission check for active sessions
        if ctx.author.is_mod or ctx.author.name.lower() in [u.lower() for u in self.allowed_users]:
            print("Identified mod or elevated user. Valid User function returning True.")
            return True
        else:
            print(f"Access denied: {ctx.author.name} is not a mod and a session is currently active.")
            # Note: ctx.send is a coroutine, so it won't work inside a synchronous def unless you use asyncio.run_coroutine_threadsafe
            # For simplicity, we usually handle the message back in the command function itself.
            return False

    def is_valid_user_old(self, ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name in self.allowed_users:
            print("Identified mod or elevated user. Valid User function returning True.")
            return True
        else:
            print("Regular user. Valid User function returning False.")
            ctx.send(
                f"Sorry {ctx.author.name}, you don't have permissions to execute this. Please wait for the run to finish or ask for mod status."
            )
            return False
        
    @commands.command(name="reboot")
    async def reboot(self, ctx: commands.Context):
        """Performs a full system reboot (Windows only)."""

        await self.kill(ctx)

        await ctx.send("Stopping stream and rebooting the system... 💻")

        await self.shutdown_obs()
        
        # Reboot the system
        import os
        print("Rebooting system...")
        os.system("shutdown /r /t 0")
        
    async def event_ready(self):
        # if not self.connection_check_task:
        #     self.connection_check_task = asyncio.create_task(self._monitor_connection())
        # Notify when we are logged in and ready to use commands
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")
        print("Ready for commands")
        for channel in self.connected_channels:
            await channel.send(f"aVIna is now online! Ready for commands.")
        
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

    @commands.command(aliases=("continue"))
    async def resume(self, ctx: commands.Context):
        if not self.is_valid_user(ctx):
            return
        global CHOSEN_SEED_NUM
        if CHOSEN_SEED_NUM == 999:
            CHOSEN_SEED_NUM = str(random.choice(range(256)))
        set_language(force='english')
        await self.start_csr(ctx)
        time.sleep(1)
        await self.start_game(ctx)
        time.sleep(2)
        focus_obs()
        
        arg_array = []
        print(ctx.message.content)
        time.sleep(2)
        arg_array.append("-state")
        arg_array.append("Nem_Farm")
        arg_array.append("-step")
        arg_array.append("100")
        arg_array.append("-platinum")
        arg_array.append("True")

        # arg_array.append("-state")
        # arg_array.append("Nem_Farm")
        # arg_array.append("-step")
        # arg_array.append("99")
        # arg_array.append("-platinum")
        # arg_array.append("True")

        # arg_array.append("-state")
        # arg_array.append("Nem_Farm")
        # arg_array.append("-step")
        # arg_array.append("99")
        # arg_array.append("-nemesis")
        # arg_array.append("True")

        # arg_array.append("-state")
        # arg_array.append("Nem_Farm")
        # arg_array.append("-step")
        # arg_array.append("9")
        # arg_array.append("-platinum")
        # arg_array.append("True")

        arg_array.append("-seed")
        arg_array.append("0")
        
        print(arg_array)
        time.sleep(2)
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
    @commands.command(aliases=("begin", "launch"))
    async def start(self, ctx: commands.Context):
        if not self.is_valid_user(ctx):
            return
        
        global CHOSEN_SEED_NUM
        # Only pick a random seed if start_all hasn't already assigned a missing one
        if CHOSEN_SEED_NUM == 999:
            CHOSEN_SEED_NUM = str(random.choice(range(256)))
            
        arg_array = []
        args = ctx.message.content.split()

        for i in range(len(args)):
            try:
                low_arg = args[i].lower()
                if low_arg in ["state", "stage"]:
                    arg_array.extend(["-state", args[i + 1]])
                if low_arg == "step":
                    arg_array.extend(["-step", args[i + 1]])
                if low_arg == "blitz":
                    arg_array.extend(["-train_blitz", "True"])
                if low_arg == "godrng":
                    arg_array.extend(["-godrng", "True"])
                if low_arg == "classic":
                    arg_array.extend(["-classic", "True"])
                elif low_arg == "story":
                    arg_array.extend(["-story", "True"])
                elif low_arg == "nem":
                    arg_array.extend(["-nemesis", "True"])
                elif low_arg == "plat":
                    arg_array.extend(["-platinum", "True"])
            except Exception:
                pass

        arg_array.extend(["-seed", str(CHOSEN_SEED_NUM)])
        
        CHOSEN_SEED_NUM = 999  # Reset

        if self.process is None and self.marbles is None:
            self.process = subprocess.Popen(["python", SCRIPT_PATH] + arg_array)
            print(f"aVIna FFX TAS started with args: {arg_array}")
        else:
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
        if not self.is_valid_user(ctx):
            return
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
        # if "plat" in ctx.message.content:
        #     logger.info("CSR undesirable for Platinum runs.")
        #     return
        arg_array = []
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
        if await self.get_current_obs_scene() != "FFX TAS runs":
            await self.change_obs_scene("FFX TAS runs")
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
        if await self.get_current_obs_scene() == "FFX TAS runs":
            await self.change_obs_scene("FFX Idle")
        write_big_text("")
        if self.game is not None:
            self.game.terminate()
            self.game.wait()
            self.game = None
            terminate_ff_processes()
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
        if self.timer is None and self.marbles is None:
            if "plat" in ctx.message.content.lower():
                cat = "platinum"
            elif "nem" in ctx.message.content.lower():
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
        if not self.is_valid_user(ctx):
            return
        clickHeader()
        print("Save successful.")
        time.sleep(0.5)
        print("Killing process.")
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
            "Primary commands: !kill, !stuck, !all, !skip_split, !undo_split | " + \
            "Instructions for starting a run are on screen after running !stuck command."
        )
        
    @commands.command(aliases=("full_schedule"))
    async def schedule(self, ctx: commands.Context):
        response = "For the basic '!all' command, the bot will decide the type of run. "
        response += "Special runs occur between 4am and 2pm PST on the following days. "
        response += "Tuesday: Classic. Thursday: Nemesis. "
        response += "Friday: Story mode. Saturday: Platinum. "
        response += "If you'd like to force a regular run, type '!all speed' instead."
        await ctx.send(response)
    
    # Start All
    @commands.command(aliases=("begin_all", "all"))
    async def start_all(self, ctx: commands.Context):
        if not self.is_valid_user(ctx):
            return
        
        await self.marbles_end(ctx)
        language_set = False

        # 1. Apply Daily Schedule to the message content if no type specified
        content = ctx.message.content.lower()
        blocking_keywords = ["classic", "story", "nem", "plat", "stage", "state", "step", "speed"]
        if not any(x in content for x in blocking_keywords):
            now = datetime.now()
            day = now.weekday()
            hour = now.hour
            is_specialty_window = bool(4 <= hour < 14)
            if is_specialty_window:
                if day == 1: ctx.message.content += " classic"
                elif day == 3: ctx.message.content += " nem"
                elif day == 4: 
                    ctx.message.content += " story"
                    language_set = True
                    set_language(force='english')
                elif day == 5: ctx.message.content += " plat"
        
        # 2. Decide the seed (uses our updated logic above)
        decide_seed(ctx)
        
        # 3. Execution Chain
        await ctx.send("Launching all elements!")
        
        # Language selection
        if not language_set:
            if "story" in content or "english" in content:
                set_language(force='english')
            elif "chinese" in content:
                set_language(force='chinese')
            else:
                set_language()

        await self.start_game(ctx)
        time.sleep(3)
        await self.start_csr(ctx)
        time.sleep(1)

        if "state" not in content:
            await self.start_timer(ctx)

        time.sleep(3)
        focus_obs()
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
        await self.change_obs_scene("Marbles scene")
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
        
    # Stuck command
    @commands.command(aliases=("stuck_all"))
    async def stuck(self, ctx: commands.Context):
        #await ctx.send("Attempting to un-stuck the system. Stand by.")
        if self.is_valid_user(ctx):
            await self.change_obs_scene("FFX Idle")
            await self.kill(ctx)
            await self.marbles_end(ctx)
            await ctx.send("Everything should now be unstuck.")
        else:
            await ctx.send("Please check with a mod - need elevated permissions to unstuck.")
    
    async def get_current_obs_scene(self) -> str:
        try:
            ws = obsws("localhost", 4455, self.obs_pwd)
            ws.connect()

            response = ws.call(requests.GetCurrentProgramScene())
            current_scene = response.getSceneName()

            ws.disconnect()
            print(f"Current OBS scene: {current_scene}")
            return current_scene

        except Exception as e:
            print(f"[ERROR] Could not get current OBS scene: {e}")
            return None
    
    @commands.command()
    async def scene(self, ctx: commands.Context):
        last_scene = await self.get_current_obs_scene()
        if last_scene != "FFX TAS runs":
            await self.change_obs_scene("FFX TAS runs")
        else:
            await self.change_obs_scene("FFX Idle")
    
    async def change_obs_scene(self, scene_name: str, host="localhost", port=4455, timeout=5):
        """
        Change OBS program scene, verify success, and return True/False.
        Runs blocking obswebsocket calls in a thread so the event loop is not blocked.
        """
        loop = asyncio.get_running_loop()

        def _blocking_change():
            try:
                ws = obsws(host, port, self.obs_pwd)
                ws.connect()
            except Exception as e:
                return {"ok": False, "error": f"Could not connect to OBS WebSocket: {e}"}

            try:
                # Try to get list of scenes
                try:
                    scenes_resp = ws.call(requests.GetSceneList())
                    # try a few different ways to extract names depending on library version
                    try:
                        scenes = [s.getSceneName() for s in scenes_resp.getScenes()]
                    except Exception:
                        # fallback if objects are dicts
                        scenes = [s.get("sceneName") or s.get("name") for s in scenes_resp.getScenes()]
                except Exception as e:
                    ws.disconnect()
                    return {"ok": False, "error": f"GetSceneList failed: {e}"}

                # Debug: return available scenes if not found
                if scene_name not in scenes:
                    ws.disconnect()
                    return {"ok": False, "error": "Scene not found", "available_scenes": scenes}

                # Set the scene
                try:
                    ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
                except Exception as e:
                    ws.disconnect()
                    return {"ok": False, "error": f"SetCurrentProgramScene failed: {e}"}

                # Verify
                try:
                    cur = ws.call(requests.GetCurrentProgramScene())
                    try:
                        cur_name = cur.getSceneName()
                    except Exception:
                        # fallback to dict access if needed
                        cur_name = cur.get("currentProgramScene") or cur.get("sceneName") or None
                except Exception as e:
                    ws.disconnect()
                    return {"ok": False, "error": f"GetCurrentProgramScene failed: {e}"}

                ws.disconnect()
                return {"ok": True, "current_scene": cur_name}
            except Exception as e:
                try:
                    ws.disconnect()
                except Exception:
                    pass
                return {"ok": False, "error": f"Unexpected error: {e}"}

        # run blocking work in default ThreadPoolExecutor
        result = await loop.run_in_executor(None, _blocking_change)

        # print/log useful debug info
        if not result.get("ok"):
            print(f"[OBS] change_obs_scene failed: {result.get('error')}")
            if "available_scenes" in result:
                print(f"[OBS] Available scenes: {result['available_scenes']}")
            return False

        cur = result.get("current_scene")
        print(f"[OBS] Successfully switched. Current scene: {cur}")
        return True

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
