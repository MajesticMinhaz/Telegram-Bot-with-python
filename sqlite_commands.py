create_client_information_table = """
    CREATE TABLE IF NOT EXISTS Client_Information (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

        USER_ID INTEGER NOT NULL UNIQUE,
        IS_SELF BOOLEAN,
        CONTRACT BOOLEAN,
        MUTUAL_CONTRACT BOOLEAN,
        DELETED BOOLEAN,
        BOT BOOLEAN,
        BOT_CHAT_HISTORY BOOLEAN,
        BOT_NO_CHATS BOOLEAN,
        VERIFIED BOOLEAN,
        RESTRICTED BOOLEAN,
        MIN BOOLEAN,
        BOT_INLINE_GEO BOOLEAN,
        SUPPORT BOOLEAN,
        SCAM BOOLEAN,
        APPLY_MIN_PHOTO BOOLEAN,
        FAKE BOOLEAN,
        BOT_ATTACH_MENU BOOLEAN,
        PREMIUM BOOLEAN,
        ATTACH_MENU_ENABLED BOOLEAN,

        ACCESS_HASH BIGINT NOT NULL,
        FIRST_NAME VARCHAR(255),
        LAST_NAME VARCHAR(255),
        USERNAME VARCHAR(255),
        PHONE VARCHAR(100),

        DC_ID INTEGER,
        SERVER_ADDRESS VARCHAR(255),
        PORT INTEGER,
        AUTH_KEY BLOB,
        TELETHON_SESSION_STRING VARCHAR
    );
"""

create_group_information_table = """
    CREATE TABLE IF NOT EXISTS Group_Information (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

        GROUP_ID INTEGER,
        CLIENT_ID INTEGER,
        TITLE VARCHAR(255),
        CREATION_DATETIME VARCHAR(50),
        CREATOR BOOLEAN,
        LEFT BOOLEAN,
        BROADCAST BOOLEAN,
        VERIFIED BOOLEAN,
        MEGA_GROUP BOOLEAN,
        RESTRICTED BOOLEAN,
        SIGNATURES BOOLEAN,
        MIN BOOLEAN,
        SCAM BOOLEAN,
        HAS_LINK BOOLEAN,
        HAS_GEO BOOLEAN,
        SLOW_MODE_ENABLED BOOLEAN,
        CALL_ACTIVE BOOLEAN,
        CALL_NOT_EMPTY BOOLEAN,
        FAKE BOOLEAN,
        GIGA_GROUP BOOLEAN,
        NO_FORWARDS BOOLEAN,
        JOIN_TO_SEND BOOLEAN,
        JOIN_REQUEST BOOLEAN,
        ACCESS_HASH BIGINT,
        USERNAME VARCHAR(255),
        INSERTED_AT VARCHAR(50),
        FOREIGN KEY(CLIENT_ID) REFERENCES Client_Information(ID)
    );
"""

create_user_information_table = """
    CREATE TABLE IF NOT EXISTS User_Information (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

        USER_ID INTEGER NOT NULL,
        IS_SELF BOOLEAN,
        CONTRACT BOOLEAN,
        MUTUAL_CONTRACT BOOLEAN,
        DELETED BOOLEAN,
        BOT BOOLEAN,
        BOT_CHAT_HISTORY BOOLEAN,
        BOT_NO_CHATS BOOLEAN,
        VERIFIED BOOLEAN,
        RESTRICTED BOOLEAN,
        MIN BOOLEAN,
        BOT_INLINE_GEO BOOLEAN,
        SUPPORT BOOLEAN,
        SCAM BOOLEAN,
        APPLY_MIN_PHOTO BOOLEAN,
        FAKE BOOLEAN,
        BOT_ATTACH_MENU BOOLEAN,
        PREMIUM BOOLEAN,
        ATTACH_MENU_ENABLED BOOLEAN,

        ACCESS_HASH BIGINT NOT NULL,
        FIRST_NAME VARCHAR(255),
        LAST_NAME VARCHAR(255),
        USERNAME VARCHAR(255),
        PHONE VARCHAR(100),

        GROUP_ID INTEGER,
        CLIENT_ID INTEGER,
        FOREIGN KEY(CLIENT_ID) REFERENCES Client_Information(ID),
        FOREIGN KEY(GROUP_ID) REFERENCES Group_Information(ID)
    );
"""

is_exists_in_client_information = """
    SELECT COUNT(ID) 
    FROM Client_Information 
    WHERE (USER_ID, TELETHON_SESSION_STRING)=(?, ?);
"""

