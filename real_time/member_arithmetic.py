# Mainly used for the reinstating of statuses and the updating of profiles that could gives roles

import sys
import json5
import mysql.connector

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class Member():
	def __init__(self, bot):
		self.bot : commands.Bot = bot

	async def join(self, user : nextcord.Member):
		guild = self.bot.get_guild(public["guild"])

		try:
			embed = nextcord.Embed(title = "New Member Joined", color=0x3ba55c, description = f"{user.global_name} has joined the server. Welcome!!! :wave:")
			embed.set_author(name = f"{user.global_name} ({user.name})", icon_url = user.display_avatar.url)
			welcomebye = self.bot.get_channel(public["channels"]["welcome-bye"])
			if not welcomebye:
				welcomebye = await self.bot.fetch_channel(public["channels"]["welcome-bye"])
			await welcomebye.send(embed = embed)
		except:
			print(f"[WARNING] Failed to enter in for user: {user.display_name} ({user.id})")

		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(f"SELECT id, role FROM roles WHERE id={user.id}")

		for ir in mycursor:
			role = guild.get_role(ir[1])
			if role.name == "@everyone" or role.id == public["roles"]["Moderator"]:
				continue
			await user.add_roles(role)
		mydb.commit()
		mycursor.close()
		mydb.close()

	async def remove(self, user : nextcord.Member):
		guild = self.bot.get_guild(public["guild"])

		try:
			kicked = False
			banned = False
			reason = ""
			async for entry in guild.audit_logs(action=nextcord.AuditLogAction.kick, after=user.joined_at, limit=16):
				if entry.target == user:
					kicked = True
					reason = entry.reason
			async for entry in guild.audit_logs(action=nextcord.AuditLogAction.ban, after=user.joined_at, limit=16):
				if entry.target == user:
					banned = True
					reason = entry.reason


			title = "Member Left"
			description = f"{user.global_name} has left the server"
			color=0xa53b3b
			if banned:
				title = "Member Banned"
				if reason is None:
					description = f"{user.global_name} was banned without a reason given"
				else:
					description = f"{user.global_name} was banned for: {reason}"
				color=0x000000
			elif kicked:
				title = "Member Kicked"
				if reason is None:
					description = f"{user.global_name} was kicked without a reason given"
				else:
					description = f"{user.global_name} was kicked for: {reason}"

			embed = nextcord.Embed(title = title, color = color, description = description)
			embed.set_author(name = f"{user.global_name} ({user.name})", icon_url = user.display_avatar.url)
			welcomebye = self.bot.get_channel(public["channels"]["welcome-bye"])
			if not welcomebye:
				welcomebye = await self.bot.fetch_channel(public["channels"]["welcome-bye"])
			await welcomebye.send(embed = embed)
		except:
			print(f"[WARNING] Failed to enter in for user: {user.display_name} ({user.id})")
		
		mydb = mysql.connector.connect(host=config["db_addr"], user=config["db_user"], password=config["db_pswd"], database=config["db_user"], autocommit=True)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(f"DELETE FROM roles WHERE id={user.id}")
		mydb.commit()
		for r in user.roles:
			if r.name == "@everyone" or role.id == public["roles"]["Moderator"]:
				continue
			mycursor.execute(f"INSERT INTO roles VALUES ({user.id}, {r.id})")
			mydb.commit
		mycursor.close()
		mydb.close()