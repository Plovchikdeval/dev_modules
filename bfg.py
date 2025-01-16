"""
██████╗ ███████╗██╗   ██╗     ██╗███╗   ███╗ ██████╗ ██████╗ ███████╗
██╔══██╗██╔════╝██║   ██║     ██║████╗ ████║██╔═══██╗██╔══██╗██╔════╝
██║  ██║█████╗  ██║   ██║     ██║██╔████╔██║██║   ██║██║  ██║███████╗
██║  ██║██╔══╝  ╚██╗ ██╔╝██   ██║██║╚██╔╝██║██║   ██║██║  ██║╚════██║
██████╔╝███████╗ ╚████╔╝ ╚█████╔╝██║ ╚═╝ ██║╚██████╔╝██████╔╝███████║
╚═════╝ ╚══════╝  ╚═══╝   ╚════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                                     
(C) 2024 t.me/devjmodules
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @devjmodules

import asyncio
import time
from telethon import functions
from .. import loader

class Farm:
    async def automining(self):
        async with self._client.conversation(self._bot) as conv:
            check_mine = "моя шахта"
            await conv.send_message(check_mine)
            r = await conv.get_response()
            mine_info = r.text

            which_ore = mine_info.split("\n")[3].split(": ")[1].split()[0].lower()
            energy_count = int(mine_info.split("\n")[2].split(": ")[1])

            ores = [
                ('золото', 'золото'),
                ('алмаз', 'алмазы'),
                ('аметист', 'аметисты'),
                ('аквамарин', 'аквамарин'),
                ('изумруд', 'изумруды'),
                ('материя', 'материю'),
                ('плазма', 'плазму'),
                ('никель', 'никель'),
                ('титан', 'титан'),
                ('эктоплазма', 'эктоплазму'),
            ]
            mine_ore = ""

            for ore, mine in ores:
                if ore == which_ore:
                    mine_ore += mine
                    break

            for _ in range(energy_count):
                await conv.send_message("копать {mine_ore}".format(mine_ore=mine_ore))
                await asyncio.sleep(1)

    async def everyday_bonus(self):
        async with self._client.conversation(self._bot) as conv:
            commands = [
                'испытать удачу',
                'ежедневный бонус',
            ]
            for command in commands:
                await conv.send_message(command)
                await asyncio.sleep(2)

    async def autofarm(self):
        async with self._client.conversation(self._bot) as conv:
            commands = [
                ('моя ферма', [0, 1]),
                ('мой бизнес', [0, 1]),
                ('мой сад', [0, 1, 3]),
                ('мое дерево', [0, 1]),
                ('мой генератор', [0, 1]),
                ('мой карьер', [0, 1]),
            ]
            for command, clicks in commands:
                await conv.send_message(command)
                r = await conv.get_response()

                for click in clicks:
                    await asyncio.sleep(3)
                    await r.click(click)

class BfgMod(loader.Module, Farm):
    """
    Автоматическая фарма в боте BFG.
    """

    strings = {"name": "BFG"}

    _bot = "@bforgame_bot"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "AutoFarm",
                True,
                "Автоматически собирать и оплачивать налоги.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "AutoMining",
                True,
                "Автоматически копать.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "EveryDayBonus",
                True,
                "Автоматически собирать бонус.",
                validator=loader.validators.Boolean(),
            )
        )

    @loader.loop(interval=1, autostart=True)
    async def main_loop(self):
        if self.config["AutoFarm"] and (not self.get("Tree_time") or (time.time() - self.get("Tree_time")) >= 3600):
            await self.autofarm()
            self.set("Tree_time", int(time.time()))

        if self.config["AutoMining"] and (not self.get("Mining_time") or (time.time() - self.get("Mining_time")) >= 3600*2+10):
            await self.automining()
            self.set("Mining_time", int(time.time()))

        if self.config["EveryDayBonus"] and (not self.get("Bonus_time") or (time.time() - self.get("Bonus_time")) >= 3600*24+10):
            await self.everyday_bonus()
            self.set("Bonus_time", int(time.time()))

        await self._client(functions.messages.ReadMentionsRequest(self._bot))

    @loader.command()
    async def bfg(self, message):
        """Начать автоматическую фарму."""
        self.config["AutoFarm"] = True
        self.main_loop.start()
        await message.edit("Автоматическая фарма включена.")

    @loader.command()
    async def rstbfg(self, message):
        """Перезапустить автоматическую фарму."""
        self.config["AutoFarm"] = False
        self.main_loop.stop()
        await asyncio.sleep(1)
        await self.autofarm()
        self.set("Tree_time", time.time() + 3600)
        self.config["AutoFarm"] = True
        self.main_loop.start()
        await message.edit("Автоматическая фарма перезапущена.")
        
    @loader.command()
    async def bfgstop(self, message):
        """Остановить автоматическую фарму."""
        self.config["AutoFarm"] = False
        self.main_loop.stop()
        await message.edit("Автоматическая фарма остановлена.")