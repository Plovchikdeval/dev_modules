# ___________________________________________
#/  _        _                         _     \
#| | | _____| |__  _ __ ___   ___   __| |___ |
#| | |/ / __| '_ \| '_ ` _ \ / _ \ / _` / __||
#| |   <\__ \ | | | | | | | | (_) | (_| \__ \|
#| |_|\_\___/_| |_|_| |_| |_|\___/ \__,_|___/|
#\___________________________________________/  

# meta developer: @kshmods
# license: GNU General Public License v3.0


from hikkatl.types import Message
from hikkatl.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import time

@loader.tds
class KSHAFK(loader.Module):
    """Скромненький AFK Модуль."""
    strings = {"name": "KSHAFK"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enter_afk",
                "<emoji document_id=5325900626909994389>🌀</emoji> Я в AFK! Причина: {reason}",
                "Сообщение при включении",
            ),
            loader.ConfigValue(
                "unafk_text",
                "<emoji document_id=4999015678238262018>✨</emoji> Я вернулся! Отсутствовал: {duration}",
                "Сообщение при выключении",
            ),
            loader.ConfigValue(
                "response_text",
                "<emoji document_id=5791714113906282664>⚡️</emoji> Я в AFK! Причина: {reason} | Время: {duration}",
                "Ответ на сообщения",
            ),
            loader.ConfigValue(
                "name_prefix",
                "[AFK] ",
                "Префикс для имени",
            )
        )
        self.state = False
        self.reason = ""
        self.start = 0
        self.notified_chats = set()

    async def client_ready(self, client, db):
        self._client = client
        me = await client.get_me()
        self.original_name = me.first_name

    async def update_name(self, afk: bool):
        name = f"{self.config['name_prefix']}{self.original_name}" if afk else self.original_name
        await self._client(UpdateProfileRequest(first_name=name))

    async def afkcmd(self, message: Message):
        """Включить AFK"""
        self.reason = utils.get_args_raw(message) or "Не указана"
        self.state = True
        self.start = time.time()
        self.notified_chats = set()

        await self.update_name(True)
        await utils.answer(message, self.config["enter_afk"].format(reason=self.reason))

    async def unafkcmd(self, message: Message):
        """Выключить AFK"""
        if not self.state:
            return

        duration = self._format_time(time.time() - self.start)
        self.state = False

        await self.update_name(False)
        await utils.answer(message, self.config["unafk_text"].format(duration=duration))

    def _format_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    async def watcher(self, message: Message):
        if not self.state:
            return

        chat_id = utils.get_chat_id(message)
        if chat_id in self.notified_chats:
            return

        if getattr(message, "out", False):
            return

        me = await self._client.get_me()
        if getattr(message, "sender_id", None) == me.id:
            return

        duration = self._format_time(time.time() - self.start)
        response = self.config["response_text"].format(reason=self.reason, duration=duration)

        if message.is_private or (me.username and f"@{me.username}" in (message.text or "").lower()):
            await message.reply(response)
            self.notified_chats.add(chat_id)

    async def on_unload(self):
        if self.state:
            await self.update_name(False)

