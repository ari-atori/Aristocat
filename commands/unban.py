import sys
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import json5

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class Unban(commands.Cog, name="unban"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="unban", description="Lift the ban of a particular user")
	async def unban(self, interaction: Interaction, snowflake : str = SlashOption(description="User ID/Snowflake", required=True), reason: str = SlashOption(description="Reason to ban the user, if any", required=False)):
		guild = self.bot.get_guild(public["guild"])
		moderator = self.bot.get_guild(public["guild"]).get_role(public["roles"]["Moderator"])

		userid = int(snowflake)
		user = None
		try:
			user = await self.bot.fetch_user(userid)
		except:
			await interaction.response.send_message("Unban unsuccessful!")
			return
		
		if interaction.user.id != public["users"]["Ari Atori"] and moderator not in interaction.user.roles:
			await interaction.response.send_message("I shall only listen to moderators and my other virgin master")
			return
		if userid == public["users"]["Ari Atori"]:
			await interaction.response.send_message("Ari Atori is already within our presence, unfortunately")
			return
		if userid == public["users"]["Aristocat"]:
			await interaction.response.send_message("Considering you used this command of mine, I am already not banned")
			return

		await guild.unban(user = user, reason = reason)
		await interaction.response.send_message("Unban successful!")

def setup(bot):
	bot.add_cog(Unban(bot))