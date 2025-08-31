import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import aiohttp

class Cat(commands.Cog, name="cat"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="cat", description="Show a picture of a cat")
	async def cat(self, interaction: Interaction):
		async with aiohttp.ClientSession() as session:
			async with session.get("https://api.thecatapi.com/v1/images/search") as r:
				if r.status == 200:
					js = await r.json()
					embed = nextcord.Embed(color=0x00cdff)
					embed.set_image(js[0]["url"])
					await interaction.response.send_message(embed = embed)
				else:
					await interaction.response.send_message(f"The Cat API errored with a status code of {r.status}")

def setup(bot):
	bot.add_cog(Cat(bot))