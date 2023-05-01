from twitchio.ext import commands
import subprocess

import yaml
import logging
from typing import Dict

logger = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Define the path to the Python script to run
SCRIPT_PATH = "main.py"
CONFIG_FILE_PATH = "bot-config.yaml"


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

    async def event_ready(self):
        # Notify when we are logged in and ready to use commands
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")
        print("Ready for commands")

    # Define the start command
    @commands.command()
    async def start(self, ctx: commands.Context):
        print(ctx.message.content)
        args = ctx.message.content.split()
        print(args)
        force_seed = ""
        for i in range(len(args)):
            try:
                if args[i].lower() == "seed":
                    force_seed = True
                    seed_num = str(args[i+1])
            except:
                force_seed = ""
        
        if force_seed == True and (int(seed_num) > 255 or int(seed_num) <= -1):
            await ctx.send(f"{seed_num} is an invalid seed number. Try again.")
        elif self.process is None:
            if force_seed:
                self.process = subprocess.Popen(["python", SCRIPT_PATH, "-seed", seed_num])
            else:
                self.process = subprocess.Popen(["python", SCRIPT_PATH])
            await ctx.send("FFX TAS started.")
        else:
            await ctx.send("FFX TAS is already running.")
        return self.process

    # Define the exit command
    @commands.command()
    async def exit(self, ctx: commands.Context):
        if not ctx.author.name in self.allowed_users:
            await ctx.send(f"Sorry {ctx.author.name}, you don't have permissions to execute commands.")
        elif self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            await ctx.send("FFX TAS stopped.")
        else:
            await ctx.send("FFX TAS is not running.")

    # Define the stop command
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.author.name in self.allowed_users:
            await ctx.send(f"Sorry {ctx.author.name}, you don't have permissions to execute commands.")
        elif self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            await ctx.send("FFX TAS stopped.")
        else:
            await ctx.send("FFX TAS is not running.")

    # Define the help command
    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send("Available commands: !start, !stop, !exit, !help")


# Main entry point of script
if __name__ == "__main__":
    conf = BotConfig(CONFIG_FILE_PATH)

    bot = Bot(conf.data)
    bot.run()
