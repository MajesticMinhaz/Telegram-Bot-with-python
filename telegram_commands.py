from telegram import Update
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
    await update.message.reply_text(f"Hello {update['message']['chat']['first_name']}!\n\n"
                                    f"Welcome to the Bot.")


