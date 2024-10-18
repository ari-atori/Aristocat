import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class Ping(commands.Cog, name="ping"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="ping", description="See if I am still alive")
	async def ping(self, interaction: Interaction):
		await interaction.response.send_message("Pong!")

def setup(bot):
	bot.add_cog(Ping(bot))