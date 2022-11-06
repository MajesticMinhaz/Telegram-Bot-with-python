import os
from datetime import datetime
from telegram import Update
from os.path import join
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import FORWARDED
from telegram.ext.filters import Document


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
        text=f"<code>Hello {update.effective_chat.first_name}!<br /><br />Welcome to the Bot.</code>",
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


async def send_message_callback(update: Update, context: CallbackContext):
    """
    This Function is created for /send_message command handler. It should be use like that /send_message group_username
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: Static Message
    """

    """
    Get Group Username from context argument
    """
    group_user_name = ' '.join(context.args)

    await update.message.reply_text(
        text=f"<code>fYou have selected {group_user_name}</code>",
        parse_mode=ParseMode.HTML
    )


async def handle_zip_file(update: Update, context: CallbackContext):
    """
    This function is created for handle .zip file
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: Download to the server.
    """

    """
    Send an notify message to user.
    """
    uploading = await update.effective_message.reply_text(
        text="<code>uploading your zip file...</code>",
        parse_mode=ParseMode.HTML
    )

    """
    Select effective file and get the file_id
    """
    file_id = update.message.effective_attachment.file_id

    """
    Wait until bot get the file with the help of file_id
    """
    attachment = await context.bot.get_file(file_id=file_id)

    """
    Get current date-time so that new attachment can identify perfectly. Format = YYYY-MM-DD-HH-MM-SS-Micro
    """
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

    """
    Download File Path setup. You have to a folder called as uploads in the base directory. The file will download there.
    """
    download_path = join(os.getcwd(), f"uploads/session-{current_datetime}.zip")

    """
    Download the file
    """
    await attachment.download(custom_path=download_path)

    """
    Deleting notify message "uploading your zip file..."
    """
    await context.bot.delete_message(
        chat_id=uploading.chat_id,
        message_id=uploading.message_id
    )

    """
    send notify message to user
    """
    await update.effective_message.reply_text(
        text="<code>your zip file was uploaded successfully.</code>",
        parse_mode=ParseMode.HTML
    )

"""
zip_file_handler variable can check which types of file is sent from users. if it is .zip file then it will response
otherwise, it will do nothing. if users send from other places then also it will do nothing. users have upload valid zip
file.
"""
zip_file_handler = MessageHandler(
    filters=(~FORWARDED) & Document.ZIP,
    callback=handle_zip_file
)
