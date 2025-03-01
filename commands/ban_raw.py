import sys
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import json5

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class BanRaw(commands.Cog, name="ban_raw"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="ban_raw", description="Ban the user in question, even if they've never visited the server")
	async def ban_raw(self, interaction: Interaction, snowflake : str = SlashOption(description="User ID/Snowflake", required=True), reason: str = SlashOption(description="Reason to ban the user, if any", required=False), delete_seconds : int = SlashOption(description="Delete messages from the them past X seconds", required=False)):
		guild = self.bot.get_guild(public["guild"])
		moderator = self.bot.get_guild(public["guild"]).get_role(public["roles"]["Moderator"])

		userid = int(snowflake)
		user = None
		try:
			user = await self.bot.fetch_user(userid)
		except:
			await interaction.response.send_message("Unban unsuccessful!")
			return
		member = guild.get_member(userid)
		
		if interaction.user.id != public["users"]["Ari Atori"] and moderator not in interaction.user.roles:
			await interaction.response.send_message("I shall only listen to moderators and my other virgin master")
			return
		if userid == public["users"]["Ari Atori"]:
			await interaction.response.send_message("Ari Atori is too feared for us to try and ban him")
			return
		if userid == public["users"]["Aristocat"]:
			await interaction.response.send_message("I shall not ban myself from this shithole")
			return
		if member is not None and moderator in member.roles and interaction.user.id != public["users"]["Ari Atori"]:
			await interaction.response.send_message("Only Ari Atori may directly deal with moderators")
			return

		await guild.ban(user = user, reason = reason, delete_message_seconds = delete_seconds)

		try:
			title = "User Preemptively Banned"
			if member is not None:
				title = "Member Banned"

			description = f"{user.global_name} has been preemptively banned banned without a reason given"
			if member is not None:
				if reason is None:
					description = f"{member.global_name} was banned without a reason given"
				else:
					description = f"{member.global_name} was banned for: {reason}"
			else:
				if reason is None:
					description = f"{user.global_name} has been preemptively banned without a reason given"
				else:
					description = f"{user.global_name} has been preemptively banned for: {reason}"
			color=0x000000

			embed = nextcord.Embed(title = title, color = color, description = description)
			embed.set_author(name = f"{user.global_name} ({userid})", icon_url = user.display_avatar.url)
			welcomebye = self.bot.get_channel(public["channels"]["welcome-bye"])
			if not welcomebye:
				welcomebye = await self.bot.fetch_channel(public["channels"]["welcome-bye"])
			await welcomebye.send(embed = embed)

			await interaction.response.send_message("Raw Ban successful!")
		except Exception as e:
			await interaction.response.send_message(f"[WARNING] Failed to enter preemptive ban in for user ({userid}): {e}")



def setup(bot):
	bot.add_cog(BanRaw(bot))