import sys
import json5
import mysql.connector

from nextcord.ext import tasks, commands

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

class SlayerCountLoop():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.slayers = 0
		self.run.start()

	@tasks.loop(minutes=15)
	async def run(self):
		guild = self.bot.get_guild(public["guild"])
	
		role = guild.get_role(public["roles"]["slayer"])
		if not role:
			role = await guild.fetch_role(public["roles"]["slayer"])

		if len(role.members) == self.slayers:
			return

		channel = guild.get_channel(public["channels"]["Slayers"])
		if not channel:
			channel = await guild.fetch_channel(public["channels"]["Slayers"])
		await channel.edit(name="[💙Slayers]: " + str(len(role.members)))

		self.slayers = len(role.members)

	@run.before_loop
	async def prep(self):
		await self.bot.wait_until_ready()
