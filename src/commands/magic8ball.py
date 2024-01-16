import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import random

class Magic8ball(commands.Cog, name="magic8ball"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="magic8ball", description="Ask me a yes/no question?")
	async def magic8ball(self, interaction: Interaction, question: str = SlashOption(description="A yes-no question", required=True)):
		responses = ["Yes", "No", "Who knows?"]
		await interaction.response.send_message(responses[random.randint(0, 2)])

def setup(bot):
	bot.add_cog(Magic8ball(bot))