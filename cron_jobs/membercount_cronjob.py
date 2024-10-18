import sys
import json5
import mysql.connector

from nextcord.ext import commands

with open("public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

with open("secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class MemberCountLoop():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.members = 0

	async def run(self):
		guild = self.bot.get_guild(public["guild"])
		if (guild.member_count == self.members):
			return
		
		channel = guild.get_channel(public["channels"]["Members"])
		if not channel:
			channel = await guild.fetch_channel(public["channels"]["Members"])
		await channel.edit(name="Members: " + str(guild.member_count))

		self.members = guild.member_count