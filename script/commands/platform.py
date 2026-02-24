from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from helpers import load_from_update
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

FE_URL = os.getenv('FE_AUTH_URL')
CORE_URL = os.getenv('API_URL')

async def getToken(telegramUserId : str, telegramUserName : str):
    resp = requests.post(CORE_URL+"token", {"telegramUserId":telegramUserId, "telegramUserName":telegramUserName})
    data = json.loads(resp.text)
    return {
        "data": data,
        "status": resp.status_code
    }

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    data = load_from_update(update)
    user = data['user']
    dataLog = await getToken(user['id'], user['username'])
    if dataLog['status'] != 201:
        await update.message.reply_html(
            "error occured or telegram user id has been registered",
            reply_markup=ForceReply(selective=True),
        )
    else:
        text = f"""
    {dataLog['data']['message']}
    {FE_URL}{dataLog['data']['data']['register_token']}
        """
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=text,
            parse_mode='HTML')
