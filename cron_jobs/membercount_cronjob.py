import sys
import json5
import mysql.connector

from nextcord.ext import tasks, commands

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

class MemberCountLoop():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.members = 0
		self.run.start()

	@tasks.loop(minutes=15)
	async def run(self):
		guild = self.bot.get_guild(public["guild"])
		if (guild.member_count == self.members):
			return
		
		channel = guild.get_channel(public["channels"]["Members"])
		if not channel:
			channel = await guild.fetch_channel(public["channels"]["Members"])
		await channel.edit(name="Members: " + str(guild.member_count))

		self.members = guild.member_count

	@run.before_loop
	async def prep(self):
		await self.bot.wait_until_ready()