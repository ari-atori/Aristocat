# Main entry point

import os
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import nextcord
import json5
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Context

import boot

from cron_jobs import birthday_cronjob
from cron_jobs import meow_cronjob

from real_time import member_arithmetic

intents = nextcord.Intents.default().all()

# TODO: Set command argument to load either beta or production configurations
with open("../secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class Aristocat(commands.Bot):
	def __init__(self, config) -> None:
		super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents, help_command=None)
		self.config: dict = config
		self.super = super()

bot = Aristocat(config=config)
booter = boot.Boot(bot)

@tasks.loop(minutes=1.0)
async def minute_tasks():
	await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="the damned voices"))

@bot.event
async def on_ready() -> None:
	if bot.user is None:
		sys.exit("Bot has no associated user!")
	await booter.boot()
	minute_tasks.start()

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
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				sys.exit(f"Failed to load extension {extension}\n{exception}")

birthdays = birthday_cronjob.BirthdayLoop(bot)
meow = meow_cronjob.Meow(bot)

scheduler = AsyncIOScheduler()
scheduler.add_job(birthdays.run, CronTrigger(hour = "8", minute = "0", second = "0", timezone="EST"))
scheduler.add_job(meow.run, CronTrigger(minute = "0", second = "0", timezone="EST"))
scheduler.start()

bot.run(config["token"])
