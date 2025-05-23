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
import asyncio
import logging
import re

logger = logging.getLogger(__name__)

@loader.tds
class KSHSpeedTest(loader.Module):
    """Проверка скорости интернета"""
    strings = {
        "name": "KSHSpeedTest",
        "testing": "<emoji document_id=5845943483382110702>🔄</emoji> Запускаю тест скорости...",
        "result": "<emoji document_id=5936143551854285132>📊</emoji> <b>Результаты SpeedTest:</b>\n\n{result}",
        "error": "<emoji document_id=5778527486270770928>❌</emoji> Ошибка: {error}",
        "not_installed": "<emoji document_id=5778527486270770928>❌</emoji> speedtest-cli не установлен\n\nУстановите:\n<code>pip install speedtest-cli</code>"
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def speedtestcmd(self, message: Message):
        """Запустить тест скорости"""
        try:
            await utils.answer(message, self.strings["testing"])

            # Проверяем доступность speedtest-cli
            proc = await asyncio.create_subprocess_shell(
                "speedtest --version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()

            if proc.returncode != 0:
                await utils.answer(message, self.strings["not_installed"])
                return

            # Запускаем тест скорости
            proc = await asyncio.create_subprocess_shell(
                "speedtest --simple",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                error = stderr.decode().strip() or "Неизвестная ошибка"
                raise Exception(error)

            # Форматируем результат
            result = stdout.decode().strip()
            formatted = re.sub(
                r"(Ping|Download|Upload):\s+(.*)",
                lambda m: f"• <b>{m.group(1)}:</b> {m.group(2)}",
                result
            )

            await utils.answer(
                message,
                self.strings["result"].format(result=formatted)
            )

        except Exception as e:
            logger.exception("Speedtest failed")
            await utils.answer(
                message,
                self.strings["error"].format(error=str(e))
            )
