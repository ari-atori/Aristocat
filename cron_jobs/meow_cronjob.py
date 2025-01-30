import sys
import json5
import random

from nextcord.ext import tasks, commands

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

class Meow(commands.Cog):
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.elapsed = 0
		self.required = random.randint(8, 12)
		self.run.start()

	@tasks.loop(hours=1.0)
	async def run(self):
		channel = self.bot.get_channel(public["channels"]["catpeople"])
		self.elapsed += 1
		if self.elapsed == self.required:
			catpeople = public["roles"]["catpeople"]
			mention = f"<@&{catpeople}>"
			await channel.send(f"{mention} meow")
			self.elapsed = 0
			self.required = random.randint(8, 12)

	@run.before_loop
	async def prep(self):
		await self.bot.wait_until_ready()

	
		