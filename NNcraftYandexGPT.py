from telethon import types
from .. import loader, utils

import requests

@loader.tds
class NNcraftYandexGPTMod(loader.Module):
    strings = {"name": "NNcraftYandexGPT",}

    async def yagptcmd(self, message):
        model = "yandexgpt"
        prompt = utils.get_args_raw(message)
        id = utils.get_chat_id(message)
        idmsg = (await message.edit(f"<b>YandexGPT (Pro) промпт</b>:\n{prompt}")).id

        wait = await self.client.send_message(id, "<b>Ваш промпт обрабатывается...</b>", reply_to=idmsg)
        response = self.yagpt(prompt, model=model)
        await wait.delete()
        splited = self.split_msg(f"<b>YandexGPT (Pro)</b>:\n{response}")

        for i in splited:
            await self.client.send_message(id, i, reply_to=idmsg)

    async def yagptlitecmd(self, message):
        model = "yandexgpt-lite"
        prompt = utils.get_args_raw(message)
        id = utils.get_chat_id(message)
        idmsg = (await message.edit(f"<b>YandexGPT (Lite) промпт</b>:\n{prompt}")).id

        wait = await self.client.send_message(id, "<b>Ваш промпт обрабатывается...</b>", reply_to=idmsg)
        response = self.yagpt(prompt, model=model)
        await wait.delete()
        splited = self.split_msg(f"<b>YandexGPT (Lite)</b>:\n{response}")

        for i in splited:
            await self.client.send_message(id, i, reply_to=idmsg)
    
    async def yagptsumcmd(self, message):
        model = "summarization"
        prompt = utils.get_args_raw(message)
        id = utils.get_chat_id(message)
        idmsg = (await message.edit(f"<b>YandexGPT (Краткий пересказ) промпт</b>:\n{prompt}")).id

        wait = await self.client.send_message(id, "<b>Ваш промпт обрабатывается...</b>", reply_to=idmsg)
        response = self.yagpt(prompt, model=model)
        await wait.delete()
        splited = self.split_msg(f"<b>YandexGPT (Краткий пересказ)</b>:\n{response}")

        for i in splited:
            await self.client.send_message(id, i, reply_to=idmsg)

    async def client_ready(self, client, db):
        self._db = db
        self.client = client
        self.me_id = (await client.get_me(True)).user_id


    def yagpt(self, user: str, system:str = None, model: str = "yandexgpt", tokens: int = 2000, temperature: float = 0.3):
        if not system:
            messages = [{"role": "user","text": user}]
        else:
            messages = [{"role": "system","text": system},{"role": "user","text": user}]

        id = ""
        apikey = ""
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        prompt = {
            "modelUri": f"gpt://{id}/{model}/latest",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": tokens
            },
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {apikey}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        status = response.status_code
        if status == 200:
            return response.json()['result']['alternatives'][0]['message']['text']
        else:
            return response.text

    def split_msg(self, msg: str):
        n = 4096
        return [msg[i:i+n] for i in range(0, len(msg), n)]
