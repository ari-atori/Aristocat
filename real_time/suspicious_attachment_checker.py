import sys
import json5

import nextcord
from nextcord.ext import commands

with open("secrets/config_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	config = json5.load(file)

with open("public_" + (sys.argv[1] if len(sys.argv) > 1 else "prod") + ".json") as file:
	public = json5.load(file)

class SuspiciousAttachmentChecker():
	def __init__(self, bot):
		self.bot : commands.Bot = bot
		self.executables = [
			"application/x-msdownload",
			"application/x-ms-installer",
			"application/x-elf",
			"application/vnd.debian.binary-package",
			"application/x-debian-package",
			"application/x-executable",
			"application/x-rpm",
			"application/x-sh",
			"application/java-archive",
			"text/x-python",
			"text/x-perl",
			"application/octet-stream"
		]
		self.compressions = [
			"application/x-zip-compressed",
			"application/zip",
			"application/zip-compressed",
			"application/x-xz",
			"application/x-bzip",
			"application/x-bzip2",
			"application/x-gtar",
			"application/x-gzip",
			"application/vnd.rar",
			"application/x-7z-compressed"
			"application/x-tar"
		]

	async def check(self, message: nextcord.Message):
		foundExec = False
		foundComp = False
		for i in range(len(message.attachments)):
			# TODO: This code is absolute dogwater. The reason this is bad is because Discord does not actually look at
			# file contents to check for MIME type, but instead just the extension. I think you can see how one can
			# exploit this shit. The problem is that the platorm I host my bot with doesn't allow installation of binary
			# packages, as libmagic1 is needed for python-magic. I see various other libraries I can check, and I can
			# even roll my own since I already do that for my video editor application. But for now, this will do
			if foundExec and foundComp:
				break
			mimetype = message.attachments[i].content_type
			if mimetype in self.executables and not foundExec:
				await message.add_reaction("⚠️")
				foundExec = True
			elif mimetype in self.compressions and not foundComp:
				await message.add_reaction("🗜️")
				foundComp = True

