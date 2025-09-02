import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

class LaTeX(commands.Cog, name="latex"):
	def __init__(self, bot):
		self.bot = bot
		plt.rcParams['mathtext.fontset'] = 'cm'

	@nextcord.slash_command(name="latex", description="Write a LaTeX expression to render")
	async def latex(self, interaction: Interaction, latex: str = SlashOption(description="LaTeX expression", required=True)):
		if not latex.startswith("$"):
			latex = "$" + latex
		if not latex.endswith("$"):
			latex += "$"

		if len(latex) > 1026: # 2^10 chars for expression + 2 potential chars for $
			await interaction.response.send_message("I'm sorry, your expression is too long. Try breaking it down into a few statements")
			return
		
		fig, axes = plt.subplots()
		fig.patch.set_facecolor('black')
		axes.set_facecolor('black')
		fig.patch.set_visible(False)
		axes.axis('off')
		axes.text(0.5, 0.5, latex, fontsize=32, ha='center', va='center', color='white', bbox=dict(facecolor='black', edgecolor='none', pad=10))

		buffer = BytesIO()
		plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2, facecolor='black', transparent=False)
		plt.close(fig)
		buffer.seek(0)

		file = nextcord.File(fp=buffer, filename="latex.png")
		embed = nextcord.Embed(color=0x00cdff)
		embed.set_image("attachment://latex.png")
		await interaction.response.send_message(embed = embed, file=file)


	
		

def setup(bot):
	bot.add_cog(LaTeX(bot))