import sys
import json5
import string

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class PassiveMeow():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.channels = {}
		self.meows = [
			"mau"
			"meaw",
			"meoa",
			"meou",
			"meow",
			"mew",
			"mewl",
			"miao",
			"miaou",
			"miaow",
			"miau",
			"miaul",
			"miyau",
			"mjau",
			"mnau",
			"moew",
			"mow",
			"mraw",
			"mrawr",
			"mrow",
			"mrowr",
			"mua",
			"myau",
			"nya",
			"nyah",
			"nyahn",
			"nyan",
			"nyav"
		]

	async def meow(self, message : nextcord.Message):
		translate = str.maketrans("", "", string.punctuation)
		content = message.content.lower().translate(translate)

		# Remove repeated characters, that way nnnnyyyyaaaahhhhhhhh could be reduced to nyah, allowing it to count
		fade = ''.join(['' if i > 0 and e == content[i - 1] else e for i,e in enumerate(content)])

		channel = message.channel
		value = self.channels.get(channel.id, None)
		if value is None:
			self.channels[channel.id] = 1 if fade in self.meows else 0
			return
		else:
			if fade not in self.meows:
				self.channels[channel.id] = 0
				return
			value += 1
			if value % 6 == 3:
				await channel.send("meow")
			self.channels[channel.id] = value
