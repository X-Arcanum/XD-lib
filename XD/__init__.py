import requests
import asyncio
import logging
import json
from functools import wraps
from .exceptions import UnAuthorizedBotToken, UnKnownError, ChatNotFound, ConversationTimeOut
from datetime import datetime

class TelegramMessage:
    def __init__(self, message_data, bot):
        self.data = message_data
        self.message_id = message_data.get('message_id', 0)
        self.date = self.format_date(message_data.get('date', 0))
        self.chat = self.Chat(message_data.get('chat', {}))
        self.from_user = self.FromUser(message_data.get('from', {}))
        self.text = message_data.get('text', '')
        self.entities = message_data.get('entities', [])
        self.command = message_data.get('command', [])
        self.bot = bot
        self.message = self.pretty_print()

    def format_date(self, timestamp):
        if timestamp:
            return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return None

    class Chat:
        def __init__(self, chat_data):
            self.id = chat_data.get('id', 0)
            self.type = chat_data.get('type', '')
            self.title = chat_data.get('title', '')
            self.username = chat_data.get('username', '')
            self.is_verified = chat_data.get('is_verified', False)
            self.is_restricted = chat_data.get('is_restricted', False)
            self.is_creator = chat_data.get('is_creator', False)
            self.is_scam = chat_data.get('is_scam', False)
            self.is_fake = chat_data.get('is_fake', False)
            self.has_protected_content = chat_data.get('has_protected_content', False)
            self.permissions = self.ChatPermissions(chat_data.get('permissions', {}))

        class ChatPermissions:
            def __init__(self, permissions_data):
                self.can_send_messages = permissions_data.get('can_send_messages', False)
                self.can_send_media_messages = permissions_data.get('can_send_media_messages', False)
                self.can_send_other_messages = permissions_data.get('can_send_other_messages', False)
                self.can_send_polls = permissions_data.get('can_send_polls', False)
                self.can_add_web_page_previews = permissions_data.get('can_add_web_page_previews', False)
                self.can_change_info = permissions_data.get('can_change_info', False)
                self.can_invite_users = permissions_data.get('can_invite_users', False)
                self.can_pin_messages = permissions_data.get('can_pin_messages', False)

    class FromUser:
        def __init__(self, from_data):
            self.id = from_data.get('id', 0)
            self.first_name = from_data.get('first_name', '')
            self.last_name = from_data.get('last_name', '')
            self.username = from_data.get('username', '')
            self.is_bot = from_data.get('is_bot', False)
            self.is_premium = from_data.get('is_premium', False)
            self.language_code = from_data.get('language_code', '')
            self.is_self = from_data.get('is_self', False)
            self.is_contact = from_data.get('is_contact', False)
            self.is_mutual_contact = from_data.get('is_mutual_contact', False)
            self.is_deleted = from_data.get('is_deleted', False)
            self.is_verified = from_data.get('is_verified', False)
            self.is_restricted = from_data.get('is_restricted', False)
            self.is_scam = from_data.get('is_scam', False)
            self.is_fake = from_data.get('is_fake', False)
            self.is_support = from_data.get('is_support', False)
            self.status = from_data.get('status', '')
            self.emoji_status = self.EmojiStatus(from_data.get('emoji_status', {}))
            self.dc_id = from_data.get('dc_id', 0)
            self.photo = self.ChatPhoto(from_data.get('photo', {}))

        class EmojiStatus:
            def __init__(self, emoji_status_data):
                self.custom_emoji_id = emoji_status_data.get('custom_emoji_id', '')

        class ChatPhoto:
            def __init__(self, photo_data):
                self.small_file_id = photo_data.get('small_file_id', '')
                self.small_photo_unique_id = photo_data.get('small_photo_unique_id', '')
                self.big_file_id = photo_data.get('big_file_id', '')
                self.big_photo_unique_id = photo_data.get('big_photo_unique_id', '')

    def pretty_print(self):
        return {
            'message_id': self.message_id,
            'date': self.date,
            'chat': {
                'id': self.chat.id,
                'type': self.chat.type,
                'title': self.chat.title,
                'username': self.chat.username,
                'is_verified': self.chat.is_verified,
                'is_restricted': self.chat.is_restricted,
                'is_creator': self.chat.is_creator,
                'is_scam': self.chat.is_scam,
                'is_fake': self.chat.is_fake,
                'has_protected_content': self.chat.has_protected_content,
                'permissions': {
                    'can_send_messages': self.chat.permissions.can_send_messages,
                    'can_send_media_messages': self.chat.permissions.can_send_media_messages,
                    'can_send_other_messages': self.chat.permissions.can_send_other_messages,
                    'can_send_polls': self.chat.permissions.can_send_polls,
                    'can_add_web_page_previews': self.chat.permissions.can_add_web_page_previews,
                    'can_change_info': self.chat.permissions.can_change_info,
                    'can_invite_users': self.chat.permissions.can_invite_users,
                    'can_pin_messages': self.chat.permissions.can_pin_messages,
                },
            },
            'from_user': {
                'id': self.from_user.id,
                'first_name': self.from_user.first_name,
                'last_name': self.from_user.last_name,
                'username': self.from_user.username,
                'is_bot': self.from_user.is_bot,
                'is_premium': self.from_user.is_premium,
                'language_code': self.from_user.language_code,
                'is_self': self.from_user.is_self,
                'is_contact': self.from_user.is_contact,
                'is_mutual_contact': self.from_user.is_mutual_contact,
                'is_deleted': self.from_user.is_deleted,
                'is_verified': self.from_user.is_verified,
                'is_restricted': self.from_user.is_restricted,
                'is_scam': self.from_user.is_scam,
                'is_fake': self.from_user.is_fake,
                'is_support': self.from_user.is_support,
                'status': self.from_user.status,
                'emoji_status': {
                    'custom_emoji_id': self.from_user.emoji_status.custom_emoji_id,
                },
                'dc_id': self.from_user.dc_id,
                'photo': {
                    'small_file_id': self.from_user.photo.small_file_id,
                    'small_photo_unique_id': self.from_user.photo.small_photo_unique_id,
                    'big_file_id': self.from_user.photo.big_file_id,
                    'big_photo_unique_id': self.from_user.photo.big_photo_unique_id,
                },
            },
            'text': self.text,
            'entities': self.entities,
            'command': self.command,
            'mentioned': self.data.get('mentioned', False),
            'scheduled': self.data.get('scheduled', False),
            'from_scheduled': self.data.get('from_scheduled', False),
            'has_protected_content': self.data.get('has_protected_content', False),
            'outgoing': self.data.get('outgoing', False),
        }


    async def reply_text(self, text, parse_mode='MARKDOWN'):
        """
        Send a text message as a reply to the current message.

        Parameters:
        text (str): The text to send.
        parse_mode (str): The mode in which the text should be parsed. Default is 'MARKDOWN'.

        Returns:
        dict: The response from the Telegram API, containing information about the sent message.

        Raises:
        Exception: If there is an error sending the message.
        """
        return await self.bot.send_message(self.chat.id, text, parse_mode, self.message_id)

    async def reply_photo(self, photo, caption=None):
        """
        Send a photo as a reply to the current message.

        Parameters:
        photo (file-like object or str): The photo to send. If a string is provided, it should be the file path.
        caption (str, optional): The caption for the photo. Default is None.

        Returns:
        dict: The response from the Telegram API, containing information about the sent photo.

        Raises:
        Exception: If there is an error sending the photo.
        """
        return await self.bot.send_photo(self.chat.id, photo, caption, self.message_id)
    
    async def reply_audio(self, audio):
        """
        Send an audio file as a reply to the current message.

        Parameters:
        audio (file-like object or str): The audio file to send. If a string is provided, it should be the file path.

        Returns:
        dict: The response from the Telegram API, containing information about the sent audio.

        Raises:
        Exception: If there is an error sending the audio.

        Note:
        This method uses the `send_audio` method of the `bot` instance to send the audio.
        The `chat.id` and `message_id` of the current message are used as parameters for the `send_audio` method.
        """
        return await self.bot.send_audio(self.chat.id, audio, self.message_id)

    async def reply_document(self, document):
        """
        Send a document as a reply to the current message.

        Parameters:
        document (file-like object or str): The document to send. If a string is provided, it should be the file path.

        Returns:
        dict: The response from the Telegram API, containing information about the sent document.

        Raises:
        Exception: If there is an error sending the document.

        Note:
        This method uses the `send_document` method of the `bot` instance to send the document.
        The `chat.id` and `message_id` of the current message are used as parameters for the `send_document` method.
        """
        return await self.bot.send_document(self.chat.id, document, self.message_id)

    async def reply_video(self, video):
        """
        Send a video as a reply to the current message.

        Parameters:
        video (file-like object or str): The video to send. If a string is provided, it should be the file path.

        Returns:
        dict: The response from the Telegram API, containing information about the sent video.

        Raises:
        Exception: If there is an error sending the video.

        Note:
        This method uses the `send_video` method of the `bot` instance to send the video.
        The `chat.id` and `message_id` of the current message are used as parameters for the `send_video` method.
        """
        return await self.bot.send_video(self.chat.id, video, self.message_id)

    async def reply_voice(self, voice):
        """
        Send a voice message as a reply to the current message.

        Parameters:
        voice (file-like object or str): The voice message to send. If a string is provided, it should be the file path.

        Returns:
        dict: The response from the Telegram API, containing information about the sent voice message.

        Raises:
        Exception: If there is an error sending the voice message.

        Note:
        This method uses the `send_voice` method of the `bot` instance to send the voice message.
        The `chat.id` and `message_id` of the current message are used as parameters for the `send_voice` method.
        """
        return await self.bot.send_voice(self.chat.id, voice, self.message_id) 

