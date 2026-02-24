from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import __version__ as TG_VER
import os
from dotenv import load_dotenv
from database import Base, engine
from script.commands.ping import *
from script.commands.basic import *
from script.commands.platform import *
from script.commands.scrapper import *
from script.commands.role import *
from script.commands.sms_classifier import info_lr_sms, download_nltk
import nltk
import easyocr
load_dotenv()
Token = os.getenv('API_KEY')
Base.metadata.create_all(engine)

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help_ajcc", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("role_set", setrole))
    application.add_handler(CommandHandler("role_get", getrole))
    # application.add_handler(CommandHandler("scrap_members", scrap_user))
    # application.add_handler(CommandHandler("scrap_chats", scrap_chat))
    # only can run in local computer
    application.add_handler(CommandHandler("info_sms_spam", info_lr_sms))
    application.add_handler(CommandHandler("nltk_download", download_nltk))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, document))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

nltk.download('stopwords')
nltk.download('punkt')
reader_ocr = easyocr.Reader(['en'])
if __name__ == "__main__":
    main()