import os
import asyncio
import time
from random import choice
from datetime import datetime
from supplier import config
from supplier import add_cursor
from supplier import add_connection
from telethon import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.sessions import StringSession
from sqlite_commands import is_exists_in_client_information
from sqlite_commands import is_exists_in_user_information
from sqlite_commands import insert_client
from sqlite_commands import insert_group
from sqlite_commands import insert_user
from sqlite_commands import get_client_id_from_client_information_table
from sqlite_commands import get_group_id_from_group_information_table


async def get_telethon_client(session: dict) -> tuple[TelegramClient | None, int | None, str | None]:
    """
    This function can accept only one parameter
    :param session: This argument should be a valid telethon session file
    :return: This function will return a TelegramClient instance or None
    """
    try:
        client = TelegramClient(
            StringSession(session.get("session")),
            api_id=19264279,
            api_hash="1811ec9eb63d3b5582a06e1d5e892ab6"
        )

        await asyncio.create_task(client.connect())
        is_client_authorized = await asyncio.create_task(client.is_user_authorized())

        if not is_client_authorized:
            print(f"unauthorized file: {session['file_path']}")
            try:
                os.remove(session['file_path'])
            except FileNotFoundError:
                pass
            return None, None, None
        else:
            client_info = await asyncio.create_task(client.get_me())  # client information

            client_information = dict()  # For store all information about this client.

            client_information['user_id'] = client_info.id
            client_information['is_self'] = client_info.is_self
            client_information['contract'] = client_info.contact
            client_information['mutual_contract'] = client_info.mutual_contact
            client_information['deleted'] = client_info.deleted
            client_information['bot'] = client_info.bot
            client_information['bot_chat_history'] = client_info.bot_chat_history
            client_information['bot_no_chats'] = client_info.bot_nochats
            client_information['verified'] = client_info.verified
            client_information['restricted'] = client_info.restricted
            client_information['min'] = client_info.min
            client_information['bot_inline_geo'] = client_info.bot_inline_geo
            client_information['support'] = client_info.support
            client_information['scam'] = client_info.scam
            client_information['apply_min_photo'] = client_info.apply_min_photo
            client_information['fake'] = client_info.fake
            client_information['bot_attach_menu'] = client_info.bot_attach_menu
            client_information['premium'] = client_info.premium
            client_information['attach_menu_enabled'] = client_info.attach_menu_enabled
            client_information['access_hash'] = client_info.access_hash
            client_information['first_name'] = client_info.first_name
            client_information['last_name'] = client_info.last_name
            client_information['username'] = client_info.username
            client_information['phone'] = client_info.phone

            client_information['dc_id'] = session.get("dc_id")
            client_information['server_address'] = session.get("server_address")
            client_information['port'] = session.get("port")
            client_information['auth_key'] = session.get("auth_key")
            client_information['telethon_session_string'] = session.get("session")

            """
            Check if Client is exists in Client_information table in Database than it should be skip otherwise 
            This client information should insert in Client_information table in Database.

            If client is exists with same values of User ID and Session String then it should be return number more than
                0 
            Otherwise it will return 0
            """
            number_of_clients = add_cursor.execute(
                is_exists_in_client_information,
                (client_information['user_id'], session['session'])
            ).fetchone()[0]

            if number_of_clients.__eq__(0):
                add_cursor.execute(
                    insert_client,
                    client_information
                )
                add_connection.commit()
            else:
                pass

            """
            Trying to join the client to the selected group
            """
            await client(JoinChannelRequest(channel=config.get("GROUP_NAME")))

            print(client, "was passed")
            return client, client_info.id, session['session']
    except AuthKeyDuplicatedError as duplicated_auth:
        print(duplicated_auth)
        print(session['file_path'], "was failed")
        os.remove(session['file_path'])
        return None, None, None


async def get_valid_clients(sessions: list) -> list:
    """
    :param sessions: sessions argument can contain lots of session file information and type is list,
    :return: It will return nothing. But this function is the entry point of this script.
    """

    """
    Make multiple client using session file and store them in clients list
    """
    clients = list()
    for session in sessions:
        telegram_client = await get_telethon_client(session=session)
        if telegram_client == (None, None, None):
            pass
        else:
            clients.append(telegram_client)

    return clients


