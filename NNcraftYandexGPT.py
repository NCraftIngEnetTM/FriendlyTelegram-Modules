from telethon import types
from .. import loader, utils

import requests

@loader.tds
class NNcraftYandexGPTMod(loader.Module):
    strings = {"name": "NNcraftYandexGPT",}

    async def yagptcmd(self, message):
        id = utils.get_chat_id(message) 
        msgid = message.reply_to
        prompt = utils.get_args_raw(message)
        assistant = None
        if msgid:
            msgid = msgid.reply_to_msg_id
            assistant = (await self.client.get_messages(id, ids=msgid)).text

        await message.edit(f"<b>YandexGPT (Pro) промпт</b>:\n{prompt}")

        wait = await message.reply("<b>Ваш промпт обрабатывается...</b>")
        response = self.yagpt(prompt, assistant)

        splited = self.split_msg(f"**YandexGPT (Pro)**:\n{response}")

        for i in range(len(splited)):
            if i == 0:
                await wait.edit(splited[i], parse_mode="markdown")
            else:
                await message.reply(splited[i], parse_mode="markdown")

    async def yagptlitecmd(self, message):
        id = utils.get_chat_id(message) 
        msgid = message.reply_to
        prompt = utils.get_args_raw(message)
        assistant = None
        if msgid:
            msgid = msgid.reply_to_msg_id
            assistant = (await self.client.get_messages(id, ids=msgid)).text
            
        await message.edit(f"<b>YandexGPT (Lite) промпт</b>:\n{prompt}")

        wait = await message.reply("<b>Ваш промпт обрабатывается...</b>")
        response = self.yagpt(prompt, assistant, model="yandexgpt-lite")

        splited = self.split_msg(f"**YandexGPT (Lite)**:\n{response}")

        for i in range(len(splited)):
            if i == 0:
                await wait.edit(splited[i], parse_mode="markdown")
            else:
                await message.reply(splited[i], parse_mode="markdown")

    async def yagptsumcmd(self, message):
        id = utils.get_chat_id(message) 
        msgid = message.reply_to
        prompt = utils.get_args_raw(message)
        assistant = None
        if msgid:
            msgid = msgid.reply_to_msg_id
            assistant = (await self.client.get_messages(id, ids=msgid)).text
            
        await message.edit(f"<b>YandexGPT (Краткий пересказ) промпт</b>:\n{prompt}")

        wait = await message.reply("<b>Ваш промпт обрабатывается...</b>")
        response = self.yagpt(prompt, assistant, model="summarization")

        splited = self.split_msg(f"**YandexGPT (Краткий пересказ)**:\n{response}")

        for i in range(len(splited)):
            if i == 0:
                await wait.edit(splited[i], parse_mode="markdown")
            else:
                await message.reply(splited[i], parse_mode="markdown")

    async def client_ready(self, client, db):
        self._db = db
        self.client = client



    def yagpt(self, user: str, assistant: str = None, system: str = None, model: str = "yandexgpt", tokens: int = 2000, temperature: float = 0.3):
        messages = []
        if system:
            messages.append({"role": "system","text": system})
        if assistant:
            messages.append({"role": "assistant","text":assistant})
        messages.append({"role": "user","text": user})

        id = ""
        api = ""
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
            "Authorization": f"Api-Key {api}"
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