get_client_id_from_client_information_table = """
    SELECT ID 
    FROM Client_Information 
    WHERE (USER_ID, TELETHON_SESSION_STRING)=(?, ?);
"""

get_group_id_from_group_information_table = """
    SELECT ID
    FROM Group_Information
    WHERE (Group_ID, Client_ID, INSERTED_AT)=(?, ?, ?)
"""

is_exists_in_user_information = """
    SELECT COUNT(ID)
    FROM User_Information 
    WHERE (USER_ID, GROUP_ID, CLIENT_ID)=(?, ?, ?);
"""

insert_client = """
    INSERT INTO Client_Information (
        USER_ID,
        IS_SELF,
        CONTRACT,
        MUTUAL_CONTRACT,
        DELETED,
        BOT,
        BOT_CHAT_HISTORY,
        BOT_NO_CHATS,
        VERIFIED,
        RESTRICTED,
        MIN,
        BOT_INLINE_GEO,
        SUPPORT,
        SCAM,
        APPLY_MIN_PHOTO,
        FAKE,
        BOT_ATTACH_MENU,
        PREMIUM,
        ATTACH_MENU_ENABLED,

        ACCESS_HASH,
        FIRST_NAME,
        LAST_NAME,
        USERNAME,
        PHONE,

        DC_ID,
        SERVER_ADDRESS,
        PORT,
        AUTH_KEY,
        TELETHON_SESSION_STRING
    ) VALUES (
        :user_id,
        :is_self,
        :contract,
        :mutual_contract,
        :deleted,
        :bot,
        :bot_chat_history,
        :bot_no_chats,
        :verified,
        :restricted,
        :min,
        :bot_inline_geo,
        :support,
        :scam,
        :apply_min_photo,
        :fake,
        :bot_attach_menu,
        :premium,
        :attach_menu_enabled,

        :access_hash,
        :first_name,
        :last_name,
        :username,
        :phone,

        :dc_id,
        :server_address,
        :port,
        :auth_key,
        :telethon_session_string
    );
"""

insert_group = """
    INSERT INTO Group_Information (
        GROUP_ID,
        CLIENT_ID,
        TITLE,
        CREATION_DATETIME,
        CREATOR,
        LEFT,
        BROADCAST,
        VERIFIED,
        MEGA_GROUP,
        RESTRICTED,
        SIGNATURES,
        MIN,
        SCAM,
        HAS_LINK,
        HAS_GEO,
        SLOW_MODE_ENABLED,
        CALL_ACTIVE,
        CALL_NOT_EMPTY,
        FAKE,
        GIGA_GROUP,
        NO_FORWARDS,
        JOIN_TO_SEND,
        JOIN_REQUEST,
        ACCESS_HASH,
        USERNAME,
        INSERTED_AT
    ) VALUES (
        :group_id,
        :client_id,
        :title,
        :creation_datetime,
        :creator,
        :left,
        :broadcast,
        :verified,
        :mega_group,
        :restricted,
        :signatures,
        :min,
        :scam,
        :has_link,
        :has_geo,
        :slow_mode_enabled,
        :call_active,
        :call_not_empty,
        :fake,
        :giga_group,
        :no_forwards,
        :join_to_send,
        :join_request,
        :access_hash,
        :username,
        :inserted_at
    );
"""

insert_user = """
    INSERT INTO User_Information (
        USER_ID,
        IS_SELF,
        CONTRACT,
        MUTUAL_CONTRACT,
        DELETED,
        BOT,
        BOT_CHAT_HISTORY,
        BOT_NO_CHATS,
        VERIFIED,
        RESTRICTED,
        MIN,
        BOT_INLINE_GEO,
        SUPPORT,
        SCAM,
        APPLY_MIN_PHOTO,
        FAKE,
        BOT_ATTACH_MENU,
        PREMIUM,
        ATTACH_MENU_ENABLED,

        ACCESS_HASH,
        FIRST_NAME,
        LAST_NAME,
        USERNAME,
        PHONE,

        GROUP_ID,
        CLIENT_ID
    ) VALUES (
        :user_id,
        :is_self,
        :contract,
        :mutual_contract,
        :deleted,
        :bot,
        :bot_chat_history,
        :bot_no_chats,
        :verified,
        :restricted,
        :min,
        :bot_inline_geo,
        :support,
        :scam,
        :apply_min_photo,
        :fake,
        :bot_attach_menu,
        :premium,
        :attach_menu_enabled,
        :access_hash,
        :first_name,
        :last_name,
        :user_name,
        :phone,
        :group_id,
        :client_id
    );
"""