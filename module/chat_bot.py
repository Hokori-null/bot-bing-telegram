import EdgeGPT
from typing import Union
from module import auxiliary
import json
import uuid
import asyncio
import config

CHAT_BOT = {}
prompt = config.PROMPT
bingstyle = config.STYLE_ENUM
with open('./module/cookie.json', 'r') as file:
    BING_COOKIE = json.load(file)

def generateChatBot(name) -> Union[tuple, None]:
    global CHAT_BOT
    token = name
    chatBot = EdgeGPT.Chatbot(cookies=BING_COOKIE)
    CHAT_BOT[token] = {}
    CHAT_BOT[token]['chatBot'] = chatBot
    CHAT_BOT[token]['useTimeStamp'] = auxiliary.getTimeStamp()
    print(token)
    return token, chatBot

    
def getChatBot(token: str) -> Union[dict, None]:
    global CHAT_BOT
    if token in CHAT_BOT:
        CHAT_BOT[token]['useTimeStamp'] = auxiliary.getTimeStamp()
        return CHAT_BOT[token]['chatBot']
    return None

async def checkChatBot(loop=True) -> None:
    global CHAT_BOT
    while True:
        for token in CHAT_BOT.copy():
            chatBot = CHAT_BOT[token]
            if auxiliary.getTimeStamp() - chatBot['useTimeStamp'] > config.TOKEN_USE_MAX_TIME_INTERVAL * 60:
                print('超时一个对话，已清空')
                await chatBot['chatBot'].close()
                del CHAT_BOT[token]
                print(CHAT_BOT)
        if loop:
            await asyncio.sleep(60)
        else:
            break

async def xnChatBot(loop=True) -> None:
    global CHAT_BOT
    while True:
        for token in CHAT_BOT.copy():
            chatBot = CHAT_BOT[token]
            if token == config.MASTER_NAME:
                if auxiliary.getTimeStamp() - chatBot['useTimeStamp'] > 5 * 60:
                    with open('./prompt/master.txt', 'r') as f:
                        text = f.read()
                    await chatBot['chatBot'].ask(prompt=text, conversation_style=bingstyle,webpage_context=prompt)
                    print('主人洗脑一次')
            else:
                if auxiliary.getTimeStamp() - chatBot['useTimeStamp'] > 5 * 60:
                    with open('./prompt/user.txt', 'r') as f:
                        text = f.read()
                    await chatBot['chatBot'].ask(prompt=text, conversation_style=bingstyle,webpage_context=prompt)
                    print('普通洗脑一次')
        if loop:
            await asyncio.sleep(60)
        else:
            break
