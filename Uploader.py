__version__ = (0, 0, 7)

"""
  █ █▀█ █▄█ █ ▄█   █▀▄ █▀█ █▀▀
 ▄▀ █▄█ █ █ █▀ █   █▄▀ █▄█ ██▄
 (C) 2024 t.me/u1n1n1a1m1e1d
 Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @djmodules
# meta banner: https://kappa.lol/--YNb

import io
import os
import random
import json

from requests import post
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class KappaMod(loader.Module):
    """Загрузка на аналог 0x.at"""

    strings = {
        "name": "Uploader",
        "uploading": "<emoji document_id=5274168450204316527>🛸</emoji> <b>Uploading...</b>",
        "noargs": "<emoji document_id=5872829476143894491>🚫</emoji> <b>No file specified</b>",
        "err": "<emoji document_id=5872829476143894491>🚫</emoji> <b>Upload error</b>",
        "uploaded": "<emoji document_id=5123163417326126159>✅</emoji> <b>File uploaded!</b>",
        "link": "<emoji document_id=5877465816030515018>🔗</emoji> <b>Link:</b>",
    }
    strings_ru = {
        "uploading": "<emoji document_id=5274168450204316527>🛸</emoji> <b>Загрузка...</b>",
        "noargs": "<emoji document_id=5872829476143894491>🚫</emoji> <b>Файл не указан</b>",
        "err": "<emoji document_id=5872829476143894491>🚫</emoji> <b>Ошибка загрузки</b>",
        "uploaded": "<emoji document_id=5123163417326126159>✅</emoji> <b>Файл загружен!</b>",
        "link": "<emoji document_id=5877465816030515018>🔗</emoji> <b>Ссылка:</b>",
    }

    async def client_ready(self, client, db):
        self.client = client
        
    async def get_media(self, message: Message):
        reply = await message.get_reply_message()
        m = None
        if reply and reply.media:
            m = reply
        elif message.media:
            m = message
        elif not reply:
            await utils.answer(message, self.strings("noargs"))
            return False

        if not m:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "file.txt"
        else:
            file = io.BytesIO(await self._client.download_media(m, bytes))
            file.name = (
                m.file.name
                or (
                    "".join(
                        [
                            random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
                            for _ in range(16)
                        ]
                    )
                )
                + m.file.ext
            )

        return file

    @loader.sudo
    async def Loadcmd(self, message: Message):
        """upload file"""
        file = await self.get_media(message)
        if not file:
            return
        
        await message.edit(self.strings("uploading"))
        
        try:
            # Загружаем файл на сервер
            devup = post("http://ndpropave5.temp.swtest.ru", files={"file": file})
        except ConnectionError:
            await message.edit(self.strings("err"))
            return
        
        resp = devup.text
 
        await message.edit(f'{self.strings("link")} {resp}')
