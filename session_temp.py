import struct
import base64
import ipaddress

"""
    Class SessionValues
    This class can take many arguments from existing session files.
    Mainly, targeted session file is Telethon session file and pyrogram session file

    1. Telethon session file return 5 values from session table:
        * dc_id (integer)
        * server_address (it is ip address but type is string)
        * port (port number and type is integer)
        * auth_key (authorization key, type is bytes)
        * takeout_id (most of the time it is None and it is not necessary)

    2. Pyrogram session file return 7 values from session table:
        * dc_id (integer)
        * api_id (api id inputted from the user type is integer)
        * test_mode (it represent that this application is created for testing purpose or not. It is return integer 
            value {0, 1} that means {True, False})
        * auth_key (authorization key, type is bytes)
        * date (it is return creation date and it is not necessary)
        * user_id (return the user's telegram profile userid and type is integer)
        * is_bot (it represent that this client is bot or not. It is return integer value {0, 1} that means {True, False
        })
"""


class SessionValues:
    def __init__(
            self,
            dc_id: int = None,
            test_mode: int = None,
            server_address: str = None,
            auth_key: bytes = None,
            port: int = None,
            user_id: int = None,
            is_bot: int = None
    ):
        """
        SessionValues Class params docs
        :param dc_id: integer value get from telethon session file as well as pyrogram session file.
               dc_id value can be only (1, 2, 3, 4, 5, 121),
        :param test_mode: integer value get from only pyrogram session file.,
        :param server_address: string value get from telethon session file only.,
        :param auth_key: bytes value get from telethon and pyrogram both of them. it is required.,
        :param port: integer value get from telethon session file only.,
        :param user_id: integer value get from pyrogram session file only.,
        :param is_bot: integer value get from pyrogram session file only.
        """

        self._dc_id = dc_id
        self._test_mode = test_mode
        self._server_address = server_address
        self._auth_key = auth_key
        self._port = port
        self._user_id = user_id
        self._is_bot = is_bot

    @property
    def dc_id(self) -> int:
        """
        This function is created for to get value of dc_id outside this class
        :return: _dc_id value
        """
        return self._dc_id

    @property
    def test_mode(self) -> int:
        """
        This function is created for to get value of test_mode outside this class
        :return: _test_mode value
        """
        return self._test_mode

    @property
    def server_address(self) -> str:
        """
        This function is created for to get value of server_address outside this class
        Here have two different variant such as Test and Production
        if test_mode is 1 (True) then it will be Test otherwise Production
        also, Here have few constant ip address depended on dc_id that will not change in the future.
        :return: _server_address value
        """

        if self._server_address is None and self.test_mode.__eq__(1):
            match self._dc_id:
                case 1:
                    return "149.154.175.10"
                case 2:
                    return "149.154.167.40"
                case 3:
                    return "149.154.175.117"
                case 121:
                    return "95.213.217.195"
                case _:
                    return "something else"
        elif self._server_address is None and self.test_mode.__eq__(0):
            match self._dc_id:
                case 1:
                    return "149.154.175.53"
                case 2:
                    return "149.154.167.51"
                case 3:
                    return "149.154.175.100"
                case 4:
                    return "149.154.167.91"
                case 5:
                    return "91.108.56.130"
                case 121:
                    return "95.213.217.195"
                case _:
                    return "something else"
        elif self._server_address is not None:
            return self._server_address
        else:
            pass

    @property
    def auth_key(self) -> bytes:
        """
        This function is created for to get value of auth_key outside this class
        remember one thing: This value will not change in the future. It should exactly as it is.
        :return: _auth_key value
        """
        return self._auth_key

    @property
    def port(self) -> int:
        """
        This function is created for to get value of _port outside this class
        Here have two different factor. Depending on that value can change.

        1. if port is None and test mode is not None then port will be 80
        2. otherwise port will be 443

        :return: _port value
        """
        if self._port is None and self.test_mode is not None:
            return 80
        elif self._port is None and self.test_mode is None:
            return 443
        else:
            return self._port

    @property
    def user_id(self) -> int:
        """
        This function is created for to get value of user_id outside this class
        :return: _user_id value
        """
        return self._user_id

    @property
    def is_bot(self) -> int:
        """
        This function is created for to get value of is_bot outside this class
        :return: _is_bot value
        """
        return self._is_bot

    def generate_telethon_session_string(self) -> str:
        """
        This function is created for return Session string for Telethon package.

        ip_address = packed version of ipaddress.ip_address()

        telethon_session_string_format = Sting format of Telethon session string. >B{length of ip address}sH{length of
                                         auth key}s -> >B4sH256s

        packed = struct.pack() with few values
                1. telethon_session_string_format
                2. value of dc_id
                3. value of ip_address
                4. value of port number
                5. value of auth key

        finally, session_string = base64.urlsafe_base64encode(packed) with "1" addon. Because this format is acceptable
                                                                                                            by telethon.
                                        .decode("ascii")

        /*
        Sample Value
        1BVtsOL4BuwV3tnXgeFITj4fancy3wi4S2JnRvmrcQeeZtQVliXj6H-24FSkFCocoaSCDeGL5bvo-aiff7U21Vq_51p6sPendLA6WBwf_r9L_t0=
        */

        :return: session_string
        """

        ip_address = ipaddress.ip_address(self.server_address).packed

        telethon_session_string_format = f">B{len(ip_address)}sH{len(self.auth_key)}s"

        packed = struct.pack(
            telethon_session_string_format,
            self.dc_id,
            ip_address,
            self.port,
            self.auth_key
        )
        session_string = "1" + base64.urlsafe_b64encode(packed).decode("ascii")

        return session_string
