"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

from .. import loader, utils

@loader.tds
class Stats(loader.Module):
    """Показывает статистику твоего аккаунта"""

    strings = {
        "name": "Stats",

        "stats": """<b><emoji document_id=5431577498364158238>📊</emoji> Моя статистика

<emoji document_id=5884510167986343350>💬</emoji> Всего чатов: <code>{all_chats}</code>

<emoji document_id=5258011929993026890>👤</emoji> <code>{u_chat}</code> личных чатов
<emoji document_id=5258513401784573443>👥</emoji> <code>{c_chat}</code> групп
<emoji document_id=5852471614628696454>📢</emoji> <code>{ch_chat}</code> каналов
<emoji document_id=5258093637450866522>🤖</emoji> <code>{b_chat}</code> ботов</b>""",

        "loading_stats": "<b><emoji document_id=5309893756244206277>🫥</emoji> Загрузка статистики...</b>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def stats(self, message):
        """Получить статистику"""

        await utils.answer(message, self.strings['loading_stats'])
        users = 0
        bots = 0
        c_chat = 0
        ch_chat = 0
        all_chats = 0

        async for dialog in self._client.iter_dialogs():
            all_chats += 1
            if dialog.is_user and not dialog.entity.bot:
                u_chat += 1
            elif dialog.is_user and dialog.entity.bot:
                b_chat += 1
            elif dialog.is_group:
                c_chat += 1
            elif dialog.is_channel:
                if dialog.entity.megagroup or dialog.entity.gigagroup or dialog.entity.channel:
                    c_chat += 1
                elif not dialog.entity.megagroup and not dialog.entity.gigagroup:
                    ch_chat += 1
        await utils.answer(message, self.strings("stats", message))
