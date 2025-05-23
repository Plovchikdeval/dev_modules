# ___________________________________________
#/  _        _                         _     \
#| | | _____| |__  _ __ ___   ___   __| |___ |
#| | |/ / __| '_ \| '_ ` _ \ / _ \ / _` / __||
#| |   <\__ \ | | | | | | | | (_) | (_| \__ \|
#| |_|\_\___/_| |_|_| |_| |_|\___/ \__,_|___/|
#\___________________________________________/                                       


# meta developer: @kshmods
# license: GNU General Public License v3.0


import subprocess
import re
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class FastFetch(loader.Module):
    """Вывод fastfetch"""

    strings = {
        "name": "FastFetch",
        "fetching": "<emoji document_id=5845943483382110702>🔄</emoji> Получаю информацию о системе..."
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command()
    async def ffetch(self, message: Message):
        """Показать системную информацию используя FastFetch"""
        await utils.answer(message, self.strings["fetching"])

        try:
            result = subprocess.run(
                ["fastfetch", "-L", "none"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            clean_result = re.sub(r'\x1B\[[0-9;]*[mGABCDHJKf]?', '', result)

            response = (
                "→ <b>fastfetch</b>\n\n"
                "<blockquote>\n"
                f"{clean_result.strip()}"
                "</blockquote>\n\n"
            )

            await utils.answer(message, response)
        except subprocess.CalledProcessError as e:
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> Ошибка: {e.stderr.strip()}")
        except FileNotFoundError:
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> fastfetch не установлен!\nУстановите: <code>sudo pacman -S fastfetch</code>(если это Arch Linux)\nИли соберите из исходников:\n<code>git clone https://github.com/fastfetch-cli/fastfetch.git && cd fastfetch && mkdir -p build && cd build && cmake .. && cmake --build . --target fastfetch</code>")

    @loader.command()
    async def fflarge(self, message: Message):
        """Подробно показывает сис.информацию используя FastFetch"""
        await utils.answer(message, self.strings["fetching"])

        try:
            result = subprocess.run(
                ["fastfetch"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            clean_result = re.sub(r'\x1B\[[0-9;]*[mGABCDHJKf]?', '', result)

            response = (
                "→ <b>fastfetch</b>\n\n"
                "<blockquote>\n"
                f"{clean_result.strip()}"
                "</blockquote>\n\n"
            )

            await utils.answer(message, response)
        except subprocess.CalledProcessError as e:
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> Ошибка: {e.stderr.strip()}")
        except FileNotFoundError:
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> fastfetch не установлен!\nУстановите: <code>sudo pacman -S fastfetch</code>(если это Arch Linux)\nИли соберите из исходников:\n<code>git clone https://github.com/fastfetch-cli/fastfetch.git && cd fastfetch && mkdir -p build && cd build && cmake .. && cmake --build . --target fastfetch</code>")
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> Неизвестная ошибка: {str(e)}")
          
