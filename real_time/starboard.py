import sys
import json5
import math
import mysql.connector

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

with open("public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

class Starboard():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	def stars_required(self, limit, typical_members, typical_stars, members):
		a = limit
		b = (math.log(limit - typical_stars) - math.log(limit - 1))/(typical_members - 1)
		c = (typical_members * math.log(limit - 1) - math.log(limit - typical_stars))/(typical_members - 1)
		return round(a - math.exp(b * members + c))

	async def star(self, payload: nextcord.RawReactionActionEvent):
		channel = self.bot.get_channel(payload.channel_id)
		if not channel:
			try:
				channel = await self.bot.fetch_channel(payload.channel_id)
			except:
				return

		category = channel.category_id
		for cat in public["categories"]:
			if category == public["categories"][cat]:
				return

		message = await channel.fetch_message(payload.message_id)
		reactions = message.reactions
		guild = self.bot.get_guild(public["guild"])
		criteria = self.stars_required(limit = 5, typical_members = 31, typical_stars = 4, members = guild.member_count)
		stars = 0
		for r in reactions:
			if r.emoji == "⭐":
				stars = r.count
				break

		if stars < criteria:
			return
		
		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		query = "SELECT EXISTS(SELECT 1 FROM starboard WHERE message_id = %s)"
		params = (payload.message_id,)
		mycursor.execute(query, params)

		if mycursor.fetchone()[0] > 0:
			mydb.close()
			return

		embeds = [nextcord.Embed(color=0xffac33, url = message.jump_url, description = message.content)]
		embeds[0].set_author(name = f"{message.author.display_name} | {r.count}⭐", icon_url = message.author.display_avatar.url, url = message.jump_url)

		attachments = ""
		if (len(message.attachments) > 0):
			attnum = 1
			for att in message.attachments:
				attachments += f"[[{att.filename}]]({att.url})\n"
				if att.content_type and att.content_type.startswith('image/'):
					embed = nextcord.Embed(color=0xffac33, url = message.jump_url)
					embed.set_image(att.url)
					embeds.append(embed)
				else:
					embeds[0].add_field(name = f"Attachment {attnum}", value=attachments)
					attnum += 1

		starboard = self.bot.get_channel(public["channels"]["starboard"])
		if not starboard:
			try:
				starboard = await self.bot.fetch_channel(public["channels"]["starboard"])
			except:
				return
		await starboard.send(embeds = embeds)
		query = "INSERT INTO starboard (message_id, stars) VALUES (%s, %s)"
		params = (message.id, stars)
		mycursor.execute(query, params)
		mydb.close()
