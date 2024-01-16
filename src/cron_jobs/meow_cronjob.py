import sys
import json5
import random

from nextcord.ext import commands

with open("../public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

with open("../secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class Meow():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.elapsed = 0
		self.required = random.randint(8, 12)

	async def run(self):
		channel = self.bot.get_channel(public["channels"]["general"])
		self.elapsed += 1
		if self.elapsed == self.required:
			catpeople = public["roles"]["catpeople"]
			mention = f"<@&{catpeople}>"
			await channel.send(f"{mention} meow")
			self.elapsed = 0
			self.required = random.randint(8, 12)
		