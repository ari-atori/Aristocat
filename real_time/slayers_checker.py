import sys
import json5
import aiohttp
import time

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class SlayerChecker():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def update(self, user : nextcord.Member):
		slayer = user.guild.get_role(public["roles"]["slayer"])
		if slayer is None:
			slayer = await user.guild.fetch_role(public["roles"]["slayer"])

		hasRole = user in slayer.members

		hasTag = False
		async with aiohttp.ClientSession() as session:
			headers = { "User-Agent": "Aristocat (https://github.com/ari-atori/Aristocat,1)", "Authorization": f"Bot {config["token"]}" }
			url = f"https://discord.com/api/users/{user.id}"
			async with session.get(url, headers=headers) as r:
				if r.status == 200:
					js = await r.json()
					if "primary_guild" in js:
						if js["primary_guild"]["identity_enabled"]:
							if int(js["primary_guild"]["identity_guild_id"]) == public["guild"]:
								hasTag = True
				elif r.status == 423:
					js = await r.json()
					time.sleep(float(js["retry_after"])) 
		
		if hasTag and not hasRole:
			await user.add_roles(slayer)
		elif not hasTag and hasRole:
			await user.remove_roles(slayer)


