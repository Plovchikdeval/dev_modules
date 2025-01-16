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
from telethon import functions
from .. import loader

@loader.tds
class PfpRepeaterMod(loader.Module):
    """Profile Photo Repeater Module"""
    strings = {"name": "PfpRepeater"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "DELAY", 900, validator=loader.validators.Integer(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.running = False
        self.task = None

    async def set_profile_photo(self, photo_path):
        while self.running:
            file = await self.client.upload_file(photo_path)
            await self.client(functions.photos.UploadProfilePhotoRequest(file=await self.client.upload_file(file)))
            await asyncio.sleep(self.config["DELAY"])

    @loader.command()
    async def pfp(self, message):
        """Start repeating profile photo"""
        reply = await message.get_reply_message()
        if reply and reply.photo:
            photo_path = await message.client.download_media(reply.photo)
        elif message.media and message.photo:
            photo_path = await message.client.download_media(message)
        else:
            await message.edit("Please provide the photo or reply to a photo.")
            return

        if not self.running:
            self.running = True
            self.task = asyncio.create_task(self.set_profile_photo(photo_path))
            await message.edit(f"Started repeating profile photo every {self.config['DELAY']} seconds.")
        else:
            await message.edit("Profile photo repeater is already running.")

    @loader.command()
    async def pfpstop(self, message):
        """Stop repeating profile photo"""
        if self.running:
            self.running = False
            self.task.cancel()
            await message.edit("Stopped repeating profile photo.")
        else:
            await message.edit("Profile photo repeater is not running.")