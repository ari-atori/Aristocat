import sys
import json5
import mysql.connector

from nextcord.ext import commands

with open("../public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

with open("../secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

class BirthdayLoop():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def run(self):
		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT id, mention, birthday FROM birthdays WHERE DAY(NOW()) = DAY(CONVERT_TZ(birthday, '+00:00', '+13:00')) AND MONTH(NOW()) = MONTH(CONVERT_TZ(birthday, '+00:00', '+13:00'))")
		channel = self.bot.get_channel(public["channels"]["general"])
		for bd in mycursor:
			await channel.send(f"Happy birthday {bd[1]}!")
		mydb.commit()
		mycursor.close()
		mydb.close()