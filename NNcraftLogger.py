import asyncio
import logging
import json

from telethon import types
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class NNcraftLoggerMod(loader.Module):
    strings = {"name": "NNcraftLogger",
               "db_name": "NNcraft.Logger"}

    async def logcmd(self, message):
        await message.delete()
        args = list(utils.get_args_split_by(message, " "))
        id = utils.get_chat_id(message)

        if not args:
            args.append("default")
            args.append(False)
        if len(args) == 1:
            args.append(False)

        ids = self._db.get(self.strings["db_name"], "ids")
        forward = self._db.get(self.strings["db_name"], "forwards")
        if not ids.get(str(id)):
            if not forward.get(args[0]):
                return
            
            ids[str(id)] = {"forward": args[0], "me": args[1]}
            self._db.set(self.strings["db_name"], "ids", ids)

            entity = await self.client.get_entity(id)
            try:
                name = entity.first_name
            except:
                name = entity.title
            await self.client.send_message(int(forward[args[0]]["id"]), f"{name}:{id} добавлен в логгер!")
        
    async def unlogcmd(self, message):
        await message.delete()
        id = utils.get_chat_id(message)

        ids = self._db.get(self.strings["db_name"], "ids")
        try:
            forward = self._db.get(self.strings["db_name"], "forwards")[ids[str(id)]["forward"]]
        except KeyError:
            return
        
        del ids[str(id)]
        self._db.set(self.strings["db_name"], "ids", ids)


        entity = await self.client.get_entity(id)
        try:
            name = entity.first_name
        except:
            name = entity.title
        await self.client.send_message(int(forward["id"]), f"{name}:{id} удален из логгера!")

    async def addforwardcmd(self, message):
        args = list(utils.get_args_split_by(message, " "))
        forwards = self._db.get(self.strings["db_name"], "forwards")

        if len(args) == 2:
            if not forwards.get(args[0]):
                forwards[args[0]] = {"id": str(args[1])}
                await message.edit("Канал добавлен!")
                return
        await message.delete()

    async def delforwardcmd(self, message):
        args = list(utils.get_args_split_by(message, " "))
        forwards = self._db.get(self.strings["db_name"], "forwards")

        if len(args) == 1:
            if forwards.get(args[0]):
                del forwards[args[0]]
                await message.edit("Канал удален!")
                return
        await message.delete()

    async def listidscmd(self, message):
        ids = self._db.get(self.strings["db_name"], "ids")
        await message.edit(json.dumps(ids))

    async def listforwardscmd(self, message):
        forwards = self._db.get(self.strings["db_name"], "forwards")
        await message.edit(json.dumps(forwards))

    async def watcher(self, message):
        id = utils.get_chat_id(message)
        if not isinstance(message, types.Message):
            return
        try:
            settings = self._db.get(self.strings["db_name"], "ids")[str(id)]
            forward = self._db.get(self.strings["db_name"], "forwards")[settings["forward"]]
        except KeyError:
            return
        if not settings["me"]:
            return
        await message.forward_to(int(forward["id"]))

    async def client_ready(self, client, db):
        self._db = db
        self.client = client
        self.me_id = (await client.get_me(True)).user_id

        if not self._db.get(self.strings["db_name"], "ids"):
            self._db.set(self.strings["db_name"], "ids", {})
        if not self._db.get(self.strings["db_name"], "forwards"):
            self._db.set(self.strings["db_name"], "forwards", {})