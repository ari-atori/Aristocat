import sys
import mysql.connector
import dateparser
from dateparser.search import search_dates
import json5

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

with open("secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class Birthday(commands.Cog, name="birthday"):
	def __init__(self, bot):
		self.bot = bot

	@nextcord.slash_command(name="setbirthday", description="Sets your birthday")
	async def setbirthday(self, interaction: Interaction, birthday: str = SlashOption(description="A date, like 'January 1st'", required=True), tz = SlashOption(description="Time Zone, like 'UTC'", required=False, default="UTC")):
		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		timeString = birthday
		time = dateparser.parse(timeString, settings={'TIMEZONE': tz, 'RETURN_AS_TIMEZONE_AWARE': True, 'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'})
		timeWords = timeString
		f = '%Y-%m-%d %H:%M:%S'
		if time is None:
			searchResults = search_dates(timeString, settings={'TIMEZONE': tz, 'RETURN_AS_TIMEZONE_AWARE': True, 'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'}, languages=['en'])
			if searchResults is None:
				await interaction.response.send_message("The time given has more spelling errors than a Hiroshiman child's DNA, please try a different format")
				return
				
			for sr in searchResults:
				time = sr[1]
				timeWords = sr[0]
				break
		if time is not None:
			timeUTC = dateparser.parse(time.strftime(f), settings={'TIMEZONE': 'UTC', 'TO_TIMEZONE': tz})
			mycursor = mydb.cursor(buffered=True)

			if timeUTC is None:
				await interaction.response.send_message("The time given has more spelling errors than a Hiroshiman child's DNA, please try a different format")
				return
			if interaction.user is None:
				await interaction.response.send_message("Your user information just does not seem to exist at the moment")
				return
			
			mycursor.execute(f"DELETE FROM birthdays WHERE id = '{interaction.user.id}'")
			mydb.commit()
			mycursor.execute("INSERT INTO birthdays (id, mention, birthday) VALUES ("+ str(interaction.user.id) +", '"+ str(interaction.user.mention) +"', '" + timeUTC.strftime(f) +"')")
			mydb.commit()
			mycursor.close()
			mydb.close()

			await interaction.response.send_message("Your birthday is set for: " + time.strftime(f) + " " + tz + " \n\nHere's the time I read: " + timeWords)
		else:
			await interaction.response.send_message("The time given has more spelling errors than a Hiroshiman child's DNA, please try a different format")

def setup(bot):
	bot.add_cog(Birthday(bot))