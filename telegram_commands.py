from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext


async def start_callback(update: Update, context: CallbackContext):
    """
    This Function is created for handle /start command on Telegram Bot
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: It will send a message for /start command. It should be static.
    """
    await update.message.reply_text(
        text=f"<code>Hello {update['message']['chat']['first_name']}!<br /><br />Welcome to the Bot.</code>",
        parse_mode=ParseMode.HTML
    )


async def upload_session_callback(update: Update, context: CallbackContext):
    """
    This Function is created for /upload_session command handler
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: Static Message
    """
    await update.message.reply_text(
        text="<code>Please upload your session files as zip format.<br/>File size should be less then 20 MB</code>",
        parse_mode=ParseMode.HTML
    )
