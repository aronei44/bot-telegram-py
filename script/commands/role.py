from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from helpers import load_from_update
from sqlalchemy import select, asc
from database import session
from models.roles import Roles
import psycopg2

async def setrole(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raw = update.message.text.lower()
        msg = raw.split(" ")
        if len(msg) < 4:
            await update.message.reply_html(
                "Mohon gunakan command ini dengan \n /role_set nama_role min_value max_value",
                reply_markup=ForceReply(selective=True),
            )
        else:
            msg = " ".join(msg[1:])
            for d in msg.split("|"):
                data = d.split(" ")
                min_val, max_val = int(data[1]), int(data[2])
                if min_val > max_val:
                    min_val, max_val = int(data[2]), int(data[1])
                data = Roles(data[0],min_val,max_val)
                session.add(data)
                session.commit()
            await update.message.reply_html(
                msg,
                reply_markup=ForceReply(selective=True),
            )
    except psycopg2.errors.UniqueViolation as e:
        session.rollback()
    except Exception as e:
        print("ERROR : ", str(e))
        await update.message.reply_html(
            "Error " + str(e),
            reply_markup=ForceReply(selective=True),
        )
        session.rollback()

async def getrole(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stmt = select(Roles).order_by(asc('min_val'))
    txt = ""
    for role in session.scalars(stmt):
        txt += f"{role.role_name} [{role.min_val} -> {role.max_val}]\n"
    await update.message.reply_html(
        txt,
        reply_markup=ForceReply(selective=True),
    )