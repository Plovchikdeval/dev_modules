__version__ = (0, 0, 5)

"""
  █ █▀█ █▄█ █ ▄█   █▀▄ █▀█ █▀▀
 ▄▀ █▄█ █ █ █▀ █   █▄▀ █▄█ ██▄
 (C) 2024 t.me/u1n1n1a1m1e1d
 Created special for TotHosting 
"""
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @devjmodules
# requires: requests
# meta banner: http://ndpropave5.temp.swtest.ru/files/EJp.jpg

import logging
import aiohttp
import requests
import typing
import asyncio
import json
from datetime import datetime, timedelta

from telethon.tl.types import PeerUser, Message
from ..inline.types import InlineCall

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ToTHostMod(loader.Module):
	"""Managing userbot on ToTHost"""

	strings = {
		"name": "ToTHost",
		"tot_info": "<blockquote><emoji document_id=5452140079495518256>💘</emoji> <b>ToTHost Manager</b></blockquote>\n\n<blockquote>👤 | <code>{userid}</code></blockquote>\n<blockquote><emoji document_id=5472026645659401564>🗓</emoji> | <b>Registration date:</b> {reg_date}</blockquote>\n<blockquote><emoji document_id=5375296873982604963>💰</emoji> | <b>Balance:</b> {balance}₽</blockquote>",
		"userbot_info": "<blockquote><emoji document_id=5452140079495518256>💘</emoji> <b>ToTHost:</b> {userbot_name}</blockquote>\n\n<blockquote>🤖 | <b>Userbot:</b> {userbot}</blockquote>\n<blockquote>🆔 | <b>ID:</b> {userbot_id}</blockquote>\n<blockquote>🟢 |<b>Status:</b> {status}</blockquote>\n<blockquote>{location} | <b>Server:</b> {server}</blockquote>\n<blockquote>⏰ | Expires: {exp_date}</blockquote>",
		"status_active": "Active",
		"status_freezed": "Freezed",
		"status_deactived": "Deactived",
		"restart": "<blockquote><emoji document_id=5375338737028841420>🔄</emoji> <b><emoji document_id=5253874021061118203>🍆</emoji><emoji document_id=5255971528469662704>🍆</emoji><emoji document_id=5255982609485283509>🍆</emoji><emoji document_id=5253803983029422224>🍆</emoji> | Restarting userbot...</b><blockquote>",
		"restart_np": "<blockquote><emoji document_id=5375338737028841420>🔄</emoji> ToTHost | Restarting userbot...</b><blockquote>",
		"restart_ok": "<blockquote><emoji document_id=5465465194056525619>👍</emoji> <b>[{botid}] Restart was successful!</b></blockquote>",
		"restart_err": "<blockquote><emoji document_id=5447644880824181073>⚠️</emoji> <b>Error! Check logs</b></blockquote>",
		"btn_restart": "🔄 Restart",
		"btn_back": "⬅️ Back",
		"btn_close": "❌ Close",
		"no_token": "<blockquote><emoji document_id=5472255352667904566>😔</emoji> <b>Token not found!</b></blockquote>\n<blockquote>Please go to @ToThosTing_bot</blockquote>\n<blockquote>Enter <code>/get_token</code></blockquote>\n<blockquote>And paste it into the config.</blockquote>",
		"args_err": "<blockquote><emoji document_id=5463358164705489689>⛔️</emoji> <b>You must provide ID</b></blockquote>",
		"wait": "⏳ Wait...",
	}

	strings_ru = {
		"tot_info": "<blockquote><emoji document_id=5452140079495518256>💘</emoji> <b>Менеджер ToTHost</b></blockquote>\n\n<blockquote>👤 | <code>{userid}</code></blockquote>\n<blockquote><emoji document_id=5472026645659401564>🗓</emoji> | <b>Дата регистрации:</b> {reg_date}</blockquote>\n<blockquote><emoji document_id=5375296873982604963>💰</emoji> | <b>Баланс:</b> {balance}₽</blockquote>",
		"userbot_info": "<blockquote><emoji document_id=5452140079495518256>💘</emoji> <b>ToTHost:</b> {userbot_name}</blockquote>\n\n<blockquote>🤖 | <b>Юзербот:</b> {userbot}</blockquote>\n<blockquote>🆔 | <b>ID:</b> {userbot_id}</blockquote>\n<blockquote>🟢 |<b>Статус:</b> {status}</blockquote>\n<blockquote>{location} | <b>Сервер:</b> {server}</blockquote>\n<blockquote>⏰ | Истекает: {exp_date}</blockquote>",
		"status_active": "Активен",
		"status_freezed": "Заморожен",
		"status_deactived": "Деактивирован",
		"restart": "<blockquote><emoji document_id=5375338737028841420>🔄</emoji> <b><emoji document_id=5253874021061118203>🍆</emoji><emoji document_id=5255971528469662704>🍆</emoji><emoji document_id=5255982609485283509>🍆</emoji><emoji document_id=5253803983029422224>🍆</emoji> | Перезапуск юзербота...</b></blockquote>",
		"restart_np": "<blockquote><emoji document_id=5375338737028841420>🔄</emoji> ToTHost | Перезапуск юзербота...</b></blockquote>",
		"restart_ok": "<blockquote><emoji document_id=5465465194056525619>👍</emoji> <b>[{botid}] Перезагрузка прошла успешно!</b></blockquote>",
		"restart_err": "<blockquote><emoji document_id=5447644880824181073>⚠️</emoji> <b>Ошибка! Проверьте логи</b></blockquote>",
		"btn_restart": "🔄 Перезапуск",
		"btn_back": "⬅️ Назад",
		"btn_close": "❌ Закрыть",
		"no_token": "<blockquote><emoji document_id=5472255352667904566>😔</emoji> <b>Токен не найден!</b></blockquote>\n<blockquote>Пожалуйста, перейдите в @ToThosTing_bot</blockquote>\n<blockquote>Введите <code>/get_token</code></blockquote>\n<blockquote>И вставьте его в конфигурацию.</blockquote>",
		"args_err": "<blockquote><emoji document_id=5463358164705489689>⛔️</emoji> <b>Вы должны указать ID</b></blockquote>",
		"wait": "⏳ Ожидайте...",
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
					"Token",
					None,
					lambda: self.strings("token"),
					validator=loader.validators.Union(
						loader.validators.Hidden(),
						loader.validators.NoneType(),
						),
				),
			)

	async def client_ready(self, client, db):
		self._client = client
		self._db = db
		self._name = self.strings("name")
		self.api = "http://api.tothost.xyz:8000/api/v1"
		self.bot = "@ToThosTing_bot"
		if not self._db.get(self.name, "token") and not self.config["Token"]:
			try:
				async with self._client.conversation(self.bot) as conversation:
					msg = await conversation.send_message("/start")
					r = await conversation.get_response()
					await msg.delete()
					await r.delete()
					r_token = await conversation.send_message("/get_token")
					token = await conversation.get_response()
					self._db.set(self.name, "token", token.text)
					await r_token.delete()
					await token.delete()
			except Exception as e:
				logger.error(f"Error: {e}", exc_info=True)

		if not self.config["Token"]:
			self.token = self._db.get(self.name, "token")
		else:
			self.token = self.config["Token"]

		try:
			restart_ok = self._db.get(self.name, "restart_ok")
			if restart_ok:
				ok_msg = json.loads(restart_ok)
				self._db.set(self.name, "restart_ok", None)
				await self._client.edit_message(ok_msg["chat_id"], ok_msg["id"], self.strings("restart_ok").format(botid=ok_msg["botid"]))
		except Exception as e:
			logger.error(f"Edit message failed: {e}", exc_info=True)

	async def get_user_info(self, token: str) -> typing.Optional[dict]:
		headers = {
			'accept': 'application/json'
		}
		async with aiohttp.ClientSession() as session:
			try:
				async with session.get(f"{self.api}/user/user_info?token={token}", headers=headers) as response:
					response.raise_for_status()
					data = await response.json()

					if data.get("status_code"):
						raise Exception(data)
						return None
					else:
						try:
							registered_date = datetime.fromisoformat(data['registeredDate']).strftime('%d.%m.%Y')
						except ValueError as e:
							logger.error(f"ToTHostMod | Date error: {e}", exc_info=True)
							registered_date = data['registeredDate']

						filtered_data = {
							'userID': data['userID'],
							'balance': data['balance'],
							'registeredDate': registered_date,
							'userbots': data['userbots']
						}

						return filtered_data

			except aiohttp.ClientResponseError as e:
				logger.error(f"ToTHostMod | Error while requesting: {e}", exc_info=True)
			except Exception as e:
				logger.error(f"ToTHostMod | Error: {e}", exc_info=True)

	async def get_userbot_info(self, botid: int, token: str) -> typing.Optional[dict]:
		headers = {
			'accept': 'application/json'
		}
		async with aiohttp.ClientSession() as session:
			try:
				async with session.get(f"{self.api}/userbot/userbot_info?userbotID={botid}&token={token}", headers=headers) as response:
					response.raise_for_status()
					data = await response.json()

					if data.get("status_code"):
						raise Exception(data)
						return None
					else:
						return data

			except aiohttp.ClientResponseError as e:
				logger.error(f"ToTHostMod | Error while requesting: {e}", exc_info=True)
			except Exception as e:
				logger.error(f"ToTHostMod | Error: {e}", exc_info=True)

	async def get_userbot_status(self, botid: int, token: str) -> typing.Optional[dict]:
		headers = {
			'accept': 'application/json'
		}
		async with aiohttp.ClientSession() as session:
			try:
				async with session.get(f"{self.api}/userbot/status?userbotID={botid}&token={token}") as response:
					response.raise_for_status()
					data = await response.json()

					if data.get("status_code"):
						raise Exception(data)
						return None
					else:
						return data["status"]
			except aiohttp.ClientResponseError as e:
				logger.error(f"ToTHostMod | Error while requesting: {e}", exc_info=True)
			except Exception as e:
				logger.error(f"ToTHostMod | Error: {e}", exc_info=True)

	async def restart_userbot(self, botid: int, token: str):
		headers = {
			'accept': 'application/json'
		}
		try:
			response = requests.get(f"{self.api}/userbot/restart?userbotID={botid}&token={token}", headers=headers)
			response.raise_for_status()
			data = await response.json()

			if data.get("status_code"):
				raise Exception(data)
			else:
				return True

		except Exception as e:
			logger.error(f"ToTHostMod | Error: {e}", exc_info=True)

	async def _general_info(self) -> str:
		user = await self.get_user_info(self.token)

		text = self.strings("tot_info").format(userid=user["userID"], reg_date=user["registeredDate"], balance=user["balance"])

		keyboard = []
		current_row = []
		for index, userbot in enumerate(user["userbots"]):
			current_row.append({"text": f'{userbot["userbotID"]} {userbot["server"]["emoji"]} | {userbot["uname"] if userbot["uname"] else userbot["name"]}', "callback": self._callback_display_userbot_info, "args": [userbot["userbotID"]]})
			if (index + 1) % 3 == 0:
				keyboard.append(current_row)
				current_row = []

		if current_row:
			keyboard.append(current_row)

		keyboard.append([{"text": self.strings("btn_close"), "callback": self._callback_handle_close}])

		return text, keyboard

	async def _userbot_info(self, botid: int, token: str) -> str:
		userbot_data = await self.get_userbot_info(botid, token)

		status = await self.get_userbot_status(botid, token)

		if status == "active":
			status = self.strings("status_active")
		elif status == "unknown" and userbot_data["status"] == "FREEZE":
			status = self.strings("status_freezed")
		else:
			status = self.strings("status_deactived")

		server = userbot_data["server"]["text"]
		location = userbot_data["server"]["emoji"]

		end_datetime = datetime(userbot_data["endDate"]["year"], userbot_data["endDate"]["month"], userbot_data["endDate"]["day"], userbot_data["endDate"]["hour"], userbot_data["endDate"]["minute"], userbot_data["endDate"]["second"])
		now = datetime.now()
		days_left = (end_datetime - now).days

		expires = end_datetime.strftime(f"%d.%m.%y %H:%M:%S ({days_left} дней)")

		userbot_info = self.strings("userbot_info").format(userbot_name=userbot_data["uname"], userbot=userbot_data["name"], userbot_id=userbot_data["userbotID"], status=status, server=server, location=location, exp_date=expires)

		return userbot_info

	async def _callback_handle_close(self, call: InlineCall):
		await call.delete()

	async def _callback_go_back(self, call: InlineCall):
		text, keyboard = await self._general_info()

		await call.edit(text=text, reply_markup=keyboard)

	async def _callback_display_userbot_info(self, call: InlineCall, botid: int):
		userbot_info = await self._userbot_info(botid, self.token)
		keyboard = [
			[
				{"text": self.strings("btn_restart"), "callback": self._callback_restart_userbot, "args": [botid]}
			],
			[{"text": self.strings("btn_back"), "callback": self._callback_go_back}]
		]

		await call.edit(text=userbot_info, reply_markup=keyboard)

	async def _callback_restart_userbot(self, call: InlineCall, botid: int):
		await call.answer(self.strings("wait"), show_alert=True)
		restart_status = await self.restart_userbot(botid, self.token)

		if not restart_status:
			await call.answer(utils.escape_html(self.strings("restart_err")))

	@loader.command(en_doc="Display info", ru_doc="Вывести инфо")
	async def totinfo(self, message: typing.Union[InlineCall, Message]):
		"""Display info"""
		if not self.token:
			await utils.answer(message, self.strings("no_token"))
			await self.invoke("config", self.name, message.chat_id)
			return

		text, keyboard = await self._general_info()

		await self.inline.form(
			text=text,
			message=message,
			reply_markup=keyboard,
			ttl=300
			)

	@loader.command(en_doc="Restart userbot", ru_doc="Перезагрузить юзербота")
	async def totrestart(self, message: Message):
		"""Restart usebot"""
		if not self.token:
			await utils.answer(message, self.strings("no_token"))
			await self.invoke("config", self.name, message.chat_id)
			return

		args = utils.get_args(message)
		if not args:
			await utils.answer(message, self.strings("args_err"))
			return

		me = await self._client.get_me()

		await utils.answer(message, self.strings("restart") if me.premium else self.strings("restart_np"))
		await asyncio.sleep(3)

		if isinstance(message.peer_id, PeerUser):
			chat_id = message.peer_id.user_id
		else:
			chat_id = message.chat.id

		ok_msg_data = {
			'id': message.id,
			'chat_id': chat_id,
			'botid': args[0],
		}

		ok_msg = json.dumps(ok_msg_data)

		self._db.set(self.name, "restart_ok", ok_msg)
		restart_status = await self.restart_userbot(args[0], self.token)
		if not restart_status:
			self._db.set(self.name, "restart_ok", None)
			await utils.answer(message, self.strings("restart_err"))
