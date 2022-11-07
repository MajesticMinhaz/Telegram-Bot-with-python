from supplier import config
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram_commands import *


application = Application.builder().token(config.get("BOT_TOKEN")).build()

application.add_handler(CommandHandler("start", start_callback))
application.add_handler(CommandHandler("upload_sessions", upload_session_callback))
application.add_handler(zip_file_handler)

application.run_polling()
