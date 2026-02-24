from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from helpers import load_from_update
from sqlalchemy import text
from database import session
# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    data = load_from_update(update)
    await update.message.reply_html(
        rf"Hi {data['user']['first_name']}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = """
Menu Bantuan.

Command:

/start - Memulai Penggunaan BOT.
/help_ajcc - Menu Bantuan.
/stats - Statistik Chat Saat Ini.

Command Lain:
/info_sms_spam - Informasi spam checker
/recommend_me_film_by_synopsis - rekomendasi film berdasarkan sinopsis
Ping:
@all - ping semua member.
@admin - ping semua admin.

by ajcc 2023.
    """
    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    data = load_from_update(update)
    sql = text("""
        SELECT
            m.user_id,
            m.name,
            CONCAT('@', m.username) as username,
            (
                SELECT COUNT(*)
                FROM
                    message_logs ml
                WHERE
                    ml.member_id = m.user_id
            ) as stats
        FROM
            members m
        ORDER BY
            stats
        DESC
        LIMIT 10
    """)
    results = session.execute(sql)
    response = "Statistik Jumlah Chat:"
    for i, record in enumerate(results):
        response += f"\n{i+1}. {record[2]} -> {record[3]} chat"
    await update.message.reply_html(
        response,
        reply_markup=ForceReply(selective=True),
    )
