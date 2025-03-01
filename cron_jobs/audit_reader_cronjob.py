import sys
import json5
import mysql.connector
from datetime import datetime

import nextcord
from nextcord.ext import tasks, commands

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

class AuditReader():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.members = 0
		self.lasttime = datetime.now()
		self.run.start()

	@tasks.loop(seconds=1)
	async def run(self):
		now = datetime.now()
		guild = self.bot.get_guild(public["guild"])
		
		async for entry in guild.audit_logs(after = self.lasttime):
			if entry.action == nextcord.AuditLogAction.unban:
				try:
					title = "User Unbanned"
					description = f"{entry.target.global_name} has gotten their ban lifted without a reason given"
					if entry.reason is not None:
						description = f"{entry.target.global_name} has gotten their ban lifted for: {entry.reason}"
					color=0xffffff

					embed = nextcord.Embed(title = title, color = color, description = description)
					embed.set_author(name = f"{entry.target.global_name} ({entry.target.name})", icon_url = entry.target.display_avatar.url)
					welcomebye = self.bot.get_channel(public["channels"]["welcome-bye"])
					if not welcomebye:
						welcomebye = await self.bot.fetch_channel(public["channels"]["welcome-bye"])
					await welcomebye.send(embed = embed)
				except:
					print(f"[WARNING] Failed to enter unban in for user: {entry.target.display_name} ({entry.target.id})")

		self.lasttime = now

	@run.before_loop
	async def prep(self):
		await self.bot.wait_until_ready()
		