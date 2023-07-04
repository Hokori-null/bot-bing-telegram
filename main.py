import asyncio
import re
import config
import os
import logging
from module import chat_bot

from telebot.async_telebot import AsyncTeleBot

from EdgeGPT import ConversationStyle

bingstyle = config.STYLE_ENUM
BOT_TOKEN = config.TELE_TOKEN
bot = AsyncTeleBot(BOT_TOKEN)
bot_username = 'holpls_bot'
prompt = config.PROMPT



async def bingChat(prompt_text,name, is_ref=False):
    token = name
    chatBot = chat_bot.getChatBot(token)
    if not chatBot:
        print('token不存在')
        token, chatBot = chat_bot.generateChatBot(token)
        asyncio.get_event_loop().create_task(chat_bot.checkChatBot())
        mastername = config.MASTER_NAME
        if token == mastername:
            print('主人模式')
            with open('./prompt/master.txt', 'r') as f:
                text = f.read()
            response_dict = await chatBot.ask(prompt=text, conversation_style=bingstyle,webpage_context=prompt)    
            response_dict = await chatBot.ask(prompt=prompt_text, conversation_style=bingstyle)

        else:
            print('普通模式')
            with open('./prompt/user.txt', 'r') as f:
                text = f.read()
            response_dict = await chatBot.ask(prompt=prompt_text, conversation_style=bingstyle,webpage_context=prompt)
            response_dict = await chatBot.ask(prompt=prompt_text, conversation_style=bingstyle)
    else:
        #asyncio.get_event_loop().create_task(chat_bot.xnChatBot())
        response_dict = await chatBot.ask(prompt=prompt_text, conversation_style=bingstyle)
    if is_ref:
        return response_dict['item']['messages'][1]["adaptiveCards"][0]["body"][0]["text"]
    return re.sub(r'\[\^\d\^\]', '', response_dict['item']['messages'][1]['text'])

async def xn(message,is_ref=False):
    try:
        prompt = message
        bot_re = await bingChat(prompt,is_ref)
        print(f"Response received - {bot_re}")
    except Exception as e:
        print("Exception happened xn")
        print(e)

@bot.message_handler(func=lambda message: message.chat.type == 'private')
async def ask(message, is_ref=False):
    try:
        username = message.from_user.username
        # if username not in authorized_id:
        #     await bot.reply_to(message, "Not authorized to use this bot")
        #     return
        namez = username
        prompt_text = message.text
        log_dir = "./log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"{username}.log")
        logging.basicConfig(filename=log_file, level=logging.INFO) 
        logging.info(f"Request received from {username} - {prompt_text}")
        print(f"Request received from {username} - {prompt_text}")
        if not prompt_text:
            await bot.reply_to(message, "Empty query sent. Add your query /ask <message>")
        else:
            bot_response = await bingChat(prompt_text,namez, is_ref)
            print(f"Response received - {bot_response}")
            qre = bot_response.replace('?\n\n', '')
            await bot.reply_to(message, bot_response.replace('?\n\n', ''))
            logging.info(qre)
    except Exception as e:
        print("Exception happened qa")
        print(e)

@bot.message_handler(func=lambda message: message.chat.type == 'group')
async def ask(message, is_ref=False):
    try:

        if message.text.startswith('/bot'):
            username = message.from_user.username
        # if username not in authorized_id:
        #     await bot.reply_to(message, "Not authorized to use this bot")
        #     return
            namez = username
            prompt_text = message.text.replace("/bot", "")
            print(f"Request received from {username} - {prompt_text}")
            if not prompt_text:
                await bot.reply_to(message, "Empty query sent. Add your query /ask <message>")
            else:
                bot_response = await bingChat(prompt_text,namez, is_ref)
                print(f"Response received - {bot_response}")
                await bot.reply_to(message, bot_response.replace('?\n\n', ''))
        elif message.text.startswith('/style'):
            bstyle = bingstyle
            styletxt = message.text.replace("/style", "")
            if styletxt == "创造":
                await bot.reply_to(message, "切换至创造")
                bstyle = 'creative'
            elif styletxt == "均衡":
                bstyle = 'balanced'
                await bot.reply_to(message, "切换至均衡")
            elif styletxt == "精准":
                bstyle = 'precise'
                await bot.reply_to(message, "切换至精准")
            else:
                await bot.reply_to(message, "请设置bing模式 /style 均衡,创造,精准")
        elif message.text.startswith('/start'):
            username = message.from_user.username
            result = f"""
            Welcome {username}!!
            """
            await bot.send_message(message.chat.id, result)
        elif message.text.startswith('/help'):
            await bot.reply_to(message, '/bot <内容> 进行对话\n/style 请设置bing模式')
        else:
            await bot.reply_to(message, '请使用/help查看指令.')
    except Exception as e:
        print("Exception happened qa")
        print(e)


async def main():
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(main())