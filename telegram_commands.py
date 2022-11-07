import asyncio
import os
import sqlite3
from sqlite3 import connect
from datetime import datetime
from telegram import Update
from os.path import join
from zipfile import ZipFile
from make_client import get_valid_clients
from make_client import get_group_info
from make_client import send_message_to_members
from session_temp import SessionValues
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import FORWARDED
from telegram.ext.filters import Document


async def start_callback(update: Update, context: CallbackContext) -> None:
    """
    This Function is created for handle /start command on Telegram Bot
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: It will send a message for /start command. It should be static.
    """
    await update.message.reply_text(
        text=f"<code>Hello {update.effective_chat.first_name}!\n\nWelcome to the Bot.</code>",
        parse_mode=ParseMode.HTML
    )


async def upload_session_callback(update: Update, context: CallbackContext) -> None:
    """
    This Function is created for /upload_session command handler
    :param update: This update parameter will automatically fill up by python-telegram-bot package. It will update for
                   every single message,
    :param context: This is the blueprint of every callback. it also will be fill up automatically, we don't need to
                    think about that, It will return an instance of entire Bot.
    :return: Static Message
    """
    await update.message.reply_text(
        text="<code>Please upload your session files as zip format.\n\nFile size should be less then 20 MB</code>",
        parse_mode=ParseMode.HTML
    )


async def handle_zip_file(update: Update, context: CallbackContext) -> None:
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
    Download File Path setup. You have to a folder called as uploads in the base directory. The file will download there
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
    send notification message to user
    """
    await update.effective_message.reply_text(
        text="<code>your zip file was uploaded successfully.</code>",
        parse_mode=ParseMode.HTML
    )

    """
    Extracting the zip file
    """
    sessions_file_path, total_files = await make_it_unzip(file_path=download_path)

    """
    send notification message to user
    """
    await update.effective_message.reply_text(
        text=f"<code>{total_files} session files found in the ZIP file.</code>",
        parse_mode=ParseMode.HTML
    )

    """
    send notification to user that current checking the valid sessions.
    """
    checking_valid_files = await update.effective_message.reply_text(
        text="<code>Checking valid sessions...</code>",
        parse_mode=ParseMode.HTML
    )

    """
    generating session string for all session files
    """
    session = [generating_session_string(sessions_path=file_path) for file_path in sessions_file_path]

    """
    Getting valid client and join to the targeted group
    """
    valid_client = await asyncio.create_task(get_valid_clients(sessions=session))

    """
    Deleting notify message "checking valid sessions..."
    """
    await context.bot.delete_message(
        chat_id=checking_valid_files.chat_id,
        message_id=checking_valid_files.message_id
    )

    await update.effective_message.reply_text(
        text=f"<code>{len(valid_client)} valid session found</code>",
        parse_mode=ParseMode.HTML
    )

    await update.effective_message.reply_text(
        text=f"<code>{total_files - len(valid_client)} invalid session found</code>",
        parse_mode=ParseMode.HTML
    )

    group_info = await get_group_info(clients=valid_client)
    sending = await update.effective_message.reply_text(
        text=f"<code>Sending message to the users</code>",
        parse_mode=ParseMode.HTML
    )
    await send_message_to_members(
        clients=valid_client,
        members=group_info[0],
        client_id=group_info[1],
        group_id=group_info[2]
    )
    await context.bot.delete_message(
        chat_id=sending.chat_id,
        message_id=sending.message_id
    )
    await update.effective_message.reply_text(
        text=f"<code>Message sent to the all users.</code>",
        parse_mode=ParseMode.HTML
    )


async def make_it_unzip(file_path: str) -> tuple:
    """
    This function is created for unzip the zip file
    :param file_path: it should be zip files path of server.
    :return: tuple of session file path and number of session file
    """
    with ZipFile(file=file_path, mode='r') as session_zip:
        """
        created a variable to store all .session file path
        """
        session_file_path = list()

        for file in session_zip.namelist():

            """
            Check if file contain .session prefix in the file name then pass otherwise fail
            """
            if file.__contains__(".session"):
                """
                It will extract to extract_session folder to the base directory. so you have to have a folder called as
                ./extract_session
                """
                extract_path = join(os.getcwd(), f'extract_session/')

                session_zip.extract(
                    member=file,
                    path=extract_path
                )

                """
                extracted file path
                """
                extracted_file_path = os.path.join(extract_path, file)

                """
                appending to session_file_path list
                """
                session_file_path.append(extracted_file_path)
            else:
                continue

    return session_file_path, len(session_file_path)


def generating_session_string(sessions_path: str) -> dict:
    """
    This function is created for generating session string for telethon pacakge
    :param sessions_path: session file path
    :return: session string if all the values is perfect otherwise skip and delete the file
    """

    """
    connect with sqlite3 database of session file
    """
    get_connection = connect(sessions_path.strip())
    get_cursor = get_connection.cursor()

    """
    for set session file data creating a dictionary
    """
    session_data = dict()

    try:
        session_data['file_path'] = sessions_path.strip()
        session_data['dc_id'] = get_cursor.execute("SELECT dc_id FROM sessions").fetchone()[0]
        session_data['server_address'] = get_cursor.execute("SELECT server_address FROM sessions").fetchone()[0]
        session_data['port'] = get_cursor.execute("SELECT port FROM sessions").fetchone()[0]
        session_data['auth_key'] = get_cursor.execute("SELECT auth_key FROM sessions").fetchone()[0]
    except sqlite3.OptimizedUnicode as exception:
        session_data['auth_key'] = b""
        print(exception)
    finally:
        if session_data['auth_key'] != b"":
            session_value = SessionValues(
                dc_id=session_data.get('dc_id'),
                server_address=session_data.get('server_address'),
                auth_key=session_data.get('auth_key'),
                port=session_data.get('port')
            )

            session = session_value.generate_telethon_session_string()
            session_data['session'] = session

            return session_data
        else:
            print(session_data)
            try:
                os.remove(sessions_path)
            except FileNotFoundError:
                pass
            return session_data


"""
zip_file_handler variable can check which types of file is sent from users. if it is .zip file then it will response
otherwise, it will do nothing. if users send from other places then also it will do nothing. users have upload valid zip
file.
"""
zip_file_handler = MessageHandler(
    filters=(~FORWARDED) & Document.ZIP,
    callback=handle_zip_file
)