class Client:
    def __init__(self, token):
        """
        Initialize a new instance of the Client class.

        Parameters:
        token (str): The bot token for authenticating with the Telegram API.

        Raises:
        ValueError: If the provided token is not 46 characters long.

        Attributes:
        token (str): The bot token.
        base_url (str): The base URL for making API requests.
        logger (logging.Logger): The logger for logging messages.
        _message_handlers (dict): A dictionary to store message handlers.
        session (requests.Session): The session for making HTTP requests.
        """
        if len(token) != 46:
            raise ValueError("Invalid bot token length. Bot token must be 46 characters long.")
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self._message_handlers = {}
        self.session = requests.Session()

    def _setup_logging(self):
        """
        Initialize and configure the logging system for the Client class.

        This method sets up a StreamHandler to log messages to the console,
        and configures the logging format and level.

        Parameters:
        None

        Returns:
        None

        Raises:
        None
        """
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def validate_token(self):
        """
        Validates the bot token by making a GET request to the Telegram API's getMe endpoint.

        Parameters:
        None

        Returns:
        bool: True if the token is valid, False otherwise.

        Raises:
        UnAuthorizedBotToken: If the token is not authorized.
        UnKnownError: If an unknown error occurs while validating the token.

        Note:
        This method logs the validation result using the logger instance.
        """
        try:
            response = self.session.get(f"{self.base_url}/getMe")
            if response.status_code == 200:
                bot_info = response.json()['result']
                self.logger.info("Bot token is valid.")
                return True
            elif response.status_code == 401:
                raise UnAuthorizedBotToken(self.token)
            else:
                raise UnKnownError(response.status_code)
        except Exception as e:
            self.logger.error(f"Exception occurred while validating bot token: {e}")
            return False

    async def _send_request(self, method, data, files=None):
        """
        Send a POST request to the Telegram API with the specified method, data, and files.

        Parameters:
        method (str): The Telegram API method to call.
        data (dict): The data to send in the request body.
        files (dict, optional): The files to send in the request. Default is None.

        Returns:
        dict: The JSON response from the Telegram API. If the request fails or encounters an error, returns None.

        Raises:
        Exception: If an exception occurs while sending the request.

        Note:
        This method logs the request details, response status code, and response text using the logger instance.
        """
        try:
            response = requests.post(f"{self.base_url}/{method}", data=data, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to send {method} request. Status code: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Exception occurred while sending {method} request: {e}")
            return None

    async def send_message(self, chat_id, text, parse_mode='MARKDOWN', reply_to_message_id=None):
        """
        Send a text message to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        text (str): The text content of the message.
        parse_mode (str, optional): The mode in which the text should be parsed. Default is 'MARKDOWN'.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent message.

        Raises:
        Exception: If there is an error sending the message.

        Note:
        This method uses the 'sendMessage' method of the Telegram API to send the message.
        The 'chat_id', 'text', 'parse_mode', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendMessage', data)

    async def send_audio(self, chat_id, audio, reply_to_message_id=None):
        """
        Send an audio file to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        audio (file-like object or str): The audio file to send. If a string is provided, it should be the file path.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent audio.

        Raises:
        Exception: If there is an error sending the audio.

        Note:
        This method uses the 'sendAudio' method of the Telegram API to send the audio.
        The 'chat_id', 'audio', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id}
        files = {'audio': audio}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendAudio', data, files)

    async def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None):
        """
        Send a photo file to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        photo (file-like object or str): The photo file to send. If a string is provided, it should be the file path.
        caption (str, optional): The caption for the photo. Default is None.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent photo.

        Raises:
        Exception: If there is an error sending the photo.

        Note:
        This method uses the 'sendPhoto' method of the Telegram API to send the photo.
        The 'chat_id', 'photo', 'caption', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        files = {'photo': photo}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendPhoto', data, files)

    async def send_document(self, chat_id, document, reply_to_message_id=None):
        """
        Send a document file to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        document (file-like object or str): The document file to send. If a string is provided, it should be the file path.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent document.

        Raises:
        Exception: If there is an error sending the document.

        Note:
        This method uses the 'sendDocument' method of the Telegram API to send the document.
        The 'chat_id', 'document', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id}
        files = {'document': document}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendDocument', data, files)

    async def send_video(self, chat_id, video, reply_to_message_id=None):
        """
        Send a video file to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        video (file-like object or str): The video file to send. If a string is provided, it should be the file path.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent video.

        Raises:
        Exception: If there is an error sending the video.

        Note:
        This method uses the 'sendVideo' method of the Telegram API to send the video.
        The 'chat_id', 'video', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id}
        files = {'video': video}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendVideo', data, files)

    async def send_voice(self, chat_id, voice, reply_to_message_id=None):
        """
        Send a voice message to a specified chat.

        Parameters:
        chat_id (int): The unique identifier for the target chat.
        voice (file-like object or str): The voice message to send. If a string is provided, it should be the file path.
        reply_to_message_id (int, optional): The unique identifier of the message to reply to. Default is None.

        Returns:
        dict: The JSON response from the Telegram API, containing information about the sent voice message.

        Raises:
        Exception: If there is an error sending the voice message.

        Note:
        This method uses the 'sendVoice' method of the Telegram API to send the voice message.
        The 'chat_id', 'voice', and 'reply_to_message_id' parameters are used as data for the request.
        """
        data = {'chat_id': chat_id}
        files = {'voice': voice}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendVoice', data, files)

    def on_message(self, command):
        """
        Decorator function to register a message handler for a specific command.

        Parameters:
        command (str): The command for which the handler should be registered.

        Returns:
        decorator: A decorator function that can be used to register a message handler.
        """
        def decorator(func):
            """
            Decorator function to register a message handler for a specific command.

            Parameters:
            func (function): The function to be registered as the message handler.

            Returns:
            wrapper: A wrapper function that can be called to handle the message.
            """
            self._message_handlers[command] = func
            @wraps(func)
            async def wrapper(message):
                """
                Wrapper function to handle the message.

                Parameters:
                message (TelegramMessage): The message to be handled.

                Returns:
                None
                """
                await func(message)
            return wrapper
        return decorator

    async def _handle_update(self, update):
        """
        Handle an incoming update by checking if it contains a message and
        invoking the appropriate message handler.

        Parameters:
        update (dict): The incoming update from the Telegram API.

        Returns:
        None

        Raises:
        None
        """
        if 'message' in update:
            message = TelegramMessage(update['message'], self)
            if message.text:
                command = message.text.split()[0]
                if command in self._message_handlers:
                    await self._message_handlers[command](message)

    async def start(self):
        """
        Start the bot and begin processing incoming updates.

        This method continuously fetches updates from the Telegram API,
        processes them, and invokes the appropriate message handlers.

        Parameters:
        None

        Returns:
        None

        Raises:
        None
        """
        if not self.validate_token():
            self.logger.error("Bot token is invalid. Exiting...")
            return

        self.logger.info("Bot started.")
        offset = None
        while True:
            updates = await self.get_updates(offset)
            if updates:
                for update in updates:
                    await self._handle_update(update)
                    offset = update['update_id'] + 1

    def extract_reply_json(self, update):
            """
            Extracts the reply message from the given update and returns it as a JSON string.

            Parameters:
            update (dict): The update received from the Telegram API. It should contain a 'message' key.

            Returns:
            str: The reply message as a JSON string, or a descriptive message if the update does not contain a reply message.

            Raises:
            None
            """
            if 'message' in update:
                message = update['message']
                if 'reply_to_message' in message:
                    reply = message['reply_to_message']
                    reply_json = json.dumps(reply, indent=2)
                    return reply_json
                else:
                    return "Not a reply message."
            else:
                return "Invalid update format."

    async def get_updates(self, offset=None):
        """
        Fetch updates from the Telegram API.

        Parameters:
        offset (int, optional): The offset from which to fetch updates. Default is None.

        Returns:
        list: A list of updates received from the Telegram API.

        Raises:
        Exception: If an exception occurs while fetching updates.

        Note:
        This method makes a GET request to the Telegram API's getUpdates endpoint.
        It logs the status code and any exceptions that occur during the request.
        """
        params = {'timeout': 100, 'offset': offset}
        try:
            response = self.session.get(f"{self.base_url}/getUpdates", params=params)
            if response.status_code == 200:
                updates = response.json()['result']
                return updates
            else:
                self.logger.error(f"Failed to get updates. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Exception occurred while getting updates: {e}")
            return None