async def get_group_info(clients: list) -> tuple:
    """
    this function is created to get selected group information
    :param clients: it can take all valid client sessions
    :return: members of selected group
    """
    if len(clients) == 0:
        return None, None, None

    """
    Get Current Datetime to this format -> YYYY-MM-DD HH:MM:SS:MMMM MM
    """
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    group_information = dict()  # For store all information about selected Group

    """
    Get selected group information
    """
    group_info = await clients[0][0].get_entity(config.get("GROUP_NAME"))

    """
    Get Client Id for FOREIGN KEY value of Group Information table.
    """
    client_id_from_client_information_table = add_cursor.execute(
        get_client_id_from_client_information_table,
        (clients[0][1], clients[0][2])
    ).fetchone()[0]

    group_information["group_id"] = group_info.id
    group_information["client_id"] = client_id_from_client_information_table
    group_information["title"] = group_info.title
    group_information["creation_datetime"] = group_info.date.strftime("%Y-%m-%d %H:%M:%S")
    group_information["creator"] = group_info.creator
    group_information["left"] = group_info.left
    group_information["broadcast"] = group_info.broadcast
    group_information["verified"] = group_info.verified
    group_information["mega_group"] = group_info.megagroup
    group_information["restricted"] = group_info.restricted
    group_information["signatures"] = group_info.signatures
    group_information["min"] = group_info.min
    group_information["scam"] = group_info.scam
    group_information["has_link"] = group_info.has_link
    group_information["has_geo"] = group_info.has_geo
    group_information["slow_mode_enabled"] = group_info.slowmode_enabled
    group_information["call_active"] = group_info.call_active
    group_information["call_not_empty"] = group_info.call_not_empty
    group_information["fake"] = group_info.fake
    group_information["giga_group"] = group_info.gigagroup
    group_information["no_forwards"] = group_info.noforwards
    group_information["join_to_send"] = group_info.join_to_send
    group_information["join_request"] = group_info.join_request
    group_information["access_hash"] = group_info.access_hash
    group_information["username"] = group_info.username
    group_information["inserted_at"] = current_datetime

    """
    Insert Group Information to Group_Information Table
    """
    add_cursor.execute(
        insert_group,
        group_information
    )
    add_connection.commit()

    """
    Get Group ID form Group Information Table
    """
    group_id_from_group_information_table = add_cursor.execute(
        get_group_id_from_group_information_table,
        (group_info.id, client_id_from_client_information_table, current_datetime)
    ).fetchone()[0]

    """
    Get Group Member's information
    """
    members = clients[0][0].iter_participants(entity=group_info, aggressive=True)

    return members, client_id_from_client_information_table, group_id_from_group_information_table


async def send_message_to_members(clients, members, client_id, group_id):
    """
    This function is created for send message to the users
    :param clients: all valid clients list
    :param members: all members list of the selected group
    :param client_id: client_id from database
    :param group_id: group_id from database
    :return: send message to the users
    """
    user_information = dict()  # For store all information about selected group of members

    """
    Get all member information using async for loop
    """
    async for member in members:
        """
        Check this user is already exists or not

        If This user is exists in User_Information Table then It will return number of user count
        otherwise it will return 0
        """
        number_of_user = add_cursor.execute(
            is_exists_in_user_information,
            (member.id, client_id, group_id)
        ).fetchone()[0]

        if number_of_user == 0:
            user_information["user_id"] = member.id
            user_information["is_self"] = member.is_self
            user_information["contract"] = member.contact
            user_information["mutual_contract"] = member.mutual_contact
            user_information["deleted"] = member.deleted
            user_information["bot"] = member.bot
            user_information["bot_chat_history"] = member.bot_chat_history
            user_information["bot_no_chats"] = member.bot_nochats
            user_information["verified"] = member.verified
            user_information["restricted"] = member.restricted
            user_information["min"] = member.min
            user_information["bot_inline_geo"] = member.bot_inline_geo
            user_information["support"] = member.support
            user_information["scam"] = member.scam
            user_information["apply_min_photo"] = member.apply_min_photo
            user_information["fake"] = member.fake
            user_information["bot_attach_menu"] = member.bot_attach_menu
            user_information["premium"] = member.premium
            user_information["attach_menu_enabled"] = member.attach_menu_enabled
            user_information["access_hash"] = member.access_hash
            user_information["first_name"] = member.first_name
            user_information["last_name"] = member.last_name
            user_information["user_name"] = member.username
            user_information["phone"] = member.phone
            user_information["group_id"] = group_id
            user_information["client_id"] = client_id

            """
            Insert User Information to User_Information Table
            """
            add_cursor.execute(
                insert_user,
                user_information
            )
            add_connection.commit()
        else:
            pass

        second_client = choice(clients)
        if member.username is not None:
            """
            Making receiver using user's username
            """
            receiver = await second_client[0].get_entity(entity=member.username)
        else:
            """
            Making receiver using user's user id
            """
            receiver = InputPeerUser(
                user_id=member.id,
                access_hash=member.access_hash
            )

        try:
            print("sending message to", member.first_name)
            await second_client[0].send_message(
                entity=receiver,
                message=f"Hello There, How are you doing today?"
            )
            time.sleep(2)
        except PeerFloodError:
            print("PeerFloodError")
        except Exception as e:
            print(e)
