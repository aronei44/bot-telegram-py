from telethon.sync import TelegramClient
from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from script.response import saveuser
import os
from helpers import logger
from dotenv import load_dotenv
load_dotenv()

async def scrap_users(link) -> list:
   data = [] 
   async with TelegramClient(os.getenv('PHONE'), os.getenv('API_ID'), os.getenv('API_HASH')) as client:
      data = await client.get_participants(link)
   return [{"id": d.id, "first_name": d.first_name, "username": d.username} for d in data]


async def scrap_chats(link) -> int:
   data = 0
   async with TelegramClient(os.getenv('PHONE'), os.getenv('API_ID'), os.getenv('API_HASH')) as client:
      async for message in client.iter_messages(link):
         # print(message)
         try:
            logger(message.id, message.message, message.from_id.user_id, message.date)
            data +=1
         except:
            pass
   return data

async def scrap_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cmd = update.message.text.split(" ")
    if len(cmd) >= 2:
        data = await scrap_users(cmd[1])
        for d in data:
            saveuser(d)
        await update.message.reply_html(
            f"Total users scrapped : {len(data)}",
            reply_markup=ForceReply(selective=True),
        )
    else: 
        await update.message.reply_html(
            "Please insert telegram group url",
            reply_markup=ForceReply(selective=True),
        )

async def scrap_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cmd = update.message.text.split(" ")
    if len(cmd) >= 2:
        await update.message.reply_html(
            f"Scrapping Chats Started",
            reply_markup=ForceReply(selective=True),
        )
        data = await scrap_chats(cmd[1])
        await update.message.reply_html(
            f"Success Scrapping Chats count : {data}",
            reply_markup=ForceReply(selective=True),
        )
    else: 
        await update.message.reply_html(
            "Please insert telegram group url",
            reply_markup=ForceReply(selective=True),
        )