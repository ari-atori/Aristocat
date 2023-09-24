# Main entry point

import os
import sys
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import nextcord
import json5
from nextcord.ext import commands
from nextcord.ext.commands import Context

from cron_jobs import birthday_cronjob

from real_time import member_arithmetic

intents = nextcord.Intents.default().all()

# TODO: Set command argument to load either beta or production configurations
with open("../secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class Aristocat(commands.Bot):
	def __init__(self, logger, config) -> None:
		super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents, help_command=None)
		self.logger: logging.Logger = logger
		self.config: dict = config
		self.super = super()

class LoggingFormatter(logging.Formatter):
	black: str = "\x1b[30m"
	gray: str = "\x1b[38m"
	red: str = "\x1b[31m"
	yellow: str = "\x1b[33m"
	green: str = "\x1b[32m"
	blue: str = "\x1b[34m"

	reset: str = "\x1b[0m"
	bold: str = "\x1b[1m"

	COLORS: dict[int, str] = {
		logging.DEBUG: gray + bold,
		logging.INFO: blue + bold,
		logging.WARNING: yellow + bold,
		logging.ERROR: red,
		logging.CRITICAL: red + bold,
	}

	def format(self, record) -> str:
		log_color: str = self.COLORS[record.levelno]
		format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
		format: str = format.replace("(black)", self.black + self.bold)
		format = format.replace("(reset)", self.reset)
		format = format.replace("(levelcolor)", log_color)
		format = format.replace("(green)", self.green + self.bold)
		formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
		return formatter.format(record)

logger: logging.Logger = logging.getLogger(name="aristocat_" + sys.argv[1])
logger.setLevel(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

file_handler = logging.FileHandler(filename="logs_" + sys.argv[1] + ".log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
	"[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

bot = Aristocat(logger=logger, config=config)

async def on_ready() -> None:
	if bot.user is None:
		sys.exit("Bot has no associated user!")

async def status_task():
	await bot.change_presence(activity=nextcord.Game("status"))

members = member_arithmetic.Member(bot)

@bot.event
async def on_member_join(member: nextcord.Member) -> None:
	await members.join(member)

@bot.event
async def on_member_remove(member: nextcord.Member) -> None:
	await members.remove(member)


@bot.event
async def on_message(message: nextcord.Message) -> None:
	if message.author == bot.user or message.author.bot:
		return

@bot.event
async def on_command_completion(context: Context) -> None:
	if context.command is None:
		return
	full_command_name: str = context.command.qualified_name
	split: list[str] = full_command_name.split(" ")
	executed_command = split[0]

async def on_command_error(context: Context, error) -> None:
	description: str
	if isinstance(error, commands.CommandOnCooldown):
		minutes, seconds = divmod(error.retry_after, 60)
		hours, minutes = divmod(minutes, 60)
		description = "**This command is on cooldown** - You may use this command in %i hours, %i minutes, and %i seconds" % (round(hours), round(minutes), round(seconds))
	elif isinstance(error, commands.MissingPermissions):
		description = "You do not have the required privileges"
	elif isinstance(error, commands.BotMissingPermissions):
		description = "I apparently do not have the needed permissions"
	elif isinstance(error, commands.MissingRequiredArgument):
		description = str(error).capitalize()

	embed = nextcord.Embed( description = description, color = 0xE02020 )
	await context.send(embed=embed)

if __name__ == "__main__":
	for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/commands"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				bot.load_extension(f"commands.{extension}")
				bot.logger.info(f"Loaded extension '{extension}'")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				bot.logger.error(f"Failed to load extension {extension}\n{exception}")

birthdays = birthday_cronjob.BirthdayLoop(bot)

scheduler = AsyncIOScheduler()
scheduler.add_job(birthdays.run, CronTrigger(hour = "8", minute = "0", second = "0", timezone="EST"))
scheduler.start()

bot.run(config["token"])
