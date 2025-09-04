import sys
import json5

import re

import nextcord
from nextcord.ext import commands

from adblockparser import AdblockRules

with open("resources/urlfilters.txt", "r", encoding="utf-8") as file:
	rules = AdblockRules([line.strip() for line in file if line.strip() != "" and not line.startswith('!') and not line.startswith("[")])

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class SuspiciousLinkChecker():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def check(self, message: nextcord.Message):
		channel = self.bot.get_channel(public["channels"]["bot-reporting-channel"])
		if not channel:
			try:
				channel = await self.bot.fetch_channel(public["channels"]["bot-reporting-channel"])
			except:
				return
			
		matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', message.content)
		suspicion = False
		for text, url in matches:
			if text != url:
				suspicion = True
				break
		
		matches = re.findall(r'(https?://[^\s)]+)', message.content)
		for match in matches:
			if rules.should_block(match):
				description = message.content.replace("](", "] (")
				embed = nextcord.Embed(color=0xa53b3b, description = description)
				embed.set_author(name = f"Potentially Malicious Link(s) Detected | {message.author.display_name} ({message.author.id})", icon_url = message.author.display_avatar.url)
				await channel.send(embed = embed)
				await message.delete()
				return
		
		if suspicion:
			await message.add_reaction("⚠️")
		
		
			
		




