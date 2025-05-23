# ___________________________________________
#/  _        _                         _     \
#| | | _____| |__  _ __ ___   ___   __| |___ |
#| | |/ / __| '_ \| '_ ` _ \ / _ \ / _` / __||
#| |   <\__ \ | | | | | | | | (_) | (_| \__ \|
#| |_|\_\___/_| |_|_| |_| |_|\___/ \__,_|___/|
#\___________________________________________/  


# meta developer: @kshmods
# license: GNU General Public License v3.0



import random
import string
from .. import loader, utils

@loader.tds
class KshPassGen(loader.Module):
    """Генератор паролей"""
    strings = {"name": "KSHPassGen"}

    async def passgencmd(self, message):
        """<длина> - сгенерировать пароль"""
        length = int(utils.get_args_raw(message)) if utils.get_args_raw(message) else 12
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        await utils.answer(message, f"<emoji document_id=6005570495603282482>🔑</emoji> Пароль:\n`{password}`")
