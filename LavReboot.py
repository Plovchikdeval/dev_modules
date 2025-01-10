__version__ = (0, 0, 3)

"""
	█ █▀█ █▄█ █ ▄█   █▀▄ █▀█ █▀▀
 ▄▀ █▄█ █ █ █▀ █   █▄▀ █▄█ ██▄
 (C) 2024 t.me/undef1n3dd
 Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# scope: hikka_min 1.3.3
# meta developer: @devjmodules
# requires: subprocess psutil signal

import logging
import subprocess
import psutil
import os
import signal

from telethon.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class LavReboot(loader.Module):
	"""Restart your LavHost without using a bot"""

	strings = {
		"name": "LavReboot",
		"restart_err": "<blockquote><emoji document_id=4915853119839011973>⚠️</emoji> | <b>Something went wrong! Check logs!</b></blockquote>",
		"only_lavhost": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>| This module works only with ✌️ lavHost !</b></blockquote>",
	}

	strings_ru = {
		"restart_err": "<blockquote><emoji document_id=4915853119839011973>⚠️</emoji> | <b>Что-то пошло не так! Проверьте логи!</b></blockquote>",
		"only_lavhost": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>| Этот модуль работает только с ✌️ lavHost !</b></blockquote>",
	}

	def find_process(self, user, process):
		for proc in psutil.process_iter(['pid', 'username', 'cmdline']):
			try:
				if proc.info['username'] == user and ' '.join(proc.info['cmdline']) == process:
					return proc
			except (psutil.NoSuchProcess, psutil.AccessDenied):
				pass
		return None

	@loader.command(en_doc="Restart", ru_doc="Перезагрузить")
	async def lhrestart(self, message: Message):
		platform = utils.get_named_platform()
		if not 'lavHost' in platform:
			await utils.answer(message, self.strings("only_lavhost"))
			return

		user = subprocess.run(["whoami"], capture_output=True, text=True).stdout.strip()
		process = "/usr/bin/python3.10 -m hikka"

		found_process = self.find_process(user, process)

		if found_process:
			await self.invoke(command="restart", args=["-f"], message=message, edit=True)
			pid = found_process.info['pid']
			try:
				os.kill(pid, signal.SIGABRT)
			except PermissionError:
				logger.error("LavReboot | You don't have permission!")
		else:
			await utils.answer(message, self.strings("restart_err"))
			logger.error("LavReboot | Userbot process not found!")
