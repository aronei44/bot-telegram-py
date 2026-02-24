from telegram import ForceReply, Update, ChatMemberAdministrator
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from sqlalchemy import text
from database import session
from script.response import response
from helpers import load_from_update, logger
from script.commands.sms_classifier import spam_check
from main import reader_ocr
import cv2
import numpy as np

async def document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    caption = update.message.caption
    if caption and "ocr" in caption.lower():
        await update.message.reply_text("Processing... OCR")
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        image = cv2.imdecode(
            np.asarray(bytearray(await file.download_as_bytearray()), dtype=np.uint8),
            cv2.IMREAD_COLOR,
        )
        result = reader_ocr.readtext(image)
        text = ""
        await update.message.reply_text("Result OCR")
        for res in result:
            text += f"{res[1]} \n"
        await update.message.reply_text(text)
        await update.message.reply_text("Done")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    res = response(load_from_update(update))
    logger.info(msg=res)
    # try:
    #     await context.bot.promoteChatMember(
    #         update.message.chat_id,
    #         update.message.from_user.id,
    #         can_change_info=True,
    #         can_delete_messages=True,
    #         can_edit_messages=False,
    #         can_manage_chat=True,
    #         can_invite_users=True,
    #         can_manage_topics=True,
    #         can_pin_messages=True,
    #         can_manage_video_chats=True,
    #         can_post_messages=False,
    #         can_promote_members=True,
    #         can_restrict_members=True,
    #         is_anonymous=False
    #     )
    #     await context.bot.setChatAdministratorCustomTitle(chat_id=update.message.chat_id, user_id=update.message.from_user.id, custom_title="si ujang")
    # except BadRequest as e:
    #     print(e)
    # except Exception as e:
    #     print(e)
    # ChatMemberAdministrator(update.message.from_user.id,False,False,False,False,False,False,False,False,False,True,True,True,False,"si Usman")
    # await update.message.reply_text(res)
    state = update.message.text.lower()
    if state == "@semua":
        await all_users(update, context)
    elif state == "@admin":
        await all_admin(update, context)
    await spam_check(update, context)

async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sql = text("""
        SELECT
            CONCAT('@', m.username) as username
        FROM
            members m
    """)
    results = session.execute(sql)
    datas = [res[0] for res in results]
    n = 50
    final_data = [datas[i * n:(i + 1) * n] for i in range((len(datas) + n - 1) // n )]
    for result in final_data:
        users = ""
        for res in result:
            users += f" {res}"
        must_delete = await update.message.reply_html(
            text=users,
            reply_markup=ForceReply(selective=True),
        )
        await context.bot.deleteMessage(
            message_id = must_delete.message_id,
            chat_id = update.message.chat_id
        )
    await update.message.reply_html(
        "Pinging all active users",
        reply_markup=ForceReply(selective=True),
    )

async def all_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = await context.bot.get_chat_administrators(update.message.chat_id)
    
    users = ""
    for d in data:
        users += f" @{d.user.username}"
    must_delete = await update.message.reply_html(
        text=users,
        reply_markup=ForceReply(selective=True),
    )
    await context.bot.deleteMessage(
        message_id = must_delete.message_id,
        chat_id = update.message.chat_id
    )
    await update.message.reply_html(
        "Pinging all administrators",
        reply_markup=ForceReply(selective=True),
    )
