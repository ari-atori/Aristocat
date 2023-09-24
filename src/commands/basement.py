import sys
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import json5

with open("../public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

class Basement(commands.Cog, name="basement"):
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	@nextcord.slash_command(name="basement", description="Cast or free someone into or from the basement")
	async def basement(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="The target user", required=True), bs : bool = SlashOption(description="True if basement, false if free", required=False, default=True)):
		
		moderator = self.bot.get_guild(public["guild"]).get_role(public["roles"]["Moderator"])
		dweller = self.bot.get_guild(public["guild"]).get_role(public["roles"]["dweller"])
		
		if interaction.user.id != public["users"]["Ari Atori"] and moderator not in interaction.user.roles:
			await interaction.response.send_message("I shall only listen to moderators and my other virgin master")
			return
		if dweller in interaction.user.roles:
			await interaction.response.send_message("I do not listen to neckbeards")
			return
		if user.id == public["users"]["Ari Atori"]:
			await interaction.response.send_message("Ari Atori is already a neckbeard, but is too feared for us to try and contain him")
			return
		if user.id == public["users"]["Aristocat"]:
			await interaction.response.send_message("I shall not condemn myself to that mere status")
			return
		if moderator in user.roles and interaction.user.id != public["users"]["Ari Atori"]:
			await interaction.response.send_message("Only Ari Atori may directly deal with moderators")
			return
		
		if bs == True:
			if dweller in user.roles:
				await interaction.response.send_message("The individual is already a neckbeard. How can you not smell their status from your distance?!")
				return
			await user.add_roles(dweller)
			await interaction.response.send_message("They grow a thorny vineyard along their neck as they are casted away")
		else:
			if dweller not in user.roles:
				await interaction.response.send_message("The individual is already a free being")
				return
			await user.remove_roles(dweller)
			await interaction.response.send_message("Their being walks out a free person")

def setup(bot):
	bot.add_cog(Basement(bot))