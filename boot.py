import sys
import json5
import mysql.connector

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class Boot():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def boot(self):
		guild = self.bot.get_guild(public["guild"])
		channel = guild.get_channel(public["channels"]["Members"])
		await channel.edit(name="Members: " + str(guild.member_count))