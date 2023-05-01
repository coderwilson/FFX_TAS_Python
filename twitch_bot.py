from twitchio.ext import commands
import subprocess
import signal

# Define the users who are allowed to send commands
allowed_users = ["YOUR_CHANNEL_NAME", "OTHER_USER1", "OTHER_USER2", "OTHER_USER3"]

# Define the path to the Python script to run
script_path = "main.py"


# Define the bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token="YOUR_BOT_TOKEN", prefix="!", initial_channels=["YOUR_CHANNEL_NAME"]
        )
        self.process = None

    async def event_ready(self):
        # Notify when we are logged in and ready to use commands
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")

    # Define the start command
    @commands.command()
    async def start(self, ctx: commands.Context):
        if ctx.author.name in allowed_users:
            subprocess.Popen(["python", script_path])
            await ctx.send(f"{ctx.author.name}, the script has started!")

    # Define the restart command
    @commands.command()
    async def restart(self, ctx: commands.Context):
        if ctx.author.name in allowed_users:
            if self.process is not None:
                # Send a SIGINT signal to the previous process
                self.process.send_signal(signal.SIGINT)
                self.process.wait()  # Wait for the previous process to terminate

            # Start a new process
            self.process = subprocess.Popen(["python", script_path])
            await ctx.send(f"{ctx.author.name}, the script has been restarted!")


# Start the bot
bot = Bot()
bot.run()
