import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import random

class RocksPaperScissors(commands.Cog, name="rps"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="rps", description="Rock Paper Scissors")
	async def rps(self, interaction: Interaction, choice: str = SlashOption(description="Choose between the three", required=True, choices={"🪨", "📄", "✂️"})):
		responses = ["🪨", "📄", "✂️"]
		response = responses[random.randint(0, 2)]
		msg = f"I chose {response}! Looks like you lost..."
		if response == choice:
			msg = f"I also chose {response}. Let's try another round!"
		elif (response, choice) in [("🪨", "📄"),("📄","✂️"),("✂️","🪨")]:
			msg = f"I chose {response}! Looks like you won!"
			
		await interaction.response.send_message(msg)

def setup(bot):
	bot.add_cog(RocksPaperScissors(bot))
	