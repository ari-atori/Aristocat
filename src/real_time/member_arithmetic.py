# Mainly used for the reinstating of statuses and the updating of profiles that could gives roles

import sys
import json5
import mysql.connector

import nextcord
from nextcord.ext import commands

with open("../secrets/config_" + sys.argv[1] + ".json") as file:
	config = json5.load(file)

with open("../public_" + sys.argv[1] + ".json") as file:
	public = json5.load(file)

class Member():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def join(self, user : nextcord.Member):
		guild = self.bot.get_guild(public["guild"])
		channel = guild.get_channel(public["channels"]["Members"])
		await channel.edit(name="Members: " + str(guild.member_count))

		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(f"SELECT id, role FROM roles WHERE id={user.id}")

		for ir in mycursor:
			role = guild.get_role(ir[1])
			if role.name == "@everyone":
				continue
			await user.add_roles(role)
		mydb.commit()
		mycursor.close()
		mydb.close()

	async def remove(self, user : nextcord.Member):
		guild = self.bot.get_guild(public["guild"])
		channel = guild.get_channel(public["channels"]["Members"])
		await channel.edit(name="Members: " + str(guild.member_count))
		
		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(f"DELETE FROM roles WHERE id={user.id}")
		mydb.commit()
		for r in user.roles:
			if r.name == "@everyone":
				continue
			mycursor.execute(f"INSERT INTO roles VALUES ({user.id}, {r.id})")
			mydb.commit
		mycursor.close()
		mydb.close()