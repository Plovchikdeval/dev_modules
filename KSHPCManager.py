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
from .. import loader, utils
import subprocess
import os
import platform
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@loader.tds
class KSHPCManager(loader.Module):
    """Удаленное управление ПК через Telegram"""
    strings = {
        "name": "KSHPCManager",
        "help": "<emoji document_id=5825579866610732647>🖥</emoji> <b>Доступные команды:</b>\n\n"
                "• <code>.shutdown</code> - Выключает ПК. (не желательно использовать на хосте)\n"
                "• <code>.pcrestart</code> - Перезагружает ПК. (не желательно использовать на хосте)                                                                                                                                                                                                                                                       \n"
                "• <code>.cmd [command]</code> - Выполнить команду в терминале.\n"
                "• <code>.files [path]</code> - Показывает список файлов в указанной директории.\n"
                "• <code>.send [path]</code> - Отправляет файл с хоста.\n"
                "• <code>.pchelp</code> - Показать это меню.",
        "shutdown": "<emoji document_id=5825579866610732647>🖥</emoji> Компьютер выключится прямо сейчас",
        "restart": "<emoji document_id=5845943483382110702>🔄</emoji> Компьютер перезагрузится прямо сейчас",
        "cmd_result": "<emoji document_id=5960551395730919906>📝</emoji> <b>Результат команды:</b>\n<code>{}</code>",
        "files_list": "<emoji document_id=6039630677182254664>📂</emoji> <b>Содержимое {}:</b>\n\n<code>{}</code>",
        "file_sent": "<emoji document_id=6039630677182254664>📂</emoji> Файл успешно отправлен",
        "file_not_found": "<emoji document_id=5778527486270770928>❌</emoji> Файл не найден",
        "error": "<emoji document_id=5778527486270770928>❌</emoji> Ошибка: {}"
    }

    def __init__(self):
        self.os_type = platform.system()
        self.screenshot_path = "telegram_screenshot.png"

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def pchelpcmd(self, message: Message):
        """Открывает список команд модуля."""
        await utils.answer(message, self.strings["help"])

    async def shutdowncmd(self, message: Message):
        """Выключает ПК. ( не желательно использовать на хосте)"""
        try:
            os.system("shutdown")
            await utils.answer(message, self.strings["shutdown"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def pcrestartcmd(self, message: Message):
        """Перезагружает ПК. (не желательно использовать на хосте)                                                                                                                                                                                                                                                                                      """
        try:
            os.system("reboot")
            await utils.answer(message, self.strings["restart"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def cmdcmd(self, message: Message):
        """Выполнить команду в терминале"""
        command = utils.get_args_raw(message)
        if not command:
            await utils.answer(message, "❌ Укажите команду для выполнения")
            return

        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                timeout=60
            )
            await utils.answer(
                message,
                self.strings["cmd_result"].format(result[:4000])
            )
        except subprocess.CalledProcessError as e:
            await utils.answer(
                message,
                self.strings["error"].format(e.output[:4000])
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def filescmd(self, message: Message):
        """Показывает список файлов в указанной директории."""
        path = utils.get_args_raw(message) or "."
        try:
            files = "\n".join(os.listdir(path))
            await utils.answer(
                message,
                self.strings["files_list"].format(path, files[:4000])
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def sendcmd(self, message: Message):
        """Отправляет файл с хоста."""
        file_path = utils.get_args_raw(message)
        if not file_path:
            await utils.answer(message, "❌ Укажите путь к файлу")
            return

        try:
            if os.path.exists(file_path):
                await self._client.send_file(
                    message.peer_id,
                    file_path,
                    caption=f"<emoji document_id=6039630677182254664>📂</emoji> Файл: {os.path.basename(file_path)}"
                )
                await utils.answer(message, self.strings["file_sent"])
            else:
                await utils.answer(message, self.strings["file_not_found"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
