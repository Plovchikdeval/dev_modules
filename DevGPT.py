__version__ = (1, 0, 3)

"""
  █ █▀█ █▄█ █ ▄█   █▀▄ █▀█ █▀▀
 ▄▀ █▄█ █ █ █▀ █   █▄▀ █▄█ ██▄
 (C) 2024 t.me/u1n1n1a1m1e1d
 Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @djmodules

import logging
import io
import os
import inspect
import aiohttp
import json

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class DevGPT(loader.Module):
	"""DevGPT - позволяет вам общаться с chatgpt и генерировать фото."""

	strings = {
		"name": "DevGPT",
		"wait": "<blockquote>🤖 <b>The server is processing the request, please wait...</b></blockquote>",
		"quest": "\n\n\n<blockquote>💭 <b>Your request:</b> {args}</blockquote>",
		"quest_img": "<blockquote><b>🔗 Link: <a href='{img_url}'>image</a></b></blockquote>\n\n<blockquote>💭 <b>Prompt:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote>🤖 <b>Model:</b> <code>{mdl}</code></blockquote>",
		"args_err": "<blockquote>ℹ️ <b>Usage: {prefix}dgpt/dgimg <model> <request></b></blockquote>",
		"query_err": "<blockquote>⛔️ <b>The request cannot be empty!</b></blockquote>",
		"server_err": "<blockquote>⚠️ <b>Server error: {error}</b></blockquote>",
		"image_err": "⚠️ <b>Error generating image: {error}</b>",
		"models_list": "<blockquote>📝 <b>Text</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote>🖼 <b>Images</b></blockquote>\n\n<blockquote>{img_models}</blockquote>",
		"model_not_found": "<blockquote>⛔️ <b>Model not found! List of available models: {prefix}dgmodels</b></blockquote>",
		"no_url": "No image URL received",
		"no_server_respond": "No response from the server",
		"fetch_failed": "<blockquote>❌ <b>Fetching data failed</b></blockquote>",
		"actual_version": "<blockquote>You have actual DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote>You have old DevGPT ({ver}) </b></blockquote>",
		"update_command": "<blockquote>To update type:</b> <code> {prefix}dlm {upd_file}</code>\n\n<b>New version: {new_ver} <b></blockquote>",
	}


	strings_ru = {
		"wait": "<blockquote>🤖 <b>Сервер обрабатывает запрос, подождите...</b></blockquote>",
		"quest": "\n\n\n<blockquote>💭 <b>Ваш запрос:</b> {args}</blockquote>",
		"quest_img": "<blockquote><b>🔗 Ссылка: <a href='{img_url}'>изображение</a></b></blockquote>\n\n<blockquote>💭 <b>Запрос:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote>🤖 <b>Модель:</b> <code>{mdl}</code></blockquote>",
		"args_err": "<blockquote>ℹ️ <b>Использование {prefix}dgpt/dgimg <модель> <запрос></b></blockquote>",
		"query_err": "<blockquote>⛔️ <b>Запрос не может быть пустым!</b></blockquote>",
		"server_err": "<blockquote>⚠️ <b>Ошибка сервера: {error}</b></blockquote>",
		"image_err": "⚠️ <b>Ошибка при генерации изображения: {error}</b>",
		"models_list": "<blockquote>📝 <b>Текст</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote>🖼 <b>Изображения</b></blockquote>\n\n<blockquote>{img_models}</blockquote>",
		"model_not_found": "<blockquote>⛔️ <b>Модель не найдена! Список доступных моделей {prefix}dgmodels</b></blockquote>",
		"no_url": "Не получен URL изображения",
		"no_server_respond": "Нет ответа от сервера",
		"fetch_failed": "<blockquote>❌ <b>Не удалось получить данные</b></blockquote>",
		"actual_version": "<blockquote>У вас актуальная версия DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote>У вас устаревшая версия DevGPT ({ver}) </b>\n\n<b>Новая версия: {new_ver} <b></blockquote>",
		"update_command": "<blockquote>Для обновления введите:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",

	}

	async def client_ready(self, client, _):
		self.server_url = "https://api.vysssotsky.ru"
		self.additional_server_url = "http://theksenon.pro/api/flux/generate"
		# self.api_key = self.config["api_key"]
		self.api_key = "xxx"

		self.repo = "https://raw.githubusercontent.com/Plovchikdeval/dev_modules/main"

		self._client = client
		self.prefix = self._client.loader.get_prefix()

		self.text_models = ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "o1-preview", "hermes-2-pro", "phi-2", "gemini-pro", "gemini-flash", "gemma-2b", "claude-3-haiku", "claude-3.5-sonnet", "blackboxai", "llava-13b", "openchat-3.5", "sonar-chat", "german-7b", "any-uncensored"]
		self.image_models = ["sd-3", "flux-pro", "flux-realism", "flux-anime", "flux-disney", "flux-pixel", "flux-4o", "any-dark"]
		self.additional_image_models = ["flux-pro", "flux-realism", "flux-anime", "flux-disney", "flux-pixel", "flux-4o"]

	async def generate_text(self, message, args):
		model = args.split()[0]
		content = args.replace(model, "").strip()

		if len(content) == 0:
			await utils.answer(message, self.strings("query_err"))
			return

		if model in self.text_models:
			try:
				payload = {
					"model": model,
					"messages": [{"role": "user", "content": content}],
					"max_tokens": 2048,
					"temperature": 0.7,
					"top_p": 1,
				}

				async with aiohttp.ClientSession() as session:
					async with session.post(f"{self.server_url}/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, data=json.dumps(payload)) as response:
						if response.status == 200:
							data = await response.json()
							answer = data.get("choices", [{}])[0].get("message", {}).get("content", self.strings("no_server_respond"))
							answer = f"<blockquote>{answer}</blockquote>"

							await utils.answer(message, answer + self.strings("quest").format(args=content))
						else:
							await utils.answer(message, self.strings("server_err").format(error=f"HTTP {response.status}"))
			except Exception as e:
				await utils.answer(message, self.strings("server_err").format(error=str(e)))
		else:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))


	async def generate_image(self, message, args):
		model = args.split()[0]
		prompt = args.replace(model, "").strip()

		if len(prompt) == 0:
			await utils.answer(message, self.strings("query_err"))
			return

		if model in self.image_models:
			try:
				payload = {
					"model": model,
					"prompt": prompt,
					"n": 1,
					"size": "1000x700",
				}

				async with aiohttp.ClientSession() as session:
					async with session.post(f"{self.server_url}/v1/images/generate", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, data=json.dumps(payload)) as response:
						if response.status == 200:
							data = await response.json()
							image_url = data.get("data", [{}])[0].get("url", None)

							if image_url:
								try:
									async with session.get(image_url) as generated_image:
										file_name = "dgimage.png"
										with open(file_name,'wb') as file:
											file.write(await generated_image.read())

									await message.delete()
									await self._client.send_file(message.chat_id, file_name, caption=(self.strings('quest_img').format(img_url=image_url, prmpt=prompt, mdl=model)))
								finally:
									if os.path.exists(file_name):
										os.remove(file_name)
							else:
								await utils.answer(message, self.strings("image_err").format(error=self.strings("no_url")))
						else:
							logger.error("API down! Trying to use another one.", exc_info=True)
							if model in self.additional_image_models:
								model = f"{model} is down used <i>flux-pro-mv</i> instead"
								headers = {"Content-Type": "application/json"}
								data = {"prompt": prompt}

								try:
									async with aiohttp.ClientSession() as session:
										async with session.post(self.additional_server_url, headers=headers, json=data) as response:
											response.raise_for_status()
											data = await response.text()
											try:
												data = json.loads(data)
												image_url = data.get("image_url")
											except json.JSONDecodeError:
												image_url = data.strip()

											async with session.get(image_url) as image_response:
												image_response.raise_for_status()
												image_content = io.BytesIO(await image_response.read())
										await message.delete()
										await self._client.send_file(message.chat_id, image_content, caption=(self.strings("quest_img").format(img_url=image_url, prmpt=prompt, mdl=model))
											)

								except aiohttp.ClientResponseError as e:
									await utils.answer(message, self.strings("server_err").format(error=str(e)))
								except Exception as e:
									await utils.answer(message, self.strings("server_err").format(error=str(e)))
							else:
								await utils.answer(message, self.strings("image_err").format(error=f"HTTP {response.status}"))
			except Exception as e:
				await utils.answer(message, self.strings("image_err").format(error=str(e)))
		else:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))

	@loader.command(en_doc="Ask gpt for something", ru_doc="Спросите gpt о чем-нибудь")
	async def dgptcmd(self, message: Message):
		"""Ask gpt for something"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await message.edit(self.strings("wait"))

		await self.generate_text(message, args)

	@loader.command(en_doc="Generate image", ru_doc="Сгенерировать изображение")
	async def dimg(self, message: Message):
		"""Generate image"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await message.edit(self.strings("wait"))

		await self.generate_image(message, args)

	@loader.command(en_doc="Display models list", ru_doc="Показать список моделей")
	async def dgmodels(self, message: Message):
		"""Display models list"""
		t_mdl = '\n'.join(self.text_models)
		i_mdl = '\n'.join(self.image_models)
		await utils.answer(message, self.strings("models_list").format(txt_models=t_mdl, img_models=i_mdl))

	@loader.command(en_doc="Check for updates", ru_doc="Проверить обновления")
	async def dgcheck(self, message: Message):
		module_name = self.strings("name")
		module = self.lookup(module_name)
		sys_module = inspect.getmodule(module)

		local_file = io.BytesIO(sys_module.__loader__.data)
		local_file.name = f"{module_name}.py"
		local_file.seek(0)
		local_first_line = local_file.readline().strip().decode("utf-8")

		correct_version = sys_module.__version__
		correct_version_str = ".".join(map(str, correct_version))

		async with aiohttp.ClientSession() as session:
			async with session.get(f"{self.repo}/{local_file.name}") as response:
				if response.status == 200:
					remote_content = await response.text()
					remote_lines = remote_content.splitlines()

					new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
				else:
					await utils.answer(message, self.strings("fetch_failed"))
					return

		if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
			await utils.answer(message, self.strings("actual_version").format(ver=correct_version_str))
		else:
			update_message = self.strings("old_version").format(ver=correct_version_str, new_ver=new_version)
			update_message += self.strings("update_command").format(prefix=self.prefix, upd_file=f"{self.repo}/{local_file.name}")
			await utils.answer(message, update_message)



